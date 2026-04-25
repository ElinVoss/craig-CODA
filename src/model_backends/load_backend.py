from __future__ import annotations

from pathlib import Path

import yaml

from .backend_types import BackendBase, BackendConfig

_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_BACKENDS_CFG = _ROOT / "configs" / "pretrained_backends.yaml"
_DEFAULT_SELECTION_CFG = _ROOT / "configs" / "backend_selection.yaml"


def _load_backends_yaml(cfg_path: Path | None) -> dict:
    path = cfg_path or _DEFAULT_BACKENDS_CFG
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def _load_selection_yaml(cfg_path: Path | None) -> dict:
    path = cfg_path or _DEFAULT_SELECTION_CFG
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def get_default_backend_name(cfg_path: Path | None = None) -> str:
    """Return the default backend name from backend_selection.yaml."""
    selection = _load_selection_yaml(cfg_path)
    name = selection.get("default_backend")
    if not name:
        raise ValueError(
            "backend_selection.yaml does not specify a default_backend."
        )
    return str(name)


def list_all_backends(cfg_path: Path | None = None) -> list[dict]:
    """Return all backend configs as raw dicts from pretrained_backends.yaml."""
    data = _load_backends_yaml(cfg_path)
    return list(data.get("backends", []))


def load_backend(
    backend_name: str | None = None,
    cfg_path: Path | None = None,
) -> BackendBase:
    """Instantiate and return a BackendBase for the given backend_name.

    If backend_name is None, reads the default from backend_selection.yaml.
    Does NOT call load() — the caller decides when to load weights.

    Raises:
        ValueError: if the backend_name is not found in pretrained_backends.yaml.
        KeyError: if the backend_type is not registered in DEFAULT_REGISTRY.
    """
    from .backend_registry import DEFAULT_REGISTRY

    if backend_name is None:
        backend_name = get_default_backend_name(cfg_path)

    all_backends = list_all_backends(cfg_path)
    matched = [b for b in all_backends if b.get("backend_name") == backend_name]

    if not matched:
        available = [b.get("backend_name") for b in all_backends]
        raise ValueError(
            f"Backend '{backend_name}' not found in pretrained_backends.yaml. "
            f"Available: {available}"
        )

    raw = matched[0]
    config = BackendConfig.from_dict(raw)

    backend_type = config.backend_type
    cls = DEFAULT_REGISTRY.get(backend_type)

    print(f"[load_backend] Loading backend '{backend_name}'  type={backend_type}  role={config.role}")
    return cls(config)
