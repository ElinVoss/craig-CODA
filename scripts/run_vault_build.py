"""
run_vault_build.py — Entry point for the craig-CODA Obsidian story-bible vault builder.

Chains all three build steps:
  1. vault_flatten.py   — walk repo, build node manifest
  2. vault_index.py     — detect connections, build pulse-cell connection graph
  3. vault_generate.py  — render Obsidian vault pages by story_role

Usage:
  python scripts/run_vault_build.py

Output:
  exports/obsidian_vault/   — open this folder as an Obsidian vault
"""

import sys
import time
from pathlib import Path

# Ensure scripts/ is on the path so we can import sibling scripts
sys.path.insert(0, str(Path(__file__).parent))

import vault_flatten
import vault_index
import vault_generate


def main():
    start = time.time()
    print("=" * 60)
    print("craig-CODA Obsidian Story Bible Builder")
    print("=" * 60)

    print("\n[1/3] Flattening repo into node manifest...")
    vault_flatten.main()

    print("\n[2/3] Building semantic connection graph...")
    vault_index.main()

    print("\n[3/3] Generating vault pages...")
    vault_generate.main()

    elapsed = time.time() - start
    vault_dir = Path(__file__).parent.parent / "exports" / "obsidian_vault"
    page_count = sum(1 for _ in vault_dir.rglob("*.md"))

    print(f"\n{'=' * 60}")
    print(f"Done in {elapsed:.1f}s — {page_count} total pages in vault")
    print(f"Open in Obsidian: {vault_dir}")
    print("=" * 60)


if __name__ == "__main__":
    main()
