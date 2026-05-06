# Master Index

This file is the current structural index of the local `D:\craig-CODA` checkout.
It absorbs the local additions that are absent from older GitHub snapshots and describes the repo as it actually exists now.

Use it for orientation, not for bypassing the root handoff path.
The root handoff files and `LIVE_HANDOFF.md` still outrank this file for in-session truth.

## How To Read This File

- root control docs tell you what is true now and how to continue
- branch docs tell you where to work when scope narrows
- source files tell you how behavior is implemented
- artifacts tell you what the pipeline has already produced
- local-only helper folders are present in this checkout, but they are not treated as source of truth

## Root Control Docs

| Path | Why it exists |
| --- | --- |
| `README.md` | Root architecture, operating assumptions, top-level map, and branch guide. |
| `AGENTS.md` | Root contract for assistants entering the repo. |
| `CURRENT_STATE.md` | Concise statement of what is working and what remains unresolved. |
| `DECISIONS.md` | Locked decisions and unresolved decision boundaries. |
| `NEXT_STEPS.md` | Immediate queue and longer-range arc. |
| `ARTIFACTS.md` | Generated-output and artifact family map. |
| `HANDOFF_PROMPT.md` | Startup contract of record. |
| `LIVE_HANDOFF.md` | Shared baton file updated between meaningful actions. |
| `MASTER_HANDOVER_NEXT_SESSION.md` | Long-form continuity bridge across sessions. |
| `SCOPE_MAP.yaml` | Scope aliases, read order, and work-from targets. |
| `graph-native-complete-handoff.md` | Deep reference document from earlier graph-native work. |

## Top-Level Directory Index

| Path | Why it exists |
| --- | --- |
| `agent/` | Local HTTP and CLI agent surfaces. |
| `artifacts/` | Generated corpus, tokenizer, model, eval, vault, and resolution outputs. |
| `checkpoints/` | Older or separate checkpoint root still present locally. |
| `cog/` | Sparse experimental field/C branch. |
| `configs/` | YAML contracts for data, retrieval, runtime, and training. |
| `data/` | Raw, clean, pretrain, SFT, preference, and eval data layers. |
| `docs/` | Architecture notes, specs, and design material. |
| `eval/` | Retrieval evaluation fixtures and logged results. |
| `examples/` | Example prompts and small reference inputs. |
| `exports/` | User model package and method-vault tree. |
| `frontend/` | React/Vite browser surface. |
| `graph/` | L1 route axes, capability nodes, constraints, and route rules. |
| `logs/` | Runtime logging outputs. |
| `notebooks/` | Optional exploration notebooks. |
| `runtime/` | Pure L1 classify/route layer. |
| `scratch/` | Local experimental scratch area. |
| `scripts/` | Executable pipeline and validation surface. |
| `src/` | Core Python implementation. |
| `template/` | Template material carried in the repo. |
| `tests/` | Runtime, routing, adapter, backend, and scope-map tests. |

## Local-Only Helper And Generated Directories Present In This Checkout

These are present locally and matter operationally, but they are not treated as the architectural source of truth:

- `.superpowers/`
- `.remember/`
- `.claude/`
- `.pytest_cache/`
- `__pycache__/`
- `agent/node_modules/`

## Config Contract Index

### Core project, runtime, and data contracts

| File | Purpose |
| --- | --- |
| `configs/project.yaml` | Root project identity, D: paths, dual-track flags, CPU-first/local-only assumptions. |
| `configs/runtime.yaml` | Local runtime safety defaults, log location, and path assumptions. |
| `configs/data_schema.yaml` | JSONL field requirements for SFT, preferences, and eval records. |
| `configs/cleaning.yaml` | Conservative text cleaning behavior for phase-two ingestion. |
| `configs/dataset_build.yaml` | Placeholder dataset-building outputs and heuristics. |
| `configs/corpus_prep.yaml` | Corpus-preparation input roots, filtering, and artifact output locations. |

