/**
 * CODA - Status
 *
 * Shows current state: storage used, audit age, plan readiness,
 * contested file count, graduation readiness indicator.
 */

import fs   from 'fs/promises';
import path from 'path';
import { AUDIT_MANIFEST, PLAN_FILE, STORAGE_LIMIT_BYTES } from './config.js';

function age(isoStr) {
  const ms   = Date.now() - new Date(isoStr).getTime();
  const mins = Math.floor(ms / 60000);
  if (mins < 60)    return `${mins}m ago`;
  if (mins < 1440)  return `${Math.floor(mins/60)}h ago`;
  return `${Math.floor(mins/1440)}d ago`;
}

export async function runStatus() {
  console.log('\n📊 CODA Status\n');

  let manifest = null, plan = null;

  try { manifest = JSON.parse(await fs.readFile(AUDIT_MANIFEST, 'utf8')); } catch { /* */ }
  try { plan      = JSON.parse(await fs.readFile(PLAN_FILE, 'utf8')); }       catch { /* */ }

  const limitGB = (STORAGE_LIMIT_BYTES / 1e9).toFixed(0);

  if (manifest) {
    const pct = ((manifest.totalBytes / STORAGE_LIMIT_BYTES) * 100).toFixed(1);
    const bar = '█'.repeat(Math.floor(pct / 5)) + '░'.repeat(20 - Math.floor(pct / 5));
    console.log(`  Storage:     [${bar}] ${manifest.totalGB} GB / ${limitGB} GB  (${pct}%)`);
    console.log(`  Audit:       ${age(manifest.generated)}  (${manifest.totalFiles} files)`);
    console.log(`  Orphans:     ${manifest.orphanCandidates}`);
    console.log(`  Contested:   ${manifest.contested}  (awaiting skeptic pass)`);
    console.log(`  Duplicates:  ${manifest.duplicates}`);
  } else {
    console.log('  No audit manifest. Run: coda audit');
  }

  if (plan) {
    console.log(`\n  Plan:        ${age(plan.generated)}  (${plan.actionCount} actions)`);
    console.log(`  To free:     ${(plan.bytesPlannedToFree / 1e9).toFixed(3)} GB`);
    console.log(`  Projected:   ${plan.projectedGB} GB`);
    if (plan.manualReviewCount > 0) {
      console.log(`\n  ⚠️  ${plan.manualReviewCount} files require manual review before prune`);
    }
  } else {
    console.log('\n  No plan. Run: coda plan');
  }

  // Graduation readiness
  if (manifest) {
    const craigNodes = manifest.entries.filter(e =>
      ['vault', 'craig', 'confluence', 'omnimeta', 'warehouse'].some(d => e.path.toLowerCase().includes(d))
      && e.centrality > 0
    );
    console.log(`\n  Graduation:  ${craigNodes.length > 0 ? `${craigNodes.length} Craig-authored nodes indexed - run: coda graduation` : 'Not ready - no Craig-authored content'}`);
  }

  console.log();
}
