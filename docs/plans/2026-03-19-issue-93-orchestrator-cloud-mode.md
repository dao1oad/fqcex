# Issue #93 Orchestrator Cloud Mode Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a cloud-friendly orchestrator mode that can dispatch and accept issue work using a portable JSON pack instead of depending on a local `.codex/orchestrator/state.json` file.

**Architecture:** Keep the current local orchestrator mode intact. Extend `prepare`, `start`, and `accept` so they can produce and consume a portable dispatch pack that carries claim and acceptance metadata, then document the cloud-mode command path in the orchestrator runbook.

**Tech Stack:** Python 3.12, argparse CLI, dataclasses, pytest, Markdown docs

---

### Task 1: Add failing tests for portable dispatch and cloud acceptance

**Files:**
- Modify: `tests/orchestrator/test_cli_prepare_dispatch_pack.py`
- Modify: `tests/orchestrator/test_cli_start.py`
- Modify: `tests/orchestrator/test_cli_accept.py`
- Modify: `tests/governance/test_issue_orchestrator_runbook_contract.py`

**Step 1: Write the failing tests**

Cover:

- `prepare` emits `claim_record` and `acceptance_payload`
- `prepare` accepts repeated `--allowed-file`, `--forbidden-file`, `--acceptance-check`
- `start --skip-state-save --dispatch-path ...` writes a portable dispatch pack but does not create `state.json`
- `accept --dispatch-path ...` accepts without a local runtime state file
- the runbook mentions `skip-state-save`, `dispatch-path`, and `accept --dispatch-path`

**Step 2: Run tests to verify they fail**

Run:

- `py -m pytest tests/orchestrator/test_cli_prepare_dispatch_pack.py -q`
- `py -m pytest tests/orchestrator/test_cli_start.py -q`
- `py -m pytest tests/orchestrator/test_cli_accept.py -q`
- `py -m pytest tests/governance/test_issue_orchestrator_runbook_contract.py -q`

Expected: FAIL because the CLI and runbook do not yet implement cloud mode

### Task 2: Extend dispatcher payload and CLI arguments

**Files:**
- Modify: `src/perp_platform/orchestrator/dispatcher.py`
- Modify: `scripts/issue_orchestrator.py`

**Step 1: Write minimal implementation**

- Add `claim_record` and `acceptance_payload` to the dispatch pack
- Add repeated boundary arguments:
  - `--allowed-file`
  - `--forbidden-file`
  - `--acceptance-check`
- Add optional `--dispatch-path`
- Add `--skip-state-save` to `start`

**Step 2: Run targeted tests**

Run:

- `py -m pytest tests/orchestrator/test_cli_prepare_dispatch_pack.py -q`
- `py -m pytest tests/orchestrator/test_cli_start.py -q`

Expected: partial PASS while `accept` and runbook tests may still fail

### Task 3: Add acceptance without local runtime state

**Files:**
- Modify: `scripts/issue_orchestrator.py`

**Step 1: Write minimal implementation**

- Extend `accept` so `--dispatch-path` can replace `--state-path`
- Reconstruct issue id and allowed-files boundary from the dispatch pack
- Continue requiring explicit `head_sha`, changed-files evidence, and non-empty review evidence

**Step 2: Run targeted tests**

Run:

- `py -m pytest tests/orchestrator/test_cli_accept.py -q`

Expected: PASS

### Task 4: Update the runbook

**Files:**
- Modify: `docs/runbooks/issue-orchestrator.md`

**Step 1: Write minimal documentation**

Document:

- local mode vs cloud mode
- `start --skip-state-save --dispatch-path ...`
- `accept --dispatch-path ...`
- portable dispatch pack as the cloud handoff unit

**Step 2: Run the runbook contract test**

Run:

- `py -m pytest tests/governance/test_issue_orchestrator_runbook_contract.py -q`

Expected: PASS

### Task 5: Run orchestrator and full verification

**Files:**
- No code changes expected

**Step 1: Run orchestrator tests**

Run:

- `py -m pytest tests/orchestrator -q`

Expected: PASS

**Step 2: Run the full suite**

Run:

- `py -m pytest tests -q`

Expected: PASS

### Task 6: Prepare issue handoff

**Files:**
- No code changes expected

**Step 1: Capture delivery**

Summarize:

- changed files
- commands run
- test results
- residual risks for `#94`

**Step 2: Keep worktree ready for master-agent acceptance**

Do not change `.codex/` local state and do not touch Bybit runtime files.
