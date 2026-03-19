# #28 合约标识与市场枚举设计

## 背景

当前仓库已经冻结了统一模型的关键约束：

- [DATA_MODEL.md](D:/fqcex/.worktrees/issue-28-instrument-id-market-enums/docs/architecture/DATA_MODEL.md) 明确 `instrument_id = BASE-QUOTE-PERP`
- [DATA_MODEL.md](D:/fqcex/.worktrees/issue-28-instrument-id-market-enums/docs/architecture/DATA_MODEL.md) 明确数量真相字段为 `base_qty`
- [AGENTS.md](D:/fqcex/.worktrees/issue-28-instrument-id-market-enums/AGENTS.md) 明确 Phase 1 仅支持 `Bybit`、`Binance`、`OKX` 的 `USDT` 线性永续

但主线代码还没有任何 domain 层的合约标识模型或市场枚举。`#28` 的目标是把这些冻结约束从文档沉淀成最小、可测试的代码形态。

另一个需要先纠正的事实是：issue 原始预期文件路径仍停留在旧的 `apps/perp-platform/...` 结构，而主线从 `#25-#27` 起已经固定在根级 `src/`。本 issue 在开始实现前已将 issue body 修正为 `src/perp_platform/domain/instruments.py`。

## 目标

- 定义最小 `InstrumentId` 值对象
- 定义最小市场枚举：`Venue`
- 定义最小合约种类枚举：`InstrumentKind`
- 固化 `BASE-QUOTE-PERP` 的字符串表示和最小验证规则

## 非目标

- 不实现 `base_qty` 或 OKX 张数换算
- 不引入 position mode、margin mode、quote asset 等额外枚举
- 不实现 parser、repo、ORM 或运行时映射
- 不扩展到现货、期权、币本位或非 `USDT` Phase 1 场景

## 方案比较

### 方案 A：最小值对象 + 最小枚举

- `Venue`: `BYBIT` / `BINANCE` / `OKX`
- `InstrumentKind`: `PERP`
- `InstrumentId`: `base`、`quote`、`kind`
- `make_perp_instrument_id(base, quote="USDT")`

优点：

- 与当前 Phase 1 冻结边界完全一致
- 为 `#29/#30` 提供稳定挂点
- 不会提前引入数量或价格语义

缺点：

- 当前模型非常窄，只覆盖 `USDT` perp

### 方案 B：只做字符串 helper

- 例如 `build_instrument_id(base, quote, suffix)`

优点：

- 改动最小

缺点：

- 容易在后续 issue 中散成多套字符串约定
- 测试和验证粒度较弱

### 方案 C：把统一模型一次做全

- 同时引入 quote enum、margin mode、quantity fields

优点：

- 一次性更完整

缺点：

- 明显越过 `#28` 边界
- 会把 `#29/#30` 偷带进来

## 选型

采用方案 A。

理由：`#28` 只需要把“合约标识与市场枚举”从文档冻结成最小代码契约，值对象 + 枚举已经足够，不需要先把统一模型整层铺开。

## 设计

### 文件布局

新增：

- [src/perp_platform/domain/__init__.py](D:/fqcex/.worktrees/issue-28-instrument-id-market-enums/src/perp_platform/domain/__init__.py)
- [src/perp_platform/domain/instruments.py](D:/fqcex/.worktrees/issue-28-instrument-id-market-enums/src/perp_platform/domain/instruments.py)
- [tests/perp_platform/test_instruments.py](D:/fqcex/.worktrees/issue-28-instrument-id-market-enums/tests/perp_platform/test_instruments.py)

`domain/__init__.py` 只是最小包出口，不额外承担逻辑。

### 枚举定义

使用 `StrEnum`：

- `Venue.BYBIT = "BYBIT"`
- `Venue.BINANCE = "BINANCE"`
- `Venue.OKX = "OKX"`
- `InstrumentKind.PERP = "PERP"`

这样 `str(enum_member)` 就能直接得到稳定的字符串值，减少后续格式化歧义。

### InstrumentId 值对象

使用不可变 `dataclass`：

- `base: str`
- `quote: str`
- `kind: InstrumentKind`

最小验证规则：

- `base` 必须是非空的大写 ASCII 字母或数字
- `quote` 必须是非空的大写 ASCII 字母或数字
- 当前 helper 默认 `quote="USDT"`

字符串表示：

- `str(instrument_id) == "BASE-QUOTE-PERP"`

### Helper

提供：

- `make_perp_instrument_id(base: str, quote: str = "USDT") -> InstrumentId`

用途：

- 给后续 issue 一个最小、显式的构造入口
- 避免测试或运行时代码自行拼接字符串

这里不实现反向解析函数。当前没有直接需求，加入只会扩大 API 面。

### 测试策略

先写失败测试，验证：

- `Venue` 只包含 `BYBIT`、`BINANCE`、`OKX`
- `InstrumentKind` 只包含 `PERP`
- `make_perp_instrument_id("BTC")` 生成 `BTC-USDT-PERP`
- `InstrumentId` 的 `str()` 输出为 canonical 形式
- 非法小写或空 base 会报错

测试只覆盖 `USDT` perp 这条冻结边界，不提前验证非 Phase 1 产品。

## 风险与控制

- 风险：issue 标题里的“市场枚举”被解读得过宽
  - 控制：收口为当前 Phase 1 需要的 `Venue` 与 `InstrumentKind`
- 风险：模型过早开放非 `USDT` 产品
  - 控制：helper 默认围绕 `USDT` perp；测试只验证 Phase 1 形态
- 风险：后续又出现第二套 instrument 字符串约定
  - 控制：把 canonical 格式封装进值对象和 helper，而不是散落在调用方

## 验证

- `py -m pytest tests/perp_platform/test_instruments.py -q`
- `py -m pytest tests -q`
