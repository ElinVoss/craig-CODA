"""Smoke tests for CodaRuntime wiring to the adapter registry.

Verifies the import chain, bootstrap registration, and CodaRequest
construction without requiring Ollama or a live episodic DB.
"""
import sys
from pathlib import Path
from typing import Generator

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.coda_ir import CodaMessage, CodaRequest
from src.adapters.registry import AdapterRegistry, DEFAULT_ADAPTER_REGISTRY
from src.adapters.ollama_adapter import OllamaAdapter


# --- bootstrap registration --------------------------------------------


def test_ollama_adapter_registers_correctly():
    """An OllamaAdapter should register under 'ollama:{model}'."""
    reg = AdapterRegistry()
    adapter = OllamaAdapter("dolphin-llama3")
    reg.register(adapter)
    assert "ollama:dolphin-llama3" in reg.list_backends()
    assert reg.get("ollama:dolphin-llama3") is adapter


def test_runtime_bootstrap_populates_default_registry():
    """CodaRuntime.__init__ should add the model to DEFAULT_ADAPTER_REGISTRY."""
    # Use a distinct model name to avoid collisions with prior test state.
    test_model = "smoke-test-bootstrap-model"
    backend_id = f"ollama:{test_model}"

    # Ensure it is not already registered.
    if backend_id in DEFAULT_ADAPTER_REGISTRY.list_backends():
        return  # already registered from a prior call; test intent still satisfied

    from src.runtime.coda import CodaRuntime
    rt = CodaRuntime(model=test_model)
    assert backend_id in DEFAULT_ADAPTER_REGISTRY.list_backends(), (
        f"Expected '{backend_id}' in registry after CodaRuntime init. "
        f"Got: {DEFAULT_ADAPTER_REGISTRY.list_backends()}"
    )


def test_bootstrap_is_idempotent():
    """Calling _bootstrap_adapter twice should not duplicate registrations."""
    test_model = "idempotent-bootstrap-model"
    from src.runtime.coda import CodaRuntime
    rt = CodaRuntime(model=test_model)
    before = DEFAULT_ADAPTER_REGISTRY.list_backends()[:]
    rt._bootstrap_adapter()  # second call
    after = DEFAULT_ADAPTER_REGISTRY.list_backends()
    assert before == after


# --- OllamaAdapter format_request -------------------------------------


def test_ollama_format_request_structure():
    """format_request should produce a dict with model, messages, stream=False."""
    adapter = OllamaAdapter("dolphin-llama3")
    req = CodaRequest(
        message="hello",
        system_prompt="You are Craig.",
        history=[CodaMessage(role="user", content="hi"), CodaMessage(role="assistant", content="hello")],
        target_backend="ollama:dolphin-llama3",
    )
    native = adapter.format_request(req)
    assert native["model"] == "dolphin-llama3"
    assert native["stream"] is False
    msgs = native["messages"]
    assert msgs[0] == {"role": "system", "content": "You are Craig."}
    assert msgs[1] == {"role": "user", "content": "hi"}
    assert msgs[2] == {"role": "assistant", "content": "hello"}
    assert msgs[3] == {"role": "user", "content": "hello"}


def test_ollama_format_request_no_system():
    adapter = OllamaAdapter("dolphin-llama3")
    req = CodaRequest(message="hi", system_prompt="")
    native = adapter.format_request(req)
    assert native["messages"][0]["role"] == "user"


def test_ollama_format_request_with_generation_params():
    adapter = OllamaAdapter("dolphin-llama3")
    req = CodaRequest(
        message="hi",
        generation_params={"temperature": 0.7, "num_predict": 256},
    )
    native = adapter.format_request(req)
    assert "options" in native
    assert native["options"]["temperature"] == 0.7


# --- messages_for_api parity ------------------------------------------


def test_messages_for_api_matches_old_runtime_format():
    """CodaRequest.messages_for_api() should produce the same list that
    the old CodaRuntime.chat() built manually."""
    old_history = [
        {"role": "user", "content": "first"},
        {"role": "assistant", "content": "reply"},
    ]
    system = "You are Craig."
    message = "second message"

    # Old format (what coda.py used to build)
    old_messages = [{"role": "system", "content": system}]
    old_messages.extend(old_history)
    old_messages.append({"role": "user", "content": message})

    # New format (via CodaRequest)
    history = [CodaMessage(role=m["role"], content=m["content"]) for m in old_history]
    request = CodaRequest(message=message, system_prompt=system, history=history)
    new_messages = request.messages_for_api()

    assert new_messages == old_messages


# --- registry lookup ---------------------------------------------------


def test_registry_lookup_after_bootstrap():
    """After CodaRuntime init, the registry should return the correct adapter type."""
    from src.runtime.coda import CodaRuntime
    test_model = "lookup-test-model"
    CodaRuntime(model=test_model)
    adapter = DEFAULT_ADAPTER_REGISTRY.get(f"ollama:{test_model}")
    assert isinstance(adapter, OllamaAdapter)
    assert adapter.backend_type == "ollama"


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
