# Scripts

This branch contains the direct execution surface for the repo.
If something gets imported, normalized, built, trained, inspected, compared, or validated, the entrypoint usually lives here.

## Script Families

### Data ingest and normalization

- `ingest_raw.py`
- `clean_text.py`
- `build_datasets.py`
- `run_pipeline.py`
- `import_markdown_export_raw.py`
- `normalize_markdown_export_raw.py`
- `extract_messages.py`

### Corpus and tokenizer

- `prepare_corpus.py`
- `train_tokenizer.py`
- `inspect_tokenizer.py`
- `run_tokenizer_pipeline.py`
- `tokenize_corpus.py`

### Runtime, memory, and graph

- `build_vault_graph.py`
- `inspect_vault_graph.py`
- `query_memory.py`
- `run_memory_ablation.py`
- `run_async_indexer.py`
- `mine_gguf.py`
- `build_training_artifacts.py`
- `run_vault_build.py`
- `vault_index.py`
- `vault_flatten.py`
- `vault_generate.py`

### Training, eval, and backend comparison

- `run_scratch_train.py`
- `run_sft_train.py`
- `run_sample_generation.py`
- `run_eval_suite.py`
- `list_backends.py`
- `validate_backends.py`
- `run_pretrained_generation.py`
- `compare_backends.py`

### Validation and operational helpers

- `validate_data.py`
- `validate_scope_map.py`
- `test_front_matter.py`
- `monitor_training.py`
- `run_qwen_manifest_openai_compat.py`
- `setup_server_host.py`

## Current State

- conversation import and normalization are now first-class script paths here
- the graph-memory query bridge is real and is consumed by the local agent server
- async indexing and GGUF mining are both present and no longer just conceptual notes
- handoff-system validation also lives here, because continuity is treated as executable contract rather than prose only
- a Windows-friendly server bootstrap helper now stages the GPU host workspace, copies the proven Qwen host kit when that optional bundle is present, and emits client/server env files plus an awakening drop area

## Continue From Here

You are in the `scripts` branch.

Read in this order:

1. `README.md`
2. `normalize_markdown_export_raw.py`
3. `prepare_corpus.py`
4. `query_memory.py`
5. `build_vault_graph.py`
6. `run_async_indexer.py`
7. `mine_gguf.py`
8. `validate_scope_map.py`

Then narrow to the exact family the user cares about instead of free-roaming the whole branch.

Keep `D:\craig-CODA\LIVE_HANDOFF.md` current between meaningful actions.
