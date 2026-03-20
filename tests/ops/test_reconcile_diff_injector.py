from __future__ import annotations

import json
from pathlib import Path
from subprocess import run
import sys


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / "scripts" / "inject_reconcile_diff.py"


def test_reconcile_diff_injector_prints_normalized_plan() -> None:
    result = run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--venue",
            "OKX",
            "--resource",
            "position",
            "--diff-kind",
            "mismatch",
            "--instrument-id",
            "ETH-USDT-PERP",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload == {
        "injector": "reconcile_diff",
        "venue": "OKX",
        "resource": "position",
        "diff_kind": "mismatch",
        "instrument_id": "ETH-USDT-PERP",
        "reason": "manual_fault_injection",
        "action": "inject_reconcile_diff",
    }


def test_reconcile_diff_injector_allows_balance_without_instrument() -> None:
    result = run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--venue",
            "OKX",
            "--resource",
            "balance",
            "--diff-kind",
            "missing",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["instrument_id"] is None
