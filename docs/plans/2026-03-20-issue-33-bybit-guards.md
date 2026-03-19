# Issue 33 Bybit Guards Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 Bybit runtime 增加 Phase 1 允许的单向持仓、逐仓、杠杆和订单能力 guard，并通过 bootstrap 暴露出来。

**Architecture:** 在 `guards.py` 中集中定义声明式 guard 值对象和校验函数，再由 `bootstrap.py` 暴露给 runtime 启动结果。整个实现只做规则建模和校验，不连接真实 API。

**Tech Stack:** Python 3.12、dataclasses、pytest

---

### Task 1: Add failing guard tests

**Files:**
- Create: `tests/perp_platform/test_bybit_guards.py`
- Modify: `tests/perp_platform/test_bybit_runtime_bootstrap.py`

**Step 1: Write the failing tests**

- 为 `build_bybit_runtime_guards()` 写测试，校验固定约束
- 为 `validate_bybit_leverage()` / `validate_bybit_order_capability()` 写通过与失败测试
- 为 bootstrap 结果新增 `guards` 字段断言

**Step 2: Run targeted tests to verify failure**

Run:

```bash
py -m pytest tests/perp_platform/test_bybit_guards.py tests/perp_platform/test_bybit_runtime_bootstrap.py -q
```

Expected:
- FAIL，因为 `guards.py` 与 bootstrap 字段尚不存在

**Step 3: Commit**

```bash
git add tests/perp_platform/test_bybit_guards.py tests/perp_platform/test_bybit_runtime_bootstrap.py
git commit -m "test: define bybit runtime guard contract"
```

### Task 2: Implement guard model and validators

**Files:**
- Create: `src/perp_platform/runtime/bybit/guards.py`
- Test: `tests/perp_platform/test_bybit_guards.py`

**Step 1: Write minimal implementation**

- 新增 `BybitRuntimeGuards`
- 新增 `build_bybit_runtime_guards()`
- 新增 `validate_bybit_leverage()`
- 新增 `validate_bybit_order_capability()`

**Step 2: Run targeted tests**

Run:

```bash
py -m pytest tests/perp_platform/test_bybit_guards.py -q
```

Expected:
- PASS

**Step 3: Commit**

```bash
git add src/perp_platform/runtime/bybit/guards.py tests/perp_platform/test_bybit_guards.py
git commit -m "feat: add bybit runtime guards"
```

### Task 3: Expose guards from bootstrap and package exports

**Files:**
- Modify: `src/perp_platform/runtime/bybit/bootstrap.py`
- Modify: `src/perp_platform/runtime/bybit/__init__.py`
- Test: `tests/perp_platform/test_bybit_runtime_bootstrap.py`

**Step 1: Update implementation**

- `BybitRuntimeBootstrapResult` 增加 `guards`
- `bootstrap_bybit_runtime()` 调用 `build_bybit_runtime_guards()`
- 在 `__init__.py` 中导出 guards 与 validator

**Step 2: Run targeted tests**

Run:

```bash
py -m pytest tests/perp_platform/test_bybit_guards.py tests/perp_platform/test_bybit_runtime_bootstrap.py -q
```

Expected:
- PASS

**Step 3: Commit**

```bash
git add src/perp_platform/runtime/bybit/bootstrap.py src/perp_platform/runtime/bybit/__init__.py tests/perp_platform/test_bybit_runtime_bootstrap.py
git commit -m "feat: expose bybit guards from bootstrap"
```

### Task 4: Verify scope and prepare cloud handoff

**Files:**
- Modify: `docs/plans/2026-03-20-issue-33-bybit-guards-design.md`
- Modify: `docs/plans/2026-03-20-issue-33-bybit-guards.md`

**Step 1: Run verification**

Run:

```bash
py -m pytest tests/perp_platform/test_bybit_guards.py tests/perp_platform/test_bybit_runtime_bootstrap.py -q
py -m pytest tests/perp_platform -q
py -m pytest tests -q
```

Expected:
- 全部 PASS

**Step 2: Confirm scope**

- 仅存在 Bybit guard、bootstrap 与对应测试改动
- 未触发真实交易 API
- 未提前实现 `#34`

**Step 3: Commit**

```bash
git add docs/plans/2026-03-20-issue-33-bybit-guards-design.md docs/plans/2026-03-20-issue-33-bybit-guards.md
git commit -m "docs: add issue 33 bybit guards plan"
```
