# Artifacts

## Root Continuity And Reference Documents

- `CURRENT_STATE.md`
- `DECISIONS.md`
- `NEXT_STEPS.md`
- `HANDOFF_PROMPT.md`
- `LIVE_HANDOFF.md`
- `MASTER_HANDOVER_NEXT_SESSION.md`
- `MASTER_INDEX.md`
- `graph-native-complete-handoff.md`
- `docs/superpowers/specs/2026-05-04-scope-routed-handoff-system-design.md`

## Core Corpus And Tokenizer Outputs

- `data/clean/conversation_exports/markdown_export_raw/threads/`
- `data/pretrain/conversation_exports/markdown_export_raw/conversation_threads.txt`
- `data/pretrain/conversation_exports/markdown_export_raw/conversation_utterances.txt`
- `data/sft/conversation_exports/markdown_export_raw/reply_pairs.jsonl`
- `artifacts/corpus/prepared_corpus.txt`
- `artifacts/corpus/prepared_corpus_manifest.json`
- `artifacts/reports/corpus_prep_report.txt`
- `artifacts/tokenizers/default/tokenizer.json`
- `artifacts/tokenizers/default/tokenizer_config.json`
- `artifacts/tokenizers/default/special_tokens_map.json`
- `artifacts/tokenizers/default/training_info.json`
- `artifacts/reports/tokenizer_report.json`
- `artifacts/reports/tokenizer_report.txt`
- `artifacts/reports/conversation_threads_token_stats.json`
- `artifacts/reports/conversation_utterances_token_stats.json`

## Training, Backend, And Eval Outputs

- `artifacts/checkpoints/tiny-qwen3-scratch/`
- `artifacts/checkpoints/tiny-qwen3-smoke/`
- `artifacts/checkpoints/training_scratch.smoke.yaml`
- `artifacts/models/tiny-qwen3-scratch/model_metadata.json`
- `artifacts/eval_reports/eval_report.json`
- `artifacts/eval_reports/eval_report.txt`
- `artifacts/eval_reports/eval_report_smoke.json`
- `artifacts/eval_reports/eval_report_smoke.txt`
- `artifacts/qwen2_5_omni_7b_offload/`
- `eval/retrieval_test_suite.yaml`
- `eval/results/`

## Vault, Memory, And Translation Outputs

- `artifacts/methods/architecture_tiny_scratch_resolution.json`
- `artifacts/methods/architecture_craig_target_resolution.json`
- `artifacts/vault/nodes.jsonl`
- `artifacts/vault/edges.jsonl`
- `artifacts/vault/index_reports/graph_summary.json`
- `artifacts/vault/mined_nodes/Qwen3-4B-Instruct-2507-Q4_K_M.jsonl`
- `artifacts/embeddings/all-MiniLM-L6-v2/`
- `artifacts/episodic/`

## Method Vault, Donor, And Substrate Outputs

- `exports/user_model_package/method_vault/`
- `exports/user_model_package/method_vault/process_mind/_method.md`
- `exports/user_model_package/method_vault/process_mind/layer1/_method.md`
- `exports/user_model_package/method_vault/process_mind/layer2/_method.md`
- `exports/user_model_package/method_vault/process_mind/layer3/_method.md`
- `exports/user_model_package/method_vault/coda/_method.md`
- `exports/user_model_package/method_vault/vaultization/craig_behavioral_reference/` — shared Craig behavioral stimulus package (7 categories, 560 prompts, 350 assertions, 10 core rules); used as the input source for all new donor passes
- `exports/user_model_package/method_vault/vaultization/gemini/_method.md`
- `exports/user_model_package/method_vault/vaultization/gpt/_method.md`
- `exports/user_model_package/method_vault/vaultization/kimi/_method.md`
- `exports/user_model_package/method_vault/vaultization/nemotron/_method.md`
- `exports/user_model_package/method_vault/vaultization/llama/_method.md`
- `exports/user_model_package/method_vault/vaultization/dolphin/_method.md`
- `exports/user_model_package/method_vault/vaultization/dolphin/specimens/prompt_set.json`
- `exports/user_model_package/method_vault/vaultization/dolphin/specimens/raw_responses.json`
- `exports/user_model_package/method_vault/vaultization/dolphin/specimens/dolphin_pass_analysis.yaml`
- `exports/user_model_package/method_vault/vaultization/qwen2_5_omni_7b/_method.md`
- `exports/user_model_package/method_vault/vaultization/qwen2_5_omni_7b/specimens/prompt_set.json`
- `exports/user_model_package/method_vault/vaultization/qwen2_5_omni_7b/specimens/raw_responses.json`
- `exports/user_model_package/method_vault/vaultization/qwen2_5_omni_7b/specimens/qwen_pass_analysis.yaml`
- `exports/user_model_package/method_vault/vaultization/qwen2_5_omni_7b/host_kit_repo/`
- `exports/user_model_package/method_vault/substrate/_method.md`
- `exports/user_model_package/method_vault/substrate/pulse_winner_policy.md`
- `exports/user_model_package/method_vault/substrate/cells/`
- `exports/user_model_package/method_vault/substrate/dolphin_pass/`
- `exports/user_model_package/method_vault/substrate/qwen2_5_omni_7b_pass/`

## Source Files That Produce Or Verify Artifacts

- `src/vault_methods.py`
- `src/model_backends/qwen2_5_omni_backend.py`
- `src/memory/async_indexer.py`
- `src/memory/gguf_mining.py`
- `src/memory/graph_router.py`
- `tests/test_qwen2_5_omni_backend.py`
- `tests/test_coda_ir.py`
- `tests/test_coda_wiring.py`
- `tests/test_l1_routing.py`
- `tests/test_scope_map.py`
