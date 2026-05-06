# Startup Prompt Of Record

Read every word in this file before doing meaningful work in `D:\craig-CODA`.

This is the canonical startup prompt for any model entering this directory. If you are `Codex`, `Claude`, `Copilot`, or any other model being pointed here for work, you must treat this as the operating contract for how to learn, navigate, and continue the repo.

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

- Copilot IDE agent mode is the chosen internal vaultimization process-mind host
- Dolphin is the first donor organism
- `D:\.lmstudio\models\lmstudio-community\Qwen2.5-Omni-7B` is the second donor organism
- GPT-5 is allowed only as an external teacher/comparator
- Gemini is excluded from the donor architecture
- the first living substrate should be composed of meaning-centered pulse cells with context shell, pulse signature, and bidirectional links
- when donor overlap is detected, mutation should start immediately
- compatibility bias is disallowed during that mutation pass
- preserve purpose only, not inherited mechanism or donor habit

The intended Copilot process-mind shape is layered:

- Layer 1: novelty pressure, immediate mutation, no compatibility bias, preserve purpose only
- Layer 2: reasoning-trace layer built from the user's pattern rejection, association style, and decision posture
- Layer 3: current donor objective, starting with extracting Dolphin personality residue

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
When the user's intent touches donor vaultization, Copilot process-mind design, or living substrate invention, keep the current vaultization direction in working memory while routing the nearer-term task.

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
