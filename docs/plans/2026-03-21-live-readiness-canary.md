# Live Readiness 与 Canary 阶段治理落地 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 更新 roadmap / memory 并创建新的 `Live Readiness 与 Canary 验收` epic、tracking 和 child issues，使主 agent 能按治理顺序继续推进到可真实交易验收阶段。

**Architecture:** 先在文档层插入新的阶段与 issue 顺序，再同步 memory 入口，最后通过 `gh` 创建 GitHub issue 树并回填实际编号。整个工作保持治理优先，不实现 live backend 或前端代码。

**Tech Stack:** Markdown docs, GitHub Issues (`gh` CLI), Git, Python memory updater

---

### Task 1: 固化 live 阶段设计文档

**Files:**
- Create: `docs/plans/2026-03-21-live-readiness-canary-design.md`
- Test: `docs/plans/2026-03-21-live-readiness-canary-design.md`

**Step 1: Write the design document**

- 记录背景、目标、非目标、方案比较、推荐方案
- 记录 `NautilusTrader`、`Supervisor`、`Control Plane`、`Audit` 的职责边界
- 记录 3 个 tracking、12 个 child issue 的建议结构

**Step 2: Verify the design file exists**

Run: `Get-Content D:\\fqcex\\.worktrees\\live-readiness-roadmap\\docs\\plans\\2026-03-21-live-readiness-canary-design.md -TotalCount 40`

Expected:

- 能看到设计文档标题与核心章节

**Step 3: Commit**

```bash
git add docs/plans/2026-03-21-live-readiness-canary-design.md
git commit -m "docs: add live readiness canary design"
```

### Task 2: 更新 roadmap 阶段顺序

**Files:**
- Modify: `docs/roadmap/ROADMAP.md`
- Test: `docs/roadmap/ROADMAP.md`

**Step 1: Write a failing contract mentally**

- 旧 roadmap 仍把原生适配器定义为 Phase 5，缺少 live readiness 阶段

**Step 2: Modify roadmap**

- 在当前 Phase 4 后新增：
  - `Phase 5: Live Readiness and Canary`
- 将现有：
  - `Phase 5` 顺延成 `Phase 6`
  - `Phase 6` 顺延成 `Phase 7`
- 为新阶段加入简明目标说明

**Step 3: Verify roadmap content**

Run: `Get-Content D:\\fqcex\\.worktrees\\live-readiness-roadmap\\docs\\roadmap\\ROADMAP.md -TotalCount 220`

Expected:

- 新的 Phase 5 存在
- 原生适配器顺延到 Phase 6
- 高可用顺延到 Phase 7

**Step 4: Commit**

```bash
git add docs/roadmap/ROADMAP.md
git commit -m "docs: insert live readiness stage into roadmap"
```

### Task 3: 更新 issue hierarchy，加入新 epic / tracking / child 顺序

**Files:**
- Modify: `docs/roadmap/ISSUE_HIERARCHY.md`
- Test: `docs/roadmap/ISSUE_HIERARCHY.md`

**Step 1: Edit hierarchy**

- 在现有 Phase 4 后加入新的第 5 阶段
- 为该阶段写入：
  - 1 个 epic
  - 3 个 tracking
  - 12 个 child issue 占位结构
- 将原有第 5、6 阶段顺延为新的第 6、7 阶段

**Step 2: Verify hierarchy**

Run: `Get-Content D:\\fqcex\\.worktrees\\live-readiness-roadmap\\docs\\roadmap\\ISSUE_HIERARCHY.md -TotalCount 420`

Expected:

- 新阶段结构完整可见
- 原阶段编号已顺延

**Step 3: Commit**

```bash
git add docs/roadmap/ISSUE_HIERARCHY.md
git commit -m "docs: add live readiness issue hierarchy"
```

### Task 4: 更新 architecture 和 memory 入口

**Files:**
- Modify: `docs/architecture/ARCHITECTURE.md`
- Modify: `docs/memory/PROJECT_STATE.md`
- Modify: `docs/memory/ACTIVE_WORK.md`
- Modify: `docs/memory/SESSION_HANDOFF.md`
- Modify: `docs/memory/generated/project_snapshot.md`
- Test: `docs/memory/PROJECT_STATE.md`

