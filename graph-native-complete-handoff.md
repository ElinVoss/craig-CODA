# Graph-Native Model Architecture: Complete Build Specification
**Self-contained handoff document — requires no companion files**
**All architecture decisions, implementation details, schemas, algorithms, evaluation criteria, and failure conditions are in this document.**

---

## Part I: What This Is

### 1. The Core Question

Everything in this document exists to progressively answer one question:

**Can deliberately structured graphs produce coherent, contextually appropriate responses through traversal, rather than through learned weight matrices?**

That question decomposes into four sub-questions, ordered from most tractable to least:

1. Can GGUF models be meaningfully decomposed into named capability circuits that survive extraction? *(Engineering + interpretability research)*
2. Can a strong model reliably classify semantic relationships between arbitrary node pairs at construction time? *(Engineering + validation design)*
3. Can multi-axis constraint filtering produce demonstrably better subgraph selection than flat semantic retrieval? *(Engineering + evaluation)*
4. Can an activated subgraph compose into a coherent response without a conventional language model backend? *(Open research — the genuinely hard one)*

Every phase of the build is designed to answer one of these. If a phase answers its question negatively, the architecture either pivots or the project learns something valuable about why not. No phase is wasted work.

### 2. The Constitutional AI Parallel — The Fastest Way to Understand This

If you need to understand the entire architecture in one paragraph, here it is:

**The graph is a constitution.** In Anthropic's Constitutional AI, a strong model writes a set of principles — the constitution. A weaker model is trained to follow those principles. The principles are explicit, inspectable, and modifiable. Changing a principle changes behavior predictably.

In this architecture:
- The graph IS the constitution — a set of named nodes (knowledge, capabilities, constraints) connected by typed, weighted edges (causal, contradicts, prerequisite_of, etc.)
- A strong external model (Claude Opus, GPT-5.5, or similar) writes the constitution during an offline construction pass — classifying nodes, typing edges, flagging contradictions
- The traversal engine enforces the constitution — when a query arrives, the graph's structure determines what can respond to it, not a model's internal weights
- The composition operator generates responses within constitutional constraints

This framing clarifies the value proposition: even if the composition operator never fully replaces a conventional language model backend, a system with an explicit, inspectable, modifiable constitution is a genuine advance over black-box weight matrices. You can read the graph. You can edit the graph. You can predict what happens when you edit the graph.

### 3. What This Is Not

Every existing framework will try to map this onto something familiar. Resist that.

- **It is not RAG** (Retrieval-Augmented Generation). RAG bolts a search index onto an existing model at inference time. The model itself remains a black box. Crucially: traversal + concatenation of node content is still RAG, just with a better retrieval architecture. That is a meaningful improvement and it is the honest near-term deliverable — but it is not the goal. The goal is traversal as computation, and that distinction is the hardest part to make real.
- **It is not a knowledge graph with an LLM on top.** That pattern uses the graph as a lookup tool, with the model doing the "real" work. Here the graph does the work — or at minimum, the graph imposes structural constraints that the model cannot ignore.
- **It is not a fine-tune or adapter** over an existing pretrained model. The point is not to adjust someone else's model.
- **It is not a GNN** (Graph Neural Network) in the traditional sense. GNNs still reduce to learned weight matrices. The whole point here is that the organizational structure is explicit, not learned.
- **It is not craig-coda**, which is a Qwen3-0.6B architecture with random-initialized weights being trained from scratch — that copies someone else's structure.

### 4. The Core Idea: Graph as Parameter Space

Current transformer models encode statistical co-occurrence across billions of tokens into floating-point weight matrices. The relationships between concepts are implicit, opaque, and emergent — nobody designed them, they fell out of gradient descent. You cannot inspect a weight matrix and read "this head handles causal reasoning about time."

The proposal is to invert this.

**The graph is the parameter space.**

Instead of weights that accidentally form relationships, the architecture begins with relationships as the explicit structure, and derives computation from traversal of that structure.

Concretely:
- A **node** is a named unit of capability, knowledge, or constraint. It has typed properties: trust level, temporal scope, domain, voice signature, reasoning mode, provenance.
- An **edge** is a typed, weighted relationship between nodes: `causal`, `contradicts`, `stylistically_similar`, `prerequisite_of`, `extracted_from`, `domain_co-occurrence`, `refines`, `exemplifies`.
- **Inference is graph traversal** — a query enters the graph as a typed node, activates relevant nodes by relevance scoring, follows edges to neighboring nodes weighted by edge type relevance, and the response is assembled from the activated subgraph.
- The tokenizer is an **interface at the boundary**, not part of the core structure. Any tokenizer can encode a query into the graph's semantic space and decode a response back out. The internal representation is tokenizer-agnostic.

This is how a story bible works in Obsidian with the graph view: every note is a node, every link is an edge, and "understanding the story" is the act of traversing that graph with a question. The difference is that here, the graph **computes** rather than just stores.

### 5. The Prompt Is Not a Visitor

This is the key structural difference from RAG that is easy to miss.

In RAG, the prompt is external. It hits the retrieval system, pulls context, gets concatenated, goes to the model. The prompt and the knowledge are different kinds of things. The prompt is a visitor.

In this architecture, the prompt becomes **native to the graph.** It enters as a structured node with typed properties — intent, domain, stakes, reasoning mode, privacy level — and those properties are **constraints on traversal, not suggestions.** The graph cannot ignore them because they determine which edges are eligible to follow.

A query tagged `reasoning_mode: audit` literally cannot activate nodes in the `voice: narrative` cluster if the traversal algorithm respects typed edges. The structure of the query shapes the structure of what can respond to it. Decision-making falls out of graph reachability, not model choice.

**The underspecification problem:** When the front matter classifier produces a low-confidence classification, the query's entry node is underspecified. Traversal from an underspecified node can reach more of the graph than intended — similar to a fuzzy search returning too many results. This is where silent failures happen. The query goes somewhere reasonable-seeming but wrong, and nothing in the system flags it. The contradiction-handling design and the underspecification problem are the same problem from different angles: both are about what happens when the graph cannot deterministically resolve a path.

### 6. Five Organizational Axes

Existing models have a single flat organization: token embedding → attention layers → MLP layers → output head. The only "structure" is depth (more layers = more capacity).

This architecture has multiple orthogonal organizational axes simultaneously:

**Trust layer:** How stable/reliable is this node?
- `stable_core` — durable, high-confidence knowledge or capability
- `interpretive_maps` — derived analysis, contextual interpretations
- `episodic_events` — time-bounded observations, specific incidents
- `review_only` — flagged for human review, never auto-loaded at runtime

**Domain:** What subject area does this node operate in? (e.g., warehouse_operations, fiction_writing, machine_learning, legal, medical)

**Temporal scope:** Is this node a durable truth, a recent event, or a time-bounded constraint? Nodes have `time_start` and `time_end` fields. Temporal decay scoring penalizes stale nodes.

**Voice signature:** What expressive register does this node speak in? Scored on `voice_score`, `reasoning_score`, `prose_score` axes. A node with high `prose_score` and low `reasoning_score` is narrative; the reverse is analytical.

**Reasoning mode:** Does this node contribute to logical inference, narrative generation, causal analysis, constraint enforcement, or creative exploration?

**Provenance:** Where did this node come from? Human-authored, GGUF extraction (which model, which layer, which head), episodic event, training artifact, strong model construction.

A query doesn't just activate nodes by semantic similarity — it activates a **subgraph** filtered by multiple axes simultaneously. A technical question in a creative writing context activates a different subgraph than the same technical question in an audit context, even if the words are identical.

### 7. Computation Levels — The Honest Spectrum

The architecture is not binary (RAG vs. graph-native computation). There are five discrete levels, each a meaningful milestone:

