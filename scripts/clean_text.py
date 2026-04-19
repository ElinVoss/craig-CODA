from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.io_utils import read_text, write_text
from src.text_cleaning import CleaningOptions, clean_text


def load_options(config_path: Path) -> CleaningOptions:
    import yaml

    data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    defaults = data["defaults"]
    return CleaningOptions(
        lowercase=bool(defaults["lowercase"]),
        remove_short_lines=bool(defaults["remove_short_lines"]),
        min_line_length=int(defaults["min_line_length"]),
        remove_duplicate_lines=bool(defaults["remove_duplicate_lines"]),
        preserve_blank_lines=bool(defaults["preserve_blank_lines"]),
        max_blank_lines=int(defaults["max_blank_lines"]),
    )


def clean_ingested(raw_ingested_root: Path, clean_root: Path, options: CleaningOptions) -> list[dict]:
    clean_root.mkdir(parents=True, exist_ok=True)
    outputs: list[dict] = []
    for source in sorted(raw_ingested_root.rglob("*")):
        if not source.is_file() or source.name == "manifest.json":
            continue
        if source.suffix.lower() not in {".txt", ".md", ".jsonl"}:
            continue
        relative = source.relative_to(raw_ingested_root)
        cleaned_path = clean_root / relative.with_suffix(relative.suffix + ".cleaned.txt")
        cleaned = clean_text(read_text(source), options)
        write_text(cleaned_path, cleaned)
        outputs.append({"source_file": relative.as_posix(), "cleaned_file": cleaned_path.relative_to(ROOT).as_posix()})
    (clean_root / "manifest.json").write_text(json.dumps(outputs, indent=2), encoding="utf-8")
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description="Clean staged raw text files.")
    parser.add_argument("--ingest-root", default=str(ROOT / "data" / "raw" / "_ingested"))
    parser.add_argument("--clean-root", default=str(ROOT / "data" / "clean"))
    parser.add_argument("--config", default=str(ROOT / "configs" / "cleaning.yaml"))
    args = parser.parse_args()

    options = load_options(Path(args.config))
    outputs = clean_ingested(Path(args.ingest_root), Path(args.clean_root), options)
    print(f"Cleaned {len(outputs)} file(s)")
    for item in outputs:
        print(f"- {item['source_file']} -> {item['cleaned_file']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
