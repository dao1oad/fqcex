# Issue 55 Checker Bootstrap Design

## 背景

Phase 3 从独立市场数据校验器开始。`#55` 只负责最小 bootstrap 和配置边界：

- 定义 checker 自己的配置对象
- 定义稳定的服务标识
- 定义后续可供 `#56` 使用的订阅计划

这个 issue 不做：

- 真实 Cryptofeed 集成
- 顶档行情归一化
- 新鲜度/偏差策略
- Supervisor 信号输出

## 方案比较

### 方案 A：`config.py` + `bootstrap.py` + 订阅计划 dataclass

- 优点：与现有 venue runtime 的 `config/bootstrap` 分层一致
- 优点：后续 `#56` 可以直接基于订阅计划接入真实 feed
- 优点：当前不需要第三方依赖

### 方案 B：只定义静态常量，不做 bootstrap

- 优点：代码更少
- 缺点：没有服务身份和环境投影
- 缺点：后续每个调用点都要重复推导订阅目标

### 方案 C：直接接入 Cryptofeed FeedHandler

- 优点：更接近最终产物
- 缺点：超出 `#55` 范围
- 缺点：需要把第三方 API 选择提前冻结

## 选型

采用方案 A。

## 设计

### 路径

- `src/perp_platform/checker/__init__.py`
- `src/perp_platform/checker/config.py`
- `src/perp_platform/checker/bootstrap.py`
- `tests/perp_platform/test_checker_bootstrap.py`

### 配置对象

定义 `CheckerConfig`：

- `service_name`
- `venues`
- `instrument_ids`

环境变量入口：

- `CHECKER_SERVICE_NAME`
- `CHECKER_VENUES`
- `CHECKER_INSTRUMENTS`

默认值：

- `service_name = "cryptofeed-checker"`
- `venues = (BYBIT, BINANCE, OKX)`
- `instrument_ids = ("BTC-USDT-PERP", "ETH-USDT-PERP")`

### Phase 1/3 边界约束

- venue 仅允许 `BYBIT` / `BINANCE` / `OKX`
- instrument 仅允许 canonical `*-USDT-PERP`
- checker 只是独立校验器，不带执行或真相写入语义

### Bootstrap 结果

定义：

- `CheckerSubscriptionTarget`
- `CheckerBootstrapResult`

bootstrap 返回：

- `app_config`
- `checker_config`
- `service_label`
- `subscription_plan`

`service_label` 规则：

- `cryptofeed-checker-test`
- `cryptofeed-checker-prod`

`subscription_plan` 是 venues × instrument_ids 的稳定笛卡尔积，用于后续 `#56` 绑定真实 feed。

## 测试策略

新增 `tests/perp_platform/test_checker_bootstrap.py`，验证：

- config 正确读取环境变量
- 非法 venue 被拒绝
- 非 `USDT-PERP` instrument 被拒绝
- bootstrap 返回稳定 service label
- subscription plan 同时覆盖三家 venue 和默认 BTC/ETH perpetual

## 非目标

- 不新增第三方依赖
- 不直接创建 Cryptofeed `FeedHandler`
- 不定义偏差阈值
- 不定义 Supervisor 输出结构
