from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.checkpoint_utils import list_checkpoint_dirs
from src.model_factory import build_model
from src.tokenizer_loader import load_tokenizer


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect tokenizer, model architecture, and checkpoint state.")
    parser.add_argument("--model-config", default=str(ROOT / "configs" / "model_architecture.yaml"))
    parser.add_argument("--train-config", default=str(ROOT / "configs" / "training_scratch.yaml"))
    args = parser.parse_args()

    tokenizer, tokenizer_meta = load_tokenizer()
    model, _, summary = build_model(args.model_config)
    training_cfg = yaml.safe_load(Path(args.train_config).read_text(encoding="utf-8"))
    checkpoint_root = Path(training_cfg["output_dir"])
    if not checkpoint_root.is_absolute():
        checkpoint_root = ROOT / checkpoint_root
    checkpoints = list_checkpoint_dirs(checkpoint_root)

    print(f"Tokenizer path: {tokenizer_meta['tokenizer_dir']}")
    print(f"Vocab size: {tokenizer.vocab_size}")
    print(f"Model name: {summary['model_name']}")
    print(f"Architecture family: {summary['architecture_family']}")
    print(f"Parameter count: {summary['parameter_count']:,}")
    print(f"Context length: {summary['max_position_embeddings']}")
    print(f"Training output dir: {checkpoint_root}")
    print(
        "Training config: "
        f"block_size={training_cfg['block_size']} "
        f"batch_size={training_cfg['batch_size']} "
        f"grad_accum={training_cfg['gradient_accumulation_steps']} "
        f"max_steps={training_cfg['max_steps']}"
    )
    print(f"Checkpoint count: {len(checkpoints)}")
    for path in checkpoints:
        print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
