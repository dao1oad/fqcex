# ROADMAP

## Phase 0: Design Freeze

- Freeze phase 1 scope and governance
- Publish architecture, state machine, data model, ADRs, runbooks

## Phase 1: Single Venue Loop

- Run Bybit linear perpetual end-to-end
- Validate trading, recovery, reconciliation

## Phase 2: Three Venue Baseline

- Add Binance and OKX
- Unify instrument, quantity, tradeability, recovery

## Phase 3: Checker and Dry Run

- Add Cryptofeed checker
- Run failure injection and small-size dry run

## Phase 4: Platformization

- Harden supervisor
- Externalize state, audit, operator controls

### Phase 4 Delivery Order

1. control-plane api surface
2. operator actions and permissions
3. read models for tradeability and recovery
4. platform boundary and migration plan
5. audit boundary and runbooks

Phase 4 exits only after the platform boundary is documented without changing truth ownership and the audit/operator surface is fully documented.

## Phase 5: Live Readiness and Canary

- Implement the minimum control-plane backend
- Add live preflight, safety gates, operator approvals, and audit query paths
- Run small-size live canaries on `Bybit`, `Binance`, and `OKX`
- Produce live closeout, residual risk, and rollout guidance

Phase 5 exits only after all three venues have live canary evidence, operator approvals, audit trail coverage, and a formal closeout.

## Phase 6: Native Tier-1 Adapters

- Replace selected Tier-1 venue paths with native adapters

## Phase 7: Scale and HA

- Multi-account
- Long-tail venues
- High availability and operational maturity
