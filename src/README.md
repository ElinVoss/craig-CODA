# Src

This branch contains the core Python implementation for `craig-CODA`.
It is where the repo stops being folder architecture and starts being executable system.

## What Lives Here

### Core top-level modules

- `vault_methods.py`
- `model_factory.py`
- `train_scratch.py`
- `train_sft.py`
- `sample_generate.py`
- tokenizer helpers
- corpus and schema helpers
- `coda_ir.py`

### Subpackages

- `adapters/` - backend adapter contract and implementations
- `runtime/` - richer runtime package
- `memory/` - vault graph extraction, retrieval, indexing, and routing
- `handoff/` - scope-map load / resolve / validate helpers
- `model_backends/` - scratch, pretrained, and Qwen2.5-Omni backend implementations
- `episodic/` - older SQLite episodic-memory lane
- `translation/` - vault-to-runtime and vault-to-training translation helpers

## Current State

- this branch now owns more than training
- it owns the adapter contract, the runtime contract, the memory contract, and the method-resolution contract
- `coda_ir.py` and `adapters/` make backend choice explicit
- `handoff/` makes scope routing explicit
- `runtime/` and `memory/` split the richer runtime stack into clearer responsibilities

## Continue From Here

You are in the broad `src` branch.

Read in this order:

1. `README.md`
2. `vault_methods.py`
3. `model_factory.py`
4. `coda_ir.py`
5. `train_scratch.py`
6. `train_sft.py`

Then narrow:

- if the user is talking about route and prompt behavior, descend into `runtime/`
- if the user is talking about retrieval or graph behavior, descend into `memory/`
- if the user is talking about backend wiring, read `adapters/`

Keep `D:\craig-CODA\LIVE_HANDOFF.md` current between meaningful actions.
