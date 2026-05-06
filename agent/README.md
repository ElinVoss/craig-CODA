# Agent

This branch contains the local agent surfaces for `craig-CODA`.
It does not define the deeper architecture by itself.
It is the layer that makes the runtime, memory graph, and vault rules interact with a live model and a live user.

## What Lives Here

- `src/server.ts` - HTTP chat surface used by the browser client
- `src/cli.ts` - terminal chat loop
- `src/memory.ts` - Node-to-Python bridge into `scripts/query_memory.py`
- `src/craig.ts` - OpenAI-backed Craig agent, tools, and instructions
- `src/craig-local.ts` - local OpenAI-compatible / LM Studio-backed variant
- `package.json` - package scripts and dependencies for this surface

## Current State

- the server now pre-retrieves from the vault graph before the model sees the user turn
- the server injects two graph-derived blocks ahead of the user message when available:
  - `[GRAPH ROUTING]`
  - `[MEMORY CONTEXT]`
- `src/memory.ts` shells out to `scripts/query_memory.py --output full` and returns both `routingBlock` and `memoryContext`
- `src/craig.ts` treats the graph as the constitution and the model as the executor
- `src/craig-local.ts` keeps the same instructions and tools but routes through a local OpenAI-compatible backend
- `src/cli.ts` is intentionally thin; it is a direct operator surface rather than a second runtime

## Important Reality

- this branch is not the source of truth for route logic, trust-layer rules, or vault extraction
- those behaviors are owned by `runtime/`, `src/runtime/`, `src/memory/`, `configs/`, and the method vault
- the agent surface is where those deeper layers get injected into a live turn

## Continue From Here

You are in the `agent` scope.

Read in this order:

1. `README.md`
2. `src/server.ts`
3. `src/memory.ts`
4. `src/craig.ts`
5. `src/craig-local.ts`
6. `src/cli.ts`

If the user asks how the agent becomes informed by repo state, trace from `src/server.ts` into:

- `scripts/query_memory.py`
- `src/memory/graph_router.py`
- `src/runtime/`
- `exports/user_model_package/method_vault/`

Keep `D:\craig-CODA\LIVE_HANDOFF.md` current between meaningful actions.
