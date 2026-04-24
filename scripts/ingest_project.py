"""
Ingest a craig-structured project into the episodic memory store.

Reads knowledge_index.json from a project directory, loads each file,
builds composite vectors, and stores them in the episodic SQLite database.

Re-ingestion is incremental: nodes whose SHA pin matches the stored content_hash
are skipped. Foundation nodes are born crystallized and decay never touches them.

Usage:
    python scripts/ingest_project.py \
        --project path/to/project_root \
        --db artifacts/episodic/memory.db

    # Force re-ingest all nodes even if SHA matches
    python scripts/ingest_project.py \
        --project path/to/project_root \
        --db artifacts/episodic/memory.db \
        --force
"""
from __future__ import annotations

import argparse
import hashlib
import json
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

# Maps index layer → MemoryNode lane scores
LANE_DEFAULTS = {
    "foundation":   {"emotional": 0.9, "circumstantial": 0.9, "developmental_phase": 0.8},
    "entity":       {"emotional": 0.7, "circumstantial": 0.6, "developmental_phase": 0.5},
    "state":        {"emotional": 0.5, "circumstantial": 0.9, "developmental_phase": 0.6},
    "output":       {"emotional": 0.6, "circumstantial": 0.7, "developmental_phase": 0.5},
    "runtime":      {"emotional": 0.5, "circumstantial": 0.5, "developmental_phase": 0.7},
}


def sha256_content(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()


def ingest(project_root: Path, db_path: Path, force: bool = False) -> None:
    index_path = project_root / "knowledge_index.json"
    if not index_path.exists():
        raise FileNotFoundError(f"knowledge_index.json not found in {project_root}")

    index = json.loads(index_path.read_text(encoding="utf-8"))
    store = EpisodicStore(db_path)
    nodes = index.get("nodes", [])

    ingested = 0
    skipped = 0
    failed = 0

    for entry in nodes:
        node_id = entry.get("id", "")
        rel_path = entry.get("path", "")
        sha_pin = entry.get("sha_pin", "")
        layer = entry.get("layer", "output")
        frame = entry.get("frame", "universal")
        crystallized = entry.get("crystallized", False)

        # Skip template placeholders
        if not node_id or node_id.startswith("{{"):
            continue
        if not rel_path or rel_path.startswith("{{"):
            continue

        file_path = project_root / rel_path
        if not file_path.exists():
            print(f"  MISSING: {rel_path}")
            failed += 1
            continue

        content = file_path.read_text(encoding="utf-8", errors="ignore")
        content_hash = sha256_content(content)

        # Verify SHA pin if set
        if sha_pin and not sha_pin.startswith("{{"):
            actual_sha = hashlib.sha256(file_path.read_bytes()).hexdigest()
            if actual_sha != sha_pin:
                print(f"  SHA MISMATCH: {rel_path} — expected {sha_pin[:8]}... got {actual_sha[:8]}...")
                # Still ingest, but flag it

        # Check if already ingested with same hash
        if not force:
            existing = store.get(node_id)
            if existing is not None:
                existing_hash = store.conn.execute(
                    "SELECT content_hash FROM nodes WHERE id=?", (node_id,)
                ).fetchone()
                if existing_hash and existing_hash[0] == content_hash:
                    skipped += 1
                    continue

        # Build episodic node
        lanes = {
            **LANE_DEFAULTS.get(layer, LANE_DEFAULTS["output"]),
            **(entry.get("episodic_lanes") or {}),
        }

        node = MemoryNode(
            id=node_id,
            content=content,
            domain=layer,
            context_tag=frame,
            emotional=lanes["emotional"],
            circumstantial=lanes["circumstantial"],
            developmental_phase=lanes["developmental_phase"],
            crystallized=crystallized,
        )

        # Foundation nodes get max reinforce_count — born crystallized
        if crystallized:
            node.reinforce_count = cfg.get("decay", {}).get("crystallize_threshold", 40) + 1

        vec = build_composite(node, cfg["weights"], cfg["semantic_model"])
        store.add(node, vec)
        print(f"  INGESTED: [{layer}] {node_id}")
        ingested += 1

    print(f"\nDone. Ingested: {ingested} | Skipped (unchanged): {skipped} | Failed: {failed}")

    # Post-ingest integrity check
    failures = store.verify_integrity()
    if failures:
        print(f"\nWARNING: {len(failures)} crystallized node(s) failed integrity check:")
        for f in failures:
            print(f"  {f['id']}")
    else:
        print("Integrity check: ✅ all crystallized nodes verified")


def main():
    ap = argparse.ArgumentParser(description="Ingest a craig project into episodic memory")
    ap.add_argument("--project", required=True, help="Path to project root (must contain knowledge_index.json)")
    ap.add_argument("--db", default="artifacts/episodic/memory.db", help="Episodic memory DB path")
    ap.add_argument("--force", action="store_true", help="Re-ingest all nodes even if SHA unchanged")
    args = ap.parse_args()

    project_root = Path(args.project).resolve()
    db_path = ROOT / args.db

    print(f"Ingesting: {project_root}")
    print(f"Database : {db_path}\n")
    ingest(project_root, db_path, force=args.force)


if __name__ == "__main__":
    main()
