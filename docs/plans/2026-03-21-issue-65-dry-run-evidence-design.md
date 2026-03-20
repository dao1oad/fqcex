# Issue 65 Dry Run Evidence Design

## Goal

在不假装 live / testnet 环境已经可用的前提下，完成 BTC 与 ETH 的 repository-scoped 干跑演练证据归档，并为 `#66` 提供可直接汇总的输入。

## Options

### Option A: 伪造外部环境演练记录

不可接受。当前仓库没有真实交易所密钥、运行态部署环境或可执行注入通道，直接写成“真实交易所演练完成”会违反治理与审计要求。

### Option B: 直接标记 `#65` blocked

这是保守兜底，但会让 Phase 3 无法在仓库内闭环，而且现有 `dry-run.env`、audit script、injector plan 和 supervisor/checker 逻辑都还没有被真正串起来。

### Option C: repository-scoped 受控演练证据（推荐）

- 使用 `deploy/dry-run.env` 作为干跑配置模板输入
- 运行现有 audit / injector CLI，生成结构化证据文件
- 运行 checker / supervisor 的最小可执行观测命令，记录降级、恢复、`REDUCE_ONLY`、`BLOCKED` 的仓库内观测结果
- 在 `docs/plans/dry-run-evidence.md` 中明确声明：
  - 本次演练是 repository-scoped
  - 使用仓库内 dry-run 配置、injector plan 和状态机逻辑
  - 不宣称真实交易所 live / testnet 已接通

## Recommendation

采用 Option C。它满足 `#63/#64` 已冻结边界，能真实地把 BTC / ETH、三家 venue、三类故障注入、审计链路和 supervisor/checker 观测串起来，同时不突破当前仓库缺少真实外部环境的事实。

## Scope

- 新增 `docs/plans/dry-run-evidence.md`
- 新增 `docs/plans/dry-run-evidence/` 下的证据 JSON 文件
- 必要时补一个最小 direct-support 修复，让 `deploy/dry-run.env` 的 preflight 能真实执行
- 新增一个直接契约测试，校验证据文档和证据文件覆盖：
  - `BTC-USDT-PERP`
  - `ETH-USDT-PERP`
  - `BYBIT`
  - `BINANCE`
  - `OKX`
- 不新增真实交易代码
- 不修改运行时、状态机、交易所客户端实现
