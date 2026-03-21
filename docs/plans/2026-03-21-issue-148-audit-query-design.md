# Issue 148 Audit Query 设计

## 背景

`#145-#147` 已经建立了最小 control-plane skeleton、read-only query surface 和 operator actions。`#148` 负责把 audit query read surface 真正落到 HTTP 接口上，供 operator UI、closeout 和人工验收读取结构化审计留痕。

## 方案比较

### 方案 A：直接接数据库并实现复杂检索

缺点：

- 当前仓库没有完整 audit query execution 层
- 超出 `#148`

### 方案 B：最小 audit query models + filter 语义 + HTTP GET handlers，推荐

优点：

- 精准贴合 issue 目标
- 先冻结 query 行为和字段边界

### 方案 C：只做单条查询，不支持过滤

不推荐：

- 不能满足 `correlation_id` 和时间窗口的最小验收

## 推荐方案

采用方案 B。

## 设计

扩展 `queries.py`：

- `AuditEventView`
- `AuditEventQuery`
- query backend:
  - `list_audit_events(query)`
  - `get_audit_event(event_id)`

扩展 `app.py`：

- `GET /control-plane/v1/audit/events`
- `GET /control-plane/v1/audit/events/{event_id}`
- 支持 query params：
  - `correlation_id`
  - `occurred_after`
  - `occurred_before`

第一版过滤语义：

- `correlation_id` 精确匹配
- 时间窗口按 ISO timestamp 字符串比较

## 非目标

- 不实现数据库连接池
- 不实现外部 export / BI
- 不新增新的 audit truth source

## 测试策略

先写失败测试：

1. audit list 返回 items
2. detail 返回单资源
3. `correlation_id` filter 生效
4. 时间窗口 filter 生效
5. unknown event -> `404`

## 文档更新

同步更新：

- `README.md`
- `docs/architecture/AUDIT_LOG.md`
