# Current State

## What This Repo Is

`craig-CODA` is a Windows-friendly, local-first, CPU-first workspace for continuity-aware runtime work, graph-native memory work, corpus and tokenizer preparation, conservative local training experiments, and donor-to-substrate architecture work.

## What Is Already Working

### Root continuity and routing

- the root handoff system exists and is active:
  - `README.md`
  - `AGENTS.md`
  - `CURRENT_STATE.md`
  - `DECISIONS.md`
  - `NEXT_STEPS.md`
  - `ARTIFACTS.md`
  - `HANDOFF_PROMPT.md`
  - `LIVE_HANDOFF.md`
  - `MASTER_HANDOVER_NEXT_SESSION.md`
  - `SCOPE_MAP.yaml`
- scope resolution is implemented and validated:
  - `src/handoff/scope_map.py`
  - `scripts/validate_scope_map.py`
  - `tests/test_scope_map.py`

### Shared data core

- raw conversation export data is preserved under `data/raw/conversation_exports/markdown_export_raw/`
- cleaned turn-ordered conversation transcripts exist under `data/clean/conversation_exports/markdown_export_raw/threads/`
- pretraining text, SFT pairs, preferences, and eval examples exist in the expected branch folders under `data/`
- import and normalization are implemented:
  - `scripts/import_markdown_export_raw.py`
  - `scripts/normalize_markdown_export_raw.py`
  - `scripts/extract_messages.py`

### Corpus and tokenizer lane

- tokenizer preparation and training scripts exist and have been used successfully
- tokenizer artifacts exist under `artifacts/tokenizers/default/`
- corpus preparation artifacts exist under `artifacts/corpus/`
- inspection reports exist under `artifacts/reports/`

### Vault-authored method control

- the method vault exists under `exports/user_model_package/method_vault/`
- method notes currently drive corpus, tokenizer, scratch, SFT, and architecture resolution
- model architecture now resolves from the vault under `weights/architecture/`
- resolved architecture artifacts are written under `artifacts/methods/`
- `src/model_factory.build_model(profile=...)` consumes vault resolution; `configs/model_architecture.yaml` is now a legacy fallback only

### Route layer, runtime, and adapters

- the pure L1 route layer exists:
  - `runtime/classify_prompt.py`
  - `runtime/route_prompt.py`
  - `graph/axes/`
  - `graph/nodes/`
  - `graph/routes/route_rules.yaml`
  - `tests/test_l1_routing.py`
- the CODA intermediate representation and adapter contract are implemented:
  - `src/coda_ir.py`
  - `src/adapters/base.py`
  - `src/adapters/registry.py`
  - `src/adapters/ollama_adapter.py`
  - `src/adapters/anthropic_adapter.py`
  - `src/adapters/local_backend_adapter.py`
- `src/runtime/coda.py` now uses the richer runtime planning path and the vault graph retrieval lane:
  - `CodaRuntime._bootstrap_adapter()` registers canonical `ollama`, `local`, or `anthropic` targets on init
  - `CodaRuntime._plan_turn()` classifies the prompt, builds the response plan, optionally retrieves vault-graph memory, derives graph routing, compiles the mode prompt, and records runtime provenance into `CodaRequest.vault_directives`
  - `CodaRuntime.chat()` routes the planned request through `adapter.stream()` while preserving history and reinforcing retrieved graph nodes for later retrieval weighting
- the richer runtime package exists under `src/runtime/`:
  - front matter builder and classifier
  - response plan builder
  - mode router
  - prompt compiler
  - session logic

### Memory and graph stack

- the vault graph path exists under `src/memory/`
- conversation transcript extraction is treated specially
- retrieval supports lexical fallback, embedding-based semantic retrieval, and a first conservative spreading-activation pass through `src/memory/spreading_activation.py`
- the graph router exists:
  - `src/memory/graph_router.py`
  - graph structure now derives a routing block with posture, response mode, coverage, and blocked-layer behavior
- `scripts/audit_edges.py` now audits effective propagation eligibility across the live graph before deeper propagation tuning
- async indexing exists:
  - `src/memory/async_indexer.py`
  - `scripts/run_async_indexer.py`
  - `configs/async_indexing.yaml`
- GGUF mining exists:
  - `src/memory/gguf_mining.py`
  - `scripts/mine_gguf.py`
  - `configs/gguf_mining.yaml`
- vault graph outputs exist under `artifacts/vault/`
- local embedding model cache exists under `artifacts/embeddings/all-MiniLM-L6-v2`

