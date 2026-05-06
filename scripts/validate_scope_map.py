from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.handoff.scope_map import load_scope_map, resolve_scope, validate_scope_map


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate SCOPE_MAP.yaml and optionally resolve a scope query.")
    parser.add_argument("--config", default=str(ROOT / "SCOPE_MAP.yaml"))
    parser.add_argument("--query", default=None)
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = ROOT / config_path

    errors = validate_scope_map(config_path, ROOT, check_paths=True)
    if errors:
        print("Scope map validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    data = load_scope_map(config_path)
    print(f"Validated {len(data['scopes'])} scopes")
    if args.query:
        print(f"Resolved scope: {resolve_scope(args.query, data)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
