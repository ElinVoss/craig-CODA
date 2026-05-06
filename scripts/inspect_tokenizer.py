from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.io_utils import write_text
from src.tokenizer_utils import load_tokenizer, load_yaml, save_json
from src.tokenizer_checks import sample_round_trip
from src.vault_methods import resolve_stage_config, write_stage_resolution


def inspect(config: dict) -> dict:
    training_cfg = config["training"]
    reporting = config["reporting"]
    samples = list(config["inspection_samples"])
    output_dir = ROOT / training_cfg["output_dir"]
    tokenizer = load_tokenizer(output_dir / "tokenizer.json")

    results = sample_round_trip(tokenizer, samples)
    report = {
        "tokenizer_type": config["tokenizer"]["type"],
        "vocab_size": tokenizer.get_vocab_size(),
        "samples": results,
        "warnings": [],
    }
    if tokenizer.get_vocab_size() < int(config["tokenizer"]["vocab_size"]) // 2:
        report["warnings"].append("Tokenizer vocabulary is smaller than the configured target; corpus may be small.")

    lines = [
        f"Tokenizer type: {report['tokenizer_type']}",
        f"Vocabulary size: {report['vocab_size']}",
        "",
        "Samples:",
    ]
    for item in results:
        lines.append(f"- input: {item['text']}")
        lines.append(f"  tokens: {item['token_count']}")
        lines.append(f"  decoded: {item['decoded']}")
    if report["warnings"]:
        lines.append("")
        lines.append("Warnings:")
        for warning in report["warnings"]:
            lines.append(f"- {warning}")

    report_text = ROOT / reporting["report_text"]
    report_json = ROOT / reporting["report_json"]
    write_text(report_text, "\n".join(lines) + "\n")
    save_json(report_json, report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect a trained local tokenizer.")
    parser.add_argument("--config", default=str(ROOT / "configs" / "tokenizer.yaml"))
    args = parser.parse_args()

    config = load_yaml(Path(args.config))
    config, method_report = resolve_stage_config("tokenizer", config)
    write_stage_resolution("tokenizer", method_report)
    report = inspect(config)
    print(f"Wrote tokenizer report with {len(report['samples'])} sample(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