### Tokenizer and training contracts

| File | Purpose |
| --- | --- |
| `configs/tokenizer.yaml` | Tokenizer type, vocab size, training output directory, and inspection samples. |
| `configs/model_architecture.yaml` | Legacy fallback architecture reference for the `craig-coda-0.6b` target shape. |
| `configs/training_scratch.yaml` | Scratch-training defaults and checkpoint cadence for the tiny Qwen3-style lane. |
| `configs/training_sft.yaml` | SFT scaffold and schema expectations. |
| `configs/eval.yaml` | Eval report paths, generation settings, and dataset mix. |

### Runtime, routing, and prompt contracts

| File | Purpose |
| --- | --- |
| `configs/runtime_modes.yaml` | Mode file sets, optional context files, and forbidden auto-load folders. |
| `configs/prompt_front_matter.yaml` | Rule-based front-matter defaults and keyword triggers. |
| `configs/backend_selection.yaml` | Default backend selection and compare-backend defaults for scripts. |
| `configs/adapter_targets.yaml` | Layer-selection targets for adapter or translation work. |

### Memory and vault contracts

| File | Purpose |
| --- | --- |
| `configs/node_schema.yaml` | Canonical vault-node field requirements and extracted-from schema. |
| `configs/memory_retrieval.yaml` | Retrieval artifacts, semantic method, trust bias rules, runtime layer rules. |
| `configs/memory_query_profiles.yaml` | Weighted retrieval profiles such as `technical`, `autobiographical`, `prose`, `constraints`, `critique`. |
| `configs/vault_translation.yaml` | Source roots and source kinds for building the vault graph. |
| `configs/translator_rules.yaml` | Which trust layers feed runtime context, SFT, preferences, and prose outputs. |
| `configs/async_indexing.yaml` | Remote Ollama embedding path, poll interval, and sidecar embedding locations. |
| `configs/episodic.yaml` | Older episodic-memory weights, decay, and hum cadence. |
| `configs/gguf_mining.yaml` | Heuristic tensor-mining limits and output path. |

### Backend and auxiliary contracts

| File | Purpose |
| --- | --- |
| `configs/pretrained_backends.yaml` | Named local pretrained backends, including the Qwen2.5-Omni text-only lane. |
| `configs/voice_conversion.yaml` | Voice-conversion batch settings and configured books. |

## Script Index

### Bootstrap, inspection, and validation

| Script | Purpose |
| --- | --- |
| `scripts/bootstrap.ps1` | Conservative Windows bootstrap helper. |
| `scripts/print_tree.py` | Tree printer for repo inspection. |
| `scripts/inspect_model.py` | Scratch-model and tokenizer setup inspection. |
| `scripts/inspect_tokenizer.py` | Tokenizer artifact inspection. |
| `scripts/inspect_vault_graph.py` | Human-readable view into the built vault graph. |
| `scripts/list_backends.py` | List configured local backends. |
| `scripts/validate_backends.py` | Validate backend config and local path presence. |
| `scripts/validate_data.py` | Validate data-layer schemas and structure. |
| `scripts/validate_scope_map.py` | Validate scope-map structure and required paths. |
| `scripts/test_front_matter.py` | Front-matter and response-plan sanity checks. |

### Data ingest, import, and normalization

| Script | Purpose |
| --- | --- |
| `scripts/ingest_raw.py` | Stage raw files into `_ingested/`. |
| `scripts/clean_text.py` | Conservative text cleaning stage. |
| `scripts/build_datasets.py` | Placeholder dataset generation step. |
| `scripts/run_pipeline.py` | Full phase-two data pipeline. |
| `scripts/import_markdown_export_raw.py` | Import one-markdown-per-conversation corpus into `data/raw/conversation_exports/markdown_export_raw/`. |
| `scripts/normalize_markdown_export_raw.py` | Convert imported markdown export files into clean thread transcripts, pretrain text, and SFT reply pairs. |
| `scripts/extract_messages.py` | Extract or shape message content from raw material. |
| `scripts/ingest_project.py` | Project-specific ingest path. |
| `scripts/ingest_personal_nodes.py` | Personal-node ingest path. |
| `scripts/extract_personal_corpus.py` | Personal corpus extraction helper. |

