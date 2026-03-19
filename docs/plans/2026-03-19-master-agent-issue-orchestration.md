# Master Agent Issue Orchestration Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a repository-local orchestrator that selects the correct next child issue, enforces single-writer execution with controlled read-only concurrency, and records runtime orchestration state for a master agent using `gpt-5.4` with `xhigh`.

**Architecture:** Implement a small orchestrator package plus a thin CLI. Keep all issue-order decisions deterministic in Python, store runtime state in `.codex/orchestrator/state.json`, and leave code generation, verification, review, merge, and close decisions to the master agent workflow described in the design document.

**Tech Stack:** Python 3.12, stdlib `dataclasses`, `enum`, `json`, `pathlib`, `subprocess`, `typing`, `pytest`

---

### Task 1: Create orchestrator package skeleton

**Files:**
- Create: `D:/fqcex/src/perp_platform/orchestrator/__init__.py`
- Create: `D:/fqcex/src/perp_platform/orchestrator/models.py`
- Create: `D:/fqcex/src/perp_platform/orchestrator/sequence.py`
- Create: `D:/fqcex/src/perp_platform/orchestrator/runtime_state.py`
- Create: `D:/fqcex/src/perp_platform/orchestrator/github_state.py`
- Create: `D:/fqcex/src/perp_platform/orchestrator/dispatcher.py`
- Test: `D:/fqcex/tests/orchestrator/test_import_contract.py`

**Step 1: Write the failing test**

```python
def test_orchestrator_modules_import() -> None:
    from perp_platform.orchestrator import dispatcher, github_state, models, runtime_state, sequence

    assert dispatcher is not None
    assert github_state is not None
    assert models is not None
    assert runtime_state is not None
    assert sequence is not None
```

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/orchestrator/test_import_contract.py -q`
Expected: FAIL with `ModuleNotFoundError` for `perp_platform.orchestrator`

**Step 3: Write minimal implementation**

```python
# src/perp_platform/orchestrator/__init__.py
from . import dispatcher, github_state, models, runtime_state, sequence

__all__ = ["dispatcher", "github_state", "models", "runtime_state", "sequence"]
```

Create empty module files for the remaining imports.

**Step 4: Run test to verify it passes**

Run: `py -m pytest tests/orchestrator/test_import_contract.py -q`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/orchestrator/test_import_contract.py src/perp_platform/orchestrator
git commit -m "feat: add orchestrator package skeleton"
```

### Task 2: Define orchestration domain models

**Files:**
- Modify: `D:/fqcex/src/perp_platform/orchestrator/models.py`
- Test: `D:/fqcex/tests/orchestrator/test_models.py`

**Step 1: Write the failing test**

```python
from perp_platform.orchestrator.models import AgentRole, OrchestratorState, WorkItem


def test_work_item_defaults() -> None:
    work_item = WorkItem(issue_id=29, issue_title="test", tracking_issue_id=11)

    assert work_item.issue_id == 29
    assert work_item.status is OrchestratorState.READY
    assert work_item.owner_agent_id is None
    assert AgentRole.OWNER.value == "owner"
```
```

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/orchestrator/test_models.py -q`
Expected: FAIL with missing symbols

**Step 3: Write minimal implementation**

```python
from dataclasses import dataclass
from enum import StrEnum


class OrchestratorState(StrEnum):
    READY = "ready"
    CLAIMED = "claimed"
    CONTEXT_GATHERING = "context_gathering"
    DESIGNING = "designing"
    PLAN_READY = "plan_ready"
    DISPATCHED = "dispatched"
    IMPLEMENTING = "implementing"
    VERIFYING = "verifying"
    REVIEW_FIXING = "review_fixing"
    ACCEPTED = "accepted"
    MERGED = "merged"
    CLOSED = "closed"
    BLOCKED = "blocked"


class AgentRole(StrEnum):
    OWNER = "owner"
    EXPLORER = "explorer"
    VERIFIER = "verifier"
    REVIEWER = "reviewer"


@dataclass(frozen=True)
class WorkItem:
    issue_id: int
    issue_title: str
    tracking_issue_id: int
    status: OrchestratorState = OrchestratorState.READY
    owner_agent_id: str | None = None
```

**Step 4: Run test to verify it passes**

