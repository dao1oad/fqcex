# Issue 87 Audit Security Design

## Goal

定义审计数据的保留、脱敏与访问控制约束，保证后续控制平面和 runbook 使用同一条安全边界。

## Scope

- 修改 `SECURITY.md`
- 修改 `docs/architecture/AUDIT_LOG.md`
- 修改 `docs/runbooks/force-resume-policy.md`
- 新增一个 governance contract test

## Recommendation

把 `#87` 收口为：

- 结构化审计事件的最小保留周期
- 审计与 runbook 工件的脱敏规则
- named operator / developer / public artifact 三层访问边界

不实现 IAM、租户隔离或外部 SIEM 接入。
