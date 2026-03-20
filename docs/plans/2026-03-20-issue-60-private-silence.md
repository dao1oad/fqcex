# Issue 60 Private Silence Injector Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 增加一个可输出标准化私有流静默注入计划的 CLI 脚本。

**Architecture:** 单文件 Python CLI 接收 venue / duration / scope，输出 JSON 注入计划到 stdout 或文件；测试通过子进程调用脚本验证返回码与 JSON。

**Tech Stack:** Python 3.12, argparse, json, pytest

---

### Task 1: Add failing tests

**Files:**
- Create: `tests/ops/test_private_silence_injector.py`

**Step 1: Write the failing test**

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/ops/test_private_silence_injector.py -q`

Expected: FAIL because `scripts/inject_private_silence.py` does not exist yet.

### Task 2: Implement CLI injector

**Files:**
- Create: `scripts/inject_private_silence.py`
- Test: `tests/ops/test_private_silence_injector.py`

**Step 1: Write minimal implementation**

**Step 2: Run test to verify it passes**

Run: `py -m pytest tests/ops/test_private_silence_injector.py -q`

Expected: PASS

### Task 3: Verify end to end

**Files:**
- Modify: `docs/plans/2026-03-20-issue-60-private-silence-design.md`
- Modify: `docs/plans/2026-03-20-issue-60-private-silence.md`

**Step 1: Run targeted tests**

Run: `py -m pytest tests/ops/test_private_silence_injector.py -q`

Expected: PASS

**Step 2: Run full test suite**

Run: `py -m pytest tests -q`

Expected: PASS

**Step 3: Final commit**

```bash
git add scripts/inject_private_silence.py tests/ops/test_private_silence_injector.py docs/plans/2026-03-20-issue-60-private-silence-design.md docs/plans/2026-03-20-issue-60-private-silence.md
git commit -m "feat: add private silence injector"
```
