from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.model_backends.load_backend import list_all_backends, get_default_backend_name, _load_selection_yaml


def main() -> int:
    all_backends = list_all_backends()
    selection = _load_selection_yaml(None)
    default_name = selection.get("default_backend", "")
    scratch_name = selection.get("scratch_backend_name", "")
    pretrained_default = selection.get("pretrained_default_backend", "")

    col_w = [24, 8, 24, 16, 46, 16]
    header = (
        f"{'NAME':<{col_w[0]}}  "
        f"{'ENABLED':<{col_w[1]}}  "
        f"{'TYPE':<{col_w[2]}}  "
        f"{'ROLE':<{col_w[3]}}  "
        f"{'MODEL PATH':<{col_w[4]}}  "
        f"{'FLAGS'}"
    )
    sep = "-" * len(header)

    print(sep)
    print(header)
    print(sep)

    for b in all_backends:
        name = str(b.get("backend_name", ""))
        enabled = "yes" if b.get("enabled") else "no"
        btype = str(b.get("backend_type", ""))
        role = str(b.get("role", ""))
        path = str(b.get("model_id_or_local_path", ""))
        if len(path) > col_w[4]:
            path = "..." + path[-(col_w[4] - 3):]

        flags = []
        if name == default_name:
            flags.append("DEFAULT")
        if name == pretrained_default:
            flags.append("PRETRAINED-DEFAULT")
        if name == scratch_name:
            flags.append("SCRATCH")
        flags_str = ", ".join(flags)

        print(
            f"{name:<{col_w[0]}}  "
            f"{enabled:<{col_w[1]}}  "
            f"{btype:<{col_w[2]}}  "
            f"{role:<{col_w[3]}}  "
            f"{path:<{col_w[4]}}  "
            f"{flags_str}"
        )

    print(sep)
    print(f"Total backends: {len(all_backends)}")
    print(f"Default backend:           {default_name or '(not set)'}")
    print(f"Scratch backend name:      {scratch_name or '(not set)'}")
    print(f"Pretrained default:        {pretrained_default or '(not set)'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
