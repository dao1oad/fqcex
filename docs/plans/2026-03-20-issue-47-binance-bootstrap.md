# Issue 47 Binance USD-M Runtime Bootstrap Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 Binance USDⓈ-M 增加最小 runtime config 与 bootstrap 入口。

**Architecture:** 沿用 Bybit 的环境变量配置思路，但只返回稳定的 endpoint/client-target 描述，不在本 issue 中引入真实 stream/execution wiring。

**Tech Stack:** Python 3.12、dataclasses、pytest

---

### Task 1: Add failing Binance bootstrap tests

**Files:**
- Create: `tests/perp_platform/test_binance_runtime_bootstrap.py`

**Step 1: Write the failing tests**

- config 读取与 override
- invalid environment 拒绝
- bootstrap 返回稳定 result

**Step 2: Run targeted tests to verify failure**

Run:

```bash
py -m pytest tests/perp_platform/test_binance_runtime_bootstrap.py -q
```

Expected:
- FAIL，因为 `perp_platform.runtime.binance` 还不存在

**Step 3: Commit**

```bash
git add tests/perp_platform/test_binance_runtime_bootstrap.py
git commit -m "test: define binance runtime bootstrap contract"
```

### Task 2: Implement Binance config and bootstrap

**Files:**
- Create: `src/perp_platform/runtime/binance/__init__.py`
- Create: `src/perp_platform/runtime/binance/config.py`
- Create: `src/perp_platform/runtime/binance/bootstrap.py`
- Test: `tests/perp_platform/test_binance_runtime_bootstrap.py`

**Step 1: Write minimal implementation**

- 实现 config dataclass 与 loader
- 实现 bootstrap result dataclass
- 实现稳定 client target 与 label

**Step 2: Run targeted tests**

Run:

```bash
py -m pytest tests/perp_platform/test_binance_runtime_bootstrap.py -q
```

Expected:
- PASS

**Step 3: Commit**

```bash
git add src/perp_platform/runtime/binance/__init__.py src/perp_platform/runtime/binance/config.py src/perp_platform/runtime/binance/bootstrap.py tests/perp_platform/test_binance_runtime_bootstrap.py
git commit -m "feat: add binance runtime bootstrap"
```

### Task 3: Verify runtime scope

**Files:**
- Verify only

**Step 1: Run runtime-focused verification**

Run:

```bash
py -m pytest tests/perp_platform/test_binance_runtime_bootstrap.py -q
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

**Step 3: Commit**

```bash
git add docs/plans/2026-03-20-issue-47-binance-bootstrap-design.md docs/plans/2026-03-20-issue-47-binance-bootstrap.md
git commit -m "docs: add issue 47 binance bootstrap plan"
```
