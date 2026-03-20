# Issue 66 Dry Run Closeout Design

## Goal

基于 `#65` 已提交的 repository-scoped 干跑证据，输出结项报告与发现总结，为关闭 `#20` 和 `#4` 提供统一结论。

## Options

### Option A: 把结论写成真实 live / testnet 演练完成

不可接受。`#65` 已明确证据只覆盖仓库内受控演练，不能在 closeout 阶段改写事实。

### Option B: 只列证据文件，不给结论

信息不完整。这样仍然需要人工二次梳理，不能直接作为 tracking / epic 的关闭说明。

### Option C: 以 repository-scoped 口径发布 closeout（推荐）

- 明确本次演练的边界
- 汇总 BTC / ETH、三家 venue、三类故障路径的结果
- 记录已完成项、残余风险和后续阶段输入
- 把 `#65` 中发现的 `dry-run` 环境兼容性修复纳入结论

## Recommendation

采用 Option C。这样既能真实反映 Phase 3 的交付范围，又能把剩余的真实交易所验证工作留到后续阶段，而不是伪装成已经完成。

## Scope

- 新增 `docs/plans/dry-run-closeout.md`
- 新增一个直接契约测试，验证 closeout 文档包含：
  - repository-scoped 边界
  - `BTC-USDT-PERP`、`ETH-USDT-PERP`
  - `BYBIT`、`BINANCE`、`OKX`
  - 已完成项、残余风险、后续输入
- 不新增新的运行时代码
- 不修改 `#65` 证据文件
