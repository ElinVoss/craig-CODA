from __future__ import annotations

from collections import defaultdict

from .index_semantic import tokenize
from .node_schema import VaultEdge, VaultNode


def build_adjacency(edges: list[VaultEdge]) -> dict[str, list[VaultEdge]]:
    adjacency: dict[str, list[VaultEdge]] = defaultdict(list)
    for edge in edges:
        adjacency[edge.source_id].append(edge)
        adjacency[edge.target_id].append(edge)
    return adjacency


def graph_weight(query: str, node: VaultNode, adjacency: dict[str, list[VaultEdge]]) -> float:
    neighbors = adjacency.get(node.id, [])
    if not neighbors:
        return 0.0
    query_tokens = tokenize(query)
    shared_token_bonus = 0.0
    for tag in node.tags + node.links + node.projects:
        if tag.lower() in query_tokens:
            shared_token_bonus += 0.08
    degree_score = min(1.0, sum(edge.weight for edge in neighbors) / max(1, len(neighbors)))
    return round(min(1.0, degree_score * 0.7 + shared_token_bonus), 6)
