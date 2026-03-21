# Issue 145 控制平面 HTTP Skeleton 设计

## 背景

Phase 4 已经冻结了 control-plane API surface，但当前仓库还没有任何可运行的 control-plane HTTP 服务。`#145` 只负责搭起最小只读服务骨架，为后续 `#146-#148` 提供稳定挂点。

## 方案比较

### 方案 A：引入新的 Web 框架

优点：

- 路由和序列化功能成熟

缺点：

- 当前仓库没有相应依赖
- 对 `#145` 来说是明显超配

### 方案 B：标准库 `http.server` + 纯函数 app/router

优点：

- 无新增依赖
- 最适合最小 skeleton
- 后续可继续扩展 `GET` 查询与 operator actions

缺点：

- 需要自己处理少量 JSON / routing 细节

### 方案 C：只做纯函数，不提供真实 HTTP 入口

优点：

- 测试最简单

缺点：

- 不满足 issue 对“可运行服务骨架”的要求

## 推荐方案

采用方案 B。

## 设计

新增 `perp_platform.control_plane` 包，包含：

- `app.py`
  - `ControlPlaneApp`
  - 纯函数式 request dispatch
  - 统一 response / error envelope
- `server.py`
  - `ThreadingHTTPServer` 入口
  - `serve_control_plane(host, port)`
- `__main__.py`
  - 允许 `python -m perp_platform.control_plane`

最小只实现：

- `GET /control-plane/v1/health`
- `GET /control-plane/v1/readiness`

返回约束：

- 成功：`data` + `meta` + `errors=[]`
- 失败：`data=null` + `meta` + `errors=[...]`

未知路径返回：

- `404`
- `code = "not_found"`

## 非目标

- 不实现业务读模型查询
- 不实现 operator actions
- 不实现 auth / RBAC
- 不引入新的 truth source

## 测试策略

先写失败测试：

1. `health` 返回 200 和 success envelope
2. `readiness` 返回 200 和 success envelope
3. 未知路径返回 404 和 error envelope
4. 真实 HTTP server 能对 `health` 做最小响应

## 文档更新

同步更新：

- `README.md`，补充最小 control-plane 启动方式
