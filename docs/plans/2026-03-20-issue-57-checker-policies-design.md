# Issue 57 Checker Policies Design

## Goal

在不提前实现 Supervisor 信号映射的前提下，为 `Cryptofeed checker` 增加最小的新鲜度（freshness）与顶档偏差（top-of-book divergence）策略层，产出后续 `#58` 可直接消费的统一评估结果。

## Context

- `#55` 已定义 checker 的配置与 bootstrap。
- `#56` 已把 `Bybit`、`Binance Futures`、`OKX` 的顶档行情归一化为 `CheckerTopOfBook`。
- `#57` 只负责策略判断，不负责：
  - 把结果写入 Supervisor
  - 改动状态机
  - 新增运行时或告警配置面

## Options

### Option A: 固定阈值的独立策略层

在 `src/perp_platform/checker/policies.py` 中定义：

- 参考顶档输入模型
- 策略阈值模型
- 策略评估结果模型
- freshness / divergence 评估函数

优点：

- 与 `#58` 解耦，策略层只负责判断
- 不引入新的配置面，最符合当前 issue 边界
- 可以在测试中稳定覆盖边界值和异常输入

缺点：

- 阈值先固定在代码里，后续若要外化配置需要再开 sibling issue

### Option B: 现在就增加环境变量阈值

把 freshness / divergence 阈值直接加入 `CheckerConfig`。

优点：

- 运行时更灵活

缺点：

- 提前扩到配置治理
- 需要同步 bootstrap、runbook 和可能的操作员文档
- 超出 `#57` 的最小边界

### Option C: 直接输出 Supervisor 可消费信号

跳过独立策略层，在本任务里直接做 signal mapping。

优点：

- 交付链路更短

缺点：

- 与 `#58` 重叠
- 会把当前 issue 扩成两件事

## Recommendation

选 **Option A**。

`#57` 只做“判断”，不做“投影”。这样 `#58` 只需要把已验证的策略结果映射成 Supervisor 输入，不会把阈值、比较口径和状态语义混在一起。

## Design

### Policy Inputs

新增 `CheckerReferenceTopOfBook`，表示主 runtime 或其他真相路径提供的同 venue / instrument 顶档参考值：

- `venue`
- `instrument_id`
- `bid_price`
- `ask_price`
- `observed_timestamp`

保留最小字段，不引入 size，因为当前偏差策略只比较 price。

### Thresholds

新增 `CheckerPolicyThresholds`：

- `max_staleness_seconds`
- `max_divergence_bps`

默认值推荐：

- `max_staleness_seconds = 3.0`
- `max_divergence_bps = 5.0`

理由：

- `3.0s` 与现有 Supervisor public-stream resync 量级一致，足够表达“checker 自己也不能太旧”
- `5.0bps` 作为顶档偏差的 Phase 3 初始阈值足够保守，但还不把更细的多档阈值体系提前带进来

### Freshness

freshness 只基于 `CheckerTopOfBook.receipt_timestamp` 计算：

- `age_seconds = now_timestamp - receipt_timestamp`
- `age_seconds > max_staleness_seconds` 时视为 stale

不以 `event_timestamp` 作为主判断口径，原因：

- `receipt_timestamp` 是本地一致时钟
- `event_timestamp` 在不同 venue 语义与精度不完全一致
- `event_timestamp` 保留用于诊断，而不是本任务的主策略依据

### Divergence

divergence 比较同 venue / instrument 的 checker 顶档与参考顶档：

- `bid_divergence_bps = abs(checker.bid_price - reference.bid_price) / reference.bid_price * 10_000`
- `ask_divergence_bps = abs(checker.ask_price - reference.ask_price) / reference.ask_price * 10_000`
- `max_divergence_bps = max(bid_divergence_bps, ask_divergence_bps)`
- `max_divergence_bps > threshold` 时视为 diverged

如果 venue 或 instrument 不一致，直接 fail closed 抛错。

### Outputs

新增统一结果 `CheckerPolicyResult`：

- `venue`
- `instrument_id`
- `age_seconds`
- `stale`
- `bid_divergence_bps`
- `ask_divergence_bps`
- `max_divergence_bps`
- `diverged`

并提供总入口 `evaluate_checker_policies(...)`，一次返回完整结果。

## Testing

新增 `tests/perp_platform/test_checker_policies.py`，覆盖：

1. receipt timestamp 在阈值内时，freshness 为 healthy
2. receipt timestamp 超阈值时，freshness 为 stale
3. checker 与 reference 小幅差异时，不触发 divergence
4. bid 或 ask 任一侧超阈值时，触发 divergence
5. venue / instrument 不一致时 fail closed

## Docs

同步更新 `docs/architecture/ARCHITECTURE.md`，增加 checker policy 口径说明：

- freshness 以 `receipt_timestamp` 为准
- divergence 以同 venue / instrument 的 bid/ask relative bps 计算
- policy 层只产出判断，不直接写 Supervisor 真相
