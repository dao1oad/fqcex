# Issue 64 Dry Run Audit Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 增加 dry-run 审计采集脚本，并把 operator checklist 写进 deploy / rollback runbook。

**Architecture:** 单文件 CLI 脚本输出结构化 JSON 审计记录；runbook 只补操作步骤和留痕要求。

**Tech Stack:** Python 3.12, argparse, json, pytest, Markdown

---

### Task 1: Add failing audit capture tests

**Files:**
- Create: `tests/ops/test_capture_dry_run_audit.py`

Run: `py -m pytest tests/ops/test_capture_dry_run_audit.py -q`

Expected: FAIL because `scripts/capture_dry_run_audit.py` does not exist yet.

### Task 2: Implement audit capture script

**Files:**
- Create: `scripts/capture_dry_run_audit.py`
- Test: `tests/ops/test_capture_dry_run_audit.py`

### Task 3: Update runbooks

**Files:**
- Modify: `docs/runbooks/deploy.md`
- Modify: `docs/runbooks/rollback.md`

### Task 4: Verify end to end

Run: `py -m pytest tests -q`

Expected: PASS