| Level | Name | What Happens | Backend Role | Status |
|-------|------|-------------|-------------|--------|
| **0** | Context retrieval | Graph retrieves nodes → concatenated into prompt → backend generates | Backend does all generation | **craig-CODA is here now** |
| **1** | Inspectable routing | Front matter classifier selects subgraph by typed axes → subgraph content sent to backend → backend generates within constraints | Backend generates, but the *selection* is graph-native and fully logged | **First real target** |
| **2** | Constrained generation | Graph selects, orders, and weights content → backend generates but is constrained by graph structure (must address nodes in activation order, must flag contradictions) | Backend generates under graph-imposed constraints | Tractable next step after L1 |
| **3** | Hybrid composition | Graph assembles response skeleton from node content → backend fills gaps, smooths transitions, handles novel phrasing | Backend is a polishing layer, not the primary author | Requires composition operator design |
| **4** | Graph-native inference | Traversal produces the response. Backend is not involved. Tokenizer is an adapter at the boundary. | None | The north star. Open research. |

Each level is a shippable milestone. Level 1 is already worth building. Level 2 adds real behavioral constraints. Level 3 is where the composition operator question gets tested. Level 4 is the research frontier.

The build targets Level 1 as the first deliverable, Level 2 as the second, and treats Level 3-4 as research phases that may or may not succeed. The project succeeds at Level 2 even if Level 4 turns out to be unreachable.

---

## Part II: The Existing Foundation

### 8. What craig-CODA Already Has

The repository at `D:\craig-CODA` has already built several components that move toward this architecture, though they are not yet connected into a unified inference engine.

### 8a. Node Schema (`configs/node_schema.yaml`, `src/memory/node_schema.py`)
A typed node definition with:
- `id`, `node_type`, `trust_layer`, `content`, `summary`
- `time_start`, `time_end`, `life_phase` (temporal axis)
- `people`, `projects`, `tags`, `links` (relational metadata)
- `confidence`, `reinforcement_count` (epistemic metadata)
- `voice_score`, `reasoning_score`, `prose_score` (capability signature scores)
- `privacy_level` (access control)

This is a strong foundation. The schema already captures most of the organizational axes.

**Required addition — provenance fields (must be added before any mining writes nodes):**

```yaml
extracted_from:
  model_name: string        # "Qwen3-4B-Instruct"
  model_file: string        # "Qwen3-4B-Instruct-2507-Q4_K_M.gguf"
  layer_index: int | null
  head_index: int | null
  component_type: string    # "attention_head", "mlp_neuron", "residual_stream"
  activation_pattern: string # human-readable description of what triggers this head
  extraction_method: string  # "TransformerLens_probing", "activation_clustering", etc.
  extraction_timestamp: ISO-8601
  confidence: float          # how clean was the extraction (0.0-1.0)
  polysemantic: boolean      # does this head serve multiple functions
  polysemantic_roles: string[] | null  # if yes, what are they
```

The `polysemantic` flag is critical. Anthropic's own interpretability research (Scaling Monosemanticity, circuits work) shows most attention heads serve multiple functions. The mining pipeline will encounter this constantly. A node extracted from a polysemantic head must be flagged so downstream systems know the capability attribution is fuzzy, not clean.

For human-authored nodes that were not mined from a model, set `extracted_from: null`.

### 8b. Edge Building (`src/memory/build_edges.py`)
Typed edges with weights:
- `same_source` (0.55) — nodes from the same document
- `shared_tag` (0.45) — nodes sharing a tag
- `shared_project` (0.65) — nodes in the same project scope
- `shared_link` (0.75) — nodes that explicitly link to the same target

**Current gap:** Edge types are structural (where did nodes come from) not semantic (what is the nature of the relationship between what they mean). Missing edge types that must exist:
- `causal` — A causes or leads to B
- `contradicts` — A and B make incompatible claims (load-bearing for contradiction handling)
- `prerequisite_of` — understanding A is required to understand B
- `stylistically_similar` — A and B share voice, register, or expressive quality
- `refines` — B is a more specific or updated version of A
- `exemplifies` — B is a concrete example of the general claim in A
- `extracted_from_model` — A was mined from the same model component as B
- `unrelated` — explicitly marked as having no meaningful semantic relationship (prevents re-classification)

### 8c. Graph Indexing (`src/memory/index_graph.py`, `index_semantic.py`, `index_temporal.py`, `index_voice.py`)
Multi-index retrieval:
- Graph adjacency traversal
- Semantic (currently lexical overlap — needs upgrade to embedding-based)
- Temporal decay scoring
- Voice/style scoring

Score fusion (`src/memory/score_fusion.py`) combines these into a ranked top-k. This is the retrieval engine. It works but is currently lexical-only on the semantic axis, which means "reasoning" and "inference" are not connected unless they share a token.

### 8d. Runtime Architecture (`src/runtime/`)
A full prompt pipeline:
```
raw prompt
→ front matter classifier (intent, domain, style, reasoning_mode, stakes)
→ response plan builder (selects backend, mode, retrieval profile)
→ memory retrieval (graph + semantic + temporal + voice scores)
→ prompt compiler (assembles context into prompt)
→ backend (Ollama / scratch model / pretrained transformers)
```

The front matter classifier (`configs/prompt_front_matter.yaml`) already classifies queries along many of the organizational axes.

**This system is already proto-graph-native.** What the runtime does — intent + domain + style + reasoning_mode → selects retrieval profile → selects backend — is a routing system that activates different subsets of the system based on typed query axes. That is structurally closer to the goal than naive retrieval. The gap is that it routes to a monolithic backend rather than routing to a composed set of nodes. Closing that gap is a more tractable first version of graph-native inference than building a full traversal engine from scratch. The front matter classifier does not need to be replaced — it needs to stop sending traffic to a single backend and start selecting a subgraph instead.

### 8e. Trust Layer Access Control
Nodes are tagged with trust layers and the retrieval system enforces which layers are eligible at runtime vs. training time. `review_only` nodes never auto-load. This is a real access control system, not just metadata.

### 8f. Translation Layer (`src/translation/`)
Translates vault nodes into:
- SFT (supervised fine-tuning) training pairs
- Adapter manifests
- Runtime context bundles
- Prose/style outputs

This is the bridge between the graph and training artifacts.

### 9. GGUF Mining — Extracting Named Capabilities From Existing Models

Existing pretrained models (stored as GGUF files) contain real, learned capability. The idea is not to copy their architecture but to **mine them for named capabilities** and import those as seeded nodes.

How this works:

1. **Load a GGUF** using `gguf-py` or `llama.cpp` tensor inspection tools.
2. **Identify capability circuits** — specific attention heads or MLP neurons that activate for particular task types (math reasoning, instruction following, code generation, narrative coherence). This is mechanistic interpretability work.
3. **Name and classify** each extracted capability as a node with typed metadata.
4. **Do not copy weights directly** — use the activation patterns and the capability signature as structural seeds for the corresponding node in the graph.

The result: instead of starting from random initialization, the graph is bootstrapped with real learned capability extracted from diverse models, each capability placed at a named position in the graph rather than buried in a weight matrix nobody can read.

**The hidden assumption to confront:** The architecture assumes transformer attention heads have cleanly separable capabilities that can be named and extracted. Anthropic's interpretability research shows this is partially true. Some heads are clearly identifiable (induction heads, copy heads, syntactic heads). But most heads are polysemantic: they activate for multiple unrelated tasks, and their "capability" is an emergent property of their interaction with neighboring heads.

