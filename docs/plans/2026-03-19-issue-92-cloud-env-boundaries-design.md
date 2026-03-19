# Issue #92 Codex Cloud Environment / Secrets / Network 设计

## 上下文

Issue `#92` 只负责冻结 Codex cloud 的 environment、secrets 与 agent internet access 约束，不改 orchestrator 代码路径，不接入真实交易凭证，也不推进 `#93` 的云端执行模型。当前仓库已经有 Linux/Bash setup 入口，但还缺少对 cloud 两阶段运行时、安全边界与网络策略的正式文档。

本设计以 Codex cloud 官方约束为依据：

- environment variables 在整个 task 生命周期内有效
- secrets 只在 setup script 阶段可用，进入 agent phase 前移除
- setup script 与 agent phase 是分离的 Bash 会话
- agent phase 默认关闭网络访问；如需开启，应使用域名 allowlist 和受限 HTTP methods

## 约束

- 只修改 `README.md`、`SECURITY.md`、`docs/runbooks/`、`docs/architecture/`、`tests/governance/` 与本 issue 的计划文档
- 不改 `src/`、`.codex/`、orchestrator 实现或 Bybit runtime 代码
- 不引入真实交易所密钥、真实账户标识或真实下单流程
- 保持与仓库现有运行安全要求一致：云端任务默认只能做文档、测试、静态校验和 mock / fake 配置类工作

## 方案对比

### 方案 A：只在 `SECURITY.md` 增补几条规则

- 优点：改动最小
- 缺点：缺少运行手册与 architecture 位置，无法冻结具体 environment / network 操作约束

### 方案 B：新增 architecture + runbook，并同步更新 `README.md` 与 `SECURITY.md`

- 优点：职责清晰
- 优点：能把两阶段运行模型、安全边界、推荐环境变量和 agent internet allowlist 原则分开表达
- 优点：适合用治理测试冻结关键约束
- 缺点：比方案 A 多两个文档文件

### 方案 C：直接连同 orchestrator 云端模式一起实现

- 优点：更完整
- 缺点：直接越界到 `#93`

## 推荐

采用 **方案 B**。

最小闭环是：

1. 在 `docs/architecture/` 新增 Codex cloud 边界文档，冻结两阶段运行模型
2. 在 `docs/runbooks/` 新增 Codex cloud 安全 runbook，给出 environment、secrets、网络访问和人工审批边界
3. 更新 `README.md` 与 `SECURITY.md`，把默认 cloud 安全要求写到仓库入口
4. 新增治理契约测试，锁定上述约束

## 设计

### 1. 两阶段运行模型

新增 `docs/architecture/CODEX_CLOUD_BOUNDARIES.md`，明确：

- Codex cloud 任务运行在隔离容器中
- setup script 可以联网安装依赖
- agent phase 默认离线
- setup script 与 agent phase 是分离会话，`export` 不会自动带入 agent phase

### 2. Environment 与 Secrets 边界

在 architecture 文档和 runbook 中冻结以下规则：

- **允许作为 environment variables 的仅限非敏感值**
  - `PERP_PLATFORM_ENVIRONMENT=test`
  - `PYTHONUNBUFFERED=1`
  - `PIP_DISABLE_PIP_VERSION_CHECK=1`
- **允许作为 secrets 的仅限 setup bootstrap 类值**
  - 私有包源或依赖安装所需凭据
  - 仅在 setup script 阶段消费
- **明确禁止**
  - `BYBIT_API_KEY`
  - `BYBIT_API_SECRET`
  - `BINANCE_API_KEY`
  - `BINANCE_API_SECRET`
  - `OKX_API_KEY`
  - `OKX_API_SECRET`
  - 任意 live account id、session token、真实订单/持仓日志

### 3. 网络访问策略

冻结本仓库在 Codex cloud 的默认网络策略：

- 默认 environment：agent internet access = `Off`
- 只有文档核对、GitHub issue / PR 操作等明确需要联网的任务，才允许临时开启
- 开启时从 `None` allowlist 起步，只添加任务所需域名
- 本仓库推荐的附加域名仅限：
  - `developers.openai.com`
  - `platform.openai.com`
  - `github.com`
  - `api.github.com`
- allowed HTTP methods 固定为：
  - `GET`
  - `HEAD`
  - `OPTIONS`

不使用 `All (unrestricted)`，也不把交易所 API 域名纳入 allowlist。

### 4. 允许与禁止的云端工作

在 runbook 中明确：

- **允许**
  - 文档
  - 测试
  - 静态校验
  - mock / fake 配置
  - GitHub 上的 issue / PR 文本协作
- **禁止**
  - 真实交易凭证接入
  - 真实账户联调
  - 私有流鉴权
  - 真实下单
  - 真实对账与恢复操作

### 5. 治理测试

新增 `tests/governance/test_codex_cloud_security_contract.py`，验证：

- `SECURITY.md` 已写明 cloud 环境下 environment / secrets / live credential 边界
- `docs/architecture/CODEX_CLOUD_BOUNDARIES.md` 已冻结两阶段运行模型与网络默认关闭
- `docs/runbooks/codex-cloud-security.md` 已冻结推荐环境变量、allowlist 域名和允许的 HTTP methods
- `README.md` 已链接新的 architecture / runbook 文档并说明不接入真实交易凭证

## 验证

- `python -m pytest tests/governance/test_codex_cloud_security_contract.py -q`
- `python -m pytest tests/governance -q`
- `python -m pytest tests -q`

## 超出范围

- orchestrator 云端状态与派发模式
- Codex cloud dry run
- GitHub / Codex cloud 集成开关本身
- 任何真实交易所密钥、网络联调或生产执行
