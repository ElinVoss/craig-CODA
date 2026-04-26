from __future__ import annotations

from dataclasses import asdict, dataclass

from .index_graph import build_adjacency, graph_weight
from .index_phase import phase_match
from .index_reinforcement import reinforcement_weight
from .index_semantic import semantic_similarity
from .index_temporal import temporal_relevance
from .index_voice import voice_similarity
from .memory_store import load_memory_graph
from .node_schema import VaultNode
from .query_classifier import classify_query_profile
from .score_fusion import fuse_scores, load_query_profiles, trust_adjustment


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
) -> list[RetrievalResult]:
    nodes, edges = load_memory_graph()
    profile = retrieval_profile or classify_query_profile(query)
    profiles = load_query_profiles()["profiles"]
    limit = int(top_k or profiles[profile]["top_k"])
    adjacency = build_adjacency(edges)
    results: list[RetrievalResult] = []

    for node in nodes:
        allowed, trust_multiplier = trust_adjustment(node, profile)
        if not allowed:
            continue
        semantic = semantic_similarity(query, node)
        temporal = temporal_relevance(node)
        phase = phase_match(query, node)
        graph = graph_weight(query, node, adjacency)
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
        )
        results.append(
            RetrievalResult(
                node=node,
                total_score=total_score,
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

    return sorted(results, key=lambda item: item.total_score, reverse=True)[:limit]
