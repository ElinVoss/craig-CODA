"""Smoke tests for CodaRuntime wiring to the adapter registry.

Verifies the import chain, bootstrap registration, and CodaRequest
construction without requiring Ollama or a live vault graph.
"""
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.coda_ir import CodaMessage, CodaRequest, CodaResponse
from src.adapters.base import BaseAdapter
from src.adapters.registry import AdapterRegistry, DEFAULT_ADAPTER_REGISTRY
from src.adapters.ollama_adapter import OllamaAdapter


# --- helpers -----------------------------------------------------------


class _CaptureAdapter(BaseAdapter):
    def __init__(self, backend_name: str) -> None:
        self._backend_name = backend_name
        self.seen_request: CodaRequest | None = None

    @property
    def backend_name(self) -> str:
        return self._backend_name

    @property
    def backend_type(self) -> str:
        return self._backend_name.split(":", 1)[0]

    def format_request(self, request: CodaRequest):
        return request

    def parse_response(self, raw, request: CodaRequest) -> CodaResponse:
        return CodaResponse(
            text=str(raw),
            backend_name=self.backend_name,
            request_id=request.request_id,
            vault_profile=request.vault_profile,
        )

    def call(self, request: CodaRequest) -> CodaResponse:
        self.seen_request = request
        return self.parse_response("ok", request)

    def stream(self, request: CodaRequest):
        self.seen_request = request
        yield "ok"

    def health_check(self) -> bool:
        return True


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


def test_runtime_bootstrap_populates_local_adapter_registry():
    """A canonical local backend id should register a LocalBackendAdapter lazily."""
    backend_id = "local:qwen2.5-1.5b-instruct"
    if backend_id in DEFAULT_ADAPTER_REGISTRY.list_backends():
        return

    from src.runtime.coda import CodaRuntime
    CodaRuntime(target_backend=backend_id)
    assert backend_id in DEFAULT_ADAPTER_REGISTRY.list_backends()


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


def test_runtime_plan_builds_vault_governed_request():
    """_plan_turn should compile prompt files and attach runtime provenance."""
    from src.runtime.coda import CodaRuntime

    backend_id = "ollama:planned-model"
    rt = CodaRuntime(target_backend=backend_id)
    rt._retrieve_memory_payload = lambda *args, **kwargs: rt._empty_memory_payload("technical")

    request, nodes, plan = rt._plan_turn("Explain the current runtime path.")

    assert nodes == []
    assert request.target_backend == backend_id
    assert request.vault_profile == plan["response_plan"].selected_mode
    assert request.vault_directives["response_plan"]["selected_backend"] == backend_id
    assert request.vault_directives["included_prompt_files"]
    assert "[system_prompt_core.txt]" in request.system_prompt
    assert request.metadata["runtime_pipeline"].startswith("front_matter")


def test_runtime_chat_includes_memory_context_in_compiled_prompt():
    """chat() should pass compiled memory context through the adapter request."""
    import src.runtime.coda as coda_module
    from src.runtime.coda import CodaRuntime

    backend_id = "ollama:memory-capture-model"
    rt = CodaRuntime(
        target_backend=backend_id,
        front_matter_overrides={"memory_scope": "scoped"},
    )
    rt._retrieve_memory_payload = lambda *args, **kwargs: {
        "results": [
            SimpleNamespace(
                node=SimpleNamespace(
                    id="node-1",
                    trust_layer="project_constraints",
                    source_path="exports/user_model_package/project_constraints/runtime.yaml",
                    summary="Important runtime memory note.",
                ),
                total_score=0.91,
                breakdown={"semantic": 0.88},
            )
        ],
        "routing": None,
        "routing_block": "[GRAPH ROUTING]\nResponse mode: synthesize\n[/GRAPH ROUTING]",
        "memory_context": "Memory Context:\n- [Constraint] Important runtime memory note.",
        "injection_text": (
            "[GRAPH ROUTING]\nResponse mode: synthesize\n[/GRAPH ROUTING]\n\n"
            "Memory Context:\n- [Constraint] Important runtime memory note."
        ),
        "profile_used": "technical",
        "graph_available": True,
    }

    capture = _CaptureAdapter(backend_id)
    DEFAULT_ADAPTER_REGISTRY.register(capture)

    original_update = coda_module.update_reinforcement
    coda_module.update_reinforcement = lambda node_ids: None
    try:
        chunks = list(rt.chat("Use the saved runtime memory note."))
    finally:
        coda_module.update_reinforcement = original_update

    assert chunks == ["ok"]
    assert capture.seen_request is not None
    assert "[memory_context]" in capture.seen_request.system_prompt
    assert "[GRAPH ROUTING]" in capture.seen_request.system_prompt
    assert "Memory Context:" in capture.seen_request.system_prompt
    assert capture.seen_request.memory_nodes[0]["id"] == "node-1"
    assert capture.seen_request.vault_directives["response_plan"]["selected_backend"] == backend_id
    assert capture.seen_request.metadata["graph_available"] is True


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
