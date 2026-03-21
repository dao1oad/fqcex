# Audit Checklist

## Manual Unblock Pre-Check

- 确认 `force_resume` 前提全部满足
- 确认最近恢复上下文、对账结果和 `Audit Event IDs` 已记录
- 确认没有未解释的订单、仓位或余额差异

## Event Replay

- 按 `correlation_id` 回放 operator action、recovery 和 supervisor state change 事件
- 核对时间顺序与 runbook 记录一致
- 标记缺失事件或来源不明事件

## Evidence Retention

- 保存 redacted incident closeout 和所需审计引用
- 确认结构化事件仍位于 append-only audit store
- 确认敏感附件留在私有上下文，不进入公开仓库

## Audit Reconciliation

- 核对 incident 模板中的 `Audit Event IDs`
- 核对恢复动作与最终 `Supervisor` 状态一致
- 在 closeout 前完成审计留痕复核
