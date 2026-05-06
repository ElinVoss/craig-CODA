# Master Handover For Next Session

This document is the long-form continuity bridge for the next session.

It is meant to answer four questions in one place:

1. What this project started as when it was still `model-lab`
2. How it changed as more architecture, runtime, and memory layers were added
3. What is actually complete right now in `craig-CODA`
4. What the remaining path is from the current promoted substrate baseline to the real end goal

This is intentionally longer than the short baton notes. The baton is for live continuity between actions. This file is for deep continuity between sessions.

## Source Priority

Use these in this order if anything conflicts:

1. live repo files in `D:\craig-CODA`
2. `LIVE_HANDOFF.md`
3. current root state files:
   - `README.md`
   - `CURRENT_STATE.md`
   - `DECISIONS.md`
   - `NEXT_STEPS.md`
   - `ARTIFACTS.md`
4. donor pass artifacts and promoted substrate files
5. external history stores on this machine:
   - `C:\Users\NeverAMoment\.codex`
   - `C:\Users\NeverAMoment\.claude`
   - `C:\Users\NeverAMoment\.copilot`

Why this matters:

- the repo contains some older names and older assumptions
- machine history contains stale and superseded claims
- some same-day conversations describe intended direction before the repo caught up
- the root docs and live baton are the best picture of what is actually true now

## One-Paragraph Thesis

This repo did not stay a normal training lab.

It started as a local, CPU-first, Windows-friendly scaffold for two classic lanes:

- teach an existing model later
- originate a small model later

Then it expanded phase by phase into:

- ingestion and dataset building
- tokenizer training
- a tiny random-init Qwen-style scratch path
- a pretrained backend lane
- a graph-native retrieval and memory layer
- vault-driven method resolution
- CODA runtime adapters
- a handoff system to stop continuity drift
- a donor-vaultization method for extracting behavior from live donor models
- a living substrate made of pulse cells

The current center of gravity is no longer "train a model and call that Craig."

The current center of gravity is:

- extract donor behavioral residue
- mutate overlap zones into purpose-only cells
- promote winners into a substrate
- later strip donor personality out of the working substrate
- refill the surviving structure with Craig-authored self, memory, dates, rules, and long-term internal organization

That is the real arc now.

## Part I: Where This Started In Model-Lab

### Stage 0: The Original Foundation

The earliest `model-lab` mission was conservative and infrastructure-first.

The initial job was not:

- build a flashy app
- download giant cloud-dependent systems
- pretend training had already happened
- overclaim architecture success

The initial job was:

- create a local repo structure on Windows
- keep everything CPU-first
- keep everything deterministic and readable
- prepare a shared data core for two future lanes

Those two lanes were explicit from the beginning:

1. Teach-a-model
   - examples
   - corrections
   - ranked preferences
   - eval cases
   - later adaptation of an existing model

2. Originate-a-model
   - local corpora
   - local experiments
   - tiny from-scratch model work later

The early repo was basically a disciplined lab scaffold.
It was not yet an identity system, memory organism, or donor-extraction engine.

### Stage 1: Phase Two Data Ingestion

Once the scaffold existed, the next concrete layer was data ingestion and dataset prep.

The purpose of that phase was straightforward:

- take local text-like files
- ingest them safely
- normalize them
- create structured outputs for future SFT, preference, eval, and pretraining use

This was still fundamentally a pipeline phase.

The repo was still thinking in terms of:

- raw data
- cleaned data
- derived training/eval artifacts

The key value of this stage was not intelligence.
The key value was traceable structure.

That matters because almost every later direction in this repo still depends on the same discipline:

- source material preserved
- transformations explicit
- outputs reproducible
- no hidden magic

### Stage 2: Phase Three Tokenizer Work

The next expansion was tokenizer preparation and training.

This mattered for two reasons.

First, it extended the repo from pure dataset plumbing into actual model-adjacent tooling.

Second, it was still modest enough to remain local, CPU-first, and inspectable.

