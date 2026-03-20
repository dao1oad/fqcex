# Issue 35 Bybit Recovery Sequence Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 Bybit 恢复闭环增加最小的重连与重订阅顺序模型，并确保恢复阶段默认保持 `REDUCE_ONLY`。

**Architecture:** 在 `recovery.py` 中定义恢复阶段、事件、状态和推进函数，用 `tests/perp_platform/bybit/test_recovery_sequence.py` 验证合法和非法顺序。实现只覆盖顺序控制，不做对账或 tradeability 投影。

**Tech Stack:** Python 3.12、Enum、dataclasses、pytest

---

### Task 1: Add failing recovery sequence tests

**Files:**
- Create: `tests/perp_platform/bybit/test_recovery_sequence.py`

**Step 1: Write the failing tests**

- 为 `begin_bybit_recovery()` 写起始状态测试
- 为合法顺序推进写测试
- 为跳步推进写失败测试
- 为终态继续推进写失败测试

**Step 2: Run targeted tests to verify failure**

Run:

```bash
py -m pytest tests/perp_platform/bybit/test_recovery_sequence.py -q
```

Expected:
- FAIL，因为 `recovery.py` 尚不存在

**Step 3: Commit**

```bash
git add tests/perp_platform/bybit/test_recovery_sequence.py
git commit -m "test: define bybit recovery sequence contract"
```

### Task 2: Implement recovery sequence model

**Files:**
- Create: `src/perp_platform/runtime/bybit/recovery.py`
- Modify: `src/perp_platform/runtime/bybit/__init__.py`
- Test: `tests/perp_platform/bybit/test_recovery_sequence.py`

**Step 1: Write minimal implementation**

- 新增 `BybitRecoveryPhase`
- 新增 `BybitRecoveryEvent`
- 新增 `BybitRecoveryState`
- 新增 `begin_bybit_recovery()`
- 新增 `advance_bybit_recovery()`
- 导出 recovery 相关符号

**Step 2: Run targeted tests**

Run:

```bash
py -m pytest tests/perp_platform/bybit/test_recovery_sequence.py -q
```

Expected:
- PASS

**Step 3: Commit**

```bash
git add src/perp_platform/runtime/bybit/recovery.py src/perp_platform/runtime/bybit/__init__.py tests/perp_platform/bybit/test_recovery_sequence.py
git commit -m "feat: add bybit recovery sequence"
```

### Task 3: Verify scope and prepare merge

**Files:**
- Modify: `docs/plans/2026-03-20-issue-35-bybit-recovery-sequence-design.md`
- Modify: `docs/plans/2026-03-20-issue-35-bybit-recovery-sequence.md`

**Step 1: Run verification**

Run:

```bash
py -m pytest tests/perp_platform/bybit/test_recovery_sequence.py -q
py -m pytest tests/perp_platform/bybit -q
py -m pytest tests -q
```

Expected:
- 全部 PASS

**Step 2: Confirm scope**

- 仅存在 recovery 顺序模型和对应测试改动
- 没有进入 reconciliation
- 没有做 tradeability projection

**Step 3: Commit**

```bash
git add docs/plans/2026-03-20-issue-35-bybit-recovery-sequence-design.md docs/plans/2026-03-20-issue-35-bybit-recovery-sequence.md
git commit -m "docs: add issue 35 recovery sequence plan"
```
