"""
Craig CODA — core runtime.

Wraps a backend adapter (via DEFAULT_ADAPTER_REGISTRY) with the richer runtime
planning path plus the vault graph retrieval lane.

Flow per turn:
  1. Classify the prompt into front matter
  2. Build a response plan (mode, backend, context policy)
  3. Retrieve vault graph nodes + derive graph routing if the plan allows memory context
  4. Compile the vault-governed system prompt with routing + memory context
  5. Build a CodaRequest and route generation through the adapter registry
  6. Reinforce retrieved graph nodes
"""
from __future__ import annotations

from dataclasses import asdict
import uuid
from pathlib import Path
from typing import Any, Generator

from src.coda_ir import CodaMessage, CodaRequest
from src.memory.graph_router import derive_routing
from src.memory.memory_store import load_memory_graph
from src.memory.retrieve_topk import RetrievalResult, retrieve_nodes
from src.memory.update_reinforcement import update_reinforcement
from src.runtime.front_matter_builder import build_prompt_front_matter
from src.runtime.prompt_compiler import compile_mode_prompt
from src.runtime.response_plan_builder import build_response_plan
from src.translation.runtime_context_translator import build_memory_context, render_memory_context

ROOT = Path(__file__).parents[2]
_CANONICAL_BACKEND_PREFIXES = {"ollama", "local", "anthropic", "openai", "groq"}


