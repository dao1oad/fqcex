# Issue 48 Binance Runtime Streams And Execution Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 Binance USDⓈ-M runtime 增加 public/private stream 与 execution path 的最小 wiring。

**Architecture:** 继续沿用 Bybit 的 dataclass wiring 方案；新增 `clients.py` 与 `runtime.py`，并把 bootstrap 扩展为返回 `runtime`，但不引入真实 SDK 和恢复逻辑。

**Tech Stack:** Python 3.12、dataclasses、pytest

---

### Task 1: Add failing Binance client/runtime tests

**Files:**
- Create: `tests/perp_platform/test_binance_runtime_clients.py`
- Modify: `tests/perp_platform/test_binance_runtime_bootstrap.py`

**Step 1: Write the failing tests**

- runtime wiring with/without credentials
- bootstrap result exposes runtime

**Step 2: Run targeted tests to verify failure**

Run:

```bash
py -m pytest tests/perp_platform/test_binance_runtime_clients.py tests/perp_platform/test_binance_runtime_bootstrap.py -q
```

Expected:
- FAIL，因为 `clients.py` / `runtime.py` 尚不存在，bootstrap 也尚未暴露 `runtime`

**Step 3: Commit**

```bash
git add tests/perp_platform/test_binance_runtime_clients.py tests/perp_platform/test_binance_runtime_bootstrap.py
git commit -m "test: define binance runtime wiring contract"
```

### Task 2: Implement Binance client and runtime wiring

**Files:**
- Create: `src/perp_platform/runtime/binance/clients.py`
- Create: `src/perp_platform/runtime/binance/runtime.py`
- Modify: `src/perp_platform/runtime/binance/bootstrap.py`
- Modify: `src/perp_platform/runtime/binance/__init__.py`
- Test: `tests/perp_platform/test_binance_runtime_clients.py`
- Test: `tests/perp_platform/test_binance_runtime_bootstrap.py`

**Step 1: Write minimal implementation**

- 定义 stream/execution client dataclass
- 定义 runtime wiring
- 在 bootstrap result 中增加 `runtime`

**Step 2: Run targeted tests**

Run:

```bash
py -m pytest tests/perp_platform/test_binance_runtime_clients.py tests/perp_platform/test_binance_runtime_bootstrap.py -q
```

Expected:
- PASS

**Step 3: Commit**

```bash
git add src/perp_platform/runtime/binance/clients.py src/perp_platform/runtime/binance/runtime.py src/perp_platform/runtime/binance/bootstrap.py src/perp_platform/runtime/binance/__init__.py tests/perp_platform/test_binance_runtime_clients.py tests/perp_platform/test_binance_runtime_bootstrap.py
git commit -m "feat: add binance runtime wiring"
```

### Task 3: Verify runtime regression

**Files:**
- Verify only

**Step 1: Run venue runtime verification**

Run:

```bash
py -m pytest tests/perp_platform/test_binance_runtime_clients.py tests/perp_platform/test_binance_runtime_bootstrap.py -q
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
git add docs/plans/2026-03-20-issue-48-binance-runtime-streams-design.md docs/plans/2026-03-20-issue-48-binance-runtime-streams.md
git commit -m "docs: add issue 48 binance runtime plan"
```
