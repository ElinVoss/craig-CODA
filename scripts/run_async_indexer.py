"""
Run the vault async indexer.

Usage:
    python scripts/run_async_indexer.py               # daemon (Ctrl+C to stop)
    python scripts/run_async_indexer.py --once        # single pass then exit
    python scripts/run_async_indexer.py --config path/to/async_indexing.yaml
"""

import argparse
import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from memory.async_indexer import VaultIndexer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Vault async indexer")
    parser.add_argument("--config", default="configs/async_indexing.yaml")
    parser.add_argument("--once", action="store_true", help="Single pass then exit")
    args = parser.parse_args()

    config_path = ROOT / args.config
    indexer = VaultIndexer(config_path)

    if args.once:
        n = indexer.run_once()
        print(f"Done — {n} new embeddings written")
        return

    indexer.start()
    try:
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        indexer.stop()


if __name__ == "__main__":
    main()
