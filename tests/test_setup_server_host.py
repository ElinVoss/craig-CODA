"""Tests for the server host bootstrap script."""
import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).parents[1]))

import scripts.setup_server_host as setup_server_host
from scripts.setup_server_host import stage_server_host


def test_stage_server_host_writes_workspace_files():
    with TemporaryDirectory() as tmp:
        report = stage_server_host(
            dest=Path(tmp) / "server-root",
            local_url="http://127.0.0.1:1234",
            advertise_host="192.168.4.25",
            probe=False,
            copy_host_kit=True,
        )
        root = Path(report["workspace_root"])
        assert (root / ".env.server").exists()
        assert (root / "client_connection.env").exists()
        assert (root / "START-SERVER-HOST.txt").exists()
        assert (root / "bootstrap_report.json").exists()
        assert (root / "probe_local_server.bat").exists()
        assert (root / "awaken_payload" / "README.txt").exists()
        assert (root / "qwen-host-kit" / "README.md").exists()


def test_stage_server_host_env_matches_live_client_keys():
    with TemporaryDirectory() as tmp:
        report = stage_server_host(
            dest=Path(tmp) / "server-root",
            local_url="http://127.0.0.1:1234",
            advertise_host="192.168.4.25",
            probe=False,
            copy_host_kit=False,
        )
        root = Path(report["workspace_root"])
        server_env = (root / ".env.server").read_text(encoding="utf-8")
        client_env = (root / "client_connection.env").read_text(encoding="utf-8")
        assert "LMSTUDIO_SERVER=http://127.0.0.1:1234" in server_env
        assert "LOCAL_MODEL_URL=http://127.0.0.1:1234/v1" in server_env
        assert "LMSTUDIO_SERVER=http://192.168.4.25:1234" in client_env
        assert "LOCAL_MODEL_URL=http://192.168.4.25:1234/v1" in client_env
        assert "CRAIG_BACKEND=local" in client_env


def test_stage_server_host_report_is_machine_readable():
    with TemporaryDirectory() as tmp:
        report = stage_server_host(
            dest=Path(tmp) / "server-root",
            local_url="http://127.0.0.1:1234",
            advertise_host="192.168.4.25",
            probe=False,
        )
        report_path = Path(report["workspace_root"]) / "bootstrap_report.json"
        payload = json.loads(report_path.read_text(encoding="utf-8"))
        assert payload["network"]["advertised_url"] == "http://192.168.4.25:1234"
        assert payload["lmstudio"]["probe_ran"] is False
        assert payload["pending_actions"]


def test_stage_server_host_tolerates_missing_optional_host_kit():
    original = setup_server_host.HOST_KIT_SOURCE
    try:
        setup_server_host.HOST_KIT_SOURCE = Path(r"Z:\missing-host-kit")
        with TemporaryDirectory() as tmp:
            report = stage_server_host(
                dest=Path(tmp) / "server-root",
                local_url="http://127.0.0.1:1234",
                advertise_host="192.168.4.25",
                probe=False,
                copy_host_kit=True,
            )
            root = Path(report["workspace_root"])
            placeholder = root / "qwen-host-kit" / "README.txt"
            assert placeholder.exists()
            assert report["host_kit"]["source_exists"] is False
            assert report["host_kit"]["staged"] is False
    finally:
        setup_server_host.HOST_KIT_SOURCE = original


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
            print(f"  FAIL  {fn.__name__}: {exc}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
    if failed:
        sys.exit(1)
