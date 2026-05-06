"""Tests for the dedicated Qwen2.5-Omni local backend.

These tests avoid real weight loads. They verify:
- backend type registration
- load_backend() selecting the right backend class
- text-only load path wiring (processor + disable_talker)
- generation stripping prompt echo and using the local chat template
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

import yaml

from src.model_backends.load_backend import load_backend


def _write_cfg(path: Path) -> None:
    payload = {
        "backends": [
            {
                "backend_name": "qwen2.5-omni-7b-text",
                "enabled": False,
                "backend_type": "qwen2_5_omni",
                "model_family": "qwen2.5-omni",
                "model_id_or_local_path": "D:/fake-qwen",
                "tokenizer_path": None,
                "quant_format": None,
                "device_preference": "cpu",
                "dtype_preference": "bfloat16",
                "max_context_length": 32768,
                "generation_defaults": {
                    "temperature": 0.2,
                    "top_p": 0.9,
                    "repetition_penalty": 1.05,
                    "max_new_tokens": 64,
                },
                "role": "comparison_only",
                "notes": "test config",
            }
        ]
    }
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def test_qwen_omni_backend_type_registered():
    from src.model_backends.backend_registry import DEFAULT_REGISTRY

    assert "qwen2_5_omni" in DEFAULT_REGISTRY.list_registered()


def test_load_backend_returns_qwen_omni_backend():
    from src.model_backends.qwen2_5_omni_backend import Qwen2_5OmniBackend

    with tempfile.TemporaryDirectory() as tmp:
        cfg_path = Path(tmp) / "pretrained_backends.yaml"
        _write_cfg(cfg_path)
        backend = load_backend("qwen2.5-omni-7b-text", cfg_path=cfg_path)
        assert isinstance(backend, Qwen2_5OmniBackend)
        assert backend.backend_name() == "qwen2.5-omni-7b-text"


class _FakeTensor:
    def __init__(self, values):
        self.values = values
        self.shape = (1, len(values[0]))

    def to(self, *_args, **_kwargs):
        return self

    def __getitem__(self, idx):
        if isinstance(idx, tuple):
            row, col_slice = idx
            if row != 0:
                raise IndexError(row)
            sliced = self.values[0][col_slice]
            return sliced
        return self.values[idx]


class _FakeProcessor:
    def __init__(self):
        self.chat_template = None
        self.last_template_input = None
        self.last_text_input = None

    @classmethod
    def from_pretrained(cls, *_args, **_kwargs):
        return cls()

    def apply_chat_template(self, conversation, add_generation_prompt=True, tokenize=False):
        self.last_template_input = {
            "conversation": conversation,
            "add_generation_prompt": add_generation_prompt,
            "tokenize": tokenize,
        }
        return f"TEMPLATE::{conversation[0]['content'][0]['text']}"

    def __call__(self, text, return_tensors="pt", padding=True):
        self.last_text_input = {
            "text": text,
            "return_tensors": return_tensors,
            "padding": padding,
        }
        return {
            "input_ids": _FakeTensor([[11, 12, 13]]),
            "attention_mask": _FakeTensor([[1, 1, 1]]),
        }

    def batch_decode(self, token_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False):
        return ["decoded text"]


class _FakeModel:
    def __init__(self):
        self.disable_talker_called = False
        self.eval_called = False
        self.device = "cpu"
        self.last_generate_kwargs = None

    @classmethod
    def from_pretrained(cls, *_args, **_kwargs):
        model = cls()
        model.from_pretrained_kwargs = _kwargs
        return model

    def disable_talker(self):
        self.disable_talker_called = True

    def to(self, device):
        self.device = device
        return self

    def eval(self):
        self.eval_called = True

    def generate(self, **kwargs):
        self.last_generate_kwargs = kwargs
        return _FakeTensor([[11, 12, 13, 21, 22]])


def test_qwen_omni_load_uses_processor_template_and_disables_talker():
    from src.model_backends.qwen2_5_omni_backend import Qwen2_5OmniBackend
    from src.model_backends.backend_types import BackendConfig

    fake_transformers = type(
        "FakeTransformers",
        (),
        {
            "Qwen2_5OmniForConditionalGeneration": _FakeModel,
            "Qwen2_5OmniProcessor": _FakeProcessor,
        },
    )

    original = sys.modules.get("transformers")
    sys.modules["transformers"] = fake_transformers
    try:
        with tempfile.TemporaryDirectory() as tmp:
            model_root = Path(tmp) / "qwen"
            model_root.mkdir()
            (model_root / "chat_template.json").write_text(
                json.dumps({"chat_template": "LOCAL_TEMPLATE"}),
                encoding="utf-8",
            )
            cfg = BackendConfig(
                backend_name="qwen2.5-omni-7b-text",
                enabled=False,
                backend_type="qwen2_5_omni",
                model_family="qwen2.5-omni",
                model_id_or_local_path=str(model_root),
                tokenizer_path=None,
                device_preference="cpu",
                dtype_preference="bfloat16",
                max_context_length=32768,
                generation_defaults={},
                role="comparison_only",
                notes="",
            )
            backend = Qwen2_5OmniBackend(cfg)
            backend.load()

            assert backend.is_loaded() is True
            assert backend._processor.chat_template == "LOCAL_TEMPLATE"
            assert backend._model.disable_talker_called is True
            assert backend._model.eval_called is True
        assert True
    finally:
        if original is None:
            del sys.modules["transformers"]
        else:
            sys.modules["transformers"] = original


def test_qwen_omni_generate_renders_template_and_strips_prompt_echo():
    from src.model_backends.qwen2_5_omni_backend import Qwen2_5OmniBackend
    from src.model_backends.backend_types import BackendConfig

    fake_transformers = type(
        "FakeTransformers",
        (),
        {
            "Qwen2_5OmniForConditionalGeneration": _FakeModel,
            "Qwen2_5OmniProcessor": _FakeProcessor,
        },
    )

    original = sys.modules.get("transformers")
    sys.modules["transformers"] = fake_transformers
    try:
        with tempfile.TemporaryDirectory() as tmp:
            model_root = Path(tmp) / "qwen"
            model_root.mkdir()
            (model_root / "chat_template.json").write_text(
                json.dumps({"chat_template": "LOCAL_TEMPLATE"}),
                encoding="utf-8",
            )
            cfg = BackendConfig(
                backend_name="qwen2.5-omni-7b-text",
                enabled=False,
                backend_type="qwen2_5_omni",
                model_family="qwen2.5-omni",
                model_id_or_local_path=str(model_root),
                tokenizer_path=None,
                device_preference="cpu",
                dtype_preference="bfloat16",
                max_context_length=32768,
                generation_defaults={"max_new_tokens": 64, "temperature": 0.2},
                role="comparison_only",
                notes="",
            )
            backend = Qwen2_5OmniBackend(cfg)
            backend.load()

            text = backend.generate("Explain this.", max_new_tokens=12, temperature=0.0)
            assert text == "decoded text"
            assert backend._processor.last_template_input["conversation"][0]["content"][0]["text"] == "Explain this."
            assert backend._model.last_generate_kwargs["return_audio"] is False
            assert backend._model.last_generate_kwargs["max_new_tokens"] == 12
        assert True
    finally:
        if original is None:
            del sys.modules["transformers"]
        else:
            sys.modules["transformers"] = original


if __name__ == "__main__":
    tests = [v for k, v in list(globals().items()) if k.startswith("test_")]
    passed = 0
    failed = 0
    for fn in tests:
        try:
            fn()
            print(f"  PASS  {fn.__name__}")
            passed += 1
        except Exception as exc:
            import traceback
            print(f"  FAIL  {fn.__name__}: {exc}")
            traceback.print_exc()
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
    if failed:
        sys.exit(1)
