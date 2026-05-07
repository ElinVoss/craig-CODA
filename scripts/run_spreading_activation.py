"""
Manual inspection harness for spreading activation.

Usage:
    python scripts/run_spreading_activation.py "your query here"
    python scripts/run_spreading_activation.py "your query" --profile technical --top-k 10 --ticks 8

Prints a side-by-side comparison:
  - Flat scorer top-K (current retrieve_topk output)
  - Spreading activation top-K (field model output)
  - Neighborhood structure for the top activated node
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.memory.index_graph import build_adjacency
from src.memory.memory_store import load_memory_graph
from src.memory.query_classifier import classify_query_profile
from src.memory.retrieve_topk import retrieve_nodes
from src.memory.score_fusion import fuse_scores, load_query_profiles, trust_adjustment
from src.memory.spreading_activation import build_propagation_adjacency, run_spreading_activation
from src.memory.index_graph import graph_weight
from src.memory.index_phase import phase_match
from src.memory.index_reinforcement import reinforcement_weight
from src.memory.index_semantic import semantic_similarity
from src.memory.index_temporal import temporal_relevance
from src.memory.index_voice import voice_similarity


def flat_seed_scores(query: str, profile: str, nodes, edges) -> dict[str, float]:
    """Compute flat score_fusion scores for all permeable nodes — these become tick-0 charge."""
    adjacency = build_adjacency(edges)
    profiles = load_query_profiles()["profiles"]
    scores: dict[str, float] = {}
    for node in nodes:
        allowed, trust_multiplier = trust_adjustment(node, profile)
        if not allowed:
            continue
        semantic = semantic_similarity(query, node)
        temporal = temporal_relevance(node)
        phase = phase_match(query, node)
        graph = graph_weight(query, node, adjacency)
        reinforcement = reinforcement_weight(node)
        voice = voice_similarity(query, node, profile)
        total = fuse_scores(
            retrieval_profile=profile,
            semantic=semantic,
            temporal=temporal,
            phase=phase,
            project=node.project_relevance,
            graph=graph,
            voice=voice,
            reinforcement=reinforcement,
            confidence=node.confidence,
            trust_multiplier=trust_multiplier,
        )
        scores[node.id] = total
    return scores


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect spreading activation vs flat retrieval")
    parser.add_argument("query", help="Query string to test")
    parser.add_argument("--profile", default=None, help="Retrieval profile override")
    parser.add_argument("--top-k", type=int, default=10, help="Number of results to show")
    parser.add_argument("--ticks", type=int, default=8, help="Max activation ticks")
    parser.add_argument("--decay", type=float, default=0.6, help="Per-tick decay factor")
    parser.add_argument("--threshold", type=float, default=0.3, help="Firing threshold")
    parser.add_argument("--fan-out", type=int, default=5, help="Max edges per firing node per tick")
    parser.add_argument("--propagation-fraction", type=float, default=0.4, help="Outward energy fraction")
    args = parser.parse_args()

    print(f"\nLoading vault graph...")
    nodes, edges = load_memory_graph()
    nodes_by_id = {n.id: n for n in nodes}
    profile = args.profile or classify_query_profile(args.query)

    print(f"Query   : {args.query!r}")
    print(f"Profile : {profile}")
    print(f"Nodes   : {len(nodes):,}   Edges: {len(edges):,}")

    # --- Flat scorer (current system) ---
    print(f"\nComputing flat seed scores...")
    seed_scores = flat_seed_scores(args.query, profile, nodes, edges)

    flat_top = sorted(seed_scores.items(), key=lambda x: -x[1])[: args.top_k]

    # --- Spreading activation ---
    prop_adjacency = build_propagation_adjacency(edges)
    eligible_edges = sum(1 for e in edges if e.propagation_eligible)
    print(f"Propagation-eligible edges: {eligible_edges:,} of {len(edges):,}")
    print(f"Running spreading activation (max_ticks={args.ticks}, decay={args.decay}, threshold={args.threshold})...")

    final_potential = run_spreading_activation(
        seed_scores=seed_scores,
        adjacency=prop_adjacency,
        nodes_by_id=nodes_by_id,
        max_ticks=args.ticks,
        decay=args.decay,
        threshold=args.threshold,
        fan_out=args.fan_out,
        propagation_fraction=args.propagation_fraction,
    )

    activated_top = sorted(final_potential.items(), key=lambda x: -x[1])[: args.top_k]

    # --- Side-by-side output ---
    W = 62
    print(f"\n{'='*W}")
    print(f"  FLAT SCORER (top {args.top_k})          |  SPREADING ACTIVATION (top {args.top_k})")
    print(f"{'='*W}")

    for i in range(args.top_k):
        flat_row = ""
        if i < len(flat_top):
            nid, score = flat_top[i]
            node = nodes_by_id.get(nid)
            label = (node.summary or node.content)[:28].replace("\n", " ") if node else nid[:28]
            flat_row = f"{i+1:2}. {score:.4f}  {label:<28}"
        else:
            flat_row = " " * 42

        act_row = ""
        if i < len(activated_top):
            nid, score = activated_top[i]
            node = nodes_by_id.get(nid)
            label = (node.summary or node.content)[:28].replace("\n", " ") if node else nid[:28]
            act_row = f"{i+1:2}. {score:.4f}  {label:<28}"

        print(f"  {flat_row}   {act_row}")

    # --- Neighborhood of top activated node ---
    if activated_top:
        top_id, top_pot = activated_top[0]
        top_node = nodes_by_id.get(top_id)
        neighbors = prop_adjacency.get(top_id, [])
        print(f"\n{'='*W}")
        print(f"NEIGHBORHOOD of top activated node (potential={top_pot:.4f})")
        print(f"  id      : {top_id}")
        if top_node:
            print(f"  type    : {top_node.node_type}")
            print(f"  trust   : {top_node.trust_layer}")
            print(f"  summary : {(top_node.summary or top_node.content)[:80].replace(chr(10), ' ')}")
        print(f"  eligible neighbors ({len(neighbors)}):")
        for edge in sorted(neighbors, key=lambda e: -e.weight)[:10]:
            nbr_id = edge.target_id if edge.source_id == top_id else edge.source_id
            nbr = nodes_by_id.get(nbr_id)
            nbr_label = (nbr.summary or nbr.content)[:50].replace("\n", " ") if nbr else nbr_id
            nbr_pot = final_potential.get(nbr_id, 0.0)
            print(f"    w={edge.weight:.2f}  pot={nbr_pot:.4f}  [{edge.edge_type}]  {nbr_label}")
    print()


if __name__ == "__main__":
    main()
