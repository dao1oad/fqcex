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
