# Issue 62 Injector Runbooks Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 把故障注入脚本接入 incident / recovery runbook，形成操作员可执行说明。

**Architecture:** 仅修改 runbook 文档，不新增代码。文档中明确命令、输出文件、incident 留痕字段和升级条件。

**Tech Stack:** Markdown documentation

---

### Task 1: Update incident template

**Files:**
- Modify: `docs/runbooks/incident-template.md`

**Step 1: Add fault injection record fields**

新增：

- injected scenario
- injector script
- injector plan path
- observed supervisor/checker state

### Task 2: Update recovery runbooks

**Files:**
- Modify: `docs/runbooks/public-stream-recovery.md`
- Modify: `docs/runbooks/private-stream-recovery.md`

**Step 1: Add injector command examples**

**Step 2: Add operator logging expectations**

### Task 3: Verify by manual review

**Files:**
- Modify: `docs/plans/2026-03-20-issue-62-injector-runbooks-design.md`
- Modify: `docs/plans/2026-03-20-issue-62-injector-runbooks.md`

**Step 1: Review docs for consistency with scripts #59-#61**

**Step 2: Final commit**

```bash
git add docs/runbooks/incident-template.md docs/runbooks/private-stream-recovery.md docs/runbooks/public-stream-recovery.md docs/plans/2026-03-20-issue-62-injector-runbooks-design.md docs/plans/2026-03-20-issue-62-injector-runbooks.md
git commit -m "docs: add fault injection runbook guidance"
```
