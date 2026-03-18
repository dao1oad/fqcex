# fqcex 项目记忆系统 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 `fqcex` 建立一套“手工稳定记忆 + 自动项目快照”的项目记忆系统，帮助新会话快速掌握当前代码现状、分支/worktree 状态和整体进展。

**Architecture:** 使用 `docs/memory` 目录承载长期稳定记忆与新会话 handoff，用 Python 脚本从 Git / GitHub 收集动态状态并生成 `generated/project_snapshot.md`，再用 PowerShell 快捷脚本为本地会话提供统一入口。更新 `README.md` 与 `AGENTS.md`，把记忆系统纳入标准工作流。

**Tech Stack:** Python 3.12, pytest, PowerShell, Git, GitHub CLI

---

### Task 1: 建立记忆文档骨架

**Files:**
- Create: `docs/memory/PROJECT_STATE.md`
- Create: `docs/memory/ACTIVE_WORK.md`
- Create: `docs/memory/SESSION_HANDOFF.md`
- Create: `docs/memory/generated/.gitkeep`

**Step 1: Write the failing test**

先写一个 Python 测试，断言记忆目录和三个核心文档路径存在。

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/memory/test_memory_docs.py -v`
Expected: FAIL，因为记忆目录和文件尚不存在。

**Step 3: Write minimal implementation**

创建目录和三个文档模板，并补 `generated/.gitkeep`。

**Step 4: Run test to verify it passes**

Run: `py -m pytest tests/memory/test_memory_docs.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add docs/memory tests/memory/test_memory_docs.py
git commit -m "docs: add project memory document skeleton"
```

### Task 2: 建立项目快照脚本的输出契约

**Files:**
- Create: `tests/memory/test_update_project_memory.py`
- Create: `scripts/update_project_memory.py`

**Step 1: Write the failing test**

写测试断言：

- 脚本生成 `docs/memory/generated/project_snapshot.md`
- 输出中至少包含：
  - `Current Branch`
  - `Worktrees`
  - `Recent Commits`
  - `Repository Docs`

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/memory/test_update_project_memory.py -v`
Expected: FAIL，因为脚本尚不存在。

**Step 3: Write minimal implementation**

实现 `update_project_memory.py`：

- 解析仓库根路径
- 执行 Git 命令
- 输出 Markdown
- 创建 `generated/project_snapshot.md`

**Step 4: Run test to verify it passes**

Run: `py -m pytest tests/memory/test_update_project_memory.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add scripts/update_project_memory.py tests/memory/test_update_project_memory.py docs/memory/generated/project_snapshot.md
git commit -m "feat: add project snapshot generator"
```

### Task 3: 为 GitHub 信息做降级处理

**Files:**
- Modify: `scripts/update_project_memory.py`
- Modify: `tests/memory/test_update_project_memory.py`

**Step 1: Write the failing test**

补测试断言：

- 当 `gh` 不可用或命令失败时
- 脚本不会崩溃
- 快照中会包含 `GitHub metadata unavailable`

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/memory/test_update_project_memory.py -v`
Expected: FAIL

**Step 3: Write minimal implementation**

在脚本里为 `gh issue list`、`gh pr list` 增加异常处理与降级文案。

**Step 4: Run test to verify it passes**

Run: `py -m pytest tests/memory/test_update_project_memory.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add scripts/update_project_memory.py tests/memory/test_update_project_memory.py
git commit -m "feat: handle github metadata fallback in memory snapshot"
```

### Task 4: 建立本地会话入口脚本

**Files:**
- Create: `scripts/project_context.ps1`
- Create: `tests/memory/test_project_context.py`

**Step 1: Write the failing test**

写测试验证 `project_context.ps1` 文件存在，并检查脚本内容包含：

- `git status`
- `git worktree list`
- `docs/memory/PROJECT_STATE.md`

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/memory/test_project_context.py -v`
Expected: FAIL

**Step 3: Write minimal implementation**

创建 `project_context.ps1`，输出：

- 当前分支
- worktree 列表
- 最近提交
- 记忆系统入口文件路径

**Step 4: Run test to verify it passes**

Run: `py -m pytest tests/memory/test_project_context.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add scripts/project_context.ps1 tests/memory/test_project_context.py
git commit -m "feat: add local project context command"
```

### Task 5: 将记忆系统接入仓库入口文档

**Files:**
- Modify: `README.md`
- Modify: `AGENTS.md`

**Step 1: Write the failing test**

补测试断言：

- `README.md` 包含 `docs/memory/PROJECT_STATE.md`
- `AGENTS.md` 包含新会话应先运行记忆脚本的说明

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/memory/test_memory_entrypoints.py -v`
Expected: FAIL

**Step 3: Write minimal implementation**

- 在 `README.md` 增加 Memory System 小节
- 在 `AGENTS.md` 增加新会话入口流程

**Step 4: Run test to verify it passes**

Run: `py -m pytest tests/memory/test_memory_entrypoints.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add README.md AGENTS.md tests/memory/test_memory_entrypoints.py
git commit -m "docs: add memory system entrypoints"
```

### Task 6: 生成初始项目快照并校验内容

**Files:**
- Modify: `docs/memory/ACTIVE_WORK.md`
- Modify: `docs/memory/SESSION_HANDOFF.md`
- Modify: `docs/memory/generated/project_snapshot.md`

**Step 1: Write the failing test**

补测试断言：

- 快照中包含当前活跃分支名
- 包含 `codex/ci-cd-bootstrap`
- 包含至少一个 roadmap / docs 文件入口

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/memory/test_update_project_memory.py -v`
Expected: FAIL

**Step 3: Write minimal implementation**

- 更新 `ACTIVE_WORK.md`
- 更新 `SESSION_HANDOFF.md`
- 运行 `scripts/update_project_memory.py`

**Step 4: Run test to verify it passes**

Run:
- `py scripts/update_project_memory.py`
- `py -m pytest tests/memory/test_update_project_memory.py -v`

Expected: PASS

**Step 5: Commit**

```bash
git add docs/memory scripts/update_project_memory.py
git commit -m "docs: generate initial project memory snapshot"
```

### Task 7: 全量验证

**Files:**
- Verify only

**Step 1: Run verification**

Run:

```bash
py -m pytest tests/memory -v
py scripts/update_project_memory.py
powershell -ExecutionPolicy Bypass -File scripts/project_context.ps1
git diff --check
```

Expected:

- 所有 memory 相关测试通过
- 快照文件成功生成
- PowerShell 上下文输出成功
- `git diff --check` 无格式问题

**Step 2: Commit**

```bash
git add .
git commit -m "feat: add repository memory system"
```

Plan complete and saved to `docs/plans/2026-03-18-project-memory-system-implementation.md`. Two execution options:

**1. Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

**Which approach?**
