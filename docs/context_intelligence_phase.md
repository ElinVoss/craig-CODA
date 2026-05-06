# Context Intelligence Phase

## Purpose

The Context Intelligence Phase adds a structured external-memory and translation layer around the existing Craig runtime. It preserves:

- the scratch lane
- the pretrained backend lane
- the current mode router
- the current prompt compiler
- the existing Craig / Elin / RS-1 runtime modes
- the forbidden auto-load behavior for review-only material

This phase is about translating vault material into runtime context and future training artifacts without pretending every note belongs in weights.

## Runtime architecture

The runtime now has an inspectable pre-routing phase:

```text
raw prompt
-> prompt front matter builder
-> response plan builder
-> mode router
-> memory retrieval
-> prompt compiler
-> backend
```

### Prompt Front Matter

Prompt front matter is a small rule-based classifier implemented in:

- `src/runtime/front_matter_schema.py`
- `src/runtime/front_matter_rules.py`
- `src/runtime/front_matter_classifier.py`
- `src/runtime/front_matter_builder.py`
- `src/runtime/front_matter_renderer.py`
- `src/runtime/response_plan_builder.py`

It emits fields such as:

- `intent`
- `task_type`
- `mode`
- `domain`
- `style`
- `reasoning_mode`
- `memory_scope`
- `retrieval_profile`
- `output_format`
- `tooling`
- `stakes`
- `uncertainty_policy`
- `privacy_level`
- `confidence`

The response plan converts those signals into:

- selected backend
- selected mode
- optional context-file inclusion
- RS-1 overlay flags
- retrieval profile
- memory top-k
- output shape

Manual overrides are supported by the builder and by the generation CLIs for mode, retrieval profile, and memory top-k.

## Vault graph

Vault building is implemented in:

- `src/memory/normalize_sources.py`
- `src/memory/extract_nodes.py`
- `src/memory/classify_nodes.py`
- `src/memory/build_edges.py`
- `src/memory/memory_store.py`
- `src/memory/gguf_mining.py` (offline GGUF capability-seed miner)

The default source roots are conservative and live in `configs/vault_translation.yaml`.
Node schema now includes optional `extracted_from` provenance metadata for mined capability nodes. This tracks model name, tensor name, optional layer/head indexes, activation pattern label, and mining timestamp.
Raw conversation markdown exports can be staged under `data/raw/conversation_exports/markdown_export_raw/` and then normalized into `data/clean/conversation_exports/markdown_export_raw/threads/`. The active retrieval/tokenization layer uses those turn-ordered thread transcripts so the corpus is observed as conversation rather than as serialized export JSON.

### Trust layers

Trust layers are defined in `configs/node_schema.yaml`:

- `stable_core`
- `project_constraints`
- `episodic_events`
- `prose_voice`
- `interpretive_maps`
- `review_only`

Rules:

- `stable_core` can feed runtime and training translation.
- `project_constraints` can feed runtime and selective training translation.
- `episodic_events` are mostly runtime memory and only selectively training eligible.
- `prose_voice` feeds prose/style outputs.
- `interpretive_maps` are reference material, not stable truth.
- `review_only` is never auto-loaded into runtime and never translated into training outputs.

## Retrieval

Retrieval is implemented in:

- `src/memory/index_semantic.py`
- `src/memory/index_temporal.py`
- `src/memory/index_phase.py`
- `src/memory/index_graph.py`
- `src/memory/index_reinforcement.py`
- `src/memory/index_voice.py`
- `src/memory/query_classifier.py`
- `src/memory/score_fusion.py`
- `src/memory/retrieve_topk.py`
- `src/memory/update_reinforcement.py`
- `src/memory/consolidate_memories.py`

The retrieval stack uses weighted score fusion with profile-specific weights from `configs/memory_query_profiles.yaml`.

### Important limitation

Semantic matching supports an embedding-backed CPU path configured in `configs/memory_retrieval.yaml`. The scorer uses a local SentenceTransformer model when available and falls back to lexical overlap if the model cannot be loaded.

## Translation outputs

Translators share the same node graph:

- `src/translation/runtime_context_translator.py`
- `src/translation/sft_translator.py`
- `src/translation/preference_translator.py`
- `src/translation/prose_translator.py`
- `src/translation/adapter_manifest_translator.py`

Output directories:

- `artifacts/vault/nodes.jsonl`
- `artifacts/vault/edges.jsonl`
- `artifacts/vault/index_reports/`
- `artifacts/memory/runtime_context/`
- `artifacts/memory/consolidation_reports/`
- `artifacts/translation/sft/`
- `artifacts/translation/prefs/`
- `artifacts/translation/prose/`
- `artifacts/translation/adapter_manifests/`
- `artifacts/methods/` for resolved vault-driven corpus/tokenizer/weight method configurations

## Vault-driven method control

Corpus preparation, tokenizer behavior, and weight/SFT parameter choices can be derived from `exports/user_model_package/method_vault/`.
The resolver walks parent and child folders, reads `_method.md` notes, merges their `config:` front matter in order, and writes the resolved method bundle to `artifacts/methods/`.

This makes the effective method stack inspectable in a vault-like format rather than hiding it entirely in flat YAML files.

## Deferred items

Explicitly deferred in this phase:

- adapter training
- adapter merging
- LoRA workflows
- pretrained weight modification
- cloud services
- distributed systems
- auto-ingesting personal folders by default