**What this means for the pipeline — three tiers of extraction:**
- **Clean capabilities** — heads that clearly serve a single function (rare but real). These become high-confidence nodes with `trust_layer: stable_core`.
- **Fuzzy capabilities** — heads that seem to specialize but activate for multiple related tasks. These become nodes with `polysemantic: true`, `trust_layer: interpretive_maps`, and a list of candidate roles.
- **Opaque capabilities** — heads whose function can't be clearly named. These get logged but NOT imported as nodes until the function is understood. The graph's value is in named, inspectable structure — importing opaque capabilities undermines that.

Available models to mine:
- `dolphin-llama3` (8B, Llama3 base): instruction following, uncensored response patterns
- `Qwen3-4B` (Alibaba, chain-of-thought): reasoning chains, multilingual, structured output
- `Qwen3-14B` (Alibaba, larger): deeper capability circuits, offline mining only (too large to run on target hardware)
- `craig-coda` checkpoints: domain-specific signals from custom training data

### 10. Strong Model Bootstrapping — The Construction Tool

The underspecification problem and the semantic edge gap are both solved by the same approach: **use a powerful external model as a construction tool during the offline build pass.**

During graph construction, a model like Claude Opus or GPT-5.5 is attached — not as part of the inference architecture, but as a one-time data structuring tool. It performs the expensive semantic work that the smaller system cannot do reliably:

- Reads raw data and decides what node type it should be, what trust layer, what domain axes
- Classifies relationship type and weight between node pairs
- Flags contradictions before they are embedded as silent conflicts — creating explicit `contradicts` edges
- Structures underspecified inputs into fully-typed graph entries with high confidence

By the time inference runs, the graph is already well-formed. The underspecification problem does not hit at runtime because the strong model resolved it during construction.

**What the strong model contributes:** Its judgment gets crystallized into graph structure. This is not distillation — no weights are copied. What is extracted is *decisions*: how a very capable model structured knowledge, made explicit and inspectable in the graph rather than buried in matrices.

**The critical quality control implication:** In a weight-matrix model, a wrong structural call gets averaged with other signals and softened. In the graph, a wrong classification by the strong model is a named, load-bearing edge. Downstream traversal trusts it. Error rate in the construction pass matters more here than in conventional training. The construction pass needs multi-layer validation (detailed in Phase 1 below).

---

## Part III: The Complete Build

### 11. Evaluation Framework — Define Before Building

You cannot know if the system works if you haven't defined what working means. These six evaluation criteria must exist before any code is written. Every phase is measured against them.

#### 11a. Retrieval Quality
**What it measures:** Does the right subgraph activate for a given query?

**Method:** Build a test suite of 50-100 query/expected-subgraph pairs. These are hand-authored: "given this query with these typed axes, these specific nodes should activate, and these should not." Run after every retrieval change.

**Example test case:**
```yaml
query: "What is the causal chain that leads from X to Y?"
axes:
  reasoning_mode: causal
  domain: [specified domain]
  trust_required: stable_core
expected_activated: [node_A, node_B, node_C]
expected_not_activated: [node_D]  # same domain but narrative mode, not causal
```

This is the most important eval. If retrieval is wrong, nothing downstream matters.

**Writing this test suite is the hardest item in the entire build plan** — because it forces you to define what "right" looks like before the system exists to show you. You have to sit with the node schema, the edge types, the axis definitions, and describe the expected subgraph for each query by hand. The discomfort of doing this is the point. If you can't describe the expected subgraph for 50 queries without running the system, you don't understand the system well enough to build it yet. Every place where you hesitate — "I'm not sure which nodes this should activate" — is a place where the architecture has an unresolved design question. The eval suite doesn't just measure the system; writing it finishes the design.

#### 11b. Routing Determinism
**What it measures:** Do identical queries with different axis constraints activate different subgraphs?

**Method:** Pairs of queries with identical content but different front matter classifications. The activated subgraphs should differ in predictable ways.

**Example:**
```
Query: "Explain the failure mode in system X"
Variant A: reasoning_mode: audit, stakes: high
Variant B: reasoning_mode: narrative, stakes: low

Variant A should activate: formal analysis nodes, constraint nodes, contradiction-surfacing
Variant B should activate: narrative explanation nodes, stylistic nodes
Overlap should be partial but not complete.
```

This eval proves the multi-axis architecture is doing real work — that the axes aren't decorative.

#### 11c. Inspectability
**What it measures:** Can a human read the traversal path and understand why a particular response was produced?

**Method:** Qualitative. For every test query, the system must output a traversal log that a person can read and say "yes, I understand why these nodes were selected and in what order." If the log requires expertise in the system's internals to interpret, the inspectability claim is false.

#### 11d. Contradiction Handling
**What it measures:** Does the system correctly identify contradicting nodes and handle them according to the chosen policy?

**Method:** Seed the graph with deliberate contradiction pairs. Run queries that activate both. Verify the system detects the contradiction and applies the correct resolution strategy.

#### 11e. Response Quality
**What it measures:** Is the composed response coherent, accurate, and contextually appropriate?

**Method:** Side-by-side comparison against the same query answered by:
- (a) The backend alone with no graph context
- (b) The backend with flat retrieval (current craig-CODA, Level 0)
- (c) The backend with graph-native routing (Level 1)

Use the strong model (Opus) as a judge: "Which response is more coherent, more relevant, more appropriately scoped?" Not a perfect eval but a usable one.

#### 11f. Behavioral Predictability
**What it measures:** When a node is added, removed, or modified, does the system's behavior change in the way you'd predict?

**Method:** Modify a single node. Re-run the test suite. The queries that should be affected change; the queries that shouldn't be affected don't. This is the "story bible" property — edit a character's backstory and every scene involving that character updates, but scenes involving other characters stay the same.

This eval is unique to this architecture. Weight-matrix models cannot do this. If this eval passes cleanly, it's the strongest argument for the whole approach.

### 12. Instrumentation — Traversal Logging From Day One

Every traversal must be logged from the first prototype. Not as a debugging afterthought — as a first-class output of the system. This is what makes the inspectability claim real.

**Traversal Log Schema:**
```yaml
traversal_id: uuid
timestamp: ISO-8601
query_node:
  raw_text: string
  classified_axes:
    intent: string
    domain: string[]
    reasoning_mode: string
    stakes: string
    voice: string
  classifier_confidence: float
  underspecification: string | null  # null, "partial_constraint", or "semantic_only"
seed_nodes:
  - node_id: string
    activation_score: float
    activation_reason: string  # "semantic_similarity", "domain_match", "tag_match", etc.
edge_traversals:
  - from_node: string
    to_node: string
    edge_type: string
    edge_weight: float
    traversal_depth: int
contradictions_detected:
  - node_a: string
    node_b: string
    resolution: string  # "trust_hierarchy", "surfaced", "stakes_gated"
    winner: string | null
final_subgraph:
  - node_id: string
    final_activation: float
    position_in_composition: int
response_metadata:
  backend_used: string
  composition_method: string  # "concatenation", "constrained", "hybrid", "graph_native"
  total_nodes_considered: int
  total_nodes_activated: int
  traversal_depth_max: int
  stopping_reason: string  # "max_depth", "activation_threshold", "fixed_count"
```

Store as JSONL alongside nodes and edges. These logs are also training data for the composition operator later — you need to know which traversal paths produced good responses and which didn't.

**Minimum viable traversal log (human-readable format):**
```
Query entered as node: {typed properties}
Seed nodes activated: [list with scores]
Edge traversal: seed_A --(causal, 0.82)--> node_B --(prerequisite, 0.71)--> node_C
Contradiction detected: node_B contradicts node_D (resolution: trust hierarchy, node_B wins)
Final subgraph: [ordered node list with activation scores]
Response assembled from: [node content excerpts in composition order]
```

---

### 13. Phase 1: Graph Foundation

**Goal:** Build a graph worth traversing. Produce real mined nodes, real semantic edges, real embedding-based retrieval. Everything here is known-how engineering, not research.

**Duration estimate:** 3-5 weeks of focused work.

