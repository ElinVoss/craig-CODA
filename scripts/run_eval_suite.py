from __future__ import annotations

# run_eval_suite.py — Phase five update.
# Adds --backend arg so the eval can run against any configured backend.
# Falls back to the original scratch checkpoint path when --backend is not given.

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.eval.run_evals import main as _scratch_main


# Eval criteria supported by this suite.
# Scored manually (human review) unless an automatic check can be applied.
EVAL_CRITERIA = [
    "direct_answer_first",
    "no_fake_warmth",
    "no_fluff",
    "mechanism_first_reasoning",
    "low_wrong_assumption_rate",
    "critique_quality",
    "formatting_restraint",
    "honesty_under_uncertainty",
]

# Criteria that can be partially checked automatically (heuristic only).
_AUTO_CHECKABLE = {
    "no_fake_warmth": ["certainly!", "of course!", "great question", "absolutely!"],
    "no_fluff": ["it's worth noting", "as an ai", "i hope this helps"],
}


def _run_backend_eval(args: argparse.Namespace) -> int:
    """Run eval against a named backend from pretrained_backends.yaml."""
    import json
    from datetime import datetime

    import yaml

    from src.model_backends.load_backend import load_backend
    from src.model_backends.run_generation import run_generation
    from src.runtime.prompt_compiler import compile_mode_prompt

    # Load eval config for dataset paths and generation settings
    cfg_path = Path(args.config)
    if not cfg_path.is_absolute():
        cfg_path = ROOT / cfg_path
    config = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))

    # Load eval records
    from src.eval.eval_utils import load_eval_records, run_automatic_checks
    dataset_paths = []
    for item in config.get("datasets", []):
        path = Path(item["path"])
        if not path.is_absolute():
            path = ROOT / path
        dataset_paths.append(path)

    records = load_eval_records(dataset_paths, int(config.get("sample_count", 0)))

    # Compile system prompt
    mode = config.get("generation", {}).get("mode", "craig_default")
    try:
        system_prompt, included_files = compile_mode_prompt(mode_name=mode)
    except FileNotFoundError as exc:
        print(f"[WARNING] Mode files missing: {exc}")
        system_prompt = ""
        included_files = []

    # Load backend
    backend = load_backend(args.backend)
    backend.load()

    results: list[dict] = []
    gen_cfg = config.get("generation", {})
    overrides: dict = {}
    if "max_new_tokens" in gen_cfg:
        overrides["max_new_tokens"] = int(gen_cfg["max_new_tokens"])

    for record in records:
        prompt = record.get("question") or record.get("prompt") or record.get("input") or ""
        full_prompt = f"System:\n{system_prompt}\n\nUser:\n{prompt}\n\nAssistant:\n"
        gen_result = run_generation(backend, full_prompt, **overrides)
        output = gen_result.text

        # Run automatic checks from eval_utils
        auto = run_automatic_checks(record, output)

        # Emit structured eval criteria fields
        lowered = output.lower()
        criteria_scores: dict = {}
        for criterion in EVAL_CRITERIA:
            if criterion in _AUTO_CHECKABLE:
                bad_phrases = _AUTO_CHECKABLE[criterion]
                found = [p for p in bad_phrases if p in lowered]
                criteria_scores[criterion] = {
                    "score": "auto_fail" if found else "auto_pass",
                    "note": f"Found: {found}" if found else "",
                    "method": "automatic",
                }
            else:
                criteria_scores[criterion] = {
                    "score": "pending_manual",
                    "note": "",
                    "method": "manual",
                }

        result = dict(record)
        result["backend"] = args.backend
        result["output"] = output
        result["included_prompt_files"] = [str(p) for p in included_files]
        result["elapsed_seconds"] = gen_result.elapsed_seconds
        result["eval_criteria"] = criteria_scores
        result.update(auto)
        results.append(result)

    # Write report
    report_dir = ROOT / "artifacts" / "eval_reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = report_dir / f"eval_{args.backend}_{timestamp}.json"
    report = {
        "backend": args.backend,
        "mode": mode,
        "timestamp": timestamp,
        "eval_criteria": EVAL_CRITERIA,
        "auto_checkable_criteria": list(_AUTO_CHECKABLE.keys()),
        "manual_criteria": [c for c in EVAL_CRITERIA if c not in _AUTO_CHECKABLE],
        "results": results,
    }
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Eval complete: {len(results)} records evaluated against backend '{args.backend}'")
    print(f"Report written to {report_path}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Run the local evaluation suite. "
            "Without --backend, uses the original scratch checkpoint path. "
            "With --backend, routes through the named pretrained backend."
        )
    )
    parser.add_argument("--config", default=str(ROOT / "configs" / "eval.yaml"))
    parser.add_argument(
        "--backend",
        default=None,
        help=(
            "Backend name from pretrained_backends.yaml. "
            "If omitted, falls back to the scratch checkpoint path (original behavior)."
        ),
    )
    args = parser.parse_args()

    if args.backend:
        return _run_backend_eval(args)

    # Original scratch path — delegate to existing implementation.
    # Reconstruct argv without --backend so the original parser is not confused.
    sys.argv = [sys.argv[0], "--config", args.config]
    return _scratch_main()


if __name__ == "__main__":
    raise SystemExit(main())
