/**
 * CODA - Skeptic
 *
 * CODA cannot fully trust its own relevance scores.
 * This module audits the auditor.
 *
 * When a file is flagged "contested" (high importance AND high redundancy),
 * Skeptic runs a second-pass from a different angle before any prune action
 * is allowed on that file.
 *
 * Second-pass signals:
 *   1. Folder-level authority  - files in high-trust directories score up
 *   2. Name pattern matching   - known scaffolding patterns score down
 *   3. Extension weight        - .md/.js/.json score up vs. .log/.tmp
 *   4. Size signal             - tiny files (<1KB) that are highly central are suspicious
 *
 * If second-pass confirms importance → file is HELD (never pruned this cycle).
 * If second-pass confirms redundancy → file is cleared for prune.
 * If ambiguous                       → file stays contested, flagged for manual review.
 */

import path from 'path';

// Directories considered high-authority (score +0.3)
const HIGH_TRUST_DIRS = [
  '01_Foundation', '02_Character_Dossiers', '03_Structural_Timeline',
  'src', 'lib', 'core', 'vault',
];

// File name patterns that suggest scaffolding / temp artifacts (score -0.3)
const SCAFFOLD_PATTERNS = [
  /handoff/i, /handover/i, /temp/i, /tmp/i, /draft/i,
  /backup/i, /bak/i, /copy/i, /old/i, /archive/i,
];

// Extension trust weights
const EXT_WEIGHT = {
  '.md':   0.8,
  '.js':   0.7,
  '.ts':   0.7,
  '.json': 0.6,
  '.txt':  0.5,
  '.log':  0.2,
  '.tmp':  0.1,
  '.bak':  0.1,
};

export function secondPassScore(entry) {
  let score = entry.relevance;  // Start from the original score

  const relPath = entry.path;
  const fname   = path.basename(relPath);
  const ext     = path.extname(fname).toLowerCase();
  const dir     = path.dirname(relPath);

  // 1. Folder authority
  if (HIGH_TRUST_DIRS.some(d => dir.includes(d))) score += 0.3;

  // 2. Scaffold name patterns
  if (SCAFFOLD_PATTERNS.some(re => re.test(fname))) score -= 0.3;

  // 3. Extension weight
  const extW = EXT_WEIGHT[ext];
  if (extW !== undefined) score = score * 0.7 + extW * 0.3;

  // 4. Size anomaly - tiny but highly central (possible symlink/stub)
  if (entry.size < 1024 && entry.centrality > 0.5) score -= 0.15;

  score = Math.max(0, Math.min(1, score));

  let verdict;
  if (score > 0.6)        verdict = 'held';         // keep
  else if (score < 0.3)   verdict = 'cleared';      // ok to prune
  else                    verdict = 'manual-review'; // human must decide

  return { ...entry, secondPassScore: parseFloat(score.toFixed(4)), verdict };
}

export function runSkeptic(manifest) {
  const contested = manifest.filter(e => e.classification === 'contested');
  const resolved  = contested.map(secondPassScore);
  return resolved;
}
