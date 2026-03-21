# Issue 147 Operator Actions 设计

## 背景

`#145` 和 `#146` 已经交付了最小 control-plane skeleton 和 read-only query surface。`#147` 需要在此基础上增加最小 operator action 写接口，为后续 live gate、operator UI 和 canary 提供受控动作入口。

## 方案比较

### 方案 A：直接实现完整 auth / RBAC / 审批链

缺点：

- 明显超出 `#147`

### 方案 B：最小 action contract + 前提校验 + 审计写入挂点，推荐

优点：

- 严格贴合 issue 边界
- 能为后续 live safety gate 和 UI 留出稳定写入口

### 方案 C：只实现文档，不实现代码

不推荐：

- 不满足 issue 目标

## 推荐方案

采用方案 B。

## 设计

新增 `actions.py`，定义：

- `OperatorActionRequest`
- `OperatorActionResult`
- `ForceResumePreconditions`
- `OperatorActionAuditHook` protocol
- `InMemoryOperatorActionAuditHook`

扩展 `app.py`：

- 支持：
  - `POST /control-plane/v1/operator-actions/force_reduce_only`
  - `POST /control-plane/v1/operator-actions/force_block`
  - `POST /control-plane/v1/operator-actions/force_resume`
- 解析 JSON request body
- 校验最小公共字段：
  - `action_type`
  - `target_scope`
  - `requested_by`
  - `reason`
  - `requested_at`

额外校验：

- path 上的动作名必须与 payload `action_type` 一致
- `force_resume` 必须同时满足：
  - `recovery_completed = true`
  - `reconciliation_passed = true`
  - `has_critical_diffs = false`

审计挂点：

- 请求通过时，调用 audit hook 生成最小 `audit_event_id`

## 非目标

- 不实现完整 auth middleware
- 不实现复杂审批链
- 不直接修改 `Supervisor` 真相
- 不实现前端

## 测试策略

先写失败测试：

1. `force_reduce_only` 成功
2. `force_block` 成功
3. `force_resume` 前提不满足时返回 `409 conflict`
4. `force_resume` 前提满足时成功
5. `action_type` 与 path 不一致时返回 `invalid_request`

## 文档更新

同步更新：

- `README.md`
- `docs/runbooks/force-resume-policy.md`
