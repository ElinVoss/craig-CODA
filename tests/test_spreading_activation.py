"""Focused tests for conservative spreading-activation retrieval.

Run:
    python tests/test_spreading_activation.py
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import src.memory.retrieve_topk as retrieve_topk_module
import src.memory.spreading_activation as spreading_module
from src.memory.build_edges import build_edges
from src.memory.node_schema import VaultEdge, VaultNode


def make_node(
    node_id: str,
    *,
    trust_layer: str = "stable_core",
    source_path: str = "exports/user_model_package/identity_core/core.md",
    source_kind: str = "runtime_bundle",
    projects: list[str] | None = None,
    tags: list[str] | None = None,
    links: list[str] | None = None,
) -> VaultNode:
    return VaultNode(
        id=node_id,
        node_type="note",
        trust_layer=trust_layer,
        content=f"content {node_id}",
        summary=f"summary {node_id}",
        source_path=source_path,
        source_kind=source_kind,
        created_at="2026-05-08T00:00:00",
        time_start=None,
        time_end=None,
        life_phase="current",
        projects=projects or [],
        tags=tags or [],
        links=links or [],
        confidence=0.8,
        project_relevance=0.5,
    )


def test_vault_edge_from_dict_infers_propagation_flag():
    same_source = VaultEdge.from_dict(
        {
            "source_id": "a",
            "target_id": "b",
            "edge_type": "same_source",
            "weight": 0.55,
            "rationale": "shared source file",
        }
    )
    shared_project = VaultEdge.from_dict(
        {
            "source_id": "a",
            "target_id": "b",
            "edge_type": "shared_project",
            "weight": 0.65,
            "rationale": "shared project",
        }
    )
    generic_tag = VaultEdge.from_dict(
        {
            "source_id": "a",
            "target_id": "b",
            "edge_type": "shared_tag",
            "weight": 0.45,
            "rationale": "shared tag: runtime",
        }
    )
    assert same_source.propagation_eligible is False
    assert shared_project.propagation_eligible is True
    assert generic_tag.propagation_eligible is False


def test_build_edges_marks_conservative_propagation_eligibility():
    left = make_node("left", source_path="a.md", projects=["craig"], tags=["warehouse_logic"])
    right = make_node("right", source_path="a.md", projects=["craig"], tags=["warehouse_logic"])
    blocked = make_node("blocked", trust_layer="interpretive_maps", source_path="b.md", projects=["craig"])

    edges = build_edges([left, right, blocked])
    by_key = {(edge.source_id, edge.target_id, edge.edge_type): edge for edge in edges}

    same_source = by_key[("left", "right", "same_source")]
    shared_project = by_key[("left", "right", "shared_project")]
    shared_tag = by_key[("left", "right", "shared_tag")]
    blocked_project = by_key[("blocked", "left", "shared_project")]

    assert same_source.propagation_eligible is False
    assert shared_project.propagation_eligible is True
    assert shared_tag.propagation_eligible is True
    assert blocked_project.propagation_eligible is False


def test_spread_activation_lifts_connected_neighbor():
    anchor = make_node("anchor", projects=["craig"])
    neighbor = make_node("neighbor", projects=["craig"])
    distractor = make_node("distractor", projects=["other"])

    candidates = [
        spreading_module.SeedCandidate(anchor, 0.9, {"semantic": 0.9, "graph": 0.0}),
        spreading_module.SeedCandidate(neighbor, 0.25, {"semantic": 0.25, "graph": 0.0}),
        spreading_module.SeedCandidate(distractor, 0.35, {"semantic": 0.35, "graph": 0.0}),
    ]
    edges = [
        VaultEdge(
            source_id="anchor",
            target_id="neighbor",
            edge_type="shared_project",
            weight=0.65,
            rationale="shared project",
            propagation_eligible=True,
        )
    ]

    original_loader = spreading_module.load_memory_config
    spreading_module.load_memory_config = lambda *_args, **_kwargs: {
        "retrieval": {
            "spreading_activation": {
                "enabled": True,
                "seed_limit": 1,
                "min_seed_score": 0.4,
                "max_hops": 1,
                "fanout_cap": 2,
                "activation_decay": 1.0,
                "min_edge_weight": 0.5,
                "min_activation": 0.1,
                "max_total_activation": 1.0,
                "edge_type_bias": {"shared_project": 1.0},
            }
        }
    }
    try:
        results = spreading_module.spread_activation(candidates, edges)
    finally:
        spreading_module.load_memory_config = original_loader

    by_id = {item.node.id: item for item in results}
    assert by_id["neighbor"].total_score > by_id["distractor"].total_score
    assert by_id["neighbor"].propagated_bonus > 0.0
    assert by_id["neighbor"].hop_distance == 1


def test_retrieve_nodes_uses_spreading_strategy():
    anchor = make_node("anchor", projects=["craig"])
    neighbor = make_node("neighbor", projects=["craig"])
    distractor = make_node("distractor", projects=["other"])
    edges = [
        VaultEdge(
            source_id="anchor",
            target_id="neighbor",
            edge_type="shared_project",
            weight=0.65,
            rationale="shared project",
            propagation_eligible=True,
        )
    ]

    originals = {
        "load_memory_config": retrieve_topk_module.load_memory_config,
        "load_memory_graph": retrieve_topk_module.load_memory_graph,
        "load_query_profiles": retrieve_topk_module.load_query_profiles,
        "trust_adjustment": retrieve_topk_module.trust_adjustment,
        "semantic_similarity": retrieve_topk_module.semantic_similarity,
        "temporal_relevance": retrieve_topk_module.temporal_relevance,
        "phase_match": retrieve_topk_module.phase_match,
        "voice_similarity": retrieve_topk_module.voice_similarity,
        "reinforcement_weight": retrieve_topk_module.reinforcement_weight,
        "fuse_scores": retrieve_topk_module.fuse_scores,
    }

    retrieve_topk_module.load_memory_config = lambda *_args, **_kwargs: {
        "retrieval": {
            "strategy": "spreading_activation",
            "max_top_k": 5,
            "spreading_activation": {
                "enabled": True,
                "seed_limit": 1,
                "min_seed_score": 0.4,
                "max_hops": 1,
                "fanout_cap": 2,
                "activation_decay": 1.0,
                "min_edge_weight": 0.5,
                "min_activation": 0.1,
                "max_total_activation": 1.0,
                "edge_type_bias": {"shared_project": 1.0},
            },
        }
    }
    retrieve_topk_module.load_memory_graph = lambda *_args, **_kwargs: ([anchor, neighbor, distractor], edges)
    retrieve_topk_module.load_query_profiles = lambda *_args, **_kwargs: {"profiles": {"technical": {"top_k": 3}}}
    retrieve_topk_module.trust_adjustment = lambda *_args, **_kwargs: (True, 1.0)
    retrieve_topk_module.semantic_similarity = lambda _query, node, config_path=None: {
        "anchor": 0.9,
        "neighbor": 0.25,
        "distractor": 0.35,
    }[node.id]
    retrieve_topk_module.temporal_relevance = lambda _node, config_path=None: 0.0
    retrieve_topk_module.phase_match = lambda _query, _node: 0.0
    retrieve_topk_module.voice_similarity = lambda _query, _node, _profile, mode=None: 0.0
    retrieve_topk_module.reinforcement_weight = lambda _node: 0.0
    retrieve_topk_module.fuse_scores = lambda **kwargs: kwargs["semantic"]

    original_spreading_loader = spreading_module.load_memory_config
    spreading_module.load_memory_config = retrieve_topk_module.load_memory_config
    try:
        results = retrieve_topk_module.retrieve_nodes("runtime query")
    finally:
        spreading_module.load_memory_config = original_spreading_loader
        for name, value in originals.items():
            setattr(retrieve_topk_module, name, value)

    assert results[0].node.id == "anchor"
    assert results[1].node.id == "neighbor"
    assert results[1].breakdown["graph"] > 0.0


if __name__ == "__main__":
    tests = [v for k, v in list(globals().items()) if k.startswith("test_")]
    passed = 0
    failed = 0
    for fn in tests:
        try:
            fn()
            print(f"  PASS  {fn.__name__}")
            passed += 1
        except Exception as exc:
            import traceback
            print(f"  FAIL  {fn.__name__}: {exc}")
            traceback.print_exc()
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
    if failed:
        sys.exit(1)
