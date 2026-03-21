# AUDIT LOG

## Purpose

定义 Phase 4 的最小审计事件模型，用于统一记录操作员动作、恢复流程和 `Supervisor` 状态变更。

审计日志是 append-only trail，不是新的 truth source。

## Common Fields

所有审计事件至少包含：

- `event_id`
- `event_type`
- `occurred_at`
- `source_component`
- `scope`
- `correlation_id`
- `recorded_by`

## Operator Action Event

用于记录人工操作员显式触发的控制动作。

典型触发点：

- `force_reduce_only`
- `force_block`
- `force_resume`

最小补充字段：

- `action_type`
- `requested_by`
- `reason`

## Recovery Event

用于记录恢复流程的开始、阶段推进、完成和阻断。

典型触发点：

- recovery started
- reconciliation passed
- reconciliation blocked
- recovery completed

最小补充字段：

- `run_id`
- `phase`
- `status`
- `trigger_reason`

## Supervisor State Change Event

用于记录 `Supervisor` 状态变更及其来源。

典型触发点：

- `LIVE -> DEGRADED`
- `DEGRADED -> RESYNCING`
- `REDUCE_ONLY -> BLOCKED`
- manual override accepted

最小补充字段：

- `previous_state`
- `next_state`
- `trigger_source`

## Event Sources

- `Supervisor`
- control-plane operator actions
- recovery orchestration
- checker projection inputs

## Truth Boundary

- 审计事件只保留留痕和关联上下文
- 审计事件不替代 `Supervisor`、runtime 或 store 的主真相
- `correlation_id` 用于把 operator action、recovery run 和 incident closeout 串在同一链路上

## Persistence Boundary

- operator action、recovery 和 supervisor state change 事件进入 append-only PostgreSQL audit store
- `audit_events` 只保存结构化审计事件，不承载订单、仓位、余额或 tradeability 真相
- incident narratives remain outside PostgreSQL
- dry-run evidence、人工 closeout 和外部 incident write-up 继续保留在 runbook 或外部证据层

## Query Boundary

- control plane 只暴露 read-only audit query surface
- 查询语义围绕 `event_id`、`event_type`、`correlation_id` 和时间窗口组织
- 审计写入不通过 control-plane 查询接口进行
- 当前最小查询接口为：
  - `GET /control-plane/v1/audit/events`
  - `GET /control-plane/v1/audit/events/{event_id}`
- 当前最小过滤条件为：
  - `correlation_id`
  - `occurred_after`
  - `occurred_before`
- shared audit query 默认返回 redacted 视图：
  - `recorded_by` 不暴露原始操作者标识
  - `scope` 只保留最小 allowlist 上下文
- 时间窗口过滤使用合法 RFC3339 时间戳，不接受未校验的自由字符串

## Retention Policy

- structured audit events retain for at least 365 days
- redacted incident closeout artifacts may outlive raw event windows when needed for governance evidence
- raw sensitive attachments remain outside the repository and follow stricter private retention controls

## Redaction Rules

- redact account identifiers in shared audit views
- redact credentials and tokens in every export path
- redact venue-private operational details before moving evidence into public or wide-read contexts

## Access Boundary

- named operators may read full-fidelity evidence for active recovery and override decisions
- developers receive redacted audit views by default
- public artifacts only carry redacted summaries and references, never raw operator evidence