### Corpus and tokenizer lane

| Script | Purpose |
| --- | --- |
| `scripts/prepare_corpus.py` | Build prepared tokenizer/training corpus from clean text. |
| `scripts/train_tokenizer.py` | Train local tokenizer artifacts. |
| `scripts/run_tokenizer_pipeline.py` | Prepare, train, inspect, and validate the tokenizer lane. |
| `scripts/tokenize_corpus.py` | Tokenize a corpus with the current tokenizer artifacts. |
| `scripts/fetch_qwen_tokenizer.py` | Fetch Qwen tokenizer assets when needed. |

### Training, eval, and generation

| Script | Purpose |
| --- | --- |
| `scripts/run_scratch_train.py` | Run the scratch-training lane. |
| `scripts/run_sft_train.py` | Run the SFT scaffold lane. |
| `scripts/run_sample_generation.py` | Generate local samples from checkpointed or backend paths. |
| `scripts/run_eval_suite.py` | Run the local eval suite. |
| `scripts/monitor_training.py` | Observe local training progress. |
| `scripts/train_adapter.py` | Adapter-training helper surface. |
| `scripts/merge_adapter.py` | Adapter merge helper. |
| `scripts/compare_backends.py` | Compile once and compare backends side by side. |
| `scripts/run_pretrained_generation.py` | Run one configured local pretrained backend. |

### Memory, graph, and translation

| Script | Purpose |
| --- | --- |
| `scripts/build_vault_graph.py` | Build vault nodes and edges from configured sources. |
| `scripts/query_memory.py` | Retrieve nodes and render both graph-routing and memory-context output. |
| `scripts/run_memory_ablation.py` | Compare retrieval behavior under ablation. |
| `scripts/run_async_indexer.py` | Start or single-pass the async embedding indexer. |
| `scripts/mine_gguf.py` | Heuristic GGUF tensor miner that emits vault nodes. |
| `scripts/build_training_artifacts.py` | Emit translation artifacts from the vault graph. |
| `scripts/vault_index.py` | Vault indexing helper. |
| `scripts/vault_generate.py` | Vault-based generation helper. |
| `scripts/vault_flatten.py` | Flatten vault structure into downstream forms. |
| `scripts/run_vault_build.py` | Orchestrate vault build flow. |
| `scripts/convert_to_voice.py` | Voice-conversion pipeline entrypoint. |

### Operational and compatibility helpers

| Script | Purpose |
| --- | --- |
| `scripts/chat.py` | Local script-level chat helper. |
| `scripts/autopilot.py` | Local automation helper surface. |
| `scripts/add_memory.py` | Manual episodic-memory addition helper. |
| `scripts/run_qwen_manifest_openai_compat.py` | Exact-donor manifest runner for a remote OpenAI-compatible or LM Studio host. |

## `runtime/` Index: Pure L1 Route Layer

| File | Purpose |
| --- | --- |
| `runtime/classify_prompt.py` | Intentionally dumb, inspectable prompt-axis classifier. |
| `runtime/route_prompt.py` | Pure route engine with no backend calls, embeddings, or side effects. |
| `runtime/__init__.py` | Package marker. |

### `graph/` route-spec companion files

