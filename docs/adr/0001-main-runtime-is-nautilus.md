# ADR 0001: Main Runtime Is NautilusTrader

## Context

Phase 1 needs a production-shaped venue runtime with execution, reconciliation, portfolio, and risk capabilities.

## Decision

Use `NautilusTrader` as the main runtime for phase 1.

## Consequences

- Faster path to a working trading and recovery loop
- Less phase 1 protocol work
- Runtime coupling remains acceptable for phase 1
- Native adapter replacement is deferred to later phases
