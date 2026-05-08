from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.runtime.front_matter_schema import PromptFrontMatter


def classify_query_profile(query: str, front_matter: PromptFrontMatter | None = None) -> str:
    if front_matter is not None and front_matter.retrieval_profile:
        return front_matter.retrieval_profile
    lowered = query.lower()
    if any(token in lowered for token in ["story", "scene", "voice", "prose", "elin"]):
        return "prose"
    if any(token in lowered for token in ["constraint", "policy", "forbidden", "allowed"]):
        return "constraints"
    if any(token in lowered for token in ["critique", "audit", "diagnose", "structural"]):
        return "critique"
    if any(token in lowered for token in ["remember", "memory", "autobiographical", "personal"]):
        return "autobiographical"
    if any(token in lowered for token in ["bridge", "analogy", "cross-domain", "transfer"]):
        return "cross_domain"
    return "technical"
