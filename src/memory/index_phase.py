from __future__ import annotations

from .node_schema import VaultNode


def phase_match(query: str, node: VaultNode) -> float:
    lowered = query.lower()
    if node.life_phase and node.life_phase.lower() in lowered:
        return 1.0
    if node.life_phase == "current":
        return 0.6
    if node.life_phase == "warehouse" and "warehouse" in lowered:
        return 0.95
    if node.life_phase == "fiction" and any(token in lowered for token in ["fiction", "story", "scene", "elin"]):
        return 0.95
    return 0.35
