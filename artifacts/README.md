# Artifacts

This branch contains generated outputs.
It is important, but it is not the branch where behavior should usually be edited.

## What Lives Here

- `corpus/` - prepared corpus and manifest
- `tokenizers/` - live tokenizer artifacts
- `reports/` - corpus and tokenizer reports
- `checkpoints/` - scratch and smoke checkpoints
- `models/` - model metadata
- `eval_reports/` - eval outputs
- `methods/` - method-vault resolution outputs
- `vault/` - built graph nodes, edges, graph reports, mined-node outputs
- `embeddings/` - local embedding-model cache
- `episodic/` - older episodic-memory storage
- `samples/` - sample generations

## Current State

- tokenizer artifacts and reports already exist and are meaningful
- architecture resolution artifacts already exist and prove the vault path is live
- vault graph outputs already exist and are not theoretical placeholders
- mined GGUF node outputs exist
- checkpoints exist, but their presence must not be over-read as proof of coherence

## Important Reality

- artifacts are evidence
- artifacts are not the canonical source definitions
- if a user wants behavior changed, the edit usually belongs in `configs/`, `scripts/`, `src/`, `runtime/`, or the method vault

## Continue From Here

You are in the `artifacts` scope.

Read in this order:

1. `README.md`
2. `../ARTIFACTS.md`
3. `corpus/`
4. `tokenizers/default/`
5. `reports/`
6. `methods/`
7. `vault/`
8. `checkpoints/`
9. `eval_reports/`

Keep `D:\craig-CODA\LIVE_HANDOFF.md` current between meaningful actions.
