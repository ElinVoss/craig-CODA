# Data

This branch contains the shared local data core for `craig-CODA`.
Everything else in the repo leans on this branch, even when the active work is runtime or donor-oriented.

## Branches

- `raw/` - preserved source material and staged imports
- `clean/` - normalized outputs used by retrieval and tokenization
- `pretrain/` - plain-text corpora for origin experiments
- `sft/` - supervised fine-tuning examples
- `prefs/` - ranked preference pairs
- `eval/` - evaluation records

## Current State

- raw conversation exports are preserved under `raw/conversation_exports/markdown_export_raw/`
- normalized turn-ordered transcripts exist under `clean/conversation_exports/markdown_export_raw/threads/`
- conversation-derived pretraining text exists under `pretrain/conversation_exports/markdown_export_raw/`
- conversation-derived SFT reply pairs exist under `sft/conversation_exports/markdown_export_raw/`
- older generic sample files still exist alongside the newer conversation-native corpus
- data lineage matters here:
  - raw stays raw
  - clean is derived
  - pretrain / sft / prefs / eval are outputs, not replacement truth

## Important Reality

- imported conversation markdown is now a first-class corpus family in this repo
- the graph and tokenizer lanes both depend on the clean thread transcripts
- do not collapse the imported conversation branch into generic "document" handling

## Continue From Here

You are in the `data` scope.

Read in this order:

1. `README.md`
2. `raw/conversation_exports/markdown_export_raw/`
3. `clean/conversation_exports/markdown_export_raw/threads/`
4. `pretrain/conversation_exports/markdown_export_raw/`
5. `sft/conversation_exports/markdown_export_raw/`
6. `prefs/`
7. `eval/`

If the user asks how the conversation corpus got here, trace into:

- `scripts/import_markdown_export_raw.py`
- `scripts/normalize_markdown_export_raw.py`
- `scripts/prepare_corpus.py`

Keep `D:\craig-CODA\LIVE_HANDOFF.md` current between meaningful actions.