**Step 1: Update architecture handoff**

- 在 `ARCHITECTURE.md` 里补充 live readiness 作为下一阶段的迁移说明
- 明确 `NautilusTrader` 在新阶段继续作为 execution / reconciliation truth path

**Step 2: Update memory docs**

- `PROJECT_STATE.md`：
  - 更新远端 `main` 提交
  - 标记 Phase 4 已完成
  - 标记下一阶段为新增 Phase 5 live readiness
- `ACTIVE_WORK.md`：
  - 标记当前没有 open PR
  - 标记下一入口为新 epic / tracking / child
- `SESSION_HANDOFF.md`：
  - 调整新会话切入点，去掉“从 #67 开始”的旧口径

**Step 3: Refresh generated snapshot**

Run: `py scripts/update_project_memory.py`

Expected:

- `docs/memory/generated/project_snapshot.md` 更新

**Step 4: Verify memory docs**

Run: `Get-Content D:\\fqcex\\.worktrees\\live-readiness-roadmap\\docs\\memory\\PROJECT_STATE.md -TotalCount 220`

Expected:

- Phase 4 已完成
- 新的 live readiness 阶段被标记为下一步

**Step 5: Commit**

```bash
git add docs/architecture/ARCHITECTURE.md docs/memory/PROJECT_STATE.md docs/memory/ACTIVE_WORK.md docs/memory/SESSION_HANDOFF.md docs/memory/generated/project_snapshot.md
git commit -m "docs: refresh memory for live readiness stage"
```

### Task 5: 用 gh 创建新的 epic、tracking 与 child issues

**Files:**
- Test: GitHub issues created under repository backlog

**Step 1: Create the new epic**

Run `gh issue create` with:

- title: `第 5 阶段：Live Readiness 与 Canary 验收`
- labels: `type/epic`
- milestone: new live readiness milestone

Expected:

- 返回新的 epic issue number

**Step 2: Create the three tracking issues**

Run `gh issue create` three times for:

- 最小控制平面与审计查询实现
- live 环境、安全闸门与 operator UI
- 三交易所 live canary 与 closeout

Expected:

- 返回 3 个 tracking issue number

**Step 3: Create the 12 child issues**

Run `gh issue create` for each planned child issue, with:

- `type/task`
- `phase/5`
- relevant `area/*`
- body including:
  - 目标
  - 负责边界
  - 范围
  - 非目标
  - 依赖
  - 预期文件
  - 交付物
  - 验收标准
  - 验证
  - 关闭规则

Expected:

- 全部 child issues 建立成功
- 标题与 hierarchy 一致

**Step 4: Backfill actual issue numbers into hierarchy**

- 将 `ISSUE_HIERARCHY.md` 中占位结构替换为真实编号

**Step 5: Commit**

```bash
git add docs/roadmap/ISSUE_HIERARCHY.md
git commit -m "docs: backfill live readiness issue numbers"
```

### Task 6: 最终验证并推送分支

**Files:**
- Test: `docs/roadmap/ROADMAP.md`
- Test: `docs/roadmap/ISSUE_HIERARCHY.md`
- Test: `docs/memory/PROJECT_STATE.md`

**Step 1: Run governance-level checks**

Run:

```bash
py -m pytest tests/governance -q
py -m pytest tests/memory -q
```

Expected:

- PASS

**Step 2: Review diff**

Run:

```bash
git status --short
git diff --stat main...HEAD
```

Expected:

- 只包含 roadmap / architecture / memory / planning docs 的治理改动

**Step 3: Commit remaining docs**

```bash
git add docs/plans
git commit -m "docs: plan live readiness issue rollout"
```

**Step 4: Push branch**

```bash
git push -u origin codex/live-readiness-roadmap
```

**Step 5: Open PR**

```bash
gh pr create --fill
```

Expected:

- 形成一个只包含治理与 backlog 更新的 PR
