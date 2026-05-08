# Src Runtime

This branch contains the richer runtime package that sits downstream of the pure L1 route layer.
It is where prompt interpretation, planning, mode resolution, prompt compilation, memory use, and backend execution become one pipeline.

## What Lives Here

- `front_matter_builder.py`
- `front_matter_classifier.py`
- `front_matter_rules.py`
- `front_matter_schema.py`
- `front_matter_renderer.py`
- `response_plan_builder.py`
- `mode_router.py`
- `prompt_compiler.py`
- `frame_policy.py`
- `session.py`
- `coda.py`
- `ollama_client.py`

## Current State

- front matter is rule-based and inspectable
- response planning is explicit
- mode routing is file-based and governed by `configs/runtime_modes.yaml`
- prompt compilation can append retrieved memory context
- `coda.py` now routes through the adapter registry rather than hardcoding one backend path
- `coda.py` now queries the vault graph directly, derives graph routing, and injects translated graph memory into the compiled prompt rather than relying on the older episodic SQLite lane

## Important Distinction

- `runtime/` is the pure route-and-classify surface
- `src/runtime/` is the runtime assembly package
- `agent/` is the user-facing execution surface that wraps this package

## Continue From Here

You are in the deeper runtime package.

Read in this order:

1. `README.md`
2. `front_matter_classifier.py`
3. `response_plan_builder.py`
4. `mode_router.py`
5. `prompt_compiler.py`
6. `coda.py`

If the user asks about backend choice, also read:

- `../coda_ir.py`
- `../adapters/`
- `../../configs/pretrained_backends.yaml`
- `../../configs/runtime_modes.yaml`

Keep `D:\craig-CODA\LIVE_HANDOFF.md` current between meaningful actions.
