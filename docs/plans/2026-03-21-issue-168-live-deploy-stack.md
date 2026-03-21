# Issue 168 Live Deploy Stack Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a deployable long-running control-plane and operator UI stack, then write a deployment acceptance manual that can be executed on the live canary host.

**Architecture:** Split the deployment surface into two services. Keep `control-plane` as the Python backend entrypoint and serve the operator UI from a separate static container, then update deploy scripts and runbooks to validate both services on the target host.

**Tech Stack:** Python 3.12, Docker, docker compose, React/Vite, Nginx, Playwright, pytest

---

### Task 1: Add failing deploy contract tests

**Files:**
- Create: `tests/ops/test_live_deploy_stack_contract.py`
- Test: `tests/ops/test_live_deploy_stack_contract.py`

**Step 1: Write the failing test**

Add tests that assert:

- `deploy/docker-compose.yml` contains `control-plane` and `operator-ui`
- `control-plane` command uses `python -m perp_platform.control_plane`
- `deploy/operator-ui.Dockerfile` exists
- `deploy/scripts/deploy.sh` uses `docker compose up -d`
- `deploy/scripts/rollback.sh` uses `docker compose up -d`

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/ops/test_live_deploy_stack_contract.py -q`

Expected: FAIL because the current compose and scripts still use the old bootstrap model.

**Step 3: Commit**

```bash
git add tests/ops/test_live_deploy_stack_contract.py
git commit -m "test: add live deploy stack contract"
```

### Task 2: Implement the dual-service deploy stack

**Files:**
- Modify: `deploy/docker-compose.yml`
- Modify: `deploy/Dockerfile`
- Create: `deploy/operator-ui.Dockerfile`
- Modify: `deploy/scripts/deploy.sh`
- Modify: `deploy/scripts/rollback.sh`

**Step 1: Write minimal implementation**

Update compose to define:

- `control-plane`
- `operator-ui`

Update the Python image to support the control-plane entrypoint cleanly. Add a new operator UI Dockerfile that builds the Vite app and serves it statically.

**Step 2: Run contract test**

Run: `py -m pytest tests/ops/test_live_deploy_stack_contract.py -q`

Expected: PASS

**Step 3: Build both services locally**

Run: `docker compose -f deploy/docker-compose.yml --env-file deploy/live-canary.env.example config`

Expected: rendered compose output with both services.

**Step 4: Commit**

```bash
git add deploy/docker-compose.yml deploy/Dockerfile deploy/operator-ui.Dockerfile deploy/scripts/deploy.sh deploy/scripts/rollback.sh
git commit -m "feat: add live deploy stack services"
```

### Task 3: Update deployment and acceptance runbooks

**Files:**
- Modify: `docs/runbooks/live-canary-deploy.md`
- Create: `docs/runbooks/live-canary-acceptance.md`
- Modify: `README.md`

**Step 1: Update the deploy runbook**

Document the new long-running services, health checks, and the difference between deployment completion and live canary execution.

**Step 2: Write the acceptance manual**

Add a runbook that covers:

- server prerequisites
- env and secrets paths
- deploy commands
- health checks
- operator UI access
- rollback commands
- readiness gate before entering `#153`

**Step 3: Verify docs are internally consistent**

Run: `py -m pytest tests/ops/test_live_deploy_stack_contract.py -q`

Expected: PASS

**Step 4: Commit**

```bash
git add docs/runbooks/live-canary-deploy.md docs/runbooks/live-canary-acceptance.md README.md
git commit -m "docs: add live deploy acceptance manual"
```

### Task 4: Verify frontend build and e2e still pass

**Files:**
- Reuse existing frontend files only

**Step 1: Build the UI**

Run: `npm --prefix apps/control-plane-ui run build`

Expected: PASS

**Step 2: Run operator UI e2e**

Run: `npx playwright test tests/e2e`

Expected: PASS

**Step 3: Commit if any test-only adjustments were required**

```bash
git add apps/control-plane-ui tests/e2e
git commit -m "test: keep operator ui deployable"
```

### Task 5: Run full Python verification

**Files:**
- Reuse current repository

**Step 1: Run full test suite**

Run: `py -m pytest tests -q`

Expected: PASS

**Step 2: Commit final verification state**

```bash
git add .
git commit -m "chore: verify live deploy stack"
```

### Task 6: Verify the deploy stack on the target host

**Files:**
- Reuse remote host `root@38.60.236.47`

**Step 1: Sync repository state**

Push the branch or sync the changed files to `/srv/perp-platform/repo`.

**Step 2: Run preflight**

Run the remote preflight against `/srv/perp-platform/deploy/.env`.

Expected: it may still fail only when credentials are absent.

**Step 3: Bring up the stack**

Run the remote deploy command and verify:

- `control-plane` is running
- `operator-ui` is running
- `/healthz` is reachable
- the UI homepage is reachable

**Step 4: Record deployment evidence**

Capture the exact commands and outputs into the acceptance runbook or issue comment for `#168`.

**Step 5: Commit docs-only evidence updates if needed**

```bash
git add docs/runbooks/live-canary-acceptance.md
git commit -m "docs: record live deploy verification"
```
