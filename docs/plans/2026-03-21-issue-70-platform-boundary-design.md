# Issue 70 Platform Boundary Design

## Goal

发布 Phase 4 平台化的切分边界与迁移计划，让后续控制平面和审计设计有统一的架构落点。

## Scope

- 修改 `docs/architecture/ARCHITECTURE.md`
- 修改 `docs/roadmap/ROADMAP.md`
- 新增一个 governance contract test

## Recommendation

把 `#70` 收口为：

- 在架构文档中明确 runtime、Supervisor、Control Plane、Audit 的平台化边界
- 在 roadmap 中明确 Phase 4 的迁移顺序和退出条件

不在本 issue 提前引入 ADR、服务拆分实现或真实控制平面部署拓扑。
