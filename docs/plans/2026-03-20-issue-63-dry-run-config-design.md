# Issue 63 Dry Run Config Design

## Goal

为 BTC / ETH 小规模干跑准备最小配置模板和安全闸门说明，但不假装 live 环境已经可用。

## Recommendation

- 新增 `deploy/dry-run.env` 作为单独模板
- 在 `docs/runbooks/deploy.md` 中增加 dry-run 启动步骤和安全闸门检查项
- 明确该模板只允许 `BTC-USDT-PERP`、`ETH-USDT-PERP`

## Safety Gates

- `DRY_RUN_ENABLED=true`
- `DRY_RUN_ALLOWED_INSTRUMENTS=BTC-USDT-PERP,ETH-USDT-PERP`
- `DRY_RUN_ABORT_ON_CHECKER_DIVERGENCE=true`
- `DRY_RUN_ABORT_ON_SUPERVISOR_REDUCE_ONLY=true`
- `DRY_RUN_ABORT_ON_SUPERVISOR_BLOCKED=true`
