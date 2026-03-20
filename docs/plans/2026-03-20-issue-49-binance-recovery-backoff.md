# Issue 49 Binance Recovery Backoff Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 Binance USDⓈ-M 恢复流程增加确定性的配额安全 backoff 策略。

**Architecture:** 使用独立的 recovery 状态机封装 backoff；以纯函数驱动状态推进，不引入真实计时器或网络客户端。

**Tech Stack:** Python 3.12、dataclasses、enum、pytest

---

### Task 1: Add failing recovery backoff tests

**Files:**
- Create: `tests/perp_platform/binance/test_recovery_backoff.py`

**Step 1: Write the failing tests**

- 初始 `BACKING_OFF`
- 正常恢复序列
- `RATE_LIMIT_HIT` 会提高 attempt 和 backoff
- backoff 封顶

**Step 2: Run targeted tests to verify failure**

Run:

```bash
py -m pytest tests/perp_platform/binance/test_recovery_backoff.py -q
```

Expected:
- FAIL，因为 `recovery.py` 尚不存在

**Step 3: Commit**

```bash
git add tests/perp_platform/binance/test_recovery_backoff.py
git commit -m "test: define binance recovery backoff contract"
```

### Task 2: Implement Binance recovery backoff state machine

**Files:**
- Create: `src/perp_platform/runtime/binance/recovery.py`
- Modify: `src/perp_platform/runtime/binance/__init__.py`
- Test: `tests/perp_platform/binance/test_recovery_backoff.py`

**Step 1: Write minimal implementation**

- 定义 recovery phase/event/state
- 定义 `begin_binance_recovery()`
- 定义 `advance_binance_recovery()`

**Step 2: Run targeted tests**

Run:

```bash
py -m pytest tests/perp_platform/binance/test_recovery_backoff.py -q
```

Expected:
- PASS

**Step 3: Commit**

```bash
git add src/perp_platform/runtime/binance/recovery.py src/perp_platform/runtime/binance/__init__.py tests/perp_platform/binance/test_recovery_backoff.py
git commit -m "feat: add binance recovery backoff"
```

### Task 3: Verify venue regression

**Files:**
- Verify only

**Step 1: Run Binance-focused verification**

Run:

```bash
py -m pytest tests/perp_platform/binance/test_recovery_backoff.py -q
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
git add docs/plans/2026-03-20-issue-49-binance-recovery-backoff-design.md docs/plans/2026-03-20-issue-49-binance-recovery-backoff.md
git commit -m "docs: add issue 49 binance recovery backoff plan"
```
