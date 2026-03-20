# Issue 38 Bybit Recovery Modes Design

## 背景

`#35` 已冻结恢复顺序，`#36` 已冻结对账结果，`#37` 已把恢复状态和对账结果投影成 `REDUCE_ONLY` / `BLOCKED`。当前还缺一层“场景证明”和运行手册说明，确保操作员能根据恢复阶段、对账结果和 blocker 清单判断是否还能交易。

`#38` 只负责：

- 用一个场景测试把 recovery / reconciliation / tradeability 串起来
- 更新 `docs/runbooks/private-stream-recovery.md`

本 issue 不再修改运行时代码，也不新增 `LIVE` 返回逻辑。

## 方案比较

### 方案 A：新增 `test_recovery_modes.py` 做场景测试，并补 runbook

- 优点：完全符合 issue 标题
- 优点：只读消费前 3 个 child issue 的实现，不新增状态机分支
- 优点：能把 `REDUCE_ONLY` / `BLOCKED` / cooldown 手册口径固定下来

### 方案 B：在现有 `test_recovery_sequence.py`、`test_tradeability_projection.py` 里继续塞场景

- 优点：文件更少
- 缺点：顺序、投影、场景语义混在一起，难以作为恢复闭环验收文件

### 方案 C：在 runbook 中直接引入 `LIVE`

- 优点：看起来更完整
- 缺点：超出当前 issue 边界；当前代码还没有 `LIVE` 恢复状态

## 选型

采用方案 A。

## 设计

### 场景测试

新增 `tests/perp_platform/bybit/test_recovery_modes.py`，覆盖以下最小场景：

1. 私有流恢复但尚未对账时，投影保持 `REDUCE_ONLY`
2. 对账失败时，投影升级为 `BLOCKED`，并暴露 blocker 清单
3. 对账通过后，投影仍保持 `REDUCE_ONLY`，原因是 `cooldown_pending`

测试只消费现有模块：

- `perp_platform.runtime.bybit.recovery`
- `perp_platform.runtime.bybit.reconciliation`
- `perp_platform.runtime.bybit.tradeability`

不新增任何生产代码。

### Runbook 更新

更新 `docs/runbooks/private-stream-recovery.md`：

- Automatic Response 明确：
  - 恢复期间维持 `REDUCE_ONLY`
  - 对账失败升级 `BLOCKED`
- Manual Actions 明确：
  - 对账通过后仍需保持 `REDUCE_ONLY`
  - 只有在 cooldown / 观察完成、且符合 force resume policy 时，才允许人工恢复
- Escalation 明确：
  - 任一无法解释的订单 / 仓位 / 余额差异都应视为 `BLOCKED`

这样 runbook 就与 `#37` 的 tradeability 投影保持一致。

## 测试策略

- `py -m pytest tests/perp_platform/bybit/test_recovery_modes.py -q`
- `py -m pytest tests/perp_platform/bybit -q`
- `py -m pytest tests -q`

同时做一次人工 runbook review，确认文案与当前实现口径一致。

## 非目标

- 不修改 `src/perp_platform/runtime/bybit/*`
- 不引入 `LIVE` 状态
- 不修改其他交易所 runbook
- 不改 `docs/runbooks/force-resume-policy.md`
