# Issue 52 OKX Contract Conversion Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 OKX runtime 增加 `sz`（contracts）到 `base_qty` 的稳定换算入口，并保持 OKX 边界语言停留在 venue 层。

**Architecture:** `runtime.okx.conversion` 作为 venue wrapper，内部复用 `domain.normalize_quantity(Venue.OKX, ...)`，不重复定义新的 quantity truth 对象。

**Tech Stack:** Python 3.12、dataclasses、pytest、Decimal

---

### Task 1: Add failing OKX conversion tests

**Files:**
- Create: `tests/perp_platform/okx/__init__.py`
- Create: `tests/perp_platform/okx/test_conversion.py`

**Step 1: Write the failing tests**

- wrapper 能把 contracts 转成 `base_qty`
- wrapper 返回 `NormalizedQuantity`
- invalid / float input 被拒绝

**Step 2: Run targeted tests to verify failure**

Run:

```bash
py -m pytest tests/perp_platform/okx/test_conversion.py -q
```

Expected:
- FAIL，因为 `perp_platform.runtime.okx.conversion` 还不存在

### Task 2: Implement OKX conversion wrapper

**Files:**
- Create: `src/perp_platform/runtime/okx/conversion.py`
- Update: `src/perp_platform/runtime/okx/__init__.py`
- Test: `tests/perp_platform/okx/test_conversion.py`

**Step 1: Write minimal implementation**

- 实现 `normalize_okx_contract_quantity(...)`
- 实现 `okx_contracts_to_base_qty(...)`
- 导出 public API

**Step 2: Run targeted tests**

Run:

```bash
py -m pytest tests/perp_platform/okx/test_conversion.py -q
```

Expected:
- PASS

### Task 3: Verify OKX runtime scope

**Files:**
- Verify only

**Step 1: Run OKX and venue runtime verification**

Run:

```bash
py -m pytest tests/perp_platform/okx/test_conversion.py -q
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
