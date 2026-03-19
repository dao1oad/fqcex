from __future__ import annotations

import importlib
import os
import subprocess
import sys
from pathlib import Path

import pytest

SRC_ROOT = Path(__file__).resolve().parents[2] / "src"


def test_main_returns_zero_and_prints_bootstrap_message(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("PERP_PLATFORM_APP_NAME", raising=False)
    monkeypatch.delenv("PERP_PLATFORM_ENVIRONMENT", raising=False)
    monkeypatch.delenv("PERP_PLATFORM_LOG_LEVEL", raising=False)
    sys.path.insert(0, str(SRC_ROOT))

    try:
        cli = importlib.import_module("perp_platform.cli")
    except ModuleNotFoundError as exc:
        pytest.fail(f"perp_platform.cli should be importable: {exc}")
    finally:
        sys.path.pop(0)

    exit_code = cli.main([])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.strip() == "perp-platform bootstrap ready [dev]"


def test_module_entrypoint_runs_successfully() -> None:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(SRC_ROOT)
    env["PERP_PLATFORM_ENVIRONMENT"] = "test"

    result = subprocess.run(
        [sys.executable, "-m", "perp_platform"],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )

    assert result.returncode == 0
    assert result.stdout.strip() == "perp-platform bootstrap ready [test]"
