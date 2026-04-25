from __future__ import annotations

from pathlib import Path

from .backend_types import BackendBase, BackendConfig

# Root of the repo, resolved relative to this file's location.
_ROOT = Path(__file__).resolve().parents[2]


class ScratchBackend(BackendBase):
    """Backend wrapping the existing scratch (random-init) model path.

    This backend builds the model via src.model_factory.build_model() using
    the random-initialization Qwen3-style architecture. It does NOT load
    pretrained weights. Output is random-init noise — this is expected and
    correct. Do not treat its output as meaningful text.

    The model is NOT loaded at construction time. Call load() before generate().
    """

    def __init__(self, config: BackendConfig) -> None:
        self._config = config
        self._model = None
        self._tokenizer = None

    def load(self) -> None:
        """Build the scratch model via model_factory and load the tokenizer."""
        print(
            f"[{self._config.backend_name}] Loading scratch (random-init) model. "
            "Output will be noise — this is expected."
        )
        from src.model_factory import build_model
        from src.tokenizer_loader import load_tokenizer

        tokenizer_dir = self._config.tokenizer_path or self._config.model_id_or_local_path
        tokenizer_path = Path(tokenizer_dir)
        if not tokenizer_path.is_absolute():
            tokenizer_path = _ROOT / tokenizer_path

        if not tokenizer_path.exists():
            raise FileNotFoundError(
                f"[{self._config.backend_name}] Tokenizer directory not found: {tokenizer_path}\n"
                "Run the tokenizer pipeline first: python scripts/run_tokenizer_pipeline.py"
            )

        self._tokenizer, _ = load_tokenizer(tokenizer_path)
        self._model, _hf_config, summary = build_model()
        print(
            f"[{self._config.backend_name}] Scratch model built: {summary['model_name']}  "
            f"params={summary['parameter_count']:,}"
        )

        import torch
        self._model.to(torch.device("cpu"))
        self._model.eval()

    def generate(self, prompt: str, **kwargs) -> str:
        """Greedy decode from the scratch model. Output is random-init noise."""
        if not self.is_loaded():
            raise RuntimeError(
                f"[{self._config.backend_name}] Backend not loaded. Call load() first."
            )

        import torch

        defaults = self._config.generation_defaults or {}
        max_new_tokens = int(kwargs.get("max_new_tokens", defaults.get("max_new_tokens", 64)))

        encoded = self._tokenizer(prompt, return_tensors="pt")
        input_ids = encoded["input_ids"]
        attention_mask = encoded.get("attention_mask")

        with torch.no_grad():
            output_ids = self._model.generate(
                input_ids=input_ids,
                attention_mask=attention_mask,
                max_new_tokens=max_new_tokens,
                do_sample=False,  # greedy for reproducibility
                pad_token_id=(
                    self._tokenizer.pad_token_id
                    or self._tokenizer.eos_token_id
                ),
                eos_token_id=self._tokenizer.eos_token_id,
            )

        # Return only the new tokens, not the echoed prompt.
        prompt_len = input_ids.shape[1]
        new_ids = output_ids[0][prompt_len:]
        return self._tokenizer.decode(new_ids, skip_special_tokens=True)

    def is_loaded(self) -> bool:
        return self._model is not None and self._tokenizer is not None

    def backend_name(self) -> str:
        return self._config.backend_name
