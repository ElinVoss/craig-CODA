# craig-CODA

## Read Every Word Before Working

If you are a model being pointed at this directory for work, read every word in this README before doing meaningful work.
There is a continuation prompt at the end of the root handoff path.
Do not skim for headings and do not begin with broad repo search.
Use the user-given scope and follow `SCOPE_MAP.yaml`.
You must also read `LIVE_HANDOFF.md` and keep updating that same file between meaningful actions so the next model inherits the freshest operational state.

## What This Repo Is Now

`craig-CODA` is a Windows-friendly, local-first, CPU-first workspace that now spans five connected layers:

- a root handoff and continuity system that keeps model-to-model transitions from drifting
- a shared local data core for raw exports, cleaned transcripts, pretraining text, SFT pairs, preferences, and evals
- a graph-native memory and runtime stack with route classification, vault retrieval, prompt compilation, and adapter-backed execution
- a local agent surface, browser surface, and CLI surface for interacting with that stack
- a method-vault and donor-vaultization layer for extracting, mutating, promoting, and later refilling a living substrate

This repo did not stay a plain training lab.
It started that way, but the current center of gravity is broader:

- preserve and normalize source material
- resolve behavior from vault-authored notes where possible
- route prompts through explicit runtime layers instead of one opaque model call
- use graph structure to shape what the system is allowed to say
- extract donor residue, mutate overlap zones, and promote substrate cells
- eventually strip donor identity from the working structure and refill it with Craig-authored self material

## What Is Real Today

The following are already real in this checkout:

- scratch-training and SFT scaffolds exist under `src/` and `scripts/`
- tokenizer preparation, training, and inspection are implemented and have produced artifacts
- imported one-markdown-per-conversation corpora exist under `data/raw/conversation_exports/markdown_export_raw/`
- normalized turn-ordered conversation transcripts exist under `data/clean/conversation_exports/markdown_export_raw/threads/`
- model architecture now resolves from the method vault, with JSON resolution artifacts written under `artifacts/methods/`
- the CODA intermediate representation and adapter contract exist under `src/coda_ir.py` and `src/adapters/`
- the pure L1 route/classify layer exists under `runtime/` and is backed by `graph/` route rules
- the richer runtime package exists under `src/runtime/`
- vault graph extraction, retrieval, async indexing, GGUF mining, and graph-derived routing exist under `src/memory/`
- the agent surface pre-retrieves graph state and injects both `[GRAPH ROUTING]` and `[MEMORY CONTEXT]` before the model sees the user turn
- donor vaultization is no longer hypothetical: Dolphin and exact-donor Qwen2.5-Omni-7B passes both exist, and a promoted substrate baseline exists under `exports/user_model_package/method_vault/substrate/cells/`

## What Is Not Finished

The following are still unresolved and should not be overstated:

- the tiny scratch lane is real, but not coherent enough yet to justify strong model claims
- the `craig_target` architecture profile exists as the serious target shape, but it has not been trained
- the graph-derived routing layer is real, but it still shapes a model call by injected contract text rather than replacing the deeper computation
- the frontend is still a minimal chat surface, not the primary continuity layer
- depersonalization, refill, and heartbeat-grade stability remain design-frontier work rather than settled implementation

## Root Control Docs

Read these before leaving the root handoff path:

- `CURRENT_STATE.md` - the best concise picture of what is working now
- `DECISIONS.md` - the decisions that are already locked and the ones that are not
- `NEXT_STEPS.md` - the active queue and the longer arc after the handoff layer
- `ARTIFACTS.md` - the main artifact families and deep references
- `HANDOFF_PROMPT.md` - the startup contract of record
- `LIVE_HANDOFF.md` - the shared baton file
- `MASTER_HANDOVER_NEXT_SESSION.md` - the long-form continuity bridge across sessions
- `MASTER_INDEX.md` - the current structural index of the repo
- `SCOPE_MAP.yaml` - scope routing contract for every major branch

## Active Scope Names

- `handoff`
- `vault`
- `tokenizer`
- `weights`
- `memory`
- `runtime`
- `coda`
- `frontend`
- `agent`
- `configs`
- `artifacts`
- `data`

## Major Branches

| Branch | What it owns |
| --- | --- |
| root handoff | continuity, scope routing, baton state, current-state docs |
| `configs/` | YAML contracts for data, runtime, retrieval, backends, front matter, and training |
| `data/` | raw imports, clean transcripts, pretraining text, SFT pairs, preferences, eval data |
| `scripts/` | execution surface for ingest, normalize, build, train, inspect, compare, validate |
| `src/` | core Python implementation: vault methods, training, runtime, memory, adapters, handoff utilities |
| `runtime/` | pure L1 prompt classification and route engine |
| `agent/` | HTTP and CLI agent surfaces backed by the runtime and vault graph |
| `frontend/` | React/Vite browser chat surface |
| `graph/` | prompt-axis and route-rule declarations for the L1 route layer |
| `exports/user_model_package/method_vault/` | vault-authored behavior, donor extraction rules, substrate rules, architecture profiles |
| `artifacts/` | generated corpus, tokenizer, model, eval, vault, and resolution outputs |
| `tests/` | runtime, routing, adapter, scope-map, and backend smoke coverage |

## Top-Level Map

