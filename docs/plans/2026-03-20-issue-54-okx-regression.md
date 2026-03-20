# Issue 54 OKX Runtime Regression Test Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 OKX venue 增加 package 级启动与换算回归测试，确保 bootstrap/conversion/guards 在公开 API 视角下保持一致。

**Architecture:** 不改生产代码，只在 `tests/perp_platform/okx` 下增加回归用例，把公开 package 导出和跨模块协同钉住。

**Tech Stack:** Python 3.12、pytest、Decimal

---

### Task 1: Add failing OKX regression tests

**Files:**
- Create: `tests/perp_platform/okx/test_bootstrap.py`
- Create: `tests/perp_platform/okx/test_runtime_regression.py`

**Step 1: Write the failing tests**

- package 顶层 bootstrap 回归
- conversion + guards 联合回归

**Step 2: Run targeted tests to verify failure**

Run:

```bash
py -m pytest tests/perp_platform/okx -q
```

Expected:
- FAIL，因为新的回归测试还未与当前公开 API 对齐

### Task 2: Align regression tests with current public API

**Files:**
- `tests/perp_platform/okx/test_bootstrap.py`
- `tests/perp_platform/okx/test_runtime_regression.py`

**Step 1: Keep tests minimal and package-oriented**

- 只走 `perp_platform.runtime.okx` 顶层导出
- 不直接复制顶层 unit test 断言全集

**Step 2: Run targeted tests**

Run:

```bash
py -m pytest tests/perp_platform/okx -q
```

Expected:
- PASS

### Task 3: Run full verification

**Files:**
- Verify only

**Step 1: Run venue and project test suites**

Run:

```bash
py -m pytest tests/perp_platform/okx -q
py -m pytest tests/perp_platform -q
py -m pytest tests -q
```

Expected:
- PASS
