# Issue 67 Control Plane API Surface Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 定义 Phase 4 外部控制平面 API 的最小资源表面，并通过文档契约测试锁定边界。

**Architecture:** 新增 `docs/architecture/control-plane-api.md` 作为控制平面 API 设计入口；在 `ARCHITECTURE.md` 中声明 control plane 组件和 truth boundary；用一个 governance contract test 锁定关键资源面与非目标。

**Tech Stack:** Markdown, pytest

---

### Task 1: Write the failing contract test

**Files:**
- Create: `tests/governance/test_control_plane_api_contract.py`

**Step 1: Write the failing test**

Assert that:
- `docs/architecture/control-plane-api.md` exists
- it contains `Venue Tradeability`
- it contains `Instrument Tradeability`
- it contains `Recovery Runs`
- it contains `Checker Signals`
- it contains `Operator Actions`
- `docs/architecture/ARCHITECTURE.md` mentions `Control Plane`

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/governance/test_control_plane_api_contract.py -q`
Expected: FAIL because the new doc does not exist yet.

### Task 2: Add the control plane API doc

**Files:**
- Create: `docs/architecture/control-plane-api.md`

**Step 1: Write the minimal doc**

Include:
- purpose and non-goals
- resource groups
- action entrypoint group
- response envelope
- error envelope
- explicit statement that the control plane is not a new truth source

**Step 2: Keep action details shallow**

Only list:
- `force_reduce_only`
- `force_block`
- `force_resume`

Do not define permissions or payload details beyond placeholders.

### Task 3: Update architecture doc

**Files:**
- Modify: `docs/architecture/ARCHITECTURE.md`

Add:
- `Control Plane` as a logical component
- statement that it projects Supervisor/store/audit views
- statement that truth ownership remains unchanged

### Task 4: Verify

**Files:**
- Test: `tests/governance/test_control_plane_api_contract.py`

Run:
- `py -m pytest tests/governance/test_control_plane_api_contract.py -q`
- `py scripts/update_project_memory.py`
- `py -m pytest tests -q`

Expected: PASS
