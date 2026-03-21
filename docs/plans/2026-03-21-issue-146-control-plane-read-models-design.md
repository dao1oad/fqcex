# Issue 146 控制平面读模型查询设计

## 背景

`#145` 已经为 control-plane 建立最小 HTTP skeleton，但当前仍只支持 `health` 和 `readiness`。`#146` 需要把 Phase 4 已冻结的四类只读资源真正挂到 HTTP 查询面上：

- venue tradeability
- instrument tradeability
- recovery runs
- checker signals

## 方案比较

### 方案 A：直接接 PostgreSQL 和真实 checker/runtime 数据源

优点：

- 看起来最接近最终形态

缺点：

- 当前仓库没有完整数据库连接 / query execution 层
- 会把 `#146` 扩成数据源集成 issue

### 方案 B：查询后端抽象 + HTTP 路由 + 序列化，推荐

优点：

- 先冻结读模型的代码合同和 HTTP 行为
- 不引入新的 truth source
- 后续可以在不改 HTTP surface 的前提下接真实 store / supervisor / checker 投影

缺点：

- 第一版查询实现仍是内存 / 适配层驱动

### 方案 C：继续只写文档，不落代码

不推荐：

- 不满足 issue 要求

## 推荐方案

采用方案 B。

## 设计

新增 `queries.py`，定义：

- `VenueTradeabilityView`
- `InstrumentTradeabilityView`
- `RecoveryRunView`
- `CheckerSignalView`
- `ControlPlaneQueryBackend` protocol
- `InMemoryControlPlaneQueryBackend`

扩展 `app.py`：

- 支持以下最小 GET 资源：
  - `/control-plane/v1/venues`
  - `/control-plane/v1/venues/{venue}`
  - `/control-plane/v1/instruments`
  - `/control-plane/v1/instruments/{instrument_id}`
  - `/control-plane/v1/recovery/runs`
  - `/control-plane/v1/recovery/runs/{run_id}`
  - `/control-plane/v1/checker/signals`
  - `/control-plane/v1/checker/signals/{signal_id}`

返回约束：

- 集合资源：`data = {"items": [...]}`
- 单资源：`data = {...}`
- 不存在资源：`404` + `not_found`

## 边界

本 issue 只负责：

- read-only query models
- query backend protocol
- HTTP GET handlers
- envelope / serialization / not_found 语义

本 issue 不负责：

- operator write actions
- audit query
- 数据库连接池或真实 SQL 执行
- 前端

## 测试策略

先写失败测试：

1. 列表与单资源都能返回正确 envelope
2. 返回字段与 Phase 4 读模型边界一致
3. 不存在资源返回 `404`
4. HTTP server 对查询端点可用

## 文档更新

同步更新：

- `README.md`，补充当前可用的 read-only query 端点
