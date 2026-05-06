"""Tests for CODA intermediate representation.

These tests cover CodaRequest, CodaResponse, and the adapter registry
without hitting any real backends. No network or model weights required.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.coda_ir import CodaMessage, CodaRequest, CodaResponse
from src.adapters.registry import AdapterRegistry
from src.adapters.base import BaseAdapter
from typing import Any


# --- helpers -----------------------------------------------------------


def make_request(**kwargs) -> CodaRequest:
    defaults = dict(message="hello", system_prompt="You are Craig.")
    defaults.update(kwargs)
    return CodaRequest(**defaults)


class _EchoAdapter(BaseAdapter):
    """Stub adapter that echoes the message back for testing."""

    @property
    def backend_name(self) -> str:
        return "test:echo"

    @property
    def backend_type(self) -> str:
        return "test"

    def format_request(self, request: CodaRequest) -> Any:
        return request.message

    def parse_response(self, raw: Any, request: CodaRequest) -> CodaResponse:
        return CodaResponse(
            text=str(raw),
            backend_name=self.backend_name,
            request_id=request.request_id,
        )

    def call(self, request: CodaRequest) -> CodaResponse:
        return self.parse_response(self.format_request(request), request)

    def health_check(self) -> bool:
        return True


# --- CodaRequest -------------------------------------------------------


def test_request_has_unique_id():
    r1 = make_request()
    r2 = make_request()
    assert r1.request_id != r2.request_id
    assert len(r1.request_id) > 0


def test_messages_for_api_system_first():
    req = make_request(system_prompt="sys", message="hi")
    msgs = req.messages_for_api()
    assert msgs[0] == {"role": "system", "content": "sys"}
    assert msgs[-1] == {"role": "user", "content": "hi"}


def test_messages_for_api_no_system():
    req = make_request(system_prompt="", message="hi")
    msgs = req.messages_for_api()
    assert msgs[0]["role"] == "user"


def test_messages_for_api_includes_history():
    history = [
        CodaMessage(role="user", content="first"),
        CodaMessage(role="assistant", content="response"),
    ]
    req = make_request(message="second", history=history, system_prompt="")
    msgs = req.messages_for_api()
    assert msgs[0]["role"] == "user"
    assert msgs[0]["content"] == "first"
    assert msgs[1]["role"] == "assistant"
    assert msgs[2]["role"] == "user"
    assert msgs[2]["content"] == "second"


def test_prompt_for_completion_includes_all_parts():
    history = [CodaMessage(role="user", content="q"), CodaMessage(role="assistant", content="a")]
    req = make_request(system_prompt="sys", message="follow-up", history=history)
    prompt = req.prompt_for_completion()
    assert "[System]" in prompt
    assert "sys" in prompt
    assert "User: q" in prompt
    assert "Assistant: a" in prompt
    assert "User: follow-up" in prompt
    assert prompt.endswith("Assistant:")


def test_prompt_for_completion_no_system():
    req = make_request(system_prompt="", message="hi", history=[])
    prompt = req.prompt_for_completion()
    assert "[System]" not in prompt
    assert "User: hi" in prompt


# --- CodaResponse ------------------------------------------------------


def test_response_ok():
    r = CodaResponse(text="hello", backend_name="test:echo")
    assert r.ok is True


def test_response_not_ok_on_error():
    r = CodaResponse(text="", backend_name="test:echo", error="timeout")
    assert r.ok is False


def test_response_defaults():
    r = CodaResponse(text="hi", backend_name="x")
    assert r.vault_profile is None
    assert r.error is None
    assert r.usage == {}


# --- AdapterRegistry ---------------------------------------------------


def test_registry_register_and_get():
    reg = AdapterRegistry()
    adapter = _EchoAdapter()
    reg.register(adapter)
    assert reg.get("test:echo") is adapter


def test_registry_list_backends():
    reg = AdapterRegistry()
    reg.register(_EchoAdapter())
    assert "test:echo" in reg.list_backends()


def test_registry_missing_backend_raises():
    reg = AdapterRegistry()
    try:
        reg.get("nope:model")
        assert False, "Should have raised KeyError"
    except KeyError as e:
        assert "nope:model" in str(e)


def test_registry_health_report():
    reg = AdapterRegistry()
    reg.register(_EchoAdapter())
    report = reg.health_report()
    assert report["test:echo"] is True


# --- BaseAdapter default stream ----------------------------------------


def test_adapter_default_stream():
    adapter = _EchoAdapter()
    req = make_request(message="ping")
    chunks = list(adapter.stream(req))
    assert len(chunks) == 1
    assert chunks[0] == "ping"


# --- round-trip --------------------------------------------------------


def test_echo_adapter_call():
    adapter = _EchoAdapter()
    req = make_request(message="hello world")
    resp = adapter.call(req)
    assert resp.ok
    assert resp.text == "hello world"
    assert resp.request_id == req.request_id
    assert resp.backend_name == "test:echo"


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
            print(f"  FAIL  {fn.__name__}: {exc}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
    if failed:
        sys.exit(1)
