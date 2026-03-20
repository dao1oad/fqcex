# Issue 39 Supervisor State Machine Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 Supervisor 增加最小状态机契约，冻结状态枚举、允许迁移表和迁移验证函数。

**Architecture:** 用 target-based transition contract 表达状态机：`#39` 只验证“当前状态是否允许迁移到目标状态”，不承载 trigger 语义；触发器求值留给 `#40`。

**Tech Stack:** Python 3.12、Enum、dataclasses、pytest

---

### Task 1: Add failing state machine tests

**Files:**
- Create: `tests/perp_platform/supervisor/test_state_machine.py`

**Step 1: Write the failing tests**

- 状态枚举值稳定
- `allowed_supervisor_targets()` 返回预期集合
- 合法迁移成功
- no-op 迁移返回 `changed = False`
- 非法迁移抛出 `ValueError`

**Step 2: Run targeted tests to verify failure**

Run:

```bash
py -m pytest tests/perp_platform/supervisor/test_state_machine.py -q
```

Expected:
- FAIL，因为 `supervisor/state_machine.py` 尚不存在

**Step 3: Commit**

```bash
git add tests/perp_platform/supervisor/test_state_machine.py
git commit -m "test: define supervisor state machine contract"
```

### Task 2: Implement supervisor state machine contract

**Files:**
- Create: `src/perp_platform/supervisor/__init__.py`
- Create: `src/perp_platform/supervisor/state_machine.py`
- Test: `tests/perp_platform/supervisor/test_state_machine.py`

**Step 1: Write minimal implementation**

- 新增 `SupervisorState`
- 新增 `SupervisorTransition`
- 新增 `allowed_supervisor_targets()`
- 新增 `transition_supervisor_state()`

**Step 2: Run targeted tests**

Run:

```bash
py -m pytest tests/perp_platform/supervisor/test_state_machine.py -q
```

Expected:
- PASS

**Step 3: Commit**

```bash
git add src/perp_platform/supervisor/__init__.py src/perp_platform/supervisor/state_machine.py tests/perp_platform/supervisor/test_state_machine.py
git commit -m "feat: add supervisor state machine contract"
```

### Task 3: Verify full scope and prepare merge

**Files:**
- Modify: `docs/plans/2026-03-20-issue-39-supervisor-state-machine-design.md`
- Modify: `docs/plans/2026-03-20-issue-39-supervisor-state-machine.md`

**Step 1: Run verification**

Run:

```bash
py -m pytest tests/perp_platform/supervisor/test_state_machine.py -q
py -m pytest tests -q
```

Expected:
- 全部 PASS

**Step 2: Confirm scope**

- 只新增 supervisor state contract
- 没有 trigger evaluation
- 没有 projection

**Step 3: Commit**

```bash
git add docs/plans/2026-03-20-issue-39-supervisor-state-machine-design.md docs/plans/2026-03-20-issue-39-supervisor-state-machine.md
git commit -m "docs: add issue 39 supervisor state plan"
```
