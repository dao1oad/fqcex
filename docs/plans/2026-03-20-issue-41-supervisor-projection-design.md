# Issue 41 Supervisor Projection Design

## 背景

`#39` 已冻结状态枚举与迁移契约，`#40` 已把流信号求值成状态变化。现在需要把这些状态投影成可消费的 tradeability 结果，并且明确区分：

- venue-level tradeability
- instrument-level tradeability

`#41` 只负责 projection，不再修改触发器求值逻辑。

## 方案比较

### 方案 A：先投影 venue-level，再在 instrument-level 上叠加更严格覆盖

- 优点：职责清晰，最容易表达“instrument 只能比 venue 更严格，不能更宽松”
- 优点：与 `Supervisor` 作为 tradeability truth source 的定位一致
- 优点：给后续更多 instrument-specific 信号留接口

### 方案 B：venue 和 instrument 用同一个函数返回统一对象

- 优点：代码更短
- 缺点：两层语义会混在一起，不利于测试和后续扩展

### 方案 C：现在就把 Bybit-specific 恢复细节揉进 projection

- 优点：表面上更贴近现有场景
- 缺点：污染 Supervisor 核心边界

## 选型

采用方案 A。

## 设计

### 包路径

沿用当前主线布局：

- `src/perp_platform/supervisor/projection.py`
- `tests/perp_platform/supervisor/test_projection.py`

### 投影对象

定义：

- `VenueTradeabilityProjection`
  - `venue`
  - `state`
  - `allow_open`
  - `allow_reduce`
  - `reason`
- `InstrumentTradeabilityProjection`
  - `venue`
  - `instrument_id`
  - `effective_state`
  - `allow_open`
  - `allow_reduce`
  - `reason`

`venue` 使用 `domain.instruments.Venue`，`instrument_id` 使用 `domain.instruments.InstrumentId`。

### Venue-level 规则

定义 `project_venue_tradeability(venue, state, reason)`：

- `LIVE`
  - `allow_open = True`
  - `allow_reduce = True`
- `DEGRADED`
  - `allow_open = True`
  - `allow_reduce = True`
- `RESYNCING`
  - `allow_open = False`
  - `allow_reduce = True`
- `REDUCE_ONLY`
  - `allow_open = False`
  - `allow_reduce = True`
- `BLOCKED`
  - `allow_open = False`
  - `allow_reduce = False`

这里把 `DEGRADED` 保持可交易，把 `RESYNCING` 明确收敛为只允许减仓。

### Instrument-level 规则

定义 `project_instrument_tradeability(venue_projection, instrument_id, instrument_state=None, reason=None)`：

- 若没有 instrument override
  - 直接继承 venue projection
- 若有 instrument override
  - 取 venue state 与 instrument state 中更严格的那个作为 `effective_state`
  - reason 优先使用 instrument reason，否则回退到 venue reason

严格程度排序：

- `LIVE`
- `DEGRADED`
- `RESYNCING`
- `REDUCE_ONLY`
- `BLOCKED`

也就是说：

- instrument 可以比 venue 更严格
- instrument 不能放松 venue 限制

## 测试策略

新增 `tests/perp_platform/supervisor/test_projection.py`：

- venue `LIVE` / `DEGRADED` 可开可减
- venue `RESYNCING` / `REDUCE_ONLY` 不可开但可减
- venue `BLOCKED` 全禁
- instrument 无 override 时继承 venue
- instrument stricter override 生效
- instrument 不能放松 stricter venue

## 非目标

- 不修改 `state_machine.py`
- 不修改 `triggers.py`
- 不引入交易所专属逻辑
- 不更新架构文档
