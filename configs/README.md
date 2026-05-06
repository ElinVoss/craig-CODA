# Configs

This branch holds the repo's YAML contracts.
These files are not scratch notes.
They are the declarative layer that keeps the pipeline, runtime, retrieval, and backend behavior inspectable.

## What Lives Here

### Core runtime and project contracts

- `project.yaml`
- `runtime.yaml`
- `runtime_modes.yaml`
- `prompt_front_matter.yaml`

### Data and corpus contracts

- `cleaning.yaml`
- `data_schema.yaml`
- `dataset_build.yaml`
- `corpus_prep.yaml`
- `translator_rules.yaml`
- `vault_translation.yaml`

### Memory and graph contracts

- `node_schema.yaml`
- `memory_retrieval.yaml`
- `memory_query_profiles.yaml`
- `async_indexing.yaml`
- `episodic.yaml`
- `gguf_mining.yaml`

### Training and backend contracts

- `tokenizer.yaml`
- `model_architecture.yaml`
- `training_scratch.yaml`
- `training_sft.yaml`
- `eval.yaml`
- `backend_selection.yaml`
- `pretrained_backends.yaml`
- `adapter_targets.yaml`

### Auxiliary contracts

- `voice_conversion.yaml`

## Current State

- architecture resolution is no longer centered on `configs/model_architecture.yaml`
- the method vault is now the primary source for architecture profiles
- `model_architecture.yaml` remains here as a legacy fallback reference and compatibility anchor
- retrieval is now more than lexical fallback:
  - `memory_retrieval.yaml` describes semantic method, trust bias, and runtime layer rules
  - `memory_query_profiles.yaml` defines the weighted retrieval profiles
- async vault embedding is wired through `async_indexing.yaml`
- the pretrained backend lane is real and includes a Qwen2.5-Omni text-only backend path in `pretrained_backends.yaml`

## Do Not Violate

- keep config names stable
- do not invent a second source of truth casually
- treat these files as contracts that other branches rely on
- if the method vault supersedes a config, state that explicitly rather than silently leaving contradictory truth behind

## Continue From Here

You are in the `configs` scope.

Read in this order:

1. `README.md`
2. `project.yaml`
3. `runtime_modes.yaml`
4. `memory_retrieval.yaml`
5. `memory_query_profiles.yaml`
6. `pretrained_backends.yaml`
7. `node_schema.yaml`
8. `vault_translation.yaml`
9. `training_scratch.yaml`
10. `training_sft.yaml`

If the task is about architecture, also compare against:

- `exports/user_model_package/method_vault/weights/architecture/`
- `src/vault_methods.py`
- `src/model_factory.py`

Keep `D:\craig-CODA\LIVE_HANDOFF.md` current between meaningful actions.
