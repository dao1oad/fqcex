# Issue #91 Codex Cloud Linux Setup Design

## Context

Issue `#91` only covers repository setup and verification entry points for Linux/Bash and Codex cloud style execution. The current repository still documents Windows-first commands such as `py ...` and `powershell -ExecutionPolicy Bypass -File scripts/project_context.ps1` in the main onboarding paths. That leaves the package install and verification flow under-specified for Linux/Bash environments even though CI already uses `python -m ...` commands.

## Constraints

- Stay within `README.md`, `AGENTS.md`, `scripts/`, `docs/runbooks/`, and `tests/governance/`
- Do not change runtime or exchange business logic
- Do not define cloud environment secrets, network, or orchestrator cloud state behavior
- Keep existing local Windows workflows available, but stop presenting them as the default cloud-compatible path

## Approaches Considered

### Option A: Documentation-only cleanup

Only rewrite `README.md` and `AGENTS.md` to mention `python -m ...`.

- Pros: smallest change
- Cons: still leaves no executable Bash setup entry point to reuse in Codex cloud or Linux shells

### Option B: Minimal Bash setup entry point plus doc alignment

Add a dedicated Bash setup script, document Linux/Bash verification commands in onboarding docs, and freeze those expectations with a governance contract test.

- Pros: provides one concrete cloud-friendly entry point without expanding scope
- Pros: keeps local Windows paths available as optional, local-only steps
- Pros: aligns docs with existing CI command style
- Cons: does not yet model secrets/network/cloud environment details

### Option C: Full Codex cloud bootstrap bundle

Add setup script, verification script, environment examples, secret conventions, and orchestrator cloud behavior.

- Pros: more complete
- Cons: crosses directly into sibling issues `#92` to `#94`

## Recommendation

Use **Option B**.

The smallest closed loop for `#91` is:

1. Add `scripts/codex_cloud_setup.sh`
2. Update `README.md` and `AGENTS.md` to make `python -m ...` the documented cloud/Linux setup and verification path
3. Add a runbook page documenting Linux/Bash setup and verification usage
4. Add a governance test that freezes those entry points and the Windows-only framing for PowerShell

## Design

### Setup entry point

Create `scripts/codex_cloud_setup.sh` with:

- `#!/usr/bin/env bash`
- `set -euo pipefail`
- `python -m pip install --upgrade pip`
- `python -m pip install -e .`

This script becomes the canonical repository setup entry point for Codex cloud and Linux/Bash environments.

### Verification contract

Document `python -m pytest tests -q` as the default verification command for Linux/Bash and Codex cloud compatible execution.

### Documentation changes

- `README.md`
  - add a Linux/Bash and Codex cloud setup section
  - switch memory/bootstrap examples away from `py` for the default path
  - keep `scripts/project_context.ps1` as an optional Windows local convenience only
- `AGENTS.md`
  - update the memory recovery section so the required command is `python scripts/update_project_memory.py`
  - mark the PowerShell script as optional and Windows-only
- `docs/runbooks/codex-cloud-setup.md`
  - describe the intended setup and verification steps for cloud/Linux environments

### Governance test

Add `tests/governance/test_codex_cloud_setup_contract.py` to assert:

- `scripts/codex_cloud_setup.sh` exists
- it contains `python -m pip install -e .`
- `README.md` documents Codex cloud or Linux/Bash setup and `python -m pytest tests -q`
- `AGENTS.md` uses `python scripts/update_project_memory.py`
- `AGENTS.md` explicitly frames `scripts/project_context.ps1` as optional and Windows-only

## Verification

- `python -m pytest tests/governance/test_codex_cloud_setup_contract.py -q`
- `python -m pytest tests/governance -q`
- `python -m pytest tests -q`

## Out of Scope

- cloud secrets or environment variables
- network access policy
- orchestrator state persistence changes
- actual Codex cloud environment configuration
