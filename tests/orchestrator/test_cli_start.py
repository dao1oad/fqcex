from pathlib import Path
import json
import subprocess
import sys


def expected_worktree_path(repo_root: Path, issue_slug: str) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--git-common-dir"],
        capture_output=True,
        text=True,
        check=True,
        cwd=repo_root,
    )
    common_dir = Path(result.stdout.strip())
    if not common_dir.is_absolute():
        common_dir = (repo_root / common_dir).resolve()
    return str(common_dir.parent / ".worktrees" / issue_slug)


def test_start_runs_sync_select_claim_and_prepare(tmp_path: Path) -> None:
    approval_path = tmp_path / "approval_bundle.json"
    gh_json_path = tmp_path / "gh_issues.json"
    hierarchy_path = tmp_path / "ISSUE_HIERARCHY.md"
    output_path = tmp_path / "issues.json"
    state_path = tmp_path / "state.json"
    repo_root = Path(__file__).resolve().parents[2]

    gh_json_path.write_text(
        json.dumps(
            [
                {
                    "number": 30,
                    "title": "Doc constraints",
                    "state": "OPEN",
                    "labels": [
                        {"name": "type/task"},
                        {"name": "phase/1"},
                        {"name": "area/architecture"},
                    ],
                    "assignees": [{"login": "dao1oad"}],
                    "body": "Tracking Parent: #11\nEpic: #2",
                }
            ]
        ),
        encoding="utf-8",
    )
    hierarchy_path.write_text(
        """
- `#2 [Epic] 第 1 阶段：单交易所闭环`
  - `#11 [Tracking] 定义统一合约与数量模型`
    - `#30 统一模型：文档化真相字段与架构约束`
""".strip(),
        encoding="utf-8",
    )

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

    result = subprocess.run(
        [
            sys.executable,
            "scripts/issue_orchestrator.py",
            "start",
            "--approval-path",
            str(approval_path),
            "--hierarchy-path",
            str(hierarchy_path),
            "--output-path",
            str(output_path),
            "--gh-json-path",
            str(gh_json_path),
            "--state-path",
            str(state_path),
            "--operator",
            "dao1oad",
        ],
        capture_output=True,
        text=True,
        check=False,
        cwd=repo_root,
    )

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["execution_context"]["issue_id"] == 30
    assert payload["worktree_path"] == expected_worktree_path(
        repo_root, "issue-30-doc-constraints"
    )
    state_payload = json.loads(state_path.read_text(encoding="utf-8"))
    assert state_payload["issue_id"] == 30
    assert state_payload["status"] == "claimed"


