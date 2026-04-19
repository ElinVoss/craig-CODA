# Repo Contract

## Purpose

`model-lab` is a Windows-friendly, local-first repository for building a CPU-first AI lab with two tracks:

- Teach-a-model: examples, corrections, preferences, and evals for adapting an existing model later.
- Originate-a-model: local datasets and experiments for training a tiny model from scratch later.

The repo exists to keep the data model, folder structure, and workflow consistent before any training code is added.

## Scope boundaries

- Keep work local and deterministic.
- Keep the first version simple and readable.
- Keep large artifacts on `D:`.
- Do not introduce cloud-only dependencies.
- Do not add training code until data formats and eval flows are established.

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

- Do not add model training code in this phase.
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
- no training runs until data formats and eval flows exist