Run: `py -m pytest tests/orchestrator/test_models.py -q`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/orchestrator/test_models.py src/perp_platform/orchestrator/models.py
git commit -m "feat: add orchestrator domain models"
```

### Task 3: Implement runtime state persistence

**Files:**
- Modify: `D:/fqcex/src/perp_platform/orchestrator/runtime_state.py`
- Test: `D:/fqcex/tests/orchestrator/test_runtime_state.py`

**Step 1: Write the failing test**

```python
from pathlib import Path

from perp_platform.orchestrator.models import OrchestratorState, WorkItem
from perp_platform.orchestrator.runtime_state import load_state, save_state


def test_runtime_state_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "state.json"
    work_item = WorkItem(issue_id=29, issue_title="issue", tracking_issue_id=11, status=OrchestratorState.CLAIMED)

    save_state(path, work_item)
    loaded = load_state(path)

    assert loaded.issue_id == 29
    assert loaded.status is OrchestratorState.CLAIMED
```
```

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/orchestrator/test_runtime_state.py -q`
Expected: FAIL because `load_state` / `save_state` do not exist

**Step 3: Write minimal implementation**

```python
import json
from dataclasses import asdict
from pathlib import Path

from .models import OrchestratorState, WorkItem


def save_state(path: Path, work_item: WorkItem) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asdict(work_item), indent=2), encoding="utf-8")


def load_state(path: Path) -> WorkItem:
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["status"] = OrchestratorState(payload["status"])
    return WorkItem(**payload)
```

Extend this task so runtime state can also store and restore an `approval_bundle_id` reference without embedding the full bundle payload.

**Step 4: Run test to verify it passes**

Run: `py -m pytest tests/orchestrator/test_runtime_state.py -q`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/orchestrator/test_runtime_state.py src/perp_platform/orchestrator/runtime_state.py
git commit -m "feat: persist orchestrator runtime state"
```

### Task 4: Encode deterministic next-issue selection

**Files:**
- Modify: `D:/fqcex/src/perp_platform/orchestrator/sequence.py`
- Test: `D:/fqcex/tests/orchestrator/test_sequence.py`

**Step 1: Write the failing test**

```python
from perp_platform.orchestrator.models import WorkItem
from perp_platform.orchestrator.sequence import select_next_ready_issue


def test_select_next_ready_issue_uses_first_open_child_after_closed_siblings() -> None:
    work_items = [
        WorkItem(issue_id=28, issue_title="closed", tracking_issue_id=11, status="closed"),
        WorkItem(issue_id=29, issue_title="ready", tracking_issue_id=11),
        WorkItem(issue_id=30, issue_title="blocked-by-order", tracking_issue_id=11),
    ]

    selected = select_next_ready_issue(work_items, closed_issue_ids={28})

    assert selected.issue_id == 29
```
```

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/orchestrator/test_sequence.py -q`
Expected: FAIL because selector does not exist

**Step 3: Write minimal implementation**

```python
from .models import WorkItem


def select_next_ready_issue(work_items: list[WorkItem], closed_issue_ids: set[int]) -> WorkItem | None:
    for work_item in work_items:
        if work_item.issue_id in closed_issue_ids:
            continue
        return work_item
    return None
```

Then refine the selector so it only returns the first open child whose earlier siblings are closed.

**Step 4: Run test to verify it passes**

Run: `py -m pytest tests/orchestrator/test_sequence.py -q`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/orchestrator/test_sequence.py src/perp_platform/orchestrator/sequence.py
git commit -m "feat: add deterministic next-issue selection"
```

### Task 5: Add dispatch payload builder

**Files:**
- Modify: `D:/fqcex/src/perp_platform/orchestrator/dispatcher.py`
- Test: `D:/fqcex/tests/orchestrator/test_dispatcher.py`

**Step 1: Write the failing test**

```python
from perp_platform.orchestrator.dispatcher import build_owner_dispatch_payload
from perp_platform.orchestrator.models import ApprovalBundle, WorkItem


