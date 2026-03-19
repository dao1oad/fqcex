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
- `main` 分支已包含治理基础和项目记忆系统。
- `main` 分支已按 issue 顺序合入 `#25-#27`：
  - 建立 `perp_platform` 最小 Python 包与模块入口
  - 建立最小配置初始化契约 `AppConfig` / `load_config()`
  - 建立共享测试基座 `tests/perp_platform/support`
- GitHub issue 树已补齐 `#79-#83`，用于承接 Phase 1 的 worktree/CI/部署基座缺口。
- GitHub issue 树已补齐 `#84-#88`，用于承接 Phase 4 的审计留痕设计缺口。
- `codex/ci-cd-bootstrap` 分支仍有 2 个未合并提交，但基于旧基线；当前应作为 `#79-#83` 的参考来源，而不是直接合并目标。
- `codex/perp-platform-bootstrap` worktree 仍存在，但该分支相对 `main` 已无独有提交，不应继续作为应用骨架现状真相源。

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
