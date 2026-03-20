# Issue 42 Supervisor State Flow And Architecture Docs Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 Supervisor 状态机补充高层状态流测试，并把 `STATE_MACHINE.md` 更新到与现有实现一致。

**Architecture:** 不新增生产代码；新增一个端到端状态流测试文件串联 state machine、triggers、projection，并同步更新架构文档。

**Tech Stack:** Python 3.12、pytest、Markdown

---

### Task 1: Add failing supervisor state flow tests

**Files:**
- Create: `tests/perp_platform/supervisor/test_state_flow.py`

**Step 1: Write the failing tests**

- LIVE -> DEGRADED -> RESYNCING -> REDUCE_ONLY -> BLOCKED
- BLOCKED 在健康输入下保持 BLOCKED
- DEGRADED 在健康输入下回 LIVE
- instrument projection 不放松 venue 限制

**Step 2: Run targeted tests to verify failure**

Run:

```bash
py -m pytest tests/perp_platform/supervisor/test_state_flow.py -q
```

Expected:
- FAIL，因为测试文件刚建立，场景尚未调通

**Step 3: Commit**

```bash
git add tests/perp_platform/supervisor/test_state_flow.py
git commit -m "test: define supervisor state flow scenarios"
```

### Task 2: Update architecture documentation

**Files:**
- Modify: `docs/architecture/STATE_MACHINE.md`
- Test: `tests/perp_platform/supervisor/test_state_flow.py`

**Step 1: Update STATE_MACHINE.md**

- 写清状态枚举
- 写清允许迁移
- 写清 trigger thresholds
- 写清 venue / instrument projection 语义
- 写清 `BLOCKED` 不能直接回 `LIVE`

**Step 2: Run targeted and area tests**

Run:

```bash
py -m pytest tests/perp_platform/supervisor/test_state_flow.py -q
py -m pytest tests/perp_platform/supervisor -q
```

Expected:
- PASS

**Step 3: Commit**

```bash
git add docs/architecture/STATE_MACHINE.md tests/perp_platform/supervisor/test_state_flow.py
git commit -m "docs: add supervisor state flow coverage"
```

### Task 3: Verify full scope and prepare merge

**Files:**
- Modify: `docs/plans/2026-03-20-issue-42-supervisor-docs-design.md`
- Modify: `docs/plans/2026-03-20-issue-42-supervisor-docs.md`

**Step 1: Run verification**

Run:

```bash
py -m pytest tests/perp_platform/supervisor/test_state_flow.py -q
py -m pytest tests/perp_platform/supervisor -q
py -m pytest tests -q
```

Expected:
- 全部 PASS

**Step 2: Confirm scope**

- 仅新增 state flow 测试
- 仅更新 `STATE_MACHINE.md`
- 无生产代码改动

**Step 3: Commit**

```bash
git add docs/plans/2026-03-20-issue-42-supervisor-docs-design.md docs/plans/2026-03-20-issue-42-supervisor-docs.md
git commit -m "docs: add issue 42 supervisor docs plan"
```
