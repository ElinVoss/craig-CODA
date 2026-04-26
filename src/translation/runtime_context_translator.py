from __future__ import annotations

from pathlib import Path

import yaml

from src.io_utils import write_json
from src.memory.retrieve_topk import RetrievalResult

ROOT = Path(__file__).resolve().parents[2]
RULES_PATH = ROOT / "configs" / "translator_rules.yaml"
TRANSLATION_PATH = ROOT / "configs" / "vault_translation.yaml"


def _load_config() -> tuple[dict, dict]:
    rules = yaml.safe_load(RULES_PATH.read_text(encoding="utf-8"))
    translation = yaml.safe_load(TRANSLATION_PATH.read_text(encoding="utf-8"))
    return rules, translation


def build_memory_context(results: list[RetrievalResult]) -> dict:
    rules, translation = _load_config()
    allowed_layers = set(rules["runtime_context"]["include_layers"])
    labels = rules["runtime_context"]["summary_prefix"]
    max_items = int(translation["runtime_context"]["max_items"])
    max_chars = int(translation["runtime_context"]["max_chars"])
    max_summary_chars = int(translation["runtime_context"]["max_summary_chars"])
    items: list[dict] = []
    current_chars = 0
    for result in results:
        node = result.node
        if node.trust_layer not in allowed_layers:
            continue
        summary = node.summary[:max_summary_chars].strip()
        current_chars += len(summary)
        if len(items) >= max_items or current_chars > max_chars:
            break
        items.append(
            {
                "node_id": node.id,
                "label": labels.get(node.trust_layer, node.trust_layer),
                "trust_layer": node.trust_layer,
                "source_path": node.source_path,
                "summary": summary,
                "score": result.total_score,
            }
        )
    return {"memory_items": items}


def render_memory_context(context_pack: dict) -> str:
    lines = ["Memory Context:"]
    for item in context_pack.get("memory_items", []):
        lines.append(
            f"- [{item['label']}] {item['summary']} "
            f"(trust={item['trust_layer']}, source={item['source_path']}, score={item['score']:.3f})"
        )
    return "\n".join(lines)


def write_runtime_context_pack(context_pack: dict, filename: str = "default_context_pack.json") -> str:
    _, translation = _load_config()
    target_dir = ROOT / translation["artifact_outputs"]["runtime_context_dir"]
    target_dir.mkdir(parents=True, exist_ok=True)
    path = target_dir / filename
    write_json(path, context_pack)
    return str(path)
