# Frontend

This branch contains the React/Vite browser surface for `craig-CODA`.
It is an interaction surface, not the repo's primary continuity or reasoning layer.

## What Lives Here

- `src/App.tsx`
- `src/Chat.tsx`
- `src/ChatWidget.tsx`

## Current State

- the frontend is intentionally minimal
- it is primarily a chat-oriented surface that talks to the local agent server
- it does not own the handoff system, route logic, vault rules, or graph memory behavior

## Important Reality

- if the UI looks too thin, that is because the architecture work happened deeper in the repo first
- the real source of truth for continuity and runtime behavior lives in:
  - root handoff docs
  - `runtime/`
  - `src/runtime/`
  - `src/memory/`
  - `agent/`

## Continue From Here

You are in the `frontend` scope.

Read in this order:

1. `README.md`
2. `src/App.tsx`
3. `src/Chat.tsx`
4. `src/ChatWidget.tsx`

If the user asks why the UI behaves a certain way, trace into the agent and runtime branches instead of assuming the answer is in React alone.

Keep `D:\craig-CODA\LIVE_HANDOFF.md` current between meaningful actions.
