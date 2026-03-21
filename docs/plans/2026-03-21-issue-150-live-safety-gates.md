# Issue 150 Live Safety Gates Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 live canary 增加可复用的运行时安全闸门，覆盖 max notional、allowlist、kill switch 和 operator approval 审计联动。

**Architecture:** 在 control-plane 层新增一个纯 Python gate evaluator，配置来自 `#149` 已冻结的 env 契约，kill switch 从文件读取状态，approval 成功时通过现有 audit hook 产出 `audit_event_id`。当前不引入 HTTP 或权限系统。

**Tech Stack:** Python 3.12, `dataclasses`, `pathlib`, `pytest`

---

### Task 1: Add failing live safety gate tests

**Files:**
- Create: `tests/perp_platform/control_plane/test_live_safety_gates.py`
- Test: `tests/perp_platform/control_plane/test_live_safety_gates.py`

**Step 1: Write the failing test**

- 覆盖：
  - missing approval rejects
  - over max notional rejects
  - venue / instrument outside allowlist rejects
  - armed kill switch rejects
  - valid request allows and returns audit event id

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/perp_platform/control_plane/test_live_safety_gates.py -q`

Expected:

- FAIL，因为 gate 模块尚不存在

**Step 3: Commit**

```bash
git add tests/perp_platform/control_plane/test_live_safety_gates.py
git commit -m "test: define live safety gate contract"
```

### Task 2: Implement gate module and audit linkage

**Files:**
- Create: `src/perp_platform/control_plane/live_safety.py`
- Modify: `src/perp_platform/control_plane/__init__.py`
- Test: `tests/perp_platform/control_plane/test_live_safety_gates.py`

**Step 1: Add minimal implementation**

- dataclasses for config/request/decision/approval
- file-backed kill switch reader
- gate evaluation logic
- successful approval records `approve_live_canary` through audit hook

**Step 2: Run targeted tests**

Run:

```bash
py -m pytest tests/perp_platform/control_plane/test_live_safety_gates.py -q
py -m pytest tests/perp_platform/control_plane -q
```

Expected:

- PASS

**Step 3: Commit**

```bash
git add src/perp_platform/control_plane/live_safety.py src/perp_platform/control_plane/__init__.py tests/perp_platform/control_plane/test_live_safety_gates.py
git commit -m "feat: add live safety gates"
```

### Task 3: Update runbooks and verify full suite

**Files:**
- Modify: `docs/runbooks/live-canary-deploy.md`
- Create: `docs/runbooks/live-canary-approval.md`
- Modify: `README.md`
- Modify: `docs/plans/2026-03-21-issue-150-live-safety-gates-design.md`
- Modify: `docs/plans/2026-03-21-issue-150-live-safety-gates.md`

**Step 1: Update docs**

- 明确 kill switch 的 `armed=true/false` 语义
- 明确 approval 是进入 live canary 的硬前提
- 明确放行成功必须留审计记录

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
git add README.md docs/runbooks/live-canary-deploy.md docs/runbooks/live-canary-approval.md docs/plans/2026-03-21-issue-150-live-safety-gates-design.md docs/plans/2026-03-21-issue-150-live-safety-gates.md
git commit -m "docs: add live safety gate runbook"
```
