"""
Craig CODA — core runtime.

Wraps a backend adapter (via DEFAULT_ADAPTER_REGISTRY) with episodic memory retrieval.
Flow per turn:
  1. Retrieve top-k episodic nodes relevant to the user message
  2. Inject them as context into the system prompt
  3. Build a CodaRequest and route generation through the adapter registry
  4. Log retrieval + update resonance bonds
"""
from __future__ import annotations

import uuid
import yaml
from pathlib import Path
from typing import Generator

from src.coda_ir import CodaMessage, CodaRequest

ROOT = Path(__file__).parents[2]


class CodaRuntime:
    def __init__(
        self,
        db_path: Path | None = None,
        system_prompt_path: Path | None = None,
        model: str = "dolphin-llama3",
        cfg_path: Path | None = None,
        top_k: int | None = None,
    ):
        cfg_path = cfg_path or ROOT / "configs" / "episodic.yaml"
        self.cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))

        self.db_path = db_path or ROOT / "artifacts" / "episodic" / "memory.db"
        self.model = model
        self.top_k = top_k or self.cfg.get("top_k", 5)

        # System prompt base
        sp_path = system_prompt_path or ROOT / "exports" / "user_model_package" / "identity_core" / "system_prompt_core.txt"
        self.system_prompt_base = sp_path.read_text(encoding="utf-8").strip() if sp_path.exists() else ""

        # Lazy-loaded episodic components
        self._store = None
        self._session_id = str(uuid.uuid4())
        self._history: list[dict] = []

        # Ensure an adapter is registered for this model.
        self._bootstrap_adapter()

    def _bootstrap_adapter(self) -> None:
        """Register an OllamaAdapter for self.model if not already in the registry."""
        from src.adapters.ollama_adapter import OllamaAdapter
        from src.adapters.registry import DEFAULT_ADAPTER_REGISTRY
        backend_id = f"ollama:{self.model}"
        if backend_id not in DEFAULT_ADAPTER_REGISTRY.list_backends():
            DEFAULT_ADAPTER_REGISTRY.register(OllamaAdapter(self.model))

    # ------------------------------------------------------------------

    @property
    def store(self):
        if self._store is None:
            from src.episodic.store import EpisodicStore
            self._store = EpisodicStore(self.db_path)
        return self._store

    def _retrieve(self, query: str, allowed_frames: list[str] | None = None) -> list:
        from src.episodic.retriever import retrieve
        results = retrieve(
            query=query,
            store=self.store,
            weights=self.cfg["weights"],
            model_name=self.cfg["semantic_model"],
            top_k=self.top_k,
            allowed_frames=allowed_frames,
        )
        return [node for node, _score in results]

    def _build_context_block(self, nodes: list) -> str:
        if not nodes:
            return ""
        lines = ["[MEMORY CONTEXT]"]
        for i, node in enumerate(nodes, 1):
            snippet = node.content[:400].replace("\n", " ").strip()
            if len(node.content) > 400:
                snippet += "..."
            lines.append(
                f"\n[{i}] domain={node.domain} ctx={node.context_tag} "
                f"emotional={node.emotional:.2f}\n{snippet}"
            )
        lines.append("[/MEMORY CONTEXT]")
        return "\n".join(lines)

    def _build_system_prompt(self, context_block: str) -> str:
        parts = [self.system_prompt_base]
        if context_block:
            parts.append("\n" + context_block)
        return "\n".join(p for p in parts if p)

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

        # Retrieve
        nodes = self._retrieve(message, allowed_frames=allowed_frames)
        node_ids = [n.id for n in nodes]

        if show_context and nodes:
            print("\n[retrieved]")
            for n in nodes:
                snippet = n.content[:80].replace("\n", " ")
                print(f"  {n.id[:8]}  {snippet}")
            print()

        # Build system prompt (vault identity + episodic memory context)
        context_block = self._build_context_block(nodes)
        system_prompt = self._build_system_prompt(context_block)

        # Build CodaRequest — vault-compiled system_prompt travels with the request
        history = [CodaMessage(role=m["role"], content=m["content"]) for m in self._history]
        request = CodaRequest(
            message=message,
            system_prompt=system_prompt,
            history=history,
            memory_nodes=[
                {"id": n.id, "domain": n.domain, "content": n.content[:400]}
                for n in nodes
            ],
            target_backend=f"ollama:{self.model}",
        )

        # Route through adapter registry (streaming)
        adapter = DEFAULT_ADAPTER_REGISTRY.get(request.target_backend)
        full_response = []
        for chunk in adapter.stream(request):
            full_response.append(chunk)
            yield chunk

        # Update conversation history
        self._history.append({"role": "user", "content": message})
        self._history.append({"role": "assistant", "content": "".join(full_response)})

        # Log retrieval + update resonance
        if node_ids:
            self.store.log_retrieval(self._session_id, node_ids)
            self.store.update_resonance(node_ids)
            for nid in node_ids:
                self.store.reinforce(nid)

    def reset(self) -> None:
        """Clear conversation history and start a new session ID."""
        self._history = []
        self._session_id = str(uuid.uuid4())
