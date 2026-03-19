# Issue #92 Codex Cloud Environment / Secrets / Network Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Freeze Codex cloud environment, secrets, and agent internet access rules for this repository without changing orchestrator code or any trading runtime implementation.

**Architecture:** Add one architecture document and one runbook that define the two-phase Codex cloud runtime model, allowed non-sensitive environment variables, setup-only secret usage, and a fail-closed agent internet policy. Update repository entry docs and lock the contract with a governance test.

**Tech Stack:** Markdown docs, pytest governance tests, GitHub issue governance

---

### Task 1: Add the failing governance contract test

**Files:**
- Create: `tests/governance/test_codex_cloud_security_contract.py`

**Step 1: Write the failing test**

Add tests that assert:

- `SECURITY.md` documents Codex cloud environment and secrets boundaries
- `docs/architecture/CODEX_CLOUD_BOUNDARIES.md` exists and freezes the two-phase runtime model
- `docs/runbooks/codex-cloud-security.md` exists and documents recommended environment variables plus network allowlist / HTTP method restrictions
- `README.md` links the new documents and states that live trading credentials do not belong in Codex cloud

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/governance/test_codex_cloud_security_contract.py -q`
Expected: FAIL because the new documents and README / SECURITY contract do not exist yet

### Task 2: Add the architecture and runbook documents

**Files:**
- Create: `docs/architecture/CODEX_CLOUD_BOUNDARIES.md`
- Create: `docs/runbooks/codex-cloud-security.md`

**Step 1: Write minimal implementation**

Document:

- setup script vs agent phase runtime split
- environment variables available for the whole task
- secrets available only during setup
- agent internet access defaulting to `Off`
- restricted allowlist / HTTP methods for exceptional tasks
- explicit ban on live exchange credentials and live venue APIs

**Step 2: Run the targeted test**

Run: `python -m pytest tests/governance/test_codex_cloud_security_contract.py -q`
Expected: still FAIL because repository entry docs are not updated yet

### Task 3: Update repository entry docs

**Files:**
- Modify: `README.md`
- Modify: `SECURITY.md`
- Modify: `docs/runbooks/codex-cloud-setup.md`

**Step 1: Write minimal documentation updates**

- `README.md`
  - link the new architecture and runbook documents
  - describe the non-sensitive environment variable policy
  - state that live exchange credentials are out of bounds for cloud tasks
- `SECURITY.md`
  - add a Codex cloud section covering environment variables, setup-only secrets, and network defaults
- `docs/runbooks/codex-cloud-setup.md`
  - cross-link the new security runbook and architecture page

**Step 2: Run the targeted test**

Run: `python -m pytest tests/governance/test_codex_cloud_security_contract.py -q`
Expected: PASS

### Task 4: Run governance and full verification

**Files:**
- No code changes expected

**Step 1: Run governance tests**

Run: `python -m pytest tests/governance -q`
Expected: PASS

**Step 2: Run full test suite**

Run: `python -m pytest tests -q`
Expected: PASS

### Task 5: Prepare handoff for master-agent acceptance

**Files:**
- No code changes expected

**Step 1: Capture delivery**

Summarize:

- changed files
- commands run
- test results
- any blockers or residual risks

**Step 2: Keep the worktree boundary clean**

Do not modify orchestrator code, runtime code, or `.codex/` local state.
