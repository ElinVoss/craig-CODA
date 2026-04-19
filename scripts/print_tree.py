from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

IGNORE_NAMES = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
}


def walk(path: Path, prefix: str = "") -> None:
    entries = [entry for entry in sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name.lower())) if entry.name not in IGNORE_NAMES]
    for index, entry in enumerate(entries):
        connector = "+-- " if index == len(entries) - 1 else "|-- "
        print(f"{prefix}{connector}{entry.name}")
        if entry.is_dir():
            next_prefix = f"{prefix}{'    ' if index == len(entries) - 1 else '|   '}"
            walk(entry, next_prefix)


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    print(ROOT.name)
    walk(ROOT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
