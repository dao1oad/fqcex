# 部署 Runbook

## 前置条件

- 已安装 `docker`
- 已安装 `docker compose`
- 仓库内容已同步到目标主机
- 已准备 `deploy/.env`
- 已记录可回退的上一个 `PERP_PLATFORM_IMAGE_TAG`

## 环境变量

从 `deploy/.env.example` 复制到 `deploy/.env`，并至少确认以下变量：

- `PERP_PLATFORM_APP_NAME`
- `PERP_PLATFORM_ENVIRONMENT`
- `PERP_PLATFORM_LOG_LEVEL`
- `PERP_PLATFORM_IMAGE_REPO`
- `PERP_PLATFORM_IMAGE_TAG`

当前 runbook 只覆盖单机、单环境、单服务启动，不包含交易所密钥或多账户部署策略。

## Dry Run 模板

`deploy/dry-run.env` 提供 Phase 3 小规模干跑的最小模板，默认只允许：

- `BTC-USDT-PERP`
- `ETH-USDT-PERP`

并默认启用以下安全闸门：

- `DRY_RUN_ABORT_ON_CHECKER_DIVERGENCE=true`
- `DRY_RUN_ABORT_ON_SUPERVISOR_REDUCE_ONLY=true`
- `DRY_RUN_ABORT_ON_SUPERVISOR_BLOCKED=true`

执行干跑前，先复制或合并该模板到目标 `deploy/.env`，不要直接在生产 env 上临时修改。

## Live Canary 模板

`deploy/live-canary.env.example` 提供 Phase 5 小资金 live canary 的最小 env 契约。

进入 live canary 前，先复制该模板到目标 `deploy/.env`，并补齐：

- host-local credentials file paths
- kill switch file path
- venue / instrument allowlist
- canary max notional

不要把真实凭证写进仓库，也不要直接沿用 dry-run env 进入 live canary。

## Dry Run Operator Checklist

启动前，操作员至少确认：

1. `deploy/dry-run.env` 已复制到目标 `deploy/.env`
2. 仅启用了 `BTC-USDT-PERP`、`ETH-USDT-PERP`
3. checker 和 supervisor 没有处于 `REDUCE_ONLY` 或 `BLOCKED`
4. 已准备审计采集命令，例如：

```sh
py scripts/capture_dry_run_audit.py --operator alice --stage btc-preflight --venue BYBIT --instrument-id BTC-USDT-PERP --action start_dry_run --result success --evidence-path docs/plans/dry-run-evidence.md
```

## Bootstrap 步骤

运行：

```sh
deploy/scripts/bootstrap-server.sh
```

该脚本会：

- 检查 `docker` 是否可用
- 检查 `docker compose` 是否可用
- 创建 `deploy/state`
- 校验 `deploy/.env` 是否存在

## Live Canary Preflight

进入 live canary 前，先运行：

```sh
deploy/scripts/preflight-live.sh
```

它会在部署前阻断缺失 credentials file、缺失 allowlist 或缺失 kill switch 的环境。

详细流程见 `docs/runbooks/live-canary-deploy.md`。

## 部署步骤

运行：

```sh
deploy/scripts/deploy.sh
```

该脚本会：

- 调用 `deploy/scripts/bootstrap-server.sh`
- 执行 `docker compose --env-file deploy/.env -f deploy/docker-compose.yml build`
- 执行 `docker compose --env-file deploy/.env -f deploy/docker-compose.yml run --rm perp-platform`

## 成功信号

最小成功信号是容器完成启动并以退出码 `0` 结束，标准输出包含类似：

```text
perp-platform bootstrap ready [dev]
```

环境名取决于 `PERP_PLATFORM_ENVIRONMENT`。

## 失败处理前置说明

- 若 `bootstrap-server.sh` 失败，先修复本机 Docker 或 `deploy/.env`
- 若镜像构建失败，保留失败日志并回到上一个可用 `PERP_PLATFORM_IMAGE_TAG`
- 若容器运行失败，不继续做 smoke 或交易相关动作
- 真正的 rollback 脚本与详细回退步骤在后续 `#83` 中补齐
