# fqcex Issue 分层细化与治理 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 将现有 roadmap backlog 改造成 `Epic -> Tracking Parent -> Child Implementation Issue` 三层结构，并把这套规则写入治理文档，支撑后续逐个 subagent 按 issue 编码。

**Architecture:** 保留现有 epics 与 feature issues，其中 `#10` 到 `#23` 改造成 tracking parents；为每个 tracking parent 创建细粒度 child issues；同步更新 `GOVERNANCE.md`、`CONTRIBUTING.md`、`AGENTS.md`，明确 issue 层级、关闭规则和 subagent 使用规则。

**Tech Stack:** GitHub Issues, GitHub CLI, Markdown, repository governance docs

---

### Task 1: 盘点现有 open issues 并确定分层映射

**Files:**
- Read: `docs/roadmap/ROADMAP.md`
- Read: `GOVERNANCE.md`
- Read: `CONTRIBUTING.md`
- Reference: GitHub issues `#2`-`#23`

**Step 1: 建立 issue 映射表**

为每个 open issue 标注：

- 是否 `epic`
- 是否 `tracking parent`
- 对应 `phase/*`
- 对应 `area/*`

**Step 2: 确认需新增的标签**

至少新增：

- `type/tracking`
- `type/task`

**Step 3: 记录 parent -> child 拆分数量**

为 `#10` 到 `#23` 分别定义 2 到 6 个 child issues。

### Task 2: 设计 child issue 模板

**Files:**
- Modify: `docs/plans/2026-03-18-issue-decomposition-governance-design.md`
- Use via GitHub issue bodies

**Step 1: 固定 child issue 正文结构**

模板必须包含：

- Parent Tracking Issue
- Parent Epic
- Objective
- Scope
- Out of Scope
- Dependencies
- Deliverables
- Acceptance Criteria
- Verification
- Close Rule

**Step 2: 固定 tracking parent 正文结构**

模板必须包含：

- Parent Epic
- Capability Goal
- Task Boundary
- Out of Scope
- Dependencies
- Child Issue Checklist
- Close Rule

### Task 3: 批量创建 child issues

**Files:**
- Remote: GitHub issues only

**Step 1: 先创建标签**

使用 `gh label create` 或 `gh api` 创建：

- `type/tracking`
- `type/task`

**Step 2: 为每个 tracking parent 创建 child issues**

要求：

- child issue 标题可直接作为开发任务
- 继承 phase / area 标签
- 引用父 issue 和父 epic

**Step 3: 记录 issue 编号映射**

整理 parent -> child issue number 映射，供后续写回 parent issue 正文与治理文档。

### Task 4: 批量重写 tracking parent issues

**Files:**
- Remote: GitHub issues `#10`-`#23`

**Step 1: 标题前缀改为 `[Tracking]`**

例如：

- `[Tracking] Bootstrap perp-platform application skeleton`

**Step 2: 更新标签**

- 去掉 `type/feature`
- 增加 `type/tracking`

**Step 3: 更新正文**

正文中写清：

- 该 issue 不直接编码
- child issue checklist
- 关闭条件

### Task 5: 校正 epics 的 child checklist

**Files:**
- Remote: GitHub issues `#2` 到 `#7`

**Step 1: 保持 epic 只引用 tracking parents**

不把 child issues 直接挂到 epic 上。

**Step 2: 明确 epic close rule**

增加“所有 tracking parents 完成后关闭”的文字。

### Task 6: 更新治理文档

**Files:**
- Modify: `GOVERNANCE.md`
- Modify: `CONTRIBUTING.md`
- Modify: `AGENTS.md`

**Step 1: 在治理文档中写入 issue 层级**

明确：

- `Epic`
- `Tracking Parent Issue`
- `Child Implementation Issue`

**Step 2: 写入 subagent 规则**

明确：

- subagent 只接 child issue
- 不直接从 epic / tracking parent 编码
- scope 扩大时开 sibling issue

**Step 3: 写入关闭规则**

child -> parent -> epic 的关闭顺序必须固定。

### Task 7: 验证 GitHub 结果与仓库文档一致

**Files:**
- Read: GitHub issues
- Read: `GOVERNANCE.md`
- Read: `CONTRIBUTING.md`
- Read: `AGENTS.md`

**Step 1: 抽样验证**

至少核对：

- 一个 Phase 1 tracking parent
- 一个 Phase 2 tracking parent
- 一个 Phase 3 或以后 tracking parent

**Step 2: 验证标签与父子关系**

确认：

- `type/tracking` 和 `type/task` 已使用
- tracking parents 都有 child checklist
- child issues 都有 parent 引用

**Step 3: 提交文档修改**

提交本地治理文档改动，GitHub issue 改动保留在远端。
