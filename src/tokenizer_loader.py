from __future__ import annotations

from pathlib import Path

from transformers import PreTrainedTokenizerFast

from .io_utils import read_json

ROOT = Path(__file__).resolve().parents[1]

TOKEN_ROLE_KEYS = {
    "pad_token": "[PAD]",
    "unk_token": "[UNK]",
    "bos_token": "[BOS]",
    "eos_token": "[EOS]",
    "cls_token": "[CLS]",
    "sep_token": "[SEP]",
    "mask_token": "[MASK]",
}


def _resolve_tokenizer_dir(tokenizer_dir: str | Path | None = None) -> Path:
    if tokenizer_dir is None:
        tokenizer_dir = ROOT / "artifacts" / "tokenizers" / "default"
    path = Path(tokenizer_dir)
    if not path.is_absolute():
        path = ROOT / path
    return path


def _build_special_token_kwargs(tokens: list[str]) -> dict[str, str]:
    kwargs: dict[str, str] = {}
    available = set(tokens)
    for key, token in TOKEN_ROLE_KEYS.items():
        if token in available:
            kwargs[key] = token
    return kwargs


def load_tokenizer(tokenizer_dir: str | Path | None = None) -> tuple[PreTrainedTokenizerFast, dict]:
    path = _resolve_tokenizer_dir(tokenizer_dir)
    tokenizer_json = path / "tokenizer.json"

    if not tokenizer_json.is_file():
        raise FileNotFoundError(
            "tokenizer.json not found. Run the phase-three tokenizer pipeline first "
            f"or fetch a reference tokenizer. Expected at: {tokenizer_json}"
        )

    # training_info.json — present in pipeline-trained tokenizers, absent in reference ones
    training_info_path = path / "training_info.json"
    training_info = read_json(training_info_path) if training_info_path.is_file() else {}

    # special tokens — prefer special_tokens_map.json, fall back to tokenizer_config.json
    special_tokens_raw: list[str] = []
    special_tokens_path = path / "special_tokens_map.json"
    tokenizer_config_path = path / "tokenizer_config.json"

    if special_tokens_path.is_file():
        special_tokens_raw = read_json(special_tokens_path).get("special_tokens", [])
        if not isinstance(special_tokens_raw, list):
            raise ValueError(f"{special_tokens_path}: expected 'special_tokens' list")
    elif tokenizer_config_path.is_file():
        cfg = read_json(tokenizer_config_path)
        special_tokens_raw = [
            v["content"]
            for v in cfg.get("added_tokens_decoder", {}).values()
            if v.get("special", False)
        ]

    tokenizer = PreTrainedTokenizerFast(
        tokenizer_file=str(tokenizer_json),
        **_build_special_token_kwargs([str(t) for t in special_tokens_raw]),
    )
    vocab_size = tokenizer.vocab_size
    metadata = {
        "tokenizer_dir": str(path),
        "tokenizer_json": str(tokenizer_json),
        "vocab_size": vocab_size,
        "training_info": training_info,
        "special_tokens": list(special_tokens_raw),
    }
    print(f"Loaded tokenizer from {path}")
    print(f"Tokenizer vocab size: {vocab_size}")
    return tokenizer, metadata