**Answers sub-question 1:** Can GGUF models be meaningfully decomposed into named capability circuits?

#### 13a. Provenance Schema Upgrade
**What:** Add `extracted_from` field to node schema (full schema in Section 8a above).

**Deliverables:**
- Updated `configs/node_schema.yaml`
- Updated `src/memory/node_schema.py`
- All existing node writers updated to include provenance fields
- Migration script for existing nodes (sets `extracted_from: null` for human-authored nodes)

**Depends on:** Nothing. Do this first.

#### 13b. GGUF Mining Pipeline
**What:** Load GGUF files, extract tensor data, identify capability circuits, write nodes in the existing schema.

**Concrete implementation steps:**

```
Step 1: GGUF tensor reader
  - Use gguf-py to load tensor metadata and shapes
  - Extract attention weight matrices (Q, K, V, O) per layer per head
  - Extract MLP weight matrices per layer
  - For Qwen3-4B: 36 layers, likely 32 heads per layer = 1,152 attention heads + 36 MLP blocks
  - For Qwen3-14B: more layers/heads, same extraction process
  - Output: raw tensor data indexed by layer/head/component

Step 2: Activation probing
  - Build a probe dataset: 200-500 short prompts covering distinct capability categories
    Categories to probe:
      arithmetic, logical_deduction, instruction_following,
      code_generation, narrative_continuation, factual_recall,
      causal_reasoning, contradiction_detection, style_transfer,
      summarization, translation
  - For each prompt, record which heads activate above baseline
  - Cluster heads by activation pattern across the probe dataset
  - This is CPU-feasible: you're doing forward passes through the model
    and recording intermediate activations, not training anything
  - For Qwen3-14B (too large to run): mine the tensor structure statically
    (weight norms, attention pattern analysis) without forward passes

Step 3: Capability classification
  - For each head cluster: what probe categories triggered it?
  - If a cluster activates for exactly one category → clean capability → high-confidence node
  - If a cluster activates for 2-3 related categories → fuzzy capability → polysemantic node
  - If a cluster activates for 4+ unrelated categories → opaque → log but don't import
  - Start rule-based: "heads that activate on arithmetic prompts but not narrative → reasoning node"
  - Optionally use dolphin-llama3 via Ollama to help label: feed it the activation
    patterns and ask it to name the capability

Step 4: Node writer
  - For each classified capability, write a node in the existing schema format
  - Set all provenance fields
  - Set trust_layer based on extraction confidence:
    clean → stable_core, fuzzy → interpretive_maps, opaque → review_only
  - Write to nodes.jsonl alongside existing human-authored nodes
```

**Hardware reality check:**
- Qwen3-4B (2.33 GB): Can run forward passes for probing on CPU. Slow (~1-2 prompts/second) but feasible for a 500-prompt probe dataset. Estimate: 5-10 minutes for full probing pass.
- Qwen3-14B (8.38 GB): Cannot run forward passes on 13.9 GB RAM. Can still extract tensor metadata and do static analysis (weight norms, sparsity patterns). Full probing would require offloading or a cloud GPU session.
- All tensor reading via gguf-py is CPU-only and memory-mappable. No GPU needed for extraction.

**Deliverables:**
- `src/mining/gguf_reader.py` — tensor extraction from GGUF files
- `src/mining/probe_dataset.py` — probe prompt generation covering all capability categories
- `src/mining/activation_probe.py` — forward pass + intermediate activation recording
- `src/mining/capability_classifier.py` — clustering heads by activation patterns + labeling
- `src/mining/node_writer.py` — schema-compliant node output with full provenance
- `data/mined_nodes/` — the actual extracted capability nodes
- `data/mining_logs/` — full extraction logs including opaque heads that were not imported

**Depends on:** 13a (provenance schema must exist before nodes are written).

**FAILURE GATE 1** — see Section 17.

#### 13c. Embedding-Based Semantic Retrieval
**What:** Replace lexical overlap in `index_semantic.py` with embedding-based similarity.

**Implementation:**
- Install `sentence-transformers` locally (CPU-only, works fine)
- Use `all-MiniLM-L6-v2` (80MB, fast on CPU) or `nomic-embed-text` via Ollama
- On node ingest: compute embedding vector, store alongside node in JSONL
- On query: compute query embedding, cosine similarity against all node embeddings, return top-k
- Score fusion (`score_fusion.py`) already combines multiple scores — embedding similarity replaces the lexical score, everything else stays the same

This is the biggest immediate quality improvement for the least architectural risk. Every downstream component works better when "reasoning" and "inference" are recognized as semantically close.

**Deliverables:**
- Updated `src/memory/index_semantic.py`
- Embedding cache for all existing nodes
- Benchmark showing retrieval quality improvement over lexical baseline

**Depends on:** Nothing. Can run in parallel with 13a and 13b.

#### 13d. Strong Model Construction Pass — Semantic Edge Classification
**What:** Use Opus/GPT-5.5 to classify semantic edges between node pairs.

**The O(n²) problem:** If you have 1,000 nodes, classifying all pairs is 499,500 API calls. This doesn't scale naively. Use a smart sampling strategy:

```
Tier 1 — Classify pairs that share structural edges (same_source, shared_tag,
         shared_project, shared_link). These already have some relationship;
         the strong model names what kind. This is O(existing_edges), not O(n²).
         Likely hundreds, not hundreds of thousands.

Tier 2 — Classify pairs with high embedding similarity (top-k nearest neighbors
         per node, k=10-20). If two nodes are semantically close, the relationship
         between them matters. This is O(n * k), manageable.

Tier 3 — Classify cross-domain pairs that share no structural or semantic link
         but might have meaningful relationships (causal, contradicts). Use the
         strong model to identify these by reading node summaries in batch:
         "Here are 50 nodes. Which pairs have causal, contradictory, or
         prerequisite relationships?" This is O(n / batch_size) API calls.

Skip — Pairs with no structural link, low embedding similarity, and different
       domains. If neither structure nor semantics connects them, they probably
       don't have a meaningful edge. Don't pay to classify nothing.
```

**Prompt template for edge classification:**
```
You are classifying the relationship between two knowledge nodes.

Node A:
  ID: {id_a}
  Summary: {summary_a}
  Domain: {domain_a}
  Trust: {trust_a}

Node B:
  ID: {id_b}
  Summary: {summary_b}
  Domain: {domain_b}
  Trust: {trust_b}

Classify their relationship. Choose exactly one:
  causal — A causes or leads to B (or B causes A; specify direction)
  contradicts — A and B make incompatible claims
  prerequisite_of — understanding A is required to understand B (or vice versa)
  stylistically_similar — A and B share voice, register, or expressive quality
  refines — B is a more specific or updated version of A
  exemplifies — B is a concrete example of the general claim in A
  unrelated — no meaningful semantic relationship

Also provide:
  weight: 0.0 to 1.0 (strength of relationship)
  direction: A→B, B→A, or bidirectional
  confidence: 0.0 to 1.0 (how confident are you in this classification)
  reasoning: one sentence explaining why

Respond in JSON only. No preamble.
```

**Three-layer validation on construction pass outputs:**

**Layer 1 — Automated consistency checks (run after the full pass):**
- If A `contradicts` B, and B `prerequisite_of` C, flag for review (how can A contradict something that C requires?)
- If A `causal` B with weight 0.9, and B `causal` A with weight 0.8, flag for review (circular causation at high confidence is suspicious)
- If an edge has `confidence < 0.5`, route to review queue, don't commit to main graph

**Layer 2 — Second-model adversarial pass (for flagged edges):**
- Send to a different strong model (if Opus for construction, use GPT-5.5 for review, or vice versa)
- "Do you agree with this classification? If not, what would you classify it as?"
- Disagreement → human review queue

