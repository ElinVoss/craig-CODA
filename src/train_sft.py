from __future__ import annotations

import argparse
from pathlib import Path

import yaml

from .io_utils import read_jsonl

ROOT = Path(__file__).resolve().parents[1]


def load_sft_config(config_path: str | Path | None = None) -> dict:
    if config_path is None:
        config_path = ROOT / "configs" / "training_sft.yaml"
    path = Path(config_path)
    if not path.is_absolute():
        path = ROOT / path
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def validate_sft_dataset(config: dict) -> tuple[Path, list[dict]]:
    dataset_path = Path(config["dataset_path"])
    if not dataset_path.is_absolute():
        dataset_path = ROOT / dataset_path
    if not dataset_path.is_file():
        raise FileNotFoundError(f"Missing SFT dataset: {dataset_path}")
    records = read_jsonl(dataset_path)
    required = list(config["schema_expectations"]["required_fields"])
    for index, record in enumerate(records, start=1):
        missing = [field for field in required if field not in record]
        if missing:
            raise ValueError(f"{dataset_path}: record {index}: missing fields: {', '.join(missing)}")
    return dataset_path, records


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the SFT path and print the next steps.")
    parser.add_argument("--config", default=str(ROOT / "configs" / "training_sft.yaml"))
    args = parser.parse_args()

    config = load_sft_config(args.config)
    dataset_path, records = validate_sft_dataset(config)
    print(f"SFT scaffold validated dataset: {dataset_path}")
    print(f"Records available: {len(records)}")
    print("This path is a later-stage scaffold. No full SFT loop is implemented in this phase.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

