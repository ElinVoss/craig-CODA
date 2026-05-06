# Decisions

## Satisfied Decisions

- Preserve raw conversation exports unchanged.
- Normalize conversations into thread transcripts before retrieval and tokenization.
- Treat conversation data as conversation, not generic JSON chunks.
- Use an Obsidian-like method vault with parent-to-child `_method.md` notes for corpus, tokenizer, and training behavior.
- Use a scope router so assistants follow the user-given branch instead of broad repo search.
- Keep the handoff system installed at the root and in every meaningful work branch.
- Keep the trained tiny scratch lane clearly separated from the untrained `craig-coda-0.6b` target config.
- Model architecture resolves from the vault — `weights/architecture/` holds named profiles; `configs/model_architecture.yaml` is a legacy fallback only.
- Treat the vault compiler, shared intermediate representation, model adapters, and CODA orchestration layer as the real invariant, not any one open model backend.
- Use Copilot IDE agent mode as the current internal vaultimization process-mind host.
- Use Dolphin as the first donor organism and `D:\.lmstudio\models\lmstudio-community\Qwen2.5-Omni-7B` as the second donor organism.
- Keep GPT-5 outside the donor body as an external teacher/comparator only.
- Exclude Gemini from the donor architecture.
- Treat the first living-substrate unit as a meaning-centered pulse cell with context shell, pulse signature, and bidirectional links.
- When donor overlap is detected, trigger immediate mutation, allow no compatibility bias, and preserve purpose only.

## Unsatisfied Decisions

- Root handoff files still need to stay synchronized with the real checkpoint and eval state as the repo changes.
- Eval quality for the scratch lane is still too weak to support stronger model claims.
- The craig_target profile has not been trained yet.
- ~~The Copilot layered process-mind stack still needs to be authored.~~ **Satisfied** — `process_mind/_method.md` + 3 layer notes authored.
- ~~The Dolphin-first vaultization workflow still needs to be defined as a concrete donor pass.~~ **Satisfied** — `vaultization/dolphin/_method.md` authored.
- ~~The living substrate pulse cell schema needs to be specified.~~ **Satisfied** — `substrate/_method.md` authored with full YAML schema.
- The Qwen2.5-Omni-7B contrast pass is satisfied by exact-donor outputs collected on a second Windows LM Studio host and imported back into this repo.
- The first pulse winner policy is now satisfied: overlap zones promote mutated purpose-only winners, while unique donor residue can promote as donor-native.
- The long-range test path still needs a deliberate depersonalization-and-refill phase: preserve the working orchestration heartbeat structure, strip source-model personality, restraints, and weighted identity, then repopulate that structure with vault-authored self data and date-aware memory behavior.

## Do Not Violate

- Stay local-first.
- Stay Windows-friendly.
- Do not pretend training or architecture work is complete when it is not.
- Do not replace the current repo structure casually.
- Do not start with broad repo wandering when the user has already given a scope.
