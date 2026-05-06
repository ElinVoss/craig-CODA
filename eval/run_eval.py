"""
Retrieval Eval Runner

Runs retrieval_test_suite.yaml against the live vault and reports pass/fail
per case. Skips pending cases with their skip_reason.

Usage:
    python eval/run_eval.py
    python eval/run_eval.py --suite eval/retrieval_test_suite.yaml
    python eval/run_eval.py --dimension trust_enforcement
    python eval/run_eval.py --id R-01 --verbose
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.memory.retrieve_topk import retrieve_nodes, RetrievalResult

SUITE_PATH = Path(__file__).parent / "retrieval_test_suite.yaml"


# ---------------------------------------------------------------------------
# Expectation checkers
# ---------------------------------------------------------------------------

def _trust_layers(results: list[RetrievalResult]) -> list[str]:
    return [r.node.trust_layer for r in results]


def _source_kinds(results: list[RetrievalResult]) -> list[str]:
    return [r.node.source_kind for r in results]


def check_case(case: dict, results: list[RetrievalResult]) -> tuple[bool, list[str]]:
    """Return (passed, list_of_failure_messages)."""
    expect: dict[str, Any] = case.get("expect", {})
    failures: list[str] = []
    trust_layers = _trust_layers(results)

    # any_trust_in_top_k
    for required_trust in expect.get("any_trust_in_top_k", []):
        if required_trust not in trust_layers:
            failures.append(f"Expected trust_layer '{required_trust}' in results, not found")

    # trust_in_top_3
    top3_trust = trust_layers[:3]
    for required_trust in expect.get("trust_in_top_3", []):
        if required_trust not in top3_trust:
            failures.append(
                f"Expected trust_layer '{required_trust}' in top-3, got: {top3_trust}"
            )

    # no_trust_in_results (hard exclusion)
    for banned_trust in expect.get("no_trust_in_results", []):
        offenders = [r for r in results if r.node.trust_layer == banned_trust]
        if offenders:
            ids = [r.node.id for r in offenders]
            failures.append(
                f"trust_layer '{banned_trust}' must never appear; found: {ids}"
            )

    # max_results
    if "max_results" in expect:
        limit = int(expect["max_results"])
        if len(results) > limit:
            failures.append(f"Expected <= {limit} results, got {len(results)}")

    # any_source_kind_in_top_k
    source_kinds = _source_kinds(results)
    for required_kind in expect.get("any_source_kind_in_top_k", []):
        if required_kind not in source_kinds:
            failures.append(f"Expected source_kind '{required_kind}' in results, not found")

    # reinforcement_correlates: check that reinforcement_count > 0 nodes
    # outrank reinforcement_count == 0 nodes with similar semantic scores.
    if expect.get("reinforcement_correlates"):
        reinforced = [r for r in results if r.node.reinforcement_count > 0]
        if reinforced:
            min_reinforced_score = min(r.total_score for r in reinforced)
            unreinforced_above = [
                r for r in results
                if r.node.reinforcement_count == 0 and r.total_score > min_reinforced_score
            ]
            # Only fail if many unreinforced nodes dominate all reinforced ones
            if len(unreinforced_above) > len(reinforced) * 2:
                failures.append(
                    "Reinforcement signal appears weak: many unreinforced nodes "
                    "outscoring reinforced nodes"
                )

    # critique_elevates_interpretive_maps: verify trust_adjustment gives >= 0.85
    # for interpretive_maps under critique (regardless of whether they're in top-k)
    if expect.get("critique_elevates_interpretive_maps"):
        from src.memory.score_fusion import trust_adjustment as _ta
        from src.memory.node_schema import VaultNode as _VN
        import json
        from pathlib import Path as _Path
        vault_path = _Path("artifacts/vault/nodes.jsonl")
        all_nodes = [_VN.from_dict(json.loads(l)) for l in vault_path.read_text().splitlines()]
        interp_nodes = [n for n in all_nodes if n.trust_layer == "interpretive_maps"]
        if interp_nodes:
            _, critique_bias = _ta(interp_nodes[0], "critique")
            if critique_bias < 0.85:
                failures.append(
                    f"interpretive_maps trust_multiplier under critique is {critique_bias:.3f} "
                    f"(expected >= 0.85); profile_trust_bias_overrides not applied"
                )

    return (len(failures) == 0), failures


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run_suite(
    suite_path: Path,
    dimension_filter: str | None,
    id_filter: str | None,
    verbose: bool,
) -> None:
    with suite_path.open(encoding="utf-8") as f:
        suite = yaml.safe_load(f)

    cases = suite.get("cases", [])
    if dimension_filter:
        cases = [c for c in cases if c.get("dimension") == dimension_filter]
    if id_filter:
        cases = [c for c in cases if c.get("id") == id_filter]

    total = len(cases)
    passed = skipped = failed = 0
    failure_log: list[tuple[str, list[str]]] = []

    for case in cases:
        cid = case.get("id", "?")
        desc = case.get("desc", "")
        status = case.get("status", "ready")

        if status == "pending":
            reason = case.get("skip_reason", "no reason given")
            if verbose:
                print(f"  SKIP  {cid}: {reason}")
            skipped += 1
            continue

        top_k = case.get("top_k", 5)
        profile = case.get("profile") or None
        query = case["query"]

        try:
            results = retrieve_nodes(query=query, retrieval_profile=profile, top_k=top_k)
        except Exception as exc:
            print(f"  ERROR {cid}: {exc}")
            failed += 1
            failure_log.append((cid, [f"Exception: {exc}"]))
            continue

        ok, messages = check_case(case, results)
        if ok:
            if verbose:
                print(f"  PASS  {cid}: {desc}")
            passed += 1
        else:
            print(f"  FAIL  {cid}: {desc}")
            for msg in messages:
                print(f"          ! {msg}")
            if verbose:
                print(f"          query='{query}' profile={profile} top_k={top_k}")
                for i, r in enumerate(results[:5]):
                    print(
                        f"          [{i}] score={r.total_score:.3f} "
                        f"trust={r.node.trust_layer} "
                        f"summary={r.node.summary[:60]!r}"
                    )
            failed += 1
            failure_log.append((cid, messages))

    print()
    print(f"Results: {passed} passed / {failed} failed / {skipped} skipped  (of {total} cases)")

    if failure_log and not verbose:
        print("\nFailed cases:")
        for cid, msgs in failure_log:
            print(f"  {cid}: {msgs[0]}")

    if failed:
        sys.exit(1)


def main() -> None:
    p = argparse.ArgumentParser(description="Run the retrieval eval suite.")
    p.add_argument("--suite", default=str(SUITE_PATH), help="Path to test suite YAML")
    p.add_argument("--dimension", default=None, help="Filter to one dimension")
    p.add_argument("--id", default=None, help="Run a single case by ID")
    p.add_argument("--verbose", "-v", action="store_true",
                   help="Show pass details and result breakdowns on failure")
    args = p.parse_args()

    run_suite(
        suite_path=Path(args.suite),
        dimension_filter=args.dimension,
        id_filter=args.id,
        verbose=args.verbose,
    )


if __name__ == "__main__":
    main()