**Layer 3 — Human spot-check:**
- Review a random 5-10% sample of edges against a rubric:
  - Does this edge type make sense when you read both nodes?
  - Is the weight reasonable?
  - Would changing this edge change the system's behavior in a way you'd predict?

**Deliverables:**
- `src/construction/edge_classifier.py` — strong model API caller with batch logic
- `src/construction/sampling_strategy.py` — implements Tier 1/2/3 pair selection
- `src/construction/validation.py` — automated consistency checks + review queue management
- `data/edges_semantic.jsonl` — the classified semantic edges
- `data/construction_logs/` — full API call logs with model responses
- `data/review_queue.jsonl` — flagged edges for human review

**Depends on:** 13c (embedding similarity needed for Tier 2 sampling). Can start Tier 1 before 13c is done.

**Cost estimate:** Tier 1 + Tier 2 with 500 nodes and k=10 nearest neighbors: ~5,500 classifications. At ~200 tokens per call using Opus: ~$17 in API costs. Very manageable.

---

### 14. Phase 2: Inspectable Routing — Level 1

**Goal:** The front matter classifier stops routing to a monolithic backend and starts selecting a subgraph. The backend still generates, but the selection is graph-native, multi-axis, and fully logged.

**Duration estimate:** 2-3 weeks after Phase 1 is solid.

**Answers sub-question 3:** Can multi-axis constraint filtering produce demonstrably better subgraph selection than flat semantic retrieval?

**This is the first time the graph's multi-axis structure does real work at inference time.**

#### 14a. Query-as-Node Implementation
When a query arrives, the front matter classifier produces typed axes. Instead of using those axes to select a backend and retrieval profile, embed the classified query as a temporary node in the graph.

```python
query_node = {
    "id": f"query_{uuid}",
    "node_type": "query",
    "trust_layer": None,  # queries don't have trust
    "content": raw_query_text,
    "summary": classified_intent,
    "domain": classified_domain,
    "reasoning_mode": classified_reasoning_mode,
    "stakes": classified_stakes,
    "voice": classified_voice,
    "embedding": query_embedding_vector,
    "classifier_confidence": confidence_score,
    "temporary": True  # removed after response is generated
}
```

The query node doesn't persist — it exists for the duration of traversal and is removed after the response is generated. But while it exists, it is a first-class node that the traversal algorithm treats identically to any other node.

#### 14b. Multi-Axis Constraint Traversal Algorithm

This is the full traversal algorithm specification. Implement exactly this.

```
Algorithm: ConstrainedSubgraphActivation

Input: query_node (typed), graph (nodes + edges), config (max_depth, min_activation, decay_factor)
Output: activated_subgraph (ordered list of nodes with scores), traversal_log

0. UNDERSPECIFICATION CHECK
   - Read query_node.classifier_confidence
   - If confidence >= 0.6: proceed normally with all axis constraints active
   - If confidence >= 0.4 and < 0.6: PARTIAL CONSTRAINT MODE
     Keep domain constraint (most reliable axis even at low confidence)
     Relax reasoning_mode: boost matching nodes but do not exclude non-matching
     Relax voice: ignore voice constraint entirely
     Widen seed selection: k = k * 1.5 (round up)
     Raise min_activation threshold to 0.25 (compensate for wider net by requiring stronger hits)
     Log: traversal_log.underspecification = "partial_constraint"
   - If confidence < 0.4: SEMANTIC-ONLY MODE
     Drop all axis constraints — rely on embedding similarity alone
     Widen seed selection: k = k * 2
     Raise min_activation threshold to 0.35 (aggressive filtering on a wide net)
     Reduce max_depth to 2 (don't follow edges far from uncertain starting points)
     Log: traversal_log.underspecification = "semantic_only"
   - In all low-confidence cases: log the raw classifier output so the
     failure mode is diagnosable after the fact

1. SEED SELECTION
   - Compute embedding similarity between query_node.embedding and all graph node embeddings
   - Filter by axis constraints:
     If query.reasoning_mode is set → exclude nodes with incompatible reasoning_mode
     If query.domain is set → boost nodes in same domain (+0.3), penalize cross-domain (-0.2)
     If query.stakes == "high" → require trust_layer >= interpretive_maps (exclude episodic_events, review_only)
     If query.stakes == "critical" → require trust_layer == stable_core
     If query.voice is set → boost nodes with matching voice_score (+0.2)
   - Select top-k seeds (k=10-20) after filtering and boosting

2. EDGE TRAVERSAL
   For each seed node, follow outgoing edges:
   - Weight traversal by: edge_weight * edge_type_relevance[query.reasoning_mode][edge.type]
   - Decay activation by depth: activation *= decay_factor ^ depth (start with decay_factor=0.7)
   - Stop at max_depth (start with max_depth=3; tune based on eval results)
   - At each traversed node: apply same axis filters as seed selection
   - If a traversed node was already activated by a different seed, take the higher activation score

3. CONTRADICTION DETECTION
   For every pair of activated nodes:
   - Check if a `contradicts` edge exists between them
   - If yes: apply resolution policy (stakes-gated — see 14c below)
   - Log the contradiction and resolution in traversal_log

4. SUBGRAPH ASSEMBLY
   - Rank all activated nodes by final activation score
   - Apply min_activation threshold (default 0.15; Step 0 overrides this to 0.25 in partial_constraint mode and 0.35 in semantic_only mode — use whatever Step 0 set, not the default)
   - Drop nodes below threshold
   - Order by: activation score descending, then by edge distance from query node
   - This ordered list is the activated subgraph

5. LOGGING
   - Write complete traversal_log per schema in Section 12
   - Every traversal gets logged. No exceptions.
```

**Edge type relevance scoring — configuration, not hardcoded:**

Store as YAML config so it can be tuned without code changes:

```yaml
edge_relevance_by_reasoning_mode:
  causal:
    causal: 1.5
    prerequisite_of: 1.3
    contradicts: 1.0
    refines: 0.8
    stylistically_similar: 0.3
    exemplifies: 1.1
  narrative:
    stylistically_similar: 1.5
    exemplifies: 1.3
    causal: 0.7
    contradicts: 0.5
    prerequisite_of: 0.6
    refines: 0.8
  audit:
    contradicts: 2.0
    causal: 1.3
    prerequisite_of: 1.2
    refines: 1.0
    exemplifies: 0.8
    stylistically_similar: 0.2
  analytical:
    causal: 1.4
    prerequisite_of: 1.4
    contradicts: 1.2
    refines: 1.1
    exemplifies: 1.0
    stylistically_similar: 0.4
  creative:
    stylistically_similar: 1.6
    exemplifies: 1.4
    causal: 0.5
    contradicts: 0.3
    prerequisite_of: 0.4
    refines: 0.7
```

#### 14c. Contradiction Handling Policy

**Policy: Stakes-gated resolution.**

```python
def resolve_contradiction(node_a, node_b, query_stakes, traversal_log):
    if query_stakes in ["high", "critical"]:
        # Surface the contradiction — include both nodes in subgraph
        # Mark them as contradicting in the traversal log
        # The response assembler will present both perspectives
        traversal_log.add_contradiction(node_a, node_b, resolution="surfaced")
        return [node_a, node_b]  # both stay in activated subgraph
    else:
        # Trust hierarchy — higher trust wins silently
        trust_order = ["stable_core", "interpretive_maps", "episodic_events", "review_only"]
        a_rank = trust_order.index(node_a.trust_layer)
        b_rank = trust_order.index(node_b.trust_layer)
        if a_rank <= b_rank:  # lower index = higher trust
            winner, loser = node_a, node_b
        else:
            winner, loser = node_b, node_a
        traversal_log.add_contradiction(
            node_a, node_b,
            resolution="trust_hierarchy",
            winner=winner.id
        )
        return [winner]  # loser is deactivated
```

