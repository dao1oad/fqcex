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
- `force_resume` request body must include explicit recovery / reconciliation preconditions

## Permission Boundary

- `force_resume` 只允许 named human operator 发起
- Codex cloud、自动化任务和只读客户端不得持有 `force_resume` 写权限
- 发起前必须复核 latest recovery context
- 发起前必须确认恢复完成、对账通过且没有未解释差异
- 如果任一前提不满足，保持 `REDUCE_ONLY` 或 `BLOCKED`
- control-plane `force_resume` handler 必须在请求入口返回 `409 conflict`，而不是静默接受不满足前提的请求

## Evidence Hygiene

- redact account identifiers in any shared operator evidence
- redact credentials and tokens before attaching artifacts to incidents or reviews
- keep full-fidelity operator evidence inside the private operator context

## Audit Checklist

- 执行前后按 `docs/runbooks/audit-checklist.md` 完成审计核对
