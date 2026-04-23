from __future__ import annotations
import numpy as np
from sentence_transformers import SentenceTransformer
from .node import MemoryNode

_model = None


def get_model(model_name: str) -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(model_name)
    return _model


def build_composite(
    node: MemoryNode,
    weights: dict,
    model_name: str,
) -> np.ndarray:
    """Build stored composite — NO temporal lane. Temporal applied at query time."""
    model = get_model(model_name)
    sem = model.encode(node.content, normalize_embeddings=True)  # (384,)

    r_score = min(1.0, np.log1p(node.reinforce_count) / 4)

    scalar_lanes = np.array([
        node.emotional,
        node.circumstantial,
        r_score,
        node.developmental_phase,
    ], dtype=np.float32)

    w = weights
    sem_w = w.get("semantic", 7) / 10
    scalar_weights = np.array([
        w.get("emotional", 4),
        w.get("circumstantial", 6),
        w.get("reinforcement", 5),
        w.get("developmental", 3),
    ], dtype=np.float32) / 10

    return np.concatenate([sem * sem_w, scalar_lanes * scalar_weights])
    # shape: (388,) — semantic(384) + 4 scalar lanes


def build_query_vector(
    query_text: str,
    weights: dict,
    model_name: str,
    emotional: float = 0.5,
    circumstantial: float = 0.5,
    developmental_phase: float = 0.5,
) -> np.ndarray:
    node = MemoryNode(
        content=query_text,
        emotional=emotional,
        circumstantial=circumstantial,
        developmental_phase=developmental_phase,
        reinforce_count=0,
    )
    return build_composite(node, weights, model_name)
