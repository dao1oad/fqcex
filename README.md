# fqcex

Private repository for a perpetual futures connection platform focused on multi-exchange arbitrage infrastructure.

## Scope

- Phase 1 exchanges: `Bybit`, `Binance`, `OKX`
- Phase 1 product scope: `USDT` linear perpetuals only
- Main runtime: `NautilusTrader`
- Control plane: custom `Supervisor`
- Market data checker: `Cryptofeed`

## Non-Goals for Phase 1

- Spot trading
- Coin-margined contracts
- Options
- Complex algo orders
- Hummingbot in production runtime

## Governance

- Default branch: `main`
- Single-repo model
- Architecture changes require ADRs in `docs/adr`
- Runtime and incident procedures live in `docs/runbooks`
- Phase freezes live in `docs/decisions`

## CI

- `governance-check` verifies the repository governance baseline files.
- `python-check` runs on Python `3.12`.
- `python-check` installs the package with `python -m pip install -e .`.
- `python-check` runs the full suite with `python -m pytest tests -q`.
- Docker, smoke, and deploy checks remain out of this minimal CI scope.

## Codex Cloud / Linux-Bash Setup

Use the Linux/Bash-compatible repository setup entry point:

```bash
bash scripts/codex_cloud_setup.sh
```

The canonical verification command for Codex cloud and Linux/Bash environments is:

```bash
python -m pytest tests -q
```

For manual setup without the helper script:

```bash
python -m pip install --upgrade pip
python -m pip install -e .
```

## Codex Cloud Security Boundary

Keep only non-sensitive environment variables such as `PERP_PLATFORM_ENVIRONMENT=test` in Codex cloud environment settings.

Do not place live venue credentials or 真实交易凭证 into Codex cloud environments.

Agent internet access should remain off by default.

Codex cloud work in this repository is limited to docs, tests, static checks, and mock configuration unless a later issue explicitly widens the boundary.

See:

- [docs/runbooks/codex-cloud-security.md](docs/runbooks/codex-cloud-security.md)
- [docs/architecture/CODEX_CLOUD_BOUNDARIES.md](docs/architecture/CODEX_CLOUD_BOUNDARIES.md)

## Docs

- Roadmap: [docs/roadmap/ROADMAP.md](docs/roadmap/ROADMAP.md)
- Issue hierarchy: [docs/roadmap/ISSUE_HIERARCHY.md](docs/roadmap/ISSUE_HIERARCHY.md)
- Architecture: [docs/architecture/ARCHITECTURE.md](docs/architecture/ARCHITECTURE.md)
- State machine: [docs/architecture/STATE_MACHINE.md](docs/architecture/STATE_MACHINE.md)
- Data model: [docs/architecture/DATA_MODEL.md](docs/architecture/DATA_MODEL.md)
- Phase 1 freeze: [docs/decisions/PHASE1_FREEZE.md](docs/decisions/PHASE1_FREEZE.md)
- Project state: [docs/memory/PROJECT_STATE.md](docs/memory/PROJECT_STATE.md)
- Active work: [docs/memory/ACTIVE_WORK.md](docs/memory/ACTIVE_WORK.md)
- Session handoff: [docs/memory/SESSION_HANDOFF.md](docs/memory/SESSION_HANDOFF.md)
- Codex cloud setup: [docs/runbooks/codex-cloud-setup.md](docs/runbooks/codex-cloud-setup.md)
- Codex cloud security boundaries: [docs/runbooks/codex-cloud-security.md](docs/runbooks/codex-cloud-security.md)
- Codex cloud execution boundary: [docs/architecture/CODEX_CLOUD_BOUNDARIES.md](docs/architecture/CODEX_CLOUD_BOUNDARIES.md)
- Governance: [GOVERNANCE.md](GOVERNANCE.md)
- Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)
- Security: [SECURITY.md](SECURITY.md)

## Memory System

新会话建议按下面顺序恢复上下文：

1. 先读 `docs/memory/PROJECT_STATE.md`
2. 再读 `docs/memory/ACTIVE_WORK.md`
3. 然后运行 `python scripts/update_project_memory.py`
4. 如需 Linux/Bash 下完整验证，可运行 `python -m pytest tests -q`
5. 如需终端快速概览，可选运行 `powershell -ExecutionPolicy Bypass -File scripts/project_context.ps1`（Windows-only）
