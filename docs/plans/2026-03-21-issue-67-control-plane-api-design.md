# Issue 67 Control Plane API Surface Design

## Goal

为 Phase 4 平台化定义一个最小、只读优先的外部控制平面 API 表面，让后续 `#68/#69/#70` 能在固定边界内继续细化，而不提前落实现代码。

## Options

### Option A: 直接定义完整 HTTP API 与认证/权限细节

不推荐。当前 issue 只要求“定义外部 API 表面”，而认证、权限、动作模型、读模型边界分别属于 `#68/#69` 和后续实现阶段。

### Option B: 只写高层叙述，不给资源面

不推荐。这样无法为后续 Phase 4 设计提供稳定的 URL/resource 边界，也不利于前端或控制平面消费方对齐。

### Option C: 只定义资源面、响应形状和错误语义（推荐）

- 新建 `docs/architecture/control-plane-api.md`
- 在 `docs/architecture/ARCHITECTURE.md` 中补 `Control Plane` 组件与 truth boundary 说明
- 定义只读资源族：
  - venue tradeability
  - instrument tradeability
  - recovery runs
  - checker signals
- 定义动作入口族但不细化权限：
  - `force_reduce_only`
  - `force_block`
  - `force_resume`
- 定义统一响应 envelope 和错误字段

## Recommendation

采用 Option C。它能给 `#68/#69` 一个稳定挂点，同时保持“control plane 不是新的 truth source”这个核心边界不被破坏。

## Scope

- Create: `docs/architecture/control-plane-api.md`
- Modify: `docs/architecture/ARCHITECTURE.md`
- Create: `tests/governance/test_control_plane_api_contract.py`

## Out of Scope

- 不实现 server、handler、auth middleware
- 不引入新的数据库 schema
- 不定义完整 operator permission matrix
- 不定义完整 read model 字段列表
