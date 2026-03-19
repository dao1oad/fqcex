# Master Agent GH Sync And Start Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Extend the issue orchestrator so the master agent can sync GitHub issues into a local snapshot, select and claim the next valid child issue, and emit a complete dispatch pack through a single `start` command.

**Architecture:** Keep deterministic orchestration decisions local. Add a GitHub sync step that normalizes issue state into `.codex/orchestrator/issues.json`, then reuse the existing local selector, approval bundle checks, and runtime state to drive `next`, `claim`, `prepare`, and the new `start` aggregator.

**Tech Stack:** Python 3.12, stdlib `argparse`, `json`, `pathlib`, `subprocess`, `dataclasses`, `pytest`, GitHub CLI (`gh`)

---

### Task 1: Add normalized issue snapshot model fields

**Files:**
- Modify: `D:/fqcex/src/perp_platform/orchestrator/models.py`
- Test: `D:/fqcex/tests/orchestrator/test_models_snapshot.py`

**Step 1: Write the failing test**

```python
from perp_platform.orchestrator.models import IssueSnapshot


def test_issue_snapshot_keeps_sequence_and_labels() -> None:
    snapshot = IssueSnapshot(
        issue_id=30,
        issue_title="Doc constraints",
        tracking_issue_id=11,
        epic_issue_id=2,
        sequence_index=2,
        state="open",
        type_label="type/task",
        phase_labels=("phase/1",),
        area_labels=("area/architecture",),
        assignees=("dao1oad",),
        body="body",
    )

    assert snapshot.sequence_index == 2
    assert snapshot.type_label == "type/task"
    assert snapshot.assignees == ("dao1oad",)
```

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/orchestrator/test_models_snapshot.py -q`
Expected: FAIL because `IssueSnapshot` does not exist

**Step 3: Write minimal implementation**

```python
@dataclass(frozen=True)
class IssueSnapshot:
    issue_id: int
    issue_title: str
    tracking_issue_id: int
    epic_issue_id: int
    sequence_index: int
    state: str
    type_label: str
    phase_labels: tuple[str, ...]
    area_labels: tuple[str, ...]
    assignees: tuple[str, ...]
    body: str
```

**Step 4: Run test to verify it passes**

Run: `py -m pytest tests/orchestrator/test_models_snapshot.py -q`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/orchestrator/test_models_snapshot.py src/perp_platform/orchestrator/models.py
git commit -m "feat: add normalized issue snapshot model"
```

### Task 2: Add hierarchy parser for sequence metadata

**Files:**
- Modify: `D:/fqcex/src/perp_platform/orchestrator/sequence.py`
- Test: `D:/fqcex/tests/orchestrator/test_sequence_hierarchy.py`

**Step 1: Write the failing test**

```python
from perp_platform.orchestrator.sequence import parse_issue_hierarchy


def test_parse_issue_hierarchy_extracts_child_order() -> None:
    content = """
    - #11 [Tracking]
      - #28 child
      - #29 child
      - #30 child
    """

    hierarchy = parse_issue_hierarchy(content)

    assert hierarchy[30]["tracking_issue_id"] == 11
    assert hierarchy[30]["sequence_index"] == 2
```

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/orchestrator/test_sequence_hierarchy.py -q`
Expected: FAIL because `parse_issue_hierarchy` does not exist

**Step 3: Write minimal implementation**

Implement a narrow parser that reads `ISSUE_HIERARCHY.md`, extracts tracking / epic / child order, and returns sequence metadata keyed by child issue id.

**Step 4: Run test to verify it passes**

Run: `py -m pytest tests/orchestrator/test_sequence_hierarchy.py -q`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/orchestrator/test_sequence_hierarchy.py src/perp_platform/orchestrator/sequence.py
git commit -m "feat: parse issue hierarchy order"
```

### Task 3: Add `gh sync` normalization helpers

**Files:**
- Create: `D:/fqcex/src/perp_platform/orchestrator/gh_sync.py`
- Modify: `D:/fqcex/src/perp_platform/orchestrator/github_state.py`
- Test: `D:/fqcex/tests/orchestrator/test_gh_sync.py`

