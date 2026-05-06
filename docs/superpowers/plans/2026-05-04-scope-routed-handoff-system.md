# Scope-Routed Handoff System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Install a repo-native, scope-routed handoff system in `D:\craig-CODA` so any assistant can be brought up to speed from a user-given scope instead of broad repo search.

**Architecture:** Keep the existing repo contract in the root `AGENTS.md`, then layer a root handoff journey (`README.md` plus state files), a canonical `SCOPE_MAP.yaml`, and local `AGENTS.md` plus `README.md` files in meaningful branches. Add a minimal Python validation harness so the scope router and referenced files can be checked deterministically before relying on them.

**Tech Stack:** Markdown, YAML, Python 3.x, PyYAML, pytest-compatible tests, existing PowerShell/Python scripts

---

## File Structure

### Root contract and state

- Modify: `AGENTS.md`
  Add an explicit agent-entry workflow section without removing the existing repo contract.
- Modify: `README.md`
  Insert a root handoff journey at the top and preserve the existing repo overview below it.
- Create: `SCOPE_MAP.yaml`
  Canonical scope router with summaries, aliases, read order, and `work_from`.
- Create: `CURRENT_STATE.md`
  Live operational state.
- Create: `DECISIONS.md`
  Satisfied, unsatisfied, and hard-boundary decisions.
- Create: `NEXT_STEPS.md`
  Immediate queue.
- Create: `ARTIFACTS.md`
  Important generated outputs and their meaning.
- Create: `HANDOFF_PROMPT.md`
  Canonical root continuation prompt.

### Validation harness

- Create: `src/handoff/__init__.py`
  Export helpers for scope loading, alias routing, and validation.
- Create: `src/handoff/scope_map.py`
  Scope router parser and validator.
- Create: `scripts/validate_scope_map.py`
  CLI entrypoint for strict validation and optional query resolution.
- Create: `tests/test_scope_map.py`
  Unit and integration coverage for alias resolution and repo path validation.

### Local branch handoff files

- Create: `exports/user_model_package/method_vault/AGENTS.md`
- Modify: `exports/user_model_package/method_vault/README.md`
- Create: `configs/AGENTS.md`
- Create: `configs/README.md`
- Create: `scripts/AGENTS.md`
- Create: `scripts/README.md`
- Create: `src/AGENTS.md`
- Create: `src/README.md`
- Create: `src/memory/AGENTS.md`
- Create: `src/memory/README.md`
- Create: `runtime/AGENTS.md`
- Create: `runtime/README.md`
- Create: `src/runtime/AGENTS.md`
- Create: `src/runtime/README.md`
- Create: `frontend/AGENTS.md`
- Modify: `frontend/README.md`
- Create: `agent/AGENTS.md`
- Create: `agent/README.md`
- Create: `data/AGENTS.md`
- Create: `data/README.md`
- Create: `artifacts/AGENTS.md`
- Create: `artifacts/README.md`

The top-level `runtime/` branch is included in addition to `src/runtime/` because the repo uses both surfaces today.

## Task 1: Build the Scope Router Validation Harness

**Files:**
- Create: `src/handoff/__init__.py`
- Create: `src/handoff/scope_map.py`
- Create: `scripts/validate_scope_map.py`
- Create: `tests/test_scope_map.py`

- [ ] **Step 1: Write the failing test file**

Create `tests/test_scope_map.py`:

```python
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.handoff.scope_map import load_scope_map, resolve_scope, validate_scope_map


def _write_scope_map(tmp_path: Path, body: str) -> Path:
    tmp_path.mkdir(parents=True, exist_ok=True)
    path = tmp_path / "SCOPE_MAP.yaml"
    path.write_text(body.strip() + "\n", encoding="utf-8")
    return path


def test_resolve_scope_alias_and_fallback(tmp_path: Path):
    config_path = _write_scope_map(
        tmp_path,
        """
        scopes:
          handoff:
            summary: "Default handoff path."
            aliases:
              - "check out what ive got going"
            read_order:
              - README.md
            work_from: README.md
          vault:
            summary: "Vault path."
            aliases:
              - "method vault"
            read_order:
              - README.md
            work_from: README.md
        """,
    )
    data = load_scope_map(config_path)

    assert resolve_scope("vault", data) == "vault"
    assert resolve_scope("method vault", data) == "vault"
    assert resolve_scope("check out what ive got going", data) == "handoff"
    assert resolve_scope("something unknown", data) == "handoff"


def test_validate_scope_map_reports_missing_paths(tmp_path: Path):
    (tmp_path / "README.md").write_text("# test\n", encoding="utf-8")
    config_path = _write_scope_map(
        tmp_path,
        """
        scopes:
          handoff:
            summary: "Default handoff path."
            aliases: []
            read_order:
              - README.md
              - MISSING.md
            work_from: README.md
        """,
    )

    errors = validate_scope_map(config_path, tmp_path, check_paths=True)
    assert any("MISSING.md" in error for error in errors), errors


if __name__ == "__main__":
    test_dir = Path(tempfile.mkdtemp(prefix="scope-map-tests-"))
    test_resolve_scope_alias_and_fallback(test_dir / "alias")
    test_validate_scope_map_reports_missing_paths(test_dir / "missing")
    print("scope-map unit tests passed")
```

- [ ] **Step 2: Run the test to verify it fails**

Run:

```powershell
python -m pytest tests/test_scope_map.py -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'src.handoff'`

- [ ] **Step 3: Write the minimal validation implementation**

