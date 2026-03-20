# Dry Run Evidence

## Scope

本文件记录的是 **repository-scoped** 干跑演练证据。

- 使用仓库内现有 `deploy/dry-run.env`、audit script、injector script、checker / supervisor 逻辑
- 覆盖 `BTC-USDT-PERP`、`ETH-USDT-PERP`
- 覆盖 `BYBIT`、`BINANCE`、`OKX`
- **不是 live 或 testnet**，不宣称真实交易所连接、真实下单或真实资金路径已经验证

## Preflight

本次演练基于 `deploy/dry-run.env` 的安全闸门：

- `DRY_RUN_ENABLED=true`
- `DRY_RUN_ALLOWED_INSTRUMENTS=BTC-USDT-PERP,ETH-USDT-PERP`
- `DRY_RUN_ABORT_ON_CHECKER_DIVERGENCE=true`
- `DRY_RUN_ABORT_ON_SUPERVISOR_REDUCE_ONLY=true`
- `DRY_RUN_ABORT_ON_SUPERVISOR_BLOCKED=true`

在开始记录证据前，先验证最小 bootstrap 路径：

```powershell
$env:PYTHONPATH='src'
$env:PERP_PLATFORM_APP_NAME='perp-platform-dry-run'
$env:PERP_PLATFORM_ENVIRONMENT='dry-run'
$env:PERP_PLATFORM_LOG_LEVEL='INFO'
py -c "from perp_platform.cli import main; raise SystemExit(main([]))"
```

输出：

```text
perp-platform-dry-run bootstrap ready [dry-run]
```

## Injector Command Samples

### WebSocket Disconnect

```powershell
py scripts/inject_ws_disconnect.py --venue BYBIT --stream public --duration-seconds 15 --instrument-id BTC-USDT-PERP
```

输出：

```json
{
  "injector": "ws_disconnect",
  "venue": "BYBIT",
  "stream": "public",
  "duration_seconds": 15,
  "instrument_id": "BTC-USDT-PERP",
  "reason": "manual_fault_injection",
  "action": "disconnect_websocket"
}
```

### Private Silence

```powershell
py scripts/inject_private_silence.py --venue BINANCE --duration-seconds 30
```

输出：

```json
{
  "injector": "private_silence",
  "venue": "BINANCE",
  "scope": "account",
  "duration_seconds": 30,
  "reason": "manual_fault_injection",
  "action": "silence_private_stream"
}
```

### Reconcile Diff

```powershell
py scripts/inject_reconcile_diff.py --venue OKX --resource position --diff-kind mismatch --instrument-id ETH-USDT-PERP
```

输出：

```json
{
  "injector": "reconcile_diff",
  "venue": "OKX",
  "resource": "position",
  "diff_kind": "mismatch",
  "instrument_id": "ETH-USDT-PERP",
  "reason": "manual_fault_injection",
  "action": "inject_reconcile_diff"
}
```

## Observed Supervisor / Checker Outcomes

仓库内状态观测命令输出如下：

```text
BYBIT|BTC-USDT-PERP|checker=RESYNCING|supervisor=RESYNCING|reason=public_stream_resync_required|recovery=LIVE
BINANCE|BTC-USDT-PERP|supervisor=REDUCE_ONLY|reason=private_stream_lagging|recovery=LIVE
OKX|BTC-USDT-PERP|supervisor=BLOCKED|reason=reconciliation_failed|recovery=REDUCE_ONLY->LIVE
BYBIT|ETH-USDT-PERP|checker=RESYNCING|supervisor=RESYNCING|reason=public_stream_resync_required|recovery=LIVE
BINANCE|ETH-USDT-PERP|supervisor=REDUCE_ONLY|reason=private_stream_lagging|recovery=LIVE
OKX|ETH-USDT-PERP|supervisor=BLOCKED|reason=reconciliation_failed|recovery=REDUCE_ONLY->LIVE
```

这说明在仓库当前逻辑下，BTC / ETH 两个 instrument 都已经覆盖：

- 由 checker / public stream 问题进入 `RESYNCING`
- 由 private stream lag 进入 `REDUCE_ONLY`
- 由 reconciliation failure 进入 `BLOCKED`
- 在人工清理或健康流恢复后回到 `LIVE`

## Rehearsal Matrix

| Phase | Venue | Instrument | Fault Plan | Observed Outcome | Audit Artifact |
| --- | --- | --- | --- | --- | --- |
| BTC | BYBIT | BTC-USDT-PERP | WebSocket disconnect | `checker=RESYNCING`, `supervisor=RESYNCING`, `recovery=LIVE` | `docs/plans/dry-run-evidence/bybit-btc.json` |
| BTC | BINANCE | BTC-USDT-PERP | Private silence | `supervisor=REDUCE_ONLY`, `recovery=LIVE` | `docs/plans/dry-run-evidence/binance-btc.json` |
| BTC | OKX | BTC-USDT-PERP | Reconcile diff | `supervisor=BLOCKED`, `recovery=REDUCE_ONLY->LIVE` | `docs/plans/dry-run-evidence/okx-btc.json` |
| ETH | BYBIT | ETH-USDT-PERP | WebSocket disconnect | `checker=RESYNCING`, `supervisor=RESYNCING`, `recovery=LIVE` | `docs/plans/dry-run-evidence/bybit-eth.json` |
| ETH | BINANCE | ETH-USDT-PERP | Private silence | `supervisor=REDUCE_ONLY`, `recovery=LIVE` | `docs/plans/dry-run-evidence/binance-eth.json` |
| ETH | OKX | ETH-USDT-PERP | Reconcile diff | `supervisor=BLOCKED`, `recovery=REDUCE_ONLY->LIVE` | `docs/plans/dry-run-evidence/okx-eth.json` |

## Findings Carried Into #66

1. 当前仓库已经可以完成 repository-scoped 干跑证据采集，但它验证的是配置、安全闸门、injector plan、audit 记录和 supervisor/checker 逻辑，不是真实交易所执行链路。
2. `deploy/dry-run.env` 初始依赖的 `PERP_PLATFORM_ENVIRONMENT=dry-run` 需要应用侧接受该环境值；本 issue 已补齐该最小 direct-support 修复。
3. 后续 `#66` 应明确把本次演练结论表述为“仓库内受控演练”，避免误写成 live / testnet 演练完成。
