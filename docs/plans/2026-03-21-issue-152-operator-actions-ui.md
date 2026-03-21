# Operator Action UI Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a minimal operator action page that enforces static preconditions and echoes accepted actions into the audit timeline.

**Architecture:** Keep the Phase 5 UI fixture-backed. Extend the existing shared shell so audit events live in one in-memory state store, then add an `/actions` route that writes to that shared state when a valid action is submitted.

**Tech Stack:** React 19, React Router 7, Vite 7, Playwright, Python pytest for repo-wide regression.

---

### Task 1: Write the failing E2E for operator actions

**Files:**
- Create: `tests/e2e/operator-actions-ui.spec.ts`
- Modify: `tests/e2e/operator-readonly-ui.spec.ts` (only if route assertions need adjustment)

**Step 1: Write the failing test**

- Cover one blocked flow and one successful flow.
- Assert:
  - `/actions` page is reachable
  - blocked `force_resume` shows unmet preconditions and disabled submit
  - valid `force_resume` submission creates a new audit event visible in the UI

**Step 2: Run test to verify it fails**

Run: `npx playwright test tests/e2e/operator-actions-ui.spec.ts`

### Task 2: Extend static fixtures and shared shell state

**Files:**
- Modify: `apps/control-plane-ui/src/static-data.ts`
- Modify: `apps/control-plane-ui/src/router.tsx`

**Step 1: Add operator action fixture types and sample targets**

- Define action target records and precondition fields.

**Step 2: Lift audit events into shared shell state**

- Initialize shared audit state in `Shell`
- Expose it to routes

**Step 3: Re-run failing E2E**

Run: `npx playwright test tests/e2e/operator-actions-ui.spec.ts`

Expected: still failing because `/actions` is not implemented yet.

### Task 3: Implement the `/actions` page

**Files:**
- Modify: `apps/control-plane-ui/src/router.tsx`
- Modify: `apps/control-plane-ui/src/styles.css`

**Step 1: Add action route and navigation entry**

**Step 2: Implement minimal form**

- target select
- action select
- reason textarea/input
- precondition checklist
- disabled submit state when invalid

**Step 3: On submit, append a new audit event using shared state**

### Task 4: Verify the UI behavior

**Files:**
- Modify: `apps/control-plane-ui/src/router.tsx`
- Modify: `apps/control-plane-ui/src/styles.css`

**Step 1: Run E2E**

Run: `npx playwright test tests/e2e/operator-actions-ui.spec.ts`

**Step 2: Run the whole E2E folder**

Run: `npx playwright test tests/e2e`

### Task 5: Update docs and run repository regression

**Files:**
- Modify: `docs/runbooks/operator-readonly-ui.md`
- Modify: `README.md`

**Step 1: Document the new `/actions` page and acceptance flow**

**Step 2: Run build and repo regression**

Run:
- `npm --prefix apps/control-plane-ui run build`
- `py -m pytest tests -q`

### Task 6: Commit and prepare PR

**Files:**
- Modify: all files changed above

**Step 1: Review diff for build artifacts**

**Step 2: Commit**

Suggested commit:

```bash
git add apps/control-plane-ui tests/e2e README.md docs/runbooks/operator-readonly-ui.md
git commit -m "feat: add operator actions ui"
```