| Path | Purpose |
| --- | --- |
| `graph/axes/domain.yaml` | Domain-axis values. |
| `graph/axes/intent.yaml` | Intent-axis values. |
| `graph/axes/reasoning_mode.yaml` | Reasoning-axis values. |
| `graph/axes/stakes.yaml` | Stakes-axis values. |
| `graph/axes/temporal_scope.yaml` | Time-axis values. |
| `graph/axes/trust_layer.yaml` | Trust-layer route values. |
| `graph/axes/voice_signature.yaml` | Voice-signature route values. |
| `graph/nodes/capabilities.yaml` | Capability node declarations. |
| `graph/nodes/constraints.yaml` | Constraint node declarations. |
| `graph/nodes/knowledge.yaml` | Knowledge-node declarations. |
| `graph/nodes/policies.yaml` | Policy-node declarations. |
| `graph/routes/route_rules.yaml` | Route definitions for L1 activation. |

## `src/` Index: Core Python Implementation

### Top-level source files

| File | Purpose |
| --- | --- |
| `src/vault_methods.py` | Parent-to-child method-vault resolution and artifact writing. |
| `src/model_factory.py` | Model construction via vault-resolved architecture profiles. |
| `src/train_scratch.py` | Scratch-training implementation. |
| `src/train_sft.py` | SFT scaffold implementation. |
| `src/sample_generate.py` | Sample-generation helper. |
| `src/tokenizer_loader.py` | Tokenizer artifact loader. |
| `src/tokenizer_utils.py` | Tokenizer helper functions. |
| `src/tokenizer_checks.py` | Tokenizer validation helpers. |
| `src/corpus_prep.py` | Corpus-prep implementation. |
| `src/dataset_builders.py` | Placeholder dataset builders. |
| `src/schema_checks.py` | Schema validation helpers. |
| `src/text_cleaning.py` | Text cleaning implementation. |
| `src/io_utils.py` | Shared read/write helpers. |
| `src/checkpoint_utils.py` | Checkpoint utility helpers. |
| `src/coda_ir.py` | CODA request/response/message data contracts. |

### `src/adapters/`

| File | Purpose |
| --- | --- |
| `src/adapters/base.py` | Adapter ABC and lifecycle contract. |
| `src/adapters/registry.py` | Canonical backend-name to adapter registry. |
| `src/adapters/ollama_adapter.py` | Ollama HTTP adapter with stream support. |
| `src/adapters/anthropic_adapter.py` | Anthropic messages adapter. |
| `src/adapters/local_backend_adapter.py` | Wrap a local backend behind the adapter contract. |

### `src/runtime/`

| File | Purpose |
| --- | --- |
| `src/runtime/coda.py` | Main CODA runtime, episodic integration, and adapter wiring. |
| `src/runtime/front_matter_builder.py` | Build prompt front matter. |
| `src/runtime/front_matter_classifier.py` | Inspectable classifier for prompt intent and routing fields. |
| `src/runtime/front_matter_rules.py` | Rule definitions for front-matter classification. |
| `src/runtime/front_matter_schema.py` | Front-matter field schema. |
| `src/runtime/front_matter_renderer.py` | Render front matter for downstream use. |
| `src/runtime/response_plan_builder.py` | Choose backend, mode, overlays, and retrieval profile. |
| `src/runtime/mode_router.py` | Resolve mode files and overlays. |
| `src/runtime/prompt_compiler.py` | Assemble prompt blocks from modes and memory context. |
| `src/runtime/frame_policy.py` | Runtime framing rules. |
| `src/runtime/session.py` | Session helpers. |
| `src/runtime/ollama_client.py` | Existing Ollama streaming helper retained underneath the adapter layer. |

### `src/memory/`

