# AGENTS.md

## 1. 语言与输出

- 默认使用简体中文回复。
- 代码、命令、文件路径、标识符保持原样，通常为英文。
- 文档优先中文；必要时可保留关键英文术语。
- 风格要求：直接、简洁、可执行，避免空话。

## 2. 仓库目标

本仓库用于建设一个面向多交易所永续合约套利的连接管理平台。

当前冻结目标：

- 交易所：`Bybit`、`Binance`、`OKX`
- 产品范围：`USDT` 线性永续
- 主 runtime：`NautilusTrader`
- 交易可用性真相源：自建 `Supervisor`
- 独立公共行情校验：`Cryptofeed`

## 3. Phase 1 冻结边界

Phase 1 只允许实现以下范围：

- `one_way`
- `isolated`
- 默认杠杆 `2x`，硬上限 `3x`
- 订单能力：
  - `LIMIT`
  - `MARKET`
  - `CANCEL`
  - `GTC`
  - `IOC`
  - `reduce_only`

Phase 1 明确不做：

- 现货
- 币本位合约
- 交割合约
- 期权
- `hedge mode`
- `cross margin`
- 复杂条件单 / algo order
- Hummingbot 进入生产 runtime
- 一开始就全面 native adapter 化

## 4. 架构边界

- 订单、仓位、余额真相以主 runtime 链路为准。
- `Supervisor` 是交易可用性唯一真相源。
- `Cryptofeed` 只提供校验输入，不直接改写主真相状态。
- 交易所差异必须停留在边界层，不得污染核心数据模型。
- 内部统一 quantity 真相字段为 `base_qty`。
- 风控和未实现盈亏统一使用 `mark_price` 口径。

## 5. 变更控制

以下变更必须走 PR，不能直接在 `main` 上无审查提交：

- 状态机
- 恢复流程
- 风控规则
- 交易准入规则
- 数据模型
- 订单与持仓真相逻辑
- runbook
- ADR

以下变更必须新增或更新 `ADR`：

- 主 runtime 路线调整
- 新交易所接入策略变化
- 新产品类型引入
- 外部总线或审计平台的引入
- Phase 冻结范围变化

以下变更必须新增或更新 `runbook`：

- 告警阈值
- 人工解封策略
- `REDUCE_ONLY / BLOCKED` 规则
- 恢复步骤
- incident 处理方式

## 6. 文档要求

所有重要实现都必须同步更新以下文档之一：

- `docs/architecture`
- `docs/adr`
- `docs/decisions`
- `docs/runbooks`
- `docs/roadmap`
- `GOVERNANCE.md`
- `CONTRIBUTING.md`
- `SECURITY.md`

如果改动影响 Phase 1 冻结边界，必须更新：

- `docs/decisions/PHASE1_FREEZE.md`

## 7. 测试与验证

任何涉及连接管理、恢复、交易准入、对账、风控的改动，必须至少说明：

- 如何验证
- 影响哪些 venue / account / instrument
- 是否影响运行安全
- 是否需要故障注入验证

禁止在没有验证说明的情况下声称：

- “恢复已完成”
- “问题已修复”
- “现在可以安全交易”

## 8. 运行安全要求

- 公共流异常时，不允许继续盲目开新仓。
- 私有流未恢复且未对账通过前，不允许恢复开仓。
- 无法解释的订单、仓位、余额差异，必须升级为 `BLOCKED` 或继续保持 `REDUCE_ONLY`。
- `BLOCKED` 默认需要人工确认后才能恢复。
- 所有人工操作都必须有审计记录。

## 9. GitHub 治理约定

- roadmap 以 `Phase 0` 到 `Phase 6` milestones 表达。
- epic 使用普通 GitHub issue，并打 `type/epic` label。
- 子 issue 必须在正文中引用所属 epic。
- 公开仓库的协作和披露规则分别以 `GOVERNANCE.md`、`CONTRIBUTING.md`、`SECURITY.md` 为准。
- 涉及交易安全的 issue，优先使用：
  - `type/bug`
  - `type/incident`
  - `area/ops`
  - `area/architecture`

## 10. 默认工作方式

- 先收口边界，再做实现。
- 先写最小闭环，再扩范围。
- 先保证恢复和对账正确，再追求吞吐和覆盖面。
- 如果发现需求与 Phase 1 冻结边界冲突，先停下并更新决策文档，不要直接扩 scope。