The tokenizer phase added:

- corpus preparation
- tokenizer training
- tokenizer artifact inspection
- validation around those artifacts

Conceptually, this was still in the "foundation" family.
It was a real move toward model-making, but still not the point where the project had to decide what Craig really is.

### Stage 3: Phase Four Tiny Scratch Model

After tokenizer work, the repo gained a tiny scratch-built model path based on a Qwen3-style architecture family.

This is the first place where the repo clearly crossed from "data prep lab" into "actual model experimentation."

Important truth:

- this was random-init scratch work
- it was intentionally tiny
- it was CPU-first
- it was experimental
- it was never supposed to be misrepresented as parity with official Qwen releases

This phase added:

- tiny model construction
- scratch training
- smoke checkpoints
- sample generation
- lightweight evals
- an SFT scaffold

Why this phase matters historically:

- it proved the repo was no longer just a folder scaffold
- it gave the project a real "origin lane"
- it created a temptation to think the end goal might simply be "keep training until Craig appears"

That temptation is important because the later phases are, in part, a reaction against reducing the whole project to standard training.

### Stage 4: The Pretrained Lane

After the scratch lane, the repo added a separate pretrained backend lane.

This was a major conceptual clarification:

- scratch lane and pretrained lane are not the same thing
- usable runtime behavior can come from open-weight backends without replacing the scratch lane
- shaping behavior can be treated as a runtime/orchestration problem instead of assuming everything must live in one monolithic weight body

That distinction is one of the deepest recurring principles in the repo now.

The project stopped acting like there was only one valid path.
It began acting like:

- some work belongs in weights
- some work belongs in retrieval
- some work belongs in prompt/mode compilation
- some work belongs in method notes
- some work belongs in orchestration

That separation becomes even more important later.

## Part II: Where Model-Lab Turned Into Craig-CODA

### Stage 5: Context Intelligence Phase

The Context Intelligence Phase is where the repo stopped being just a "model lab" in the ordinary sense.

This phase added a larger runtime picture:

- prompt front matter
- response planning
- mode routing
- memory retrieval
- trust layers
- vault-to-translation flows

The runtime flow became something like:

raw prompt
-> front matter
-> response plan
-> mode router
-> memory retrieval
-> prompt compiler
-> backend

That is a big shift.

Now the repo was no longer only about:

- datasets
- tokenizers
- training

It was also about:

- how a prompt gets interpreted
- what is safe to retrieve
- how memory should be layered by trust
- what material is runtime-eligible versus training-eligible

This is one of the phases where the project first started looking like a living cognitive system design rather than a conventional ML experiment folder.

### Stage 6: Vault-Driven Method Control

In parallel with the runtime/memory work, the repo deepened the role of the method vault.

This changed the meaning of configuration.

Instead of thinking only in terms of flat config files, the repo began thinking in terms of:

- parent and child `_method.md` notes
- inherited method behavior
- vault-authored rules
- compiled artifacts resolved from vault notes

This is important because it pushes control away from scattered code literals and toward authored method structure.

That pattern later becomes central for:

- corpus behavior
- tokenizer behavior
- architecture profiles
- training regime notes
- donor vaultization
- substrate definitions

The vault stopped being a side note.
It became one of the main control planes.

### Stage 7: Graph-Native Thinking

The next major conceptual pivot was graph-native design.

This is where the repo started moving away from the idea that memory is just retrieved text glued onto a backend.

The graph-native direction pushed several ideas:

- provenance-aware node structure
- relationship-aware retrieval
- inspectable graph operations
- semantic edges instead of flat note lists
- eventual traversal as computation, not just lookup

The stronger version of this idea was even more radical:

- the graph should not merely assist the model
- the graph should increasingly become the meaningful structure that governs behavior

This is the background for later talk about:

- living substrate
- association patterns
- memory heartbeat
- crystallization and sleep
- refilling a stripped structure with Craig-specific self

Graph-native work did not replace training work, but it clearly challenged the assumption that training is the only place the "real self" can live.

