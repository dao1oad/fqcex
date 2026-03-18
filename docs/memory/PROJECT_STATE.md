# PROJECT_STATE

## 项目目标

`fqcex` 是一个面向多交易所永续合约套利的连接管理平台。

## Phase 1 范围

- 交易所：`Bybit`、`Binance`、`OKX`
- 产品范围：`USDT` 线性永续
- 主 runtime：`NautilusTrader`
- 交易可用性真相源：自建 `Supervisor`
- 独立公共行情校验：`Cryptofeed`

## 主架构

- 订单、仓位、余额真相以主 runtime 链路为准。
- `Supervisor` 决定交易是否可继续。
- `Cryptofeed` 只提供公共行情校验输入。
- 交易所差异停留在边界层，不污染核心数据模型。
- 内部统一使用 `base_qty` 和 `mark_price` 作为核心真相口径。

## 已完成基础设施

- 仓库治理骨架已建立，包含 `GOVERNANCE.md`、`CONTRIBUTING.md`、`SECURITY.md`。
- GitHub 侧已建立 roadmap milestones、labels、epics 和首批 issues。
- `main` 分支保留治理与文档基础。
- `codex/ci-cd-bootstrap` 分支已实现 CI/CD、Playwright smoke 和自动部署骨架，但尚未合并到 `main`。
- `codex/perp-platform-bootstrap` 分支已建立最小应用骨架，但尚未合并到 `main`。

## 当前冻结边界

- `one_way`
- `isolated`
- 默认杠杆 `2x`
- 硬上限 `3x`
- `LIMIT`、`MARKET`、`CANCEL`
- `GTC`、`IOC`
- `reduce_only`

## 当前不做

- 现货
- 币本位合约
- 交割合约
- 期权
- `hedge mode`
- `cross margin`
- 复杂条件单 / algo order
- Hummingbot 进入生产 runtime
