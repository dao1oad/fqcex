# Issue 85 Audit Event Model Design

## Goal

为 Phase 4 平台化定义统一的操作员动作与恢复事件模型，让后续审计存储、保留策略和 runbook 都围绕同一组事件语义展开。

## Scope

- 创建 `docs/architecture/AUDIT_LOG.md`
- 更新 `docs/runbooks/incident-template.md`
- 新增一个 governance contract test

## Recommendation

把 `#85` 收口为三类事件：

- Operator Action Event
- Recovery Event
- Supervisor State Change Event

统一约束最小字段、事件来源和触发点，并明确 audit 只是 append-only trail，不是新的 truth source。
