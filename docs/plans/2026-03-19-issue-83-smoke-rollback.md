# #83 Smoke Rollback Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 `perp_platform` 建立手动触发的最小 smoke workflow、Playwright 工具基线、显式 tag 的 rollback 脚本和 rollback runbook。

**Architecture:** 通过 `cd.yml` 串联 `deploy/scripts/deploy.sh` 与 `npm run smoke:e2e`，把 shell 驱动的最小部署 smoke 作为主链路；Playwright 只验证本地 fixture 以确保 e2e 工具基线可用。rollback 使用独立脚本读取当前 env 并生成临时 env，将镜像 tag 切回显式传入的 previous tag，再通过 `docker compose run --rm --no-build` 执行最小回退验证。

**Tech Stack:** GitHub Actions, Node.js 22, npm, Playwright, POSIX shell, Markdown, Python 3.12, `pytest`.

---

### Task 1: 建立 smoke / rollback 契约测试

**Files:**
- Create: `tests/governance/test_smoke_rollback_contract.py`

**Step 1: Write the failing test**

```python
from pathlib import Path


def test_cd_workflow_exists():
    assert Path(".github/workflows/cd.yml").exists()
```

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/governance/test_smoke_rollback_contract.py -q`
Expected: FAIL because the smoke / rollback scaffold does not exist yet.

**Step 3: Commit**

```bash
git add tests/governance/test_smoke_rollback_contract.py
git commit -m "test: add smoke rollback contract"
```

### Task 2: 落地 smoke workflow、Playwright 基线与 rollback 文档

**Files:**
- Create: `.github/workflows/cd.yml`
- Create: `package.json`
- Create: `playwright.config.ts`
- Create: `tests/e2e/fixtures/index.html`
- Create: `tests/e2e/smoke.spec.ts`
- Create: `deploy/scripts/rollback.sh`
- Create: `docs/runbooks/rollback.md`
- Modify: `.gitignore`
- Modify: `tests/governance/test_smoke_rollback_contract.py`

**Step 1: Write minimal implementation**

```yaml
on:
  workflow_dispatch:
```

```json
{
  "scripts": {
    "smoke:e2e": "playwright test tests/e2e/smoke.spec.ts"
  }
}
```

```sh
docker compose --env-file "$TMP_ENV" -f "$COMPOSE_FILE" run --rm --no-build perp-platform
```

**Step 2: Generate package lock**

Run: `npm install --save-dev @playwright/test`
Expected: `package-lock.json` created and `package.json` updated with the resolved dependency version.

**Step 3: Run targeted tests**

Run: `py -m pytest tests/governance/test_smoke_rollback_contract.py -q`
Expected: PASS

**Step 4: Run full tests**

Run: `py -m pytest tests -q`
Expected: PASS

**Step 5: Commit**

```bash
git add .github/workflows/cd.yml package.json package-lock.json playwright.config.ts tests/e2e/fixtures/index.html tests/e2e/smoke.spec.ts deploy/scripts/rollback.sh docs/runbooks/rollback.md .gitignore tests/governance/test_smoke_rollback_contract.py
git commit -m "ops: add smoke and rollback scaffold"
```

### Task 3: 做本地 smoke 工具链验证

**Files:**
- Verify only: `package.json`
- Verify only: `playwright.config.ts`
- Verify only: `tests/e2e/smoke.spec.ts`
- Verify only: `deploy/scripts/rollback.sh`
- Verify only: `.github/workflows/cd.yml`

**Step 1: Install Node dependencies**

Run: `npm ci`
Expected: dependency install succeeds with the generated lockfile.

**Step 2: Install Playwright browser**

Run: `npx playwright install chromium`
Expected: Chromium installed for local smoke validation.

**Step 3: Run smoke spec**

Run: `npx playwright test tests/e2e/smoke.spec.ts`
Expected: PASS

**Step 4: Re-run Python tests**

Run: `py -m pytest tests -q`
Expected: PASS

**Step 5: Commit**

```bash
git add docs/plans/2026-03-19-issue-83-smoke-rollback-design.md docs/plans/2026-03-19-issue-83-smoke-rollback.md
git commit -m "docs: add issue 83 design and plan"
```
