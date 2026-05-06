from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.io_utils import read_text, write_text
from src.vault_methods import resolve_stage_config, write_stage_resolution


def load_config(path: Path) -> dict:
    import yaml

    return yaml.safe_load(path.read_text(encoding="utf-8"))


def collect_sources(config: dict) -> list[Path]:
    input_cfg = config["inputs"]
    roots = [ROOT / root for root in input_cfg["roots"]]
    extensions = {ext.lower() for ext in input_cfg["extensions"]}
    include_markdown = bool(input_cfg.get("include_markdown", False))

    sources: list[Path] = []
    seen: set[Path] = set()
    for root in roots:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            suffix = path.suffix.lower()
            if suffix == ".md" and not include_markdown:
                continue
            if suffix not in extensions and not (include_markdown and suffix == ".md"):
                continue
            if path.name in {"manifest.json"}:
                continue
            if "_ingested" in path.parts:
                continue
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            sources.append(path)
    return sources


def build_corpus(config: dict) -> tuple[str, list[dict]]:
    filter_cfg = config["filtering"]
    max_files = int(config["inputs"].get("max_files", 0))
    max_bytes_per_file = int(config["inputs"].get("max_bytes_per_file", 0))

    source_paths = collect_sources(config)
    if max_files > 0:
        source_paths = source_paths[:max_files]

    chunks: list[str] = []
    manifest: list[dict] = []
    for path in source_paths:
        text = read_text(path)
        if max_bytes_per_file > 0:
            text = text[:max_bytes_per_file]
        if not filter_cfg.get("preserve_case", True):
            text = text.lower()
        lines = [line.strip() if filter_cfg.get("strip_whitespace", True) else line for line in text.splitlines()]
        cleaned: list[str] = []
        seen: set[str] = set()
        blank_run = 0
        for line in lines:
            if not line:
                blank_run += 1
                if blank_run <= int(filter_cfg.get("max_blank_lines", 2)):
                    cleaned.append("")
                continue
            blank_run = 0
            if filter_cfg.get("remove_short_lines", False) and len(line) < int(filter_cfg.get("min_line_length", 1)):
                continue
            key = line.lower() if not filter_cfg.get("preserve_case", True) else line
            if filter_cfg.get("remove_duplicate_lines", False) and key in seen:
                continue
            seen.add(key)
            cleaned.append(line)

        normalized = "\n".join(cleaned).strip()
        if normalized:
            chunks.append(f"### SOURCE: {path.relative_to(ROOT).as_posix()}\n{normalized}")
            manifest.append(
                {
                    "source_file": path.relative_to(ROOT).as_posix(),
                    "bytes": path.stat().st_size,
                    "lines": len(cleaned),
                }
            )

    corpus = "\n\n".join(chunks).strip() + ("\n" if chunks else "")
    return corpus, manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare a deterministic tokenizer corpus from cleaned text.")
    parser.add_argument("--config", default=str(ROOT / "configs" / "corpus_prep.yaml"))
    args = parser.parse_args()

    config = load_config(Path(args.config))
    config, method_report = resolve_stage_config("corpus", config)
    method_report_path = write_stage_resolution("corpus", method_report)
    corpus, manifest = build_corpus(config)
    output_cfg = config["output"]

    corpus_path = ROOT / output_cfg["corpus_file"]
    manifest_path = ROOT / output_cfg["manifest_file"]
    report_path = ROOT / output_cfg["report_file"]

    write_text(corpus_path, corpus)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    report_lines = [
        f"Prepared corpus: {corpus_path.relative_to(ROOT)}",
        f"Sources included: {len(manifest)}",
        f"Characters: {len(corpus)}",
        f"Method prompts applied: {len(method_report['applied_prompts'])}",
        f"Method resolution: {method_report_path.relative_to(ROOT)}",
    ]
    if len(manifest) < 2:
        report_lines.append("Warning: corpus is very small; tokenizer quality will be limited by input size.")
    write_text(report_path, "\n".join(report_lines) + "\n")

    print("\n".join(report_lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