def test_owner_dispatch_payload_contains_model_and_scope() -> None:
    work_item = WorkItem(issue_id=29, issue_title="Quantity", tracking_issue_id=11)
    approval_bundle = ApprovalBundle(
        bundle_id="exec-2026-03-19-001",
        approved_by_user=True,
        approved_at="2026-03-19T10:00:00+08:00",
        scope_label="issues_29_to_33",
        issue_start=29,
        issue_end=33,
        execution_mode="proceed_with_recommended_defaults",
        issue_parallelism=1,
        write_agents_per_issue=1,
        read_only_sidecars_per_issue=2,
        merge_policy="auto_merge_main",
        close_policy="auto_close_child_and_update_tracking",
        reporting_policy="issue_completion_or_blocked_only",
        pause_only_on=("sibling_issue_required",),
        recommended_defaults=("recommended",),
        model="gpt-5.4",
        reasoning_effort="xhigh",
    )

    payload = build_owner_dispatch_payload(
        work_item=work_item,
        approval_bundle=approval_bundle,
        worktree_path="D:/fqcex/.worktrees/issue-29",
        allowed_files=["src/perp_platform/domain/quantity.py"],
        acceptance_checks=["py -m pytest tests/perp_platform/test_quantity.py -q"],
    )

    assert payload["model"] == "gpt-5.4"
    assert payload["reasoning_effort"] == "xhigh"
    assert payload["approval_bundle_id"] == "exec-2026-03-19-001"
    assert payload["issue_id"] == 29
```
```

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/orchestrator/test_dispatcher.py -q`
Expected: FAIL because payload builder does not exist

**Step 3: Write minimal implementation**

```python
from .models import WorkItem


def build_owner_dispatch_payload(
    *,
    work_item: WorkItem,
    worktree_path: str,
    allowed_files: list[str],
    acceptance_checks: list[str],
) -> dict[str, object]:
    return {
        "issue_id": work_item.issue_id,
        "issue_title": work_item.issue_title,
        "worktree_path": worktree_path,
        "allowed_files": allowed_files,
        "acceptance_checks": acceptance_checks,
        "model": "gpt-5.4",
        "reasoning_effort": "xhigh",
    }
```

**Step 4: Run test to verify it passes**

Run: `py -m pytest tests/orchestrator/test_dispatcher.py -q`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/orchestrator/test_dispatcher.py src/perp_platform/orchestrator/dispatcher.py
git commit -m "feat: add orchestrator dispatch payload builder"
```

### Task 6: Add runtime status CLI

**Files:**
- Create: `D:/fqcex/scripts/issue_orchestrator.py`
- Test: `D:/fqcex/tests/orchestrator/test_cli_status.py`

**Step 1: Write the failing test**

```python
from pathlib import Path
import subprocess
import sys


def test_issue_orchestrator_status_reads_runtime_state(tmp_path: Path) -> None:
    state_path = tmp_path / "state.json"
    state_path.write_text('{"issue_id": 29, "issue_title": "Quantity", "tracking_issue_id": 11, "status": "claimed", "owner_agent_id": null}', encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "scripts/issue_orchestrator.py", "status", "--state-path", str(state_path)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "29" in result.stdout
    assert "claimed" in result.stdout
```
```

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/orchestrator/test_cli_status.py -q`
Expected: FAIL because the CLI script does not exist

**Step 3: Write minimal implementation**

```python
from pathlib import Path
import argparse

from perp_platform.orchestrator.runtime_state import load_state


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["status"])
    parser.add_argument("--state-path", default=".codex/orchestrator/state.json")
    args = parser.parse_args()

    if args.command == "status":
        work_item = load_state(Path(args.state_path))
        print(f"{work_item.issue_id} {work_item.status}")
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
```

**Step 4: Run test to verify it passes**

Run: `py -m pytest tests/orchestrator/test_cli_status.py -q`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/orchestrator/test_cli_status.py scripts/issue_orchestrator.py
git commit -m "feat: add orchestrator status cli"
```

### Task 7: Add `next` and `claim` CLI commands

**Files:**
- Modify: `D:/fqcex/scripts/issue_orchestrator.py`
- Modify: `D:/fqcex/src/perp_platform/orchestrator/github_state.py`
- Modify: `D:/fqcex/src/perp_platform/orchestrator/sequence.py`
- Test: `D:/fqcex/tests/orchestrator/test_cli_next_claim.py`

**Step 1: Write the failing test**

```python
def test_cli_next_prints_unique_ready_issue():
    ...


def test_cli_claim_persists_claimed_state():
    ...
```
```

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/orchestrator/test_cli_next_claim.py -q`
Expected: FAIL because `next` and `claim` are not implemented

**Step 3: Write minimal implementation**

Implement:

- `github_state.py` parser for issue metadata returned by `gh issue view` / `gh issue list`
- `sequence.py` rule that rejects non-`type/task` issues and already-closed siblings
- CLI `next`
- CLI `claim <issue>`
- persistence of `CLAIMED` state to `.codex/orchestrator/state.json`

**Step 4: Run test to verify it passes**

Run: `py -m pytest tests/orchestrator/test_cli_next_claim.py -q`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/orchestrator/test_cli_next_claim.py scripts/issue_orchestrator.py src/perp_platform/orchestrator/github_state.py src/perp_platform/orchestrator/sequence.py
git commit -m "feat: add next and claim orchestration commands"
```

