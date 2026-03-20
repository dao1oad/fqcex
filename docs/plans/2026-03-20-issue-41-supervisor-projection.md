# Issue 41 Supervisor Projection Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 Supervisor 增加 venue-level 与 instrument-level 的最小 tradeability projection。

**Architecture:** 先从 `SupervisorState` 生成 venue projection，再在 instrument projection 上叠加更严格的 instrument override，不允许 instrument 放松 venue 限制。

**Tech Stack:** Python 3.12、dataclasses、pytest

---

### Task 1: Add failing projection tests

**Files:**
- Create: `tests/perp_platform/supervisor/test_projection.py`

**Step 1: Write the failing tests**

- venue state 到开仓/减仓能力的映射
- instrument 无 override 时继承 venue
- instrument stricter override 生效
- instrument 不能放松 stricter venue

**Step 2: Run targeted tests to verify failure**

Run:

```bash
py -m pytest tests/perp_platform/supervisor/test_projection.py -q
```

Expected:
- FAIL，因为 `projection.py` 尚不存在

**Step 3: Commit**

```bash
git add tests/perp_platform/supervisor/test_projection.py
git commit -m "test: define supervisor projection contract"
```

### Task 2: Implement tradeability projection

**Files:**
- Create: `src/perp_platform/supervisor/projection.py`
- Modify: `src/perp_platform/supervisor/__init__.py`
- Test: `tests/perp_platform/supervisor/test_projection.py`

**Step 1: Write minimal implementation**

- 新增 venue/instrument projection dataclass
- 新增 `project_venue_tradeability()`
- 新增 `project_instrument_tradeability()`

**Step 2: Run targeted tests**

Run:

```bash
py -m pytest tests/perp_platform/supervisor/test_projection.py -q
```

Expected:
- PASS

**Step 3: Commit**

```bash
git add src/perp_platform/supervisor/projection.py src/perp_platform/supervisor/__init__.py tests/perp_platform/supervisor/test_projection.py
git commit -m "feat: add supervisor tradeability projection"
```

### Task 3: Verify full scope and prepare merge

**Files:**
- Modify: `docs/plans/2026-03-20-issue-41-supervisor-projection-design.md`
- Modify: `docs/plans/2026-03-20-issue-41-supervisor-projection.md`

**Step 1: Run verification**

Run:

```bash
py -m pytest tests/perp_platform/supervisor/test_projection.py -q
py -m pytest tests/perp_platform/supervisor -q
py -m pytest tests -q
```

Expected:
- 全部 PASS

**Step 2: Confirm scope**

- 仅新增 projection
- 没有改 trigger evaluation
- 没有改 runtime 逻辑

**Step 3: Commit**

```bash
git add docs/plans/2026-03-20-issue-41-supervisor-projection-design.md docs/plans/2026-03-20-issue-41-supervisor-projection.md
git commit -m "docs: add issue 41 projection plan"
```
