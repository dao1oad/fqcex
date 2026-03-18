# Force Resume Policy

## When Force Resume Is Allowed

- Recovery completed successfully
- Reconciliation passed
- No active critical diffs
- Operator has reviewed the latest incident context

## When Force Resume Is Not Allowed

- Venue is still `BLOCKED` for unknown order state
- Position truth remains unresolved
- Balance truth remains unresolved
- Recent repeated recovery failures suggest instability

## Requirements

- Operator name
- Reason for override
- Timestamp
- Target venue or instrument
- Audit trail entry
