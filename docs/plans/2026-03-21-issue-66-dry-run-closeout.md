# Issue 66 Dry Run Closeout Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 产出 Phase 3 干跑演练的结项报告与发现总结。

**Architecture:** 只消费已存在的 `docs/plans/dry-run-evidence.md` 和 `docs/plans/dry-run-evidence/*.json`，把事实汇总成一份 closeout 文档，并用契约测试锁定核心结论。

**Tech Stack:** Python 3.12, pytest, Markdown

---

### Task 1: Add failing closeout contract test

**Files:**
- Create: `tests/ops/test_dry_run_closeout_contract.py`

Run: `py -m pytest tests/ops/test_dry_run_closeout_contract.py -q`

Expected: FAIL because `docs/plans/dry-run-closeout.md` does not exist yet.

### Task 2: Write the closeout document

**Files:**
- Create: `docs/plans/dry-run-closeout.md`

Document:
- scope statement
- completed rehearsal matrix summary
- findings
- residual risk
- follow-up input for next phase

### Task 3: Verify and commit

**Files:**
- Modify: `docs/plans/2026-03-21-issue-66-dry-run-closeout-design.md`
- Modify: `docs/plans/2026-03-21-issue-66-dry-run-closeout.md`
- Test: `tests/ops/test_dry_run_closeout_contract.py`

Run:
- `py -m pytest tests/ops/test_dry_run_closeout_contract.py -q`
- `py scripts/update_project_memory.py`
- `py -m pytest tests -q`

Expected: PASS
