from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

from .index_graph import build_adjacency, graph_weight
from .index_phase import phase_match
from .index_reinforcement import reinforcement_weight
from .index_semantic import semantic_similarity
from .index_temporal import temporal_relevance
from .index_voice import voice_similarity
from .memory_store import load_memory_config, load_memory_graph
from .node_schema import VaultNode
from .query_classifier import classify_query_profile
from .score_fusion import fuse_scores, load_query_profiles, trust_adjustment
from .spreading_activation import SeedCandidate, spread_activation


@dataclass
class RetrievalResult:
    node: VaultNode
    total_score: float
    breakdown: dict[str, float]

    def to_dict(self) -> dict:
        data = asdict(self)
        data["node"] = self.node.to_dict()
        return data


def retrieve_nodes(
    query: str,
    retrieval_profile: str | None = None,
    mode: str | None = None,
    top_k: int | None = None,
    config_path: str | Path | None = None,
    query_profile_path: str | Path | None = None,
) -> list[RetrievalResult]:
    config = load_memory_config(config_path)
    nodes, edges = load_memory_graph(config_path)
    profile = retrieval_profile or classify_query_profile(query)
    profiles = load_query_profiles(query_profile_path)["profiles"]
    limit = int(top_k or profiles[profile]["top_k"])
    limit = min(limit, int(config["retrieval"].get("max_top_k", limit)))
    strategy = str(config["retrieval"].get("strategy", "flat_topk"))
    adjacency = build_adjacency(edges)
    include_graph_bonus = strategy != "spreading_activation"
    candidates: list[SeedCandidate] = []

    for node in nodes:
        allowed, trust_multiplier = trust_adjustment(node, profile, config_path=config_path)
        if not allowed:
            continue
        semantic = semantic_similarity(query, node, config_path=config_path)
        temporal = temporal_relevance(node, config_path=config_path)
        phase = phase_match(query, node)
        graph = graph_weight(query, node, adjacency) if include_graph_bonus else 0.0
        reinforcement = reinforcement_weight(node)
        voice = voice_similarity(query, node, profile, mode=mode)
        total_score = fuse_scores(
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
            query_profile_path=query_profile_path,
        )
        candidates.append(
            SeedCandidate(
                node=node,
                seed_score=total_score,
                breakdown={
                    "semantic": semantic,
                    "temporal": temporal,
                    "phase": phase,
                    "project": node.project_relevance,
                    "graph": graph,
                    "voice": voice,
                    "reinforcement": reinforcement,
                    "confidence": node.confidence,
                    "trust_multiplier": trust_multiplier,
                },
            )
        )

    if strategy == "spreading_activation":
        activated = spread_activation(candidates, edges, config_path=config_path)
        return [
            RetrievalResult(
                node=item.node,
                total_score=item.total_score,
                breakdown=item.breakdown,
            )
            for item in activated[:limit]
        ]

    results = [
        RetrievalResult(
            node=candidate.node,
            total_score=candidate.seed_score,
            breakdown=candidate.breakdown,
        )
        for candidate in sorted(candidates, key=lambda item: item.seed_score, reverse=True)[:limit]
    ]
    return results
