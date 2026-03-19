# Issue #94 Codex Cloud Dry Run Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Establish the operator-facing GitHub -> Codex cloud workflow, run one auditable dry run, and record the evidence so later child issues can move from local execution to cloud execution.

**Architecture:** Keep code changes out of the trading runtime. Update contribution and PR entry points, add one dry-run runbook and one governance test, then use the real `#94` branch PR to trigger a bounded Codex cloud task and write the evidence back into the runbook.

**Tech Stack:** Markdown docs, GitHub PR workflow, pytest governance tests

---

### Task 1: Add the failing governance contract test

**Files:**
- Create: `tests/governance/test_codex_cloud_dry_run_contract.py`

**Step 1: Write the failing test**

Assert that:

- `CONTRIBUTING.md` documents the Codex cloud PR workflow
- `.github/PULL_REQUEST_TEMPLATE.md` contains a `Codex Cloud Evidence` section
- `docs/runbooks/codex-cloud-dry-run.md` exists and contains a `Dry Run Record`

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/governance/test_codex_cloud_dry_run_contract.py -q`
Expected: FAIL because the workflow docs and runbook do not exist yet

### Task 2: Add workflow docs and PR template changes

**Files:**
- Modify: `CONTRIBUTING.md`
- Modify: `.github/PULL_REQUEST_TEMPLATE.md`
- Create: `docs/runbooks/codex-cloud-dry-run.md`

**Step 1: Write minimal implementation**

- add `Codex Cloud Workflow` to `CONTRIBUTING.md`
- add `Codex Cloud Evidence` to the PR template
- add the dry-run runbook with prerequisites, trigger steps, rollback path, and an empty evidence section

**Step 2: Run the targeted test**

Run: `py -m pytest tests/governance/test_codex_cloud_dry_run_contract.py -q`
Expected: PASS

### Task 3: Run governance verification

**Files:**
- No code changes expected

**Step 1: Run governance tests**

Run: `py -m pytest tests/governance -q`
Expected: PASS

### Task 4: Create the real dry-run PR and trigger Codex cloud

**Files:**
- No repository file changes yet

**Step 1: Push the branch and open a PR**

Use `gh` to create a PR for `codex/issue-94-cloud-dry-run`.

**Step 2: Trigger a bounded Codex cloud task**

Post a PR comment like:

`@codex summarize the cloud handoff in this PR and confirm whether later child issues can be executed in Codex cloud using the documented workflow. Do not make code changes.`

**Step 3: Wait for Codex response**

Capture:

- PR URL
- trigger comment URL
- Codex response URL
- outcome

### Task 5: Record dry-run evidence in the runbook

**Files:**
- Modify: `docs/runbooks/codex-cloud-dry-run.md`

**Step 1: Write the actual evidence**

Fill in the dry-run record with the real URLs and outcome.

**Step 2: Re-run the targeted test and governance tests**

Run:

- `py -m pytest tests/governance/test_codex_cloud_dry_run_contract.py -q`
- `py -m pytest tests/governance -q`

Expected: PASS

### Task 6: Final verification and handoff

**Files:**
- No code changes expected

**Step 1: Run full test suite**

Run: `py -m pytest tests -q`
Expected: PASS

**Step 2: Prepare cloud switch handoff**

Capture:

- PR URL
- dry-run evidence URLs
- next issue to execute in cloud (`#32`)
- any residual blockers
