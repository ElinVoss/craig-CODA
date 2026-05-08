/**
 * CODA - Graduation
 *
 * CODA knows it is done when it can tell Craig what his best memory is
 * without being asked.
 *
 * Rules:
 *   - If CODA asks → it isn't done. Keep running.
 *   - If CODA answers → Craig confirms or denies.
 *   - If confirmed → CODA deletes all coda-bootstrap files and exits permanently.
 *
 * This module builds the answer from the vault graph topology:
 *   - It finds the highest-centrality Craig-authored node in the manifest
 *   - It composes an answer from that node's metadata
 *   - It outputs the answer without prompting the user
 *
 * The graduation test cannot be gamed. A model merely storing facts about Craig
 * might guess. A model structurally filled with Craig doesn't need to.
 */

import fs   from 'fs/promises';
import path from 'path';
import readline from 'readline/promises';
import { AUDIT_MANIFEST, PLAN_FILE, CODA_LOG } from './config.js';
import { logEntry } from './logger.js';

// Craig-authored directories (used to weight the graduation answer)
const CRAIG_AUTHORED_DIRS = ['vault', 'craig', 'confluence', 'omnimeta', 'warehouse'];

function isCraigAuthored(filePath) {
  return CRAIG_AUTHORED_DIRS.some(d => filePath.toLowerCase().includes(d));
}

export async function runGraduation({ assess = false, answer = null } = {}) {
  console.log('\n🎓 CODA Graduation check\n');

  let manifest;
  try {
    manifest = JSON.parse(await fs.readFile(AUDIT_MANIFEST, 'utf8'));
  } catch {
    console.log('  No audit manifest. Run: coda audit first.');
    return;
  }

  // Find the highest-centrality Craig-authored node
  const craigNodes = manifest.entries
    .filter(e => isCraigAuthored(e.path) && e.centrality > 0)
    .sort((a, b) => b.centrality - a.centrality);

  if (craigNodes.length === 0) {
    console.log('  Vault is empty or no Craig-authored content indexed yet.');
    console.log('  CODA is not ready.\n');
    await logEntry('graduation', 'NOT READY - no Craig-authored content found');
    return;
  }

  const topNode  = craigNodes[0];
  const nodeName = path.basename(topNode.path, path.extname(topNode.path));

  // Read the file content to surface the answer
  let content = '';
  try {
    content = await fs.readFile(topNode.path, 'utf8');
  } catch { /* binary or missing */ }

  const excerpt = content.slice(0, 400).replace(/\n+/g, ' ').trim();

  // CODA answers. No prompt. No ask.
  console.log('─'.repeat(60));
  console.log("CODA's answer:\n");
  console.log(`Your best memory lives in: ${nodeName}`);
  console.log(`Centrality score:          ${topNode.centrality.toFixed(4)}`);
  if (excerpt) {
    console.log(`\nOpening passage:\n  "${excerpt.slice(0, 200)}..."`);
  }
  console.log('\n' + '-'.repeat(60));

  // In assess-only mode, stop here — the extension will surface the answer and ask separately
  if (assess) return;

  // Non-interactive: answer passed in directly from an extension tool call
  let confirmed;
  if (answer !== null) {
    confirmed = answer.trim().toLowerCase() === 'yes';
  } else {
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    const reply = await rl.question('\nIs that right? (yes / no): ');
    rl.close();
    confirmed = reply.trim().toLowerCase() === 'yes';
  }

  if (confirmed) {
    console.log('\n✓ Graduation confirmed.\n');
    await logEntry('graduation', `CONFIRMED - best memory: ${nodeName}`);

    // Execute coda-bootstrap deletions
    let plan;
    try {
      plan = JSON.parse(await fs.readFile(PLAN_FILE, 'utf8'));
    } catch { plan = { actions: [] }; }

    const bootstrapActions = plan.actions.filter(a => a.action === 'delete-on-graduation');
    if (bootstrapActions.length === 0) {
      console.log('  No bootstrap files to clean up. CODA exits.\n');
    } else {
      console.log(`  Removing ${bootstrapActions.length} bootstrap files...\n`);
      for (const action of bootstrapActions) {
        try {
          await fs.unlink(action.path);
          console.log(`  ✓ Removed: ${path.basename(action.path)}`);
        } catch (err) {
          console.log(`  ✗ Could not remove ${action.path}: ${err.message}`);
        }
      }
      await logEntry('graduation', 'BOOTSTRAP PRUNED - CODA has exited');
      console.log('\n  CODA has finished.\n');
    }
  } else {
    console.log('\n  Not yet. Heartbeat continues.\n');
    await logEntry('graduation', 'DENIED - continuing');
  }
}
