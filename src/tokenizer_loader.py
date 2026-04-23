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
    training_info_path = path / "training_info.json"
    special_tokens_path = path / "special_tokens_map.json"

    missing = [item.name for item in [tokenizer_json, training_info_path, special_tokens_path] if not item.is_file()]
    if missing:
        raise FileNotFoundError(
            "Tokenizer artifacts are missing. Run the phase-three tokenizer pipeline first. "
            f"Missing: {', '.join(missing)}"
        )

    training_info = read_json(training_info_path)
    special_tokens_raw = read_json(special_tokens_path).get("special_tokens", [])
    if not isinstance(special_tokens_raw, list):
        raise ValueError(f"{special_tokens_path}: expected 'special_tokens' list")
    tokenizer = PreTrainedTokenizerFast(
        tokenizer_file=str(tokenizer_json),
        **_build_special_token_kwargs([str(token) for token in special_tokens_raw]),
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

