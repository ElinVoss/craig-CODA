"""CODA adapters package.

Exposes the adapter contract (BaseAdapter), registry (AdapterRegistry,
DEFAULT_ADAPTER_REGISTRY), and the three built-in adapter implementations.

Usage:
    from src.adapters import DEFAULT_ADAPTER_REGISTRY
    from src.adapters.ollama_adapter import OllamaAdapter

    DEFAULT_ADAPTER_REGISTRY.register(OllamaAdapter("dolphin-llama3"))
    adapter = DEFAULT_ADAPTER_REGISTRY.get("ollama:dolphin-llama3")
    response = adapter.call(request)
"""
from src.adapters.base import BaseAdapter
from src.adapters.registry import AdapterRegistry, DEFAULT_ADAPTER_REGISTRY

__all__ = [
    "BaseAdapter",
    "AdapterRegistry",
    "DEFAULT_ADAPTER_REGISTRY",
]
