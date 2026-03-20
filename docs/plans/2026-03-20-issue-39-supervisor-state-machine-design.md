# Issue 39 Supervisor State Machine Design

## 背景

Phase 2 的 tracking `#14` 需要先冻结 Supervisor 的状态契约，再分别实现触发器求值和投影逻辑。当前仓库只有架构文档里的状态列表，还没有可导入的状态机契约。

`#39` 只负责：

- 定义状态枚举
- 定义允许迁移表
- 提供一个最小的迁移验证函数

本 issue 不负责：

- 流触发器求值（留给 `#40`）
- venue / instrument 投影（留给 `#41`）
- 架构文档补充（留给 `#42`）

## 方案比较

### 方案 A：定义状态枚举 + 允许迁移表 + 纯函数验证

- 优点：边界最清晰
- 优点：`#40` 可以基于这份契约做 trigger evaluation，而不会被提前锁死事件命名
- 优点：测试可以直接围绕“允许/禁止迁移”展开

### 方案 B：直接定义状态枚举 + 事件枚举 + `apply(event)`

- 优点：看起来更像完整状态机
- 缺点：会把触发器语义提前塞进 `#39`，侵入 `#40`

### 方案 C：现在就把触发器和投影一起实现

- 优点：一次看起来更完整
- 缺点：明显跨越 `#40/#41` 边界

## 选型

采用方案 A。

## 设计

### 包路径

沿用主线实际布局，而不是 issue 中的旧 `apps/...` 路径：

- `src/perp_platform/supervisor/state_machine.py`
- `src/perp_platform/supervisor/__init__.py`
- `tests/perp_platform/supervisor/test_state_machine.py`

### 状态枚举

定义 `SupervisorState`：

- `LIVE`
- `DEGRADED`
- `RESYNCING`
- `REDUCE_ONLY`
- `BLOCKED`

状态口径对齐 `docs/architecture/STATE_MACHINE.md`。

### 迁移契约

定义允许迁移表：

- `LIVE` -> `DEGRADED`, `RESYNCING`, `REDUCE_ONLY`, `BLOCKED`
- `DEGRADED` -> `LIVE`, `RESYNCING`, `REDUCE_ONLY`, `BLOCKED`
- `RESYNCING` -> `LIVE`, `REDUCE_ONLY`, `BLOCKED`
- `REDUCE_ONLY` -> `LIVE`, `BLOCKED`
- `BLOCKED` -> `REDUCE_ONLY`

安全含义：

- `BLOCKED` 不允许直接回到 `LIVE`
- 必须先回到 `REDUCE_ONLY`，再由后续恢复逻辑决定是否回 `LIVE`

### 迁移对象

定义：

- `SupervisorTransition`
  - `previous_state`
  - `next_state`
  - `reason`
  - `changed`

### 迁移函数

定义：

- `allowed_supervisor_targets(state) -> tuple[SupervisorState, ...]`
- `transition_supervisor_state(current_state, next_state, reason) -> SupervisorTransition`

规则：

- 如果 `next_state == current_state`
  - 允许作为 no-op
  - `changed = False`
- 如果 `next_state` 在允许迁移表中
  - 返回 `changed = True`
- 否则抛出 `ValueError`

这样 `#40` 可以先根据 trigger 计算 target，再调用 `transition_supervisor_state()` 完成契约校验。

## 测试策略

新增 `tests/perp_platform/supervisor/test_state_machine.py`：

- 状态枚举值稳定
- `allowed_supervisor_targets()` 返回预期目标集
- 合法迁移返回 `SupervisorTransition`
- 相同状态返回 no-op transition
- `BLOCKED -> LIVE` 等非法迁移抛错

## 非目标

- 不定义 trigger enum
- 不实现 trigger evaluation
- 不定义 venue / instrument projection
- 不更新架构文档
