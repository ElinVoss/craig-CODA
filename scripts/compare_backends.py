from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.model_backends.load_backend import list_all_backends, load_backend, _load_selection_yaml
from src.model_backends.run_generation import run_comparison
from src.runtime.prompt_compiler import compile_mode_prompt


def _default_comparison_backends() -> list[str]:
    selection = _load_selection_yaml(None)
    names = selection.get("comparison_backend_names", [])
    if names:
        return list(names)
    # Fallback: all enabled backends
    return [b["backend_name"] for b in list_all_backends() if b.get("enabled")]


def _render_text_report(
    compiled_prompt: str,
    mode: str,
    results,
    timestamp: str,
) -> str:
    sep = "=" * 70
    thin = "-" * 70
    lines = [
        sep,
        f"BACKEND COMPARISON REPORT",
        f"Timestamp : {timestamp}",
        f"Mode      : {mode}",
        f"Backends  : {', '.join(r.backend_name for r in results)}",
        sep,
        "",
        "PROMPT USED:",
        thin,
        compiled_prompt[:2000] + ("..." if len(compiled_prompt) > 2000 else ""),
        "",
    ]
    for r in results:
        lines += [
            sep,
            f"BACKEND: {r.backend_name}",
            f"Elapsed: {r.elapsed_seconds:.2f}s   Approx tokens generated: {r.tokens_generated}",
            thin,
            r.text or "(no output)",
            "",
        ]
    lines += [
        sep,
        "SUMMARY",
        thin,
    ]
    for r in results:
        lines.append(f"  {r.backend_name:<30} {r.elapsed_seconds:.2f}s")
    lines.append(sep)
    return "\n".join(lines)


def _render_json_report(
    compiled_prompt: str,
    mode: str,
    results,
    timestamp: str,
) -> str:
    record = {
        "timestamp": timestamp,
        "mode": mode,
        "prompt_used": compiled_prompt,
        "results": [
            {
                "backend_name": r.backend_name,
                "output": r.text,
                "elapsed_seconds": r.elapsed_seconds,
                "tokens_generated": r.tokens_generated,
                "prompt_length": r.prompt_length,
            }
            for r in results
        ],
    }
    return json.dumps(record, indent=2, ensure_ascii=False)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the same prompt through multiple backends and compare outputs."
    )
    parser.add_argument("--prompt", required=True, help="Prompt text to compare.")
    parser.add_argument(
        "--backends",
        nargs="+",
        default=None,
        help="Backend names to compare. Defaults to comparison_backend_names in backend_selection.yaml.",
    )
    parser.add_argument("--mode", default="craig_default", help="Runtime mode (default: craig_default).")
    parser.add_argument("--rs1-specialty", action="store_true", help="Apply rs1_specialty overlay.")
    parser.add_argument("--rs1-creative", action="store_true", help="Apply rs1_creative overlay.")
    parser.add_argument("--save", action="store_true", help="Save comparison report to artifacts/samples/.")
    parser.add_argument(
        "--report-format",
        choices=["text", "json"],
        default="text",
        help="Output format: text (default) or json.",
    )
    args = parser.parse_args()

    backend_names = args.backends or _default_comparison_backends()
    if not backend_names:
        print("[ERROR] No backends specified and no comparison_backend_names configured.")
        print("        Use --backends b1 b2 or set comparison_backend_names in backend_selection.yaml.")
        return 1

    # Step 1: compile prompt once
    print(f"\n[compare_backends] Mode: {args.mode}  Backends: {backend_names}")
    try:
        compiled_prompt, included_files = compile_mode_prompt(
            mode_name=args.mode,
            include_context=False,
            include_rs1_specialty=args.rs1_specialty,
            include_rs1_creative=args.rs1_creative,
        )
    except FileNotFoundError as exc:
        print(f"[WARNING] Could not load mode files: {exc}")
        print("[WARNING] Running with empty system prompt.")
        compiled_prompt = ""
        included_files = []

    composed_prompt = f"System:\n{compiled_prompt}\n\nUser:\n{args.prompt}\n\nAssistant:\n"

    # Step 2: load all specified backends
    backends = []
    for name in backend_names:
        try:
            b = load_backend(name)
            b.load()
            backends.append(b)
        except Exception as exc:
            print(f"[SKIP] Could not load backend '{name}': {exc}")

    if not backends:
        print("[ERROR] No backends could be loaded.")
        return 1

    # Step 3: run comparison
    results = run_comparison(backends, composed_prompt)

    # Step 4: render and print
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if args.report_format == "json":
        report_text = _render_json_report(composed_prompt, args.mode, results, timestamp)
    else:
        report_text = _render_text_report(composed_prompt, args.mode, results, timestamp)

    print("\n" + report_text)

    # Step 5: save if requested
    if args.save:
        output_dir = ROOT / "artifacts" / "samples"
        output_dir.mkdir(parents=True, exist_ok=True)
        ext = "json" if args.report_format == "json" else "txt"
        out_path = output_dir / f"comparison_{timestamp}.{ext}"
        out_path.write_text(report_text, encoding="utf-8")
        print(f"Saved comparison report to {out_path}")

    # Step 6: print summary
    print("\nSummary:")
    for r in results:
        print(f"  {r.backend_name:<30} responded in {r.elapsed_seconds:.2f}s")
    responded = len(results)
    skipped = len(backend_names) - len(backends)
    print(f"\nBackends responded: {responded}  Skipped: {skipped}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
