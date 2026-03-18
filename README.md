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
- Governance: [GOVERNANCE.md](GOVERNANCE.md)
- Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)
- Security: [SECURITY.md](SECURITY.md)

## Memory System

新会话建议按下面顺序恢复上下文：

1. 先读 `docs/memory/PROJECT_STATE.md`
2. 再读 `docs/memory/ACTIVE_WORK.md`
3. 然后运行 `py scripts/update_project_memory.py`
4. 如需终端快速概览，运行 `powershell -ExecutionPolicy Bypass -File scripts/project_context.ps1`
