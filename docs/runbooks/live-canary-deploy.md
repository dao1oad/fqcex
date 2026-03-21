# Live Canary 部署 Runbook

## 适用范围

本 runbook 只覆盖第 5 阶段的小资金 live canary 主机准备与部署前 preflight，不等价于生产放量或多账户部署。

## 前置条件

- 目标主机已同步仓库内容
- 已安装 `docker`
- 已安装 `docker compose` 或 `docker-compose`
- 已安装 `python3`
- 已从 `deploy/live-canary.env.example` 生成目标 `deploy/.env`
- 已在主机上准备：
  - kill switch 文件
  - venue credentials files

## 必需文件

- `deploy/.env`
- `LIVE_CANARY_KILL_SWITCH_PATH` 指向的文件
- `BYBIT_CREDENTIALS_FILE`
- `BINANCE_CREDENTIALS_FILE`
- `OKX_CREDENTIALS_FILE`

这些路径都必须指向主机本地文件，不能把真实凭证提交进仓库。

## 最小 env 契约

必须至少确认：

- `PERP_PLATFORM_ENVIRONMENT=live-canary`
- `LIVE_CANARY_ENABLED=true`
- `CONTROL_PLANE_BIND_ADDRESS`
- `LIVE_CANARY_ALLOWED_VENUES`
- `LIVE_CANARY_ALLOWED_INSTRUMENTS`
- `LIVE_CANARY_MAX_NOTIONAL_USD`
- `LIVE_CANARY_KILL_SWITCH_PATH`
- `OPERATOR_UI_BIND_ADDRESS`
- `BYBIT_CREDENTIALS_FILE`
- `BINANCE_CREDENTIALS_FILE`
- `OKX_CREDENTIALS_FILE`

## Preflight

在目标主机运行：

```sh
sh deploy/scripts/preflight-live.sh
```

如果 `deploy/.env` 不在默认位置，可显式传入：

```sh
sh deploy/scripts/preflight-live.sh /srv/perp-platform/deploy/.env
```

preflight 会阻断：

- 缺失 env 文件
- 环境名不是 `live-canary`
- `LIVE_CANARY_ENABLED` 未开启
- venue / instrument allowlist 缺失
- kill switch 文件缺失
- 对应 venue 的 credentials file 缺失

## 部署前操作员检查

1. 当前 supervisor/operator 流程已经进入允许 live canary 的窗口
2. allowlist 只包含本轮批准的 venue / instrument
3. `LIVE_CANARY_MAX_NOTIONAL_USD` 已设置为本轮批准的小资金上限
4. kill switch 文件存在且路径正确
5. 三家 venue 的 credentials file 都已落在主机，且不在仓库内
6. 已准备 incident 记录入口与 operator 审批记录

## 部署步骤

preflight 通过后，在目标主机运行：

```sh
sh deploy/scripts/deploy.sh /srv/perp-platform/deploy/.env
```

该脚本会：

1. 构建 `control-plane` 与 `operator-ui` 两个服务
2. 使用 `docker compose up -d` 或 `docker-compose up -d` 拉起长期运行栈
3. 对 `control-plane` 健康接口和 `operator-ui` 首页做最小健康检查

默认情况下，这两个服务只绑定宿主 `127.0.0.1`，不要直接把未认证 operator write API 暴露到公网。

## 后续步骤

部署栈通过后，再进入：

- operator UI 人工验收
- canary issue

部署通过不等价于真实交易已执行。详细人工验收步骤见：

- `docs/runbooks/live-canary-acceptance.md`

## Kill Switch 约定

`LIVE_CANARY_KILL_SWITCH_PATH` 指向的文件使用最小格式：

```text
armed=false
```

若文件不存在，或内容为 `armed=true`，则 live canary gate 必须拒绝放行。

## Approval 入口

进入 live canary 前，必须满足 operator approval。详细规则见：

- `docs/runbooks/live-canary-approval.md`
