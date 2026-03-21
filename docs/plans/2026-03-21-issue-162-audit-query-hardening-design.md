# Issue 162 Audit Query Hardening 设计

## 背景

`#148` 已把 audit query HTTP surface 合入主线，但后续预审确认了 3 个有效问题：

- shared audit query 默认暴露了未脱敏的 `scope` 和 `recorded_by`
- 时间窗口过滤对 RFC3339 时间戳做了字符串比较
- 非法时间查询参数没有返回 `invalid_request`

`#162` 只负责把这三点收回，不扩 scope。

## 方案比较

### 方案 A：默认 redacted audit view + RFC3339 解析与校验，推荐

优点：

- 直接满足当前文档里的 redaction 边界
- 不引入新的权限模型
- 在现有 in-memory backend 上就能稳定覆盖行为

### 方案 B：补 caller context / auth，再区分 full-fidelity 与 redacted view

缺点：

- 明显超出 `#162`
- 会把权限模型和 control-plane auth 提前带进来

### 方案 C：仅修时间过滤，不处理脱敏

不推荐：

- 保留了当前最危险的数据暴露问题

## 推荐方案

采用方案 A。

## 设计

### 1. 默认 redacted query view

保持 `AuditEventView` 作为内部 read model，但 control-plane HTTP 默认只返回 redacted 视图：

- `recorded_by` 固定返回 `"redacted"`
- `scope` 只保留最小 allowlist：
  - `venue`
  - `instrument_id`
  - `run_id`
- 其余 scope key 一律裁剪

这样可以保证：

- operator UI 仍然有最小上下文
- 默认 shared view 不泄露 account/operator/private detail

### 2. 时间窗口按真实时间比较

- `occurred_after`
- `occurred_before`

都先解析为 aware `datetime`

- 支持 `Z`
- 支持 `+08:00` 这类 offset

过滤时把 event 的 `occurred_at` 也按相同规则解析后比较。

### 3. 非法参数直接返回 `invalid_request`

如果 query string 中的时间参数不是合法 RFC3339 时间戳：

- HTTP `400`
- error code `invalid_request`

不再静默返回空列表。

## 测试策略

先写失败测试：

1. 默认 audit list/detail 返回 redacted `recorded_by`
2. 非 allowlist 的 scope 字段不会暴露
3. `+08:00` 与 `Z` 的时间窗口比较正确
4. 非法时间参数返回 `400 invalid_request`

## 文档更新

同步更新：

- `docs/architecture/AUDIT_LOG.md`
- `README.md`
