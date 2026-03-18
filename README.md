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
- Architecture: [docs/architecture/ARCHITECTURE.md](docs/architecture/ARCHITECTURE.md)
- State machine: [docs/architecture/STATE_MACHINE.md](docs/architecture/STATE_MACHINE.md)
- Data model: [docs/architecture/DATA_MODEL.md](docs/architecture/DATA_MODEL.md)
- Phase 1 freeze: [docs/decisions/PHASE1_FREEZE.md](docs/decisions/PHASE1_FREEZE.md)
- Governance: [GOVERNANCE.md](GOVERNANCE.md)
- Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)
- Security: [SECURITY.md](SECURITY.md)
