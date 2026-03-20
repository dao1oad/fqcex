# Issue 50 Binance Smoke And Recovery Consistency Tests Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 Binance runtime 增加 smoke 与 recovery consistency tests，冻结当前最小闭环行为。

**Architecture:** 只写测试，不改生产代码；通过 bootstrap smoke 与 recovery consistency 两组用例把 Phase 2 的 Binance runtime contract 固定下来。

**Tech Stack:** Python 3.12、pytest

---

### Task 1: Add failing Binance smoke and consistency tests

**Files:**
- Create: `tests/perp_platform/binance/test_bootstrap.py`
- Create: `tests/perp_platform/binance/test_recovery_consistency.py`

**Step 1: Write the failing tests**

- bootstrap smoke
- recovery consistency

**Step 2: Run targeted tests to verify failure**

Run:

```bash
py -m pytest tests/perp_platform/binance -q
```

Expected:
- FAIL，因为新测试文件中的断言还未由现有 contract 覆盖完全

**Step 3: Commit**

```bash
git add tests/perp_platform/binance/test_bootstrap.py tests/perp_platform/binance/test_recovery_consistency.py
git commit -m "test: define binance smoke and recovery consistency"
```

### Task 2: Adjust tests until they match the merged runtime contract

**Files:**
- Modify: `tests/perp_platform/binance/test_bootstrap.py`
- Modify: `tests/perp_platform/binance/test_recovery_consistency.py`

**Step 1: Run targeted tests**

Run:

```bash
py -m pytest tests/perp_platform/binance -q
```

Expected:
- PASS

**Step 2: Confirm no production-code changes are needed**

- 不修改 `src/perp_platform/runtime/binance/*`

**Step 3: Commit**

```bash
git add tests/perp_platform/binance/test_bootstrap.py tests/perp_platform/binance/test_recovery_consistency.py
git commit -m "test: add binance runtime smoke coverage"
```

### Task 3: Verify full Binance scope

**Files:**
- Verify only

**Step 1: Run Binance suite**

Run:

```bash
py -m pytest tests/perp_platform/binance -q
```

Expected:
- PASS

**Step 2: Run broader regression**

Run:

```bash
py -m pytest tests/perp_platform -q
py -m pytest tests -q
```

Expected:
- PASS

**Step 3: Commit**

```bash
git add docs/plans/2026-03-20-issue-50-binance-smoke-design.md docs/plans/2026-03-20-issue-50-binance-smoke.md
git commit -m "docs: add issue 50 binance test plan"
```
