from __future__ import annotations

import json
from pathlib import Path

from .backend_types import BackendBase, BackendConfig

_ROOT = Path(__file__).resolve().parents[2]


class Qwen2_5OmniBackend(BackendBase):
    """Text-only local backend for Qwen2.5-Omni checkpoints.

    This backend is intentionally narrower than the full Omni feature set:
    it loads the exact local checkpoint, reuses the local chat template when
    present, disables the talker, and returns text only.

    It does not currently handle image/audio/video inputs. The goal is a
    CPU/local-friendly text path that can participate in the existing local
    backend lane without pretending Omni is a generic AutoModelForCausalLM.
    """

    def __init__(self, config: BackendConfig) -> None:
        self._config = config
        self._model = None
        self._processor = None

    def _resolve_local_dir(self, value: str) -> Path:
        path = Path(value)
        if path.is_absolute():
            return path
        return _ROOT / path

    def _load_chat_template(self, model_dir: Path) -> str | None:
        template_path = model_dir / "chat_template.json"
        if not template_path.exists():
            return None
        data = json.loads(template_path.read_text(encoding="utf-8"))
        template = data.get("chat_template")
        return str(template) if template else None

    def load(self) -> None:
        try:
            from transformers import (
                Qwen2_5OmniForConditionalGeneration,
                Qwen2_5OmniProcessor,
            )
        except ImportError as exc:
            raise ImportError(
                "The 'transformers' package with Qwen2.5-Omni support is required "
                "for Qwen2_5OmniBackend."
            ) from exc

        import torch

        model_dir = self._resolve_local_dir(self._config.model_id_or_local_path)
        tokenizer_dir = self._resolve_local_dir(self._config.tokenizer_path or self._config.model_id_or_local_path)

        if not model_dir.exists() or not model_dir.is_dir():
            raise FileNotFoundError(
                f"[{self._config.backend_name}] Local model path does not exist: {model_dir}"
            )
        if not tokenizer_dir.exists() or not tokenizer_dir.is_dir():
            raise FileNotFoundError(
                f"[{self._config.backend_name}] Local tokenizer path does not exist: {tokenizer_dir}"
            )

        dtype_map = {
            "float32": torch.float32,
            "float16": torch.float16,
            "bfloat16": torch.bfloat16,
        }
        torch_dtype = dtype_map.get(self._config.dtype_preference, torch.float32)

        print(f"[{self._config.backend_name}] Loading Qwen2.5-Omni processor from: {tokenizer_dir}")
        self._processor = Qwen2_5OmniProcessor.from_pretrained(
            str(tokenizer_dir),
            local_files_only=True,
            trust_remote_code=False,
        )
        chat_template = self._load_chat_template(model_dir)
        if chat_template:
            self._processor.chat_template = chat_template

        device = self._config.device_preference or "cpu"
        load_kwargs = {
            "torch_dtype": torch_dtype,
            "local_files_only": True,
            "trust_remote_code": False,
        }
        if device == "auto":
            offload_dir = _ROOT / "artifacts" / "offload" / self._config.backend_name
            offload_dir.mkdir(parents=True, exist_ok=True)
            load_kwargs.update(
                {
                    "device_map": "auto",
                    "low_cpu_mem_usage": True,
                    "offload_folder": str(offload_dir),
                    "offload_state_dict": True,
                }
            )

        print(f"[{self._config.backend_name}] Loading Qwen2.5-Omni model from: {model_dir}")
        print(f"[{self._config.backend_name}] dtype={self._config.dtype_preference}  device={device}")
        self._model = Qwen2_5OmniForConditionalGeneration.from_pretrained(
            str(model_dir),
            **load_kwargs,
        )
        self._model.disable_talker()
        if device != "auto" and hasattr(self._model, "to"):
            self._model.to(device)
        self._model.eval()
        print(f"[{self._config.backend_name}] Model loaded in text-only mode.")

    def generate(self, prompt: str, **kwargs) -> str:
        if not self.is_loaded():
            raise RuntimeError(
                f"[{self._config.backend_name}] Backend not loaded. Call load() first."
            )

        defaults = self._config.generation_defaults or {}
        temperature = float(kwargs.get("temperature", defaults.get("temperature", 0.2)))
        top_p = float(kwargs.get("top_p", defaults.get("top_p", 0.9)))
        repetition_penalty = float(kwargs.get("repetition_penalty", defaults.get("repetition_penalty", 1.05)))
        max_new_tokens = int(kwargs.get("max_new_tokens", defaults.get("max_new_tokens", 128)))

        conversation = [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}],
            }
        ]
        rendered = self._processor.apply_chat_template(
            conversation,
            add_generation_prompt=True,
            tokenize=False,
        )
        inputs = self._processor(text=rendered, return_tensors="pt", padding=True)

        device = self._config.device_preference or "cpu"
        if device != "auto":
            inputs = {
                key: value.to(device) if hasattr(value, "to") else value
                for key, value in inputs.items()
            }

        output_ids = self._model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=temperature > 0,
            temperature=temperature if temperature > 0 else 1.0,
            top_p=top_p,
            repetition_penalty=repetition_penalty,
            return_audio=False,
        )

        prompt_len = inputs["input_ids"].shape[1]
        new_ids = output_ids[0][prompt_len:]
        decoded = self._processor.batch_decode(
            [new_ids],
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False,
        )
        return decoded[0] if decoded else ""

    def is_loaded(self) -> bool:
        return self._model is not None and self._processor is not None

    def backend_name(self) -> str:
        return self._config.backend_name