### Task 8: Add `prepare` dispatch generation

**Files:**
- Modify: `D:/fqcex/scripts/issue_orchestrator.py`
- Modify: `D:/fqcex/src/perp_platform/orchestrator/dispatcher.py`
- Test: `D:/fqcex/tests/orchestrator/test_cli_prepare.py`

**Step 1: Write the failing test**

```python
def test_cli_prepare_outputs_worktree_branch_and_dispatch_payload():
    ...
```
```

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/orchestrator/test_cli_prepare.py -q`
Expected: FAIL because `prepare` is not implemented

**Step 3: Write minimal implementation**

Implement:

- branch naming with `codex/`
- worktree path generation under `.worktrees/`
- owner dispatch payload output
- placeholder sidecar payload output for explorer / verifier / reviewer
- frozen approval fields in every owner payload:
  - `approved_design = true`
  - `approval_owner = "master_agent"`
  - `execution_mode = "proceed_with_recommended_defaults"`
  - `recommended_defaults`
  - `escalation_triggers`
- approval bundle reference fields:
  - `approval_bundle_id`
  - `merge_policy`
  - `close_policy`
  - `reporting_policy`

**Step 4: Run test to verify it passes**

Run: `py -m pytest tests/orchestrator/test_cli_prepare.py -q`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/orchestrator/test_cli_prepare.py scripts/issue_orchestrator.py src/perp_platform/orchestrator/dispatcher.py
git commit -m "feat: add orchestrator prepare command"
```

### Task 9: Add approval bundle persistence and CLI

**Files:**
- Modify: `D:/fqcex/src/perp_platform/orchestrator/models.py`
- Modify: `D:/fqcex/src/perp_platform/orchestrator/runtime_state.py`
- Modify: `D:/fqcex/scripts/issue_orchestrator.py`
- Create: `D:/fqcex/tests/orchestrator/test_approval_bundle.py`

**Step 1: Write the failing test**

```python
from pathlib import Path

from perp_platform.orchestrator.runtime_state import load_approval_bundle, save_approval_bundle
from perp_platform.orchestrator.models import ApprovalBundle


def test_approval_bundle_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "approval_bundle.json"
    bundle = ApprovalBundle(
        bundle_id="exec-2026-03-19-001",
        approved_by_user=True,
        approved_at="2026-03-19T10:00:00+08:00",
        scope_label="issues_30_to_33",
        issue_start=30,
        issue_end=33,
        execution_mode="proceed_with_recommended_defaults",
        issue_parallelism=1,
        write_agents_per_issue=1,
        read_only_sidecars_per_issue=2,
        merge_policy="auto_merge_main",
        close_policy="auto_close_child_and_update_tracking",
        reporting_policy="issue_completion_or_blocked_only",
        pause_only_on=("sibling_issue_required",),
        recommended_defaults=("recommended",),
        model="gpt-5.4",
        reasoning_effort="xhigh",
    )

    save_approval_bundle(path, bundle)
    loaded = load_approval_bundle(path)

    assert loaded.bundle_id == "exec-2026-03-19-001"
    assert loaded.issue_start == 30
    assert loaded.model == "gpt-5.4"
```

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/orchestrator/test_approval_bundle.py -q`
Expected: FAIL because `ApprovalBundle` or approval bundle persistence does not exist

**Step 3: Write minimal implementation**

Implement:

- `ApprovalBundle` in `models.py`
- `save_approval_bundle` and `load_approval_bundle` in `runtime_state.py`
- CLI subcommands:
  - `approval create --issue-start <n> --issue-end <n>`
  - `approval show`
  - `approval check --issue <n>`
- default approval bundle values fixed to:
  - `gpt-5.4`
  - `xhigh`
  - single writer
  - two read-only sidecars

**Step 4: Run test to verify it passes**

Run: `py -m pytest tests/orchestrator/test_approval_bundle.py -q`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/orchestrator/test_approval_bundle.py scripts/issue_orchestrator.py src/perp_platform/orchestrator/models.py src/perp_platform/orchestrator/runtime_state.py
git commit -m "feat: add approval bundle persistence and cli"
```

### Task 10: Add acceptance guardrails

**Files:**
- Modify: `D:/fqcex/scripts/issue_orchestrator.py`
- Modify: `D:/fqcex/src/perp_platform/orchestrator/runtime_state.py`
- Create: `D:/fqcex/tests/orchestrator/test_cli_accept.py`

**Step 1: Write the failing test**

```python
def test_cli_accept_rejects_head_sha_mismatch():
    ...


