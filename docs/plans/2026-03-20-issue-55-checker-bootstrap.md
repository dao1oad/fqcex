# Issue 55 Checker Bootstrap Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为独立市场数据 checker 增加最小配置与 bootstrap 入口，产出后续可消费的订阅计划。

**Architecture:** 新增 `checker/config.py` 与 `checker/bootstrap.py`，保持和现有 runtime bootstrap 一致的分层，不提前接第三方 feed。

**Tech Stack:** Python 3.12、dataclasses、pytest

---

### Task 1: Add failing checker bootstrap tests

**Files:**
- Create: `tests/perp_platform/test_checker_bootstrap.py`

**Step 1: Write the failing tests**

- config 读取与校验
- bootstrap 返回稳定 service label
- subscription plan 形状稳定

**Step 2: Run targeted tests to verify failure**

Run:

```bash
py -m pytest tests/perp_platform/test_checker_bootstrap.py -q
```

Expected:
- FAIL，因为 `perp_platform.checker` 还不存在

### Task 2: Implement checker config and bootstrap

**Files:**
- Create: `src/perp_platform/checker/__init__.py`
- Create: `src/perp_platform/checker/config.py`
- Create: `src/perp_platform/checker/bootstrap.py`
- Test: `tests/perp_platform/test_checker_bootstrap.py`

**Step 1: Write minimal implementation**

- 实现 `CheckerConfig` 与 loader
- 实现 `CheckerSubscriptionTarget`
- 实现 `bootstrap_checker(...)`

**Step 2: Run targeted tests**

Run:

```bash
py -m pytest tests/perp_platform/test_checker_bootstrap.py -q
```

Expected:
- PASS

### Task 3: Verify checker scope

**Files:**
- Verify only

**Step 1: Run package verification**

Run:

```bash
py -m pytest tests/perp_platform/test_checker_bootstrap.py -q
py -m pytest tests/perp_platform -q
```

Expected:
- PASS

**Step 2: Run full regression**

Run:

```bash
py -m pytest tests -q
```

Expected:
- PASS
