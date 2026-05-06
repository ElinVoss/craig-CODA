"""Adapter registry.

Maps canonical backend_name strings to BaseAdapter instances.
One adapter instance per backend_name — adapters lazy-load their
heavyweight resources on first call(), not at registration time.
"""
from __future__ import annotations

from src.adapters.base import BaseAdapter


class AdapterRegistry:
    """Maps backend_name → BaseAdapter. Thread-unsafe; single-process use only."""

    def __init__(self) -> None:
        self._adapters: dict[str, BaseAdapter] = {}

    def register(self, adapter: BaseAdapter) -> None:
        """Register an adapter under its backend_name. Overwrites existing."""
        self._adapters[adapter.backend_name] = adapter

    def get(self, backend_name: str) -> BaseAdapter:
        """Return the adapter for backend_name.

        Raises KeyError with a clear message listing registered names if not found.
        """
        if backend_name not in self._adapters:
            available = list(self._adapters.keys())
            raise KeyError(
                f"No adapter registered for '{backend_name}'. "
                f"Registered: {available}"
            )
        return self._adapters[backend_name]

    def list_backends(self) -> list[str]:
        """Return sorted list of all registered backend names."""
        return sorted(self._adapters.keys())

    def health_report(self) -> dict[str, bool]:
        """Return a dict of backend_name → health_check() for all registered adapters."""
        return {name: adapter.health_check() for name, adapter in self._adapters.items()}


# Global registry. Register adapters at startup with DEFAULT_ADAPTER_REGISTRY.register(adapter).
DEFAULT_ADAPTER_REGISTRY = AdapterRegistry()
