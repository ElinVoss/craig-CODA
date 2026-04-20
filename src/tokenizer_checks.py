from __future__ import annotations

from pathlib import Path

from tokenizers import Tokenizer


def validate_tokenizer_artifacts(output_dir: Path) -> list[str]:
    required = [
        output_dir / "tokenizer.json",
        output_dir / "tokenizer_config.json",
        output_dir / "special_tokens_map.json",
        output_dir / "training_info.json",
    ]
    missing = [str(path) for path in required if not path.is_file()]
    return missing


def sample_round_trip(tokenizer: Tokenizer, samples: list[str]) -> list[dict]:
    results: list[dict] = []
    for text in samples:
        encoded = tokenizer.encode(text)
        decoded = tokenizer.decode(encoded.ids)
        results.append(
            {
                "text": text,
                "token_count": len(encoded.ids),
                "decoded": decoded,
            }
        )
    return results

