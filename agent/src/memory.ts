import { spawnSync } from "child_process";
import { resolve } from "path";

const REPO_ROOT = "D:\\craig-CODA";
const PYTHON = process.env.PYTHON_BIN ?? "python";
const SCRIPT = resolve(REPO_ROOT, "scripts", "query_memory.py");

export interface MemoryResult {
  /** Rendered memory context block — the retrieved node summaries. */
  memoryContext: string;
  /**
   * Routing block derived from graph structure — trust layers, node types,
   * edge clusters, coverage. This is the behavioral contract for the turn.
   */
  routingBlock: string;
}

/**
 * Query the vault knowledge graph.
 *
 * Returns both the rendered memory context (what the graph contains) and the
 * routing block (what the graph structure implies the agent should do).
 *
 * Returns null if the graph is missing, no nodes were retrieved, or the
 * subprocess fails — callers must degrade gracefully in all three cases.
 */
export function queryMemory(
  query: string,
  profile?: string,
  topK?: number,
): MemoryResult | null {
  const args = [
    SCRIPT,
    "--query", query,
    "--output", "full",
    ...(profile ? ["--profile", profile] : []),
    ...(topK != null ? ["--top-k", String(topK)] : []),
  ];

  const result = spawnSync(PYTHON, args, {
    cwd: REPO_ROOT,
    encoding: "utf-8",
    timeout: 15_000,
  });

  if (result.error || result.status !== 0) {
    console.error("[memory] vault query failed:", result.stderr?.trim() || result.error?.message);
    return null;
  }

  const raw = result.stdout.trim();
  if (!raw) return null;

  let parsed: { memory_context: string; routing_block: string };
  try {
    parsed = JSON.parse(raw);
  } catch {
    console.error("[memory] failed to parse vault output:", raw.slice(0, 200));
    return null;
  }

  if (!parsed.memory_context && !parsed.routing_block) return null;

  return {
    memoryContext: parsed.memory_context,
    routingBlock: parsed.routing_block,
  };
}
