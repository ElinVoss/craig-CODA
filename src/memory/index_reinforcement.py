from __future__ import annotations

from math import log1p

from .node_schema import VaultNode


def reinforcement_weight(node: VaultNode) -> float:
    return round(min(1.0, log1p(max(0, node.reinforcement_count)) / 2.0), 6)
