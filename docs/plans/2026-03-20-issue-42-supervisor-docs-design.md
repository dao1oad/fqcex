# Issue 42 Supervisor State Flow And Architecture Docs Design

## 背景

`#39`、`#40`、`#41` 已分别落地：

- 状态枚举与迁移契约
- 流触发器求值
- venue / instrument tradeability projection

当前剩下的缺口是：

- 没有一个高层状态流测试把这三层串起来
- `docs/architecture/STATE_MACHINE.md` 仍停留在概念列表，没有同步最新实现细节

`#42` 只做测试与文档收口，不新增新的 Supervisor 行为。

## 方案比较

### 方案 A：新增 `test_state_flow.py` 做端到端状态流测试，并更新 `STATE_MACHINE.md`

- 优点：完全符合 issue 标题
- 优点：能把状态契约、触发器、projection 一次串起来
- 优点：不再引入生产代码改动

### 方案 B：把高层场景散进已有 3 个测试文件

- 优点：文件更少
- 缺点：架构级状态流不集中，不利于作为 final guard

### 方案 C：同时补更多 runtime 集成

- 优点：更像最终集成测试
- 缺点：超出 `#42` 的测试/文档边界

## 选型

采用方案 A。

## 设计

### 测试文件

新增 `tests/perp_platform/supervisor/test_state_flow.py`，覆盖最小高层流：

1. `LIVE` + public lag -> `DEGRADED`，projection 仍允许 open/reduce
2. `DEGRADED` + public lag 继续恶化 -> `RESYNCING`，projection 只允许 reduce
3. `RESYNCING` + private lag -> `REDUCE_ONLY`
4. `REDUCE_ONLY` + reconciliation failure -> `BLOCKED`
5. `BLOCKED` 在健康输入下仍保持 `BLOCKED`
6. `DEGRADED` 在健康输入下恢复到 `LIVE`

必要时再加一个 instrument stricter override 场景，证明 projection 层不会放松 venue 限制。

### 文档更新

更新 `docs/architecture/STATE_MACHINE.md`，把当前实现明确写清：

- 状态枚举
- 允许迁移关系
- trigger thresholds
- `DEGRADED / RESYNCING / REDUCE_ONLY / BLOCKED` 的 tradeability 行为
- venue vs instrument projection 关系
- `BLOCKED` 不能直接回 `LIVE`

文档目标是让读者不看代码也能理解当前 Supervisor Phase 2 的最小实现。

## 测试策略

- `py -m pytest tests/perp_platform/supervisor/test_state_flow.py -q`
- `py -m pytest tests/perp_platform/supervisor -q`
- `py -m pytest tests -q`

并人工 review `docs/architecture/STATE_MACHINE.md`，确认与现有实现口径一致。

## 非目标

- 不新增新的 Supervisor 状态
- 不修改 `state_machine.py`、`triggers.py`、`projection.py`
- 不扩展到控制平面 API