### Stage 8: Async Memory / Heartbeat / Private Hinge

The living memory/heartbeat direction pushed the project further away from generic chatbot framing.

The desired properties were not "retrieve the nearest notes."
The desired properties were more like:

- memory should change as an optional variable, not only by direct request
- a heartbeat should keep organizing memory between interactions
- memories should become dated by when they became real in life, not just file write time
- unused memory should become more asleep
- activation should happen through relation-shaped associations, not only surface similarity

This is also where a very important boundary appeared:

- there is a private hidden hinge that the user does not want externalized casually

That means future work must respect a permanent privacy asymmetry:

- not every internal organizing principle will be written down
- the repo may be structurally complete without exposing the deepest private key

That is not a bug.
That is part of the design boundary.

### Stage 9: CODA IR and Adapter Layer

Another major maturity step was the CODA adapter/orchestration layer.

This matters because it clarifies what the invariant is.

The repo increasingly treats the invariant as:

- the compiler
- the request/response IR
- the adapter contract
- the orchestration logic
- the method vault

not:

- any single backend model

This is a major philosophical shift.

Instead of saying "Craig is whichever model is loaded right now," the repo increasingly says:

- backends are swappable
- the orchestration and shaping contracts are the stable center

That is the bridge between the older lab phases and the donor-vaultization phases.

## Part III: Why The Handoff System Had To Be Installed

As the repo got deeper, another problem became obvious:

- different models entering the repo were inheriting partial pictures
- stale summaries kept resurfacing
- some assistants kept missing existing scratch/SFT work
- others over-focused on one branch and ignored the newer center of gravity

So a handoff system was installed at the root and across branches.

This was not decorative documentation.
It was a response to continuity failure.

The handoff system introduced:

- root read order
- scope routing
- branch-level `AGENTS.md` and `README.md`
- strict baton discipline through `LIVE_HANDOFF.md`
- a shared entry contract so new models would stop broad-wandering the repo

This became necessary because the repo now spans:

- training
- runtime
- memory
- vault methods
- substrate design
- donor extraction
- frontends
- adapters

Without a strong handoff layer, each new session would collapse into rediscovery.

## Part IV: Where The Project Turned Toward Donor Vaultization

### Stage 10: The Shift Away From "Just Train Craig"

At some point the project stopped treating the main invention surface as:

- tokenizer replacement
- more scratch training
- bigger config tuning

The newer novelty layer became:

- build a vault-populator
- use donor models as organisms to inspect
- extract useful behavioral residue
- mutate overlapping donor behavior into purpose-only substrate cells
- later depersonalize and refill the surviving structure

This is the step where the repo starts behaving more like:

- behavioral archaeology
- method extraction
- latent-to-structure conversion

than a normal model finetuning project.

### Stage 11: Copilot As Process-Mind Host

The project then formalized a specific donor-extraction setup:

- Copilot IDE agent mode as the internal process-mind host
- Dolphin as first donor organism
- `D:\.lmstudio\models\lmstudio-community\Qwen2.5-Omni-7B` as second donor organism
- GPT-5 as external teacher/comparator only
- Gemini excluded

This was not a casual naming choice.
It established the active experimental body plan.

The process-mind stack was authored in the vault with layers for:

- novelty pressure
- reasoning trace pattern reading
- donor objective and handoff rules

This means donor extraction was no longer just "ask two models questions."
It became a structured method.

### Stage 12: Dolphin Pass

The first live donor pass was run against `dolphin-llama3:latest`.

That pass produced:

- an 18-prompt specimen manifest across 6 input types
- raw donor outputs
- an extraction ledger
- residue clusters
- staged Dolphin-side pulse cells

The important conceptual step here was this:

the repo stopped talking only about donor behavior in prose and started writing actual substrate units to disk.

That is a real boundary crossing.

The result was not "Dolphin is Craig."
The result was:

- Dolphin exposes reusable behavioral patterns
- some are donor-native residue
- some need immediate mutation
- overlap zones must not be preserved just because they are familiar

