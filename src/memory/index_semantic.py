from __future__ import annotations

import re
import threading
from pathlib import Path
from typing import Optional

from .memory_store import load_memory_config
from .node_schema import VaultNode

TOKEN_PATTERN = re.compile(r"[a-z0-9][a-z0-9_-]+")
ROOT = Path(__file__).resolve().parents[2]

# Embedding model cache — loaded once per process
_embed_model = None
_embed_lock = threading.Lock()

# Sidecar embeddings cache — populated by async_indexer daemon
_sidecar: dict[str, list[float]] | None = None
_sidecar_lock = threading.Lock()
_SIDECAR_PATH = ROOT / "artifacts" / "vault" / "embeddings.jsonl"


def _get_sidecar() -> dict[str, list[float]]:
    global _sidecar
    if _sidecar is not None:
        return _sidecar
    with _sidecar_lock:
        if _sidecar is not None:
            return _sidecar
        from .async_indexer import load_embeddings
        _sidecar = load_embeddings(_SIDECAR_PATH)
    return _sidecar


def _get_embed_model(model_path: str):
    global _embed_model
    if _embed_model is not None:
        return _embed_model
    with _embed_lock:
        if _embed_model is not None:
            return _embed_model
        try:
            from sentence_transformers import SentenceTransformer
            resolved = ROOT / model_path if not Path(model_path).is_absolute() else Path(model_path)
            if not resolved.exists():
                return None
            _embed_model = SentenceTransformer(str(resolved))
        except Exception:
            return None
    return _embed_model


def tokenize(text: str, stopwords: set[str] | None = None) -> set[str]:
    tokens = {match.group(0).lower() for match in TOKEN_PATTERN.finditer(text.lower())}
    if stopwords:
        return {token for token in tokens if token not in stopwords}
    return tokens


def _lexical_score(query: str, node: VaultNode, stopwords: set[str]) -> float:
    query_tokens = tokenize(query, stopwords)
    node_tokens = tokenize(f"{node.summary} {node.content}", stopwords)
    if not query_tokens or not node_tokens:
        return 0.0
    overlap = query_tokens.intersection(node_tokens)
    coverage = len(overlap) / max(1, len(query_tokens))
    jaccard = len(overlap) / max(1, len(query_tokens.union(node_tokens)))
    return round(min(1.0, (coverage * 0.7) + (jaccard * 0.3)), 6)


def _embedding_score(query: str, node: VaultNode, model) -> float:
    import numpy as np
    query_vec, node_vec = model.encode([query, f"{node.summary} {node.content}"])
    cos = float(np.dot(query_vec, node_vec) / (np.linalg.norm(query_vec) * np.linalg.norm(node_vec) + 1e-9))
    return round(max(0.0, min(1.0, cos)), 6)


def _sidecar_score(query: str, node: VaultNode, model) -> float | None:
    """Use precomputed node embedding from async_indexer sidecar if available."""
    import numpy as np
    sidecar = _get_sidecar()
    node_vec = sidecar.get(node.id)
    if node_vec is None:
        return None
    query_vec = model.encode([query])[0]
    nv = np.array(node_vec)
    cos = float(np.dot(query_vec, nv) / (np.linalg.norm(query_vec) * np.linalg.norm(nv) + 1e-9))
    return round(max(0.0, min(1.0, cos)), 6)


def semantic_similarity(query: str, node: VaultNode, config_path: str | Path | None = None) -> float:
    config = load_memory_config(config_path)
    retrieval = config["retrieval"]
    method = retrieval.get("semantic_method", "lexical_overlap")
    stopwords = set(retrieval.get("lexical_stopwords", []))

    if method == "embedding":
        model_path = retrieval.get("embedding_model_path", "artifacts/embeddings/all-MiniLM-L6-v2")
        model = _get_embed_model(model_path)
        if model is not None:
            # Prefer sidecar (Ollama-generated) embedding over local model encoding
            score = _sidecar_score(query, node, model)
            if score is not None:
                return score
            return _embedding_score(query, node, model)
        # model path missing — fall back to lexical

    return _lexical_score(query, node, stopwords)
