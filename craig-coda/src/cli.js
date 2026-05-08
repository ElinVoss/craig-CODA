#!/usr/bin/env node
/**
 * CODA - CLI entry point
 * Usage: coda <command> [options]
 *
 * Commands:
 *   audit       Walk the target and score every artifact
 *   plan        Build a consolidation plan from the last audit
 *   prune       Execute the plan (writes checkpoint first)
 *   status      Show current state, storage used, graduation readiness
 *   graduation  Run the graduation check (no prompts - CODA answers or it doesn't)
 *   rollback    Restore the most recent checkpoint
 *
 * CODA never asks permission. It checkpoints, acts, and logs.
 */

import { Command } from 'commander';
import { runAudit } from './auditor.js';
import { runPlan } from './planner.js';
import { runPrune } from './executor.js';
import { runStatus } from './status.js';
import { runGraduation } from './graduation.js';
import { runRollback } from './executor.js';
import { CODA_LOG, TARGET_DIR, STORAGE_LIMIT_BYTES } from './config.js';

// Commander is a zero-dep CLI framework built into the Node ecosystem.
// If not available: npm install commander
const program = new Command();

program
  .name('coda')
  .description('Audit. Consolidate. Prune. Disappear.')
  .version('0.1.0');

program
  .command('audit')
  .description('Walk the target directory and score every artifact')
  .option('-t, --target <path>', 'Target directory to audit', TARGET_DIR)
  .option('-v, --verbose', 'Show every file scored', false)
  .action(async (opts) => {
    await runAudit(opts.target, opts.verbose);
  });

program
  .command('plan')
  .description('Build a consolidation plan from the last audit')
  .option('--dry-run', 'Print the plan without writing it', false)
  .action(async (opts) => {
    await runPlan(opts.dryRun);
  });

program
  .command('prune')
  .description('Execute the consolidation plan (checkpoints first)')
  .option('--force', 'Skip contested-artifact hold', false)
  .action(async (opts) => {
    await runPrune(opts.force);
  });

program
  .command('status')
  .description('Show storage usage, audit age, graduation readiness')
  .action(async () => {
    await runStatus();
  });

program
  .command('graduation')
  .description("Run the graduation check -- CODA answers or it doesn't")
  .option('--assess', 'Print graduation answer without prompting for confirmation', false)
  .option('--answer <reply>', 'Non-interactive confirmation: yes or no')
  .action(async (opts) => {
    await runGraduation({ assess: opts.assess, answer: opts.answer });
  });

program
  .command('rollback')
  .description('Restore the most recent checkpoint')
  .action(async () => {
    await runRollback();
  });

program.parse();
