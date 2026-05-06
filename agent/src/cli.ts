import { fileURLToPath } from "url";
import { dirname, resolve } from "path";
import { config } from "dotenv";

const __dirname = dirname(fileURLToPath(import.meta.url));
config({ path: resolve(__dirname, "../../.env") });

import * as readline from "readline";
import { Runner, type AgentInputItem } from "@openai/agents";

const useLocal = process.env.CRAIG_BACKEND === "local";
const { craig }      = useLocal ? { craig: null }      : await import("./craig.js");
const { craigLocal } = useLocal ? await import("./craig-local.js") : { craigLocal: null };
const agent = useLocal ? craigLocal! : craig!;

const runner = new Runner();
const history: AgentInputItem[] = [];

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: true,
});

const RESET  = "\x1b[0m";
const DIM    = "\x1b[2m";
const CYAN   = "\x1b[36m";
const GREEN  = "\x1b[32m";
const YELLOW = "\x1b[33m";
const RED    = "\x1b[31m";

console.log(`\n${CYAN}╔══════════════════════════════════════╗${RESET}`);
console.log(`${CYAN}║  Craig — craig-CODA collaborator     ║${RESET}`);
console.log(`${CYAN}╚══════════════════════════════════════╝${RESET}`);
console.log(`${DIM}  D:\\craig-CODA  •  ${useLocal ? "local model" : "OpenAI"}  •  type 'exit' to quit${RESET}\n`);

const ask = () => {
  rl.question(`${GREEN}You ❯${RESET} `, async (input) => {
    const text = input.trim();
    if (!text) { ask(); return; }
    if (text.toLowerCase() === "exit" || text.toLowerCase() === "quit") {
      console.log(`\n${DIM}bye.${RESET}\n`);
      rl.close();
      process.exit(0);
    }

    const turn: AgentInputItem[] = [
      ...history,
      { role: "user", content: [{ type: "input_text", text }] },
    ];

    process.stdout.write(`\n${YELLOW}Craig ❯${RESET} `);
    try {
      const result = await runner.run(agent, turn);

      if (!result.finalOutput) throw new Error("No output");

      // Print response, preserving line breaks
      process.stdout.write(result.finalOutput + "\n\n");

      // Update history
      history.push({ role: "user", content: [{ type: "input_text", text }] });
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      result.newItems.forEach((item: any) => history.push(item.rawItem));
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : String(err);
      console.error(`\n${RED}Error: ${msg}${RESET}\n`);
    }

    ask();
  });
};

ask();
