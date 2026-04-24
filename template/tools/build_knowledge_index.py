"""
Build or update knowledge_index.json for a craig-structured project.

Scans the standard directory layers (01_Foundation, 02_Entities, 03_State_Tracking,
04_Outputs, 06_Runtime) and generates a machine-readable index with SHA256 pins
for every file found.

Run this after any commit that changes project files. The output is committed
alongside the changes so the index always reflects the current state.

Usage:
    python tools/build_knowledge_index.py --root . --out knowledge_index.json
    python tools/build_knowledge_index.py --root . --out knowledge_index.json --commit-sha <sha>
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

# Maps directory prefixes to episodic layer metadata
LAYER_MAP = {
    "01_Foundation": {
        "layer": "foundation",
        "frame": "universal",
        "crystallized": True,
        "priority": "mandatory",
        "episodic_lanes": {"emotional": 0.9, "circumstantial": 0.9, "developmental_phase": 0.8},
    },
    "02_Entities": {
        "layer": "entity",
        "frame": None,   # derived from parent folder name inside frames/
        "crystallized": False,
        "priority": "mandatory",
        "episodic_lanes": {"emotional": 0.7, "circumstantial": 0.6, "developmental_phase": 0.5},
    },
    "03_State_Tracking": {
        "layer": "state",
        "frame": "universal",
        "crystallized": False,
        "priority": "mandatory",
        "episodic_lanes": {"emotional": 0.5, "circumstantial": 0.9, "developmental_phase": 0.6},
    },
    "04_Outputs": {
        "layer": "output",
        "frame": "universal",
        "crystallized": False,
        "priority": "context_chain",
        "episodic_lanes": {"emotional": 0.6, "circumstantial": 0.7, "developmental_phase": 0.5},
    },
    "06_Runtime": {
        "layer": "runtime",
        "frame": "universal",
        "crystallized": True,
        "priority": "mandatory",
        "episodic_lanes": {"emotional": 0.5, "circumstantial": 0.5, "developmental_phase": 0.7},
    },
}

SKIP_PATTERNS = [".gitkeep", "TEMPLATE", "PLACEHOLDER", ".DS_Store"]
ALLOWED_SUFFIXES = {".md", ".yaml", ".yml", ".json", ".txt"}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def get_commit_sha(root: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root, capture_output=True, text=True
        )
        return result.stdout.strip()
    except Exception:
        return "unknown"


def slugify(path: Path) -> str:
    stem = path.stem.lower()
    return re.sub(r"[^a-z0-9]+", "_", stem).strip("_")


def extract_frame_from_path(path: Path) -> str | None:
    """For entity files, extract frame name from path like 02_Entities/name/frames/frame_id/file.md"""
    parts = path.parts
    if "frames" in parts:
        idx = list(parts).index("frames")
        if idx + 1 < len(parts):
            return parts[idx + 1]
    return "universal"


def extract_sequence_n(path: Path) -> int | None:
    """For output files, extract sequence number from filename like N03_title.md"""
    m = re.match(r"N(\d+)_", path.name)
    return int(m.group(1)) if m else None


def scan_layer(root: Path, prefix: str, meta: dict) -> list[dict]:
    layer_dir = root / prefix
    if not layer_dir.exists():
        return []

    nodes = []
    for file in sorted(layer_dir.rglob("*")):
        if not file.is_file():
            continue
        if file.suffix not in ALLOWED_SUFFIXES:
            continue
        if any(skip in file.name for skip in SKIP_PATTERNS):
            continue

        rel = file.relative_to(root)
        node_meta = dict(meta)

        # Entity frame detection
        if prefix == "02_Entities":
            frame = extract_frame_from_path(rel)
            node_meta["frame"] = frame or "universal"

        # Output sequence detection
        seq_n = extract_sequence_n(file)
        if seq_n is not None:
            node_meta["sequence_n"] = seq_n

        node = {
            "id": f"{node_meta['layer']}_{slugify(rel)}",
            "path": str(rel).replace("\\", "/"),
            "sha_pin": sha256_file(file),
            **node_meta,
            "description": f"{file.stem} ({prefix})",
        }
        nodes.append(node)

    return nodes


def build_index(root: Path, commit_sha: str | None = None) -> dict:
    sha = commit_sha or get_commit_sha(root)

    all_nodes = []
    for prefix, meta in LAYER_MAP.items():
        all_nodes.extend(scan_layer(root, prefix, meta))

    # Foundation ledger
    ledger_path = root / "05_Continuity" / "hashes" / "foundation.sha256.txt"
    validation_path = root / "configs" / "validation_protocol.yaml"

    index = {
        "_meta": {
            "template_version": "1.0",
            "project": root.name,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "commit_sha": sha,
        },
        "nodes": all_nodes,
        "foundation_ledger": {
            "path": "05_Continuity/hashes/foundation.sha256.txt",
            "sha_pin": sha256_file(ledger_path) if ledger_path.exists() else None,
        },
        "validation_protocol": {
            "path": "configs/validation_protocol.yaml",
            "sha_pin": sha256_file(validation_path) if validation_path.exists() else None,
        },
    }
    return index


def main():
    ap = argparse.ArgumentParser(description="Build craig knowledge_index.json")
    ap.add_argument("--root", default=".", help="Project root directory")
    ap.add_argument("--out", default="knowledge_index.json", help="Output file")
    ap.add_argument("--commit-sha", default=None, help="Override commit SHA")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    index = build_index(root, args.commit_sha)

    out_path = root / args.out
    out_path.write_text(json.dumps(index, indent=2), encoding="utf-8")
    print(f"Written: {out_path} ({len(index['nodes'])} nodes)")


if __name__ == "__main__":
    main()
