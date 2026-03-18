# ADR 0003: Supervisor Owns Tradeability

## Context

Venue runtimes can expose connectivity and execution state, but tradeability decisions must be centralized across exchanges and data sources.

## Decision

Use a custom `Supervisor` as the tradeability truth source.

## Consequences

- Trading decisions are decoupled from venue-specific runtime readiness
- Cross-venue downgrade logic becomes consistent
- Extra control-plane code is required in phase 1
