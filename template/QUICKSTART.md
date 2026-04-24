# Craig Template — Quickstart

This is the craig project template. Copy this directory to start a new project.
Fill every `{{PLACEHOLDER}}` before activating the MasterMind.

---

## Step 1 — Fill the Keystone

Open `06_Runtime/craig_mastermind_template.md`.
Replace every `{{PLACEHOLDER}}` with your project's specifics.
Save it as `06_Runtime/mastermind_instructions.md` (the filled version, not the template).

This file is what the AI agent reads as its operating instructions.

## Step 2 — Define Your Foundation

Edit `01_Foundation/FOUNDATION_TEMPLATE.md` → save as `01_Foundation/canon.md`.
Edit `01_Foundation/forbidden_terms.yaml` with your domain's forbidden vocabulary.
Add additional foundation files as needed (lexicon, mechanics, world rules).

These files are born crystallized — any change triggers a downstream re-validation cascade.

## Step 3 — Define Your Entities

Copy `02_Entities/ENTITY_TEMPLATE.md` for each entity.
Save each to `02_Entities/{entity_name}/frames/{frame_name}/dossier.md`.
Fill the frame access rules in `configs/frame_access_policy.yaml`.

## Step 4 — Configure the Constraint Graph

Edit `configs/constraint_graph.yaml`.
Replace example operations with your domain's actual operations.
Define which operations cannot follow which.

## Step 5 — Configure the Validation Protocol

Edit `configs/validation_protocol.yaml`.
Replace example rules with your domain's actual quality gates.
Set `action: block` for hard failures, `action: warn` for soft warnings.

## Step 6 — Configure the Output Template

Edit `configs/output_template.yaml`.
Define the sections every output unit must contain.
Set `unit_count` to match your domain's internal structure.

## Step 7 — Build the Knowledge Index

```bash
python tools/build_knowledge_index.py --root . --out knowledge_index.json
```

This scans all layers, SHA-pins every file, and generates the machine-readable index.
Run this after every commit that changes project files.

## Step 8 — Ingest into Craig's Episodic Memory

```bash
python path/to/craig/scripts/ingest_project.py \
    --project . \
    --db path/to/craig/artifacts/episodic/memory.db
```

This loads all nodes into craig's episodic memory with correct lane scores,
frame tags, and crystallization states.

## Step 9 — Start a Session

```python
from src.runtime.session import Session
from pathlib import Path

session = Session(project_root=Path("."))
session.start(task="Generate output N01", stage="phase_1")
# ... generate output ...
session.close(
    outputs_created=["04_Outputs/bibles/N01_title.md"],
    next_task="Generate output N02"
)
```

## Step 10 — Generate Outputs

Use the `04_Outputs/bibles/OUTPUT_PLACEHOLDER_TEMPLATE.md` as your starting point.
The MasterMind instructions guide the AI through every generation step.
The context chain is injected automatically by `session.py`.

---

## Directory Reference

```
01_Foundation/       ← immutable canon — SHA-pinned, crystallized
02_Entities/         ← multi-frame entity definitions
  {name}/frames/{frame}/
03_State_Tracking/   ← live-tracked progression and state changes
04_Outputs/          ← generated artifacts
  bibles/            ← output units
  engines/           ← system prompts / runtime configurations
05_Continuity/       ← SHA hashes, integrity ledger
  hashes/
06_Runtime/          ← mastermind instructions, session protocol
configs/             ← constraint graph, frame policy, templates, validation
tools/               ← build_knowledge_index.py, linter
```

---

## The Keystone Rule

**Foundation nodes are born crystallized.** They never decay. Any change to them
is a breaking change and must be SHA-re-pinned and re-validated against all outputs.

**Output units build a context chain.** Every output N references all previous outputs.
This is enforced automatically. Never break the chain.

**Frame access is gated.** Locked frames cannot be queried until their stage is reached.
The integrity of hidden-truth architectures depends on this never being violated.
