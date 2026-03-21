# Issue 149 Live Deploy 设计

## 背景

`#145-#148` 已建立最小 control-plane backend。`#149` 负责把 live canary 进入真实主机前必须具备的部署边界补齐：production-like env 模板、secret 入口契约、host preflight 和可执行 runbook。

## 方案比较

### 方案 A：`live-canary.env` 模板 + Python preflight + shell wrapper，推荐

优点：

- preflight 可以在 Windows 本地测试，也可以在 Linux 主机执行
- 缺失凭证路径、allowlist、kill switch 的阻断逻辑可直接写成 `pytest` 契约测试
- deploy boundary 与 runbook 边界清晰，不把真实交易 runtime 逻辑提前塞进来

### 方案 B：纯 shell preflight

缺点：

- 本地和 CI 验证更弱
- 行为细节更难通过 Python 测试稳定覆盖

### 方案 C：只补 env 和 runbook，不做可执行 preflight

不推荐：

- 不满足 issue 的验收标准
- live canary 前缺少真正的部署阻断点

## 推荐方案

采用方案 A。

## 设计

新增一份 production-like env 模板：

- `deploy/live-canary.env.example`

最小配置边界：

- `PERP_PLATFORM_ENVIRONMENT=live-canary`
- `LIVE_CANARY_ENABLED=true`
- `LIVE_CANARY_ALLOWED_VENUES`
- `LIVE_CANARY_ALLOWED_INSTRUMENTS`
- `LIVE_CANARY_KILL_SWITCH_PATH`
- `LIVE_CANARY_MAX_NOTIONAL_USD`
- `BYBIT_CREDENTIALS_FILE`
- `BINANCE_CREDENTIALS_FILE`
- `OKX_CREDENTIALS_FILE`

新增 preflight 实现：

- `scripts/live_canary_preflight.py`
- `deploy/scripts/preflight-live.sh`

第一版 preflight 只负责阻断明显不安全的部署前状态：

- env 文件缺失
- 环境名不是 `live-canary`
- `LIVE_CANARY_ENABLED` 未开启
- allowlist 缺失
- kill switch 路径缺失或目标文件不存在
- 所选 venue 的 credentials file 路径缺失或文件不存在

第一版不负责：

- 校验真实凭证内容
- 发起交易所连接
- 执行真实 canary
- 实施 max notional 运行时闸门

文档新增一份 host runbook：

- `docs/runbooks/live-canary-deploy.md`

并在现有 `deploy.md` 中加入口。

## 测试策略

先写失败测试，覆盖：

1. 有效 env + secret files + kill switch file 时 preflight 成功
2. 缺失 credentials file 时阻断
3. 缺失 allowlist 时阻断
4. 缺失 kill switch file 时阻断

## 文档更新

同步更新：

- `docs/runbooks/deploy.md`
- `docs/runbooks/live-canary-deploy.md`
- `README.md`
