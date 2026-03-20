# Issue 53 OKX Runtime Guards Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 OKX runtime 增加单向持仓、逐仓与下单能力约束，并把这些约束通过 bootstrap 暴露为稳定运行时边界。

**Architecture:** 用 `guards.py` 集中表达 Phase 1 约束，用 `runtime.py` 投影运行时边界，再由 `bootstrap.py` 一次性装配。

**Tech Stack:** Python 3.12、dataclasses、pytest

---

### Task 1: Add failing OKX guard tests

**Files:**
- Create: `tests/perp_platform/test_okx_guards.py`
- Update: `tests/perp_platform/test_okx_runtime_bootstrap.py`

**Step 1: Write the failing tests**

- guards 的冻结值
- leverage 校验
- order capability 组合校验
- bootstrap 返回 runtime / guards

**Step 2: Run targeted tests to verify failure**

Run:

```bash
py -m pytest tests/perp_platform/test_okx_guards.py tests/perp_platform/test_okx_runtime_bootstrap.py -q
```

Expected:
- FAIL，因为 OKX guards/runtime 还不存在

### Task 2: Implement OKX guards and runtime wiring

**Files:**
- Create: `src/perp_platform/runtime/okx/guards.py`
- Create: `src/perp_platform/runtime/okx/runtime.py`
- Update: `src/perp_platform/runtime/okx/bootstrap.py`
- Update: `src/perp_platform/runtime/okx/__init__.py`
- Test: `tests/perp_platform/test_okx_guards.py`
- Test: `tests/perp_platform/test_okx_runtime_bootstrap.py`

**Step 1: Write minimal implementation**

- 实现 guards builder 与 validators
- 实现最小 runtime wiring
- bootstrap 集成 runtime / guards

**Step 2: Run targeted tests**

Run:

```bash
py -m pytest tests/perp_platform/test_okx_guards.py tests/perp_platform/test_okx_runtime_bootstrap.py -q
```

Expected:
- PASS

### Task 3: Verify OKX runtime scope

**Files:**
- Verify only

**Step 1: Run venue runtime verification**

Run:

```bash
py -m pytest tests/perp_platform/test_okx_guards.py tests/perp_platform/test_okx_runtime_bootstrap.py -q
py -m pytest tests/perp_platform/okx -q
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
