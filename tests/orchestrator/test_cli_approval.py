from pathlib import Path
import json
import subprocess
import sys


def test_cli_approval_create_and_show(tmp_path: Path) -> None:
    approval_path = tmp_path / "approval_bundle.json"
    repo_root = Path(__file__).resolve().parents[2]

    create_result = subprocess.run(
        [
            sys.executable,
            "scripts/issue_orchestrator.py",
            "approval",
            "create",
            "--issue-start",
            "30",
            "--issue-end",
            "33",
            "--approval-path",
            str(approval_path),
        ],
        capture_output=True,
        text=True,
        check=False,
        cwd=repo_root,
    )

    assert create_result.returncode == 0
    payload = json.loads(approval_path.read_text(encoding="utf-8"))
    assert payload["issue_start"] == 30
    assert payload["model"] == "gpt-5.4"

    show_result = subprocess.run(
        [
            sys.executable,
            "scripts/issue_orchestrator.py",
            "approval",
            "show",
            "--approval-path",
            str(approval_path),
        ],
        capture_output=True,
        text=True,
        check=False,
        cwd=repo_root,
    )

    assert show_result.returncode == 0
    assert "issues_30_to_33" in show_result.stdout
    assert "gpt-5.4" in show_result.stdout


def test_cli_approval_check_rejects_issue_out_of_scope(tmp_path: Path) -> None:
    approval_path = tmp_path / "approval_bundle.json"
    repo_root = Path(__file__).resolve().parents[2]

    subprocess.run(
        [
            sys.executable,
            "scripts/issue_orchestrator.py",
            "approval",
            "create",
            "--issue-start",
            "30",
            "--issue-end",
            "33",
            "--approval-path",
            str(approval_path),
        ],
        capture_output=True,
        text=True,
        check=True,
        cwd=repo_root,
    )

    check_result = subprocess.run(
        [
            sys.executable,
            "scripts/issue_orchestrator.py",
            "approval",
            "check",
            "--issue",
            "34",
            "--approval-path",
            str(approval_path),
        ],
        capture_output=True,
        text=True,
        check=False,
        cwd=repo_root,
    )

    assert check_result.returncode == 1
    assert "out of approved scope" in check_result.stdout
