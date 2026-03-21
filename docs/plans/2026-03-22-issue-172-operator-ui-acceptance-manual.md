# Operator UI Acceptance Manual Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a practical operator UI acceptance manual that explains how to verify the currently implemented frontend behavior page by page.

**Architecture:** Keep the current UI unchanged and add a documentation-only runbook focused on human acceptance. Link it from the existing operator UI runbook and, if useful, the README so the manual is discoverable from the deployed surface and project docs.

**Tech Stack:** Markdown runbooks, existing React Router UI routes, existing deployment/public entrypoints

---

### Task 1: Draft the acceptance structure

**Files:**
- Create: `docs/runbooks/operator-ui-acceptance-manual.md`

**Step 1: Write the first draft**

Cover:

- public access URLs
- scope and limitations
- page-by-page acceptance steps
- action-page precondition behavior
- checklist

**Step 2: Verify coverage against the UI**

Check:

- `apps/control-plane-ui/src/router.tsx`
- `apps/control-plane-ui/src/static-data.ts`
- `docs/runbooks/operator-readonly-ui.md`

Expected: every visible page and current boundary is represented in the draft.

### Task 2: Link the manual from existing docs

**Files:**
- Modify: `docs/runbooks/operator-readonly-ui.md`
- Modify: `README.md`

**Step 1: Add discoverability links**

- Point the existing operator UI runbook to the new acceptance manual
- Add a short README entry to help reviewers find the manual quickly

**Step 2: Verify links**

Run:

```bash
Select-String -Path docs/runbooks/operator-readonly-ui.md,README.md -Pattern "operator-ui-acceptance-manual.md"
```

Expected: both files reference the new manual.

### Task 3: Final verification

**Files:**
- No additional files required

**Step 1: Validate final document content**

Check manually that the manual:

- uses the current public URLs
- mentions `/tradeability`, `/recovery`, `/audit`, `/actions`
- distinguishes static acceptance UI from real live canary

**Step 2: Record completion**

Commit the documentation changes with a docs-focused commit message.
