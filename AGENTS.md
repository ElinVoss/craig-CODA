# Repo Contract

## Agent Entry Workflow

When an assistant enters this directory, it must not begin with broad repo search.

Required read order before meaningful work:

1. Read `README.md` fully.
2. Read `CURRENT_STATE.md`.
3. Read `DECISIONS.md`.
4. Read `NEXT_STEPS.md`.
5. Read `ARTIFACTS.md`.
6. Read `LIVE_HANDOFF.md` before meaningful work.
7. Read `HANDOFF_PROMPT.md`.
8. Read `SCOPE_MAP.yaml`.
9. Resolve the user-given scope or natural onboarding phrase.
10. Follow only the mapped `read_order` for that scope.
11. Read local `AGENTS.md` and local `README.md` whenever the route enters a scoped branch.
12. Start work from that branch's `Continue From Here` prompt.
13. Update `LIVE_HANDOFF.md` between every meaningful action so the next model inherits the freshest state.

If the user says something like `check out what ive got going`, `bring yourself up to speed`, or `learn this directory`, route to the `handoff` scope first.
If the scope is still ambiguous after alias matching, ask the user to choose among the named scopes instead of wandering the repo.

`LIVE_HANDOFF.md` is the shared baton file. If true asynchronous updating is not possible in the current environment, update it immediately after each meaningful action and before the next one.

## Purpose

`craig-CODA` is a Windows-friendly, local-first repository for building a CPU-first AI lab with two tracks:

- Teach-a-model: examples, corrections, preferences, and evals for adapting an existing model later.
- Originate-a-model: local datasets and experiments for training a tiny model from scratch later.

The repo exists to keep the data model, folder structure, workflow, and handoff path consistent while local scratch-training, SFT, runtime, and memory work evolve conservatively.

## Scope boundaries

- Keep work local and deterministic.
- Keep the first version simple and readable.
- Keep large artifacts on `D:`.
- Do not introduce cloud-only dependencies.
- Do not expand training or architecture claims faster than the data and eval evidence supports.

## Coding style

- Prefer compact, direct code.
- Prefer plain text configs and simple Python.
- Prefer explicit validation over implicit assumptions.
- Prefer stable names and simple folder conventions.
- Explain assumptions instead of hiding them.

## File ownership expectations

- Treat shared config and schema files as repo-level contracts.
- Update docs when directory layout, schema fields, or runtime conventions change.
- Keep sample files aligned with the schemas.
- Avoid scattered ad hoc files when a shared location already exists.

## Constraints

- CPU-first.
- Windows-friendly.
- Local-first.
- No Docker.
- No GPU assumptions.
- No cloud dependency required for first-run success.
- No heavy package installs unless clearly needed.

## Forbidden actions

- Do not invent or overstate model-training success.
- Do not add large frameworks casually.
- Do not add fake production claims.
- Do not commit anything to git.
- Do not delete user work.
- Do not replace the current structure without a clear reason.

## What done means

A future task is done when:

- the requested files exist and are internally consistent
- the relevant scripts run successfully
- sample data validates against the current schema
- any structural change is reflected in docs
- assumptions are stated clearly

## Safe working rules

- Make minimal, high-confidence changes.
- Validate before claiming completion.
- Prefer updating existing files over creating new variants.
- Avoid adding dependencies casually.
- Keep sample data realistic and generic.
- Preserve schema consistency across docs, configs, and examples.

## Operating notes

- CPU-first
- Windows-friendly
- local-first
- training scaffolds and checkpoint artifacts already exist
- vault-authored architecture and CODA adapter wiring already exist
- current novelty work is Copilot-first donor vaultization, living substrate design, and the later depersonalization-and-refill path

