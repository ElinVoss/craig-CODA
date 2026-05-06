from __future__ import annotations

from typing import Type

from .backend_types import BackendBase


class BackendRegistry:
    """Registry mapping backend_type strings to BackendBase subclasses.

    Backends are registered by type name (e.g. 'pretrained_transformers',
    'scratch'). load_backend.py uses the registry to instantiate the correct
    class for a given config entry.
    """

    def __init__(self) -> None:
        self._registry: dict[str, Type[BackendBase]] = {}

    def register(self, name: str, cls: Type[BackendBase]) -> None:
        """Register a backend class under a type name."""
        self._registry[name] = cls

    def get(self, name: str) -> Type[BackendBase]:
        """Return the backend class for the given type name.

        Raises KeyError if the type is not registered.
        """
        if name not in self._registry:
            registered = list(self._registry.keys())
            raise KeyError(
                f"Backend type '{name}' is not registered. "
                f"Registered types: {registered}"
            )
        return self._registry[name]

    def list_registered(self) -> list[str]:
        """Return sorted list of all registered backend type names."""
        return sorted(self._registry.keys())


# Global registry instance. Backend modules register themselves on import.
DEFAULT_REGISTRY = BackendRegistry()


def _register_defaults() -> None:
    """Auto-register scratch and local pretrained backend types."""
    from .scratch_backend import ScratchBackend
    from .pretrained_transformers_backend import PretrainedTransformersBackend
    from .qwen2_5_omni_backend import Qwen2_5OmniBackend

    DEFAULT_REGISTRY.register("scratch", ScratchBackend)
    DEFAULT_REGISTRY.register("pretrained_transformers", PretrainedTransformersBackend)
    DEFAULT_REGISTRY.register("qwen2_5_omni", Qwen2_5OmniBackend)


# Register on module import so callers can use DEFAULT_REGISTRY immediately.
_register_defaults()
