from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .index_graph import build_adjacency
from .memory_store import load_memory_config
from .node_schema import VaultEdge, VaultNode

_BLOCKED_PROPAGATION_LAYERS = {"review_only", "interpretive_maps"}


@dataclass
class SeedCandidate:
    node: VaultNode
    seed_score: float
    breakdown: dict[str, float]


@dataclass
class ActivationResult:
    node: VaultNode
    total_score: float
    activation_score: float
    propagated_bonus: float
    hop_distance: int | None
    breakdown: dict[str, float]


def _other_node_id(edge: VaultEdge, source_id: str) -> str:
    return edge.target_id if edge.source_id == source_id else edge.source_id


def edge_is_effectively_propagation_eligible(edge: VaultEdge, node_by_id: dict[str, VaultNode]) -> bool:
    if not edge.propagation_eligible:
        return False
    left = node_by_id.get(edge.source_id)
    right = node_by_id.get(edge.target_id)
    if left is None or right is None:
        return False
    if left.trust_layer in _BLOCKED_PROPAGATION_LAYERS:
        return False
    if right.trust_layer in _BLOCKED_PROPAGATION_LAYERS:
        return False
    return True


def spread_activation(
    candidates: list[SeedCandidate],
    edges: list[VaultEdge],
    config_path: str | Path | None = None,
) -> list[ActivationResult]:
    if not candidates:
        return []

    config = load_memory_config(config_path)
    settings = config["retrieval"].get("spreading_activation", {})
    if not settings.get("enabled", False):
        return [
            ActivationResult(
                node=candidate.node,
                total_score=candidate.seed_score,
                activation_score=candidate.seed_score,
                propagated_bonus=0.0,
                hop_distance=0,
                breakdown={**candidate.breakdown, "seed_score": candidate.seed_score, "activation_score": candidate.seed_score},
            )
            for candidate in sorted(candidates, key=lambda item: item.seed_score, reverse=True)
        ]

    seed_limit = int(settings.get("seed_limit", 8))
    min_seed_score = float(settings.get("min_seed_score", 0.18))
    max_hops = int(settings.get("max_hops", 2))
    fanout_cap = int(settings.get("fanout_cap", 4))
    activation_decay = float(settings.get("activation_decay", 0.72))
    min_edge_weight = float(settings.get("min_edge_weight", 0.5))
    min_activation = float(settings.get("min_activation", 0.08))
    max_total_activation = float(settings.get("max_total_activation", 1.0))
    edge_type_bias = {
        str(key): float(value)
        for key, value in settings.get("edge_type_bias", {}).items()
    }

    adjacency = build_adjacency(edges)
    candidate_by_id = {candidate.node.id: candidate for candidate in candidates}
    node_by_id = {candidate.node.id: candidate.node for candidate in candidates}
    ordered = sorted(candidates, key=lambda item: item.seed_score, reverse=True)
    seeds = [
        candidate
        for candidate in ordered
        if candidate.seed_score >= min_seed_score
    ][:seed_limit]

    activation_scores = {candidate.node.id: candidate.seed_score for candidate in seeds}
    hop_distance = {candidate.node.id: 0 for candidate in seeds}
    frontier = {candidate.node.id: candidate.seed_score for candidate in seeds}

    for hop in range(1, max_hops + 1):
        next_frontier: dict[str, float] = {}
        for source_id, source_activation in sorted(frontier.items(), key=lambda item: item[1], reverse=True):
            eligible_edges = [
                edge
                for edge in adjacency.get(source_id, [])
                if edge.weight >= min_edge_weight and edge_is_effectively_propagation_eligible(edge, node_by_id)
            ]
            eligible_edges.sort(key=lambda edge: edge.weight, reverse=True)
            for edge in eligible_edges[:fanout_cap]:
                target_id = _other_node_id(edge, source_id)
                if target_id not in candidate_by_id:
                    continue
                if hop_distance.get(target_id, max_hops + 1) < hop:
                    continue
                propagated = source_activation * activation_decay * edge.weight * edge_type_bias.get(edge.edge_type, 1.0)
                propagated = min(max_total_activation, propagated)
                if propagated < min_activation:
                    continue
                next_frontier[target_id] = next_frontier.get(target_id, 0.0) + propagated

        frontier = {}
        for target_id, score in next_frontier.items():
            bounded = min(max_total_activation, score)
            if bounded < min_activation:
                continue
            if bounded <= activation_scores.get(target_id, 0.0):
                continue
            activation_scores[target_id] = bounded
            hop_distance.setdefault(target_id, hop)
            frontier[target_id] = bounded

        if not frontier:
            break

    results: list[ActivationResult] = []
    for candidate in ordered:
        activation_score = activation_scores.get(candidate.node.id, 0.0)
        total_score = max(candidate.seed_score, activation_score)
        propagated_bonus = max(0.0, total_score - candidate.seed_score)
        results.append(
            ActivationResult(
                node=candidate.node,
                total_score=round(total_score, 6),
                activation_score=round(activation_score, 6),
                propagated_bonus=round(propagated_bonus, 6),
                hop_distance=hop_distance.get(candidate.node.id),
                breakdown={
                    **candidate.breakdown,
                    "graph": round(propagated_bonus, 6),
                    "seed_score": round(candidate.seed_score, 6),
                    "activation_score": round(activation_score, 6),
                },
            )
        )
    return sorted(results, key=lambda item: item.total_score, reverse=True)
