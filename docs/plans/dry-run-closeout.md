# Dry Run Closeout

## Closeout Scope

本结项报告只覆盖 **repository-scoped** Phase 3 干跑演练：

- 输入来自 `docs/plans/dry-run-evidence.md`
- 输入来自 `docs/plans/dry-run-evidence/*.json`
- 覆盖 `BTC-USDT-PERP`、`ETH-USDT-PERP`
- 覆盖 `BYBIT`、`BINANCE`、`OKX`
- **不把本次结论表述为真实交易所 live 或 testnet 演练完成**

## Completed Items

本阶段已经完成：

1. `deploy/dry-run.env` 的最小 dry-run 配置模板与安全闸门
2. 操作员审计采集脚本与 rollback 审计要求
3. 三类故障注入 plan：
   - WebSocket disconnect
   - private silence
   - reconcile diff
4. BTC / ETH 两个 instrument 在三家 venue 上的 repository-scoped 证据矩阵
5. checker / supervisor 的降级、恢复、`REDUCE_ONLY`、`BLOCKED` 观测
6. `PERP_PLATFORM_ENVIRONMENT=dry-run` 的 direct-support 配置修复

## Rehearsal Summary

| Venue | BTC-USDT-PERP | ETH-USDT-PERP | Covered Fault Path |
| --- | --- | --- | --- |
| BYBIT | `RESYNCING -> LIVE` | `RESYNCING -> LIVE` | public stream / checker divergence |
| BINANCE | `REDUCE_ONLY -> LIVE` | `REDUCE_ONLY -> LIVE` | private stream silence |
| OKX | `BLOCKED -> REDUCE_ONLY -> LIVE` | `BLOCKED -> REDUCE_ONLY -> LIVE` | reconcile diff |

对应证据文件：

- `docs/plans/dry-run-evidence/bybit-btc.json`
- `docs/plans/dry-run-evidence/binance-btc.json`
- `docs/plans/dry-run-evidence/okx-btc.json`
- `docs/plans/dry-run-evidence/bybit-eth.json`
- `docs/plans/dry-run-evidence/binance-eth.json`
- `docs/plans/dry-run-evidence/okx-eth.json`

## Findings

1. 当前仓库已经可以在 dry-run 配置、安全闸门、injector plan、audit 记录和 supervisor/checker 逻辑层面完成受控演练闭环。
2. `deploy/dry-run.env` 与应用配置契约原先不一致；`#65` 已补齐 `dry-run` 环境值支持，使 preflight 能真实执行。
3. 现有注入工具仍然是 plan generator，而不是直接作用于真实交易所连接的执行器；这与当前 repository-scoped 边界一致。

## Residual Risk

### 残余风险

1. 还没有真实交易所 live / testnet 连接验证。
2. 还没有真实订单、仓位、余额链路上的外部系统观测。
3. 还没有证明 Docker / deploy 路径在真实目标主机上的长期稳定性。

## Recommendation

在 **Phase 3 的仓库内干跑边界** 下，当前交付已经满足：

- BTC 与 ETH 都已完成受控演练
- 已观察到降级与恢复行为
- 操作员动作与审计链路已验证

因此建议：

- 关闭 `#20`
- 关闭 `#4`

前提是关闭说明中继续使用本报告的边界表述，不把它升级解释成真实交易所演练完成。

## Follow-up Input

### 后续输入

1. 后续阶段若要扩大到真实交易所或 testnet，需要新增独立 child issue，不应直接复用本次 closeout 结论。
2. 真实外部环境验证应把凭证、网络、注入执行器和操作员审批链路单独纳入治理。
3. Phase 4 及以后可以继续复用本次的 audit 记录格式和 evidence 目录结构。
