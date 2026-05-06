# Memory

This branch owns the vault graph lane.
It is where source material becomes nodes, nodes become indexed graph state, graph state becomes retrieval, and retrieval becomes a behavioral contract.

## What Lives Here

### Extraction and normalization

- `extract_nodes.py`
- `classify_nodes.py`
- `normalize_sources.py`
- `build_edges.py`
- `node_schema.py`
- `memory_store.py`

### Indexing and retrieval

- `index_semantic.py`
- `index_temporal.py`
- `index_phase.py`
- `index_voice.py`
- `index_reinforcement.py`
- `retrieve_topk.py`
- `score_fusion.py`
- `query_classifier.py`
- `update_reinforcement.py`

### Newer graph and autonomy work

- `graph_router.py`
- `async_indexer.py`
- `gguf_mining.py`
- `consolidate_memories.py`

## Current State

- conversation transcript extraction is now a first-class path, not generic chunking
- retrieval supports both lexical fallback and embedding-backed semantic search
- trust layers are first-class and are not decorative metadata
- `graph_router.py` derives a per-turn routing contract from the retrieved subgraph:
  - response mode
  - posture
  - trust ceiling
  - blocked-layer behavior
  - edge-cluster visibility
- `async_indexer.py` writes embedding sidecars without mutating the main node file
- `gguf_mining.py` can emit heuristic capability-seed nodes from a GGUF file

## Important Reality

- this branch is not just memory lookup
- it now shapes what the runtime is allowed to say
- but it still does that by informing a model call, not by replacing the deeper computation

## Continue From Here

You are in the `memory` scope.

Read in this order:

1. `README.md`
2. `extract_nodes.py`
3. `index_semantic.py`
4. `score_fusion.py`
5. `query_classifier.py`
6. `graph_router.py`
7. `async_indexer.py`
8. `gguf_mining.py`
9. `node_schema.py`

If the user asks about schema or trust layers, also read:

- `../../configs/node_schema.yaml`
- `../../configs/memory_retrieval.yaml`
- `../../configs/memory_query_profiles.yaml`

Keep `D:\craig-CODA\LIVE_HANDOFF.md` current between meaningful actions.