| File | Purpose |
| --- | --- |
| `src/memory/node_schema.py` | Vault node and provenance data structures. |
| `src/memory/memory_store.py` | Read/write helpers for vault nodes and edges. |
| `src/memory/extract_nodes.py` | Extract nodes from configured sources. |
| `src/memory/classify_nodes.py` | Assign node types and trust layers. |
| `src/memory/normalize_sources.py` | Normalize source material before extraction. |
| `src/memory/build_edges.py` | Build graph edges between nodes. |
| `src/memory/index_graph.py` | Graph indexing helpers. |
| `src/memory/index_semantic.py` | Semantic retrieval with embedding path and lexical fallback. |
| `src/memory/index_temporal.py` | Temporal indexing helpers. |
| `src/memory/index_phase.py` | Life-phase indexing helpers. |
| `src/memory/index_voice.py` | Voice-axis indexing helpers. |
| `src/memory/index_reinforcement.py` | Reinforcement indexing helpers. |
| `src/memory/retrieve_topk.py` | Multi-signal retrieval entrypoint. |
| `src/memory/score_fusion.py` | Weighted fusion across semantic, temporal, phase, project, graph, voice, reinforcement, confidence. |
| `src/memory/query_classifier.py` | Classify queries into retrieval profiles. |
| `src/memory/update_reinforcement.py` | Reinforcement update path. |
| `src/memory/consolidate_memories.py` | Consolidation helper. |
| `src/memory/async_indexer.py` | Remote Ollama embedding daemon that writes a sidecar embeddings file. |
| `src/memory/gguf_mining.py` | GGUF tensor-mining helper that emits capability-seed nodes. |
| `src/memory/graph_router.py` | Derive per-turn behavioral contract from retrieved graph structure. |

### Other source subpackages

| Path | Purpose |
| --- | --- |
| `src/episodic/` | Older SQLite episodic-memory lane retained alongside the vault graph. |
| `src/eval/` | Eval helpers. |
| `src/translation/` | Runtime-context and training-artifact translation logic. |
| `src/handoff/` | Scope-map load, resolve, and validation helpers. |
| `src/model_backends/` | Scratch, pretrained, and Qwen2.5-Omni backend implementations. |

## `agent/` Index

| File | Purpose |
| --- | --- |
| `agent/src/server.ts` | HTTP chat surface that pre-retrieves graph state before model execution. |
| `agent/src/cli.ts` | Terminal chat loop. |
| `agent/src/memory.ts` | Node-to-Python subprocess bridge for `scripts/query_memory.py`. |
| `agent/src/craig.ts` | OpenAI-backed agent definition, tools, and instructions. |
| `agent/src/craig-local.ts` | Local OpenAI-compatible / LM Studio-backed variant. |
| `agent/package.json` | Agent package dependencies and scripts. |

## `frontend/` Index

| Path | Purpose |
| --- | --- |
| `frontend/src/App.tsx` | Frontend application root. |
| `frontend/src/Chat.tsx` | Main chat component. |
| `frontend/src/ChatWidget.tsx` | Widget/chat shell component. |

## `exports/user_model_package/method_vault/` Index

### Root vault contracts

| Path | Purpose |
| --- | --- |
| `exports/user_model_package/method_vault/_method.md` | Root vault constitution for method resolution. |
| `exports/user_model_package/method_vault/README.md` | Branch README for the vault scope. |
| `exports/user_model_package/method_vault/AGENTS.md` | Branch read order and rules. |

### Corpus, tokenizer, and weights

| Path | Purpose |
| --- | --- |
| `corpus/_method.md` | Parent corpus behavior. |
| `corpus/conversation/_method.md` | Conversation-specific corpus behavior. |
| `tokenizer/_method.md` | Parent tokenizer behavior. |
| `tokenizer/default/_method.md` | Default tokenizer behavior. |
| `weights/_method.md` | Parent weight behavior. |
| `weights/architecture/_method.md` | Architecture-resolution branch. |
| `weights/architecture/tiny_scratch/_method.md` | Tiny scratch architecture profile. |
| `weights/architecture/craig_target/_method.md` | Serious target architecture profile. |
| `weights/scratch/_method.md` | Scratch-training behavior. |
| `weights/sft/_method.md` | SFT behavior. |

### CODA, donor, and substrate

