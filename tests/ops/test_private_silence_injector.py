from __future__ import annotations

import json
from pathlib import Path
from subprocess import run
import sys


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / "scripts" / "inject_private_silence.py"


def test_private_silence_injector_prints_normalized_plan() -> None:
    result = run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--venue",
            "BINANCE",
            "--duration-seconds",
            "30",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload == {
        "injector": "private_silence",
        "venue": "BINANCE",
        "scope": "account",
        "duration_seconds": 30,
        "reason": "manual_fault_injection",
        "action": "silence_private_stream",
    }


def test_private_silence_injector_rejects_non_positive_duration() -> None:
    result = run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--venue",
            "BINANCE",
            "--duration-seconds",
            "-1",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode != 0
    assert "duration" in result.stderr.lower()
