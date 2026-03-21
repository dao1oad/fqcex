# Issue 68 Operator Actions Design

## Goal

为 Phase 4 控制平面定义最小的操作员动作模型与权限边界，只处理人工动作的类型、约束和安全边界，不实现控制平面服务。

## Scope

- 修改 `docs/architecture/control-plane-api.md`
- 修改 `docs/runbooks/force-resume-policy.md`
- 修改 `SECURITY.md`
- 新增一个 governance contract test

## Recommendation

把 `#68` 收口为三件事：

- 定义动作类型和最小请求字段
- 定义只读资源与人工写动作之间的权限边界
- 定义 `force_resume` 的最小审批前提和 cloud/secrets 安全约束

不在本 issue 提前定义完整 RBAC、审计存储 schema 或读模型字段。
