# Public Stream Recovery

## Trigger

- Public order book stream silent beyond threshold
- Sequence gap detected
- Checksum mismatch detected

## Automatic Response

- Set symbol tradeability to `DEGRADED` or `RESYNCING`
- Block new opens for the affected symbol
- Trigger recovery run

## Manual Actions

1. Confirm affected venue, symbol, and timestamps
2. Inspect latest recovery run and step failures
3. If repeated failures continue, set symbol or venue to `REDUCE_ONLY`
4. Escalate to `BLOCKED` if state remains unexplained

## Escalation

- Three consecutive failed recoveries
- Divergence persists after successful reconnect