| Path | Purpose |
| --- | --- |
| `coda/_method.md` | Adapter-contract and CODA orchestration rules. |
| `process_mind/_method.md` | Root Copilot process-mind stack. |
| `process_mind/layer1/_method.md` | Novelty pressure and mutation rules. |
| `process_mind/layer2/_method.md` | Reasoning-trace and pattern-rejection layer. |
| `process_mind/layer3/_method.md` | Donor objective and transition rules. |
| `vaultization/_method.md` | Overall vaultization contract. |
| `vaultization/dolphin/_method.md` | Dolphin donor-pass workflow. |
| `vaultization/qwen2_5_omni_7b/_method.md` | Exact-donor Qwen contrast workflow. |
| `substrate/_method.md` | Pulse-cell schema. |
| `substrate/pulse_winner_policy.md` | Winner selection and promotion rule. |
| `substrate/cells/` | Promoted active substrate baseline. |
| `substrate/dolphin_pass/` | Dolphin staging cells. |
| `substrate/qwen2_5_omni_7b_pass/` | Qwen staging cells. |

## Data Index

### Branches

| Path | Purpose |
| --- | --- |
| `data/raw/` | Preserved source material, staged imports, personal inputs, converted text. |
| `data/clean/` | Normalized outputs suitable for retrieval and tokenizer use. |
| `data/pretrain/` | Pretraining-ready plain-text corpora. |
| `data/sft/` | SFT JSONL examples. |
| `data/prefs/` | Preference comparison records. |
| `data/eval/` | Eval JSONL records. |

### Important subpaths

| Path | Purpose |
| --- | --- |
| `data/raw/conversation_exports/markdown_export_raw/` | Imported one-markdown-per-conversation corpus. |
| `data/clean/conversation_exports/markdown_export_raw/threads/` | Turn-ordered transcript files used by retrieval and tokenization. |
| `data/pretrain/conversation_exports/markdown_export_raw/` | Conversation-derived pretraining corpora. |
| `data/sft/conversation_exports/markdown_export_raw/` | Conversation-derived reply-pair outputs. |
| `data/raw/examples/` | Small curated source seeds. |
| `data/raw/personal/` | Personal source branch. |
| `data/raw/converted/` | Voice-converted raw texts. |

## Artifact Index

| Path | Purpose |
| --- | --- |
| `artifacts/corpus/` | Prepared corpus and manifest. |
| `artifacts/tokenizers/default/` | Live tokenizer artifacts. |
| `artifacts/reports/` | Tokenizer and corpus reports. |
| `artifacts/checkpoints/` | Scratch and smoke checkpoints. |
| `artifacts/models/` | Scratch-model metadata. |
| `artifacts/eval_reports/` | Eval outputs. |
| `artifacts/methods/` | Method-vault resolution outputs. |
| `artifacts/vault/` | Nodes, edges, graph reports, mined-node outputs. |
| `artifacts/embeddings/` | Local embedding-model cache. |
| `artifacts/episodic/` | Older episodic-memory storage. |
| `artifacts/samples/` | Sample generations. |

## Tests

| File | Purpose |
| --- | --- |
| `tests/test_scope_map.py` | Scope routing and validation rules. |
| `tests/test_l1_routing.py` | Pure route-layer semantics. |
| `tests/test_coda_ir.py` | IR contract coverage. |
| `tests/test_coda_wiring.py` | Runtime-to-adapter smoke coverage. |
| `tests/test_qwen2_5_omni_backend.py` | Qwen2.5-Omni backend registration and text-only path coverage. |

## Sparse Or Experimental Side Branches

| Path | Purpose |
| --- | --- |
| `cog/src/cog.c` | Experimental C-side stub for the `cog` branch. |
| `cog/src/cog.h` | Header companion for the experimental `cog` branch. |
| `cog/model/cells/` | Placeholder directory for model-cell structure in the `cog` branch. |
| `cog/spec/` | Placeholder spec directory for the `cog` branch. |

## Practical Use

If you only need the shortest current navigation:

1. read the root handoff docs first
2. use `SCOPE_MAP.yaml`
3. use the branch README for the active scope
4. use this file when you need the repo-wide structural picture rather than one branch
