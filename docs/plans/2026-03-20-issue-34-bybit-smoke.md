# Issue 34 Bybit Smoke Tests Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 Bybit runtime 增加启动 smoke 与基础下单路径 smoke，验证 bootstrap、wiring 和 guards 能组成最小闭环。

**Architecture:** 在 `order_path.py` 中定义一个纯本地的最小 order-path 描述对象和构建函数，测试目录单独落在 `tests/perp_platform/bybit/`，把 smoke 契约与前序单元测试分开。

**Tech Stack:** Python 3.12、dataclasses、pytest

---

### Task 1: Add failing smoke tests

**Files:**
- Create: `tests/perp_platform/bybit/test_bootstrap.py`
- Create: `tests/perp_platform/bybit/test_order_path.py`

**Step 1: Write the failing tests**

- 在 `test_bootstrap.py` 中验证 bootstrap 结果具备 runtime 与 guard 组合闭环
- 在 `test_order_path.py` 中验证允许的 order path 可以被构建，非法能力会失败

**Step 2: Run targeted tests to verify failure**

Run:

```bash
py -m pytest tests/perp_platform/bybit -q
```

Expected:
- FAIL，因为 `order_path.py` 与 smoke 测试目录尚不存在

**Step 3: Commit**

```bash
git add tests/perp_platform/bybit/test_bootstrap.py tests/perp_platform/bybit/test_order_path.py
git commit -m "test: define bybit smoke contract"
```

### Task 2: Implement minimal order path builder

**Files:**
- Create: `src/perp_platform/runtime/bybit/order_path.py`
- Modify: `src/perp_platform/runtime/bybit/__init__.py`
- Test: `tests/perp_platform/bybit/test_order_path.py`

**Step 1: Write minimal implementation**

- 新增 `BybitOrderPath`
- 新增 `build_bybit_order_path()`
- 导出对应符号

**Step 2: Run targeted tests**

Run:

```bash
py -m pytest tests/perp_platform/bybit/test_order_path.py -q
```

Expected:
- bootstrap smoke 仍未完全通过，但 order path 相关测试应转绿

**Step 3: Commit**

```bash
git add src/perp_platform/runtime/bybit/order_path.py src/perp_platform/runtime/bybit/__init__.py tests/perp_platform/bybit/test_order_path.py
git commit -m "feat: add bybit order path smoke builder"
```

### Task 3: Finalize bootstrap smoke coverage

**Files:**
- Modify: `tests/perp_platform/bybit/test_bootstrap.py`
- Modify: `tests/perp_platform/bybit/test_order_path.py`
- Modify: `tests/perp_platform/test_bybit_runtime_bootstrap.py` only if needed for shared fixture shape

**Step 1: Finalize assertions**

- 确认 bootstrap smoke 只覆盖启动闭环
- 确认 order path smoke 只覆盖允许/拒绝的最小下单路径

**Step 2: Run smoke tests**

Run:

```bash
py -m pytest tests/perp_platform/bybit -q
```

Expected:
- PASS

**Step 3: Commit**

```bash
git add tests/perp_platform/bybit/test_bootstrap.py tests/perp_platform/bybit/test_order_path.py tests/perp_platform/test_bybit_runtime_bootstrap.py
git commit -m "test: add bybit smoke coverage"
```

### Task 4: Verify scope and prepare merge

**Files:**
- Modify: `docs/plans/2026-03-20-issue-34-bybit-smoke-design.md`
- Modify: `docs/plans/2026-03-20-issue-34-bybit-smoke.md`

**Step 1: Run verification**

Run:

```bash
py -m pytest tests/perp_platform/bybit -q
py -m pytest tests/perp_platform -q
py -m pytest tests -q
```

Expected:
- 全部 PASS

**Step 2: Confirm scope**

- 仅有 Bybit smoke 与最小 order-path 描述层改动
- 没有真实网络请求
- 没有提前做更后续 venue/runtime 任务

**Step 3: Commit**

```bash
git add docs/plans/2026-03-20-issue-34-bybit-smoke-design.md docs/plans/2026-03-20-issue-34-bybit-smoke.md
git commit -m "docs: add issue 34 bybit smoke plan"
```