```text
craig-CODA/
  AGENTS.md                          Root contract for assistants entering this repo
  README.md                          Root architecture and navigation guide
  CURRENT_STATE.md                   What is real now
  DECISIONS.md                       Locked and unresolved decisions
  NEXT_STEPS.md                      Immediate queue and longer-range arc
  ARTIFACTS.md                       Generated-output and artifact map
  HANDOFF_PROMPT.md                  Startup contract of record
  LIVE_HANDOFF.md                    Shared baton file
  MASTER_HANDOVER_NEXT_SESSION.md    Long-form session bridge
  MASTER_INDEX.md                    Exhaustive current-state structural index
  SCOPE_MAP.yaml                     Scope router contract

  agent/                             Local HTTP and CLI agent surfaces
  artifacts/                         Generated tokenizer, model, vault, and eval outputs
  cog/                               Sparse experimental field/C branch
  configs/                           YAML contracts
  data/                              Shared local data core
  docs/                              Architecture notes and design specs
  eval/                              Retrieval test suite and result logs
  examples/                          Example prompts and fixtures
  exports/                           User model package and method vault
  frontend/                          Browser UI
  graph/                             L1 route axes, capability nodes, constraints, route rules
  runtime/                           Pure L1 classify/route layer
  scripts/                           Executable pipeline and validation surface
  src/                               Core Python implementation
  tests/                             Smoke and contract tests
```

## How Requests Flow

There are now three related runtime surfaces:

### 1. Pure route surface

`runtime/classify_prompt.py` and `runtime/route_prompt.py` implement the L1 route layer.
This layer is intentionally simple and inspectable:

- classify a prompt into explicit axes
- match those axes against `graph/routes/route_rules.yaml`
- activate a constrained subgraph of capabilities and constraints

This layer has no backend calls and no vector search.
It exists to make route logic explicit and testable before the rest of the runtime gets involved.

### 2. Full runtime package

`src/runtime/` carries the richer runtime pipeline:

```text
raw prompt
-> front matter builder / classifier
-> response plan builder
-> mode router
-> memory retrieval
-> prompt compiler
-> backend adapter
```

This is where prompt shaping, vault directives, memory usage, and backend selection meet.

### 3. Agent surface

`agent/src/server.ts` and `agent/src/cli.ts` sit on top of the runtime and graph layers.
The live server path now does this before the model sees a user turn:

```text
user message
-> Python memory query bridge
-> graph-derived routing block
-> rendered memory context block
-> model run
```

That means the graph gets to speak first.
The model is no longer treated as the only seat of behavior.

## Data And Training Flow

The data and training side now has multiple linked stages:

1. import or place raw text-like material under `data/raw/`
2. normalize conversation exports into clean thread transcripts
3. prepare corpora and tokenizer artifacts
4. build placeholder SFT, preference, and eval outputs
5. train or inspect scratch and pretrained-local backends conservatively

Important reality:

- scratch training and SFT scaffolds exist
- checkpoint artifacts exist
- the scratch lane is still experimental
- the presence of training code is not proof of coherence

## Vault, Donor, And Substrate Flow

The method vault is no longer only about corpus and tokenizer settings.
It now also governs:

- architecture profiles
- CODA adapter rules
- process-mind layers
- donor vaultization workflows
- substrate schema and winner policy

The current donor path is:

- the local interactive agent mode as the internal process-mind host
- Dolphin as the first donor organism
- exact-donor `D:\.lmstudio\models\lmstudio-community\Qwen2.5-Omni-7B` as the second donor organism
- the expanded donor queue now continues with Gemini (pass 3), GPT (pass 4), Kimi (pass 5), Nemotron (pass 6), LLaMA (pass 7), and a contamination-flagged pass 8 for stricter cross-donor confirmation

The current substrate path is:

- collect donor specimens
- cluster residue
- mutate overlap zones
- promote winners into `substrate/cells/`
- refine activation and link structure
- later strip donor identity and refill the structure with Craig-authored self material

## Commands You Will Actually Use

### Root bring-up and validation

```powershell
python .\scripts\validate_data.py
python .\scripts\validate_scope_map.py
```

### Conversation import and normalization

```powershell
python .\scripts\import_markdown_export_raw.py
python .\scripts\normalize_markdown_export_raw.py
```

### Tokenizer and corpus pipeline

```powershell
python .\scripts\run_tokenizer_pipeline.py
python .\scripts\inspect_tokenizer.py
```

### Memory and vault graph

```powershell
python .\scripts\build_vault_graph.py
python .\scripts\inspect_vault_graph.py
python .\scripts\query_memory.py --query "Explain the current runtime path."
python .\scripts\run_async_indexer.py --once
python .\scripts\mine_gguf.py --gguf D:\gguf-models\Qwen3-4B-Instruct-2507-Q4_K_M.gguf
```

### Runtime and backend checks

```powershell
python .\scripts\list_backends.py
python .\scripts\validate_backends.py --all
python .\scripts\run_pretrained_generation.py --backend qwen2.5-1.5b-instruct --prompt "Summarize the local-first constraints."
python .\scripts\compare_backends.py --prompt "Summarize the local-first constraints."
```

### Training and eval

```powershell
python .\scripts\run_scratch_train.py
python .\scripts\run_sft_train.py
python .\scripts\run_eval_suite.py
```

### Agent surfaces

```powershell
cd .\agent
npm install
npm run dev
```

### Remote server host prep

```powershell
python .\scripts\setup_server_host.py --dest C:\CODA-SERVER --skip-probe
```

The helper will stage a normal GitHub clone even if the optional Qwen exact-donor host kit bundle is not present locally.

## Master Index

For the exhaustive current-state map, read `MASTER_INDEX.md`.
It absorbs the local additions that are absent from older GitHub snapshots and indexes the repo as it actually exists now.

## Continue From Here

If you are continuing work in this directory:

1. finish the root handoff path
2. read `SCOPE_MAP.yaml`
3. resolve the user's scope
4. follow only that branch

Do not start with broad repo search.
Do not re-derive the current repo state from scratch.
Take the continuation prompt from the branch you are routed into and work from there.
Keep `LIVE_HANDOFF.md` current while you work.
