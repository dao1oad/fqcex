# Issue 61 Reconcile Diff Injector Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 增加一个可输出标准化对账差异注入计划的 CLI 脚本。

**Architecture:** 单文件 Python CLI 接收 venue / resource / diff kind / instrument 参数，输出 JSON 到 stdout 或文件；测试通过子进程验证脚本返回码与 JSON 内容。

**Tech Stack:** Python 3.12, argparse, json, pytest

---

### Task 1: Add failing tests

**Files:**
- Create: `tests/ops/test_reconcile_diff_injector.py`

**Step 1: Write the failing test**

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/ops/test_reconcile_diff_injector.py -q`

Expected: FAIL because `scripts/inject_reconcile_diff.py` does not exist yet.

### Task 2: Implement CLI injector

**Files:**
- Create: `scripts/inject_reconcile_diff.py`
- Test: `tests/ops/test_reconcile_diff_injector.py`

**Step 1: Write minimal implementation**

**Step 2: Run test to verify it passes**

Run: `py -m pytest tests/ops/test_reconcile_diff_injector.py -q`

Expected: PASS

### Task 3: Verify end to end

**Files:**
- Modify: `docs/plans/2026-03-20-issue-61-reconcile-diff-design.md`
- Modify: `docs/plans/2026-03-20-issue-61-reconcile-diff.md`

**Step 1: Run targeted tests**

Run: `py -m pytest tests/ops/test_reconcile_diff_injector.py -q`

Expected: PASS

**Step 2: Run full test suite**

Run: `py -m pytest tests -q`

Expected: PASS

**Step 3: Final commit**

```bash
git add scripts/inject_reconcile_diff.py tests/ops/test_reconcile_diff_injector.py docs/plans/2026-03-20-issue-61-reconcile-diff-design.md docs/plans/2026-03-20-issue-61-reconcile-diff.md
git commit -m "feat: add reconcile diff injector"
```
