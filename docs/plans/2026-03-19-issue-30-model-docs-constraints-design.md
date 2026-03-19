# #30 真相字段与架构约束文档设计

## 背景

当前仓库已经具备：

- 合约标识与市场枚举模型 [src/perp_platform/domain/instruments.py](D:/fqcex/.worktrees/issue-30-model-docs-constraints/src/perp_platform/domain/instruments.py)
- 数量归一化模型 [src/perp_platform/domain/quantity.py](D:/fqcex/.worktrees/issue-30-model-docs-constraints/src/perp_platform/domain/quantity.py)
- 最小架构文档 [docs/architecture/DATA_MODEL.md](D:/fqcex/.worktrees/issue-30-model-docs-constraints/docs/architecture/DATA_MODEL.md)
- 最小冻结边界文档 [docs/decisions/PHASE1_FREEZE.md](D:/fqcex/.worktrees/issue-30-model-docs-constraints/docs/decisions/PHASE1_FREEZE.md)

但当前文档仍然偏“条目清单”，没有把下面这些已经在仓库治理中冻结的约束解释成可审计的架构契约：

- 内部数量真相字段是 `base_qty`
- 风控和未实现盈亏统一使用 `mark_price`
- 交易所差异必须停留在边界层
- Phase 1 只支持 `USDT` 线性永续、`one_way`、`isolated`、`2x` 默认 / `3x` 上限和最小订单能力

`#30` 的目标是把这些约束固化进文档，并通过最小契约测试避免后续文档回退，而不是继续实现运行时代码。

## 目标

- 补全文档中的统一真相字段约束
- 补全文档中的边界层隔离约束
- 补全文档中的 Phase 1 模型冻结约束
- 为上述约束增加最小文档契约测试

## 非目标

- 不修改 `src/` 下业务代码
- 不引入新的 venue / product / runtime 行为
- 不更新 ADR 或 runbook
- 不顺手实现 `#31+` 的运行时初始化

## 方案比较

### 方案 A：只改文档

- 只更新 `DATA_MODEL.md`
- 只更新 `PHASE1_FREEZE.md`

优点：

- 变更最小
- 不新增测试负担

缺点：

- 后续文档很容易再次回退
- 无法把 `#30` 的完成标准变成可重复验证的契约

### 方案 B：文档 + 最小契约测试

- 更新 `DATA_MODEL.md`
- 更新 `PHASE1_FREEZE.md`
- 新增一个 governance 级文档契约测试

优点：

- 仍然保持 doc-only 边界
- 可以稳定检查关键术语和约束是否存在
- 最符合 “文档化真相字段与架构约束” 的最小闭环

缺点：

- 会新增一份轻量测试

### 方案 C：文档 + 代码内常量或 schema

- 用代码结构再表达一遍这些约束

优点：

- 表面上更“强约束”

缺点：

- 会直接越出 `#30`
- 容易和 `#31+`、`#39+` 的模型 / 状态机工作交叉

## 选型

采用方案 B。

理由：`#30` 的范围是文档化与约束冻结，而不是新增行为。文档加最小契约测试可以在不触碰运行时逻辑的前提下完成闭环。

## 设计

### 文档改动

`DATA_MODEL.md` 需要从“最小字段表”升级为“最小契约文档”，至少明确：

- canonical instrument 仍然是 `BASE-QUOTE-PERP`
- truth quantity 统一为 `base_qty`
- 风控与未实现盈亏使用 `mark_price`
- venue quantity mapping 的语义只是边界换算，不进入核心模型
- 交易所差异必须停留在边界层，不污染核心数据模型
- 当前位置范围固定为 `one_way` 与 `isolated`

`PHASE1_FREEZE.md` 需要明确：

- Phase 1 只支持 `USDT` 线性永续
- canonical instrument 形式与 `DATA_MODEL.md` 保持一致
- 数量真相仍然是 `base_qty`
- edge quantity mapping 只存在于适配器边界
- 风控价格口径为 `mark_price`
- 杠杆和订单能力边界不变

### 测试策略

新增一个最小 governance 契约测试，例如：

- `tests/governance/test_data_model_docs_contract.py`

测试只做文本约束检查，不做实现验证，重点确认：

- `DATA_MODEL.md` 含有 `base_qty`
- `DATA_MODEL.md` 含有 `mark_price`
- `DATA_MODEL.md` 含有“边界层隔离”的明确表述
- `PHASE1_FREEZE.md` 含有 `USDT` 线性永续、`one_way`、`isolated`
- `PHASE1_FREEZE.md` 含有 `base_qty` / `mark_price` 口径

### 风险与控制

- 风险：把文档 issue 扩成代码实现
  - 控制：禁止修改 `src/`，只改文档和测试
- 风险：测试过度脆弱
  - 控制：只检查关键术语，不绑定大段原文
- 风险：`DATA_MODEL.md` 与 `PHASE1_FREEZE.md` 说法不一致
  - 控制：用同一组核心术语收口：`base_qty`、`mark_price`、边界层隔离、Phase 1 产品边界

## 验证

- `py -m pytest tests/governance/test_data_model_docs_contract.py -q`
- `py -m pytest tests/governance -q`
- `py -m pytest tests -q`
