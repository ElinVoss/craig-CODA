# Scope-Routed Handoff System Design

## Purpose

Build a repo-native handoff system for `D:\craig-CODA` so any model opened in this directory can be brought up to speed quickly and consistently without broad repo searching.

The system is designed for the user's real workflow:

- the user opens the directory in a terminal
- the user starts an assistant (`Codex`, `Claude`, `Copilot`, or another model)
- the user points the assistant at a scope such as `vault`, `tokenizer`, `weights`, `runtime`, or `frontend`
- the assistant should be guided through an exact reading path instead of discovering context by roaming the tree
- if the user hits model limits and changes assistants, the next model should inherit a clean transition path

This system is not a generic documentation refresh. It is a structured machine-and-human handoff layer.

## Goals

- Force a consistent first-read path for agents entering the repo.
- Make the user-given scope the primary router instead of repo search.
- Preserve a narrative journey for the model, not just a pile of notes.
- Carry active decisions, satisfied decisions, unsatisfied decisions, and next steps forward across model changes.
- Allow each important subtree to narrow the work with local instructions and local prompts.
- Keep the first version local, simple, readable, and easy to maintain.

## Non-Goals

- Do not build a UI-first solution.
- Do not require a browser or external service to use the handoff system.
- Do not try to auto-solve all documentation updates in the first version.
- Do not replace the existing repo architecture or project files.
- Do not require full repo indexing before an agent can begin.

## Recommended Structure

The handoff system has four layers.

### 1. Root Enforcement Layer

Files:

- `AGENTS.md`
- `README.md`
- `SCOPE_MAP.yaml`

Responsibilities:

- `AGENTS.md` is the hard instruction layer.
- `README.md` is the bring-up-to-speed journey.
- `SCOPE_MAP.yaml` is the canonical router from a user-given scope to an ordered reading chain.

### 2. Root State Layer

Files:

- `CURRENT_STATE.md`
- `DECISIONS.md`
- `NEXT_STEPS.md`
- `ARTIFACTS.md`
- optional `HANDOFF_PROMPT.md`

Responsibilities:

- `CURRENT_STATE.md` states what the repo currently is, what is active now, what is complete, and what is blocked.
- `DECISIONS.md` records satisfied decisions, unsatisfied decisions, hard rules, and open questions.
- `NEXT_STEPS.md` records the immediate working queue.
- `ARTIFACTS.md` points to important generated outputs, datasets, reports, and runtime artifacts.
- `HANDOFF_PROMPT.md` can hold the current end-of-journey continuation prompt if separating that from `README.md` proves easier to maintain.

### 3. Scope-Specific Journey Layer

Each important branch gets both:

- local `AGENTS.md`
- local `README.md`

These live only in meaningful work roots, not everywhere indiscriminately.

Initial target branches:

- `exports/user_model_package/method_vault/`
- `data/`
- `artifacts/`
- `scripts/`
- `src/`
- `src/memory/`
- `src/runtime/`
- `frontend/`
- `agent/`
- `configs/`

Each local pair narrows the journey:

- local `AGENTS.md` tells the agent what to read next in that subtree and what not to do
- local `README.md` explains that subtree's purpose, current state, local decisions, and ends with a subtree-specific working prompt

### 4. Prompt Trail Layer

Every important journey endpoint ends with a concrete working prompt.

That prompt is not decorative. It is the continuation handoff for the current branch. It should tell the next model:

- what this branch is for
- what is already done
- what is still unresolved
- what files matter most next
- what assumptions not to violate
- what the next concrete task is

## Entry Contract

The root contract should be explicit and hard to ignore.

### Root `AGENTS.md`

The root `AGENTS.md` should enforce this behavior:

