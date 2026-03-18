# Governance Bootstrap Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 初始化 `dao1oad/fqcex` 私有 GitHub 仓库和本地 `D:\fqcex` 工作区，建立项目治理骨架、文档体系和最小 CI/PR 约束。

**Architecture:** 使用单仓治理模式，以 `main` 为唯一长期分支。仓库首批内容只包含治理骨架：README、roadmap、architecture、ADR、runbooks、GitHub issue/PR 模板、CODEOWNERS 和最小 CI。后续代码实现统一在该治理骨架之上展开。

**Tech Stack:** Git, GitHub CLI, Markdown, YAML, GitHub Actions.

---

### Task 1: Initialize Private Repository

**Files:**
- Create: `D:\fqcex\.git\`

**Step 1: Verify repository does not already exist**

Run: `gh repo view dao1oad/fqcex --json name,owner,visibility,url`  
Expected: FAIL with repository not found

**Step 2: Create the private GitHub repository**

Run: `gh repo create dao1oad/fqcex --private --description "Perp connection platform for multi-exchange arbitrage" --disable-issues=false --disable-wiki=true`
Expected: Repo created successfully

**Step 3: Initialize local git repository**

Run: `git init -b main`
Expected: Local repository initialized on `main`

**Step 4: Add remote origin**

Run: `git remote add origin https://github.com/dao1oad/fqcex.git`
Expected: `origin` points to the new repo

**Step 5: Commit**

```bash
git status --short
```

Expected: Clean repo before adding governance files

### Task 2: Add Repository Governance Skeleton

**Files:**
- Create: `D:\fqcex\README.md`
- Create: `D:\fqcex\.gitignore`
- Create: `D:\fqcex\docs\roadmap\ROADMAP.md`
- Create: `D:\fqcex\docs\architecture\ARCHITECTURE.md`
- Create: `D:\fqcex\docs\architecture\STATE_MACHINE.md`
- Create: `D:\fqcex\docs\architecture\DATA_MODEL.md`
- Create: `D:\fqcex\docs\decisions\PHASE1_FREEZE.md`

**Step 1: Write the failing validation checklist**

Document expected root files and folders:

- `README.md`
- `.gitignore`
- `docs/roadmap`
- `docs/architecture`
- `docs/decisions`

**Step 2: Implement the minimal governance docs**

Add:

- project scope
- non-goals
- phase roadmap
- first-stage freeze list
- core architecture references

**Step 3: Verify structure**

Run: `Get-ChildItem -Recurse D:\fqcex`
Expected: Governance files and folders exist

**Step 4: Commit**

```bash
git add README.md .gitignore docs
git commit -m "docs: add governance skeleton"
```

### Task 3: Add ADRs and Runbooks

**Files:**
- Create: `D:\fqcex\docs\adr\0001-main-runtime-is-nautilus.md`
- Create: `D:\fqcex\docs\adr\0002-phase1-usdt-linear-perps-only.md`
- Create: `D:\fqcex\docs\adr\0003-supervisor-owns-tradeability.md`
- Create: `D:\fqcex\docs\runbooks\public-stream-recovery.md`
- Create: `D:\fqcex\docs\runbooks\private-stream-recovery.md`
- Create: `D:\fqcex\docs\runbooks\force-resume-policy.md`
- Create: `D:\fqcex\docs\runbooks\incident-template.md`

**Step 1: Add ADRs with Context / Decision / Consequences**

Each ADR should answer:

- what was decided
- why it was chosen
- what trade-offs were accepted

**Step 2: Add runbooks with trigger / action / escalation**

Each runbook should define:

- symptom
- automatic response
- manual actions
- escalation conditions

**Step 3: Verify docs render cleanly**

Run: `Get-Content D:\fqcex\docs\adr\0001-main-runtime-is-nautilus.md -TotalCount 40`
Expected: ADR format is complete and readable

**Step 4: Commit**

```bash
git add docs/adr docs/runbooks
git commit -m "docs: add adrs and runbooks"
```

### Task 4: Add GitHub Governance Files

**Files:**
- Create: `D:\fqcex\.github\ISSUE_TEMPLATE\feature_request.md`
- Create: `D:\fqcex\.github\ISSUE_TEMPLATE\bug_report.md`
- Create: `D:\fqcex\.github\ISSUE_TEMPLATE\ops_incident.md`
- Create: `D:\fqcex\.github\ISSUE_TEMPLATE\adr_proposal.md`
- Create: `D:\fqcex\.github\PULL_REQUEST_TEMPLATE.md`
- Create: `D:\fqcex\.github\CODEOWNERS`
- Create: `D:\fqcex\.github\workflows\ci.yml`

**Step 1: Define issue templates**

Templates should cover:

- feature request
- bug report
- ops incident
- ADR proposal

**Step 2: Define PR template**

The PR template must require:

- purpose
- impact area
- risk
- verification
- docs/runbook/ADR implications

**Step 3: Define minimal CI**

The workflow should at least:

- checkout repo
- validate markdown files exist
- run a simple shell verification step

**Step 4: Commit**

```bash
git add .github
git commit -m "chore: add github governance files"
```

### Task 5: Push Initial Governance Baseline

**Files:**
- Modify: `D:\fqcex\*`

**Step 1: Review git history**

Run: `git log --oneline --decorate -5`
Expected: Governance commits are present locally

**Step 2: Push main to origin**

Run: `git push -u origin main`
Expected: `main` published to `dao1oad/fqcex`

**Step 3: Verify repository view**

Run: `gh repo view dao1oad/fqcex --web`
Expected: Repo opens with governance files visible

**Step 4: Manual follow-up**

After push, configure:

- branch protection on `main`
- default labels
- milestone set for `Phase 0` to `Phase 6`

**Step 5: Commit**

No additional commit; this task ends with published baseline.
