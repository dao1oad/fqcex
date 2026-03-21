# Live Canary Approval Runbook

## 目标

定义进入 live canary 前的最小人工放行规则。

## 硬前提

以下任一条件不满足时，不得进入 live canary：

- operator approval 缺失
- `venue` 不在 allowlist
- `instrument_id` 不在 allowlist
- `requested_notional_usd` 超过批准上限
- kill switch 处于 `armed=true`

## Kill Switch 语义

`LIVE_CANARY_KILL_SWITCH_PATH` 指向的文件使用最小键值格式：

```text
armed=false
```

如果文件不存在，或文件中显式写成：

```text
armed=true
```

则必须阻断 live canary。

## 最小 approval 记录

operator approval 至少包含：

- `approved_by`
- `approved_at`
- `reason`

## 审计联动

放行成功后，必须写一条 `approve_live_canary` 审计记录，并返回 `audit_event_id`。

没有审计记录的“口头放行”视为无效。

## 当前边界

本 runbook 只定义第 5 阶段的最小 live canary 放行规则，不等价于完整权限系统或 RBAC。
