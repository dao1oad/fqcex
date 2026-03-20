# Issue 36 Bybit Reconciliation Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 Bybit 恢复闭环增加订单、仓位、余额的最小对账模型，并产出可供后续 tradeability 投影消费的结果对象。

**Architecture:** 在 `reconciliation.py` 中定义三类快照对象和一个聚合对账结果对象，再通过 `reconcile_bybit_state()` 做纯本地集合比对。实现不触发真实查询，不改变恢复状态机。

**Tech Stack:** Python 3.12、dataclasses、pytest

---

### Task 1: Add failing reconciliation tests

**Files:**
- Create: `tests/perp_platform/bybit/test_reconciliation.py`

**Step 1: Write the failing tests**

- 完整匹配测试
- 顺序不同仍通过测试
- 订单差异测试
- 仓位差异测试
- 余额差异测试

**Step 2: Run targeted tests to verify failure**

Run:

```bash
py -m pytest tests/perp_platform/bybit/test_reconciliation.py -q
```

Expected:
- FAIL，因为 `reconciliation.py` 尚不存在

**Step 3: Commit**

```bash
git add tests/perp_platform/bybit/test_reconciliation.py
git commit -m "test: define bybit reconciliation contract"
```

### Task 2: Implement reconciliation model

**Files:**
- Create: `src/perp_platform/runtime/bybit/reconciliation.py`
- Modify: `src/perp_platform/runtime/bybit/__init__.py`
- Test: `tests/perp_platform/bybit/test_reconciliation.py`

**Step 1: Write minimal implementation**

- 新增三类 snapshot dataclass
- 新增 `BybitReconciliationResult`
- 新增 `reconcile_bybit_state()`
- 导出 reconciliation 相关符号

**Step 2: Run targeted tests**

Run:

```bash
py -m pytest tests/perp_platform/bybit/test_reconciliation.py -q
```

Expected:
- PASS

**Step 3: Commit**

```bash
git add src/perp_platform/runtime/bybit/reconciliation.py src/perp_platform/runtime/bybit/__init__.py tests/perp_platform/bybit/test_reconciliation.py
git commit -m "feat: add bybit reconciliation model"
```

### Task 3: Verify scope and prepare merge

**Files:**
- Modify: `docs/plans/2026-03-20-issue-36-bybit-reconciliation-design.md`
- Modify: `docs/plans/2026-03-20-issue-36-bybit-reconciliation.md`

**Step 1: Run verification**

Run:

```bash
py -m pytest tests/perp_platform/bybit/test_reconciliation.py -q
py -m pytest tests/perp_platform/bybit -q
py -m pytest tests -q
```

Expected:
- 全部 PASS

**Step 2: Confirm scope**

- 仅存在 reconciliation 模型与测试改动
- 没有 tradeability projection
- 没有 runbook 改动

**Step 3: Commit**

```bash
git add docs/plans/2026-03-20-issue-36-bybit-reconciliation-design.md docs/plans/2026-03-20-issue-36-bybit-reconciliation.md
git commit -m "docs: add issue 36 reconciliation plan"
```
