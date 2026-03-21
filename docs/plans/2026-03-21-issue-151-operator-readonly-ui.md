# Issue 151 Operator Readonly UI Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 增加最小只读 operator 验收控制台，支持查看 tradeability、recovery runs 和 audit events，并提供基础 Playwright E2E 验证。

**Architecture:** 在 `apps/control-plane-ui` 中建立独立 React/Vite 前端骨架，用静态 adapter 提供当前 control-plane 契约对应的 fixture 数据。第一版只做只读页面和导航，不接真实 API，不做写动作。

**Tech Stack:** React 19, TypeScript, Vite, React Router, Playwright

---

### Task 1: Add failing E2E for readonly operator UI

**Files:**
- Create: `tests/e2e/operator-readonly-ui.spec.ts`
- Modify: `playwright.config.ts`
- Modify: `package.json`

**Step 1: Write the failing test**

- 覆盖：
  - tradeability 页面能看到 venue 和 instrument 状态
  - recovery 页面能看到 recovery runs
  - audit 页面能看到 audit events

**Step 2: Run test to verify it fails**

Run: `npx playwright test tests/e2e/operator-readonly-ui.spec.ts`

Expected:

- FAIL，因为前端 app 尚不存在

**Step 3: Commit**

```bash
git add tests/e2e/operator-readonly-ui.spec.ts playwright.config.ts package.json
git commit -m "test: define operator readonly ui contract"
```

### Task 2: Implement frontend app skeleton and readonly pages

**Files:**
- Create: `apps/control-plane-ui/*`
- Test: `tests/e2e/operator-readonly-ui.spec.ts`

**Step 1: Add minimal implementation**

- Vite app skeleton
- route shell
- static data adapter
- `tradeability` / `recovery` / `audit` 页面

**Step 2: Run targeted verification**

Run:

```bash
npm --prefix apps/control-plane-ui install
npx playwright test tests/e2e/operator-readonly-ui.spec.ts
```

Expected:

- PASS

**Step 3: Commit**

```bash
git add apps/control-plane-ui tests/e2e/operator-readonly-ui.spec.ts playwright.config.ts package.json package-lock.json
git commit -m "feat: add readonly operator ui"
```

### Task 3: Update docs and run full frontend verification

**Files:**
- Create: `docs/runbooks/operator-readonly-ui.md`
- Modify: `README.md`
- Modify: `docs/plans/2026-03-21-issue-151-operator-readonly-ui-design.md`
- Modify: `docs/plans/2026-03-21-issue-151-operator-readonly-ui.md`

**Step 1: Update docs**

- 说明如何启动 UI
- 说明页面用途与边界

**Step 2: Run verification**

Run:

```bash
npm --prefix apps/control-plane-ui run build
npx playwright test tests/e2e/operator-readonly-ui.spec.ts
py -m pytest tests -q
```

Expected:

- PASS

**Step 3: Commit**

```bash
git add README.md docs/runbooks/operator-readonly-ui.md docs/plans/2026-03-21-issue-151-operator-readonly-ui-design.md docs/plans/2026-03-21-issue-151-operator-readonly-ui.md
git commit -m "docs: add operator readonly ui runbook"
```
