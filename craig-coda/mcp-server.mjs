import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";
import { execFile } from "child_process";
import { promisify } from "util";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const execFileAsync = promisify(execFile);
const __dirname = dirname(fileURLToPath(import.meta.url));
const CLI = join(__dirname, "src", "cli.js");

async function run(args) {
  try {
    const { stdout, stderr } = await execFileAsync(
      process.execPath,
      [CLI, ...args],
      { timeout: 120_000, cwd: __dirname, encoding: "utf8" }
    );
    return (stdout || "") + (stderr ? `\n[stderr]\n${stderr}` : "");
  } catch (err) {
    return err.stdout
      ? err.stdout + (err.stderr ? `\n[stderr]\n${err.stderr}` : "")
      : `Error: ${err.message}`;
  }
}

const TOOLS = [
  {
    name: "coda_status",
    description: "Show CODA status: manifest age, plan summary, and checkpoint info.",
    inputSchema: { type: "object", properties: {} },
  },
  {
    name: "coda_audit",
    description: "Audit the target directory. Walks the filesystem, scores files by relevance (frequency, centrality, recency), detects duplicates. Saves results to manifest.",
    inputSchema: {
      type: "object",
      properties: {
        dir: { type: "string", description: "Directory to audit (defaults to home dir)" },
      },
    },
  },
  {
    name: "coda_plan",
    description: "Build a consolidation plan from the last audit. Identifies files to prune, showing scores and reasons.",
    inputSchema: { type: "object", properties: {} },
  },
  {
    name: "coda_prune",
    description: "Execute the consolidation plan: move/delete low-relevance files. Creates a checkpoint for rollback safety.",
    inputSchema: {
      type: "object",
      properties: {
        dryRun: { type: "boolean", description: "If true, show what would be pruned without actually doing it" },
      },
    },
  },
  {
    name: "coda_rollback",
    description: "Roll back the last prune operation using the saved checkpoint.",
    inputSchema: { type: "object", properties: {} },
  },
  {
    name: "coda_graduation_assess",
    description: "Run graduation assessment: CODA finds the highest-centrality node representing Craig's best memory and states it. Does NOT ask for confirmation.",
    inputSchema: { type: "object", properties: {} },
  },
  {
    name: "coda_graduation_confirm",
    description: "Confirm or reject the graduation (self-prune) after coda_graduation_assess.",
    inputSchema: {
      type: "object",
      properties: {
        answer: {
          type: "string",
          enum: ["yes", "no"],
          description: "yes to confirm graduation (CODA self-destructs), no to cancel",
        },
      },
      required: ["answer"],
    },
  },
];

const server = new Server(
  { name: "coda", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({ tools: TOOLS }));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args = {} } = request.params;

  let output;
  switch (name) {
    case "coda_status":
      output = await run(["status"]);
      break;
    case "coda_audit":
      output = await run(args.dir ? ["audit", args.dir] : ["audit"]);
      break;
    case "coda_plan":
      output = await run(["plan"]);
      break;
    case "coda_prune":
      output = await run(args.dryRun ? ["prune", "--dry-run"] : ["prune"]);
      break;
    case "coda_rollback":
      output = await run(["rollback"]);
      break;
    case "coda_graduation_assess":
      output = await run(["graduation", "--assess"]);
      break;
    case "coda_graduation_confirm":
      output = await run(["graduation", "--answer", args.answer]);
      break;
    default:
      output = `Unknown tool: ${name}`;
  }

  return { content: [{ type: "text", text: output }] };
});

const transport = new StdioServerTransport();
await server.connect(transport);
