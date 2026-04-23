from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tokenizers import Tokenizer
from tokenizers.models import BPE, WordLevel
from tokenizers.pre_tokenizers import ByteLevel, Whitespace
from tokenizers.trainers import BpeTrainer, WordLevelTrainer

from src.io_utils import read_text
from src.tokenizer_utils import load_yaml, save_json


def train_tokenizer(config: dict) -> dict:
    training_cfg = config["training"]
    tok_cfg = config["tokenizer"]
    norm_cfg = config["normalization"]
    output_dir = ROOT / training_cfg["output_dir"]
    corpus_path = ROOT / training_cfg["corpus_path"]
    tok_type = tok_cfg["type"].lower()
    special_tokens = list(tok_cfg["special_tokens"])

    if tok_type == "bpe":
        tokenizer = Tokenizer(BPE(unk_token="[UNK]"))
        tokenizer.pre_tokenizer = ByteLevel(add_prefix_space=False)
        trainer = BpeTrainer(
            vocab_size=int(tok_cfg["vocab_size"]),
            min_frequency=int(training_cfg["min_frequency"]),
            special_tokens=special_tokens,
            show_progress=bool(training_cfg.get("show_progress", False)),
        )
    else:
        tokenizer = Tokenizer(WordLevel(unk_token="[UNK]"))
        tokenizer.pre_tokenizer = Whitespace()
        trainer = WordLevelTrainer(
            vocab_size=int(tok_cfg["vocab_size"]),
            min_frequency=int(training_cfg["min_frequency"]),
            special_tokens=special_tokens,
            show_progress=bool(training_cfg.get("show_progress", False)),
        )

    tokenizer.train([str(corpus_path)], trainer)

    output_dir.mkdir(parents=True, exist_ok=True)
    tokenizer_json = output_dir / "tokenizer.json"
    tokenizer.save(str(tokenizer_json))

    tokenizer_config = {
        "tokenizer_type": tok_cfg["type"],
        "vocab_size": int(tok_cfg["vocab_size"]),
        "special_tokens": special_tokens,
        "normalization": dict(norm_cfg),
        "corpus_path": training_cfg["corpus_path"],
    }
    save_json(output_dir / "tokenizer_config.json", tokenizer_config)
    save_json(output_dir / "special_tokens_map.json", {"special_tokens": special_tokens})

    actual_vocab_size = tokenizer.get_vocab_size()
    info = {
        "tokenizer_type": tok_cfg["type"],
        "vocab_size": actual_vocab_size,
        "special_tokens": special_tokens,
        "corpus_source": training_cfg["corpus_path"],
        "training_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "config": {
            "min_frequency": int(training_cfg["min_frequency"]),
            "show_progress": bool(training_cfg.get("show_progress", False)),
        },
        "artifact_files": [
            "tokenizer.json",
            "tokenizer_config.json",
            "special_tokens_map.json",
        ],
    }
    save_json(output_dir / "training_info.json", info)
    return info


def main() -> int:
    parser = argparse.ArgumentParser(description="Train a local tokenizer from the prepared corpus.")
    parser.add_argument("--config", default=str(ROOT / "configs" / "tokenizer.yaml"))
    args = parser.parse_args()

    config = load_yaml(Path(args.config))
    info = train_tokenizer(config)
    print(f"Trained {info['tokenizer_type']} tokenizer with vocab size {info['vocab_size']}")
    print(f"Artifacts written to {ROOT / config['training']['output_dir']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