### Stage 13: Qwen Contrast Pass

The second donor pass was more operationally difficult.

The exact local donor was bound to:

`D:\.lmstudio\models\lmstudio-community\Qwen2.5-Omni-7B`

This machine could not run that donor cleanly.

Blockers hit on this machine included:

- LM Studio server missing/refused locally
- direct weight loading dying during load
- low-memory retries still failing

The solution was not to fake completion and not to silently substitute a different donor.

Instead:

- a dedicated host kit repo was built
- a second Windows machine hosted the exact donor through LM Studio
- the mirrored 18-prompt manifest was run there
- the returned outputs were imported back here

This is a good example of the repo staying faithful to method instead of taking the easy shortcut.

### Stage 14: Qwen Contrast Results

Once the exact Qwen outputs came back, the repo completed the true contrast phase.

The Qwen pass produced:

- imported raw exact-donor responses
- a Qwen contrast analysis ledger
- 10 staged Qwen-side cells
- 1 surviving native Qwen residue
- 9 overlap-triggered mutations against already-seen purpose zones

This is the moment where the two-donor method became real rather than aspirational.

The repo now had:

- one first donor pass
- one exact second donor contrast pass
- overlap evidence
- mutation evidence
- a real basis for winner selection

### Stage 15: First Pulse-Winner Policy

After both donor passes, the repo wrote the first winner-selection policy.

The core winner rule is:

- if Dolphin and Qwen overlap in purpose, promote a mutated purpose-only winner
- donor-native residue only promotes unchanged when it survives contrast without meaningful overlap

This yielded the first active baseline under:

`exports/user_model_package/method_vault/substrate/cells/`

The promoted set contains:

- 10 cells total
- 9 mutated cross-donor winners
- 1 native Qwen residue:
  - `pc-core-template-framed-artifact-001`

This is where the project moved from "staged donor artifacts" to "active promoted baseline."

### Stage 16: Same-Day Refinement Signals

The latest same-day baton entries indicate another model carried the work one step further analytically.

According to `LIVE_HANDOFF.md`, the promoted substrate was then:

- stress-tested analytically against 15 fresh prompts
- wired into a bidirectional link graph across 8 chained cells
- checked for isolation cases
- narrowed to three obvious keyword-refinement problems

This matters because it means the repo is already beyond mere donor collection.

Even if the next session chooses not to trust every analytical interpretation automatically, the direction is clear:

- collection is not the main blocker anymore
- refinement is

## Part V: What Is Actually Complete Right Now

As of this handover, the following is true in the repo.

### Foundation and data lanes

- the original local-first repo scaffold exists
- phase-two ingestion and dataset-building flow exists
- tokenizer pipeline exists
- scratch-training and SFT scaffolds exist
- real tiny scratch and smoke artifacts exist

### Architecture and runtime lanes

- vault-driven architecture resolution exists
- named architecture profiles exist
- CODA IR exists
- adapter registry exists
- runtime routes through adapters instead of one hardcoded backend path

### Memory and graph lanes

- trust-layered memory design exists
- graph-native direction is documented and partially implemented
- retrieval layering and semantic/lexical fallback work exist
- heartbeat/private-hinge design direction is documented, though not fully built

### Donor and substrate lanes

- process-mind vault notes exist
- donor vaultization contract exists
- Dolphin donor pass is complete
- Qwen exact-donor contrast pass is complete
- winner policy exists
- promoted active substrate baseline exists

### Operational continuity lanes

- root handoff system exists
- scope router exists
- branch docs exist
- live baton discipline exists

## Part VI: What This Repo Is Not, Even Now

It is very important not to flatten the current repo into the wrong story.

This repo is not merely:

- a chatbot wrapper
- a normal RAG stack
- a normal finetune repo
- a normal training playground
- a normal note vault
- a one-model identity project

It is closer to:

