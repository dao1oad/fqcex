from __future__ import annotations

import json
from pathlib import Path
from subprocess import run
import sys


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / "scripts" / "inject_ws_disconnect.py"


def test_ws_disconnect_injector_prints_normalized_plan() -> None:
    result = run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--venue",
            "BYBIT",
            "--stream",
            "public",
            "--duration-seconds",
            "15",
            "--instrument-id",
            "BTC-USDT-PERP",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload == {
        "injector": "ws_disconnect",
        "venue": "BYBIT",
        "stream": "public",
        "duration_seconds": 15,
        "instrument_id": "BTC-USDT-PERP",
        "reason": "manual_fault_injection",
        "action": "disconnect_websocket",
    }


def test_ws_disconnect_injector_rejects_non_positive_duration() -> None:
    result = run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--venue",
            "BYBIT",
            "--stream",
            "public",
            "--duration-seconds",
            "0",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode != 0
    assert "duration" in result.stderr.lower()
