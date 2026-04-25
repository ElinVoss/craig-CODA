from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.model_backends.load_backend import list_all_backends

REQUIRED_FIELDS = [
    "backend_name",
    "enabled",
    "backend_type",
    "model_family",
    "model_id_or_local_path",
    "role",
    "generation_defaults",
]


def _looks_like_local_path(value: str) -> bool:
    """Heuristic: if the string contains a path separator or starts with a drive letter."""
    return "/" in value or "\\" in value or (len(value) >= 2 and value[1] == ":")


def validate_one(b: dict) -> list[tuple[str, str, str]]:
    """Validate a single backend dict. Returns list of (check_name, status, detail)."""
    results = []
    name = b.get("backend_name", "(unnamed)")

    # 1. Required fields present
    missing = [f for f in REQUIRED_FIELDS if f not in b]
    if missing:
        results.append(("required_fields", "FAIL", f"Missing: {missing}"))
    else:
        results.append(("required_fields", "PASS", "All required fields present"))

    # 2. Local path existence check
    model_path = str(b.get("model_id_or_local_path", ""))
    if model_path and _looks_like_local_path(model_path):
        p = Path(model_path)
        if p.exists():
            results.append(("local_path_exists", "PASS", f"{model_path}"))
        else:
            results.append(("local_path_exists", "FAIL", f"Path not found: {model_path}"))
    else:
        results.append(("local_path_exists", "SKIP", f"Not a local path: {model_path}"))

    # 3. Backend class importable
    backend_type = str(b.get("backend_type", ""))
    try:
        from src.model_backends.backend_registry import DEFAULT_REGISTRY
        cls = DEFAULT_REGISTRY.get(backend_type)
        results.append(("backend_class_import", "PASS", f"Class: {cls.__name__}"))
    except KeyError as exc:
        results.append(("backend_class_import", "FAIL", str(exc)))
    except Exception as exc:
        results.append(("backend_class_import", "FAIL", f"Unexpected error: {exc}"))

    return results


def print_backend_results(name: str, checks: list[tuple[str, str, str]]) -> bool:
    """Print results for one backend. Returns True if all passed."""
    all_pass = all(status in ("PASS", "SKIP") for _, status, _ in checks)
    banner = "OK" if all_pass else "ISSUES FOUND"
    print(f"\n--- {name} [{banner}] ---")
    for check_name, status, detail in checks:
        icon = {"PASS": "[PASS]", "FAIL": "[FAIL]", "SKIP": "[SKIP]"}.get(status, status)
        print(f"  {icon}  {check_name:<30} {detail}")
    return all_pass


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate configured backends without loading weights."
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--backend", help="Validate one specific backend by name.")
    group.add_argument("--all", action="store_true", help="Validate all enabled backends.")
    args = parser.parse_args()

    all_backends = list_all_backends()

    if not args.backend and not args.all:
        parser.print_help()
        print(
            "\nNote: Use --all to validate all enabled backends, "
            "or --backend <name> for a specific one."
        )
        return 0

    if args.backend:
        targets = [b for b in all_backends if b.get("backend_name") == args.backend]
        if not targets:
            available = [b.get("backend_name") for b in all_backends]
            print(f"[FAIL] Backend '{args.backend}' not found. Available: {available}")
            return 1
    else:
        # --all: only enabled backends
        targets = [b for b in all_backends if b.get("enabled")]
        if not targets:
            print("No enabled backends found in pretrained_backends.yaml.")
            print("Set enabled: true for at least one backend to validate.")
            return 0

    overall_ok = True
    for b in targets:
        name = str(b.get("backend_name", "(unnamed)"))
        checks = validate_one(b)
        ok = print_backend_results(name, checks)
        if not ok:
            overall_ok = False

    print()
    if overall_ok:
        print("All checks passed.")
    else:
        print("Some checks failed. See above for details.")
    return 0 if overall_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
