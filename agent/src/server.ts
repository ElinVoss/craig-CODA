import { fileURLToPath } from "url";
import { dirname, resolve } from "path";
import { config } from "dotenv";

const __dirname = dirname(fileURLToPath(import.meta.url));
config({ path: resolve(__dirname, "../../.env") });

import express from "express";
import cors from "cors";
import { Runner, type AgentInputItem } from "@openai/agents";
import { queryMemory } from "./memory.js";

const useLocal = process.env.CRAIG_BACKEND === "local";
const { craig }     = useLocal ? { craig: null } : await import("./craig.js");
const { craigLocal } = useLocal ? await import("./craig-local.js") : { craigLocal: null };
const agent = useLocal ? craigLocal! : craig!;

console.log(`Craig backend: ${useLocal ? `local (${process.env.LOCAL_MODEL_URL ?? "http://localhost:1234/v1"})` : "OpenAI"}`);

const app = express();
app.use(cors({ origin: "http://localhost:5173" }));
app.use(express.json());

app.post("/api/chat", async (req, res) => {
  try {
    const { history = [], userMessage } = req.body as {
      history: AgentInputItem[];
      userMessage: string;
    };

    // Pre-retrieve from vault graph before the model sees the message.
    // The routing block (from graph structure) tells the agent what behavioral
    // contract applies for this turn. The memory context gives it the content.
    // Both are derived from the graph — not from static instructions.
    const memoryResult = queryMemory(userMessage);
    let enrichedMessage = userMessage;
    if (memoryResult) {
      const parts: string[] = [];
      if (memoryResult.routingBlock) parts.push(memoryResult.routingBlock);
      if (memoryResult.memoryContext) parts.push(`[MEMORY CONTEXT]\n${memoryResult.memoryContext}\n[/MEMORY CONTEXT]`);
      if (parts.length > 0) enrichedMessage = `${parts.join("\n\n")}\n\n${userMessage}`;
    }

    const conversationHistory: AgentInputItem[] = [
      ...history,
      { role: "user", content: [{ type: "input_text", text: enrichedMessage }] },
    ];

    const runner = new Runner();
    const result = await runner.run(agent, conversationHistory);

    if (!result.finalOutput) {
      throw new Error("Craig returned no output");
    }

    const updatedHistory: AgentInputItem[] = [
      ...conversationHistory,
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      ...result.newItems.map((item: any) => item.rawItem),
    ];

    res.json({ response: result.finalOutput, history: updatedHistory });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : String(err);
    console.error("Craig error:", message);
    res.status(500).json({ error: message });
  }
});

app.get("/health", (_req, res) => res.json({ status: "ok" }));

const PORT = 8001;
app.listen(PORT, () => {
  console.log(`Craig agent server running on http://localhost:${PORT}`);
});
