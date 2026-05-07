# AI Guidance

`craig-CODA` is a local-first Windows repo for a CPU-first AI lab with two tracks:

- Teach-a-model for examples, corrections, preferences, and evals
- Originate-a-model for tiny from-scratch experiments later

Use the existing repo structure as the contract. Keep changes small, deterministic, and readable. Do not add training code until the data formats and eval flows are established.

## Working rules

- Prefer minimal, high-confidence changes.
- Keep everything Windows-friendly and local-first.
- Keep large data and artifacts on `D:`.
- Avoid adding dependencies casually.
- Update docs when structure or schema changes.
- Validate before saying a task is complete.
- State assumptions instead of hiding them.

## Do not

- add Docker
- add cloud dependencies
- add GPU-specific assumptions
- introduce random abstractions
- delete user work
- commit anything to git

