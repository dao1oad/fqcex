# Issue 86 Audit Storage Boundary Design

## Goal

定义审计事件进入 PostgreSQL 的边界，以及控制平面对审计事件的只读查询边界。

## Scope

- 修改 `docs/architecture/AUDIT_LOG.md`
- 修改 `docs/architecture/DATA_MODEL.md`
- 修改 `docs/architecture/control-plane-api.md`
- 新增一个 governance contract test

## Recommendation

把 `#86` 收口为：

- 审计事件进入 append-only PostgreSQL audit store
- incident narrative、dry-run evidence 和外部 closeout 保持在库外证据层
- control plane 只提供 audit query surface，不提供审计写入接口
