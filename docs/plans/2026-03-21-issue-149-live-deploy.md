# Issue 149 Live Deploy Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 live canary 增加 production-like env 模板、secret path 契约、host preflight 和 runbook。

**Architecture:** 用一份显式的 `deploy/live-canary.env.example` 冻结部署配置边界，用 `scripts/live_canary_preflight.py` 执行跨平台 preflight 校验，再由 `deploy/scripts/preflight-live.sh` 作为 Linux 主机入口。第一版只负责阻断危险部署前状态，不引入真实交易或 runtime 逻辑。

**Tech Stack:** Python 3.12, `pathlib`, `pytest`, POSIX shell

---

### Task 1: Add failing live canary preflight tests

**Files:**
- Create: `tests/ops/test_live_canary_preflight.py`
- Test: `tests/ops/test_live_canary_preflight.py`

**Step 1: Write the failing test**

- 覆盖：
  - valid env succeeds
  - missing credentials file fails
  - missing allowlist fails
  - missing kill switch file fails

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/ops/test_live_canary_preflight.py -q`

Expected:

- FAIL，因为 preflight 脚本尚不存在

**Step 3: Commit**

```bash
git add tests/ops/test_live_canary_preflight.py
git commit -m "test: define live canary preflight contract"
```

### Task 2: Implement env template and preflight

**Files:**
- Create: `deploy/live-canary.env.example`
- Create: `scripts/live_canary_preflight.py`
- Create: `deploy/scripts/preflight-live.sh`
- Modify: `tests/ops/test_live_canary_preflight.py`

**Step 1: Add minimal implementation**

- 定义 env template
- 实现 env parsing
- 校验：
  - `PERP_PLATFORM_ENVIRONMENT == live-canary`
  - `LIVE_CANARY_ENABLED == true`
  - `LIVE_CANARY_ALLOWED_VENUES`
  - `LIVE_CANARY_ALLOWED_INSTRUMENTS`
  - `LIVE_CANARY_KILL_SWITCH_PATH`
  - venue-specific credentials file paths
- shell wrapper 只负责调用 Python preflight

**Step 2: Run targeted tests**

Run:

```bash
py -m pytest tests/ops/test_live_canary_preflight.py -q
```

Expected:

- PASS

**Step 3: Commit**

```bash
git add deploy/live-canary.env.example deploy/scripts/preflight-live.sh scripts/live_canary_preflight.py tests/ops/test_live_canary_preflight.py
git commit -m "feat: add live canary preflight"
```

### Task 3: Update runbooks and verify full ops suite

**Files:**
- Modify: `docs/runbooks/deploy.md`
- Create: `docs/runbooks/live-canary-deploy.md`
- Modify: `README.md`
- Modify: `docs/plans/2026-03-21-issue-149-live-deploy-design.md`
- Modify: `docs/plans/2026-03-21-issue-149-live-deploy.md`

**Step 1: Update docs**

- 补充 live canary deploy/preflight 入口
- 明确 secret path 与 kill switch 文件只作为 host 契约，不将真实凭证提交到仓库

**Step 2: Run verification**

Run:

```bash
py -m pytest tests/ops -q
py -m pytest tests -q
```

Expected:

- PASS

**Step 3: Commit**

```bash
git add README.md docs/runbooks/deploy.md docs/runbooks/live-canary-deploy.md docs/plans/2026-03-21-issue-149-live-deploy-design.md docs/plans/2026-03-21-issue-149-live-deploy.md
git commit -m "docs: add live canary deploy runbook"
```
