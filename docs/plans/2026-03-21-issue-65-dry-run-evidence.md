# Issue 65 Dry Run Evidence Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 产出 BTC / ETH repository-scoped 干跑演练证据文档，并提交可复查的证据文件。

**Architecture:** 不改交易 runtime，只消费现有 `dry-run.env`、audit script、injector script、checker/supervisor 逻辑。证据文件落到 `docs/plans/dry-run-evidence/`，总览写入 `docs/plans/dry-run-evidence.md`。

**Tech Stack:** Python 3.12, pytest, Markdown, JSON, existing CLI scripts

---

### Task 1: Add failing evidence contract test

**Files:**
- Create: `tests/ops/test_dry_run_evidence_contract.py`

Run: `py -m pytest tests/ops/test_dry_run_evidence_contract.py -q`

Expected: FAIL because `docs/plans/dry-run-evidence.md` and the evidence artifacts do not exist yet.

### Task 2: Generate dry-run evidence artifacts

**Files:**
- Create: `docs/plans/dry-run-evidence/bybit-btc.json`
- Create: `docs/plans/dry-run-evidence/binance-btc.json`
- Create: `docs/plans/dry-run-evidence/okx-btc.json`
- Create: `docs/plans/dry-run-evidence/bybit-eth.json`
- Create: `docs/plans/dry-run-evidence/binance-eth.json`
- Create: `docs/plans/dry-run-evidence/okx-eth.json`
- Modify: `src/perp_platform/config.py`
- Modify: `tests/perp_platform/test_config.py`

Run the existing CLI scripts to generate normalized audit / injector evidence and keep the outputs in the repo. If preflight shows that `deploy/dry-run.env` cannot start because `dry-run` is rejected as an environment value, make the minimal direct-support fix and cover it with a failing test first.

### Task 3: Write the evidence document

**Files:**
- Create: `docs/plans/dry-run-evidence.md`

Document:
- repository-scoped disclaimer
- preflight inputs
- BTC / ETH rehearsal matrix across `BYBIT` / `BINANCE` / `OKX`
- observed degradation / recovery outcomes from checker / supervisor logic
- links to the JSON evidence artifacts

### Task 4: Verify and commit

**Files:**
- Modify: `docs/plans/2026-03-21-issue-65-dry-run-evidence-design.md`
- Modify: `docs/plans/2026-03-21-issue-65-dry-run-evidence.md`
- Test: `tests/ops/test_dry_run_evidence_contract.py`

Run:
- `py -m pytest tests/ops/test_dry_run_evidence_contract.py -q`
- `py scripts/update_project_memory.py`
- `py -m pytest tests -q`

Expected: PASS
