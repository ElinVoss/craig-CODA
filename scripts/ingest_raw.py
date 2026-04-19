from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
SUPPORTED_EXTENSIONS = {".txt", ".md", ".jsonl"}


def load_config() -> dict:
    import yaml

    return yaml.safe_load((ROOT / "configs" / "cleaning.yaml").read_text(encoding="utf-8"))


def find_sources(raw_root: Path) -> list[Path]:
    sources: list[Path] = []
    for path in sorted(raw_root.rglob("*")):
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            if "_ingested" in path.relative_to(raw_root).parts:
                continue
            sources.append(path)
    return sources


def ingest(raw_root: Path, ingest_root: Path) -> list[dict]:
    if ingest_root.exists():
        shutil.rmtree(ingest_root)
    ingest_root.mkdir(parents=True, exist_ok=True)

    manifest: list[dict] = []
    for source in find_sources(raw_root):
        relative = source.relative_to(raw_root)
        destination = ingest_root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        manifest.append(
            {
                "source_file": relative.as_posix(),
                "source_type": source.suffix.lower().lstrip("."),
                "bytes": source.stat().st_size,
            }
        )
    (ingest_root / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest local raw files into a staged raw area.")
    parser.add_argument("--raw-root", default=str(ROOT / "data" / "raw"))
    parser.add_argument("--ingest-root", default=str(ROOT / "data" / "raw" / "_ingested"))
    args = parser.parse_args()

    raw_root = Path(args.raw_root)
    ingest_root = Path(args.ingest_root)
    if not raw_root.exists():
        raise FileNotFoundError(f"Missing raw root: {raw_root}")

    manifest = ingest(raw_root, ingest_root)
    print(f"Ingested {len(manifest)} file(s) from {raw_root}")
    for item in manifest:
        print(f"- {item['source_file']} ({item['source_type']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