### Agent and local interaction surfaces

- the local agent surface exists under `agent/`
- `agent/src/server.ts` pre-retrieves graph state before model execution
- `agent/src/memory.ts` bridges Node to Python `scripts/query_memory.py`
- `agent/src/craig.ts` defines the OpenAI-backed agent contract and tools
- `agent/src/craig-local.ts` defines the local OpenAI-compatible variant
- `agent/src/cli.ts` provides the terminal loop
- `scripts/setup_server_host.py` now stages the remote GPU server workspace:
  - copies the existing Qwen other-machine host kit when that optional bundle is present
  - writes `.env.server` plus `client_connection.env`
  - creates `awaken_payload/` for later bootstrap delivery
  - emits `bootstrap_report.json` with LM Studio detection and probe status
- the frontend exists under `frontend/`, but remains a minimal chat-oriented browser surface rather than the main continuity layer

### Training and backend lanes

- local scratch-training and SFT scaffolds exist in `src/train_scratch.py`, `src/train_sft.py`, `scripts/run_scratch_train.py`, and `scripts/run_sft_train.py`
- recorded scratch and smoke training runs exist under `artifacts/checkpoints/`
- tiny scratch model metadata and eval reports exist under `artifacts/models/` and `artifacts/eval_reports/`
- the pretrained backend registry exists in `configs/pretrained_backends.yaml`
- a dedicated Qwen2.5-Omni text-only backend path exists:
  - `src/model_backends/qwen2_5_omni_backend.py`
  - backend type `qwen2_5_omni` is registered
  - `tests/test_qwen2_5_omni_backend.py` exists

### Donor, vaultization, and substrate lane

- the process-mind stack is authored under `exports/user_model_package/method_vault/process_mind/`
- the vaultization contract is authored under `exports/user_model_package/method_vault/vaultization/`
- the living substrate pulse-cell schema is authored under `exports/user_model_package/method_vault/substrate/_method.md`
- the first pulse-winner policy is written in `substrate/pulse_winner_policy.md`
- the active promoted substrate baseline exists under `substrate/cells/`
- the Dolphin donor pass exists under `vaultization/dolphin/`
- the exact-donor Qwen2.5-Omni-7B contrast pass exists under `vaultization/qwen2_5_omni_7b/`
- the standalone host-kit repo used for second-machine exact-donor collection exists under `vaultization/qwen2_5_omni_7b/host_kit_repo/`
- the Craig behavioral reference package is now imported under `vaultization/craig_behavioral_reference/` — 7 behavioral categories, 80 prompts each (560 total), 50 assertions each (350 total), plus 10 core rules; this is the shared stimulus source for all new donor passes
- five new donor vaultization passes are scaffolded: Gemini (pass 3), GPT (pass 4, decision reversal), Kimi (pass 5), Nemotron (pass 6), LLaMA (pass 7) — each has a `_method.md` under `vaultization/{donor}/`
- an additional contamination-flagged donor pass (pass 8) now exists in the vaultization lane; category A is already imported and carries a stricter contamination flag for Layer 2 evaluation

## What Is Also Present

- `eval/` contains retrieval evaluation fixtures and run logs
- `examples/` contains prompt examples
- `docs/` contains architecture notes and handoff design specs
- `graph-native-complete-handoff.md` remains as a deeper reference document
- `cog/` exists as a sparse experimental branch with C stubs and placeholder structure

## What Is Still Unresolved

- the tiny scratch model loss is still high and the output is not coherent enough for strong claims
- the `craig_target` profile has not been trained
- some older provenance still points back to `D:\Model-Lab`, which remains easy to confuse with current `D:\craig-CODA` state
- the frontend is still minimal and is not the main continuity or runtime-debug surface
- the exact local `Qwen2.5-Omni-7B` donor path is still not runnable on this machine even though the pass was completed from a second Windows host
- the graph-derived routing layer is real, but it still speaks to the backend through injected contract text rather than replacing the deeper computation
- the substrate winner set exists, but keyword refinement, runtime influence, depersonalization, and refill remain ahead

## What Is Active Right Now

- keep the handoff system and branch docs synchronized with the actual code and artifact state
- keep scope routing explicit and testable
- keep the runtime local, deterministic, and CPU-first by default
- keep training and eval claims evidence-based while the scratch lane remains experimental
- keep the L1 route layer, the richer runtime package, and the agent bridge conceptually separate
- keep the donor passes stable while refining the promoted substrate baseline
- keep the longer-range target visible: vault-governed orchestration first, Craig-native refill later
