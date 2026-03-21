# Live Deploy Hardening Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Harden the live deploy stack so deployment acceptance can pass on the real host without exposing unauthenticated operator APIs or failing on legacy `docker-compose`.

**Architecture:** Keep the existing dual-service stack, but tighten host exposure, add restart semantics, make deploy/rollback deterministic on standalone `docker-compose`, and align the runbooks with the actual script contract. Do not expand into real exchange canaries in this issue.

**Tech Stack:** Docker Compose, POSIX shell, Python pytest, Markdown runbooks

---

### Task 1: Lock the failing contracts

**Files:**
- Modify: `tests/governance/test_deploy_contract.py`
- Modify: `tests/ops/test_live_deploy_stack_contract.py`

**Step 1: Write the failing tests**

- Add assertions for:
  - loopback host binding defaults
  - restart policy
  - bootstrap `python3` prerequisite
  - legacy compose cleanup before `up`
  - rollback UI image validation
  - acceptance runbook mentioning compose variants and env-driven ports

**Step 2: Run tests to verify they fail**

Run:

```bash
py -m pytest tests/governance/test_deploy_contract.py tests/ops/test_live_deploy_stack_contract.py -q
```

Expected: FAIL on the new deploy hardening assertions.

### Task 2: Implement minimal deploy hardening

**Files:**
- Modify: `deploy/docker-compose.yml`
- Modify: `deploy/live-canary.env.example`
- Modify: `deploy/scripts/bootstrap-server.sh`
- Modify: `deploy/scripts/deploy.sh`
- Modify: `deploy/scripts/rollback.sh`

**Step 1: Update compose defaults**

- Add loopback bind address env vars
- Add restart policy to both services

**Step 2: Update scripts**

- Add `python3` precheck in bootstrap
- Add standalone `docker-compose` cleanup path before `up`
- Add UI image existence validation in rollback

**Step 3: Run tests to verify they pass**

Run:

```bash
py -m pytest tests/governance/test_deploy_contract.py tests/ops/test_live_deploy_stack_contract.py -q
```

Expected: PASS

### Task 3: Align roadmap and runbooks

**Files:**
- Modify: `docs/roadmap/ISSUE_HIERARCHY.md`
- Modify: `docs/runbooks/deploy.md`
- Modify: `docs/runbooks/live-canary-acceptance.md`
- Modify: `docs/runbooks/live-canary-deploy.md`

**Step 1: Update docs**

- Insert `#170` in the Phase 5 order before `#153`
- Document loopback binding, compose variants, `python3` prerequisite, and env-driven ports

**Step 2: Verify doc contracts**

Run:

```bash
py -m pytest tests/governance/test_deploy_contract.py tests/ops/test_live_deploy_stack_contract.py -q
```

Expected: PASS with updated docs.

### Task 4: Re-verify on the real host

**Files:**
- No repo file changes required unless a new defect appears

**Step 1: Sync host to `origin/main`**

Run on `38.60.236.47`:

```bash
cd /srv/perp-platform/repo
git fetch origin
git checkout main
git reset --hard origin/main
```

**Step 2: Re-deploy**

Run:

```bash
sh deploy/scripts/deploy.sh /srv/perp-platform/deploy/.env
```

Expected: stack starts without legacy compose recreate failure.

**Step 3: Health checks**

Run:

```bash
python3 - <<'PY'
import urllib.request
for url in [
    "http://127.0.0.1:8080/control-plane/v1/health",
    "http://127.0.0.1:4173/",
    "http://127.0.0.1:4173/actions",
]:
    with urllib.request.urlopen(url, timeout=10) as resp:
        print(url, resp.status)
PY
```

Expected: all return `200`.

### Task 5: Full verification and issue closeout

**Files:**
- No mandatory file changes

**Step 1: Run full verification**

```bash
py -m pytest tests -q
```

Expected: PASS

**Step 2: Record GitHub evidence**

- Update the PR with review evidence
- Comment on `#170` with remote deployment proof
- Comment on `#153` that deploy stack defects are cleared and only real credentials remain blocked

**Step 3: Merge and close**

- Merge PR to `main`
- Close `#170`
