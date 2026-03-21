# SECURITY

## Supported Scope

This repository is in active development. Security-sensitive reports that may expose:

- exchange credentials
- account identifiers
- live trading setup
- incident details not suitable for public disclosure

should not be filed as public GitHub issues.

## Reporting

For now, report sensitive issues privately to the repository owner instead of opening a public issue.

Suggested report content:

- summary
- affected area
- reproduction conditions
- risk assessment
- recommended mitigation

## Secrets Policy

Never commit:

- API keys
- secret keys
- account IDs tied to live venues
- private logs containing sensitive exchange or account data
- environment files containing live credentials

## Codex cloud boundary

Never place live venue credentials into Codex cloud environments.

Codex cloud environment variables may persist across the full task, so environment variables must never be used to carry 真实交易凭证.

The `setup script` may use read-only bootstrap secrets, but those secrets must stay limited to dependency installation or read-only artifact fetches and must not grant trading, deploy, operator, or infrastructure access.

The `agent phase` must not receive live credentials or privileged infrastructure access.

The following credentials remain prohibited from Codex cloud task configuration, setup scripts, and agent phase execution:

- exchange API keys
- exchange secret keys
- exchange passphrases
- account identifiers tied to live venues
- `BYBIT_API_KEY`
- production database credentials
- deploy credentials
- control-plane admin tokens
- VPN / SSH / bastion credentials

If a task requires any of the above, keep it local or behind explicit human approval instead of moving it into Codex cloud.

## Control-plane operator boundary

Control-plane write tokens must not be placed into Codex cloud environments.

Control-plane write access must stay behind human-scoped identities and explicit operator intent.

Read-only clients may consume control-plane projections, but write actions must remain separated from read-only access paths.

The following controls apply to operator actions:

- write credentials stay local to named operators
- human-scoped identities are required for operator write access
- write actions must remain auditable
- cloud automation must not receive control-plane write tokens

## Public Issue Guidance

If the issue is not sensitive, you may open a public bug or ops issue.

If it is sensitive:

- redact venue account details
- redact credentials
- redact precise operational data that could expose live trading posture
