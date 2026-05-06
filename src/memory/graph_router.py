"""Graph routing layer.

Reads the structure of retrieved nodes + edges — trust layers, node types,
edge clusters, coverage score — and derives a GraphRoutingDescriptor that
tells the agent what behavioral contract applies for this response turn.

This is the front-facing logic layer. The agent's posture, what it can
surface, and how confidently it speaks are determined here by graph
structure, not by a static instruction string.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field

from .node_schema import VaultEdge
from .retrieve_topk import RetrievalResult

# Trust layer precedence — highest trust first (stable_core is most trusted)
_TRUST_PRECEDENCE = [
    "stable_core",
    "project_constraints",
    "episodic_events",
    "prose_voice",
    "interpretive_maps",
    "review_only",
]

# What each node type says the response should do
_TYPE_TO_MODE: dict[str, str] = {
    "constraint_note":    "enumerate_constraints",
    "identity_note":      "reflect_identity",
    "event_note":         "recall_events",
    "conversation_record": "recall_events",
    "prose_fragment":     "match_voice",
    "interpretive_note":  "frame_hypothesis",
    "review_note":        "blocked",
    "note":               "synthesize",
}

# What each trust ceiling says about posture
_TRUST_TO_POSTURE: dict[str, str] = {
    "stable_core":         "authoritative",
    "project_constraints": "constrained",
    "episodic_events":     "reflective",
    "prose_voice":         "stylistic",
    "interpretive_maps":   "hedged",
    "review_only":         "blocked",
}

# Which trust layers are never surfaceable
_BLOCKED_LAYERS = {"review_only"}


@dataclass
class GraphRoutingDescriptor:
    response_mode: str         # what kind of response to produce
    posture: str               # how confidently / what register
    trust_ceiling: str         # highest-trust layer among results
    surfaceable_layers: list[str]  # layers the agent may draw from
    blocked: bool              # True if any review_only node was retrieved
    dominant_node_types: list[str]
    edge_clusters: list[dict]  # edges that connect retrieved nodes to each other
    confidence_floor: float    # minimum node confidence in result set
    graph_coverage: float      # semantic score of top result (0–1 proxy for match quality)
    profile_used: str
    node_count: int

    def render_routing_block(self) -> str:
        """Render a structured text block for injection into the agent's turn context."""
        if self.blocked:
            return (
                "[GRAPH ROUTING]\n"
                "Response mode: blocked\n"
                "Reason: retrieved nodes include review_only material.\n"
                "Contract: do not surface any content from these nodes. "
                "Acknowledge the topic without drawing on restricted material.\n"
                "[/GRAPH ROUTING]"
            )

        lines = [
            "[GRAPH ROUTING]",
            f"Response mode: {self.response_mode}",
            f"Posture: {self.posture}",
            f"Trust ceiling: {self.trust_ceiling}",
            f"Surfaceable layers: {', '.join(self.surfaceable_layers) or 'none'}",
            f"Dominant node types: {', '.join(self.dominant_node_types[:3]) or 'none'}",
            f"Graph coverage: {self.graph_coverage:.2f}  "
            f"Confidence floor: {self.confidence_floor:.2f}  "
            f"Nodes: {self.node_count}  "
            f"Profile: {self.profile_used}",
        ]

        if self.edge_clusters:
            cluster_lines = [
                f"  {e['from_summary']} →[{e['edge_type']}]→ {e['to_summary']}"
                for e in self.edge_clusters[:4]
            ]
            lines.append("Edge clusters (retrieved nodes that are connected):")
            lines.extend(cluster_lines)

        lines.append("")
        lines.append(self._behavioral_contract())
        lines.append("[/GRAPH ROUTING]")
        return "\n".join(lines)

    def _behavioral_contract(self) -> str:
        rules: list[str] = ["Behavioral contract for this turn:"]

        if self.response_mode == "enumerate_constraints":
            rules += [
                "- State constraints as facts. Source each to its node.",
                "- Do not speculate beyond what the constraint nodes say.",
                "- If the query asks for something outside the constraint boundary, name the boundary — do not work around it.",
            ]
        elif self.response_mode == "reflect_identity":
            rules += [
                "- These are stable_core nodes. Affirm them at face value.",
                "- Speak in first person when reflecting identity material.",
                "- Do not hedge stable_core claims with 'I think' or 'possibly'.",
            ]
        elif self.response_mode == "recall_events":
            rules += [
                "- Frame recalled events with temporal context (when, what phase of the project).",
                "- Hedge if node confidence is below 0.8 or if the event is old.",
                "- Do not treat episodic events as permanent constraints or identity facts.",
            ]
        elif self.response_mode == "match_voice":
            rules += [
                "- Use retrieved prose nodes as style reference, not factual authority.",
                "- Match register and rhythm from the prose_fragment nodes.",
                "- Do not assert prose fragments as biographical facts.",
            ]
        elif self.response_mode == "frame_hypothesis":
            rules += [
                "- Frame all claims from interpretive_maps nodes as hypotheses, not facts.",
                "- Use language like 'one reading is...', 'this could indicate...'.",
                "- Invite correction — do not assert interpretation as truth.",
            ]
        elif self.response_mode == "synthesize":
            rules += [
                "- Synthesize across node types. Label which layer each claim comes from.",
                "- Separate stable claims (stable_core) from contextual ones (episodic_events).",
                "- Do not flatten different trust layers into a single undifferentiated answer.",
            ]

        if self.posture == "hedged":
            rules.append("- Hedge posture: surface interpretive content as explicitly uncertain.")

        if self.graph_coverage < 0.3:
            rules.append(
                "- Coverage warning: graph had low semantic match for this query. "
                "Acknowledge the gap rather than confabulating."
            )

        if self.edge_clusters:
            rules.append(
                "- Edge clusters present: these retrieved nodes are structurally related. "
                "Treat them as a coherent group, not isolated facts."
            )

        return "\n".join(rules)


