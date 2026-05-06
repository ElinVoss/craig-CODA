"""
L1 Routing Test Suite

Tests the pure route() function against expected subgraph outputs.
This is the evaluation harness from the architecture spec — the test
suite that defines what "correct routing" means before the system exists.

Writing these tests IS finishing the design. Every place where the
expected subgraph is unclear is an unresolved design question.

Run:
    python -m pytest tests/test_l1_routing.py -v
    python tests/test_l1_routing.py  (no pytest dependency)
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from runtime.route_prompt import route, load_route_rules
from runtime.classify_prompt import classify_prompt


# ── Fixtures ─────────────────────────────────────────────────────────

def get_rules():
    return load_route_rules(ROOT / "graph" / "routes" / "route_rules.yaml")


# ── Unit tests: route() pure function ────────────────────────────────

def test_architecture_design_prompt():
    """
    A design prompt about the architecture should hit l1_architecture_design.
    Expected capabilities: architectural_decomposition, implementation_planning, tradeoff_analysis
    Expected constraints: avoid_rag_framing, distinguish_engineering_from_research,
                         prefer_minimal_working_version, prompt_enters_graph
    """
    axes = {
        "intent": "design",
        "domain": "architecture",
        "stakes": "medium",
        "reasoning_mode": "systems",
        "temporal_scope": "current_project",
        "trust_layer": "internal",
        "voice_signature": "collaborator",
    }
    result = route(axes, get_rules(), classification_confidence=0.85)

    assert "l1_architecture_design" in result.matched_routes, (
        f"Expected l1_architecture_design in matched_routes, got {result.matched_routes}"
    )
    assert "architectural_decomposition" in result.active_subgraph["capabilities"]
    assert "avoid_rag_framing" in result.active_subgraph["constraints"]
    assert "prompt_enters_graph" in result.active_subgraph["constraints"]
    assert result.constraint_mode == "normal"
    print("✓ test_architecture_design_prompt")


def test_build_implementation_prompt():
    """
    A concrete build prompt should hit l1_implementation_build.
    Overlaps with l1_architecture_design on domain=architecture —
    should merge both routes (union + dedupe).
    """
    axes = {
        "intent": "build",
        "domain": "implementation",
        "stakes": "medium",
        "reasoning_mode": "procedural",
        "temporal_scope": "current_project",
        "trust_layer": "internal",
        "voice_signature": "collaborator",
    }
    result = route(axes, get_rules(), classification_confidence=0.75)

    assert "l1_implementation_build" in result.matched_routes
    assert "implementation_planning" in result.active_subgraph["capabilities"]
    assert "prefer_minimal_working_version" in result.active_subgraph["constraints"]
    print("✓ test_build_implementation_prompt")


def test_research_boundary_prompt():
    """
    An L3/L4 research question should hit l1_research_boundary.
    Should NOT activate architectural_decomposition (that's for build/design).
    Should activate failure_mode_detection (research needs adversarial lens).
    """
    axes = {
        "intent": "explain",
        "domain": "research",
        "stakes": "medium",
        "reasoning_mode": "systems",
        "temporal_scope": "future",
        "trust_layer": "internal",
        "voice_signature": "collaborator",
    }
    result = route(axes, get_rules(), classification_confidence=0.70)

    assert "l1_research_boundary" in result.matched_routes
    assert "failure_mode_detection" in result.active_subgraph["capabilities"]
    assert "distinguish_engineering_from_research" in result.active_subgraph["constraints"]
    assert "avoid_rag_framing" in result.active_subgraph["constraints"]
    print("✓ test_research_boundary_prompt")


def test_evaluation_prompt():
    """
    A critique/tradeoff prompt should hit l1_evaluation.
    """
    axes = {
        "intent": "evaluate",
        "domain": "architecture",
        "stakes": "medium",
        "reasoning_mode": "comparative",
        "temporal_scope": "current_project",
        "trust_layer": "internal",
        "voice_signature": "collaborator",
    }
    result = route(axes, get_rules(), classification_confidence=0.80)

    assert "l1_evaluation" in result.matched_routes
    assert "tradeoff_analysis" in result.active_subgraph["capabilities"]
    assert "failure_mode_detection" in result.active_subgraph["capabilities"]
    print("✓ test_evaluation_prompt")


def test_unknown_axis_fails_match():
    """
    If a required axis is 'unknown', the route should not match.
    This is the unknown_axis_behavior: required_axis_unknown_fails_match rule.
    """
    axes = {
        "intent": "unknown",   # classifier couldn't determine
        "domain": "architecture",
        "stakes": "medium",
        "reasoning_mode": "systems",
        "temporal_scope": "current_project",
        "trust_layer": "internal",
        "voice_signature": "collaborator",
    }
    result = route(axes, get_rules(), classification_confidence=0.30)

    # l1_architecture_design requires intent in [design, build] — unknown fails it
    assert "l1_architecture_design" not in result.matched_routes
    # With low confidence and no matches: semantic_only
    assert result.constraint_mode == "semantic_only"
    print("✓ test_unknown_axis_fails_match")


def test_no_match_returns_semantic_only():
    """
    A prompt that matches no route should return constraint_mode: semantic_only
    and an empty active subgraph.
    """
    axes = {
        "intent": "debug",
        "domain": "product",
        "stakes": "low",
        "reasoning_mode": "causal",
        "temporal_scope": "prior_context",
        "trust_layer": "external",
        "voice_signature": "formal",
    }
    result = route(axes, get_rules())

    assert result.matched_routes == []
    assert result.active_subgraph["capabilities"] == []
    assert result.active_subgraph["constraints"] == []
    assert result.constraint_mode == "semantic_only"
    print("✓ test_no_match_returns_semantic_only")


def test_multi_route_union_dedupe():
    """
    A prompt matching multiple routes should produce a union of all
    activated nodes with deduplication.

    intent=build, domain=architecture, reasoning_mode=systems matches:
      - l1_architecture_design (intent=[design,build], domain=[architecture])
      - l1_implementation_build (intent=[build], domain=[implementation,architecture])

    The union should contain capabilities from both routes.
    """
    axes = {
        "intent": "build",
        "domain": "architecture",
        "stakes": "medium",
        "reasoning_mode": "systems",
        "temporal_scope": "current_project",
        "trust_layer": "internal",
        "voice_signature": "collaborator",
    }
    result = route(axes, get_rules(), classification_confidence=0.85)

    # Both routes should match
    assert "l1_architecture_design" in result.matched_routes
    assert "l1_implementation_build" in result.matched_routes

    # Union: architectural_decomposition comes from both, no duplicate
    caps = result.active_subgraph["capabilities"]
    assert caps.count("architectural_decomposition") == 1, "Deduplication failed"
    assert "tradeoff_analysis" in caps        # from l1_architecture_design
    assert "implementation_planning" in caps  # from both
    print("✓ test_multi_route_union_dedupe")


def test_partial_confidence_mode():
    """
    Confidence 0.40-0.59 should produce constraint_mode: partial.
    """
    axes = {
        "intent": "design",
        "domain": "architecture",
        "stakes": "medium",
        "reasoning_mode": "systems",
        "temporal_scope": "current_project",
        "trust_layer": "internal",
        "voice_signature": "collaborator",
    }
    result = route(axes, get_rules(), classification_confidence=0.50)
    assert result.constraint_mode == "partial"
    print("✓ test_partial_confidence_mode")


def test_semantic_only_confidence_mode():
    """
    Confidence < 0.40 should produce constraint_mode: semantic_only
    even if routes matched.
    """
    axes = {
        "intent": "design",
        "domain": "architecture",
        "stakes": "medium",
        "reasoning_mode": "systems",
        "temporal_scope": "current_project",
        "trust_layer": "internal",
        "voice_signature": "collaborator",
    }
    result = route(axes, get_rules(), classification_confidence=0.30)
    assert result.constraint_mode == "semantic_only"
    print("✓ test_semantic_only_confidence_mode")


# ── Integration tests: classify_prompt → route ────────────────────────

def test_acceptance_case_build_routing_layer():
    """
    THE ACCEPTANCE TEST from the architecture spec.

    Input:
        "Build the minimal L1 routing layer for the graph architecture."

    Expected classification approximately:
        intent: build
        domain: architecture
        reasoning_mode: procedural or systems

    Expected matched routes:
        l1_architecture_design
        l1_implementation_build

    Expected constraints include:
        avoid_rag_framing
        distinguish_engineering_from_research
        prefer_minimal_working_version
        prompt_enters_graph

    Expected capabilities include:
        architectural_decomposition
        implementation_planning
        tradeoff_analysis
    """
    prompt = "Build the minimal L1 routing layer for the graph architecture."
    classification = classify_prompt(prompt)
    result = route(
        prompt_axes=classification.axes,
        route_rules=get_rules(),
        classification_confidence=classification.confidence,
        classifier_constraint_mode=classification.constraint_mode,
    )

    print(f"\n  Classified axes: {classification.axes}")
    print(f"  Confidence: {classification.confidence:.2f} ({classification.constraint_mode})")
    print(f"  Matched routes: {result.matched_routes}")
    print(f"  Capabilities: {result.active_subgraph['capabilities']}")
    print(f"  Constraints: {result.active_subgraph['constraints']}")

    assert "build" == classification.axes.get("intent"), (
        f"Expected intent=build, got {classification.axes.get('intent')}"
    )
    assert "architecture" == classification.axes.get("domain"), (
        f"Expected domain=architecture, got {classification.axes.get('domain')}"
    )
    assert len(result.matched_routes) >= 1, "Expected at least one matched route"
    assert "prompt_enters_graph" in result.active_subgraph["constraints"]
    assert "prefer_minimal_working_version" in result.active_subgraph["constraints"]
    assert "implementation_planning" in result.active_subgraph["capabilities"]
    print("✓ test_acceptance_case_build_routing_layer")


def test_routing_determinism():
    """
    ROUTING DETERMINISM EVAL from the architecture spec.

    Identical content, different axis constraints → different subgraphs.

    Variant A: audit/high-stakes → should activate failure_mode_detection
    Variant B: narrative/low-stakes → should NOT activate failure_mode_detection
    """
    # Same conceptual content, different context
    variant_a = {
        "intent": "evaluate",
        "domain": "architecture",
        "stakes": "high",
        "reasoning_mode": "adversarial",
        "temporal_scope": "current_project",
        "trust_layer": "internal",
        "voice_signature": "collaborator",
    }
    variant_b = {
        "intent": "explain",
        "domain": "architecture",
        "stakes": "low",
        "reasoning_mode": "generative",
        "temporal_scope": "current_project",
        "trust_layer": "internal",
        "voice_signature": "collaborator",
    }

    result_a = route(variant_a, get_rules(), classification_confidence=0.80)
    result_b = route(variant_b, get_rules(), classification_confidence=0.80)

    caps_a = set(result_a.active_subgraph["capabilities"])
    caps_b = set(result_b.active_subgraph["capabilities"])

    # They should not be identical
    assert caps_a != caps_b, (
        "Routing determinism failed: different axis constraints produced identical subgraphs"
    )
    print(f"  Variant A capabilities: {sorted(caps_a)}")
    print(f"  Variant B capabilities: {sorted(caps_b)}")
    print(f"  Difference: A-B={sorted(caps_a - caps_b)}, B-A={sorted(caps_b - caps_a)}")
    print("✓ test_routing_determinism")


def test_research_l4_prompt():
    """
    A question about L3/L4 (graph-native inference) should be routed to
    the research boundary, not the architecture design route.
    """
    prompt = "How would graph-native inference actually work at L4 without any backend?"
    classification = classify_prompt(prompt)
    result = route(
        prompt_axes=classification.axes,
        route_rules=get_rules(),
        classification_confidence=classification.confidence,
        classifier_constraint_mode=classification.constraint_mode,
    )

    print(f"\n  Axes: {classification.axes}")
    print(f"  Routes: {result.matched_routes}")

    assert "distinguish_engineering_from_research" in result.active_subgraph["constraints"], (
        "Research-boundary prompt should activate distinguish_engineering_from_research"
    )
    print("✓ test_research_l4_prompt")


# ── Runner ────────────────────────────────────────────────────────────

def run_all():
    tests = [
        test_architecture_design_prompt,
        test_build_implementation_prompt,
        test_research_boundary_prompt,
        test_evaluation_prompt,
        test_unknown_axis_fails_match,
        test_no_match_returns_semantic_only,
        test_multi_route_union_dedupe,
        test_partial_confidence_mode,
        test_semantic_only_confidence_mode,
        test_acceptance_case_build_routing_layer,
        test_routing_determinism,
        test_research_l4_prompt,
    ]

    passed = 0
    failed = 0

    print(f"\nRunning {len(tests)} L1 routing tests\n" + "=" * 50)

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} (error): {e}")
            failed += 1

    print("\n" + "=" * 50)
    print(f"Results: {passed} passed, {failed} failed")

    if failed:
        print("\nFailed tests indicate unresolved design questions.")
        print("Do not proceed to Phase 2 until all tests pass.")
        sys.exit(1)
    else:
        print("\nAll tests passed. L1 routing is implementation-ready.")


if __name__ == "__main__":
    run_all()