def test_start_fails_without_approval_bundle(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[2]

    result = subprocess.run(
        [
            sys.executable,
            "scripts/issue_orchestrator.py",
            "start",
            "--approval-path",
            str(tmp_path / "missing-approval.json"),
        ],
        capture_output=True,
        text=True,
        check=False,
        cwd=repo_root,
    )

    assert result.returncode == 1
    assert "missing approval bundle" in result.stdout


def test_start_can_emit_portable_dispatch_pack_without_state_file(
    tmp_path: Path,
) -> None:
    approval_path = tmp_path / "approval_bundle.json"
    gh_json_path = tmp_path / "gh_issues.json"
    hierarchy_path = tmp_path / "ISSUE_HIERARCHY.md"
    output_path = tmp_path / "issues.json"
    state_path = tmp_path / "state.json"
    dispatch_path = tmp_path / "dispatch.json"
    repo_root = Path(__file__).resolve().parents[2]

    gh_json_path.write_text(
        json.dumps(
            [
                {
                    "number": 93,
                    "title": "Cloud orchestrator mode",
                    "state": "OPEN",
                    "labels": [
                        {"name": "type/task"},
                        {"name": "phase/1"},
                        {"name": "area/ops"},
                    ],
                    "assignees": [{"login": "dao1oad"}],
                    "body": "Tracking Parent: #90\nEpic: #2",
                }
            ]
        ),
        encoding="utf-8",
    )
    hierarchy_path.write_text(
        """
- `#2 [Epic] 第 1 阶段：单交易所闭环`
  - `#90 [Tracking] 迁移仓库到 Codex cloud 开发环境`
    - `#93 Codex cloud 迁移：调整主 agent / orchestrator 的云端执行模式`
""".strip(),
        encoding="utf-8",
    )

    subprocess.run(
        [
            sys.executable,
            "scripts/issue_orchestrator.py",
            "approval",
            "create",
            "--issue-start",
            "93",
            "--issue-end",
            "94",
            "--approval-path",
            str(approval_path),
        ],
        capture_output=True,
        text=True,
        check=True,
        cwd=repo_root,
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/issue_orchestrator.py",
            "start",
            "--approval-path",
            str(approval_path),
            "--hierarchy-path",
            str(hierarchy_path),
            "--output-path",
            str(output_path),
            "--gh-json-path",
            str(gh_json_path),
            "--state-path",
            str(state_path),
            "--dispatch-path",
            str(dispatch_path),
            "--skip-state-save",
            "--allowed-file",
            "scripts/issue_orchestrator.py",
            "--acceptance-check",
            "py -m pytest tests/orchestrator -q",
            "--operator",
            "dao1oad",
        ],
        capture_output=True,
        text=True,
        check=False,
        cwd=repo_root,
    )

    assert result.returncode == 0
    assert not state_path.exists()
    assert dispatch_path.exists()

    payload = json.loads(dispatch_path.read_text(encoding="utf-8"))
    assert payload["execution_context"]["issue_id"] == 93
    assert payload["claim_record"]["issue_id"] == 93
    assert payload["acceptance_payload"]["allowed_files"] == [
        "scripts/issue_orchestrator.py"
    ]
    assert payload["constraints"]["acceptance_checks"] == [
        "py -m pytest tests/orchestrator -q"
    ]


def test_start_fails_closed_when_open_task_is_missing_from_hierarchy(
    tmp_path: Path,
) -> None:
    approval_path = tmp_path / "approval_bundle.json"
    gh_json_path = tmp_path / "gh_issues.json"
    hierarchy_path = tmp_path / "ISSUE_HIERARCHY.md"
    output_path = tmp_path / "issues.json"
    state_path = tmp_path / "state.json"
    repo_root = Path(__file__).resolve().parents[2]

    gh_json_path.write_text(
        json.dumps(
            [
                {
                    "number": 89,
                    "title": "Review governance",
                    "state": "OPEN",
                    "labels": [{"name": "type/task"}, {"name": "phase/1"}],
                    "assignees": [{"login": "dao1oad"}],
                    "body": "Tracking Parent: #79\nEpic: #2",
                }
            ]
        ),
        encoding="utf-8",
    )
    hierarchy_path.write_text(
        """
- `#2 [Epic] 第 1 阶段：单交易所闭环`
  - `#79 [Tracking] 收敛开发工作流与最小交付基座`
    - `#81 交付基座：增加面向 perp-platform 的 CI workflow`
""".strip(),
        encoding="utf-8",
    )

    subprocess.run(
        [
            sys.executable,
            "scripts/issue_orchestrator.py",
            "approval",
            "create",
            "--issue-start",
            "80",
            "--issue-end",
            "90",
            "--approval-path",
            str(approval_path),
        ],
        capture_output=True,
        text=True,
        check=True,
        cwd=repo_root,
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/issue_orchestrator.py",
            "start",
            "--approval-path",
            str(approval_path),
            "--hierarchy-path",
            str(hierarchy_path),
            "--output-path",
            str(output_path),
            "--gh-json-path",
            str(gh_json_path),
            "--state-path",
            str(state_path),
            "--operator",
            "dao1oad",
        ],
        capture_output=True,
        text=True,
        check=False,
        cwd=repo_root,
    )

    assert result.returncode == 1
    assert "open task issue missing from ISSUE_HIERARCHY.md" in result.stdout
