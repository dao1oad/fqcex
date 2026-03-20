# STATE_MACHINE

## Supervisor 状态

- `LIVE`
- `DEGRADED`
- `RESYNCING`
- `REDUCE_ONLY`
- `BLOCKED`

状态严格度（由低到高）：

`LIVE < DEGRADED < RESYNCING < REDUCE_ONLY < BLOCKED`

## 触发输入（Triggers）

`SupervisorTriggerInputs` 包含：

- `public_stream_lag_seconds`
- `private_stream_lag_seconds`
- `reconciliation_failed`
- `repeated_recovery_failure`

阈值：

- `PUBLIC_DEGRADED_LAG_SECONDS = 1.5`
- `PUBLIC_RESYNC_LAG_SECONDS = 3.0`
- `PRIVATE_REDUCE_ONLY_LAG_SECONDS = 10.0`

## 触发优先级与结果

按以下固定优先级评估（命中即返回，不继续往下）：

1. `reconciliation_failed=True` -> `BLOCKED`（`reconciliation_failed`）
2. `repeated_recovery_failure=True` -> `BLOCKED`（`repeated_recovery_failure`）
3. `private_stream_lag_seconds >= 10.0` -> `REDUCE_ONLY`（`private_stream_lagging`）
4. `public_stream_lag_seconds >= 3.0`
   - 当前是 `REDUCE_ONLY` 或 `BLOCKED`：保持原状态（`current_state_stricter_than_resyncing`）
   - 其他状态：-> `RESYNCING`（`public_stream_resync_required`）
5. `public_stream_lag_seconds >= 1.5`
   - 当前是 `RESYNCING` / `REDUCE_ONLY` / `BLOCKED`：保持原状态（`current_state_stricter_than_degraded`）
   - 其他状态：-> `DEGRADED`（`public_stream_degraded`）
6. 无异常阈值命中：
   - 当前是 `REDUCE_ONLY`：保持 `REDUCE_ONLY`（`cooldown_or_manual_clear_required`）
   - 当前是 `BLOCKED`：保持 `BLOCKED`（`manual_unblock_required`）
   - 其他状态：-> `LIVE`（`healthy_streams`）

## 状态机允许迁移

`transition_supervisor_state` 的合法迁移：

- `LIVE -> {DEGRADED, RESYNCING, REDUCE_ONLY, BLOCKED}`
- `DEGRADED -> {LIVE, RESYNCING, REDUCE_ONLY, BLOCKED}`
- `RESYNCING -> {LIVE, REDUCE_ONLY, BLOCKED}`
- `REDUCE_ONLY -> {LIVE, BLOCKED}`
- `BLOCKED -> {REDUCE_ONLY}`

补充规则：

- 同态迁移（例如 `RESYNCING -> RESYNCING`）允许，记为 no-op（`changed=False`）。
- `BLOCKED` 不能直接返回 `LIVE`；必须先到 `REDUCE_ONLY`。

## 交易可用性投影（Projection）

### Venue 投影

`project_venue_tradeability(venue, state, reason)`：

- `LIVE` / `DEGRADED` -> `allow_open=True`, `allow_reduce=True`
- `RESYNCING` / `REDUCE_ONLY` -> `allow_open=False`, `allow_reduce=True`
- `BLOCKED` -> `allow_open=False`, `allow_reduce=False`

### Instrument 投影

`project_instrument_tradeability(venue_projection, instrument_id, instrument_state=None, reason=None)`：

- 若未给 `instrument_state`，instrument 继承 venue 状态与原因。
- 若给了 `instrument_state`，生效状态取 `max(venue_state, instrument_state)`（按严格度比较）。
- instrument 不能放宽 venue 限制；只能保持或更严格。

## 与恢复流程的关系

状态机只定义“判定与权限收敛”契约，不替代完整恢复编排。恢复链路（重连、重鉴权、重订阅、快照、对账、观察窗口）完成后，仍需通过触发输入回到健康条件，才可回归 `LIVE`。