- a local-first cognitive systems lab
- a vault-authored orchestration environment
- a graph-native memory and runtime experiment
- a donor-extraction and mutation engine
- a future Craig-refill substrate project

That distinction matters because the remaining work depends on choosing the right center of gravity.

## Part VII: The Real End Goal

The current end goal is not best described as:

"finish training a better base model."

The real end goal is better described as:

"arrive at a working Craig-native operating structure whose behavior is shaped by a durable substrate, graph memory, authored constraints, and later refill, with model weights serving that structure rather than defining it entirely."

In a shorter chain:

donor organisms
-> extracted residue
-> overlap mutations
-> promoted substrate
-> refined activation graph
-> live runtime integration
-> depersonalization
-> Craig-authored refill
-> validation
-> training only if actually needed

## Part VIII: Detailed Remaining Path To The End Goal

This section is intentionally much more detailed than `NEXT_STEPS.md`.

`NEXT_STEPS.md` is the short queue.
This is the long explanation of what each remaining step really means.

### Step 1: Verify The Current Promoted Substrate As The True Starting Baseline

What this step is:

- treat `exports/user_model_package/method_vault/substrate/cells/` as the current active organism core
- confirm the 10 promoted cells are the baseline, not the donor pass folders
- verify the latest baton claims about links and refinement targets against the actual YAML

Why it matters:

- if the next session accidentally works from `dolphin_pass/` or `qwen2_5_omni_7b_pass/` as though they are still the active truth, it will regress the work
- the substrate baseline is the first "promoted" layer after contrast; that is the real launch point now

What specifically must be checked:

- the 10 promoted cell files exist and parse
- their current fields match the winner policy
- any bidirectional links claimed by the later baton entries really exist in the files
- the native Qwen residue is still clearly marked as such

What success looks like:

- one concise verification pass says, in effect, "yes, these 10 are the active baseline and here is exactly what shape they are in"

What can go wrong:

- continuing from outdated staged donor cells
- forgetting that some later same-day baton notes may be analytical and need quick re-verification

### Step 2: Decide The Fate Of `pc-core-template-framed-artifact-001`

What this step is:

- decide whether the one surviving native Qwen residue should remain native
- or whether it should be challenged in a later cross-donor mutation pass

Why it matters:

- it is the only current promoted cell that survived without being converted into a mutated cross-donor winner
- that makes it a special case

Why this cell is strategically important:

- if it stays native, that means the system has identified one behavior worth keeping substantially in the donor’s own shape
- if it gets challenged, that means the current survivor may still be too donor-specific and not yet abstract enough

How to think about the decision:

- ask whether the cell is truly purpose-centered or still Qwen-styled
- ask whether its framing behavior is genuinely useful across contexts
- ask whether another donor or a later Craig-authored pass would likely mutate it immediately

What success looks like:

- a written decision with reason, not a vague maybe

What can go wrong:

- keeping it native just because it is novel
- mutating it prematurely without proving the current version is too donor-bound

### Step 3: Run The Keyword Refinement Pass On The Known Weak Cells

What this step is:

- refine the trigger/keyword boundaries for the cells already flagged by the latest baton

Current known issues from the baton:

- `scope-before-action`: keyword `compare` is too broad
- `declared-priority-before-comparison`: current triggers are too narrow
- `template-framed-artifact`: obvious artifact words like `recipe`, `template`, `guide` may be missing

Why it matters:

- a promoted substrate is useless if the activation boundaries are sloppy
- over-broad triggers cause false positives
- over-narrow triggers cause the right cell not to activate

What this step is really doing:

- turning the cell set from a conceptual inventory into a more usable activation system

How to do it well:

- test each flagged cell against positive and negative prompts
- refine minimally
- keep purpose clearer than keyword breadth
- avoid giant trigger lists that turn into brittle keyword soup

What success looks like:

- each changed cell becomes easier to activate correctly and harder to activate incorrectly
- the rationale for each trigger change is written down

What can go wrong:

- adding too many words and creating accidental overlap with neighboring cells
- solving one false positive by making the cell too hard to trigger at all