Rationale: Low-stakes queries get a clean answer without surfacing internal conflicts. High-stakes queries get the full picture — the user sees that two sources disagree and can make their own judgment. The front matter classifier already produces a stakes classification, so this policy costs nothing to implement.

#### 14d. Response Assembly (Level 1 — Structured Concatenation)

At Level 1, the activated subgraph is still sent to the backend as context. But the assembly is structured, not naive concatenation.

```
Prompt template for backend:
---
The following context nodes were activated for this query, in order of relevance.
Each node has a type, domain, and trust level. Use them accordingly.

[Node 1: {node_type}, domain={domain}, trust={trust_layer}, activation={score}]
{content}

[Node 2: {node_type}, domain={domain}, trust={trust_layer}, activation={score}]
{content}

[CONTRADICTION DETECTED between Node 3 and Node 5]
Node 3 ({trust_layer}) claims: {summary}
Node 5 ({trust_layer}) claims: {summary}
These nodes make incompatible claims. Present both perspectives.

Query: {original query text}
Reasoning mode: {classified reasoning_mode}
Stakes: {classified stakes}
Voice: {classified voice}
---
```

This is still technically RAG. But the retrieval is multi-axis, the contradictions are surfaced, the traversal is logged, and the behavior changes predictably when nodes change. That's Level 1, and it's worth building.

#### 14e. Evaluation Gate
Run the full evaluation suite from Section 11:
- Retrieval quality: does the right subgraph activate?
- Routing determinism: do different axis constraints produce different subgraphs?
- Inspectability: can you read the traversal log and understand the decision?
- Contradiction handling: are contradictions detected and resolved correctly?
- Response quality: is Level 1 output better than Level 0 (flat retrieval)?
- Behavioral predictability: does modifying a node change behavior predictably?

**FAILURE GATE 2** — see Section 17.

---

### 15. Phase 3: Constrained Generation — Level 2

**Goal:** The backend doesn't just receive the subgraph as context — the graph imposes structural constraints on generation.

**Duration estimate:** 2-4 weeks after Phase 2 is stable.

#### 15a. What Constraints Mean
At Level 2, the graph tells the backend not just *what* to use but *how* to use it:

- **Ordering constraints:** "Address node A before node B because A is `prerequisite_of` B"
- **Inclusion constraints:** "Node C must appear in the response because it was activated above threshold"
- **Exclusion constraints:** "Node D was activated but contradicts the trust hierarchy winner; do not use it unless stakes are high"
- **Voice constraints:** "The query requested audit voice; do not adopt narrative register even if narrative nodes were activated"
- **Citation constraints:** "If using content from a mined capability node, name the provenance"

#### 15b. Constraint Compiler
A new component between the traversal engine and the backend. Takes the activated subgraph + traversal log and produces a structured generation prompt with explicit constraints.

```python
def compile_constraints(subgraph, traversal_log, query_node):
    constraints = []

    # Ordering from prerequisite edges
    for edge in traversal_log.edge_traversals:
        if edge.type == "prerequisite_of":
            constraints.append(
                f"ORDERING: Discuss {edge.to_node} only after establishing {edge.from_node}"
            )

    # Contradiction handling
    for contradiction in traversal_log.contradictions:
        if contradiction.resolution == "surfaced":
            constraints.append(
                f"CONTRADICTION: Present both perspectives — "
                f"{contradiction.node_a} vs {contradiction.node_b}"
            )
        elif contradiction.resolution == "trust_hierarchy":
            constraints.append(
                f"EXCLUSION: Use {contradiction.winner}'s position. "
                f"Do not present {contradiction.loser}'s claim."
            )

    # Voice constraints
    if query_node.voice:
        constraints.append(f"VOICE: Maintain {query_node.voice} register throughout.")

    # Inclusion constraints
    high_activation_nodes = [n for n in subgraph if n.activation > 0.7]
    for node in high_activation_nodes:
        constraints.append(
            f"INCLUSION: Must reference content from node {node.id} ({node.summary})"
        )

    # Provenance citation
    mined_nodes = [n for n in subgraph if n.extracted_from is not None]
    if mined_nodes:
        constraints.append(
            "CITATION: When using content from mined capability nodes, "
            "note the source model in the response."
        )

    return constraints
```

**Compiled constraint prompt template:**
```
GENERATION CONSTRAINTS (these are mandatory, not suggestions):
{numbered list of constraints from compile_constraints()}

CONTEXT NODES (in activation order):
{subgraph content as in Level 1}

Query: {original query text}

Generate a response that satisfies ALL constraints above.
```

#### 15c. What This Proves
Level 2 tests whether graph structure can meaningfully constrain language model behavior. If the constraints produce noticeably different (and better) outputs than unconstrained generation from the same context, the graph is doing real computational work — not through traversal-as-computation, but through structure-as-constraint. This is a meaningful intermediate result even if Level 3-4 never ship.

**FAILURE GATE 3** — see Section 17.

---

### 16. Phase 4: Composition Research — Level 3+

**Goal:** Begin answering the actual hard question. Can the graph compose responses without a conventional backend?

**Duration estimate:** Open-ended. This is research, not engineering.

**Answers sub-question 4:** Can an activated subgraph compose into a coherent response without a conventional language model backend?

#### 16a. The Embedding Space Question

Before composition can be designed, the internal representation must be defined. You cannot design the traversal algorithm without knowing what representation lives inside the graph. This question must be DESIGNED before Phase 3, even though implementation comes after.

**Three options:**

**Option A: Adopt an existing embedding space**
Use `nomic-embed-text` or `all-MiniLM-L6-v2` as the native representation inside the graph. Every node lives in that space. Composition operates on vectors in that space.

- Pro: Works immediately. No training needed. Embedding model is small and CPU-friendly.
- Con: Dependent on someone else's representation. The embedding space wasn't designed for composition — it was designed for similarity search. "Close in embedding space" doesn't mean "composable into a coherent response."
- Con: Can't improve the representation without swapping the embedding model, which changes the entire graph.

**Option B: Learn a custom embedding space from graph structure**
Train an embedding space where distance reflects graph relationships, not just semantic similarity. Nodes connected by strong edges should be close; nodes separated by many hops should be distant.

- Pro: Truly native to the graph. The representation encodes the architecture's own structure.
- Con: Requires training, which means gradient descent — you're back to learned parameters.
- Con: Small graph (hundreds to low thousands of nodes) may not have enough structure to learn a meaningful space.

**Option C: Multi-space approach**
Each axis gets its own embedding space. Semantic similarity, voice similarity, temporal proximity, trust distance — each is a separate low-dimensional space. Composition operates across all spaces simultaneously.

- Pro: Matches the multi-axis architecture.
- Con: Composition across multiple spaces is itself an unsolved research problem.

**Recommendation:** Start with Option A for Phase 1-3. Design Option B in parallel for Phase 4. Don't attempt Option C until A or B has proved the concept.

#### 16b. Composition Operator Candidates

The composition operator turns an activated subgraph into a response. Four candidates, ranked by architectural honesty:

**Candidate 1: Template-based composition**
Node content is slotted into response templates based on node type and query type. A `causal` reasoning query with three activated nodes produces: "[Node A context]. This leads to [Node B context], which results in [Node C context]."

- Expressiveness: Very low. Sophisticated string interpolation.
- Inspectability: Perfect. You can read exactly what happened.
- When to use: As the Level 3 baseline prototype. Proves that subgraph ordering matters. Establishes comparison point for more sophisticated operators.

**Candidate 2: Attention over subgraph**
The activated subgraph's node embeddings are treated as a sequence. A small attention mechanism (trained or hand-designed) computes attention weights over the nodes and produces a weighted combination in embedding space, which is then decoded.

