# Issue 63 Dry Run Config Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 BTC / ETH 小规模干跑补齐配置模板与部署安全闸门说明。

**Architecture:** 只新增 `deploy/dry-run.env` 模板并更新 `docs/runbooks/deploy.md`，不引入新的运行时代码。

**Tech Stack:** dotenv template, Markdown documentation

---

### Task 1: Add dry-run env template

**Files:**
- Create: `deploy/dry-run.env`

### Task 2: Update deploy runbook

**Files:**
- Modify: `docs/runbooks/deploy.md`

### Task 3: Manual verification

**Files:**
- Modify: `docs/plans/2026-03-20-issue-63-dry-run-config-design.md`
- Modify: `docs/plans/2026-03-20-issue-63-dry-run-config.md`

**Step 1: Review env template and deploy runbook for consistency**

**Step 2: Final commit**

```bash
git add deploy/dry-run.env docs/runbooks/deploy.md docs/plans/2026-03-20-issue-63-dry-run-config-design.md docs/plans/2026-03-20-issue-63-dry-run-config.md
git commit -m "docs: add dry run config template"
```
