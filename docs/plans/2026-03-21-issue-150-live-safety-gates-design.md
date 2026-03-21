# Issue 150 Live Safety Gates 设计

## 背景

`#149` 已定义 production-like env、host preflight 和 live canary deploy runbook。`#150` 负责把真正的放行条件收口成可测试的运行时安全闸门，避免 operator、UI 或后续 canary 逻辑直接绕开约束。

## 方案比较

### 方案 A：独立 `live_safety` gate 模块 + kill switch reader + approval audit hook，推荐

优点：

- 与 `#149` 的 env 契约直接对齐
- 后续 `#151/#152/#153-#155` 都能复用
- 不把 UI、HTTP 或真实 canary 逻辑提前混进来

### 方案 B：把 gate 直接塞进 preflight 脚本

不推荐：

- preflight 是部署前静态检查，不是运行时放行裁决
- 会把“主机准备”与“operator 放行”混成一个阶段

### 方案 C：把 gate 直接写进 future operator UI / endpoint

不推荐：

- 当前 UI 还没开始
- 核心安全约束不应被页面实现反向定义

## 推荐方案

采用方案 A。

## 设计

新增一个最小 gate 模块：

- `src/perp_platform/control_plane/live_safety.py`

核心对象：

- `LiveSafetyGateConfig`
- `LiveCanaryApproval`
- `LiveCanaryRequest`
- `LiveCanaryDecision`
- `FileBackedKillSwitch`
- `LiveSafetyGate`

最小 gate 规则：

1. `requested_notional_usd` 不能超过 `LIVE_CANARY_MAX_NOTIONAL_USD`
2. `venue` 必须在 `LIVE_CANARY_ALLOWED_VENUES`
3. `instrument_id` 必须在 `LIVE_CANARY_ALLOWED_INSTRUMENTS`
4. kill switch 处于 `armed=true` 时不得放行
5. 没有 operator approval 不得放行
6. 放行成功时必须写一条审计记录

审计联动：

- 复用现有 `OperatorActionAuditHook`
- 成功放行时记录一个 `approve_live_canary` action
- 返回 `audit_event_id`

第一版不做：

- 多级审批
- RBAC / auth
- 数据库存储
- HTTP endpoint

## 测试策略

先写失败测试：

1. 缺少 approval -> reject
2. 超过 max notional -> reject
3. 非 allowlist venue / instrument -> reject
4. kill switch armed -> reject
5. 合法 request -> allow，并返回 `audit_event_id`

## 文档更新

同步更新：

- `docs/runbooks/live-canary-deploy.md`
- 新增 `docs/runbooks/live-canary-approval.md`
- `README.md`
