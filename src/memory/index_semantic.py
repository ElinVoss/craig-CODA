from __future__ import annotations

import re
from pathlib import Path

from .memory_store import load_memory_config
from .node_schema import VaultNode

TOKEN_PATTERN = re.compile(r"[a-z0-9][a-z0-9_-]+")


def tokenize(text: str, stopwords: set[str] | None = None) -> set[str]:
    tokens = {match.group(0).lower() for match in TOKEN_PATTERN.finditer(text.lower())}
    if stopwords:
        return {token for token in tokens if token not in stopwords}
    return tokens


def semantic_similarity(query: str, node: VaultNode, config_path: str | Path | None = None) -> float:
    config = load_memory_config(config_path)
    stopwords = set(config["retrieval"]["lexical_stopwords"])
    query_tokens = tokenize(query, stopwords)
    node_tokens = tokenize(f"{node.summary} {node.content}", stopwords)
    if not query_tokens or not node_tokens:
        return 0.0
    overlap = query_tokens.intersection(node_tokens)
    coverage = len(overlap) / max(1, len(query_tokens))
    jaccard = len(overlap) / max(1, len(query_tokens.union(node_tokens)))
    return round(min(1.0, (coverage * 0.7) + (jaccard * 0.3)), 6)
