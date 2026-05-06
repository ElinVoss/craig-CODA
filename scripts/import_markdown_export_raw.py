from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = Path(r"D:\conversation-export-work\markdown_export_raw")
DEST_DIR = ROOT / "data" / "raw" / "conversation_exports" / "markdown_export_raw"


def import_export(source: Path, dest: Path, clear: bool = False) -> tuple[int, int]:
    dest.mkdir(parents=True, exist_ok=True)

    if clear:
        for existing in dest.glob("*"):
            if existing.is_file():
                existing.unlink()

    copied = 0
    skipped = 0
    for path in sorted(source.glob("*.md")):
        if path.name.startswith("0000-"):
            skipped += 1
            continue
        shutil.copy2(path, dest / path.name)
        copied += 1
    return copied, skipped


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Import one-markdown-per-conversation exports into Craig-CODA's raw conversation corpus."
    )
    parser.add_argument("--source", default=str(DEFAULT_SOURCE))
    parser.add_argument("--dest", default=str(DEST_DIR))
    parser.add_argument("--clear", action="store_true", help="Clear existing imported markdown files before copying.")
    args = parser.parse_args()

    source = Path(args.source)
    dest = Path(args.dest)

    if not source.is_dir():
        raise SystemExit(f"Source directory not found: {source}")

    copied, skipped = import_export(source, dest, clear=args.clear)
    print(f"Imported {copied} conversation markdown files into {dest}")
    print(f"Skipped {skipped} convenience files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
