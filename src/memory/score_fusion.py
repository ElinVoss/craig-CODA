from __future__ import annotations

from pathlib import Path

import yaml

from .memory_store import ROOT, load_memory_config
from .node_schema import VaultNode

QUERY_PROFILES_PATH = ROOT / "configs" / "memory_query_profiles.yaml"


def load_query_profiles(config_path: str | Path | None = None) -> dict:
    path = Path(config_path) if config_path is not None else QUERY_PROFILES_PATH
    if not path.is_absolute():
        path = ROOT / path
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def trust_adjustment(node: VaultNode, retrieval_profile: str, config_path: str | Path | None = None) -> tuple[bool, float]:
    config = load_memory_config(config_path)
    bias = float(config["retrieval"]["trust_layer_bias"].get(node.trust_layer, 0.5))
    if node.trust_layer == "review_only":
        return False, 0.0
    if node.trust_layer == "interpretive_maps" and retrieval_profile != "critique":
        bias *= float(config["retrieval"]["interpretive_penalty"])
    if node.trust_layer == "prose_voice" and retrieval_profile not in {"prose", "cross_domain"}:
        bias *= float(config["retrieval"]["prose_runtime_cap"])
    return True, round(min(1.0, bias), 6)


def fuse_scores(
    retrieval_profile: str,
    semantic: float,
    temporal: float,
    phase: float,
    project: float,
    graph: float,
    voice: float,
    reinforcement: float,
    confidence: float,
    trust_multiplier: float,
    query_profile_path: str | Path | None = None,
) -> float:
    profiles = load_query_profiles(query_profile_path)["profiles"]
    weights = profiles[retrieval_profile]["weights"]
    total = (
        weights["semantic"] * semantic
        + weights["temporal"] * temporal
        + weights["phase"] * phase
        + weights["project"] * project
        + weights["graph"] * graph
        + weights["voice"] * voice
        + weights["reinforcement"] * reinforcement
        + weights["confidence"] * confidence
    )
    return round(total * trust_multiplier, 6)
