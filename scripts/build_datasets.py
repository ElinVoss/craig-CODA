from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.dataset_builders import (
    IngestedDocument,
    build_eval_records,
    build_pref_records,
    build_pretrain_corpus,
    build_sft_records,
)
from src.io_utils import read_text, write_jsonl, write_text


def load_build_config(config_path: Path) -> dict:
    import yaml

    return yaml.safe_load(config_path.read_text(encoding="utf-8"))


def load_cleaned_documents(clean_root: Path) -> list[IngestedDocument]:
    documents: list[IngestedDocument] = []
    for path in sorted(clean_root.rglob("*.txt")):
        if path.name == "manifest.json":
            continue
        relative = path.relative_to(clean_root).as_posix()
        source_name = relative.removesuffix(".cleaned.txt")
        source_type = Path(source_name).suffix.lstrip(".")
        documents.append(
            IngestedDocument(
                source_file=source_name,
                source_type=source_type,
                text=read_text(path),
            )
        )
    return documents


def build_outputs(clean_root: Path, config: dict) -> dict:
    documents = load_cleaned_documents(clean_root)
    build_cfg = config["build"]

    pretrain_corpus = build_pretrain_corpus(documents)
    write_text(ROOT / build_cfg["pretrain_output"], pretrain_corpus)

    sft_records = build_sft_records(documents)
    pref_records = build_pref_records(documents)
    eval_records = build_eval_records(documents)

    write_jsonl(ROOT / build_cfg["sft_output"], sft_records)
    write_jsonl(ROOT / build_cfg["prefs_output"], pref_records)
    write_jsonl(ROOT / build_cfg["eval_output"], eval_records)

    return {
        "documents": len(documents),
        "pretrain_chars": len(pretrain_corpus),
        "sft": len(sft_records),
        "prefs": len(pref_records),
        "eval": len(eval_records),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build local dataset outputs from cleaned text.")
    parser.add_argument("--clean-root", default=str(ROOT / "data" / "clean"))
    parser.add_argument("--config", default=str(ROOT / "configs" / "dataset_build.yaml"))
    args = parser.parse_args()

    summary = build_outputs(Path(args.clean_root), load_build_config(Path(args.config)))
    print("Built datasets:")
    for key, value in summary.items():
        print(f"- {key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