**Step 1: Write the failing test**

```python
from pathlib import Path

from perp_platform.orchestrator.gh_sync import normalize_github_issues


def test_normalize_github_issues_merges_hierarchy_and_issue_metadata(tmp_path: Path) -> None:
    issues = [
        {
            "number": 30,
            "title": "Doc constraints",
            "state": "OPEN",
            "labels": [{"name": "type/task"}, {"name": "phase/1"}],
            "assignees": [{"login": "dao1oad"}],
            "body": "Tracking Parent: #11\\nEpic: #2",
        }
    ]
    hierarchy = {30: {"tracking_issue_id": 11, "epic_issue_id": 2, "sequence_index": 2}}

    normalized = normalize_github_issues(issues, hierarchy)

    assert normalized[0]["issue_id"] == 30
    assert normalized[0]["tracking_issue_id"] == 11
    assert normalized[0]["type_label"] == "type/task"
```

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/orchestrator/test_gh_sync.py -q`
Expected: FAIL because normalization helpers do not exist

**Step 3: Write minimal implementation**

Implement:

- label extraction
- assignee extraction
- body link extraction
- hierarchy merge into normalized `issues.json` entries

Do not call `gh` directly in this unit test path; keep normalization pure.

**Step 4: Run test to verify it passes**

Run: `py -m pytest tests/orchestrator/test_gh_sync.py -q`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/orchestrator/test_gh_sync.py src/perp_platform/orchestrator/gh_sync.py src/perp_platform/orchestrator/github_state.py
git commit -m "feat: normalize github issue sync data"
```

### Task 4: Add `gh sync` CLI command

**Files:**
- Modify: `D:/fqcex/scripts/issue_orchestrator.py`
- Modify: `D:/fqcex/src/perp_platform/orchestrator/github_state.py`
- Test: `D:/fqcex/tests/orchestrator/test_cli_gh_sync.py`

**Step 1: Write the failing test**

```python
def test_cli_gh_sync_writes_normalized_issue_snapshot():
    ...
```

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/orchestrator/test_cli_gh_sync.py -q`
Expected: FAIL because `gh sync` is not implemented

**Step 3: Write minimal implementation**

Implement:

- `gh sync`
- a thin shell-out to `gh issue list`
- read `ISSUE_HIERARCHY.md`
- normalize into `.codex/orchestrator/issues.json`

Use dependency injection or a helper function so the CLI path remains testable without live GitHub calls.

**Step 4: Run test to verify it passes**

Run: `py -m pytest tests/orchestrator/test_cli_gh_sync.py -q`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/orchestrator/test_cli_gh_sync.py scripts/issue_orchestrator.py src/perp_platform/orchestrator/github_state.py
git commit -m "feat: add github sync command"
```

### Task 5: Tighten next-ready selection with assignee and metadata checks

**Files:**
- Modify: `D:/fqcex/src/perp_platform/orchestrator/sequence.py`
- Modify: `D:/fqcex/src/perp_platform/orchestrator/github_state.py`
- Test: `D:/fqcex/tests/orchestrator/test_sequence_ready_state.py`

**Step 1: Write the failing test**

```python
def test_select_next_ready_issue_rejects_other_assignee():
    ...


def test_select_next_ready_issue_rejects_invalid_type_label():
    ...
```

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/orchestrator/test_sequence_ready_state.py -q`
Expected: FAIL because selector is too permissive

**Step 3: Write minimal implementation**

Refine selection rules so a ready issue must be:

- `type/task`
- `open`
- in correct sibling order
- unassigned or assigned to the current operator
- within approval scope when used by `prepare/start`

**Step 4: Run test to verify it passes**

Run: `py -m pytest tests/orchestrator/test_sequence_ready_state.py -q`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/orchestrator/test_sequence_ready_state.py src/perp_platform/orchestrator/sequence.py src/perp_platform/orchestrator/github_state.py
git commit -m "feat: tighten ready issue selection"
```

### Task 6: Upgrade `prepare` to emit full dispatch pack

