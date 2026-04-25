from __future__ import annotations

from pathlib import Path

from .backend_types import BackendBase, BackendConfig


class PretrainedTransformersBackend(BackendBase):
    """HuggingFace transformers backend for local pretrained open-weight models.

    Uses AutoModelForCausalLM and AutoTokenizer. Loads in float32 by default
    for CPU-first compatibility. If model_id_or_local_path is a local directory
    that exists, sets local_files_only=True to prevent any network calls.

    The model is NOT loaded at construction time. Call load() before generate().
    """

    def __init__(self, config: BackendConfig) -> None:
        self._config = config
        self._model = None
        self._tokenizer = None

    def load(self) -> None:
        """Load tokenizer and model weights.

        Raises FileNotFoundError if a local path is specified but does not exist.
        Raises ImportError if the transformers package is not installed.
        """
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer
        except ImportError as exc:
            raise ImportError(
                "The 'transformers' package is required for PretrainedTransformersBackend. "
                "Install it with: pip install transformers"
            ) from exc

        model_path = self._config.model_id_or_local_path
        tokenizer_path = self._config.tokenizer_path or model_path

        # Determine if this is a local path
        local_path = Path(model_path)
        is_local = local_path.exists() and local_path.is_dir()

        if not is_local and "/" not in model_path and "\\" not in model_path:
            # Short HF hub ID — treat as remote (not a local path)
            is_local = False
        elif not is_local:
            # Looks like a local path but does not exist
            raise FileNotFoundError(
                f"[{self._config.backend_name}] Local model path does not exist: {model_path}\n"
                "Download the model weights and place them at the configured path, "
                "or set enabled: false in configs/pretrained_backends.yaml."
            )

        print(f"[{self._config.backend_name}] Loading tokenizer from: {tokenizer_path}")
        self._tokenizer = AutoTokenizer.from_pretrained(
            tokenizer_path,
            local_files_only=is_local,
            trust_remote_code=False,
        )

        print(f"[{self._config.backend_name}] Loading model from: {model_path}")
        print(f"[{self._config.backend_name}] dtype={self._config.dtype_preference}  device={self._config.device_preference}")

        import torch
        dtype_map = {
            "float32": torch.float32,
            "float16": torch.float16,
            "bfloat16": torch.bfloat16,
        }
        torch_dtype = dtype_map.get(self._config.dtype_preference, torch.float32)

        self._model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch_dtype,
            local_files_only=is_local,
            trust_remote_code=False,
        )
        device = self._config.device_preference or "cpu"
        self._model.to(device)
        self._model.eval()
        print(f"[{self._config.backend_name}] Model loaded and ready on {device}.")

    def generate(self, prompt: str, **kwargs) -> str:
        """Tokenize prompt, generate, decode. Returns generated text only (no prompt echo)."""
        if not self.is_loaded():
            raise RuntimeError(
                f"[{self._config.backend_name}] Backend not loaded. Call load() first."
            )

        import torch

        defaults = self._config.generation_defaults or {}
        temperature = float(kwargs.get("temperature", defaults.get("temperature", 0.7)))
        top_p = float(kwargs.get("top_p", defaults.get("top_p", 0.9)))
        repetition_penalty = float(kwargs.get("repetition_penalty", defaults.get("repetition_penalty", 1.1)))
        max_new_tokens = int(kwargs.get("max_new_tokens", defaults.get("max_new_tokens", 256)))

        encoded = self._tokenizer(prompt, return_tensors="pt")
        device = self._config.device_preference or "cpu"
        input_ids = encoded["input_ids"].to(device)
        attention_mask = encoded.get("attention_mask")
        if attention_mask is not None:
            attention_mask = attention_mask.to(device)

        with torch.no_grad():
            output_ids = self._model.generate(
                input_ids=input_ids,
                attention_mask=attention_mask,
                max_new_tokens=max_new_tokens,
                do_sample=temperature > 0,
                temperature=temperature if temperature > 0 else 1.0,
                top_p=top_p,
                repetition_penalty=repetition_penalty,
                pad_token_id=(
                    self._tokenizer.pad_token_id
                    or self._tokenizer.eos_token_id
                ),
                eos_token_id=self._tokenizer.eos_token_id,
            )

        # Decode only the newly generated tokens (strip prompt echo)
        prompt_len = input_ids.shape[1]
        new_ids = output_ids[0][prompt_len:]
        return self._tokenizer.decode(new_ids, skip_special_tokens=True)

    def is_loaded(self) -> bool:
        return self._model is not None and self._tokenizer is not None

    def backend_name(self) -> str:
        return self._config.backend_name
