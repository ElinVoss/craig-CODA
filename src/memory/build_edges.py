from __future__ import annotations

from collections import defaultdict

from .node_schema import VaultEdge, VaultNode


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

    # shared_link and shared_project carry genuine structural signal and are safe to propagate.
    # same_source and shared_tag are too coarse — they create hubs that flood the field.
    _propagation_eligible = {"shared_link", "shared_project"}

    def add_edge(source_id: str, target_id: str, edge_type: str, weight: float, rationale: str) -> None:
        if source_id == target_id:
            return
        key = tuple(sorted((source_id, target_id))) + (edge_type,)
        if key not in edges or weight > edges[key].weight:
            left, right = sorted((source_id, target_id))
            edges[key] = VaultEdge(
                source_id=left,
                target_id=right,
                edge_type=edge_type,
                weight=weight,
                rationale=rationale,
                propagation_eligible=edge_type in _propagation_eligible,
            )

    for grouped in by_source.values():
        for index, left in enumerate(grouped):
            for right in grouped[index + 1 :]:
                add_edge(left.id, right.id, "same_source", 0.55, "shared source file")

    for tag, grouped in by_tag.items():
        for index, left in enumerate(grouped):
            for right in grouped[index + 1 :]:
                add_edge(left.id, right.id, "shared_tag", 0.45, f"shared tag: {tag}")

    for project, grouped in by_project.items():
        for index, left in enumerate(grouped):
            for right in grouped[index + 1 :]:
                add_edge(left.id, right.id, "shared_project", 0.65, f"shared project: {project}")

    for target, grouped in by_link_target.items():
        for index, left in enumerate(grouped):
            for right in grouped[index + 1 :]:
                add_edge(left.id, right.id, "shared_link", 0.75, f"shared link target: {target}")

    return sorted(edges.values(), key=lambda edge: (edge.edge_type, edge.source_id, edge.target_id))
