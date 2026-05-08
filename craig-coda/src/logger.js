/**
 * CODA - Logger
 * Append-only log. Every action is written here.
 * coda.log is the immutable record of what CODA did and why.
 */

import fs   from 'fs/promises';
import { CODA_LOG } from './config.js';

export async function logEntry(type, message) {
  const line = `${new Date().toISOString()}  [${type.toUpperCase().padEnd(12)}]  ${message}\n`;
  try {
    await fs.appendFile(CODA_LOG, line);
  } catch { /* log write failure is non-fatal */ }
}
