# Issue 37 Bybit Tradeability Projection Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 Bybit 恢复闭环增加 `REDUCE_ONLY` / `BLOCKED` 的最小投影层，基于恢复状态和对账结果生成统一 tradeability 结果。

**Architecture:** 在 `tradeability.py` 中定义模式、原因和 blocker 列表，再用一个纯函数消费 `recovery.py` 与 `reconciliation.py` 的结果。实现不进入 `LIVE`，只处理 `REDUCE_ONLY` / `BLOCKED`。

**Tech Stack:** Python 3.12、Enum、dataclasses、pytest

---

### Task 1: Add failing tradeability tests

**Files:**
- Create: `tests/perp_platform/bybit/test_tradeability_projection.py`

**Step 1: Write the failing tests**

- 恢复进行中 -> `REDUCE_ONLY`
- 已到 `RECONCILIATION_PENDING` 但无结果 -> `REDUCE_ONLY`
- 对账失败 -> `BLOCKED`
- 对账通过 -> `REDUCE_ONLY`

**Step 2: Run targeted tests to verify failure**

Run:

```bash
py -m pytest tests/perp_platform/bybit/test_tradeability_projection.py -q
```

Expected:
- FAIL，因为 `tradeability.py` 尚不存在

**Step 3: Commit**

```bash
git add tests/perp_platform/bybit/test_tradeability_projection.py
git commit -m "test: define bybit tradeability projection contract"
```

### Task 2: Implement tradeability projection

**Files:**
- Create: `src/perp_platform/runtime/bybit/tradeability.py`
- Modify: `src/perp_platform/runtime/bybit/__init__.py`
- Test: `tests/perp_platform/bybit/test_tradeability_projection.py`

**Step 1: Write minimal implementation**

- 新增 `BybitTradeabilityMode`
- 新增 `BybitTradeabilityProjection`
- 新增 `project_bybit_tradeability()`
- 导出对应符号

**Step 2: Run targeted tests**

Run:

```bash
py -m pytest tests/perp_platform/bybit/test_tradeability_projection.py -q
```

Expected:
- PASS

**Step 3: Commit**

```bash
git add src/perp_platform/runtime/bybit/tradeability.py src/perp_platform/runtime/bybit/__init__.py tests/perp_platform/bybit/test_tradeability_projection.py
git commit -m "feat: add bybit tradeability projection"
```

### Task 3: Verify scope and prepare merge

**Files:**
- Modify: `docs/plans/2026-03-20-issue-37-bybit-tradeability-design.md`
- Modify: `docs/plans/2026-03-20-issue-37-bybit-tradeability.md`

**Step 1: Run verification**

Run:

```bash
py -m pytest tests/perp_platform/bybit/test_tradeability_projection.py -q
py -m pytest tests/perp_platform/bybit -q
py -m pytest tests -q
```

Expected:
- 全部 PASS

**Step 2: Confirm scope**

- 仅存在 tradeability projection 与测试改动
- 没有恢复到 `LIVE`
- 没有 runbook 改动

**Step 3: Commit**

```bash
git add docs/plans/2026-03-20-issue-37-bybit-tradeability-design.md docs/plans/2026-03-20-issue-37-bybit-tradeability.md
git commit -m "docs: add issue 37 tradeability plan"
```