- Expressiveness: Medium. Can learn to emphasize relevant nodes and suppress irrelevant ones.
- Inspectability: Medium. Attention weights are readable but the combination in embedding space is not.
- Training signal: The strong model's responses to the same queries provide the target.
- Hardware feasibility: A small attention layer (single head, node-count-sized) is trivially CPU-trainable.

**Candidate 3: Iterative refinement (RECOMMENDED)**
Start with the highest-activation node's content as the initial response. For each subsequent activated node in order, refine the response by integrating that node's content. Each refinement step is a constrained edit: add what the new node contributes, don't lose what's already there.

- Expressiveness: Medium-high. Can produce coherent multi-source responses.
- Inspectability: High. Each refinement step is logged and readable.
- The refinement operator itself needs a small model — but it's a much smaller task than full generation. Essentially an "integrate this paragraph into this draft" operator.
- This is the most promising candidate because each refinement step is independently evaluable.

**Stopping criterion for Candidate 3 (must be designed before prototyping):**

Iterative refinement needs to know when to stop integrating nodes. An unspecified stopping criterion means the system either stops too early (misses relevant content) or integrates too many nodes (dilutes coherence). Four options:

1. **Fixed node count** — stop after integrating N nodes. Blunt. Ignores that some queries need 3 nodes and others need 12. Useful only as a prototype ceiling, not a real policy.

2. **Activation threshold (RECOMMENDED START)** — stop when the next node's marginal activation score drops below a threshold relative to the seed node. E.g., stop when `next_node.activation < 0.3 * seed_node.activation`. Heuristic, tunable, doesn't require a model.

3. **Diminishing return detection** — after each integration step, measure how much the response changed (embedding distance between pre- and post-integration drafts). When the delta drops below a threshold, the next node isn't contributing enough to justify inclusion. Requires embedding the draft at each step, which is cheap.

4. **Learned stopping criterion** — train a small binary classifier: given (current_draft, next_node), should integration continue? Training signal comes from the strong model: during training signal generation (16c), have Opus mark which nodes in the subgraph actually contributed to its response and which were noise. This produces (draft, node, should_include) labels. Adds a small model but it's a classifier, not a generator — tiny and fast.

Start with option 2 for the prototype. Collect data during prototyping to train option 4 later if the heuristic proves too blunt. Option 3 is a good middle ground if 2 is insufficient and 4 isn't ready yet.

**Candidate 4: Learned generation from graph state**
Train a small model whose input is the graph state (activated subgraph as structured input) and whose output is tokens. Trained end-to-end on (subgraph, response) pairs where responses come from the strong model.

- Expressiveness: High. Full generation capability.
- Inspectability: Low. The model is a small black box.
- This is essentially distillation with extra steps. It's the furthest from the architecture's stated goals.
- When to use: Only if candidates 1-3 hit a quality ceiling and Level 4 matters enough to justify the tradeoff.

**Build order:** Prototype Candidate 1 first (baseline). Then Candidate 3 (iterative refinement). Candidate 3 is the most architecturally honest — it keeps each composition step inspectable and bounded.

#### 16c. Training Signal Generation

Where does the learning signal come from for any learned composition operator?

The strong model provides it:

1. Run 500-1000 test queries through the Level 2 system
2. Record the activated subgraph for each query
3. Send each (query, activated_subgraph) pair to Opus with the prompt: "Given this query and these activated context nodes, write the ideal response that uses the nodes coherently."
4. Opus generates the "ideal" response given that subgraph
5. These (subgraph, ideal_response) pairs are the training data for the composition operator
6. Additionally: have Opus mark which nodes actually contributed to its response and which were noise — this produces stopping criterion training labels

The strong model's role expands: it's not just the construction tool for the graph, it's also the teacher for the composition operator. Its judgment gets crystallized twice — once into graph structure, once into composition behavior.

**Cost estimate:** 1,000 Opus calls at ~500 tokens input + ~300 tokens output each: ~$24.

**FAILURE GATE 4** — see Section 17.

---

### 17. Failure Conditions — When to Stop and Redesign

These are the most important structural decisions in the entire document. They are the conditions under which you stop building forward and redesign, because building on a wrong assumption produces a system that is confidently wrong in ways that are expensive to diagnose later. Most projects fail because they don't define failure conditions early enough.

Each gate is a decision point, not a progress report. Passing means the assumption held and the next phase is justified. Failing means the assumption broke and the next action is redesign, not persistence.

**Gate 1: GGUF Mining Viability** *(end of Phase 1, step 13b)*

After mining Qwen3-4B, manually inspect 20 mined nodes.

- **Pass:** At least 12 of 20 nodes are clearly nameable — you can read the node and say "yes, this represents [specific capability] and I understand why." Proceed with mining additional models.
- **Fail:** Fewer than 8 of 20 are nameable. The capability classifier needs revision. Do not mine more models until the classifier improves. If revision doesn't help, the polysemantic reality of transformer heads may be harder to decompose than the architecture assumes — scope the "named capabilities from GGUF mining" claim down to the clean-capability tier only.
- **What's at stake:** The entire GGUF mining value proposition. If mining mostly produces opaque nodes, the graph's seed capabilities come only from human-authored nodes and strong model bootstrapping, not from existing model weights. The architecture still works but loses its most novel component.

**Gate 2: Multi-Axis Differentiation** *(end of Phase 2, step 14e)*

Run the routing determinism eval (Section 11b). Do identical queries with different axis constraints produce meaningfully different subgraphs?

- **Pass:** Axis-varied query pairs activate subgraphs that differ by at least 40% of their nodes. The axes are doing real filtering work.
- **Fail:** Axis-varied query pairs activate nearly identical subgraphs (less than 20% difference). The axis system is decorative — the semantic similarity signal dominates and the typed constraints aren't constraining anything.
- **What's at stake:** The entire multi-axis architecture claim. If axes don't differentiate, the system is just embedding-based retrieval with extra metadata that doesn't affect behavior. Redesign the constraint filtering algorithm, or redesign the axes themselves, before Phase 3. Do not proceed to constrained generation if the constraints don't constrain.

**Gate 3: Constrained Generation Value** *(end of Phase 3, step 15c)*

Side-by-side comparison: does the constraint compiler (Level 2) produce noticeably better responses than unconstrained context injection (Level 1)?

- **Pass:** In blind evaluation (strong model as judge, or human evaluation), Level 2 responses are preferred on coherence, ordering, and contradiction handling in at least 60% of test cases.
- **Fail:** Level 2 responses are not consistently preferred. The constraints are either too weak (backend ignores them) or too rigid (they make responses worse).
- **What's at stake:** Whether the graph's structure can meaningfully shape language model output. If not, Level 2 is not a real milestone and the path from Level 1 to Level 3 needs a different intermediate step.

**Gate 4: Composition Operator Viability** *(early Phase 4, after first Candidate 3 prototype)*

The iterative refinement operator produces a 50-response test set.

