# Issue 147 Operator Actions Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 control-plane 增加 `force_reduce_only`、`force_block`、`force_resume` 的最小写接口和前提校验。

**Architecture:** 在 `actions.py` 中定义动作请求、结果和审计挂点协议；在 `app.py` 中扩展 POST handlers，并使用最小 JSON body 校验和 `force_resume` 前提校验实现行为。

**Tech Stack:** Python 3.12, `dataclasses`, `json`, `typing.Protocol`, `pytest`

---

### Task 1: Add failing operator action tests

**Files:**
- Create: `tests/perp_platform/control_plane/test_operator_actions.py`
- Test: `tests/perp_platform/control_plane/test_operator_actions.py`

**Step 1: Write the failing test**

- 覆盖：
  - `force_reduce_only` success
  - `force_block` success
  - `force_resume` conflict on unmet preconditions
  - `force_resume` success on satisfied preconditions
  - invalid action type mismatch

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/perp_platform/control_plane/test_operator_actions.py -q`

Expected:

- FAIL，因为 `actions.py` 与 POST handlers 尚不存在

**Step 3: Commit**

```bash
git add tests/perp_platform/control_plane/test_operator_actions.py
git commit -m "test: define operator action handlers"
```

### Task 2: Implement minimal operator actions

**Files:**
- Create: `src/perp_platform/control_plane/actions.py`
- Modify: `src/perp_platform/control_plane/app.py`
- Modify: `src/perp_platform/control_plane/server.py`
- Modify: `src/perp_platform/control_plane/__init__.py`
- Test: `tests/perp_platform/control_plane/test_operator_actions.py`
- Test: `tests/perp_platform/control_plane/test_http_skeleton.py`

**Step 1: Add minimal implementation**

- 定义 action request / result
- 定义 in-memory audit hook
- 为 `POST` 路径增加 body parsing 和最小校验

**Step 2: Run targeted tests**

Run:

```bash
py -m pytest tests/perp_platform/control_plane/test_operator_actions.py -q
py -m pytest tests/perp_platform/control_plane/test_http_skeleton.py -q
```

Expected:

- PASS

**Step 3: Commit**

```bash
git add src/perp_platform/control_plane/actions.py src/perp_platform/control_plane/app.py src/perp_platform/control_plane/server.py src/perp_platform/control_plane/__init__.py tests/perp_platform/control_plane/test_operator_actions.py
git commit -m "feat: add control plane operator actions"
```

### Task 3: Update docs and run full verification

**Files:**
- Modify: `README.md`
- Modify: `docs/runbooks/force-resume-policy.md`
- Modify: `docs/plans/2026-03-21-issue-147-operator-actions-design.md`
- Modify: `docs/plans/2026-03-21-issue-147-operator-actions.md`

**Step 1: Update docs**

- 在 `README.md` 中加入 operator action endpoints
- 在 `force-resume-policy.md` 中补充 control-plane 最小前提口径

**Step 2: Run verification**

Run:

```bash
py -m pytest tests/perp_platform/control_plane -q
py -m pytest tests -q
```

Expected:

- PASS

**Step 3: Commit**

```bash
git add README.md docs/runbooks/force-resume-policy.md docs/plans/2026-03-21-issue-147-operator-actions-design.md docs/plans/2026-03-21-issue-147-operator-actions.md
git commit -m "docs: add issue 147 operator action plan"
```