def test_cli_accept_rejects_issue_boundary_violation():
    ...
```
```

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/orchestrator/test_cli_accept.py -q`
Expected: FAIL because `accept` is not implemented

**Step 3: Write minimal implementation**

Implement:

- runtime state fields for `base_sha` and `head_sha`
- CLI `accept <issue>`
- checks for issue id match, SHA match, allowed files, required review evidence marker, and expected acceptance checks list presence

**Step 4: Run test to verify it passes**

Run: `py -m pytest tests/orchestrator/test_cli_accept.py -q`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/orchestrator/test_cli_accept.py scripts/issue_orchestrator.py src/perp_platform/orchestrator/runtime_state.py
git commit -m "feat: add orchestrator acceptance guardrails"
```

### Task 11: Add block and close lifecycle commands

**Files:**
- Modify: `D:/fqcex/scripts/issue_orchestrator.py`
- Modify: `D:/fqcex/src/perp_platform/orchestrator/runtime_state.py`
- Create: `D:/fqcex/tests/orchestrator/test_cli_block_close.py`

**Step 1: Write the failing test**

```python
def test_cli_block_records_reason():
    ...


def test_cli_close_clears_runtime_state():
    ...
```
```

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/orchestrator/test_cli_block_close.py -q`
Expected: FAIL because `block` and `close` are not implemented

**Step 3: Write minimal implementation**

Implement:

- `block <issue>` to persist blocker reason and status
- `close <issue>` to clear active state after merge / close
- keep GitHub close / tracking checklist update as explicit human or master-agent follow-up, not hidden CLI side effects

**Step 4: Run test to verify it passes**

Run: `py -m pytest tests/orchestrator/test_cli_block_close.py -q`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/orchestrator/test_cli_block_close.py scripts/issue_orchestrator.py src/perp_platform/orchestrator/runtime_state.py
git commit -m "feat: add orchestrator block and close commands"
```

### Task 12: Document operating procedure

**Files:**
- Create: `D:/fqcex/docs/runbooks/issue-orchestrator.md`
- Test: `D:/fqcex/tests/governance/test_issue_orchestrator_runbook_contract.py`

**Step 1: Write the failing test**

```python
def test_issue_orchestrator_runbook_mentions_single_writer_and_gpt_5_4_xhigh():
    ...
```
```

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/governance/test_issue_orchestrator_runbook_contract.py -q`
Expected: FAIL because the runbook does not exist

**Step 3: Write minimal implementation**

Document:

- required sequence rules
- necessary concurrency rules
- `gpt-5.4` / `xhigh` requirement
- state transitions
- acceptance and blocker handling
- what the master agent may and may not delegate
- approval delegation policy:
  - only the master agent gets user design approval
  - subagents must execute approved defaults without re-asking the user
  - subagents only escalate on defined governance, scope, or architecture triggers
- execution approval template:
  - one-shot confirmation checklist
  - recommended default values
  - standard approval wording
  - approval bundle fields stored and passed to subagents

**Step 4: Run test to verify it passes**

Run: `py -m pytest tests/governance/test_issue_orchestrator_runbook_contract.py -q`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/governance/test_issue_orchestrator_runbook_contract.py docs/runbooks/issue-orchestrator.md
git commit -m "docs: add issue orchestrator runbook"
```

### Task 13: Full verification

**Files:**
- Verify only: `D:/fqcex/tests/orchestrator`
- Verify only: `D:/fqcex/tests/governance`

**Step 1: Run orchestrator test suite**

Run: `py -m pytest tests/orchestrator -q`
Expected: PASS

**Step 2: Run governance contract tests**

Run: `py -m pytest tests/governance -q`
Expected: PASS

**Step 3: Run full repository tests**

Run: `py -m pytest tests -q`
Expected: PASS

**Step 4: Manually smoke the CLI**

Run: `py scripts/issue_orchestrator.py status --state-path .codex/orchestrator/state.json`
Expected: Returns `0` and prints current state or a clear missing-state message

**Step 5: Commit**

```bash
git add .
git commit -m "test: verify issue orchestrator end to end"
```
