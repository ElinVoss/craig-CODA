from __future__ import annotations

from pathlib import Path

from src.io_utils import write_json

from .memory_store import ROOT, load_memory_config, load_memory_graph


def consolidate_memories(config_path: str | Path | None = None) -> dict:
    config = load_memory_config(config_path)
    threshold = int(config["consolidation"]["reinforcement_threshold"])
    limit = int(config["consolidation"]["report_limit"])
    report_dir = ROOT / config["artifacts"]["consolidation_report_dir"]
    report_dir.mkdir(parents=True, exist_ok=True)
    nodes, _ = load_memory_graph(config_path)
    selected = [
        {
            "id": node.id,
            "trust_layer": node.trust_layer,
            "summary": node.summary,
            "reinforcement_count": node.reinforcement_count,
        }
        for node in sorted(nodes, key=lambda item: item.reinforcement_count, reverse=True)
        if node.reinforcement_count >= threshold and node.trust_layer != "review_only"
    ][:limit]
    report = {
        "threshold": threshold,
        "selected_count": len(selected),
        "selected_nodes": selected,
    }
    write_json(report_dir / "consolidation_report.json", report)
    return report