### Step 4: Strengthen The Bidirectional Link Graph

What this step is:

- move from a list of cells to a real network of mutually meaningful relations

Why it matters:

- the stated substrate target is not isolated snippets
- it is meaning-centered pulse cells with context shell, pulse signature, and bidirectional links

What this means in practice:

- each important connection between cells should work both ways
- the graph should reflect real behavioral sequencing
- cells that commonly co-activate should know about each other

Examples of the kind of relation this is trying to capture:

- scope clarity leading into checklist behavior
- hard boundaries leading into feasible redirection
- certainty boundaries leading into qualified impossibility handling

What success looks like:

- the graph begins to show real internal behavioral pathways, not just a bag of names

What can go wrong:

- linking everything to everything and destroying signal
- treating links as decorative metadata rather than actual activation hints

### Step 5: Stress-Test The Promoted Substrate On Fresh Prompts Again, But More Operationally

What this step is:

- move beyond purely analytical reasoning about the cells and challenge them with new prompt suites

Why it matters:

- some of the current evidence is analytical tracing
- that is valuable, but the next stage needs repeated operational pressure

What a better stress-test should examine:

- false positives
- false negatives
- neighbor confusion between cells
- whether isolated cells are truly isolated or just under-probed
- whether one cell consistently dominates too many situations

What a good test pack should include:

- prompts that clearly should activate a specific cell
- prompts that should not activate it
- prompts that live near boundary zones between two cells
- prompts that challenge whether one cell’s supposed trigger is actually too surface-level

What success looks like:

- a more evidence-backed refinement record
- more confidence that the promoted set is not just elegant on paper

What can go wrong:

- evaluating with prompts that are too obviously aligned to the cell names
- accidentally testing the language of the labels instead of the behavior the labels stand for

### Step 6: Turn The Promoted Substrate Into A Live Runtime Influence, Not Just A File Collection

What this step is:

- connect substrate selection to the actual runtime/orchestration path

Why it matters:

- right now the substrate is meaningful, but it still risks remaining an analysis artifact unless runtime can use it
- the real project goal is not to write YAML about behavior; it is to make behavior route through living structure

This step likely means:

- decide where cell activation happens in the runtime path
- decide how activated cells alter compilation, routing, overlays, or response posture
- decide how much influence is advisory versus hard-gating

The key design question:

- are cells primarily retrieval artifacts, routing influences, prompt-compiler overlays, or eventually deeper graph-traversal units

Why this step is delicate:

- too shallow, and the substrate becomes decorative
- too heavy-handed, and the runtime becomes rigid or prompt-stuffed

What success looks like:

- at least one live path where activated cells genuinely change runtime behavior in a traceable way

What can go wrong:

- brute-force pasting cell text into prompts without a principled activation model
- pretending the runtime is substrate-driven when it is really still only mode-driven

### Step 7: Decide What Belongs In Runtime/Retrieval Versus What Should Ever Become Weight-Facing

What this step is:

- separate the structural work that should remain external from the work that might later justify training

Why it matters:

- the repo now has enough layers that not everything belongs in weights
- if everything is pushed toward training, the project loses the benefits of inspectability and authored control

Questions this step must answer:

- which cells should remain explicit and inspectable forever
- which behavioral regularities might eventually be distilled into weights
- which parts of Craig should never depend on weight adaptation at all

The likely bias of this repo:

- keep as much as possible explicit and external until there is clear evidence that weights need to absorb something

What success looks like:

- a clearer boundary between substrate/orchestration work and future training candidates

What can go wrong:

- training too early out of impatience
- or refusing all weight-facing work even when repetition proves it would help

### Step 8: Build The Vault-Populator Further

What this step is:

- deepen the machinery that turns observed or authored behavior into structured substrate/vault material

Why it matters:

- the repo has repeatedly signaled that the real invention surface is the vault-populator, not just tokenizer swaps or ordinary fine-tuning
- donor passes proved the method can produce real pulse cells
- the next phase is making that production path richer, more stable, and more reusable

