"""
Download Qwen3-0.6B tokenizer files only (no weights) from HuggingFace.
Saves to artifacts/tokenizers/qwen3/

Usage:
    python scripts/fetch_qwen_tokenizer.py
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT))

REPO_ID = "Qwen/Qwen3-0.6B"
OUTPUT_DIR = ROOT / "artifacts" / "tokenizers" / "qwen3"

TOKENIZER_FILES = [
    "tokenizer.json",
    "tokenizer_config.json",
    "special_tokens_map.json",
    "vocab.json",
    "merges.txt",
]


def main():
    from huggingface_hub import hf_hub_download

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Fetching tokenizer from {REPO_ID}")
    print(f"Destination: {OUTPUT_DIR}\n")

    for filename in TOKENIZER_FILES:
        try:
            path = hf_hub_download(
                repo_id=REPO_ID,
                filename=filename,
                local_dir=str(OUTPUT_DIR),
            )
            size = Path(path).stat().st_size
            print(f"  OK  {filename}  ({size:,} bytes)")
        except Exception as e:
            # vocab.json and merges.txt may not exist for tiktoken-based models
            print(f"  --  {filename}  (not found — skipping)")

    print(f"\nDone. Tokenizer files at: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
