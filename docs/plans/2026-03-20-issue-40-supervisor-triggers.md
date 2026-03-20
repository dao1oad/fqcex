# Issue 40 Supervisor Trigger Evaluation Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 Supervisor 增加最小流触发器求值逻辑，把流延迟与恢复故障信号映射成合法的状态迁移结果。

**Architecture:** 定义一个 state-aware evaluator，读取 `SupervisorTriggerInputs` 并通过 `transition_supervisor_state()` 生成 `SupervisorTransition`。不实现 projection，不扩展到 venue / instrument。

**Tech Stack:** Python 3.12、dataclasses、pytest

---

### Task 1: Add failing trigger evaluation tests

**Files:**
- Create: `tests/perp_platform/supervisor/test_triggers.py`

**Step 1: Write the failing tests**

- reconciliation failure -> `BLOCKED`
- repeated recovery failure -> `BLOCKED`
- private stream stale -> `REDUCE_ONLY`
- public stream lag 3s -> `RESYNCING`
- public stream lag 1.5s -> `DEGRADED`
- healthy + degraded -> `LIVE`
- healthy + reduce_only / blocked 保持原状态

**Step 2: Run targeted tests to verify failure**

Run:

```bash
py -m pytest tests/perp_platform/supervisor/test_triggers.py -q
```

Expected:
- FAIL，因为 `triggers.py` 尚不存在

**Step 3: Commit**

```bash
git add tests/perp_platform/supervisor/test_triggers.py
git commit -m "test: define supervisor trigger evaluation contract"
```

### Task 2: Implement trigger evaluation

**Files:**
- Create: `src/perp_platform/supervisor/triggers.py`
- Modify: `src/perp_platform/supervisor/__init__.py`
- Test: `tests/perp_platform/supervisor/test_triggers.py`

**Step 1: Write minimal implementation**

- 新增 `SupervisorTriggerInputs`
- 新增 lag threshold constants
- 新增 `evaluate_supervisor_triggers()`
- 从 `__init__.py` 导出相关符号

**Step 2: Run targeted tests**

Run:

```bash
py -m pytest tests/perp_platform/supervisor/test_triggers.py -q
```

Expected:
- PASS

**Step 3: Commit**

```bash
git add src/perp_platform/supervisor/triggers.py src/perp_platform/supervisor/__init__.py tests/perp_platform/supervisor/test_triggers.py
git commit -m "feat: add supervisor trigger evaluation"
```

### Task 3: Verify full scope and prepare merge

**Files:**
- Modify: `docs/plans/2026-03-20-issue-40-supervisor-triggers-design.md`
- Modify: `docs/plans/2026-03-20-issue-40-supervisor-triggers.md`

**Step 1: Run verification**

Run:

```bash
py -m pytest tests/perp_platform/supervisor/test_triggers.py -q
py -m pytest tests/perp_platform/supervisor -q
py -m pytest tests -q
```

Expected:
- 全部 PASS

**Step 2: Confirm scope**

- 仅新增 trigger evaluation
- 没有 projection
- 没有更改 `state_machine.py` 契约

**Step 3: Commit**

```bash
git add docs/plans/2026-03-20-issue-40-supervisor-triggers-design.md docs/plans/2026-03-20-issue-40-supervisor-triggers.md
git commit -m "docs: add issue 40 trigger evaluation plan"
```