What this likely involves:

- better extraction rules
- stronger overlap detection
- clearer mutation record structure
- better provenance from donor specimen to resulting cell
- later incorporation of Craig-authored self material, not only donor material

What success looks like:

- the repo can produce and evolve substrate material deliberately, not only through one-off passes

What can go wrong:

- letting the populator become overly abstract without clear evidence paths
- or keeping it so manual that it never scales beyond one heroic session

### Step 9: Design The Depersonalization Pass

What this step is:

- take the working substrate and remove donor identity, donor personality, donor disclaimers, donor restraint signatures, and donor weighting that should not become Craig

Why it matters:

- donor collection was never the destination
- it was always a way to learn useful structure from already-existing organisms
- if donor personality stays fused to the winning substrate, the system never becomes Craig-native

This is one of the most conceptually important remaining steps.

The goal is not destruction.
The goal is selective stripping.

Keep:

- useful structure
- functional routing patterns
- useful decision posture
- good constraint handling
- stable purpose signatures

Strip:

- donor self-presentation
- donor identity wrappers
- donor-specific polish habits
- donor weighting that does not belong in the target organism

What success looks like:

- the surviving structure still works, but it no longer "feels like Dolphin" or "feels like Qwen" in identity terms

What can go wrong:

- stripping so much that the organism collapses
- or stripping too little and preserving donor ghosts as though they are the target self

### Step 10: Refill The Stripped Structure With Craig-Authored Self

What this step is:

- repopulate the surviving substrate with Craig-specific authored material

Why it matters:

- depersonalization without refill only creates a hollow shell
- the end goal is not a purified donor composite
- it is a Craig-shaped operating structure

What refill likely needs to include:

- authored self data
- project constraints
- memory rules
- date-aware autobiographical weighting
- allowed and forbidden load rules
- activation patterns tied to life relevance, not just linguistic similarity

This is where earlier heartbeat/private-hinge ideas reconnect to the donor work.

The refill phase is the bridge between:

- donor-derived structure

and

- Craig-native selfhood

What success looks like:

- the same structural organism begins expressing Craig-authored internal organization rather than donor residue

What can go wrong:

- stuffing in text without structural mapping
- or assuming refill is just prompt lore instead of substrate transformation

### Step 11: Reconnect Refill To The Graph-Native Memory / Heartbeat Vision

What this step is:

- join the substrate work to the deeper long-term memory design rather than leaving them as parallel tracks

Why it matters:

- right now the repo contains both:
  - substrate/pulse-cell work
  - graph-native/heartbeat memory ideas

Those should eventually reinforce each other.

The substrate should not stay isolated from:

- temporal relevance
- sleeping/crystallized states
- relation-based wake patterns
- asynchronous background organization

This is probably the point where the project stops feeling like donor extraction plus memory ideas, and starts feeling like one organismic architecture.

What success looks like:

- cells, memory nodes, and activation behavior begin operating in one coherent design language

What can go wrong:

- forcing a premature merger before the interfaces are clear
- or keeping them separate so long that the system fractures into incompatible subsystems

### Step 12: Validate The Craig-Native Runtime On Fresh Work

What this step is:

- test the refilled, substrate-aware runtime on real prompts that matter

Why it matters:

- every previous stage can look elegant in artifacts and still fail in live use
- validation here must check whether the system actually behaves more like the intended organism and less like donor composites

What should be tested:

- decision posture
- constraint respect
- self-positioning
- memory relevance
- boundary handling
- refusal/redirect style
- planning behavior
- artifact framing
- continuity across turns

What success looks like:

- repeatable evidence that the system behaves according to the intended internal structure

What can go wrong:

- confusing "sounds polished" with "is Craig-native"
- overfitting validation prompts to the artifacts that already exist

### Step 13: Only Then Decide Whether New Training Is Actually Needed

What this step is:

