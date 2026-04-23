"""
Usage:
  python scripts/add_memory.py \
    --content "Side bins occur at every 6th position and force 8-foot pallet depth" \
    --domain warehouse \
    --context floor_shift \
    --mood focused \
    --emotional 0.6 \
    --circumstantial 0.8 \
    --phase 0.7
"""
import argparse
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.episodic.node import MemoryNode
from src.episodic.store import EpisodicStore
from src.episodic.encoder import build_composite

ROOT = Path(__file__).parents[1]
cfg = yaml.safe_load((ROOT / "configs/episodic.yaml").read_text())


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--content", required=True)
    p.add_argument("--domain", default="")
    p.add_argument("--context", default="")
    p.add_argument("--mood", default="")
    p.add_argument("--emotional", type=float, default=0.5)
    p.add_argument("--circumstantial", type=float, default=0.5)
    p.add_argument("--phase", type=float, default=0.5)
    args = p.parse_args()

    node = MemoryNode(
        content=args.content,
        domain=args.domain,
        context_tag=args.context,
        mood_tag=args.mood,
        emotional=args.emotional,
        circumstantial=args.circumstantial,
        developmental_phase=args.phase,
    )
    store = EpisodicStore(ROOT / "artifacts/episodic/memory.db")
    vec = build_composite(node, cfg["weights"], cfg["semantic_model"])
    nid = store.add(node, vec)
    print(f"Added: {nid}")


if __name__ == "__main__":
    main()
