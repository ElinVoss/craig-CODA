# Runtime Route Layer

This branch contains the pure L1 route layer.
It exists to make route logic explicit before the richer runtime package or the backend model gets involved.

## What Lives Here

- `classify_prompt.py` - inspectable prompt-axis classifier
- `route_prompt.py` - pure route function with no backend calls or side effects
- companion graph declarations under:
  - `../graph/axes/`
  - `../graph/nodes/`
  - `../graph/routes/route_rules.yaml`

## Current State

- the classifier is intentionally dumb and replaceable
- the route engine is intentionally pure and testable
- this branch is where route semantics become inspectable instead of implied
- the associated tests live in `../tests/test_l1_routing.py`

## Important Distinction

- `runtime/` is the top-level route-and-classify surface
- `src/runtime/` is the richer runtime package that assembles front matter, plans, modes, prompts, and backend calls
- do not flatten those two layers together

## Continue From Here

You are in the `runtime` scope.

Read in this order:

1. `README.md`
2. `classify_prompt.py`
3. `route_prompt.py`
4. `../graph/routes/route_rules.yaml`
5. `../tests/test_l1_routing.py`

Keep `D:\craig-CODA\LIVE_HANDOFF.md` current between meaningful actions.
