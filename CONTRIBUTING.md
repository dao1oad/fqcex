# CONTRIBUTING

## Scope

This repository is currently focused on a connection-management platform for:

- `Bybit`
- `Binance`
- `OKX`
- `USDT` linear perpetuals only

If a contribution expands beyond this scope, open an ADR or scope proposal first.

## Before Opening a PR

1. Read:
   - `README.md`
   - `AGENTS.md`
   - `GOVERNANCE.md`
   - relevant `ADR` and `runbook` docs
2. Confirm whether the change affects:
   - architecture
   - tradeability
   - recovery
   - risk
   - public operating procedures
3. Update docs together with code

## Branch Naming

Use one of:

- `feat/<topic>`
- `fix/<topic>`
- `docs/<topic>`
- `ops/<topic>`
- `adr/<topic>`

## Pull Request Requirements

PRs should state:

- what changed
- why it changed
- what risks it introduces
- how it was verified
- which docs were updated

For safety-critical changes, include:

- affected venues
- affected instruments
- recovery impact
- runbook impact

## Review Requirements

Every `type/task` PR must include `Review Evidence` before merge.

`Review Evidence` must include:

- child issue reference
- `Base SHA`
- `Head SHA`
- reviewed scope
- review method
- findings
- findings resolution
- final verification commands and results

In the current single-account phase, review evidence is only valid when both exist:

- the `Review Evidence` section in the PR body
- one additional independent review comment on the PR

No PR should merge without review evidence.
No child issue should close without review evidence linked from the merged PR.

Current required check names are:

- `governance-check`
- `python-check`

`python-check` is reserved for the minimal Python CI guardrail and does not cover Docker, smoke, or deploy verification.

## Issue Hierarchy

This repository uses a three-level backlog:

- `type/epic`
- `type/tracking`
- `type/task`

Rules:

- only `type/task` issues are valid direct implementation units
- do not start coding directly from an epic or tracking issue
- one PR should usually close one `type/task` issue
- if implementation scope expands, open a new sibling `type/task` issue rather than silently broadening the current one
- issue 标题、正文、进展更新、关闭说明默认使用简体中文；仅文件路径、命令、标签名和必要技术术语保留英文

Reference:

- `docs/roadmap/ISSUE_HIERARCHY.md`

## Documentation Expectations

Update the matching docs when applicable:

- `docs/adr`
- `docs/architecture`
- `docs/runbooks`
- `docs/roadmap`
- `docs/decisions`

## What Not To Submit

- scope expansion without design review
- undocumented runtime safety changes
- secrets, credentials, or production-sensitive logs
- code that claims recovery is fixed without verification evidence
- a PR that references only an epic or tracking issue without a child implementation issue
