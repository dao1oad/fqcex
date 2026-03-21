# CONTROL PLANE API

## Purpose

为 Phase 4 平台化定义一个最小、只读优先的外部控制平面 API 表面。

该表面用于：

- 对外暴露 `Supervisor`、store 和 audit 的投影视图
- 给后续操作员界面、审计查询和运维集成提供稳定挂点
- 为 `#68`、`#69`、`#70` 固定资源边界

## Non-Goals

本设计当前不负责：

- 实现 HTTP server、handler 或 transport
- 定义完整认证与授权机制
- 引入新的 truth source
- 定义完整持久化 schema
- 实现真实 operator action 执行链路

## Design Principles

- 控制平面是 projection layer，不是新的业务真相源
- `Supervisor` 仍然是交易可用性的唯一真相源
- 订单、仓位、余额真相仍来自 runtime/store 主链路
- audit 只保留留痕与查询语义，不反向改写主状态
- 资源命名优先围绕 venue、instrument、recovery、checker、operator action

## Resource Groups

### Venue Tradeability

面向 venue 级别的可交易性投影。

最小资源面：

- `GET /control-plane/v1/venues`
- `GET /control-plane/v1/venues/{venue}`

#### Venue Tradeability Read Model

该读模型来自 `Supervisor` 投影和 `tradeability_states`，是 projection, not a new truth source。

最小字段：

- `venue`
- `supervisor_state`
- `allow_open`
- `allow_reduce`

### Instrument Tradeability

面向统一 `instrument_id` 的交易对级可交易性投影。

最小资源面：

- `GET /control-plane/v1/instruments`
- `GET /control-plane/v1/instruments/{instrument_id}`

#### Instrument Tradeability Read Model

该读模型来自 `Supervisor` 投影和 `tradeability_states`，是 projection, not a new truth source。

最小字段：

- `instrument_id`
- `venue`
- `supervisor_state`
- `allow_open`
- `allow_reduce`

### Recovery Runs

面向恢复流程与对账阶段的只读投影。

最小资源面：

- `GET /control-plane/v1/recovery/runs`
- `GET /control-plane/v1/recovery/runs/{run_id}`

#### Recovery Run Read Model

该读模型来自 `recovery_runs`，是 projection, not a new truth source。

最小字段：

- `run_id`
- `phase`
- `status`
- `trigger_reason`
- `blockers_json`

### Checker Signals

面向 checker 判断与投影输入的只读资源。

最小资源面：

- `GET /control-plane/v1/checker/signals`
- `GET /control-plane/v1/checker/signals/{signal_id}`

具体 read model 字段与投影细节延后到 `#69`。

### Audit Events

面向审计留痕的 read-only audit query surface。

最小资源面：

- `GET /control-plane/v1/audit/events`
- `GET /control-plane/v1/audit/events/{event_id}`

该查询面只消费 `audit_events` 和相关 `correlation_id` 关联上下文，不提供审计写入入口。

### Operator Actions

动作入口定义最小动作模型与权限边界，但不实现 transport、auth middleware 或完整 RBAC。

最小动作名：

- `POST /control-plane/v1/operator-actions/force_reduce_only`
- `POST /control-plane/v1/operator-actions/force_block`
- `POST /control-plane/v1/operator-actions/force_resume`

最小动作请求字段：

- `action_type`
- `target_scope`
- `requested_by`
- `reason`
- `requested_at`

### Action Permission Boundary

- `GET` 资源默认面向 read-only clients
- 写动作只允许 named human operator 发起
- automation、Codex cloud task 和只读 token 不得调用 operator write actions
- `force_reduce_only` 只能收紧可交易性，不能恢复交易
- `force_block` 只能提升到更严格的人工阻断态，不能直接恢复交易
- `force_resume` 只能在恢复和对账前提满足后请求执行
- `force_resume` cannot bypass unresolved recovery or reconciliation prerequisites

动作 payload 的扩展字段、审批链和审计事件联动细节延后到 `#85`。

## Response Envelope

所有资源和动作响应统一使用 envelope：

```json
{
  "data": {},
  "meta": {
    "request_id": "string",
    "generated_at": "2026-03-21T00:00:00Z"
  },
  "errors": []
}
```

约束：

- 成功响应以 `data` 为主
- `meta.request_id` 用于审计和诊断链路
- `errors` 在成功时为空数组

## Error Envelope

失败响应仍保持统一 envelope 结构：

```json
{
  "data": null,
  "meta": {
    "request_id": "string",
    "generated_at": "2026-03-21T00:00:00Z"
  },
  "errors": [
    {
      "code": "conflict",
      "message": "control plane request conflicts with current supervisor state"
    }
  ]
}
```

最小错误语义：

- `invalid_request`
- `not_found`
- `conflict`
- `upstream_unavailable`

## Truth Boundary

控制平面不是新的 truth source。

- `Supervisor` 决定 tradeability
- runtime/store 决定订单、仓位、余额真相
- checker 信号只作为 projection input
- audit 记录 operator/recovery 留痕，但不反向声明系统真相

## Follow-On Issues

- `#70` 发布平台化切分边界与迁移计划
- `#85` 定义操作员动作与恢复事件模型
