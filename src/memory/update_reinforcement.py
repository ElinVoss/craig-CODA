from __future__ import annotations

from pathlib import Path

from src.io_utils import read_jsonl, write_jsonl

from .memory_store import ROOT, load_memory_config


def update_reinforcement(node_ids: list[str], config_path: str | Path | None = None) -> None:
    config = load_memory_config(config_path)
    nodes_path = ROOT / config["artifacts"]["nodes_path"]
    records = read_jsonl(nodes_path)
    wanted = set(node_ids)
    for record in records:
        if record["id"] in wanted:
            record["reinforcement_count"] = int(record.get("reinforcement_count", 0)) + 1
    write_jsonl(nodes_path, records)
