# STATE_MACHINE

## Supervisor States

- `LIVE`
- `DEGRADED`
- `RESYNCING`
- `REDUCE_ONLY`
- `BLOCKED`

## Stream Types

- `public_book`
- `private_user`
- `execution_rest`

## Trigger Rules

- Public stream stale:
  - `DEGRADED` after 1.5s
  - `RESYNCING` after 3s
- Private stream stale:
  - `REDUCE_ONLY` after 10s
- Reconciliation failure:
  - `BLOCKED`
- Repeated recovery failure:
  - `BLOCKED`

## Recovery Sequence

1. reconnect
2. re-authenticate
3. re-subscribe
4. fetch snapshot
5. query open orders
6. query positions
7. query balances
8. reconcile
9. cooldown observe

## Return to LIVE

Only after:

- connectivity restored
- subscriptions restored
- reconciliation passed
- no new anomalies within cooldown window
