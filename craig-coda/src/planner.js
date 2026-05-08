/**
 * CODA - Planner
 *
 * Builds a consolidation plan from the last audit manifest.
 * Directly maps the planning.js logic from the warehouse app:
 *
 *   candidatePriorityTuple:
 *     1. Emptied bins first    → merge duplicate fragments first
 *     2. Source quality        → Craig-authored > donor-derived
 *     3. Move count            → fewest operations to consolidated state
 *     4. Leftover              → minimize orphaned fragments post-consolidation
 *
 * chooseBestNonEmptyPlan → find existing structure to merge INTO
 * chooseBestEmptyPackPlan → find empty space to pack multiple fragments together
 *
 * The plan is written to consolidation.plan.json.
 * executor.js reads the plan and acts on it.
 */

import fs   from 'fs/promises';
import path from 'path';
import {
  AUDIT_MANIFEST, PLAN_FILE, PRUNE_ORDER, STORAGE_LIMIT_BYTES,
} from './config.js';
import { runSkeptic } from './skeptic.js';
import { logEntry } from './logger.js';

// ── Priority tuple comparator (lower = higher priority to prune) ──────────────
// Maps PRUNE_ORDER classification → numeric priority
function classificationPriority(c) {
  const idx = PRUNE_ORDER.indexOf(c);
  return idx === -1 ? PRUNE_ORDER.length : idx;
}

// ── candidatePriorityTuple ─────────────────────────────────────────────────────
// Returns a tuple used for sorting: [prune_order, -relevance, size_desc]
// Lower tuple = higher prune priority
function candidatePriorityTuple(entry) {
  const order    = classificationPriority(entry.classification);
  const quality  = -entry.relevance;          // lower relevance → prune sooner
  const moves    = entry.size;                // larger files → more bytes freed per prune
  const leftover = entry.redundancy;          // higher redundancy → safe to prune
  return [order, quality, -moves, -leftover];
}

function tupleCompare(a, b) {
  const ta = candidatePriorityTuple(a);
  const tb = candidatePriorityTuple(b);
  for (let i = 0; i < ta.length; i++) {
    if (ta[i] < tb[i]) return -1;
    if (ta[i] > tb[i]) return  1;
  }
  return 0;
}

// ── chooseBestNonEmptyPlan ─────────────────────────────────────────────────────
// Find the best consolidation target to MERGE duplicates into.
// Prefers the highest-relevance copy, Craig-authored directory signals, .md/.js exts.
function chooseBestNonEmptyPlan(group) {
  return group.slice().sort((a, b) => {
    const aScore = a.relevance + (a.path.includes('craig') || a.path.includes('vault') ? 0.2 : 0);
    const bScore = b.relevance + (b.path.includes('craig') || b.path.includes('vault') ? 0.2 : 0);
    return bScore - aScore;
  })[0];
}

// ── chooseBestEmptyPackPlan ────────────────────────────────────────────────────
// Find the best target directory to pack multiple orphan fragments into.
// Prefers directories with existing high-relevance content.
function chooseBestEmptyPackPlan(orphans, allEntries) {
  const dirScores = new Map();
  for (const e of allEntries) {
    const d = path.dirname(e.path);
    dirScores.set(d, Math.max(dirScores.get(d) || 0, e.relevance));
  }
  // Return the directory that already has the most relevant content
  let best = null, bestScore = -1;
  for (const [dir, score] of dirScores) {
    if (score > bestScore) { best = dir; bestScore = score; }
  }
  return best;
}

