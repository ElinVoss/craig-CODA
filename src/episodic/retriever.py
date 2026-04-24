from __future__ import annotations
import numpy as np
from datetime import datetime
from .store import EpisodicStore
from .encoder import build_query_vector
from .node import MemoryNode


def retrieve(
    query: str,
    store: EpisodicStore,
    weights: dict,
    model_name: str,
    top_k: int = 10,
    emotional: float = 0.5,
    circumstantial: float = 0.5,
    developmental_phase: float = 0.5,
    session_id: str = "default",
    allowed_frames: list[str] | None = None,  # None = all frames; list = restrict by context_tag
) -> list[tuple[MemoryNode, float]]:

    qvec = build_query_vector(
        query, weights, model_name,
        emotional=emotional,
        circumstantial=circumstantial,
        developmental_phase=developmental_phase,
    )

    # NOTE: pulls all vectors into RAM — fine under ~50k nodes
    ids, matrix = store.all_vectors()
    if len(ids) == 0:
        return []

    qnorm = qvec / (np.linalg.norm(qvec) + 1e-9)
    norms = np.linalg.norm(matrix, axis=1, keepdims=True) + 1e-9
    cosine_scores = (matrix / norms) @ qnorm

    # Apply temporal multiplier at query time against live timestamps
    now = datetime.utcnow()
    t_weight = weights.get("temporal", 5) / 10
    timestamps = store.all_timestamps()

    final_scores = []
    for i, nid in enumerate(ids):
        ts = timestamps.get(nid, now)
        delta_days = (now - ts).total_seconds() / 86400
        t_score = float(np.exp(-delta_days / 30))
        adjusted = float(cosine_scores[i]) + (t_score * t_weight * 0.2)
        final_scores.append(adjusted)

    final_scores = np.array(final_scores)
    top_idx = np.argsort(final_scores)[::-1][:top_k]

    results = []
    retrieved_ids = []
    for idx in top_idx:
        node = store.get(ids[idx])
        if node:
            # Apply frame access gate — skip nodes in locked frames
            if allowed_frames is not None and node.context_tag not in allowed_frames:
                continue
            results.append((node, float(final_scores[idx])))
            retrieved_ids.append(ids[idx])
            store.reinforce(ids[idx])

    store.log_retrieval(session_id, retrieved_ids)
    store.update_resonance(retrieved_ids)
    return results
