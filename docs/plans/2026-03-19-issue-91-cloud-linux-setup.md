# Issue #91 Codex Cloud Linux Setup Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a Linux/Bash-compatible repository setup entry point and standardize setup and verification documentation around `python -m ...` commands.

**Architecture:** Keep the change at the repository edge. Add one Bash setup script, update the primary onboarding and runbook docs to point at Linux/Bash-compatible commands, and lock the contract with a governance test. Do not change runtime or cloud-state logic.

**Tech Stack:** Python 3.12, Bash, pytest, Markdown docs

---

### Task 1: Add the failing governance contract test

**Files:**
- Create: `tests/governance/test_codex_cloud_setup_contract.py`

**Step 1: Write the failing test**

Add tests that assert:

- `scripts/codex_cloud_setup.sh` exists
- the script contains `python -m pip install -e .`
- `README.md` mentions Codex cloud or Linux/Bash setup and `python -m pytest tests -q`
- `AGENTS.md` contains `python scripts/update_project_memory.py`
- `AGENTS.md` marks `scripts/project_context.ps1` as optional and Windows-only

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/governance/test_codex_cloud_setup_contract.py -q`
Expected: FAIL because the script and updated docs do not exist yet

### Task 2: Add the Bash setup entry point

**Files:**
- Create: `scripts/codex_cloud_setup.sh`

**Step 1: Write minimal implementation**

Create a Bash script with:

- shebang `#!/usr/bin/env bash`
- `set -euo pipefail`
- `python -m pip install --upgrade pip`
- `python -m pip install -e .`

**Step 2: Run the targeted test**

Run: `python -m pytest tests/governance/test_codex_cloud_setup_contract.py -q`
Expected: still FAIL because the docs are not updated yet

### Task 3: Update the documented setup and verification path

**Files:**
- Modify: `README.md`
- Modify: `AGENTS.md`
- Create: `docs/runbooks/codex-cloud-setup.md`

**Step 1: Write minimal documentation updates**

- `README.md`
  - add Linux/Bash and Codex cloud setup steps using `python -m ...`
  - document `python -m pytest tests -q`
  - keep the PowerShell context script as optional Windows local usage
- `AGENTS.md`
  - update memory recovery step `4` to `python scripts/update_project_memory.py`
  - mark step `6` as optional Windows-only PowerShell convenience
- `docs/runbooks/codex-cloud-setup.md`
  - document the Bash setup script and verification command

**Step 2: Run the targeted test**

Run: `python -m pytest tests/governance/test_codex_cloud_setup_contract.py -q`
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

### Task 5: Prepare issue handoff

**Files:**
- No code changes expected

**Step 1: Summarize delivery**

Capture:

- changed files
- commands run
- test results
- blockers

**Step 2: Keep worktree ready for master-agent acceptance**

Do not modify files outside the allowed boundary.
