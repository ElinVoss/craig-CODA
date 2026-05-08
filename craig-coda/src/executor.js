/**
 * CODA - Executor
 *
 * Runs the consolidation plan. Checkpoints before every prune.
 * CODA never eliminates without a recoverable state one step back.
 *
 * handleIgnoreMove pattern:
 *   If a prune is rolled back, the reason is recorded
 *   and the plan rebuilds around it (not silently retried).
 *
 * Prune order is enforced: coda-bootstrap is ALWAYS last.
 */

import fs   from 'fs/promises';
import path from 'path';
import { PLAN_FILE, CHECKPOINT_DIR, CODA_DIR } from './config.js';
import { logEntry } from './logger.js';

// ── Checkpoint ────────────────────────────────────────────────────────────────
async function writeCheckpoint(action) {
  await fs.mkdir(CHECKPOINT_DIR, { recursive: true });
  const ts      = Date.now();
  const cpDir   = path.join(CHECKPOINT_DIR, String(ts));
  await fs.mkdir(cpDir, { recursive: true });

  // Save a copy of the file about to be deleted/moved
  if (action.action === 'delete' || action.action === 'delete-on-graduation') {
    try {
      const dest = path.join(cpDir, path.basename(action.path));
      await fs.copyFile(action.path, dest);
    } catch { /* file may already be gone - that's ok */ }
  }

  await fs.writeFile(
    path.join(cpDir, 'action.json'),
    JSON.stringify({ ts, action }, null, 2)
  );

  return cpDir;
}

// ── Execute one action ────────────────────────────────────────────────────────
async function executeAction(action, force = false) {
  if (action.action === 'delete-on-graduation') {
    // Only executed when graduation is confirmed - not during normal prune runs
    return { status: 'skipped', reason: 'awaiting-graduation' };
  }

  const cpDir = await writeCheckpoint(action);

  try {
    if (action.action === 'delete') {
      await fs.unlink(action.path);
      await logEntry('prune', `DELETE ${action.path} [${action.reason}] checkpoint=${cpDir}`);
      return { status: 'done', path: action.path };

    } else if (action.action === 'move') {
      await fs.mkdir(path.dirname(action.dest), { recursive: true });
      await fs.rename(action.path, action.dest);
      await logEntry('prune', `MOVE ${action.path} → ${action.dest} [${action.reason}]`);
      return { status: 'done', path: action.path, dest: action.dest };
    }

  } catch (err) {
    // handleIgnoreMove: record the failure reason, mark for plan rebuild
    await logEntry('rollback', `FAILED ${action.path} reason=${err.message}`);
    return { status: 'failed', path: action.path, reason: err.message };
  }

  return { status: 'skipped', reason: 'unknown-action' };
}

// ── Main ──────────────────────────────────────────────────────────────────────
export async function runPrune(force = false) {
  console.log('\n⚙️  CODA Executor - running consolidation plan');

  let plan;
  try {
    plan = JSON.parse(await fs.readFile(PLAN_FILE, 'utf8'));
  } catch {
    console.error('  ✗ No plan found. Run: coda plan');
    process.exit(1);
  }

  const actions = plan.actions.filter(a => {
    if (a.action === 'delete-on-graduation') return false;
    if (!force && a.verdict === 'manual-review') return false;
    return true;
  });

  let done = 0, failed = 0, skipped = 0;
  const failedPaths = [];

  for (const action of actions) {
    const result = await executeAction(action, force);
    if (result.status === 'done')    done++;
    else if (result.status === 'failed') { failed++; failedPaths.push(result.path); }
    else skipped++;
  }

  console.log('\n✅ Prune complete');
  console.log(`   Done:     ${done}`);
  console.log(`   Failed:   ${failed}`);
  console.log(`   Skipped:  ${skipped}`);
  if (failedPaths.length > 0) {
    console.log('\n  Failed paths (plan will rebuild around these):');
    for (const p of failedPaths) console.log(`   ${p}`);
  }
  console.log('\n  Re-run: coda audit && coda plan to update state\n');
}

// ── Rollback ──────────────────────────────────────────────────────────────────
export async function runRollback() {
  console.log('\n↩️  CODA Rollback - restoring most recent checkpoint');

  let dirs;
  try {
    dirs = (await fs.readdir(CHECKPOINT_DIR)).sort().reverse();
  } catch {
    console.error('  ✗ No checkpoints found.');
    process.exit(1);
  }

  if (dirs.length === 0) {
    console.log('  Nothing to roll back.');
    return;
  }

  const latest = path.join(CHECKPOINT_DIR, dirs[0]);
  const meta   = JSON.parse(await fs.readFile(path.join(latest, 'action.json'), 'utf8'));
  const action = meta.action;

  if (action.action === 'delete' || action.action === 'delete-on-graduation') {
    const src  = path.join(latest, path.basename(action.path));
    try {
      await fs.mkdir(path.dirname(action.path), { recursive: true });
      await fs.copyFile(src, action.path);
      await logEntry('rollback', `RESTORED ${action.path} from checkpoint ${latest}`);
      console.log(`  ✓ Restored: ${action.path}\n`);
    } catch (err) {
      console.error(`  ✗ Rollback failed: ${err.message}`);
    }
  } else {
    console.log(`  Checkpoint action type "${action.action}" - no file to restore.`);
  }
}
