# #29 数量归一化与 OKX 张数换算设计

## 背景

当前仓库已经具备：

- 统一合约标识模型 [src/perp_platform/domain/instruments.py](D:/fqcex/.worktrees/issue-29-quantity-normalization/src/perp_platform/domain/instruments.py)
- 文档冻结的数量真相规则 [docs/architecture/DATA_MODEL.md](D:/fqcex/.worktrees/issue-29-quantity-normalization/docs/architecture/DATA_MODEL.md)

其中数量模型已经在文档中明确：

- Truth quantity: `base_qty`
- Edge fields:
  - `exchange_qty`
  - `exchange_qty_kind`
- Venue mapping:
  - Bybit: `base_qty = qty`
  - Binance: `base_qty = quantity`
  - OKX: `base_qty = sz * base_per_exchange_qty`

`#29` 的目标是把这组冻结规则从文档转成最小可测试代码，而不提前扩展到 notional、运行时接线或额外文档工作。

## 目标

- 定义统一数量归一化模型
- 定义最小 `ExchangeQtyKind` 枚举
- 提供统一入口 `normalize_quantity(...)`
- 提供 OKX 特化入口 `okx_contracts_to_base_qty(...)`

## 非目标

- 不实现 `notional_usdt`
- 不更新架构文档或 Phase freeze 文档
- 不接入运行时 adapter
- 不扩展到除 Bybit / Binance / OKX 之外的 venue

## 方案比较

### 方案 A：最小值对象 + `Decimal` 归一化函数

- `ExchangeQtyKind`: `BASE` / `CONTRACTS`
- `NormalizedQuantity` 值对象：
  - `base_qty`
  - `exchange_qty`
  - `exchange_qty_kind`
  - `base_per_exchange_qty`
- `normalize_quantity(venue, exchange_qty, *, base_per_exchange_qty=None)`
- `okx_contracts_to_base_qty(exchange_qty, base_per_exchange_qty)`

优点：

- 与文档冻结字段完全对齐
- API 足够小，便于后续 `#30` 和 runtime issue 复用
- 不会把 `#29` 扩成更大的模型层

缺点：

- 当前只处理数量，不处理 notional 或价格

### 方案 B：只返回 `Decimal`

- `normalize_quantity(...) -> Decimal`

优点：

- 实现最短

缺点：

- 丢掉 `exchange_qty` 与 `exchange_qty_kind` 这些已冻结的边界字段
- 后续运行时还要再补一层包装

### 方案 C：把 notional、quote precision 一起做掉

优点：

- 表面上更完整

缺点：

- 明显越出 `#29`
- 会和 `#30`、后续 runtime/风控工作交叉

## 选型

采用方案 A。

理由：`#29` 只需要把数量真相模型和 OKX 张数换算收口成最小代码契约，值对象 + 显式函数就足够。

## 设计

### 文件布局

新增：

- [src/perp_platform/domain/quantity.py](D:/fqcex/.worktrees/issue-29-quantity-normalization/src/perp_platform/domain/quantity.py)
- [tests/perp_platform/test_quantity.py](D:/fqcex/.worktrees/issue-29-quantity-normalization/tests/perp_platform/test_quantity.py)

如有必要，同时更新 [src/perp_platform/domain/__init__.py](D:/fqcex/.worktrees/issue-29-quantity-normalization/src/perp_platform/domain/__init__.py) 暴露新的模型类型。

### 数值类型

全部使用 `Decimal`，并显式拒绝 `float`。

原因：

- 数量换算不能依赖浮点
- 拒绝 `float` 比静默转换更安全

支持的输入类型：

- `Decimal`
- `str`
- `int`

### 枚举与值对象

`ExchangeQtyKind`：

- `BASE`
- `CONTRACTS`

`NormalizedQuantity`：

- `base_qty: Decimal`
- `exchange_qty: Decimal`
- `exchange_qty_kind: ExchangeQtyKind`
- `base_per_exchange_qty: Decimal | None`

语义：

- Bybit / Binance：`exchange_qty_kind = BASE`
- OKX：`exchange_qty_kind = CONTRACTS`

### API

`okx_contracts_to_base_qty(exchange_qty, base_per_exchange_qty) -> Decimal`

- `exchange_qty > 0`
- `base_per_exchange_qty > 0`
- 返回 `exchange_qty * base_per_exchange_qty`

`normalize_quantity(venue, exchange_qty, *, base_per_exchange_qty=None) -> NormalizedQuantity`

- `venue` 使用前一 issue 已定义的 `Venue`
- Bybit / Binance：
  - `base_qty = exchange_qty`
  - `exchange_qty_kind = BASE`
  - 不允许传 `base_per_exchange_qty`
- OKX：
  - 要求提供 `base_per_exchange_qty`
  - `base_qty = exchange_qty * base_per_exchange_qty`
  - `exchange_qty_kind = CONTRACTS`

### 校验规则

- `exchange_qty` 必须是正数
- `base_per_exchange_qty` 必须是正数（仅 OKX 路径）
- `float` 输入一律报错
- Bybit / Binance 传入 `base_per_exchange_qty` 报错

### 测试策略

先写失败测试，验证：

- Bybit 数量直通
- Binance 数量直通
- OKX `sz * base_per_exchange_qty`
- OKX 缺少换算因子时报错
- 非正数量报错
- `float` 输入报错

测试不覆盖文档改写；那是 `#30` 的职责。

## 风险与控制

- 风险：把文档工作偷进 `#29`
  - 控制：只写模型代码和测试，不改 `DATA_MODEL.md`
- 风险：数值类型不稳
  - 控制：统一使用 `Decimal`，拒绝 `float`
- 风险：Bybit / Binance / OKX 路径混淆
  - 控制：用 `ExchangeQtyKind` 和显式 venue 分支固定语义

## 验证

- `py -m pytest tests/perp_platform/test_quantity.py -q`
- `py -m pytest tests -q`
