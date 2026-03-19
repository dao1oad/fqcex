from pathlib import Path
import json
import subprocess
import sys


def test_cli_accept_rejects_head_sha_mismatch(tmp_path: Path) -> None:
    state_path = tmp_path / "state.json"
    changed_files_path = tmp_path / "changed_files.json"
    review_evidence_path = tmp_path / "review.md"
    repo_root = Path(__file__).resolve().parents[2]

    state_path.write_text(
        json.dumps(
            {
                "issue_id": 29,
                "issue_title": "Quantity",
                "tracking_issue_id": 11,
                "status": "verifying",
                "owner_agent_id": "agent-1",
                "approval_bundle_id": "exec-1",
                "head_sha": "abc123",
                "allowed_files": ["src/perp_platform/domain/quantity.py"],
            }
        ),
        encoding="utf-8",
    )
    changed_files_path.write_text(
        json.dumps(["src/perp_platform/domain/quantity.py"]),
        encoding="utf-8",
    )
    review_evidence_path.write_text("review complete", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/issue_orchestrator.py",
            "accept",
            "29",
            "--state-path",
            str(state_path),
            "--head-sha",
            "def456",
            "--changed-files-path",
            str(changed_files_path),
            "--review-evidence-path",
            str(review_evidence_path),
        ],
        capture_output=True,
        text=True,
        check=False,
        cwd=repo_root,
    )

    assert result.returncode == 1
    assert "head sha mismatch" in result.stdout


def test_cli_accept_rejects_issue_boundary_violation(tmp_path: Path) -> None:
    state_path = tmp_path / "state.json"
    changed_files_path = tmp_path / "changed_files.json"
    review_evidence_path = tmp_path / "review.md"
    repo_root = Path(__file__).resolve().parents[2]

    state_path.write_text(
        json.dumps(
            {
                "issue_id": 29,
                "issue_title": "Quantity",
                "tracking_issue_id": 11,
                "status": "verifying",
                "owner_agent_id": "agent-1",
                "approval_bundle_id": "exec-1",
                "head_sha": "abc123",
                "allowed_files": ["src/perp_platform/domain/quantity.py"],
            }
        ),
        encoding="utf-8",
    )
    changed_files_path.write_text(
        json.dumps(["docs/runbooks/rollback.md"]),
        encoding="utf-8",
    )
    review_evidence_path.write_text("review complete", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/issue_orchestrator.py",
            "accept",
            "29",
            "--state-path",
            str(state_path),
            "--head-sha",
            "abc123",
            "--changed-files-path",
            str(changed_files_path),
            "--review-evidence-path",
            str(review_evidence_path),
        ],
        capture_output=True,
        text=True,
        check=False,
        cwd=repo_root,
    )

    assert result.returncode == 1
    assert "boundary violation" in result.stdout


def test_cli_accept_supports_dispatch_pack_without_runtime_state(
    tmp_path: Path,
) -> None:
    dispatch_path = tmp_path / "dispatch.json"
    changed_files_path = tmp_path / "changed_files.json"
    review_evidence_path = tmp_path / "review.md"
    repo_root = Path(__file__).resolve().parents[2]

    dispatch_path.write_text(
        json.dumps(
            {
                "execution_context": {
                    "issue_id": 93,
                    "issue_title": "Cloud orchestrator mode",
                    "tracking_issue_id": 90,
                    "epic_issue_id": 2,
                    "approval_bundle_id": "exec-93",
                    "model": "gpt-5.4",
                    "reasoning_effort": "xhigh",
                },
                "constraints": {
                    "allowed_files": ["scripts/issue_orchestrator.py"],
                    "forbidden_files": [],
                    "acceptance_checks": ["py -m pytest tests/orchestrator -q"],
                    "escalation_triggers": ["forbidden_file_change"],
                    "review_requirements": [
                        "review evidence required",
                        "verification required before merge",
                    ],
                },
                "acceptance_payload": {
                    "issue_id": 93,
                    "approval_bundle_id": "exec-93",
                    "allowed_files": ["scripts/issue_orchestrator.py"],
                    "review_required": True,
                },
            }
        ),
        encoding="utf-8",
    )
    changed_files_path.write_text(
        json.dumps(["scripts/issue_orchestrator.py"]),
        encoding="utf-8",
    )
    review_evidence_path.write_text("review complete", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/issue_orchestrator.py",
            "accept",
            "93",
            "--dispatch-path",
            str(dispatch_path),
            "--head-sha",
            "abc123",
            "--changed-files-path",
            str(changed_files_path),
            "--review-evidence-path",
            str(review_evidence_path),
        ],
        capture_output=True,
        text=True,
        check=False,
        cwd=repo_root,
    )

    assert result.returncode == 0
    assert "accepted" in result.stdout