1. Read root `README.md` fully before doing meaningful work.
2. Use the user-given scope. Do not broadly inspect the repo first.
3. Read `SCOPE_MAP.yaml`.
4. Follow only the ordered reading chain for the requested scope unless a listed file is missing or blocked.
5. Read local `AGENTS.md` and local `README.md` when entering the mapped branch.
6. Start work from the end-of-journey prompt for that branch.
7. If the current scope is ambiguous, ask the user to choose among the existing scopes instead of broad searching.
8. If a file in the chain is missing, report the gap and continue with the next mapped item where safe.
9. If the user gives a natural onboarding phrase instead of a clean scope name, route to the default `handoff` scope first.

### Root `README.md`

The root `README.md` should begin with the user's stated rule:

- the model must read every word
- there is a prompt at the end
- if the model is being pointed here for work, it must take the ending prompt seriously as the handoff prompt for learning and continuing this directory

After that opening warning, the root `README.md` should contain:

1. What this directory currently is.
2. What workflow is active now.
3. What decisions have been satisfied.
4. What decisions remain unsatisfied.
5. What scope names exist.
6. What the current high-priority branches are.
7. What changed recently.
8. Where to find state and artifact files.
9. The ending continuation prompt.

The root `README.md` is narrative and instructional, not just a table of links.

## Scope Routing

`SCOPE_MAP.yaml` is the canonical routing layer.

It should be easy for a model to parse and easy for a human to maintain.

Recommended schema:

```yaml
scopes:
  vault:
    summary: "Vault-authored method system for corpus, tokenizer, architecture, and training behavior."
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
    summary: "Prepared corpus, tokenizer training, tokenizer inspection, and token statistics."
    read_order:
      - README.md
      - CURRENT_STATE.md
      - DECISIONS.md
      - configs/AGENTS.md
      - configs/README.md
      - configs/tokenizer.yaml
      - scripts/prepare_corpus.py
      - scripts/train_tokenizer.py
      - scripts/inspect_tokenizer.py
    work_from: configs/README.md
```

Required properties:

- `summary`
- `read_order`
- `work_from`

Optional properties:

- `aliases`
- `depends_on`
- `blocked_by`
- `artifacts`
- `notes`

The first implementation should include these root scopes:

- `handoff`
- `vault`
- `tokenizer`
- `weights`
- `runtime`
- `memory`
- `frontend`
- `agent`
- `configs`
- `artifacts`

The router should also support natural-language aliases.

Examples:

- `handoff`
  aliases:
  - `look at what ive got going`
  - `check out what ive got going`
  - `bring yourself up to speed`
  - `learn this directory`
- `vault`
  aliases:
  - `method vault`
  - `obsidian vault`
  - `vault methods`
- `weights`
  aliases:
  - `parameters`
  - `training behavior`
  - `model shape`

If the user does not give a clean scope, the system should first try alias resolution.
If no alias matches with confidence, it should fall back to the `handoff` scope rather than broad search.

## Local Branch Contract

Each important scoped folder gets a local pair.

### Local `AGENTS.md`

Local instruction files should be short and sharp:

- define what this subtree is for
- define the local read order
- define branch-specific boundaries
- define what files are considered authoritative here
- tell the agent what prompt to continue from after reading

### Local `README.md`

Local README files should carry the branch journey:

- what this subtree does
- current branch state
- branch-level decisions
- branch-level open questions
- important files
- related artifacts
- end-of-branch continuation prompt

This keeps the "well deserved journey" feeling the user wants while still making the path deterministic.

## Writing Style Rules

These files need to work for both humans and models.

Rules:

- Prefer direct prose over bloated framework language.
- Keep the first paragraph of each README oriented around "what this branch is doing now."
- Use explicit labels such as `Satisfied Decisions`, `Unsatisfied Decisions`, `Active Scope`, `Do Not Violate`, and `Continue From Here`.
- End each README with one clear continuation prompt block.
- Avoid vague statements like "see code for details."
- Avoid over-linking to unrelated branches.

## State Maintenance Model

The first version should be hybrid, not fully automated.

### Human-maintained first

These files are primarily human-maintained:

- `README.md`
- `CURRENT_STATE.md`
- `DECISIONS.md`
- `NEXT_STEPS.md`
- local `README.md`

