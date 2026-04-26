from __future__ import annotations

from datetime import datetime
from math import exp
from pathlib import Path

from .memory_store import load_memory_config
from .node_schema import VaultNode


def temporal_relevance(node: VaultNode, reference_time: datetime | None = None, config_path: str | Path | None = None) -> float:
    config = load_memory_config(config_path)
    half_life = float(config["retrieval"]["temporal_half_life_days"])
    now = reference_time or datetime.utcnow()
    try:
        created = datetime.fromisoformat(node.time_end or node.time_start or node.created_at)
    except ValueError:
        return 0.5
    delta_days = abs((now - created).total_seconds()) / 86400
    return round(float(exp(-delta_days / half_life)), 6)
