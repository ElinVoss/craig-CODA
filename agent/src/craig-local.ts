import OpenAI from "openai";
import { Agent, OpenAIChatCompletionsModel, setOpenAIAPI } from "@openai/agents";
import {
  CRAIG_INSTRUCTIONS,
  queryMemoryTool,
  readFileTool,
  writeFileTool,
  listDirTool,
  searchFilesTool,
} from "./craig.js";

// Local models use Chat Completions — not the OpenAI Responses API
setOpenAIAPI("chat_completions");

const LOCAL_URL   = process.env.LOCAL_MODEL_URL   ?? "http://localhost:1234/v1";
const LOCAL_MODEL = process.env.LOCAL_MODEL_NAME  ?? "lmstudio-community/Qwen3-4B-Instruct-2507-GGUF/Qwen3-4B-Instruct-2507-Q4_K_M.gguf";
const LOCAL_KEY   = process.env.LOCAL_MODEL_API_KEY ?? "lm-studio";

const localClient = new OpenAI({
  baseURL: LOCAL_URL,
  apiKey:  LOCAL_KEY,
});

export const craigLocal = new Agent({
  name: "Craig",
  instructions: CRAIG_INSTRUCTIONS,
  model: new OpenAIChatCompletionsModel(localClient, LOCAL_MODEL),
  tools: [queryMemoryTool, readFileTool, writeFileTool, listDirTool, searchFilesTool],
  modelSettings: {
    store: false,
  },
});