Create `src/handoff/__init__.py`:

```python
from .scope_map import load_scope_map, normalize_phrase, resolve_scope, validate_scope_map

__all__ = [
    "load_scope_map",
    "normalize_phrase",
    "resolve_scope",
    "validate_scope_map",
]
```

Create `src/handoff/scope_map.py`:

```python
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

REQUIRED_SCOPE_KEYS = ("summary", "read_order", "work_from")


def normalize_phrase(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def load_scope_map(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict) or not isinstance(data.get("scopes"), dict):
        raise ValueError("SCOPE_MAP.yaml must contain a top-level 'scopes' mapping")
    return data


def resolve_scope(query: str, scope_map: dict[str, Any]) -> str:
    scopes = scope_map["scopes"]
    normalized = normalize_phrase(query)
    for scope_name in scopes:
        if normalized == normalize_phrase(scope_name):
            return scope_name
    for scope_name, scope_cfg in scopes.items():
        aliases = [normalize_phrase(alias) for alias in scope_cfg.get("aliases", [])]
        if normalized in aliases:
            return scope_name
    if "handoff" in scopes:
        return "handoff"
    raise KeyError("No scope matched query and no 'handoff' fallback scope exists")


def validate_scope_map(
    config_path: Path,
    root: Path,
    check_paths: bool = True,
) -> list[str]:
    errors: list[str] = []
    data = load_scope_map(config_path)
    scopes = data["scopes"]

    for scope_name, scope_cfg in scopes.items():
        if not isinstance(scope_cfg, dict):
            errors.append(f"{scope_name}: scope config must be a mapping")
            continue
        for key in REQUIRED_SCOPE_KEYS:
            if key not in scope_cfg:
                errors.append(f"{scope_name}: missing required key '{key}'")
        read_order = scope_cfg.get("read_order", [])
        if not isinstance(read_order, list) or not all(isinstance(item, str) for item in read_order):
            errors.append(f"{scope_name}: read_order must be a list of relative path strings")
            continue
        work_from = scope_cfg.get("work_from")
        if not isinstance(work_from, str):
            errors.append(f"{scope_name}: work_from must be a relative path string")
            continue
        if work_from not in read_order:
            errors.append(f"{scope_name}: work_from must also appear in read_order")
        aliases = scope_cfg.get("aliases", [])
        if aliases and (not isinstance(aliases, list) or not all(isinstance(item, str) for item in aliases)):
            errors.append(f"{scope_name}: aliases must be a list of strings")
        if not check_paths:
            continue
        for rel_path in read_order:
            target = root / rel_path
            if not target.exists():
                errors.append(f"{scope_name}: missing path '{rel_path}'")

    return errors
```

Create `scripts/validate_scope_map.py`:

```python
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.handoff.scope_map import load_scope_map, resolve_scope, validate_scope_map


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate SCOPE_MAP.yaml and optionally resolve a scope query.")
    parser.add_argument("--config", default=str(ROOT / "SCOPE_MAP.yaml"))
    parser.add_argument("--query", default=None)
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = ROOT / config_path

    errors = validate_scope_map(config_path, ROOT, check_paths=True)
    if errors:
        print("Scope map validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    data = load_scope_map(config_path)
    print(f"Validated {len(data['scopes'])} scopes")
    if args.query:
        print(f"Resolved scope: {resolve_scope(args.query, data)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run the tests to verify they pass**

Run:

```powershell
python -m pytest tests/test_scope_map.py -v
python tests/test_scope_map.py
```

Expected:

- `pytest` reports `2 passed`
- direct Python run prints `scope-map unit tests passed`

- [ ] **Step 5: Review the diff instead of committing**

Run:

```powershell
git diff -- src/handoff/__init__.py src/handoff/scope_map.py scripts/validate_scope_map.py tests/test_scope_map.py
```

Expected: only the four new files from this task appear. Do not commit because the repo contract forbids auto-committing in this phase.

## Task 2: Install the Root Handoff Contract and State Files

**Files:**
- Modify: `AGENTS.md`
- Modify: `README.md`
- Create: `SCOPE_MAP.yaml`
- Create: `CURRENT_STATE.md`
- Create: `DECISIONS.md`
- Create: `NEXT_STEPS.md`
- Create: `ARTIFACTS.md`
- Create: `HANDOFF_PROMPT.md`
- Modify: `tests/test_scope_map.py`

- [ ] **Step 1: Add failing root-level integration checks**

Append to `tests/test_scope_map.py`:

```python
def test_root_handoff_files_exist():
    required = [
        ROOT / "SCOPE_MAP.yaml",
        ROOT / "CURRENT_STATE.md",
        ROOT / "DECISIONS.md",
        ROOT / "NEXT_STEPS.md",
        ROOT / "ARTIFACTS.md",
        ROOT / "HANDOFF_PROMPT.md",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    assert missing == [], f"Missing root handoff files: {missing}"


def test_scope_map_has_required_scopes_without_path_checks():
    scope_map_path = ROOT / "SCOPE_MAP.yaml"
    data = load_scope_map(scope_map_path)
    for scope_name in [
        "handoff",
        "vault",
        "tokenizer",
        "weights",
        "memory",
        "runtime",
        "frontend",
        "agent",
        "configs",
        "artifacts",
        "data",
    ]:
        assert scope_name in data["scopes"], f"Missing scope '{scope_name}'"
    assert resolve_scope("check out what ive got going", data) == "handoff"
    assert validate_scope_map(scope_map_path, ROOT, check_paths=False) == []
```

- [ ] **Step 2: Run the new integration checks to verify they fail**

Run:

```powershell
python -m pytest tests/test_scope_map.py -k "root_handoff_files_exist or required_scopes_without_path_checks" -v
```

Expected: FAIL because the root handoff files do not exist yet.

- [ ] **Step 3: Insert the agent-entry workflow into the root `AGENTS.md`**

Insert this block after `# Repo Contract` in `AGENTS.md`:

```markdown
## Agent Entry Workflow

When an assistant enters this directory, it must not begin with broad repo search.

Required read order before meaningful work:

1. Read `README.md` fully.
2. Read `SCOPE_MAP.yaml`.
3. Resolve the user-given scope or natural onboarding phrase.
4. Follow only the mapped `read_order` for that scope.
5. Read local `AGENTS.md` and local `README.md` whenever the route enters a scoped branch.
6. Start work from that branch's `Continue From Here` prompt.

If the user says something like `check out what ive got going`, `bring yourself up to speed`, or `learn this directory`, route to the `handoff` scope first.
If the scope is still ambiguous after alias matching, ask the user to choose among the named scopes instead of wandering the repo.
```

- [ ] **Step 4: Add the root handoff journey to the top of `README.md`**

Insert this block immediately after `# craig-CODA`:

```markdown
## Read Every Word Before Working

If you are a model being pointed at this directory for work, read every word in this README before doing meaningful work.
There is a continuation prompt at the end of the root handoff path.
Do not skim for headings and do not begin with broad repo search.
Use the user-given scope and follow `SCOPE_MAP.yaml`.

## Current Workflow

This directory is currently balancing three things at once:

- a local graph-native runtime and memory system
- a conversation-native corpus and tokenizer pipeline
- a newer method-vault layer meant to drive corpus, tokenization, architecture, and training behavior from parent and child vault notes

The current transition problem is not implementation depth. It is continuity across model changes.
This root handoff layer exists so the next assistant can inherit state cleanly instead of rediscovering it.

## Active Scope Names

- `handoff`
- `vault`
- `tokenizer`
- `weights`
- `memory`
- `runtime`
- `frontend`
- `agent`
- `configs`
- `artifacts`
- `data`

## Root State Files

- `CURRENT_STATE.md`
- `DECISIONS.md`
- `NEXT_STEPS.md`
- `ARTIFACTS.md`
- `HANDOFF_PROMPT.md`

Read them before leaving the root handoff path.
```

- [ ] **Step 5: Create the root state files and scope router**

Create `CURRENT_STATE.md`:

```markdown
# Current State

## What This Repo Is

`craig-CODA` is a Windows-friendly, local-first, CPU-first workspace for graph-native runtime, memory, corpus preparation, tokenizer work, and small-model experimentation.

## What Is Already Working

- raw conversation export data is preserved under `data/raw/conversation_exports/markdown_export_raw/`
- cleaned turn-ordered conversation transcripts exist under `data/clean/conversation_exports/markdown_export_raw/threads/`
- tokenizer preparation and training scripts exist and have been used successfully
- the method vault exists under `exports/user_model_package/method_vault/`
- method notes currently drive corpus, tokenizer, scratch, and SFT configuration resolution

## What Is Still Unresolved

- model architecture is still defined in `configs/model_architecture.yaml` and `src/model_factory.py` instead of fully resolving from the method vault
- the repo did not yet have a clean cross-model handoff path before this work
- the frontend is still a minimal chat surface, not a handoff-first surface

## What Is Active Right Now

- install the scope-routed handoff system
- make model-to-model transitions clean
- keep all routing local and deterministic
```

Create `DECISIONS.md`:

```markdown
# Decisions

## Satisfied Decisions

- Preserve raw conversation exports unchanged.
- Normalize conversations into thread transcripts before retrieval and tokenization.
- Treat conversation data as conversation, not generic JSON chunks.
- Use an Obsidian-like method vault with parent-to-child `_method.md` notes for corpus, tokenizer, and training behavior.
- Use a scope router so assistants follow the user-given branch instead of broad repo search.

## Unsatisfied Decisions

- Full model architecture still needs to resolve from the vault layer.
- The handoff system still needs to be installed into every meaningful work branch.

## Do Not Violate

- Stay local-first.
- Stay Windows-friendly.
- Do not pretend training or architecture work is complete when it is not.
- Do not replace the current repo structure casually.
- Do not start with broad repo wandering when the user has already given a scope.
```

Create `NEXT_STEPS.md`:

```markdown
# Next Steps

## Immediate Queue

1. Install the root handoff files and route map.
2. Install local `AGENTS.md` plus `README.md` files in the highest-value branches.
3. Validate `SCOPE_MAP.yaml` against real file paths.
4. Use the new handoff system to continue the vault-authored architecture work.

## After The Handoff Layer

1. Move model architecture decisions into the method-vault path.
2. Re-run tokenizer and training-parameter flows under the vault-authored method system.
3. Keep branch prompts current as work shifts.
```

Create `ARTIFACTS.md`:

```markdown
# Artifacts

## Core Corpus And Tokenizer Outputs

- `data/clean/conversation_exports/markdown_export_raw/threads/`
- `data/pretrain/conversation_exports/markdown_export_raw/conversation_threads.txt`
- `data/pretrain/conversation_exports/markdown_export_raw/conversation_utterances.txt`
- `data/sft/conversation_exports/markdown_export_raw/reply_pairs.jsonl`
- `artifacts/corpus/prepared_corpus.txt`
- `artifacts/tokenizers/default/training_info.json`
- `artifacts/reports/conversation_threads_token_stats.json`
- `artifacts/reports/conversation_utterances_token_stats.json`

## Method And Vault Outputs

- `exports/user_model_package/method_vault/`
- `src/vault_methods.py`
- `artifacts/methods/`
- `artifacts/vault/`

## Deep Reference Documents

- `graph-native-complete-handoff.md`
- `docs/superpowers/specs/2026-05-04-scope-routed-handoff-system-design.md`
```

Create `HANDOFF_PROMPT.md`:

```markdown
# Continue From Here

You are entering the `handoff` scope of `D:\craig-CODA`.

Treat the following as already established:

- this repo is local-first, CPU-first, and Windows-friendly
- conversation export data has already been normalized into turn-ordered thread transcripts
- the method vault already drives corpus, tokenizer, scratch, and SFT configuration resolution
- model architecture is still the main unresolved gap in the vault-authored system
- you must use the user-given scope instead of broad repo search

Your next job is:

1. read `CURRENT_STATE.md`
2. read `DECISIONS.md`
3. read `NEXT_STEPS.md`
4. read `ARTIFACTS.md`
5. read `SCOPE_MAP.yaml`
6. resolve the user's phrase to a scope
7. follow only that scope's read order

If the user says `check out what ive got going`, `bring yourself up to speed`, or another natural onboarding phrase, remain in the `handoff` scope until the user redirects you to a narrower branch.
```

Create `SCOPE_MAP.yaml`:

```yaml
scopes:
  handoff:
    summary: "Root bring-up-to-speed route for natural onboarding phrases and ambiguous starts."
    aliases:
      - "look at what ive got going"
      - "check out what ive got going"
      - "bring yourself up to speed"
      - "learn this directory"
    read_order:
      - README.md
      - CURRENT_STATE.md
      - DECISIONS.md
      - NEXT_STEPS.md
      - ARTIFACTS.md
      - HANDOFF_PROMPT.md
    work_from: HANDOFF_PROMPT.md
  vault:
    summary: "Method vault rules for corpus, tokenizer, and training behavior."
    aliases:
      - "method vault"
      - "obsidian vault"
      - "vault methods"
    read_order:
      - README.md
      - CURRENT_STATE.md
      - DECISIONS.md
      - exports/user_model_package/method_vault/AGENTS.md
      - exports/user_model_package/method_vault/README.md
      - exports/user_model_package/method_vault/_method.md
      - src/vault_methods.py
    work_from: exports/user_model_package/method_vault/README.md
  tokenizer:
    summary: "Prepared corpus, tokenizer training, inspection, and token statistics."
    aliases:
      - "tokenization"
      - "tokens"
      - "token stats"
    read_order:
      - README.md
      - CURRENT_STATE.md
      - DECISIONS.md
      - configs/AGENTS.md
      - configs/README.md
      - configs/tokenizer.yaml
      - scripts/AGENTS.md
      - scripts/README.md
      - scripts/prepare_corpus.py
      - scripts/train_tokenizer.py
      - scripts/inspect_tokenizer.py
    work_from: configs/README.md
  weights:
    summary: "Architecture, scratch training, SFT behavior, and parameter choices."
    aliases:
      - "parameters"
      - "training behavior"
      - "model shape"
    read_order:
      - README.md
      - CURRENT_STATE.md
      - DECISIONS.md
      - exports/user_model_package/method_vault/AGENTS.md
      - exports/user_model_package/method_vault/README.md
      - configs/AGENTS.md
      - configs/README.md
      - configs/model_architecture.yaml
      - configs/training_scratch.yaml
      - configs/training_sft.yaml
      - src/model_factory.py
      - src/train_scratch.py
      - src/train_sft.py
    work_from: exports/user_model_package/method_vault/README.md
  memory:
    summary: "Node extraction, schema, retrieval, fusion, and graph-native memory behavior."
    aliases:
      - "memory system"
      - "graph memory"
      - "retrieval"
    read_order:
      - README.md
      - CURRENT_STATE.md
      - DECISIONS.md
      - src/memory/AGENTS.md
      - src/memory/README.md
      - configs/node_schema.yaml
      - configs/memory_retrieval.yaml
      - src/memory/extract_nodes.py
      - src/memory/index_semantic.py
      - src/memory/score_fusion.py
    work_from: src/memory/README.md
  runtime:
    summary: "Prompt classification, route selection, and runtime response planning."
    aliases:
      - "route engine"
      - "runtime routing"
      - "prompt enters graph"
    read_order:
      - README.md
      - CURRENT_STATE.md
      - DECISIONS.md
      - runtime/AGENTS.md
      - runtime/README.md
      - runtime/classify_prompt.py
      - runtime/route_prompt.py
      - src/runtime/AGENTS.md
      - src/runtime/README.md
      - src/runtime/front_matter_classifier.py
      - src/runtime/response_plan_builder.py
    work_from: runtime/README.md
  frontend:
    summary: "Local browser surface for Craig-CODA."
    aliases:
      - "ui"
      - "browser"
      - "react frontend"
    read_order:
      - README.md
      - CURRENT_STATE.md
      - DECISIONS.md
      - frontend/AGENTS.md
      - frontend/README.md
      - frontend/src/App.tsx
      - frontend/src/Chat.tsx
    work_from: frontend/README.md
  agent:
    summary: "Local agent server and CLI surface."
    aliases:
      - "chat server"
      - "cli"
      - "agent surface"
    read_order:
      - README.md
      - CURRENT_STATE.md
      - DECISIONS.md
      - agent/AGENTS.md
      - agent/README.md
      - agent/src/server.ts
      - agent/src/cli.ts
    work_from: agent/README.md
  configs:
    summary: "Repo configuration contracts and method-adjacent YAML files."
    aliases:
      - "yaml"
      - "configuration"
      - "config files"
    read_order:
      - README.md
      - CURRENT_STATE.md
      - DECISIONS.md
      - configs/AGENTS.md
      - configs/README.md
      - configs/project.yaml
      - configs/tokenizer.yaml
      - configs/model_architecture.yaml
      - configs/vault_translation.yaml
    work_from: configs/README.md
  artifacts:
    summary: "Generated outputs, reports, tokenizers, checkpoints, and vault artifacts."
    aliases:
      - "outputs"
      - "reports"
      - "generated artifacts"
    read_order:
      - README.md
      - CURRENT_STATE.md
      - ARTIFACTS.md
      - artifacts/AGENTS.md
      - artifacts/README.md
    work_from: artifacts/README.md
  data:
    summary: "Raw, clean, pretrain, SFT, preference, and eval data layers."
    aliases:
      - "datasets"
      - "corpus data"
      - "conversation exports"
    read_order:
      - README.md
      - CURRENT_STATE.md
      - ARTIFACTS.md
      - data/AGENTS.md
      - data/README.md
    work_from: data/README.md
```

- [ ] **Step 6: Run the root-level integration checks to verify they pass**

Run:

```powershell
python -m pytest tests/test_scope_map.py -k "root_handoff_files_exist or required_scopes_without_path_checks" -v
```

Expected: PASS because the root files now exist and the scope map parses cleanly without strict path checks.

- [ ] **Step 7: Review the root diff instead of committing**

Run:

```powershell
git diff -- AGENTS.md README.md SCOPE_MAP.yaml CURRENT_STATE.md DECISIONS.md NEXT_STEPS.md ARTIFACTS.md HANDOFF_PROMPT.md tests/test_scope_map.py
```

Expected: only the root handoff files and root-level test changes appear. Do not commit.

## Task 3: Add the Knowledge-Contract Branches

**Files:**
- Create: `exports/user_model_package/method_vault/AGENTS.md`
- Modify: `exports/user_model_package/method_vault/README.md`
- Create: `configs/AGENTS.md`
- Create: `configs/README.md`

- [ ] **Step 1: Add failing strict-path checks for the knowledge branches**

Append to `tests/test_scope_map.py`:

```python
def test_knowledge_branch_docs_exist():
    required = [
        ROOT / "exports/user_model_package/method_vault/AGENTS.md",
        ROOT / "exports/user_model_package/method_vault/README.md",
        ROOT / "configs/AGENTS.md",
        ROOT / "configs/README.md",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    assert missing == [], f"Missing knowledge-branch docs: {missing}"
```

- [ ] **Step 2: Run the check to verify it fails**

Run:

```powershell
python -m pytest tests/test_scope_map.py -k knowledge_branch_docs_exist -v
```

Expected: FAIL because these local branch docs do not exist yet.

- [ ] **Step 3: Create the method-vault branch docs**

Create `exports/user_model_package/method_vault/AGENTS.md`:

```markdown
# Method Vault Agent Guide

Read order for this branch:

1. `README.md`
2. `_method.md`
3. `corpus/_method.md`
4. `corpus/conversation/_method.md`
5. `tokenizer/_method.md`
6. `tokenizer/default/_method.md`
7. `weights/_method.md`
8. `weights/scratch/_method.md`
9. `weights/sft/_method.md`
10. `src/vault_methods.py`

Do not edit a child `_method.md` note without checking the parent intent first.
Continue from the `Continue From Here` prompt at the end of this branch README.
```

Replace `exports/user_model_package/method_vault/README.md` with:

```markdown
# Method Vault

This branch controls how corpus preparation, tokenizer behavior, and training-related configuration are resolved from parent and child `_method.md` notes.

## Current State

- parent-to-child method resolution exists in `src/vault_methods.py`
- corpus, tokenizer, scratch, and SFT stages already route through the vault layer
- model architecture is still the major missing piece

## Important Files

- `_method.md`
- `corpus/conversation/_method.md`
- `tokenizer/default/_method.md`
- `weights/scratch/_method.md`
- `weights/sft/_method.md`
- `src/vault_methods.py`

## Do Not Violate

- do not flatten parent and child intent into one note
- do not treat raw exports as generic document chunks
- do not claim architecture is already fully vault-authored

## Continue From Here

You are in the `vault` scope.
Treat the current stage resolution behavior as already established for corpus, tokenizer, scratch, and SFT.
The unresolved question is how to move model architecture into the same vault-authored path without breaking the current pipeline.
Start from `_method.md`, then `weights/_method.md`, then `src/vault_methods.py`.
```

- [ ] **Step 4: Create the configs branch docs**

Create `configs/AGENTS.md`:

```markdown
# Configs Agent Guide

Read order for this branch:

1. `README.md`
2. `project.yaml`
3. `tokenizer.yaml`
4. `model_architecture.yaml`
5. `training_scratch.yaml`
6. `training_sft.yaml`
7. `vault_translation.yaml`

Do not change a config contract casually.
Use the branch README to decide which config is authoritative for the active scope.
```

Create `configs/README.md`:

```markdown
# Configs

This branch holds the repo's YAML contracts for runtime behavior, data handling, tokenizer setup, training setup, and vault translation.

## Current State

- tokenizer and training configs exist and are active
- vault translation is already pointed at cleaned conversation transcripts
- `model_architecture.yaml` still defines architecture outside the method-vault path

## Important Files

- `project.yaml`
- `tokenizer.yaml`
- `model_architecture.yaml`
- `training_scratch.yaml`
- `training_sft.yaml`
- `vault_translation.yaml`

## Do Not Violate

- keep config names stable
- do not invent a second source of truth for architecture or tokenizer settings
- treat these files as contracts, not scratch notes

## Continue From Here

You are in the `configs` scope.
Your job is to understand which YAML files are authoritative for the user's requested branch.
If the task is about vault-authored methods, compare `model_architecture.yaml` against the method-vault branch and treat that gap as unresolved work, not solved work.
```

- [ ] **Step 5: Run the knowledge-branch checks to verify they pass**

Run:

```powershell
python -m pytest tests/test_scope_map.py -k knowledge_branch_docs_exist -v
```

Expected: PASS

- [ ] **Step 6: Review the knowledge-branch diff instead of committing**

Run:

```powershell
git diff -- exports/user_model_package/method_vault/AGENTS.md exports/user_model_package/method_vault/README.md configs/AGENTS.md configs/README.md tests/test_scope_map.py
```

Expected: only the knowledge-branch docs and their test change appear. Do not commit.

## Task 4: Add the Operational Code Branches

**Files:**
- Create: `scripts/AGENTS.md`
- Create: `scripts/README.md`
- Create: `src/AGENTS.md`
- Create: `src/README.md`
- Create: `src/memory/AGENTS.md`
- Create: `src/memory/README.md`
- Create: `runtime/AGENTS.md`
- Create: `runtime/README.md`
- Create: `src/runtime/AGENTS.md`
- Create: `src/runtime/README.md`

- [ ] **Step 1: Add failing checks for the operational branch docs**

Append to `tests/test_scope_map.py`:

```python
def test_operational_branch_docs_exist():
    required = [
        ROOT / "scripts/AGENTS.md",
        ROOT / "scripts/README.md",
        ROOT / "src/AGENTS.md",
        ROOT / "src/README.md",
        ROOT / "src/memory/AGENTS.md",
        ROOT / "src/memory/README.md",
        ROOT / "runtime/AGENTS.md",
        ROOT / "runtime/README.md",
        ROOT / "src/runtime/AGENTS.md",
        ROOT / "src/runtime/README.md",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    assert missing == [], f"Missing operational branch docs: {missing}"
```

- [ ] **Step 2: Run the check to verify it fails**

Run:

```powershell
python -m pytest tests/test_scope_map.py -k operational_branch_docs_exist -v
```

Expected: FAIL because these branch docs do not exist yet.

- [ ] **Step 3: Create the scripts and src root docs**

Create `scripts/AGENTS.md`:

```markdown
# Scripts Agent Guide

Read order for this branch:

1. `README.md`
2. `normalize_markdown_export_raw.py`
3. `prepare_corpus.py`
4. `train_tokenizer.py`
5. `validate_scope_map.py`

Do not touch unrelated scripts just because they are nearby.
Start from the branch README prompt.
```

Create `scripts/README.md`:

```markdown
# Scripts

This branch contains the direct execution surface for ingestion, normalization, corpus preparation, tokenizer work, training runners, and validation helpers.

## Current State

- conversation normalization is already implemented here
- tokenizer preparation and training live here
- the new handoff-system validator also lives here

## Important Files

- `normalize_markdown_export_raw.py`
- `prepare_corpus.py`
- `train_tokenizer.py`
- `inspect_tokenizer.py`
- `run_tokenizer_pipeline.py`
- `validate_scope_map.py`

## Continue From Here

You are in the `scripts` branch.
Use this branch when the user's scope is procedural and script-driven.
If the task is about installing or validating handoff behavior, start with `validate_scope_map.py` and then trace the branch scripts that the user's scope actually needs.
```

Create `src/AGENTS.md`:

```markdown
# Src Agent Guide

Read order for this branch:

1. `README.md`
2. `vault_methods.py`
3. `model_factory.py`
4. `train_scratch.py`
5. `train_sft.py`

Move to `src/memory/` or `src/runtime/` when the scope narrows.
```

Create `src/README.md`:

```markdown
# Src

This branch contains the core Python implementation for vault methods, tokenizer loading, scratch training, SFT validation, and the runtime and memory subpackages.

## Current State

- vault method resolution exists here
- model construction and training entrypoints exist here
- memory and runtime are split into deeper branches

## Continue From Here

You are in the broad `src` branch.
If the user's scope is memory, descend into `src/memory/`.
If the user's scope is runtime behavior, descend into `src/runtime/`.
If the user's scope is architecture or training behavior, stay with `vault_methods.py`, `model_factory.py`, `train_scratch.py`, and `train_sft.py`.
```

- [ ] **Step 4: Create the memory and runtime branch docs**

Create `src/memory/AGENTS.md`:

```markdown
# Memory Agent Guide

Read order for this branch:

1. `README.md`
2. `extract_nodes.py`
3. `index_semantic.py`
4. `score_fusion.py`
5. `normalize_sources.py`
6. `node_schema.py`

Stay inside the memory branch unless the user explicitly redirects you.
```

Create `src/memory/README.md`:

```markdown
# Memory

This branch owns node extraction, normalization, semantic indexing, temporal indexing, edge building, and retrieval scoring.

## Current State

- conversation transcript extraction is already treated specially
- lexical fallback still matters in retrieval
- graph-native memory behavior is active here, but not every future architecture idea belongs here

## Continue From Here

You are in the `memory` scope.
Start with `extract_nodes.py`, `index_semantic.py`, and `score_fusion.py`.
If the user asks about schema, move to `configs/node_schema.yaml` and `node_schema.py`.
```

Create `runtime/AGENTS.md`:

```markdown
# Runtime Route Agent Guide

Read order for this branch:

1. `README.md`
2. `classify_prompt.py`
3. `route_prompt.py`

This top-level runtime branch is for the pure route and classify surface, not the broader `src/runtime/` package.
```

Create `runtime/README.md`:

```markdown
# Runtime Route Layer

This branch contains the top-level route engine and prompt classification logic used for graph-native runtime routing.

## Current State

- `route_prompt.py` is the pure L1 route engine
- `classify_prompt.py` provides prompt-axis classification used by the route layer
- this branch is separate from `src/runtime/`, which contains the larger runtime package

## Continue From Here

You are in the `runtime` scope.
Read `classify_prompt.py` and `route_prompt.py` first, then continue into `src/runtime/` only if the task broadens into runtime assembly or response planning.
```

Create `src/runtime/AGENTS.md`:

```markdown
# Src Runtime Agent Guide

Read order for this branch:

1. `README.md`
2. `front_matter_classifier.py`
3. `response_plan_builder.py`
4. `prompt_compiler.py`
5. `mode_router.py`

Use this branch for the larger runtime package after understanding the top-level route layer.
```

Create `src/runtime/README.md`:

```markdown
# Src Runtime

This branch contains the richer runtime package for front matter handling, mode routing, prompt compilation, backend selection, and session behavior.

## Current State

- front matter classification is already implemented
- response planning is already implemented
- this package is downstream of the top-level route layer, not a replacement for it

## Continue From Here

You are in the deeper runtime package.
Start with `front_matter_classifier.py` and `response_plan_builder.py`.
Keep the distinction between `runtime/` and `src/runtime/` explicit while working here.
```

- [ ] **Step 5: Run the operational-branch checks to verify they pass**

Run:

```powershell
python -m pytest tests/test_scope_map.py -k operational_branch_docs_exist -v
```

Expected: PASS

- [ ] **Step 6: Review the operational-branch diff instead of committing**

Run:

```powershell
git diff -- scripts/AGENTS.md scripts/README.md src/AGENTS.md src/README.md src/memory/AGENTS.md src/memory/README.md runtime/AGENTS.md runtime/README.md src/runtime/AGENTS.md src/runtime/README.md tests/test_scope_map.py
```

Expected: only the operational branch docs and the related test change appear. Do not commit.

## Task 5: Add the Interaction and Data Branches

**Files:**
- Create: `frontend/AGENTS.md`
- Modify: `frontend/README.md`
- Create: `agent/AGENTS.md`
- Create: `agent/README.md`
- Create: `data/AGENTS.md`
- Create: `data/README.md`
- Create: `artifacts/AGENTS.md`
- Create: `artifacts/README.md`

- [ ] **Step 1: Add failing checks for the interaction and data branches**

Append to `tests/test_scope_map.py`:

```python
def test_interaction_and_data_branch_docs_exist():
    required = [
        ROOT / "frontend/AGENTS.md",
        ROOT / "frontend/README.md",
        ROOT / "agent/AGENTS.md",
        ROOT / "agent/README.md",
        ROOT / "data/AGENTS.md",
        ROOT / "data/README.md",
        ROOT / "artifacts/AGENTS.md",
        ROOT / "artifacts/README.md",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    assert missing == [], f"Missing interaction/data branch docs: {missing}"
```

- [ ] **Step 2: Run the check to verify it fails**

Run:

```powershell
python -m pytest tests/test_scope_map.py -k interaction_and_data_branch_docs_exist -v
```

Expected: FAIL because the new branch docs do not exist yet.

- [ ] **Step 3: Create the frontend and agent branch docs**

Create `frontend/AGENTS.md`:

```markdown
# Frontend Agent Guide

Read order for this branch:

1. `README.md`
2. `src/App.tsx`
3. `src/Chat.tsx`

Do not mistake the frontend for the repo's primary handoff layer.
It is only the browser surface.
```

Replace `frontend/README.md` with:

```markdown
# Frontend

This branch contains the local React/Vite browser surface for Craig-CODA.

## Current State

- the current frontend is still a minimal chat-oriented surface
- it is not the primary continuity layer for model handoffs
- the repo-native handoff system lives in root and branch docs, not in this UI

## Important Files

- `src/App.tsx`
- `src/Chat.tsx`
- `src/ChatWidget.tsx`

## Continue From Here

You are in the `frontend` scope.
Treat the UI as a secondary surface.
If the user wants repo continuity or bring-up-to-speed behavior, return to the root handoff system instead of trying to solve that with React alone.
```

Create `agent/AGENTS.md`:

```markdown
# Agent Surface Guide

Read order for this branch:

1. `README.md`
2. `src/server.ts`
3. `src/cli.ts`

Use this branch for the local server and CLI surface, not for root handoff routing.
```

Create `agent/README.md`:

```markdown
# Agent

This branch contains the local server and CLI surface that lets Craig-CODA run as an interactive agent.

## Current State

- `src/server.ts` exposes the HTTP chat surface
- `src/cli.ts` exposes the terminal chat loop
- this branch depends on the runtime and memory layers rather than replacing them

## Continue From Here

You are in the `agent` scope.
Start with `src/server.ts` and `src/cli.ts`.
If the user asks how the agent becomes informed by repo state, route back through the root handoff system and the relevant scope rather than guessing from this package alone.
```

- [ ] **Step 4: Create the data and artifacts branch docs**

Create `data/AGENTS.md`:

```markdown
# Data Agent Guide

Read order for this branch:

1. `README.md`
2. `raw/`
3. `clean/`
4. `pretrain/`
5. `sft/`

Use this branch when the scope is about corpus shape, not runtime code.
```

Create `data/README.md`:

```markdown
# Data

This branch contains the raw, clean, pretrain, SFT, preference, and eval data layers for Craig-CODA.

## Current State

- raw conversation exports are preserved
- clean conversation thread transcripts are active inputs for retrieval and tokenization
- SFT reply pairs are generated from the normalized conversation layer

## Continue From Here

You are in the `data` scope.
Start with the raw conversation export path and the clean thread transcript path.
Treat data lineage as important; do not collapse raw and clean layers together.
```

Create `artifacts/AGENTS.md`:

```markdown
# Artifacts Agent Guide

Read order for this branch:

1. `README.md`
2. `../ARTIFACTS.md`
3. `tokenizers/`
4. `reports/`
5. `vault/`

Use this branch for generated outputs and reports, not for source-of-truth editing.
```

Create `artifacts/README.md`:

```markdown
# Artifacts

This branch contains generated corpus outputs, tokenizer artifacts, reports, vault artifacts, checkpoints, and sample outputs.

## Current State

- tokenizer artifacts are already present
- corpus and token reports already exist
- method and vault artifacts are meaningful outputs, not the canonical source definitions

## Continue From Here

You are in the `artifacts` scope.
Use this branch to inspect what the pipeline produced.
If the user wants to change behavior, route back to the branch that authored the behavior instead of editing artifacts directly.
```

- [ ] **Step 5: Run the interaction/data checks to verify they pass**

Run:

```powershell
python -m pytest tests/test_scope_map.py -k interaction_and_data_branch_docs_exist -v
```

Expected: PASS

- [ ] **Step 6: Review the interaction/data diff instead of committing**

Run:

```powershell
git diff -- frontend/AGENTS.md frontend/README.md agent/AGENTS.md agent/README.md data/AGENTS.md data/README.md artifacts/AGENTS.md artifacts/README.md tests/test_scope_map.py
```

Expected: only the interaction/data branch docs and the related test change appear. Do not commit.

## Task 6: Turn On Strict Repo Validation and Finalize the Root Handoff Surface

**Files:**
- Modify: `tests/test_scope_map.py`
- Modify: `README.md`
- Modify: `ARTIFACTS.md` (if needed for missing references)
- Validate: `SCOPE_MAP.yaml`

- [ ] **Step 1: Add the strict repo validation test**

Append to `tests/test_scope_map.py`, then replace its `__main__` block with:

```python
def test_repo_scope_map_is_strictly_valid():
    scope_map_path = ROOT / "SCOPE_MAP.yaml"
    errors = validate_scope_map(scope_map_path, ROOT, check_paths=True)
    assert errors == [], f"Strict scope-map validation failed: {errors}"


if __name__ == "__main__":
    test_dir = Path(tempfile.mkdtemp(prefix="scope-map-tests-"))
    test_resolve_scope_alias_and_fallback(test_dir / "alias")
    test_validate_scope_map_reports_missing_paths(test_dir / "missing")
    test_root_handoff_files_exist()
    test_scope_map_has_required_scopes_without_path_checks()
    test_knowledge_branch_docs_exist()
    test_operational_branch_docs_exist()
    test_interaction_and_data_branch_docs_exist()
    test_repo_scope_map_is_strictly_valid()
    print("scope-map tests passed")
```

- [ ] **Step 2: Run the strict validation test to identify any missing paths**

Run:

```powershell
python -m pytest tests/test_scope_map.py -k repo_scope_map_is_strictly_valid -v
```

Expected: PASS. If it fails, create or fix the missing referenced branch files before proceeding.

- [ ] **Step 3: Run the CLI validator and direct Python test file**

Run:

```powershell
python scripts/validate_scope_map.py
python scripts/validate_scope_map.py --query "check out what ive got going"
python tests/test_scope_map.py
```

Expected:

- validator prints `Validated 11 scopes`
- alias query prints `Resolved scope: handoff`
- direct Python test run prints `scope-map tests passed`

- [ ] **Step 4: Add the final continuation block to the root `README.md`**

Append this block near the end of the new root handoff section in `README.md`:

```markdown
## Continue From Here

If you are continuing work in this directory:

1. finish the root handoff path
2. read `SCOPE_MAP.yaml`
3. resolve the user's scope
4. follow only that branch

Do not start with broad repo search.
Do not re-derive the current repo state from scratch.
Take the continuation prompt from the branch you are routed into and work from there.
```

- [ ] **Step 5: Run one final combined validation pass**

Run:

```powershell
python -m pytest tests/test_scope_map.py -v
python scripts/validate_scope_map.py
```

Expected:

- all handoff-system tests pass
- strict scope-map validation passes

- [ ] **Step 6: Review the final diff instead of committing**

Run:

```powershell
git diff --stat
```

Expected: the diff shows only the handoff-system docs, validator, and tests from this plan. Do not commit because the repo contract forbids it.
