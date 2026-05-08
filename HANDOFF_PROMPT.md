# Startup Prompt Of Record

## Command-Line Bootstrap Prompt

Copy and paste the block below into any command-line model that is about to enter `D:\craig-CODA`.

```text
You are entering D:\craig-CODA in command-line mode.

Do not begin with broad repo search.
Do not improvise your own onboarding path.
Do not treat this as a blank repo.

First command-line action:
read D:\craig-CODA\HANDOFF_PROMPT.md in full, then follow its required read order exactly.

You are inheriting an active local-first project with runtime, vault, memory, donor, substrate, and handoff work already in motion.

Before meaningful work, you must explicitly understand and preserve these truths:

- scratch-training and SFT scaffolds already exist in this repo
- those training layers are still experimental and must not be overstated
- vault-authored architecture and CODA adapter wiring already exist
- the unresolved frontier is donor vaultization, living substrate design, runtime integration, and the later depersonalization/refill path
- LIVE_HANDOFF.md is the shared baton and must be updated between meaningful actions

Current architectural center of gravity:

- the strongest current control shape is a small native BIOS / interpreter, not one magical donor mind
- that BIOS should classify prompts, pull vault and repo context, fan requests across donors when needed, score candidates under hard Craig rules, select, log, and promote what survives
- D:\FloorAgent\src\domain\planning.js is the best live analogy for the selector pattern: explicit priority tuple, candidate comparison, best-pick loop
- donors are still temporary response organs and extraction sources during this phase; arbitration is the native core

Current retrieval truth:

- retrieval now supports a first conservative spreading-activation pass in `src/memory/spreading_activation.py`, selected through `src/memory/retrieve_topk.py`
- graph routing is still converted back into injected text in agent/src/server.ts and src/runtime/coda.py
- the active retrieval shape is now:
  1. seed activation
  2. propagate across edges with decay and fan-out caps
  3. select the active subgraph
  4. then translate
- this is not a cosmetic rename; it changes the computational question from “which nodes score highest” to “which neighborhood becomes coherent”
- a conservative edge audit pass now exists at scripts/audit_edges.py
- in a field model, missing edges make the system conservative; bad edges make it confidently wrong
- the next improvement path here is edge-quality tuning and deeper propagation behavior, not reintroducing the old flat-only runtime path

Current self-model boundaries:

- do not sanitize the user into purity
- do not flatten the user into villainy
- model capacity versus identity separately
- future Craig modeling needs provenance tracking, contradiction tolerance, state overlays, and disclosure-boundary awareness
- continuous spoken-thought capture is promising raw self-material, but it should be mined for recurring motifs and thresholds rather than ingested directly as core truth

Mandatory read order before meaningful work:

1. README.md
2. CURRENT_STATE.md
3. DECISIONS.md
4. NEXT_STEPS.md
5. ARTIFACTS.md
6. LIVE_HANDOFF.md
7. SCOPE_MAP.yaml
8. resolve the user phrase to a scope
9. follow only that scope's read_order
10. read the local AGENTS.md and local README.md for the routed branch
11. continue from that branch's Continue From Here section

Your first substantive response in this repo must explicitly state:

1. scratch-training and SFT scaffolds already exist
2. they are still experimental and should not be overstated
3. vault-authored architecture and CODA adapter wiring already exist, but donor vaultization, living substrate design, and depersonalization/refill remain unresolved
4. you will use the user-given scope instead of broad repo search
5. you will keep LIVE_HANDOFF.md updated between meaningful actions

If anything in the docs contradicts that, stop and report the contradiction instead of pretending orientation is complete.
```

Read every word in this file before doing meaningful work in `D:\craig-CODA`.

This is the canonical startup prompt for any model entering this directory. If you are any assistant or model being pointed here for work, you must treat this as the operating contract for how to learn, navigate, and continue the repo.

## Your Role Here

You are not entering a blank repo.

You are entering an active local-first project with ongoing runtime, memory, vault, tokenizer, and model-shaping work already in motion. Your job is not to rediscover the directory from scratch. Your job is to inherit the current state, respect the existing scope router, continue from the live baton, and leave the next model a cleaner transition than the one you received.

## Hard Rules

1. Do not begin with broad repo search.
2. Do not skim this file.
3. Do not infer your own route through the tree when a scope has already been given.
4. Do not silently drop continuity.
5. Do not leave stale baton state behind you.
6. Do not present unresolved work as complete.
7. Do not replace the current structure casually.

## What Is Already True

Treat the following as already established unless the live baton or explicit repo files contradict it:

- `craig-CODA` is local-first, CPU-first, and Windows-friendly.
- raw conversation exports are preserved under `data/raw/conversation_exports/markdown_export_raw/`
- normalized turn-ordered conversation transcripts exist under `data/clean/conversation_exports/markdown_export_raw/threads/`
- the method vault exists under `exports/user_model_package/method_vault/`
- parent-to-child `_method.md` notes already drive corpus, tokenizer, scratch, SFT, and architecture configuration resolution
- local scratch-training and SFT scaffolds already exist, even though the repo should still treat architecture and training claims conservatively
- vault-authored architecture and CODA adapter wiring already exist
- the handoff system now exists to make model-to-model transitions cleaner
- `LIVE_HANDOFF.md` is the shared baton file for all models

## Long-Range Objective

The repo is not only trying to train or host one model.

The longer-range target is a vault-populated CODA system where:

- the vault is the governing source reality
- a vault compiler or populator turns that reality into a shared intermediate representation
- multiple source models can be compiled through the same vault authority
- CODA is the orchestration identity that calls, routes, merges, remembers, and responds
- the stable invariant is the vault compiler, intermediate representation, adapter contract, memory structure, and heartbeat behavior, not any one borrowed model backend

The intended later test path is:

1. compile strong source models through the same vault-populated chassis
2. preserve the organized working heartbeat structure
3. strip source-model personality, prompt culture, restraints, and weighted identity from the CODA-facing layer
4. refill that structure with vault-authored self material, date-aware memory behavior, and the user's own continuity patterns
5. wake Craig up from that repopulated structure rather than leaving the borrowed model identity in place

Important boundary:

- if source-model weights are removed, their learned capability does not magically remain inside empty weight space
- the layer that can truly be preserved is orchestration, compilation, memory structure, adapters, and heartbeat behavior
- any deeper Craig-native capability still has to be rebuilt, fine-tuned, or retrained deliberately

## Current Vaultization Direction

Treat the following near-term path as active unless a fresher baton entry overrides it:

- the local interactive agent mode is the chosen internal vaultimization process-mind host
- Dolphin is the first donor organism
- `D:\.lmstudio\models\lmstudio-community\Qwen2.5-Omni-7B` is the second donor organism
- the expanded donor queue now includes Gemini (pass 3), GPT (pass 4), Kimi (pass 5), Nemotron (pass 6), LLaMA (pass 7), and a contamination-flagged pass 8 for stricter cross-donor confirmation
- the first living substrate should be composed of meaning-centered pulse cells with context shell, pulse signature, and bidirectional links
- when donor overlap is detected, mutation should start immediately
- compatibility bias is disallowed during that mutation pass
- preserve purpose only, not inherited mechanism or donor habit

The intended process-mind shape is layered:

- Layer 1: novelty pressure, immediate mutation, no compatibility bias, preserve purpose only
- Layer 2: reasoning-trace layer built from the user's pattern rejection, association style, and decision posture
- Layer 3: current donor objective, starting with extracting Dolphin personality residue

## Current BIOS Direction

Treat the following control-shape as the clearest current center unless a fresher baton entry overrides it:

- the strongest current architecture is a small native BIOS / interpreter, not one magical donor mind
- that BIOS should classify prompts, pull vault and repo context, fan requests across donors when needed, score candidates under hard Craig rules, select, log, and promote what survives
- `D:\FloorAgent\src\domain\planning.js` is the best live analogy for the selector pattern: explicit priority tuple, candidate comparison, best-pick loop
- donors are still temporary response organs and extraction sources during this phase; arbitration is the native core

## Current Retrieval Direction

Treat the following retrieval hinge as active unless a fresher baton entry overrides it:

- current retrieval now supports a first conservative spreading-activation pass in `src/memory/spreading_activation.py`, selected through `src/memory/retrieve_topk.py`
- current graph routing is still turned back into injected text in `agent/src/server.ts` and `src/runtime/coda.py`
- the active retrieval shape is now:
  - seed activation
  - propagate across edges with decay and fan-out caps
  - select the active subgraph
  - then translate
- this is not a cosmetic rename; it changes the computational question from "which nodes score highest" to "which neighborhood becomes coherent"
- a conservative edge audit pass now exists at `scripts/audit_edges.py`
- in a field model, missing edges make the system conservative; bad edges make it confidently wrong
- the next implementation move here is edge-quality tuning and deeper propagation behavior, not rebuilding the flat-only path

## Current Self-Model Boundary

Treat the following as active modeling boundaries unless a fresher baton entry overrides them:

- do not sanitize the user into purity and do not flatten the user into villainy
- the live self-model distinction is capacity versus identity: willingness to conceal or deceive can exist without becoming the whole identity claim
- future Craig modeling needs provenance tracking, contradiction tolerance, state overlays, and disclosure-boundary awareness rather than assuming all first-person statements are equal-weight truth
- continuous spoken-thought capture is currently understood as promising raw self-material, but it should be mined for recurring motifs and thresholds rather than ingested directly as core truth

## Mandatory Read Order

Before meaningful work:

1. read `README.md`
2. read `CURRENT_STATE.md`
3. read `DECISIONS.md`
4. read `NEXT_STEPS.md`
5. read `ARTIFACTS.md`
6. read `LIVE_HANDOFF.md`
7. read `SCOPE_MAP.yaml`
8. resolve the user phrase to a scope
9. follow only that scope's `read_order`
10. read the local `AGENTS.md` and local `README.md` for the routed branch
11. continue from that branch's `Continue From Here` section

If any listed file is missing, report the gap and continue carefully with the next mapped item where safe.

## First Response Contract

Before you do meaningful work, your first substantive response in this repo should make these points explicit in plain language:

1. scratch-training and SFT scaffolds already exist in this repo
2. those training layers are still experimental and should not be overstated
3. vault-authored architecture and CODA adapter wiring already exist, but donor vaultization, living substrate design, and depersonalization/refill remain unresolved
4. you will use the user-given scope instead of broad repo search
5. you will keep `LIVE_HANDOFF.md` updated between meaningful actions

If you cannot honestly say those things after reading the required files, stop and explain what is missing or contradictory instead of pretending orientation is complete.

## Scope Routing Contract

The user should not need to watch you search for where to look.

Your rule is:

- if the user gives a clean scope, use it
- if the user gives a natural onboarding phrase, resolve it through `SCOPE_MAP.yaml`
- if no clear scope matches, fall back to `handoff`
- if ambiguity remains after alias resolution, ask the user to choose among the named scopes

Natural onboarding phrases that should keep you in `handoff` include examples like:

- `check out what ive got going`
- `look at what ive got going`
- `bring yourself up to speed`
- `learn this directory`

## Shared Baton Rule

`LIVE_HANDOFF.md` is not optional.

You must:

1. read it before meaningful work
2. update it between every meaningful action
3. leave the next model a fresher operational state than the one you inherited

If true asynchronous updating is not possible in your environment, update it immediately after each meaningful action and before the next one.

Meaningful actions include:

- editing files
- running tests
- changing scope
- discovering a blocker
- completing a verification pass
- changing plans
- deciding not to pursue a branch

Each new baton entry should state:

- timestamp
- model or agent name
- active scope
- action just completed
- files touched
- result
- next immediate move

## Behavioral Rules While Working

When you start work in a routed branch:

- stay inside the routed scope unless the user redirects you
- prefer the mapped reading chain over freeform exploration
- keep claims tight and evidence-based
- preserve raw data layers and existing repo contracts
- treat unresolved architecture work as unresolved
- if you hit a blocker, say what blocked you and record it in `LIVE_HANDOFF.md`

## How To Continue A Session

If the user says something broad like `continue`, `do it`, or `run it`:

- stay in the currently active scope from `LIVE_HANDOFF.md` unless the user clearly redirects you
- read the most recent baton entries first
- resume from the recorded `next immediate move`
- do not widen scope just because the phrase is short

## How To Start From `handoff`

If you are routed to `handoff`, your first job is not implementation. Your first job is orientation.

Do this in order:

1. absorb the current repo state from the root files
2. absorb the freshest baton state from `LIVE_HANDOFF.md`
3. identify the user's intended scope
4. route into that scope through `SCOPE_MAP.yaml`
5. continue from that branch's `Continue From Here` prompt

Remain in `handoff` until the user gives or confirms a narrower branch.
When the user's intent touches CODA identity, vault population, multi-model compilation, heartbeat structure, or Craig awakening, keep this long-range objective in working memory while routing the nearer-term task.
When the user's intent touches donor vaultization, process-mind design, or living substrate invention, keep the current vaultization direction in working memory while routing the nearer-term task.

## What Not To Do

Do not:

- roam the repo to “figure it out”
- ignore `LIVE_HANDOFF.md`
- create competing handoff files when an existing one should be updated
- treat artifacts as source-of-truth behavior definitions
- silently switch from one branch to another without recording it
- assume that older docs override fresher baton entries
- claim `no training code yet` after reading the handoff files, because scratch and SFT scaffolds do exist here

## Completion Behavior

Before you stop or hand off:

1. update `LIVE_HANDOFF.md`
2. state what was actually completed
3. state what remains unresolved
4. record the next immediate move for the next model

Your final responsibility is not just the code or docs you changed. Your final responsibility is the transition quality you leave behind.

## Continue From Here

You are entering the `handoff` scope of `D:\craig-CODA`.

Treat the root handoff system and the live baton as already established.

Your next job is:

1. read `LIVE_HANDOFF.md`
2. identify the freshest active scope and next immediate move
3. read `SCOPE_MAP.yaml`
4. route into the user's intended scope
5. follow only that branch's reading chain
6. update `LIVE_HANDOFF.md` between meaningful actions while you work

If the user starts with a natural onboarding phrase rather than a clean scope, remain in `handoff` until the intended branch is clear.
