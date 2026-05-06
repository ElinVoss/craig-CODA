"""
L1 Route Engine

Pure function routing. No backend calls. No embeddings. No side effects.

Contract: route(prompt_axes, route_rules) -> RouteResult

Match semantics (locked at L1):
  - Within one axis: ANY listed value may match
  - Across axes: ALL specified axes must match
  - Missing or unknown required axes fail the route
  - Multiple matching routes merge by union + dedupe
  - If no routes match: constraint_mode = semantic_only

See graph/routes/route_rules.yaml for the routing configuration.
See graph/nodes/ for capability and constraint definitions.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Any, List, Set

import yaml

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class RouteResult:
    prompt_axes: Dict[str, str]
    classification_confidence: float | None
    constraint_mode: str
    matched_routes: List[str]
    active_subgraph: Dict[str, List[str]]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def load_route_rules(path: str | Path | None = None) -> Dict[str, Any]:
    if path is None:
        path = ROOT / "graph" / "routes" / "route_rules.yaml"
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def route(
    prompt_axes: Dict[str, str],
    route_rules: Dict[str, Any],
    classification_confidence: float | None = None,
    classifier_constraint_mode: str | None = None,
) -> RouteResult:
    """
    Pure L1 route function.

    No backend calls.
    No embeddings.
    No vector search.
    No side effects.

    Match semantics:
    - ANY value within an axis.
    - ALL specified axes across a route.
    - Missing or unknown required axes fail the route.
    - Multiple matching routes merge by union + dedupe.
    """

    matched_routes: List[str] = []
    active_capabilities: Set[str] = set()
    active_constraints: Set[str] = set()

    routes = route_rules.get("routes", {})

    for route_name, route_def in routes.items():
        match_block = route_def.get("match", {})

        if _route_matches(prompt_axes, match_block):
            matched_routes.append(route_name)

            activate = route_def.get("activate", {})

            for capability in activate.get("capabilities", []):
                active_capabilities.add(capability)

            for constraint in activate.get("constraints", []):
                active_constraints.add(constraint)

    # Determine constraint mode
    if not matched_routes:
        constraint_mode = "semantic_only"
    elif classifier_constraint_mode is not None:
        constraint_mode = classifier_constraint_mode
    elif classification_confidence is not None:
        constraint_mode = _confidence_to_constraint_mode(classification_confidence)
    else:
        constraint_mode = "normal"

    return RouteResult(
        prompt_axes=prompt_axes,
        classification_confidence=classification_confidence,
        constraint_mode=constraint_mode,
        matched_routes=matched_routes,
        active_subgraph={
            "capabilities": sorted(active_capabilities),
            "constraints": sorted(active_constraints),
        },
    )


def _route_matches(prompt_axes: Dict[str, str], match_block: Dict[str, List[str]]) -> bool:
    """
    Match semantics (per route_rules.yaml header):
      match_logic: all_axes_any_value
      unknown_axis_behavior: required_axis_unknown_fails_match

    ALL axes in match_block must pass.
    Within each axis, ANY listed value may match.
    If prompt_axes has 'unknown' or missing for a required axis, route fails.
    """
    for axis, allowed_values in match_block.items():
        prompt_value = prompt_axes.get(axis)

        if prompt_value is None:
            return False

        if prompt_value == "unknown":
            return False

        if prompt_value not in allowed_values:
            return False

    return True


def _confidence_to_constraint_mode(confidence: float) -> str:
    if confidence >= 0.60:
        return "normal"
    if confidence >= 0.40:
        return "partial"
    return "semantic_only"


def assemble_backend_prompt(result: RouteResult, user_prompt: str) -> str:
    """
    Assemble the structured backend prompt from the active subgraph.

    At L1, this is still backend-mediated. The graph does routing,
    not generation. The value is that the routing is inspectable
    and the constraints are explicit rather than implicit.
    """
    lines = []

    if result.active_subgraph["constraints"]:
        lines.append("You are operating under the following active graph constraints:")
        lines.append("")
        for constraint in result.active_subgraph["constraints"]:
            lines.append(f"- {_humanize(constraint)}")
        lines.append("")

    if result.active_subgraph["capabilities"]:
        lines.append("Active capabilities:")
        lines.append("")
        for capability in result.active_subgraph["capabilities"]:
            lines.append(f"- {_humanize(capability)}")
        lines.append("")

    if result.constraint_mode != "normal":
        lines.append(f"[Routing note: constraint_mode={result.constraint_mode}]")
        lines.append("")

    lines.append("User prompt:")
    lines.append("")
    lines.append(user_prompt)

    return "\n".join(lines)


def _humanize(snake_str: str) -> str:
    """Convert snake_case node names to readable labels."""
    return snake_str.replace("_", " ").capitalize()


def route_prompt_text(
    text: str,
    route_rules_path: str | Path | None = None,
) -> RouteResult:
    """
    Convenience wrapper: classify text, then route it.

    Keeps classify_prompt.py replaceable — this function is the
    integration point between the classifier and the router.
    """
    from runtime.classify_prompt import classify_prompt

    classification = classify_prompt(text)
    rules = load_route_rules(route_rules_path)

    return route(
        prompt_axes=classification.axes,
        route_rules=rules,
        classification_confidence=classification.confidence,
        classifier_constraint_mode=classification.constraint_mode,
    )


# ── CLI ───────────────────────────────────────────────────────────────


if __name__ == "__main__":
    rules_path = ROOT / "graph" / "routes" / "route_rules.yaml"

    if len(sys.argv) > 1:
        sample = " ".join(sys.argv[1:])
    else:
        sample = "Build the minimal L1 routing layer for the graph architecture."

    result = route_prompt_text(sample, rules_path)
    print(json.dumps(result.to_dict(), indent=2))

    print("\n--- Backend prompt preview ---\n")
    print(assemble_backend_prompt(result, sample))
