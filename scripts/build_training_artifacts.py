from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.io_utils import write_json, write_jsonl
from src.memory.memory_store import load_memory_graph
from src.memory.retrieve_topk import retrieve_nodes
from src.translation.adapter_manifest_translator import build_adapter_manifests
from src.translation.preference_translator import build_preference_records
from src.translation.prose_translator import build_prose_shards
from src.translation.runtime_context_translator import build_memory_context, write_runtime_context_pack
from src.translation.sft_translator import build_sft_records


def main() -> int:
    nodes, _ = load_memory_graph()
    translation_root = ROOT / "artifacts" / "translation"
    translation_root.mkdir(parents=True, exist_ok=True)

    sft_records = build_sft_records(nodes)
    pref_records = build_preference_records(nodes)
    prose_shards = build_prose_shards(nodes)
    manifests = build_adapter_manifests(nodes)
    context_results = retrieve_nodes(
        query="Explain the local-first warehouse runtime constraints.",
        retrieval_profile="technical",
        mode="craig_default",
        top_k=5,
    )
    context_pack = build_memory_context(context_results)

    write_jsonl(translation_root / "sft" / "context_sft.jsonl", sft_records)
    write_jsonl(translation_root / "prefs" / "context_prefs.jsonl", pref_records)
    write_jsonl(translation_root / "prose" / "context_prose.jsonl", prose_shards)
    write_runtime_context_pack(context_pack)
    write_json(translation_root / "adapter_manifests" / "manifest_index.json", {"targets": manifests})

    print(f"SFT records: {len(sft_records)}")
    print(f"Preference records: {len(pref_records)}")
    print(f"Prose shards: {len(prose_shards)}")
    print(f"Adapter manifests: {len(manifests)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
