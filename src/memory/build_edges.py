from __future__ import annotations

from collections import defaultdict

from .node_schema import VaultEdge, VaultNode, default_propagation_eligible

_BLOCKED_PROPAGATION_LAYERS = {"review_only", "interpretive_maps"}


def _edge_is_propagation_eligible(left: VaultNode, right: VaultNode, edge_type: str, rationale: str) -> bool:
    if not default_propagation_eligible(edge_type, rationale):
        return False
    if left.trust_layer in _BLOCKED_PROPAGATION_LAYERS:
        return False
    if right.trust_layer in _BLOCKED_PROPAGATION_LAYERS:
        return False
    return True


def build_edges(nodes: list[VaultNode]) -> list[VaultEdge]:
    edges: dict[tuple[str, str, str], VaultEdge] = {}
    by_tag: dict[str, list[VaultNode]] = defaultdict(list)
    by_project: dict[str, list[VaultNode]] = defaultdict(list)
    by_source: dict[str, list[VaultNode]] = defaultdict(list)
    by_link_target: dict[str, list[VaultNode]] = defaultdict(list)

    for node in nodes:
        by_source[node.source_path].append(node)
        for tag in node.tags:
            by_tag[tag].append(node)
        for project in node.projects:
            by_project[project].append(node)
        for link in node.links:
            by_link_target[link.lower()].append(node)

    def add_edge(left: VaultNode, right: VaultNode, edge_type: str, weight: float, rationale: str) -> None:
        if left.id == right.id:
            return
        key = tuple(sorted((left.id, right.id))) + (edge_type,)
        if key not in edges or weight > edges[key].weight:
            source_id, target_id = sorted((left.id, right.id))
            edges[key] = VaultEdge(
                source_id=source_id,
                target_id=target_id,
                edge_type=edge_type,
                weight=weight,
                rationale=rationale,
                propagation_eligible=_edge_is_propagation_eligible(left, right, edge_type, rationale),
            )

    for grouped in by_source.values():
        for index, left in enumerate(grouped):
            for right in grouped[index + 1 :]:
                add_edge(left, right, "same_source", 0.55, "shared source file")

    for tag, grouped in by_tag.items():
        for index, left in enumerate(grouped):
            for right in grouped[index + 1 :]:
                add_edge(left, right, "shared_tag", 0.45, f"shared tag: {tag}")

    for project, grouped in by_project.items():
        for index, left in enumerate(grouped):
            for right in grouped[index + 1 :]:
                add_edge(left, right, "shared_project", 0.65, f"shared project: {project}")

    for target, grouped in by_link_target.items():
        for index, left in enumerate(grouped):
            for right in grouped[index + 1 :]:
                add_edge(left, right, "shared_link", 0.75, f"shared link target: {target}")

    return sorted(edges.values(), key=lambda edge: (edge.edge_type, edge.source_id, edge.target_id))
