# Issue 51 OKX Swap Runtime Bootstrap Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 OKX USDT perpetual runtime 增加最小 config 与 bootstrap 入口。

**Architecture:** 沿用 Binance 的 config/bootstrap 分层，但采用 OKX 官方 `demo/mainnet` 环境命名，并显式纳入 `api_passphrase`。

**Tech Stack:** Python 3.12、dataclasses、pytest

---

### Task 1: Add failing OKX bootstrap tests

**Files:**
- Create: `tests/perp_platform/test_okx_runtime_bootstrap.py`

**Step 1: Write the failing tests**

- config 读取与 override
- invalid environment 拒绝
- bootstrap 返回稳定 result

**Step 2: Run targeted tests to verify failure**

Run:

```bash
py -m pytest tests/perp_platform/test_okx_runtime_bootstrap.py -q
```

Expected:
- FAIL，因为 `perp_platform.runtime.okx` 还不存在

**Step 3: Commit**

```bash
git add tests/perp_platform/test_okx_runtime_bootstrap.py
git commit -m "test: define okx runtime bootstrap contract"
```

### Task 2: Implement OKX config and bootstrap

**Files:**
- Create: `src/perp_platform/runtime/okx/__init__.py`
- Create: `src/perp_platform/runtime/okx/config.py`
- Create: `src/perp_platform/runtime/okx/bootstrap.py`
- Test: `tests/perp_platform/test_okx_runtime_bootstrap.py`

**Step 1: Write minimal implementation**

- 实现 config dataclass 与 loader
- 实现 bootstrap result dataclass
- 实现稳定 client target 与 label

**Step 2: Run targeted tests**

Run:

```bash
py -m pytest tests/perp_platform/test_okx_runtime_bootstrap.py -q
```

Expected:
- PASS

**Step 3: Commit**

```bash
git add src/perp_platform/runtime/okx/__init__.py src/perp_platform/runtime/okx/config.py src/perp_platform/runtime/okx/bootstrap.py tests/perp_platform/test_okx_runtime_bootstrap.py
git commit -m "feat: add okx runtime bootstrap"
```

### Task 3: Verify runtime scope

**Files:**
- Verify only

**Step 1: Run venue runtime verification**

Run:

```bash
py -m pytest tests/perp_platform/test_okx_runtime_bootstrap.py -q
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
git add docs/plans/2026-03-20-issue-51-okx-bootstrap-design.md docs/plans/2026-03-20-issue-51-okx-bootstrap.md
git commit -m "docs: add issue 51 okx bootstrap plan"
```
