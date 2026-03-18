# AGENTS And Roadmap Issues Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 `fqcex` 仓库新增全局 `AGENTS.md`，并按已冻结的 roadmap 在 GitHub 中批量初始化 epics 和 issues。

**Architecture:** `AGENTS.md` 作为仓库级协作约束文件，负责冻结语言、范围、架构边界、Phase 1 限制、文档更新与运行安全要求。GitHub issues 采用“普通 issue + `type/epic` label”的方式表达 epic，并按 `Phase 0` 到 `Phase 6` 分 milestones 和 phase labels 管理。

**Tech Stack:** Markdown, Git, GitHub CLI.

---

### Task 1: Define Global Agent Contract

**Files:**
- Create: `D:\fqcex\AGENTS.md`

**Step 1: Write the required sections checklist**

The file must define:

- language and documentation rules
- repo mission and phase 1 scope
- frozen phase 1 constraints
- architecture ownership boundaries
- change control rules
- testing and runbook update requirements

**Step 2: Implement the AGENTS document**

Add a concise but strict repo-level instruction file covering all required sections.

**Step 3: Verify file exists**

Run: `Get-Content D:\fqcex\AGENTS.md -TotalCount 80`
Expected: All required sections are present

**Step 4: Commit**

```bash
git -C D:\fqcex add AGENTS.md
git -C D:\fqcex commit -m "docs: add repository agents guide"
```

### Task 2: Add Phase Labels and Epic Label

**Files:**
- Modify: GitHub repo labels only

**Step 1: Create missing labels**

Create:

- `type/epic`
- `phase/0`
- `phase/1`
- `phase/2`
- `phase/3`
- `phase/4`
- `phase/5`
- `phase/6`

**Step 2: Verify labels**

Run: `gh label list --repo dao1oad/fqcex`
Expected: The new labels are present

**Step 3: Commit**

No git commit; this task changes GitHub metadata only.

### Task 3: Create Phase Epics

**Files:**
- Modify: GitHub issues only

**Step 1: Create one epic per roadmap phase**

Required epics:

- Phase 0 - Design Freeze
- Phase 1 - Single Venue Loop
- Phase 2 - Three Venue Baseline
- Phase 3 - Checker and Dry Run
- Phase 4 - Platformization
- Phase 5 - Native Tier-1 Adapters
- Phase 6 - Scale and HA

**Step 2: Assign labels and milestones**

Each epic should get:

- `type/epic`
- matching `phase/x`
- the matching milestone

**Step 3: Verify issue list**

Run: `gh issue list --repo dao1oad/fqcex --limit 20`
Expected: Seven roadmap epics appear

### Task 4: Create Phase 0 to Phase 3 Delivery Issues

**Files:**
- Modify: GitHub issues only

**Step 1: Create child issues for early roadmap execution**

Minimum issues:

- governance and design freeze
- supervisor state machine implementation
- truth store schema
- Bybit runtime bootstrap
- Bybit recovery and reconciliation
- Binance runtime bootstrap
- Binance quota-safe recovery tuning
- OKX runtime bootstrap
- OKX quantity conversion
- Cryptofeed checker
- failure injection and dry run

**Step 2: Link each issue to a parent epic in the body**

Use the issue body to reference the parent epic number.

**Step 3: Verify issue structure**

Run: `gh issue list --repo dao1oad/fqcex --limit 50`
Expected: Early execution issues appear under matching labels and milestones

### Task 5: Push and Verify Repository State

**Files:**
- Modify: `D:\fqcex\*`

**Step 1: Push AGENTS commit**

Run: `git -C D:\fqcex push`
Expected: Remote `main` updated

**Step 2: Verify AGENTS file on GitHub**

Run: `gh repo view dao1oad/fqcex --web`
Expected: Repository opens with `AGENTS.md` present on `main`

**Step 3: Verify issues and epics**

Run: `gh issue list --repo dao1oad/fqcex --limit 50`
Expected: Epics and initial roadmap issues exist
