/**
 * CODA - Central configuration
 * Edit TARGET_DIR and STORAGE_LIMIT_BYTES to match your environment.
 */

import os   from 'os';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// The root of everything CODA will audit.
export const TARGET_DIR = process.env.CODA_TARGET || os.homedir();

// Hard storage limit: 500 GB
export const STORAGE_LIMIT_BYTES = parseInt(process.env.CODA_LIMIT_BYTES || String(500 * 1024 * 1024 * 1024));

// Where CODA writes its state -- separate from source so upgrades don't wipe state
export const CODA_DIR       = process.env.CODA_STATE_DIR || path.join(os.homedir(), '.coda');
export const CODA_LOG       = path.join(CODA_DIR, 'coda.log');
export const AUDIT_MANIFEST = path.join(CODA_DIR, 'audit.manifest.json');
export const PLAN_FILE      = path.join(CODA_DIR, 'consolidation.plan.json');
export const CHECKPOINT_DIR = path.join(CODA_DIR, 'checkpoint/');

// Scoring weights (tune these)
export const WEIGHT_FREQUENCY  = 0.40;   // how often is the file accessed
export const WEIGHT_CENTRALITY = 0.35;   // how many other artifacts depend on it
export const WEIGHT_RECENCY    = 0.25;   // when was it last validated / modified

// A file scoring below this threshold is flagged as an orphan candidate
export const ORPHAN_THRESHOLD = 0.10;

// A file that scores both > HIGH_IMPORTANCE_THRESHOLD and > HIGH_REDUNDANCY_THRESHOLD
// is flagged as contested and held for second-pass review
export const HIGH_IMPORTANCE_THRESHOLD  = 0.65;
export const HIGH_REDUNDANCY_THRESHOLD  = 0.60;

// Prune order (lower index = pruned first)
export const PRUNE_ORDER = [
  'orphan-scaffolding',
  'donor-residue',
  'vault-duplicate',
  'low-centrality-lore',
  'contested-cleared',
  'coda-bootstrap',       // CODA prunes itself last
];