def _edge_clusters(
    results: list[RetrievalResult],
    edges: list[VaultEdge],
) -> list[dict]:
    """Return edges that connect two retrieved nodes — the in-subgraph structure."""
    result_ids = {r.node.id for r in results}
    id_to_summary = {r.node.id: r.node.summary[:55] for r in results}
    clusters = []
    for edge in edges:
        if edge.source_id in result_ids and edge.target_id in result_ids:
            clusters.append({
                "from_id":      edge.source_id,
                "to_id":        edge.target_id,
                "from_summary": id_to_summary.get(edge.source_id, edge.source_id),
                "to_summary":   id_to_summary.get(edge.target_id, edge.target_id),
                "edge_type":    edge.edge_type,
                "weight":       edge.weight,
            })
    return sorted(clusters, key=lambda e: e["weight"], reverse=True)


def derive_routing(
    results: list[RetrievalResult],
    edges: list[VaultEdge],
    profile: str,
) -> GraphRoutingDescriptor:
    """Derive the behavioral routing descriptor from graph structure.

    Args:
        results: Retrieved nodes with scores and breakdowns.
        edges:   All vault edges (used to find in-subgraph connections).
        profile: The retrieval profile that was used.

    Returns:
        A GraphRoutingDescriptor capturing what the graph structure implies
        about how the agent should respond.
    """
    if not results:
        return GraphRoutingDescriptor(
            response_mode="synthesize",
            posture="exploratory",
            trust_ceiling="episodic_events",
            surfaceable_layers=[],
            blocked=False,
            dominant_node_types=[],
            edge_clusters=[],
            confidence_floor=0.0,
            graph_coverage=0.0,
            profile_used=profile,
            node_count=0,
        )

    trust_layers = [r.node.trust_layer for r in results]
    blocked = any(layer in _BLOCKED_LAYERS for layer in trust_layers)

    # Surfaceable layers — ordered by precedence, excluding blocked layers
    surfaceable_set = {l for l in trust_layers if l not in _BLOCKED_LAYERS}
    surfaceable_layers = [l for l in _TRUST_PRECEDENCE if l in surfaceable_set]

    # Trust ceiling — highest-precedence layer among surfaceable results
    trust_ceiling = surfaceable_layers[0] if surfaceable_layers else "episodic_events"

    # Dominant node types (from surfaceable nodes only)
    type_counts = Counter(
        r.node.node_type for r in results
        if r.node.trust_layer not in _BLOCKED_LAYERS
    )
    dominant_node_types = [t for t, _ in type_counts.most_common(3)]

    # Response mode from dominant type
    if blocked and not surfaceable_layers:
        response_mode = "blocked"
    else:
        top_type = dominant_node_types[0] if dominant_node_types else "note"
        response_mode = _TYPE_TO_MODE.get(top_type, "synthesize")

    posture = "blocked" if (blocked and not surfaceable_layers) else _TRUST_TO_POSTURE.get(trust_ceiling, "reflective")

    confidence_floor = min(r.node.confidence for r in results)
    graph_coverage = results[0].breakdown.get("semantic", 0.0) if results else 0.0

    return GraphRoutingDescriptor(
        response_mode=response_mode,
        posture=posture,
        trust_ceiling=trust_ceiling,
        surfaceable_layers=surfaceable_layers,
        blocked=blocked,
        dominant_node_types=dominant_node_types,
        edge_clusters=_edge_clusters(results, edges),
        confidence_floor=confidence_floor,
        graph_coverage=graph_coverage,
        profile_used=profile,
        node_count=len(results),
    )
