# Private Stream Recovery

## Trigger

- Private user stream silent beyond threshold
- Authentication failure
- Subscription restore failure
- Reconciliation mismatch after recovery

## Automatic Response

- Set venue trade mode to `REDUCE_ONLY`
- Start recovery sequence
- Run order, position, and balance reconciliation

## Manual Actions

1. Verify whether order state is still explainable
2. Review reconciliation diffs
3. Keep venue in `REDUCE_ONLY` until diffs are resolved
4. Move to `BLOCKED` if order or position truth cannot be confirmed

## Escalation

- Unknown order state
- Critical position diff
- Critical balance diff
