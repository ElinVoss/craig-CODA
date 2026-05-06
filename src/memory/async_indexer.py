"""
Async background indexer: enriches vault nodes with semantic embeddings
via Ollama at http://192.168.4.25:11434.

Runs as a daemon thread. Polls nodes.jsonl for un-embedded nodes,
calls Ollama /api/embeddings, writes results to artifacts/vault/embeddings.jsonl.

The sidecar (embeddings.jsonl) is separate from nodes.jsonl — keeps the
vault graph clean and lets the indexer write without touching graph state.
"""

from __future__ import annotations

import json
import logging
import threading
import time
from pathlib import Path

import requests
import yaml

logger = logging.getLogger(__name__)


def _load_nodes(nodes_path: Path) -> dict[str, dict]:
    nodes: dict[str, dict] = {}
    if not nodes_path.exists():
        return nodes
    with open(nodes_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                node = json.loads(line)
                if "id" in node:
                    nodes[node["id"]] = node
            except json.JSONDecodeError:
                continue
    return nodes


def load_embeddings(embed_path: Path) -> dict[str, list[float]]:
    embeddings: dict[str, list[float]] = {}
    if not embed_path.exists():
        return embeddings
    with open(embed_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
                if "id" in rec and "embedding" in rec:
                    embeddings[rec["id"]] = rec["embedding"]
            except json.JSONDecodeError:
                continue
    return embeddings


def _save_embeddings(embed_path: Path, embeddings: dict[str, list[float]]) -> None:
    """Atomic write: temp file then rename."""
    embed_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = embed_path.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        for node_id, vector in embeddings.items():
            f.write(json.dumps({"id": node_id, "embedding": vector}) + "\n")
    tmp.replace(embed_path)


def _embed_text(text: str, ollama_url: str, model: str, timeout: int) -> list[float] | None:
    try:
        resp = requests.post(
            f"{ollama_url}/api/embeddings",
            json={"model": model, "prompt": text},
            timeout=timeout,
        )
        resp.raise_for_status()
        return resp.json().get("embedding")
    except Exception as e:
        logger.warning(f"Embedding request failed: {e}")
        return None


def _node_text(node: dict) -> str:
    summary = (node.get("summary") or "").strip()
    content = (node.get("content") or "").strip()
    return f"{summary} {content}".strip()


def _run_pass(cfg: dict) -> int:
    """Single indexing pass. Returns number of new embeddings written."""
    ollama_url = cfg["ollama"]["base_url"]
    model = cfg["ollama"]["embed_model"]
    timeout = cfg["ollama"].get("timeout_seconds", 30)
    batch_size = cfg["ollama"].get("batch_size", 8)

    root = Path(cfg["_root"])
    nodes_path = root / cfg["indexer"]["nodes_path"]
    embed_path = root / cfg["indexer"]["embeddings_path"]

    nodes = _load_nodes(nodes_path)
    if not nodes:
        logger.debug("No nodes found, skipping pass")
        return 0

    embeddings = load_embeddings(embed_path)

    pending = [
        n for n in nodes.values()
        if n.get("trust_layer") != "review_only"
        and n["id"] not in embeddings
    ]

    if not pending:
        logger.debug(f"All {len(nodes)} nodes embedded")
        return 0

    logger.info(f"Embedding {len(pending)} pending nodes via {model} @ {ollama_url}")
    new_count = 0

    for i in range(0, len(pending), batch_size):
        batch = pending[i:i + batch_size]
        for node in batch:
            text = _node_text(node)
            if not text:
                continue
            vec = _embed_text(text, ollama_url, model, timeout)
            if vec is not None:
                embeddings[node["id"]] = vec
                new_count += 1

    if new_count:
        _save_embeddings(embed_path, embeddings)
        logger.info(f"Wrote {new_count} new embeddings → {embed_path}")

    return new_count


def _indexer_loop(cfg: dict, stop_event: threading.Event) -> None:
    poll_interval = cfg["indexer"].get("poll_interval_seconds", 60)
    logger.info(f"Vault indexer daemon running (poll every {poll_interval}s)")
    while not stop_event.is_set():
        try:
            _run_pass(cfg)
        except Exception as e:
            logger.error(f"Indexer pass failed: {e}")
        stop_event.wait(timeout=poll_interval)
    logger.info("Vault indexer daemon stopped")


class VaultIndexer:
    """
    Background daemon that keeps embeddings.jsonl in sync with nodes.jsonl.

    Usage:
        indexer = VaultIndexer("configs/async_indexing.yaml")
        indexer.start()
        ...
        indexer.stop()
    """

    def __init__(self, config_path: str | Path):
        config_path = Path(config_path)
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        cfg["_root"] = str(config_path.parent.parent)
        self._cfg = cfg
        self._stop = threading.Event()
        self._thread = threading.Thread(
            target=_indexer_loop,
            args=(self._cfg, self._stop),
            daemon=True,
            name="vault-indexer",
        )

    def start(self) -> None:
        self._thread.start()
        logger.info("VaultIndexer started")

    def stop(self, timeout: float = 10.0) -> None:
        self._stop.set()
        self._thread.join(timeout=timeout)
        logger.info("VaultIndexer stopped")

    def run_once(self) -> int:
        """Synchronous single pass — useful for testing."""
        return _run_pass(self._cfg)
