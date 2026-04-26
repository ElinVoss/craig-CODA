import { fileURLToPath } from "url";
import { dirname, resolve } from "path";
import { config } from "dotenv";

const __dirname = dirname(fileURLToPath(import.meta.url));
config({ path: resolve(__dirname, "../../.env") });

import express from "express";
import cors from "cors";
import { Runner, type AgentInputItem } from "@openai/agents";
import { craig } from "./craig.js";

const app = express();
app.use(cors({ origin: "http://localhost:5173" }));
app.use(express.json());

app.post("/api/chat", async (req, res) => {
  try {
    const { history = [], userMessage } = req.body as {
      history: AgentInputItem[];
      userMessage: string;
    };

    const conversationHistory: AgentInputItem[] = [
      ...history,
      { role: "user", content: [{ type: "input_text", text: userMessage }] },
    ];

    const runner = new Runner();
    const result = await runner.run(craig, conversationHistory);

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
