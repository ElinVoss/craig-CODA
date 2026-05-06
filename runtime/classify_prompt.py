"""
L1 Heuristic Prompt Classifier

Intentionally simple keyword-based classification.
The point is not ML quality — the point is making axes explicit
and keeping the classifier replaceable without touching route_prompt.py.

Contract: classify_prompt(text) -> PromptClassification
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Any


AXES = [
    "intent",
    "domain",
    "stakes",
    "reasoning_mode",
    "temporal_scope",
    "trust_layer",
    "voice_signature",
]


@dataclass(frozen=True)
class PromptClassification:
    axes: Dict[str, str]
    axis_confidence: Dict[str, float]
    confidence: float
    constraint_mode: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def classify_prompt(text: str) -> PromptClassification:
    """
    L1 heuristic classifier.

    This is intentionally dumb and inspectable.
    It should be easy to replace later without changing route_prompt.py.
    """

    lowered = text.lower()

    axes = {
        "intent": classify_intent(lowered),
        "domain": classify_domain(lowered),
        "stakes": classify_stakes(lowered),
        "reasoning_mode": classify_reasoning_mode(lowered),
        "temporal_scope": classify_temporal_scope(lowered),
        "trust_layer": classify_trust_layer(lowered),
        "voice_signature": classify_voice_signature(lowered),
    }

    axis_confidence = {
        axis: 0.0 if value == "unknown" else 1.0
        for axis, value in axes.items()
    }

    assigned = sum(1 for value in axes.values() if value != "unknown")
    confidence = assigned / len(AXES)

    constraint_mode = confidence_to_constraint_mode(confidence)

    return PromptClassification(
        axes=axes,
        axis_confidence=axis_confidence,
        confidence=confidence,
        constraint_mode=constraint_mode,
    )


def confidence_to_constraint_mode(confidence: float) -> str:
    if confidence >= 0.60:
        return "normal"
    if confidence >= 0.40:
        return "partial"
    return "semantic_only"


# ── Individual axis classifiers ──────────────────────────────────────


def classify_intent(text: str) -> str:
    if any(k in text for k in ["build", "implement", "write", "create", "make", "scaffold"]):
        return "build"
    if any(k in text for k in ["design", "architect", "structure", "schema", "interface"]):
        return "design"
    if any(k in text for k in ["evaluate", "critique", "review", "assess", "judge"]):
        return "evaluate"
    if any(k in text for k in ["choose", "decide", "recommend", "pick"]):
        return "decide"
    if any(k in text for k in ["debug", "fix", "broken", "error", "failing"]):
        return "debug"
    if any(k in text for k in ["explain", "clarify", "what is", "why"]):
        return "explain"
    return "unknown"


def classify_domain(text: str) -> str:
    # Research keywords checked first — more specific than architecture
    if any(k in text for k in ["l3", "l4", "graph-native", "native inference", "research frontier"]):
        return "research"
    if any(k in text for k in ["route", "routing", "graph", "node", "edge", "axis", "constitution", "architecture"]):
        return "architecture"
    if any(k in text for k in ["python", "yaml", "test", "runtime", "function", "file", "code"]):
        return "implementation"
    if any(k in text for k in ["policy", "trust", "provenance", "audit", "governance"]):
        return "governance"
    if any(k in text for k in ["user", "ux", "product", "interface"]):
        return "product"
    return "unknown"


def classify_stakes(text: str) -> str:
    if any(k in text for k in ["safety", "security", "legal", "medical", "financial", "high stakes"]):
        return "high"
    if any(k in text for k in ["architecture", "lock-in", "core", "design decision", "handoff"]):
        return "medium"
    if any(k in text for k in ["sketch", "rough", "brainstorm", "toy", "example"]):
        return "low"
    # Default to medium — safer than assuming low
    return "medium"


def classify_reasoning_mode(text: str) -> str:
    if any(k in text for k in ["step by step", "procedure", "implement", "write", "scaffold"]):
        return "procedural"
    if any(k in text for k in ["tradeoff", "compare", "versus", "vs", "alternative"]):
        return "comparative"
    if any(k in text for k in ["failure", "attack", "break", "risk", "adversarial"]):
        return "adversarial"
    if any(k in text for k in ["cause", "effect", "because", "mechanism"]):
        return "causal"
    if any(k in text for k in ["design", "generate", "candidate", "propose"]):
        return "generative"
    if any(k in text for k in ["system", "architecture", "graph", "routing", "interface"]):
        return "systems"
    return "unknown"


def classify_temporal_scope(text: str) -> str:
    if any(k in text for k in ["now", "current", "this repo", "craig-coda", "craig coda", "model-lab", "first deliverable", "mvp"]):
        return "current_project"
    if any(k in text for k in ["later", "future", "eventually", "north star", "l4"]):
        return "future"
    if any(k in text for k in ["history", "previous", "past", "handoff"]):
        return "prior_context"
    # Default to current_project — most prompts are about what's happening now
    return "current_project"


def classify_trust_layer(text: str) -> str:
    if any(k in text for k in ["external", "web", "source", "citation"]):
        return "external"
    if any(k in text for k in ["internal", "repo", "craig-coda", "craig coda", "model-lab", "handoff", "constitution"]):
        return "internal"
    # Default to internal — the system is primarily self-referential at L1
    return "internal"


def classify_voice_signature(text: str) -> str:
    if any(k in text for k in ["collaborator", "craig", "work with me"]):
        return "collaborator"
    if any(k in text for k in ["formal", "report", "executive"]):
        return "formal"
    if any(k in text for k in ["teach", "explain", "tutorial"]):
        return "teacher"
    # Default to collaborator — the primary interaction mode
    return "collaborator"


# ── CLI test ─────────────────────────────────────────────────────────


if __name__ == "__main__":
    import json
    import sys

    if len(sys.argv) > 1:
        sample = " ".join(sys.argv[1:])
    else:
        sample = "Build the minimal L1 routing layer for the graph architecture."

    result = classify_prompt(sample)
    print(json.dumps(result.to_dict(), indent=2))