Reason:

- these contain intent, judgment, and branch-specific working prompts
- fully generating them in the first version would weaken the quality of handoffs

### Generated or semi-generated later

These may later gain script support:

- `ARTIFACTS.md`
- recent artifact inventories
- changed-file summaries
- route validation against missing paths in `SCOPE_MAP.yaml`

But automation should sit under the human layer, not replace it.

## Initial File Tree

Recommended first-pass additions:

```text
AGENTS.md
README.md
SCOPE_MAP.yaml
CURRENT_STATE.md
DECISIONS.md
NEXT_STEPS.md
ARTIFACTS.md
HANDOFF_PROMPT.md

exports/user_model_package/method_vault/AGENTS.md
exports/user_model_package/method_vault/README.md

configs/AGENTS.md
configs/README.md

scripts/AGENTS.md
scripts/README.md

src/AGENTS.md
src/README.md
src/memory/AGENTS.md
src/memory/README.md
src/runtime/AGENTS.md
src/runtime/README.md

frontend/AGENTS.md
frontend/README.md

agent/AGENTS.md
agent/README.md

artifacts/AGENTS.md
artifacts/README.md

data/AGENTS.md
data/README.md
```

Not every folder in the repo gets this treatment. Only branches that are meaningful entry points for real work.

## Handoff Prompt Pattern

Every major README should end with a continuation prompt block that follows a stable pattern.

Recommended shape:

```text
Continue From Here

You are working in the <scope> scope of D:\craig-CODA.
You have already read the required handoff files for this branch.
Treat the following as already established:
- ...
- ...

Do not broaden scope unless the user explicitly redirects you.
Do not re-discover the repo from scratch.
Your next job is:
- ...

Start by reading:
- ...
- ...
```

This is the thing the next model should "take" when the user says they are continuing work in that branch.

## Failure Modes To Guard Against

The system must explicitly protect against these behaviors:

### Broad wandering

The model ignores scope and starts searching the repo.

Countermeasure:

- hard rule in root `AGENTS.md`
- explicit `SCOPE_MAP.yaml`
- local AGENTS files that keep narrowing the path

### Shallow skimming

The model reads only headers and misses the branch prompt.

Countermeasure:

- opening warning in root `README.md`
- branch README ending prompt blocks
- concise but direct writing

### Stale continuity

The notes are old enough that model-to-model transitions drift.

Countermeasure:

- `CURRENT_STATE.md` and `NEXT_STEPS.md` must be updated whenever the active direction changes
- README files summarize, but state files carry the freshest operational truth

### Prompt sprawl

Too many prompts dilute the path instead of clarifying it.

Countermeasure:

- only meaningful branches get local prompt layers
- each scope has one canonical read chain
- each branch ends with one continuation prompt, not many competing prompts

## Verification Criteria

This design is successful when:

1. A model given a scope can begin without broad repo search.
2. The root files make the current workflow understandable in one reading pass.
3. Local branch files narrow the work instead of duplicating the root.
4. A model switch midstream can resume from the same scope without large context loss.
5. The continuation prompts are strong enough that the next model starts from the established state rather than re-deriving it.

## Implementation Notes

The first implementation should create the structure and populate it with the current repo state, especially around:

- the conversation-native corpus import
- the method vault for corpus, tokenizer, scratch, and SFT behavior
- the remaining gap where model architecture still bypasses the vault layer
- the current distinction between completed work and still-unfinished vault-authored architecture work

The first implementation should not try to automate everything.

## Constraints

- Stay local-first.
- Stay repo-native.
- No cloud dependency.
- No commit is required here because the repo contract forbids auto-committing in this phase.
- Prefer readable markdown and YAML over clever machinery.

## Recommended Next Phase

After this spec is approved, the implementation plan should do three things:

1. Create the root handoff files and populate them from the current state of `craig-CODA`.
2. Create the first scoped branch layers for the most important work roots.
3. Add validation so `SCOPE_MAP.yaml` cannot silently point at missing paths.
