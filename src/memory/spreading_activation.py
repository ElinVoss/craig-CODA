"""
Spreading activation engine for vault retrieval.

Architecture (Field Resonance Model):
  Phase I  — Permeability: handled upstream by trust_adjustment() before this module is called.
  Phase II  — Excitation: seed_scores are the tick-0 charge (score_fusion output = ACT-R base-level).
  Phase III — Propagation: energy spreads across propagation_eligible edges with proportional split.
  Phase IV  — Crystallization: deferred; callers receive final_potential per node and can apply it.

Energy is budgeted, not copied. A firing node splits propagation_fraction of its potential
across its top-N eligible neighbors (by edge weight). The source retains the remainder.
This prevents hubs from flooding the graph.
"""
from __future__ import annotations

from collections import defaultdict

from .node_schema import VaultEdge, VaultNode


def build_propagation_adjacency(
    edges: list[VaultEdge],
) -> dict[str, list[VaultEdge]]:
    """Build adjacency list restricted to propagation-eligible edges."""
    adjacency: dict[str, list[VaultEdge]] = defaultdict(list)
    for edge in edges:
        if not edge.propagation_eligible:
            continue
        adjacency[edge.source_id].append(edge)
        adjacency[edge.target_id].append(edge)
    return adjacency


def run_spreading_activation(
    seed_scores: dict[str, float],
    adjacency: dict[str, list[VaultEdge]],
    nodes_by_id: dict[str, VaultNode],
    max_ticks: int = 8,
    decay: float = 0.6,
    threshold: float = 0.3,
    fan_out: int = 5,
    propagation_fraction: float = 0.4,
) -> dict[str, float]:
    """
    Run the spreading activation tick loop.

    Args:
        seed_scores: node_id → initial charge (output of score_fusion at tick 0).
                     Only nodes present here are active; others start at 0.
        adjacency: propagation-eligible adjacency (from build_propagation_adjacency).
        nodes_by_id: full node lookup (used for guard checks, not scoring).
        max_ticks: hard tick limit to guarantee termination.
        decay: per-tick multiplicative decay applied to all potentials.
        threshold: minimum potential for a node to fire and propagate energy.
        fan_out: max propagation-eligible neighbors a firing node pushes to per tick.
                 Neighbors selected by descending edge weight.
        propagation_fraction: fraction of a firing node's potential shared outward.
                              Source retains (1 - propagation_fraction).

    Returns:
        dict[node_id → final_potential] for all nodes that accumulated any charge.
    """
    potential: dict[str, float] = dict(seed_scores)

    for _tick in range(max_ticks):
        pulses: dict[str, float] = defaultdict(float)
        any_fired = False

        for node_id, pot in potential.items():
            if pot < threshold:
                continue
            neighbors = adjacency.get(node_id, [])
            if not neighbors:
                continue
            # Top-N eligible neighbors by edge weight
            top_neighbors = sorted(neighbors, key=lambda e: e.weight, reverse=True)[:fan_out]
            outgoing = pot * propagation_fraction
            total_weight = sum(e.weight for e in top_neighbors)
            if total_weight == 0:
                continue
            any_fired = True
            # Source retains (1 - propagation_fraction) — no copy, just split
            pulses[node_id] += pot * (1.0 - propagation_fraction) - pot  # net = -outgoing
            for edge in top_neighbors:
                neighbor_id = edge.target_id if edge.source_id == node_id else edge.source_id
                share = outgoing * (edge.weight / total_weight)
                pulses[neighbor_id] += share

        if not any_fired:
            break

        # Integrate pulses
        for node_id, delta in pulses.items():
            potential[node_id] = potential.get(node_id, 0.0) + delta

        # Decay all potentials toward zero
        potential = {nid: v * decay for nid, v in potential.items() if v * decay > 1e-6}

    return potential
