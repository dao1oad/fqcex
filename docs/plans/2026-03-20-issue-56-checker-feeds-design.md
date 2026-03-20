# #56 Cryptofeed 顶档接入与归一化设计

## 目标

在不引入新鲜度/偏差策略和 Supervisor 信号的前提下，把 `Bybit`、`BinanceFutures`、`OKX` 的顶档盘口接入到 `checker` 边界层，并归一化成仓库内部可复用的统一模型。

## 方案比较

### 方案 A：统一使用 `L1_BOOK`

- 优点：概念上最贴近“顶档盘口”。
- 缺点：`Cryptofeed` 官方文档虽然定义了 `L1_BOOK` / `L1Book`，但官方 exchange 实现里这三家更稳定、明确的顶档来源是 `TICKER` 回调中的 bid/ask 与 raw size 字段，而不是统一的 `L1_BOOK` 接线。

### 方案 B：使用 `TICKER` 并在边界层提取 bid/ask 与 size，推荐

- 优点：与官方 exchange 实现一致，三家都已提供稳定的 `TICKER` 通道和 raw 顶档 size 字段。
- 优点：可以在 `#56` 只完成“接入并归一化”，把新鲜度与偏差逻辑留给 `#57`。
- 缺点：size 需要从不同 venue 的 raw payload 字段中提取，不能只依赖 `Ticker` 对象公开字段。

### 方案 C：只做本地订阅规格，不真正接 `Cryptofeed`

- 优点：实现最轻。
- 缺点：不满足“接入”要求，只是又做了一层静态配置。

## 推荐设计

采用方案 B：

- 在 `pyproject.toml` 中增加 `cryptofeed>=2.4,<3`。
- 在 `src/perp_platform/checker/models.py` 中定义统一的 `CheckerTopOfBook` 模型。
- 在 `src/perp_platform/checker/feeds.py` 中提供：
  - Phase 1 最小符号映射预热；
  - venue 到 `Cryptofeed` exchange class 的绑定；
  - 基于 `FeedHandler + TICKER` 的 feed 构造；
  - `Ticker/raw` 到 `CheckerTopOfBook` 的归一化。

## 关键设计点

### 1. 顶档来源

基于官方 `Cryptofeed` 源码，三家顶档最稳的接入面如下：

- `Bybit`：`TICKER` / `tickers`
- `BinanceFutures`：`TICKER` / `bookTicker`
- `OKX`：`TICKER` / `tickers`

归一化时使用：

- `Ticker.bid` / `Ticker.ask`
- `Ticker.raw` 中的 venue-specific 顶档 size 字段

### 2. 规避运行时符号发现

`Cryptofeed` exchange 在构造时会尝试通过 REST 拉取 symbol mapping。对当前仓库这会带来两个问题：

- 本地/云端执行时受代理或交易所限流影响；
- `#56` 不需要为 Phase 1 的两个合约去做全市场发现。

因此在 `#56` 只预热当前冻结范围内的最小映射：

- `Bybit`
  - `BTC-USDT-PERP -> BTCUSDT`
  - `ETH-USDT-PERP -> ETHUSDT`
- `BinanceFutures`
  - `BTC-USDT-PERP -> BTCUSDT`
  - `ETH-USDT-PERP -> ETHUSDT`
- `OKX`
  - `BTC-USDT-PERP -> BTC-USDT-SWAP`
  - `ETH-USDT-PERP -> ETH-USDT-SWAP`

这层映射保持在 checker 边界内，不污染核心模型。

### 3. 统一模型

`CheckerTopOfBook` 只保留本任务需要的最小字段：

- `venue`
- `instrument_id`
- `exchange_symbol`
- `bid_price`
- `bid_size`
- `ask_price`
- `ask_size`
- `event_timestamp`
- `receipt_timestamp`

不在本 issue 中加入：

- 新鲜度判断
- 偏差阈值
- Supervisor 信号

### 4. 输出形态

`#56` 的 feed 层产出是“归一化后的顶档事件”回调，不直接写 Supervisor。

后续：

- `#57` 基于该事件做 freshness / divergence policy
- `#58` 再把策略结果投影成 Supervisor 可消费信号

## 测试策略

先写失败测试，覆盖：

1. 符号预热后，三家 exchange 能在不做 REST symbol discovery 的情况下构造 feed。
2. feed builder 会为 `Bybit` / `BinanceFutures` / `OKX` 注册 `TICKER` 回调。
3. 三家 raw payload 能被正确归一化为 `CheckerTopOfBook`。
4. 缺失顶档 size 字段时给出清晰错误，而不是静默退化。

## 文档影响

本任务会顺手把 checker 接入面补进 `docs/architecture/ARCHITECTURE.md`，说明：

- Phase 3 checker 的顶档来源是 `Cryptofeed TICKER`
- venue-specific size 字段只停留在 checker 边界