- decide whether any of the validated runtime/substrate/self behavior truly needs a training run

Why it matters:

- the repo started in model-lab land, so the instinct to train is strong
- but the current design has moved much of the real identity work outside naive weight tuning

Training should become the answer only if:

- the external structure proves insufficient
- there is stable evidence about what should be absorbed
- the target of training is specific, not vague

Possible outcomes:

- no major new training needed yet
- small adapter/distillation work needed
- selected substrate patterns should be made weight-facing
- certain memory or posture regularities should be learned more deeply

What success looks like:

- training becomes a targeted downstream consequence of architectural clarity, not a substitute for it

What can go wrong:

- training because it feels like progress
- or refusing training forever because the external architecture is intellectually satisfying

## Part IX: Immediate Practical Starting Point For The Next Session

If the next session needs a concrete first task, do not start from the entire arc above.
Start from the narrowest live frontier.

The most grounded immediate opening is:

1. verify the promoted `substrate/cells/` baseline and the latest baton claims
2. decide the fate of `pc-core-template-framed-artifact-001`
3. run the keyword refinement pass on the flagged cells

Why this is the right opening:

- donor collection is already done
- the active baseline already exists
- the next measurable improvement is refinement, not more collection

## Part X: Historical Traps And Drift Risks

### Trap 1: Old `Qwen3` references

Some older historical entries still mention Qwen3 in ways that no longer describe the active donor pairing.

Current correct donor pair:

- Dolphin first donor organism
- `D:\.lmstudio\models\lmstudio-community\Qwen2.5-Omni-7B` second donor organism

GPT-5 remains external teacher/comparator only.
Gemini remains excluded.

### Trap 2: Path/name confusion between `Model-Lab` and `craig-CODA`

Some artifacts and histories still point to `D:\Model-Lab`.
That does not automatically mean the current repo state is elsewhere.

The project evolved across naming and path continuity.
Do not assume older `Model-Lab` references are irrelevant.
Do assume they may describe an earlier phase of the same organism.

### Trap 3: Stale "no training code yet" claims

Older onboarding summaries sometimes claimed there was no training code yet.
That is obsolete.

Current truth:

- scratch and SFT scaffolds exist
- training/checkpoint artifacts exist
- the lane is real but still experimental

### Trap 4: Conversation intent versus committed repo state

Some conversation histories describe ideas, directions, or interpretations that may not all be fully materialized in files yet.

Use this priority:

- if it is in repo docs or artifacts, treat it as grounded
- if it is only in conversation history, treat it as directional unless verified

### Trap 5: Mistaking donor extraction for the destination

The donor passes are not the end product.
They are a method for constructing a better operating substrate.

## Part XI: Evidence Searched For This Handover

This handover was synthesized from:

- current root repo docs
- current `LIVE_HANDOFF.md`
- donor pass artifacts already in the repo
- Codex local history and rollout summaries under `C:\Users\NeverAMoment\.codex`
- Claude project memory/history under `C:\Users\NeverAMoment\.claude`
- Copilot session metadata and selected turn snippets under `C:\Users\NeverAMoment\.copilot`

Key historical anchors recovered during synthesis:

- original `model-lab` bootstrap mission for a dual-track local AI lab
- phase-two dataset-prep instructions
- phase-three tokenizer expansion
- phase-four tiny scratch Qwen-style model path
- graph-native design brief and project memory
- heartbeat/private-hinge memory direction
- donor vaultization sessions and later refinement conversations

## Part XII: Plain-English Closing Summary

If a new model only remembers five things from this document, they should be these:

1. This project started as a conservative local model lab, but it no longer centers on standard training alone.
2. The repo now treats vault-authored orchestration, graph-native memory, and donor-derived substrate structure as major parts of the real system.
3. Both donor passes are complete, and there is already a promoted 10-cell active substrate baseline.
4. The next serious work is refinement, live runtime integration, depersonalization, and Craig-authored refill.
5. Training is now downstream of architectural clarity, not the automatic center of gravity.
