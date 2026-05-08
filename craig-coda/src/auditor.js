/**
 * CODA - Auditor
 *
 * Walks the target directory tree and scores every artifact.
 * Produces audit.manifest.json - the input to every other module.
 *
 * Scoring formula:
 *   relevance = (frequency * WEIGHT_FREQUENCY)
 *             + (centrality * WEIGHT_CENTRALITY)
 *             + (recency    * WEIGHT_RECENCY)
 *
 * All three signals are normalized 0.0-1.0 before weighting.
 *
 * Files scoring below ORPHAN_THRESHOLD are flagged as orphan candidates.
 * Files that are both high-importance and high-redundancy are flagged contested.
 */

import fs   from 'fs/promises';
import path from 'path';
import { createReadStream } from 'fs';
import {
  TARGET_DIR, AUDIT_MANIFEST, ORPHAN_THRESHOLD,
  HIGH_IMPORTANCE_THRESHOLD, HIGH_REDUNDANCY_THRESHOLD,
  WEIGHT_FREQUENCY, WEIGHT_CENTRALITY, WEIGHT_RECENCY,
  CODA_DIR,
} from './config.js';
import { logEntry } from './logger.js';

// ── Exclusions ──────────────────────────────────────────────────────────────
const SKIP_DIRS  = new Set(['node_modules', '.git', '.obsidian']);
const SKIP_EXTS  = new Set(['.DS_Store', 'Thumbs.db']);

// ── Walk ─────────────────────────────────────────────────────────────────────
async function walk(dir, files = []) {
  let entries;
  try {
    entries = await fs.readdir(dir, { withFileTypes: true });
  } catch {
    return files;
  }
  for (const e of entries) {
    if (SKIP_DIRS.has(e.name)) continue;
    const full = path.join(dir, e.name);
    if (e.isDirectory()) {
      await walk(full, files);
    } else {
      if (!SKIP_EXTS.has(path.extname(e.name))) files.push(full);
    }
  }
  return files;
}

// ── Parse wikilinks from markdown ────────────────────────────────────────────
async function extractLinks(filePath) {
  const links = [];
  const ext = path.extname(filePath).toLowerCase();
  if (!['.md', '.markdown', '.txt', '.js', '.ts', '.json'].includes(ext)) return links;
  try {
    const content = await fs.readFile(filePath, 'utf8');
    // Obsidian-style [[wikilinks]]
    const wikiRe = /\[\[([^\]]+)\]\]/g;
    let m;
    while ((m = wikiRe.exec(content)) !== null) links.push(m[1].split('|')[0].trim());
    // JS/TS imports
    const importRe = /(?:import|require)\s*(?:\(|['"])([^'")]+)(?:['"]|\))/g;
    while ((m = importRe.exec(content)) !== null) links.push(m[1]);
  } catch { /* binary or unreadable */ }
  return links;
}

// ── Build link graph ─────────────────────────────────────────────────────────
async function buildLinkGraph(files) {
  // Map: basename (no ext) → full path
  const nameMap = new Map();
  for (const f of files) {
    const base = path.basename(f, path.extname(f)).toLowerCase();
    nameMap.set(base, f);
  }

  // in-degree (how many files point TO this file)
  const inDegree = new Map(files.map(f => [f, 0]));

  for (const f of files) {
    const links = await extractLinks(f);
    for (const lnk of links) {
      const target = nameMap.get(lnk.toLowerCase());
      if (target && target !== f) {
        inDegree.set(target, (inDegree.get(target) || 0) + 1);
      }
    }
  }
  return inDegree;
}

// ── Normalize array of values to 0-1 ─────────────────────────────────────────
function normalize(map) {
  const vals = [...map.values()];
  const max  = Math.max(...vals, 1);
  return new Map([...map.entries()].map(([k, v]) => [k, v / max]));
}

// ── Build frequency proxy from mtime ─────────────────────────────────────────
// Real frequency requires an access log; without one we proxy via recency.
// A separate access-log integration (e.g. inotify / fs.watch) can replace this.
async function buildFrequencyProxy(files) {
  const map = new Map();
  const now  = Date.now();
  const YEAR = 365 * 24 * 60 * 60 * 1000;
  for (const f of files) {
    try {
      const stat = await fs.stat(f);
      const ageMs = now - stat.mtimeMs;
      // Exponential decay: files modified recently score higher
      map.set(f, Math.exp(-ageMs / YEAR));
    } catch {
      map.set(f, 0);
    }
  }
  return map;
}

// ── Build recency from mtime ──────────────────────────────────────────────────
async function buildRecency(files) {
  const map = new Map();
  for (const f of files) {
    try {
      const stat = await fs.stat(f);
      map.set(f, stat.mtimeMs);
    } catch {
      map.set(f, 0);
    }
  }
  return map;
}