// ── Build plan ────────────────────────────────────────────────────────────────
export async function runPlan(dryRun = false) {
  console.log('\n📐 CODA Planner - building consolidation plan');

  let manifest;
  try {
    manifest = JSON.parse(await fs.readFile(AUDIT_MANIFEST, 'utf8'));
  } catch {
    console.error('  ✗ No audit manifest found. Run: coda audit');
    process.exit(1);
  }

  const entries = manifest.entries;

  // Run skeptic pass on contested entries and update classifications
  const contestedResolved = runSkeptic(entries);
  for (const r of contestedResolved) {
    const idx = entries.findIndex(e => e.path === r.path);
    if (idx !== -1) {
      entries[idx] = {
        ...entries[idx],
        secondPassScore: r.secondPassScore,
        verdict: r.verdict,
        classification: r.verdict === 'cleared' ? 'contested-cleared'
                       : r.verdict === 'held'   ? 'normal'          // promoted to safe
                       : 'contested',           // stays for manual review
      };
    }
  }

  // Sort all entries by prune priority
  const pruneQueue = entries
    .filter(e => e.classification !== 'normal' && e.verdict !== 'manual-review')
    .sort(tupleCompare);

  // Calculate bytes currently used and bytes to free
  const currentBytes = manifest.totalBytes;
  const bytesToFree  = Math.max(0, currentBytes - STORAGE_LIMIT_BYTES);
  let bytesPlanned   = 0;

  const actions = [];

  // Duplicate groups → merge
  const dupEntries = entries.filter(e => e.classification === 'vault-duplicate');
  const groupMap   = new Map();
  for (const e of dupEntries) {
    // Group by content similarity (use first 3 dirs of path as proxy group key)
    const key = path.dirname(e.path).split(path.sep).slice(-3).join('/');
    if (!groupMap.has(key)) groupMap.set(key, []);
    groupMap.get(key).push(e);
  }
  for (const [, group] of groupMap) {
    if (group.length < 2) continue;
    const keep    = chooseBestNonEmptyPlan(group);
    const discard = group.filter(e => e.path !== keep.path);
    for (const d of discard) {
      actions.push({ action: 'delete', reason: 'vault-duplicate', path: d.path, bytesFreed: d.size, keep: keep.path });
      bytesPlanned += d.size;
    }
  }

  // Orphan scaffolding → delete
  for (const e of pruneQueue.filter(e => e.classification === 'orphan-scaffolding' || (e.classification === 'orphan-candidate' && e.relevance < 0.05))) {
    actions.push({ action: 'delete', reason: 'orphan-scaffolding', path: e.path, bytesFreed: e.size });
    bytesPlanned += e.size;
  }

  // Remaining orphans → try to pack into high-relevance directory
  const remainingOrphans = pruneQueue.filter(e => e.classification === 'orphan-candidate');
  if (remainingOrphans.length > 0) {
    const packTarget = chooseBestEmptyPackPlan(remainingOrphans, entries);
    for (const e of remainingOrphans) {
      const dest = path.join(packTarget, path.basename(e.path));
      if (dest !== e.path) {
        actions.push({ action: 'move', reason: 'consolidate-orphan', path: e.path, dest, bytesFreed: 0 });
      }
    }
  }

  // Donor residue → delete if cleared
  for (const e of pruneQueue.filter(e => e.classification === 'donor-residue')) {
    actions.push({ action: 'delete', reason: 'donor-residue', path: e.path, bytesFreed: e.size });
    bytesPlanned += e.size;
  }

  // Low-centrality lore → delete
  for (const e of pruneQueue.filter(e => e.classification === 'low-centrality-lore')) {
    actions.push({ action: 'delete', reason: 'low-centrality-lore', path: e.path, bytesFreed: e.size });
    bytesPlanned += e.size;
  }

  // coda-bootstrap → delete LAST (only if graduation is confirmed)
  for (const e of entries.filter(e => e.classification === 'coda-bootstrap')) {
    actions.push({ action: 'delete-on-graduation', reason: 'coda-bootstrap', path: e.path, bytesFreed: e.size });
  }

  const manualReview = entries.filter(e => e.verdict === 'manual-review');

  const plan = {
    generated:       new Date().toISOString(),
    currentBytes,
    currentGB:       parseFloat((currentBytes / 1e9).toFixed(3)),
    limitGB:         parseFloat((STORAGE_LIMIT_BYTES / 1e9).toFixed(3)),
    bytesToFree,
    bytesPlannedToFree: bytesPlanned,
    projectedGB:     parseFloat(((currentBytes - bytesPlanned) / 1e9).toFixed(3)),
    actionCount:     actions.length,
    manualReviewCount: manualReview.length,
    manualReview:    manualReview.map(e => ({ path: e.path, score: e.secondPassScore })),
    actions,
  };

  if (!dryRun) {
    await fs.writeFile(PLAN_FILE, JSON.stringify(plan, null, 2));
    await logEntry('plan', `${actions.length} actions planned, ${(bytesPlanned / 1e9).toFixed(3)} GB to free, ${manualReview.length} manual review`);
  }

  console.log('\n📋 Plan summary');
  console.log(`   Current:    ${plan.currentGB} GB`);
  console.log(`   To free:    ${(bytesPlanned / 1e9).toFixed(3)} GB`);
  console.log(`   Projected:  ${plan.projectedGB} GB`);
  console.log(`   Actions:    ${actions.length}`);
  console.log(`   Manual:     ${manualReview.length} files need human review`);
  if (!dryRun) console.log(`   Plan →      ${PLAN_FILE}`);
  console.log();

  if (manualReview.length > 0) {
    console.log('⚠️  Manual review required for:');
    for (const r of manualReview) {
      console.log(`   ${r.score.toFixed(3)}  ${r.path}`);
    }
    console.log();
  }

  return plan;
}