**Files:**
- Modify: `D:/fqcex/src/perp_platform/orchestrator/dispatcher.py`
- Modify: `D:/fqcex/scripts/issue_orchestrator.py`
- Test: `D:/fqcex/tests/orchestrator/test_cli_prepare_dispatch_pack.py`

**Step 1: Write the failing test**

```python
def test_prepare_outputs_execution_context_constraints_and_prompt():
    ...
```

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/orchestrator/test_cli_prepare_dispatch_pack.py -q`
Expected: FAIL because `prepare` only emits a minimal payload

**Step 3: Write minimal implementation**

Extend `prepare` output with:

- `execution_context`
- `constraints`
- `subagent_prompt`
- reviewer / verifier requirements

Render `subagent_prompt` from structured fields, not ad-hoc string assembly in the CLI.

**Step 4: Run test to verify it passes**

Run: `py -m pytest tests/orchestrator/test_cli_prepare_dispatch_pack.py -q`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/orchestrator/test_cli_prepare_dispatch_pack.py scripts/issue_orchestrator.py src/perp_platform/orchestrator/dispatcher.py
git commit -m "feat: emit full dispatch pack from prepare"
```

### Task 7: Add `start` orchestration command

**Files:**
- Modify: `D:/fqcex/scripts/issue_orchestrator.py`
- Modify: `D:/fqcex/src/perp_platform/orchestrator/runtime_state.py`
- Test: `D:/fqcex/tests/orchestrator/test_cli_start.py`

**Step 1: Write the failing test**

```python
def test_start_runs_sync_select_claim_and_prepare():
    ...


def test_start_fails_without_approval_bundle():
    ...
```

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/orchestrator/test_cli_start.py -q`
Expected: FAIL because `start` does not exist

**Step 3: Write minimal implementation**

Implement `start` as a pure orchestration aggregator that:

- checks approval bundle
- runs sync
- selects the next ready issue
- claims it
- emits the final dispatch pack

Do not auto-dispatch subagents or create a real worktree in this task.

**Step 4: Run test to verify it passes**

Run: `py -m pytest tests/orchestrator/test_cli_start.py -q`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/orchestrator/test_cli_start.py scripts/issue_orchestrator.py src/perp_platform/orchestrator/runtime_state.py
git commit -m "feat: add start orchestration command"
```

### Task 8: Update runbook for the new master-agent flow

**Files:**
- Modify: `D:/fqcex/docs/runbooks/issue-orchestrator.md`
- Test: `D:/fqcex/tests/governance/test_issue_orchestrator_runbook_contract.py`

**Step 1: Write the failing test**

```python
def test_issue_orchestrator_runbook_mentions_gh_sync_and_start():
    ...
```

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/governance/test_issue_orchestrator_runbook_contract.py -q`
Expected: FAIL because the runbook does not mention `gh sync` and `start`

**Step 3: Write minimal implementation**

Document:

- `gh sync`
- `start`
- local snapshot path
- dispatch pack output
- what remains manual vs automated

**Step 4: Run test to verify it passes**

Run: `py -m pytest tests/governance/test_issue_orchestrator_runbook_contract.py -q`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/governance/test_issue_orchestrator_runbook_contract.py docs/runbooks/issue-orchestrator.md
git commit -m "docs: document sync and start flow"
```

### Task 9: Full verification

**Files:**
- Verify only: `D:/fqcex/tests/orchestrator`
- Verify only: `D:/fqcex/tests/governance`

**Step 1: Run orchestrator tests**

Run: `py -m pytest tests/orchestrator -q`
Expected: PASS

**Step 2: Run governance tests**

Run: `py -m pytest tests/governance -q`
Expected: PASS

**Step 3: Run full repository tests**

Run: `py -m pytest tests -q`
Expected: PASS

**Step 4: Manually smoke the CLI**

Run: `py scripts/issue_orchestrator.py approval show`
Expected: Prints the current approval bundle summary or a clear missing-file message

Run: `py scripts/issue_orchestrator.py start`
Expected: Emits a dispatch pack or a clear reason why there is no ready issue

**Step 5: Commit**

```bash
git add .
git commit -m "test: verify master agent sync and start flow"
```
