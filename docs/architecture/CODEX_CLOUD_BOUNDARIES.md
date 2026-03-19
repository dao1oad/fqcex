# CODEX_CLOUD_BOUNDARIES

## Objective

Freeze the repository-level Codex cloud execution boundary without changing Phase 1 trading scope, runtime truth ownership, or orchestrator behavior.

## Two-Phase Runtime

Codex cloud for this repository follows a **two-phase runtime**:

- `setup script`
  - runs first in a separate bootstrap session
  - may install dependencies or fetch read-only bootstrap artifacts
  - may consume setup-only bootstrap secrets
- `agent phase`
  - starts after setup completes
  - receives the repository checkout plus non-secret environment values
  - does not receive setup-only secrets

## Environment and Secret Boundary

- Non-secret environment values may persist across the full task.
- Setup-only secrets are removed before the `agent phase` starts.
- Live venue, production, deploy, operator, and infrastructure credentials remain prohibited from Codex cloud configuration.

## Network Boundary

- Codex cloud `agent phase` 默认关闭网络访问。
- If network access must be enabled for the `agent phase`, use a narrow allowlist with trusted resources only.
- Keep allowed HTTP methods restricted to `GET`, `HEAD`, and `OPTIONS`.
- Live exchange REST/WebSocket access is out of bounds.
- Production control-plane APIs, deploy targets, secrets managers, bastions, and arbitrary untrusted URLs are out of bounds.

## Allowed Cloud Work

Codex cloud is allowed for documentation, tests, static checks, and mock configuration only.

## Local or Manual-Only Work

Live trading, deploys, and real-account reconciliation remain local or manual-only.

The following work must stay outside Codex cloud:

- real exchange connectivity checks
- private-stream validation against live accounts
- production or production-like deployment workflows
- tasks requiring VPN, SSH, bastion, or privileged internal network access

## Phase 1 Alignment

- Phase 1 exchange and product boundaries remain unchanged.
- Supervisor remains the only tradeability truth source.
- Codex cloud policy does not authorize real venue interaction, real credential handling, or changes to recovery safety rules.