class CodaRuntime:
    def __init__(
        self,
        db_path: Path | None = None,
        system_prompt_path: Path | None = None,
        model: str = "dolphin-llama3",
        target_backend: str | None = None,
        mode_name: str | None = None,
        front_matter_overrides: dict[str, Any] | None = None,
        generation_params: dict[str, Any] | None = None,
        cfg_path: Path | None = None,
        top_k: int | None = None,
    ):
        # Legacy compatibility only. Retrieval no longer uses the episodic SQLite lane.
        self.db_path = db_path
        self.cfg_path = cfg_path
        self.top_k = top_k
        self.target_backend = self._normalize_target_backend(target_backend or model)
        self.model = self.target_backend.split(":", 1)[1]
        self.mode_name = mode_name
        self.front_matter_overrides = dict(front_matter_overrides or {})
        self.generation_params = dict(generation_params or {})

        # Optional legacy system prompt override. The richer mode prompt now provides
        # the base system prompt; only append this block if an explicit override path
        # was provided and it is not the default identity-core file.
        default_sp_path = ROOT / "exports" / "user_model_package" / "identity_core" / "system_prompt_core.txt"
        self.system_prompt_override = ""
        if system_prompt_path is not None:
            sp_path = system_prompt_path
            if sp_path.exists() and sp_path.resolve() != default_sp_path.resolve():
                self.system_prompt_override = sp_path.read_text(encoding="utf-8").strip()

        self._session_id = str(uuid.uuid4())
        self._history: list[dict] = []

        # Ensure an adapter is registered for this model.
        self._bootstrap_adapter()

    def _normalize_target_backend(self, backend_name: str) -> str:
        prefix, sep, rest = backend_name.partition(":")
        if sep and prefix in _CANONICAL_BACKEND_PREFIXES and rest:
            return backend_name
        return f"ollama:{backend_name}"

    def _bootstrap_adapter(self) -> None:
        """Register the configured adapter if not already in the registry."""
        from src.adapters.anthropic_adapter import AnthropicAdapter
        from src.adapters.local_backend_adapter import LocalBackendAdapter
        from src.adapters.ollama_adapter import OllamaAdapter
        from src.adapters.registry import DEFAULT_ADAPTER_REGISTRY
        backend_id = self.target_backend
        if backend_id not in DEFAULT_ADAPTER_REGISTRY.list_backends():
            backend_type, backend_value = backend_id.split(":", 1)
            if backend_type == "ollama":
                DEFAULT_ADAPTER_REGISTRY.register(OllamaAdapter(backend_value))
            elif backend_type == "local":
                DEFAULT_ADAPTER_REGISTRY.register(LocalBackendAdapter(backend_value))
            elif backend_type == "anthropic":
                DEFAULT_ADAPTER_REGISTRY.register(AnthropicAdapter(backend_value))
            else:
                raise ValueError(f"Unsupported adapter backend type: {backend_type}")

    # ------------------------------------------------------------------

    def _empty_memory_payload(self, retrieval_profile: str) -> dict[str, Any]:
        return {
            "results": [],
            "routing": None,
            "routing_block": "",
            "memory_context": "",
            "injection_text": "",
            "profile_used": retrieval_profile,
            "graph_available": False,
        }

    def _retrieve_memory_payload(
        self,
        query: str,
        retrieval_profile: str,
        mode_name: str,
        top_k: int | None = None,
    ) -> dict[str, Any]:
        try:
            results = retrieve_nodes(
                query=query,
                retrieval_profile=retrieval_profile,
                mode=mode_name,
                top_k=top_k,
            )
            _, edges = load_memory_graph()
        except FileNotFoundError:
            return self._empty_memory_payload(retrieval_profile)

        routing = derive_routing(results, edges, retrieval_profile)
        routing_block = routing.render_routing_block()
        memory_context = render_memory_context(build_memory_context(results)) if results else ""
        injection_parts = [part for part in [routing_block, memory_context] if part]
        return {
            "results": results,
            "routing": routing,
            "routing_block": routing_block,
            "memory_context": memory_context,
            "injection_text": "\n\n".join(injection_parts),
            "profile_used": retrieval_profile,
            "graph_available": True,
        }

    def _apply_system_prompt_override(self, compiled_prompt: str) -> str:
        if not self.system_prompt_override:
            return compiled_prompt
        if not compiled_prompt:
            return f"[legacy_system_prompt_override]\n{self.system_prompt_override}"
        return (
            f"{compiled_prompt}\n\n"
            f"[legacy_system_prompt_override]\n{self.system_prompt_override}"
        )

    def _plan_turn(
        self,
        message: str,
        allowed_frames: list[str] | None = None,
        front_matter_overrides: dict[str, Any] | None = None,
    ) -> tuple[CodaRequest, list, dict[str, Any]]:
        overrides = dict(self.front_matter_overrides)
        overrides.update(front_matter_overrides or {})
        if self.mode_name is not None:
            overrides.setdefault("mode", self.mode_name)
        front_matter = build_prompt_front_matter(
            prompt=message,
            overrides=overrides or None,
        )
        response_plan = build_response_plan(
            front_matter=front_matter,
            backend_name=self.target_backend,
            mode_name=self.mode_name,
            memory_top_k=self.top_k,
        )
        memory_payload = self._empty_memory_payload(response_plan.retrieval_profile)
        if response_plan.include_memory_context:
            memory_payload = self._retrieve_memory_payload(
                message,
                retrieval_profile=response_plan.retrieval_profile,
                mode_name=response_plan.selected_mode,
                top_k=response_plan.memory_top_k,
            )
        results: list[RetrievalResult] = memory_payload["results"]
        context_block = memory_payload["injection_text"] or None
        system_prompt, included_files = compile_mode_prompt(
            mode_name=response_plan.selected_mode,
            include_context=response_plan.include_context,
            include_rs1_specialty=response_plan.include_rs1_specialty,
            include_rs1_creative=response_plan.include_rs1_creative,
            memory_context=context_block,
        )
        system_prompt = self._apply_system_prompt_override(system_prompt)

        history = [CodaMessage(role=m["role"], content=m["content"]) for m in self._history]
        request = CodaRequest(
            message=message,
            system_prompt=system_prompt,
            history=history,
            vault_profile=response_plan.selected_mode,
            vault_directives={
                "front_matter": front_matter.to_dict(),
                "response_plan": response_plan.to_dict(),
                "included_prompt_files": [str(path.relative_to(ROOT)) for path in included_files],
                "allowed_frames": allowed_frames or [],
                "graph_available": memory_payload["graph_available"],
                "graph_profile": memory_payload["profile_used"],
                "routing": asdict(memory_payload["routing"]) if memory_payload["routing"] is not None else None,
                "routing_block": memory_payload["routing_block"],
                "memory_context": memory_payload["memory_context"],
                "legacy_system_prompt_override": bool(self.system_prompt_override),
            },
            memory_nodes=[
                {
                    "id": result.node.id,
                    "trust_layer": result.node.trust_layer,
                    "source_path": result.node.source_path,
                    "summary": result.node.summary,
                    "score": result.total_score,
                    "breakdown": result.breakdown,
                }
                for result in results
            ],
            target_backend=response_plan.selected_backend,
            generation_params=dict(self.generation_params),
            metadata={
                "session_id": self._session_id,
                "runtime_pipeline": "front_matter -> response_plan -> vault_graph -> prompt_compiler -> adapter",
                "retrieved_node_count": len(results),
                "graph_available": memory_payload["graph_available"],
                "graph_profile": memory_payload["profile_used"],
                "legacy_allowed_frames_ignored": bool(allowed_frames),
            },
        )
        plan = {
            "front_matter": front_matter,
            "response_plan": response_plan,
            "included_files": included_files,
            "context_block": context_block or "",
            "memory_payload": memory_payload,
        }
        return request, [result.node for result in results], plan

    # ------------------------------------------------------------------

    def chat(
        self,
        message: str,
        allowed_frames: list[str] | None = None,
        show_context: bool = False,
    ) -> Generator[str, None, None]:
        """
        Send a message. Yields response text chunks as they stream.

        Args:
            message: user input
            allowed_frames: restrict episodic retrieval to specific frames
            show_context: if True, print retrieved node summaries before streaming
        """
        from src.adapters.registry import DEFAULT_ADAPTER_REGISTRY

        request, nodes, _plan = self._plan_turn(
            message=message,
            allowed_frames=allowed_frames,
        )
        node_ids = [n.id for n in nodes]

        if show_context and nodes:
            print("\n[retrieved]")
            for result in _plan["memory_payload"]["results"]:
                snippet = result.node.summary[:80].replace("\n", " ")
                print(
                    f"  {result.node.id[:8]}  {snippet}  "
                    f"score={result.total_score:.3f} trust={result.node.trust_layer}"
                )
            print()

        # Route through adapter registry (streaming)
        adapter = DEFAULT_ADAPTER_REGISTRY.get(request.target_backend)
        full_response = []
        for chunk in adapter.stream(request):
            full_response.append(chunk)
            yield chunk

        # Update conversation history
        self._history.append({"role": "user", "content": message})
        self._history.append({"role": "assistant", "content": "".join(full_response)})

        # Reinforce retrieved graph nodes for later retrieval weighting.
        if node_ids:
            update_reinforcement(node_ids)

    def reset(self) -> None:
        """Clear conversation history and start a new session ID."""
        self._history = []
        self._session_id = str(uuid.uuid4())
