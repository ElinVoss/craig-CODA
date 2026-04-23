from __future__ import annotations

from pathlib import Path

import yaml
from transformers import AutoModelForCausalLM, Qwen3Config

from .io_utils import write_json
from .tokenizer_loader import load_tokenizer

ROOT = Path(__file__).resolve().parents[1]


def load_model_architecture_config(config_path: str | Path | None = None) -> dict:
    if config_path is None:
        config_path = ROOT / "configs" / "model_architecture.yaml"
    path = Path(config_path)
    if not path.is_absolute():
        path = ROOT / path
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def resolve_vocab_size(architecture_cfg: dict) -> tuple[int, dict]:
    source = architecture_cfg["vocab_size_source"]
    if source == "tokenizer_artifacts":
        tokenizer, metadata = load_tokenizer(architecture_cfg["tokenizer_dir"])
        return tokenizer.vocab_size, metadata
    vocab_size = architecture_cfg.get("vocab_size")
    if vocab_size is None:
        raise ValueError("vocab_size must be set when vocab_size_source is not tokenizer_artifacts")
    return int(vocab_size), {"tokenizer_dir": None, "vocab_size": int(vocab_size)}


def build_qwen3_config(architecture_cfg: dict, vocab_size: int, tokenizer_metadata: dict) -> Qwen3Config:
    tokenizer, _ = load_tokenizer(architecture_cfg["tokenizer_dir"])
    pad_token_id = tokenizer.convert_tokens_to_ids(architecture_cfg.get("pad_token_fallback", "[PAD]"))
    bos_token_id = tokenizer.convert_tokens_to_ids(architecture_cfg.get("bos_token_fallback", "[BOS]"))
    eos_token_id = tokenizer.convert_tokens_to_ids(architecture_cfg.get("eos_token_fallback", "[EOS]"))

    return Qwen3Config(
        vocab_size=vocab_size,
        hidden_size=int(architecture_cfg["hidden_size"]),
        intermediate_size=int(architecture_cfg["intermediate_size"]),
        num_hidden_layers=int(architecture_cfg["num_hidden_layers"]),
        num_attention_heads=int(architecture_cfg["num_attention_heads"]),
        num_key_value_heads=int(architecture_cfg["num_key_value_heads"]),
        head_dim=int(architecture_cfg["head_dim"]),
        max_position_embeddings=int(architecture_cfg["max_position_embeddings"]),
        hidden_act=str(architecture_cfg["hidden_act"]),
        rms_norm_eps=float(architecture_cfg["rms_norm_eps"]),
        tie_word_embeddings=bool(architecture_cfg["tie_word_embeddings"]),
        attention_dropout=float(architecture_cfg["attention_dropout"]),
        initializer_range=float(architecture_cfg["initializer_range"]),
        use_cache=bool(architecture_cfg["use_cache"]),
        pad_token_id=pad_token_id if pad_token_id >= 0 else None,
        bos_token_id=bos_token_id if bos_token_id >= 0 else None,
        eos_token_id=eos_token_id if eos_token_id >= 0 else None,
    )


def count_parameters(model) -> int:
    return sum(param.numel() for param in model.parameters())


def build_model(config_path: str | Path | None = None):
    architecture_cfg = load_model_architecture_config(config_path)
    vocab_size, tokenizer_metadata = resolve_vocab_size(architecture_cfg)
    hf_config = build_qwen3_config(architecture_cfg, vocab_size, tokenizer_metadata)
    model = AutoModelForCausalLM.from_config(hf_config)
    parameter_count = count_parameters(model)
    summary = {
        "model_name": architecture_cfg["model_name"],
        "architecture_family": architecture_cfg["architecture_family"],
        "vocab_size": vocab_size,
        "hidden_size": architecture_cfg["hidden_size"],
        "intermediate_size": architecture_cfg["intermediate_size"],
        "num_hidden_layers": architecture_cfg["num_hidden_layers"],
        "num_attention_heads": architecture_cfg["num_attention_heads"],
        "num_key_value_heads": architecture_cfg["num_key_value_heads"],
        "head_dim": architecture_cfg["head_dim"],
        "max_position_embeddings": architecture_cfg["max_position_embeddings"],
        "parameter_count": parameter_count,
        "tokenizer_dir": tokenizer_metadata["tokenizer_dir"],
    }
    print(f"Built model '{summary['model_name']}' from random weights")
    print(f"Parameter count: {parameter_count:,}")
    return model, hf_config, summary


def save_model_metadata(summary: dict, config_path: str | Path | None = None) -> Path:
    architecture_cfg = load_model_architecture_config(config_path)
    output_path = Path(architecture_cfg["metadata_output"])
    if not output_path.is_absolute():
        output_path = ROOT / output_path
    write_json(output_path, summary)
    return output_path

