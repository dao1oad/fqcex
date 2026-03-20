# Issue 52 OKX Contract Conversion Design

## 背景

`#51` 已经把 OKX USDT perpetual 的 config/bootstrap 入口落地。`#52` 只解决下一步：

- 在 OKX runtime 边界层提供 `sz`（contracts）到 `base_qty` 的稳定换算入口
- 保持核心真相字段仍然是 `base_qty`
- 不把 OKX 的张数语义泄漏到更深的核心模型

它不提前实现：

- OKX runtime / order path guards
- OKX 启动回归测试
- 新的核心 quantity 数据结构

## 方案比较

### 方案 A：在 runtime/okx 增加轻量 wrapper，复用 domain quantity

- 优点：不重复定义 `NormalizedQuantity`
- 优点：runtime 层可以把 OKX 边界语言收口为 `base_per_contract`
- 优点：为 `#53` 的 guards 提供稳定入口

### 方案 B：直接在各调用点使用 `domain.normalize_quantity(...)`

- 优点：代码更少
- 缺点：OKX 边界语言会散落到多个调用点
- 缺点：后续 runtime 层约束难以集中维护

### 方案 C：在 runtime/okx 再定义一套新的 quantity dataclass

- 优点：表面上更“独立”
- 缺点：和 `domain.NormalizedQuantity` 重复
- 缺点：超出当前 issue 最小范围

## 选型

采用方案 A。

## 设计

### 路径

- `src/perp_platform/runtime/okx/conversion.py`
- `src/perp_platform/runtime/okx/__init__.py`
- `tests/perp_platform/okx/__init__.py`
- `tests/perp_platform/okx/test_conversion.py`

### 运行时换算入口

新增两个函数：

- `normalize_okx_contract_quantity(exchange_qty, *, base_per_contract)`
- `okx_contracts_to_base_qty(exchange_qty, *, base_per_contract)`

设计原则：

- 输入语言使用 OKX venue 边界口径：`base_per_contract`
- 内部复用 `domain.normalize_quantity(Venue.OKX, ...)`
- 输出保持核心统一结构：`NormalizedQuantity`

### 包装语义

`normalize_okx_contract_quantity(...)` 返回：

- `base_qty`
- `exchange_qty`
- `exchange_qty_kind = CONTRACTS`
- `base_per_exchange_qty`

`okx_contracts_to_base_qty(...)` 只是 `normalize_okx_contract_quantity(...).base_qty` 的便捷入口。

### 边界约束

- `exchange_qty` 必须是正数
- `base_per_contract` 必须是正数
- 不接受 `float`
- 不接受缺失的 `base_per_contract`

这些约束由现有 `domain.quantity` 统一执行，runtime wrapper 不重新发明一套校验逻辑。

## 测试策略

新增 `tests/perp_platform/okx/test_conversion.py`，验证：

- contracts 精确换算为 `base_qty`
- wrapper 返回 `NormalizedQuantity`
- `exchange_qty_kind` 保持 `CONTRACTS`
- `base_per_contract` 缺失或非正数时报错
- `float` 输入被拒绝

另外增加 `tests/perp_platform/okx/__init__.py`，为后续 `#54` 的 `test_bootstrap.py` 预留 package 边界，避免 pytest 模块名冲突。

## 非目标

- 不新增 `runtime.py`
- 不新增 `guards.py`
- 不修改 `docs/architecture/DATA_MODEL.md`
- 不改变全局 `domain.quantity` 契约
