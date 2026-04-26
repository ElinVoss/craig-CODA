from __future__ import annotations

from .node_schema import VaultNode


def voice_similarity(query: str, node: VaultNode, retrieval_profile: str, mode: str | None = None) -> float:
    lowered = query.lower()
    if retrieval_profile == "prose" or mode == "elin_fiction":
        return round(node.prose_score, 6)
    if retrieval_profile in {"technical", "constraints", "critique"}:
        return round((node.reasoning_score * 0.6) + (node.voice_score * 0.4), 6)
    if "direct" in lowered:
        return round(node.voice_score, 6)
    return round((node.voice_score + node.prose_score) / 2.0, 6)
