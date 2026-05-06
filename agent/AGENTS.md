# Agent Surface Guide

Read order for this branch:

1. `README.md`
2. `src/server.ts`
3. `src/memory.ts`
4. `src/craig.ts`
5. `src/craig-local.ts`
6. `src/cli.ts`

Use this branch for the local HTTP and CLI surfaces, not for root handoff routing or deeper route-law decisions.
If the task is really about graph routing or runtime planning, trace into `scripts/query_memory.py`, `src/memory/`, or `src/runtime/` instead of guessing from this package alone.
Update `D:\craig-CODA\LIVE_HANDOFF.md` between meaningful actions while working in this branch.
