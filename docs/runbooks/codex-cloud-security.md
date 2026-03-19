# Codex Cloud Security

## 目标

冻结本仓库在 Codex cloud 中的 environment、setup script secrets、agent phase 网络访问和执行安全边界，确保后续 issue 迁到云端时仍然不接入真实交易凭证。

## 官方约束摘要

- Environment variables persist for the full task.
- Secrets are only available to setup scripts.
- Setup scripts run in a separate Bash session from the agent.
- Agent internet access 默认关闭；如需启用，必须使用 allowlist。

参考：

- [Codex cloud environments](https://developers.openai.com/codex/cloud/environments)
- [Codex cloud internet access](https://developers.openai.com/codex/cloud/internet-access)
- [Agent approvals and security](https://developers.openai.com/codex/agent-approvals-security)

## Allowed Environment Values

允许进入 Codex cloud 的 environment values 只应覆盖非敏感执行开关、测试配置和安装行为参数。

示例：

- `PERP_PLATFORM_ENVIRONMENT=test`
- `PYTHONUNBUFFERED=1`
- `PIP_DISABLE_PIP_VERSION_CHECK=1`

下列内容不得作为普通 environment values 注入：

- `BYBIT_API_KEY`
- `BYBIT_API_SECRET`
- `OKX_API_KEY`
- `BINANCE_API_KEY`
- 任何真实账户 ID 或账户别名

## Setup-Only Secrets

允许的 setup-only secrets 必须只用于 bootstrap，且权限为只读或最小化。

允许示例：

- read-only package registry tokens
- read-only source checkout tokens

禁止示例：

- exchange API keys
- exchange secret keys
- exchange passphrases
- venue account identifiers
- production database credentials
- deploy credentials
- VPN / SSH / bastion credentials
- operator approval tokens

如果某个任务必须依赖以上禁止项，该任务不得迁移到 Codex cloud，必须保留在本地或人工审批链路中执行。

## Network Access Policy

- agent phase 默认不启用互联网访问。
- `internet_access: None` 是默认安全值。
- setup script 可以联网安装依赖，但不应连接真实交易网络或生产内部网络。
- 如 agent phase 必须开启互联网访问，只允许：
  - 显式 allowlist
  - 可信域名
  - 只读方法 `GET`、`HEAD`、`OPTIONS`

推荐 allowlist 只包含任务所需最小域名，例如：

- `developers.openai.com`
- `platform.openai.com`
- `github.com`
- `api.github.com`

以下地址或能力保持禁用：

- 实盘交易所 REST / WebSocket
- 生产控制平面
- secrets manager
- deploy 目标环境
- 任意未审计外部 URL

## 何时必须留在本地

以下工作不进入 Codex cloud：

- 真实账户联调
- 实盘或仿真下单
- 私有流恢复与对账的真实网络验证
- 需要人工审计确认的 `REDUCE_ONLY` / `BLOCKED` 解封动作
- 任何依赖 VPN、堡垒机、SSH 或生产数据库的任务

## 执行前检查

在把后续 issue 迁到 Codex cloud 前，先确认：

1. 当前任务不接入真实交易凭证
2. 当前任务不需要真实交易网络
3. 当前任务不需要生产或生产近邻基础设施访问
4. 如需外网，allowlist 已最小化
5. 文档、测试和 review 证据路径已明确
