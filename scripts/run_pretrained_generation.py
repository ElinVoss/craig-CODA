from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.model_backends.load_backend import get_default_backend_name, load_backend
from src.model_backends.run_generation import run_generation
from src.runtime.prompt_compiler import compile_mode_prompt


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run local generation through a configured pretrained backend."
    )
    parser.add_argument(
        "--backend",
        default=None,
        help="Backend name from pretrained_backends.yaml. Defaults to default_backend in backend_selection.yaml.",
    )
    parser.add_argument(
        "--prompt",
        default=None,
        help="Prompt text. If omitted, reads from stdin.",
    )
    parser.add_argument("--mode", default="craig_default", help="Runtime mode (default: craig_default).")
    parser.add_argument("--include-context", action="store_true", help="Include optional context files.")
    parser.add_argument("--rs1-specialty", action="store_true", help="Apply rs1_specialty overlay.")
    parser.add_argument("--rs1-creative", action="store_true", help="Apply rs1_creative overlay.")
    parser.add_argument("--max-new-tokens", type=int, default=None, help="Override max_new_tokens for this run.")
    parser.add_argument("--save", action="store_true", help="Save output to artifacts/samples/.")
    args = parser.parse_args()

    # Resolve prompt
    if args.prompt:
        user_prompt = args.prompt
    elif not sys.stdin.isatty():
        user_prompt = sys.stdin.read().strip()
    else:
        parser.error("--prompt is required (or pipe prompt text via stdin).")
        return 1

    # Resolve backend name
    backend_name = args.backend or get_default_backend_name()

    # Step 1: compile prompt via existing mode_router + prompt_compiler
    print(f"\n[run_pretrained_generation] Mode: {args.mode}  Backend: {backend_name}")
    try:
        system_prompt, included_files = compile_mode_prompt(
            mode_name=args.mode,
            include_context=args.include_context,
            include_rs1_specialty=args.rs1_specialty,
            include_rs1_creative=args.rs1_creative,
        )
    except FileNotFoundError as exc:
        print(f"[WARNING] Could not load mode files: {exc}")
        print("[WARNING] Running with empty system prompt.")
        system_prompt = ""
        included_files = []

    composed_prompt = f"System:\n{system_prompt}\n\nUser:\n{user_prompt}\n\nAssistant:\n"

    # Step 2: load backend
    backend = load_backend(backend_name)
    backend.load()

    # Step 3: generate
    overrides = {}
    if args.max_new_tokens is not None:
        overrides["max_new_tokens"] = args.max_new_tokens

    result = run_generation(backend, composed_prompt, **overrides)

    # Step 4: print output
    sep = "=" * 60
    print(f"\n{sep}")
    print(f"Backend: {result.backend_name}")
    print(f"Elapsed: {result.elapsed_seconds:.2f}s")
    print(sep)
    print(result.text)
    print(sep)

    # Step 5: optionally save
    if args.save:
        import json
        output_dir = ROOT / "artifacts" / "samples"
        output_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        txt_path = output_dir / f"pretrained_{stamp}.txt"
        json_path = output_dir / f"pretrained_{stamp}.json"
        txt_path.write_text(result.text + "\n", encoding="utf-8")
        record = {
            "timestamp": stamp,
            "backend": result.backend_name,
            "mode": args.mode,
            "included_files": [str(p) for p in included_files],
            "prompt": user_prompt,
            "composed_prompt_length": result.prompt_length,
            "output": result.text,
            "elapsed_seconds": result.elapsed_seconds,
        }
        json_path.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Saved to {output_dir}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
