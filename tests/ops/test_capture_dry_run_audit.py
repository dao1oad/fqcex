from __future__ import annotations

import json
from pathlib import Path
from subprocess import run
import sys


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / "scripts" / "capture_dry_run_audit.py"


def test_capture_dry_run_audit_prints_normalized_record() -> None:
    result = run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--operator",
            "alice",
            "--stage",
            "btc-preflight",
            "--venue",
            "BYBIT",
            "--instrument-id",
            "BTC-USDT-PERP",
            "--action",
            "start_dry_run",
            "--result",
            "success",
            "--evidence-path",
            "docs/plans/dry-run-evidence.md",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload == {
        "operator": "alice",
        "stage": "btc-preflight",
        "venue": "BYBIT",
        "instrument_id": "BTC-USDT-PERP",
        "action": "start_dry_run",
        "result": "success",
        "evidence_path": "docs/plans/dry-run-evidence.md",
    }