- **Pass:** At least 35 of 50 responses are coherent (readable, logically structured) AND every claim in the response can be traced to a specific node in the subgraph.
- **Fail:** Responses are incoherent, OR traceability breaks (content appears that isn't in any activated node, or node content is distorted beyond recognition during integration).
- **What's at stake:** Whether Level 3 is achievable at all. If iterative refinement can't compose coherent responses from subgraphs, the composition problem is harder than expected. Options: try Candidate 2 (attention over subgraph), accept that the project tops out at Level 2 (still valuable), or redefine what Level 3 means.

---

### 18. Dependency Map

```
Phase 1 (Graph Foundation)
├── 13a. Provenance schema ─────────────────┐
├── 13b. GGUF mining pipeline ◄─────────────┤ (needs schema first)
│   └── GATE 1: inspect 20 nodes ───────────┤
├── 13c. Embedding retrieval ───────────────┤ (parallel, no dependency)
└── 13d. Strong model construction pass ◄───┤ (needs embeddings for Tier 2)
                                            │
Phase 2 (Inspectable Routing — Level 1)     │
├── 14a. Query-as-node ◄───────────────────┤ (needs schema + embeddings)
├── 14b. Constraint traversal ◄─────────────┤ (needs edges from 13d)
├── 14c. Contradiction handling ◄───────────┤ (needs 14b traversal)
├── 14d. Response assembly ◄────────────────┤ (needs 14b + 14c)
└── 14e. Evaluation gate ◄─────────────────┤ (needs all of Phase 2)
    └── GATE 2: axis differentiation ───────┤
                                            │
Phase 3 (Constrained Generation — Level 2)  │
├── 15a-15b. Constraint compiler ◄──────────┤ (needs Phase 2 stable)
└── 15c. Evaluation ◄──────────────────────┤
    └── GATE 3: constrained gen value ──────┤
                                            │
Phase 4 (Composition Research — Level 3+)   │
├── 16a. Embedding space design ◄───────────┤ (design during Phase 2,
│                                            │  implement after Phase 3)
├── 16b. Composition operator prototypes ◄──┤ (needs 16a)
│   └── GATE 4: composition viability ──────┤
├── 16c. Training signal generation ◄───────┤ (needs Phase 2 running
│                                            │  to produce subgraphs)
└── Full evaluation ◄──────────────────────┘
```

---

### 19. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| GGUF mining produces mostly opaque/unnameable capabilities | Medium | High — undermines "named capabilities" claim | Start with Qwen3-4B (smaller, more interpretable). Set minimum confidence threshold. Don't import what you can't name. Gate 1 catches this. |
| Strong model makes systematic classification errors that propagate through graph | Medium | High — load-bearing wrong edges | Three-layer validation (automated consistency, adversarial second model, human spot-check). Low-confidence edges go to review queue. |
| Multi-axis constraint filtering doesn't produce meaningfully different subgraphs from flat retrieval | Low-Medium | Critical — means axis system is decorative | Gate 2 catches this. If axes don't differentiate, redesign axes before proceeding. |
| Composition operator can't produce coherent responses from subgraph alone | Medium-High | Medium — Levels 1-2 still valuable | Design Levels 1-2 as valuable endpoints, not just stepping stones. Project succeeds at Level 2 even if Level 4 is unreachable. Gate 4 catches this. |
| Hardware limitations slow iteration speed to stalling | Medium | Medium | GGUF mining and embedding computation are batch/offline. Strong model construction is API-based. Graph traversal is CPU-native. Only Ollama-assisted labeling is bottlenecked by local compute. |
| Graph grows large enough that traversal becomes slow | Low (near-term) | Low (near-term) | JSONL + in-memory graph for hundreds to low thousands of nodes is fast. If scale requires it, move to NetworkX or a graph DB later. Don't over-engineer storage now. |

---

### 20. Hardware Constraints

**Machine:** AMD Radeon Vega 11 (integrated GPU, 2 GB VRAM), 13.9 GB RAM, Windows.

- No CUDA. All inference is CPU or ROCm (Vega 11 has limited ROCm support on Windows).
- Embedding models must be small (`nomic-embed-text` at 274M params is fine; `all-MiniLM-L6-v2` at 80MB is better for speed).
- GGUF mining can be done CPU-only; it's offline/batch work.
- Graph traversal is CPU-native — no GPU needed.
- The existing Ollama setup (`dolphin-llama3`) is the available local inference backend for LLM-assisted steps (GGUF capability labeling, edge classification fallback).
- Strong model construction pass uses cloud API (Opus, GPT-5.5) — not constrained by local hardware.

**Available GGUF files on disk:**
- `D:\gguf-models\Qwen3-14B-Q4_K_M.gguf` (8.38 GB) — too large for this machine to run inference, but can be mined offline for tensor metadata and static analysis
- `D:\gguf-models\Qwen3-4B-Instruct-2507-Q4_K_M.gguf` (2.33 GB) — runnable via CPU offload for activation probing
- Ollama: `dolphin-llama3:latest` (4.7 GB, 8B Q4_0) — currently running, available as local inference backend

**Repository location:** `D:\craig-CODA`

---

### 21. What Success Looks Like at Each Level

**Level 0 → Level 1:** You can read a traversal log for any query and understand exactly why those nodes were selected, in what order, through which edges. A non-technical person can follow the log. Changing a single node or edge produces a predictable, explainable change in the output. This alone is publishable — "inspectable retrieval-augmented generation with multi-axis constraint filtering."

**Level 1 → Level 2:** The constraint compiler produces noticeably better responses than unconstrained generation from the same context. Specifically: prerequisite ordering makes explanations more coherent, contradiction surfacing makes high-stakes responses more trustworthy, and voice constraints make the register more consistent. Side-by-side comparisons show the difference.

**Level 2 → Level 3:** The iterative refinement operator (Candidate 3) produces responses that are (a) coherent, (b) traceable to specific nodes, and (c) not significantly worse than the backend generating from the same context. "Not significantly worse" is the bar — the value is inspectability and predictability, not raw quality.

**Level 3 → Level 4:** The graph produces responses without any conventional backend. This is the north star. It may or may not be achievable. If it is, it's a genuine new kind of model. If it isn't, Levels 1-3 are still real and valuable.

---

### 22. Immediate First Actions

These are the literal first things to do, in order, before Phase 1 engineering begins:

1. **Write the evaluation test suite** (Section 11). 50 query/expected-subgraph pairs. Before any code changes. This is the most important deliverable in the entire plan because everything else is measured against it. It is also the hardest — it forces you to define what "right" looks like before the system exists. Every place where you hesitate is a place where the architecture has an unresolved design question. The eval suite doesn't just measure the system; writing it finishes the design.

2. **Update node schema with provenance fields** (Section 8a / Step 13a). One file change. Deploy immediately so all subsequent node writers include provenance from the start.

3. **Install gguf-py and run a tensor inventory on Qwen3-4B.** Don't build the full pipeline — just confirm you can read the tensor shapes, count the heads, and extract weight matrices. This de-risks the mining pipeline before committing to it.

4. **Install sentence-transformers and embed 10 existing nodes.** Confirm the embedding quality is good enough to replace lexical overlap. This de-risks the retrieval upgrade.

5. **Draft the contradiction handling policy document.** One page. Pick stakes-gated (Section 14c). Write the specific rules. This design decision must be settled before Phase 2 coding begins.

After these five, the foundation is solid and Phase 1 engineering begins.

---

### 23. Final Framing

This architecture is not trying to compete with transformers on raw language generation quality. A 4B parameter transformer will generate more fluent text than any graph traversal system for the foreseeable future.

What this architecture competes on is everything transformers are bad at:
- **Inspectability** — why did it say that? Read the traversal log.
- **Predictability** — what happens if I change this piece of knowledge? Change the node and re-run.
- **Explicit contradiction handling** — it knows when it disagrees with itself, and it has a policy for what to do about it.
- **Provenance** — where did this capability come from? Read the node's `extracted_from` field.
- **Structural modification** — add a node, change behavior in a bounded, predictable way. Remove a node, the behavior change is equally bounded and predictable.

The transformers are black boxes that produce beautiful text for reasons nobody can fully explain. This is a transparent system that produces adequate text for reasons you can read in a log file. The bet is that the second property is more valuable than the first — or at least, valuable enough to build.

Level 1-2 makes that bet payable immediately. Level 3-4 is the long play.

**The graph is a constitution.** You can read it, edit it, and predict what changes when you edit it. A strong model writes it; the traversal engine enforces it. That's the architecture. Everything else is implementation.
