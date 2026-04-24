"""
Ingest personal identity/insight documents directly into craig's episodic memory.

These are not project template nodes. They are Craig's own foundational nodes —
high-salience, crystallized — that should never decay.

Usage:
    python scripts/ingest_personal_nodes.py
    python scripts/ingest_personal_nodes.py --db artifacts/episodic/memory.db
    python scripts/ingest_personal_nodes.py --dry-run
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT))

from src.episodic.node import MemoryNode
from src.episodic.store import EpisodicStore
from src.episodic.encoder import build_composite

CFG_PATH = ROOT / "configs" / "episodic.yaml"
cfg = yaml.safe_load(CFG_PATH.read_text(encoding="utf-8"))

DESKTOP = Path.home() / "Desktop"

# Each entry: (file_path, node_id, metadata_dict)
PERSONAL_NODES: list[tuple[Path, str, dict]] = [
    (
        DESKTOP / "the-realization.txt",
        "personal::the-realization",
        {
            "domain": "identity",
            "context_tag": "analogical_transfer",
            "mood_tag": "convergence",
            "emotional": 0.95,
            "circumstantial": 0.85,
            "developmental_phase": 0.90,
            "crystallized": True,
        },
    ),
    (
        DESKTOP / "research_map.md",
        "personal::research-map",
        {
            "domain": "identity",
            "context_tag": "behavioral_arc",
            "mood_tag": "analytical",
            "emotional": 0.80,
            "circumstantial": 0.75,
            "developmental_phase": 0.95,
            "crystallized": True,
        },
    ),
]


def ingest(db_path: Path, dry_run: bool = False) -> None:
    store = None if dry_run else EpisodicStore(db_path)
    threshold = cfg.get("decay", {}).get("crystallize_threshold", 40)

    for file_path, node_id, meta in PERSONAL_NODES:
        if not file_path.exists():
            print(f"  MISSING: {file_path}")
            continue

        content = file_path.read_text(encoding="utf-8", errors="ignore")

        if not dry_run:
            # Skip if already ingested with same content
            existing = store.get(node_id)
            if existing is not None:
                stored = store.conn.execute(
                    "SELECT content_hash FROM nodes WHERE id=?", (node_id,)
                ).fetchone()
                import hashlib
                current_hash = hashlib.sha256(content.encode()).hexdigest()
                if stored and stored[0] == current_hash:
                    print(f"  SKIPPED (unchanged): {node_id}")
                    continue

        node = MemoryNode(
            id=node_id,
            content=content,
            domain=meta["domain"],
            context_tag=meta["context_tag"],
            mood_tag=meta["mood_tag"],
            emotional=meta["emotional"],
            circumstantial=meta["circumstantial"],
            developmental_phase=meta["developmental_phase"],
            crystallized=meta["crystallized"],
            reinforce_count=threshold + 1 if meta["crystallized"] else 0,
        )

        label = f"[{meta['domain']}:{meta['context_tag']}] {node_id}"
        if dry_run:
            print(f"  DRY RUN — would ingest: {label}")
            print(f"    file   : {file_path}")
            print(f"    chars  : {len(content)}")
            print(f"    emotional={meta['emotional']}  circumstantial={meta['circumstantial']}  phase={meta['developmental_phase']}")
            print(f"    crystallized={meta['crystallized']}")
        else:
            vec = build_composite(node, cfg["weights"], cfg["semantic_model"])
            store.add(node, vec)
            print(f"  INGESTED: {label}")

    if not dry_run:
        failures = store.verify_integrity()
        if failures:
            print(f"\nWARNING: {len(failures)} crystallized node(s) failed integrity check:")
            for f in failures:
                print(f"  {f['id']}")
        else:
            print("\nIntegrity check: OK — all crystallized nodes verified")


def main():
    ap = argparse.ArgumentParser(description="Ingest personal identity nodes into episodic memory")
    ap.add_argument("--db", default="artifacts/episodic/memory.db", help="Episodic DB path")
    ap.add_argument("--dry-run", action="store_true", help="Show what would be ingested without writing")
    args = ap.parse_args()

    db_path = ROOT / args.db
    print(f"Database : {db_path}")
    print(f"Dry run  : {args.dry_run}\n")
    ingest(db_path, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
