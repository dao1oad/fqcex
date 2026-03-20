# Issue 38 Bybit Recovery Modes Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 Bybit 恢复闭环补充场景测试与运行手册说明，证明恢复期间的 `REDUCE_ONLY` / `BLOCKED` 行为与当前实现一致。

**Architecture:** 不新增生产代码；用一个新的 recovery modes 场景测试串联 recovery、reconciliation、tradeability 三个模块，并同步更新 `private-stream-recovery.md` 的操作口径。

**Tech Stack:** Python 3.12、pytest、Markdown runbook

---

### Task 1: Add failing recovery mode scenario tests

**Files:**
- Create: `tests/perp_platform/bybit/test_recovery_modes.py`

**Step 1: Write the failing tests**

- 恢复未完成时保持 `REDUCE_ONLY`
- 对账失败时投影为 `BLOCKED`
- 对账通过后仍为 `REDUCE_ONLY`，原因是 `cooldown_pending`

**Step 2: Run targeted tests to verify failure**

Run:

```bash
py -m pytest tests/perp_platform/bybit/test_recovery_modes.py -q
```

Expected:
- FAIL，因为测试文件刚建立且可能需要补齐模块导入或场景细节

**Step 3: Commit**

```bash
git add tests/perp_platform/bybit/test_recovery_modes.py
git commit -m "test: define bybit recovery mode scenarios"
```

### Task 2: Update recovery runbook

**Files:**
- Modify: `docs/runbooks/private-stream-recovery.md`
- Test: `tests/perp_platform/bybit/test_recovery_modes.py`

**Step 1: Update runbook**

- 写清恢复期间默认 `REDUCE_ONLY`
- 写清对账失败进入 `BLOCKED`
- 写清对账通过后仍需 cooldown / 人工恢复审查

**Step 2: Run targeted and area tests**

Run:

```bash
py -m pytest tests/perp_platform/bybit/test_recovery_modes.py -q
py -m pytest tests/perp_platform/bybit -q
```

Expected:
- PASS

**Step 3: Commit**

```bash
git add docs/runbooks/private-stream-recovery.md tests/perp_platform/bybit/test_recovery_modes.py
git commit -m "docs: add bybit recovery mode guidance"
```

### Task 3: Verify full scope and prepare merge

**Files:**
- Modify: `docs/plans/2026-03-20-issue-38-bybit-recovery-modes-design.md`
- Modify: `docs/plans/2026-03-20-issue-38-bybit-recovery-modes.md`

**Step 1: Run full verification**

Run:

```bash
py -m pytest tests/perp_platform/bybit/test_recovery_modes.py -q
py -m pytest tests/perp_platform/bybit -q
py -m pytest tests -q
```

Expected:
- 全部 PASS

**Step 2: Confirm scope**

- 仅新增 recovery modes 场景测试
- 仅更新 `private-stream-recovery.md`
- 无生产代码改动

**Step 3: Commit**

```bash
git add docs/plans/2026-03-20-issue-38-bybit-recovery-modes-design.md docs/plans/2026-03-20-issue-38-bybit-recovery-modes.md
git commit -m "docs: add issue 38 recovery mode plan"
```