// ── Detect duplicates (same content hash) ─────────────────────────────────────
async function buildDuplicateGroups(files) {
  const { createHash } = await import('node:crypto');
  const hashMap = new Map();
  for (const f of files) {
    try {
      const buf = await fs.readFile(f);
      const h   = createHash('sha256').update(buf).digest('hex').slice(0, 16);
      if (!hashMap.has(h)) hashMap.set(h, []);
      hashMap.get(h).push(f);
    } catch { /* skip */ }
  }
  // Return only groups with >1 file
  const dupes = new Set();
  for (const [, group] of hashMap) {
    if (group.length > 1) group.forEach(f => dupes.add(f));
  }
  return dupes;
}

// ── Detect CODA bootstrap files ───────────────────────────────────────────────
function isCodaBootstrap(filePath) {
  return filePath.startsWith(CODA_DIR);
}

// ── Main ──────────────────────────────────────────────────────────────────────
export async function runAudit(targetDir = TARGET_DIR, verbose = false) {
  console.log(`\n🔍 CODA Auditor - scanning ${targetDir}`);

  const files = await walk(targetDir);
  console.log(`   ${files.length} files found`);

  const [frequencyRaw, inDegree, recencyRaw, dupeSet] = await Promise.all([
    buildFrequencyProxy(files),
    buildLinkGraph(files),
    buildRecency(files),
    buildDuplicateGroups(files),
  ]);

  const freqNorm  = normalize(frequencyRaw);
  const centNorm  = normalize(inDegree);
  const recNorm   = normalize(recencyRaw);

  const manifest = [];
  let totalBytes = 0;

  for (const f of files) {
    let size = 0;
    try { size = (await fs.stat(f)).size; } catch { /* */ }
    totalBytes += size;

    const freq = freqNorm.get(f)  ?? 0;
    const cent = centNorm.get(f)  ?? 0;
    const rec  = recNorm.get(f)   ?? 0;

    const relevance = (freq * WEIGHT_FREQUENCY)
                    + (cent * WEIGHT_CENTRALITY)
                    + (rec  * WEIGHT_RECENCY);

    // Redundancy proxy: duplicate content = 1.0, else 0
    const redundancy = dupeSet.has(f) ? 1.0 : 0.0;

    // Classification
    let classification = 'normal';
    if (relevance < ORPHAN_THRESHOLD) {
      classification = 'orphan-candidate';
    }
    if (redundancy > 0) {
      classification = 'vault-duplicate';
    }
    if (relevance > HIGH_IMPORTANCE_THRESHOLD && redundancy > HIGH_REDUNDANCY_THRESHOLD) {
      classification = 'contested';  // skeptic.js will do second-pass
    }
    if (isCodaBootstrap(f)) {
      classification = 'coda-bootstrap';
    }

    const entry = {
      path: f,
      size,
      relevance: parseFloat(relevance.toFixed(4)),
      redundancy: parseFloat(redundancy.toFixed(4)),
      centrality: parseFloat(cent.toFixed(4)),
      recency:    parseFloat(rec.toFixed(4)),
      frequency:  parseFloat(freq.toFixed(4)),
      classification,
    };

    manifest.push(entry);
    if (verbose) {
      console.log(`   [${classification.padEnd(20)}] ${relevance.toFixed(3)}  ${f.replace(targetDir, '.')}`);
    }
  }

  // Sort: contested first (need review), then orphans, then normal, then coda-bootstrap
  const ORDER = { contested: 0, 'orphan-candidate': 1, 'vault-duplicate': 2, normal: 3, 'coda-bootstrap': 99 };
  manifest.sort((a, b) => (ORDER[a.classification] ?? 5) - (ORDER[b.classification] ?? 5));

  const output = {
    generated: new Date().toISOString(),
    target: targetDir,
    totalFiles: files.length,
    totalBytes,
    totalGB: parseFloat((totalBytes / 1e9).toFixed(3)),
    orphanCandidates: manifest.filter(e => e.classification === 'orphan-candidate').length,
    contested:        manifest.filter(e => e.classification === 'contested').length,
    duplicates:       manifest.filter(e => e.classification === 'vault-duplicate').length,
    codaBootstrap:    manifest.filter(e => e.classification === 'coda-bootstrap').length,
    entries: manifest,
  };

  await fs.writeFile(AUDIT_MANIFEST, JSON.stringify(output, null, 2));
  await logEntry('audit', `Scanned ${files.length} files, ${output.totalGB} GB, ${output.orphanCandidates} orphans, ${output.contested} contested`);

  console.log(`\n📊 Audit complete`);
  console.log(`   Total:      ${files.length} files  /  ${output.totalGB} GB`);
  console.log(`   Orphans:    ${output.orphanCandidates}`);
  console.log(`   Contested:  ${output.contested}`);
  console.log(`   Duplicates: ${output.duplicates}`);
  console.log(`   Manifest →  ${AUDIT_MANIFEST}\n`);

  return output;
}
