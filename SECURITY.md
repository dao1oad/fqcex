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

## Public Issue Guidance

If the issue is not sensitive, you may open a public bug or ops issue.

If it is sensitive:

- redact venue account details
- redact credentials
- redact precise operational data that could expose live trading posture
