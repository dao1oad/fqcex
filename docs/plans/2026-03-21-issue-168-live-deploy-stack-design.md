# Issue 168 Live Deploy Stack Design

## 背景

`#149` 已经交付了 `live-canary` 的 env 契约、host preflight 和 runbook，但当前仓库的实际部署入口仍然只有：

- `deploy/docker-compose.yml` 中的 `python -m perp_platform`
- `src/perp_platform/cli.py` 中只打印 `bootstrap ready` 后退出

这意味着目标主机即使 preflight 通过，也只能跑一个瞬时 bootstrap 进程，不能形成可长期运行的 control-plane 和 operator UI 部署栈。该缺口会阻断 `#153`、`#154`、`#155` 的真实 canary 执行，因此需要新增 sibling issue 单独补齐。

## 目标

为 Phase 5 提供一个可长期运行的最小部署栈，使目标主机能够：

1. 启动 `control-plane` 后端服务
2. 启动 `operator UI` 静态前端
3. 通过健康检查验证服务可用
4. 按 runbook 完成部署验收

本设计不负责执行真实交易，也不把真实凭证写入仓库。

## 方案对比

### 方案 A：继续复用 `python -m perp_platform`

只在 `cli.py` 中把默认入口改成长期运行服务。

优点：

- 改动少

缺点：

- 把“bootstrap CLI”和“部署入口”混成一个接口
- 无法清晰表达 control-plane / operator UI 的部署职责
- 未来继续扩 live canary runner 时会再次挤压边界

结论：不推荐。

### 方案 B：单容器同时承载 API 与静态 UI

把 control-plane 和前端静态文件都塞进一个 Python 进程，统一由一个 HTTP server 对外提供。

优点：

- 对外只有一个服务

缺点：

- 需要继续扩展当前 control-plane server 的静态文件能力
- 把前端托管逻辑硬塞进控制平面实现
- 当前 UI 仍是静态 adapter，耦合不值得

结论：不推荐。

### 方案 C：双服务部署栈，推荐

使用两个长期运行服务：

- `control-plane`：Python 容器，运行 `python -m perp_platform.control_plane --host 0.0.0.0 --port 8080`
- `operator-ui`：独立静态容器，构建 `apps/control-plane-ui` 并通过 Nginx 提供静态页面

优点：

- 与当前仓库边界最一致
- 不修改 control-plane 的 truth boundary
- 部署模型清晰，便于运维与回滚
- 后续即使 UI 变成真实后端消费，也不需要推翻容器切分

缺点：

- 比单容器多一个服务

结论：推荐。

## 架构设计

### 服务划分

#### 1. control-plane

- 继续使用当前 Python 镜像
- 启动命令改为 `python -m perp_platform.control_plane --host 0.0.0.0 --port 8080`
- 对外暴露 `/healthz`、`/control-plane/v1/...`

#### 2. operator-ui

- 新增独立 `deploy/operator-ui.Dockerfile`
- 构建 `apps/control-plane-ui`
- 运行时使用 Nginx 托管 `dist/`
- 默认暴露 80，宿主映射到可配置端口

### compose 模型

`deploy/docker-compose.yml` 调整为两个长期运行服务：

- `control-plane`
- `operator-ui`

并增加：

- 显式端口映射
- 最小健康检查
- `depends_on`（仅限服务顺序，不表达业务真相）

### 部署脚本

`deploy/scripts/deploy.sh` 不再 `run --rm` 一个瞬时 bootstrap 容器，而是：

1. 执行 bootstrap/preflight
2. `docker compose build`
3. `docker compose up -d`
4. 运行健康检查

`rollback.sh` 也同步调整为回滚并重新拉起长期运行服务，而不是 `run --rm` 一次性容器。

## 验收手册

新增 `docs/runbooks/live-canary-acceptance.md`，覆盖：

1. 前置条件
2. 目标主机文件与凭证位置
3. 部署命令
4. 健康检查
5. operator UI 打开方式
6. control-plane 验证命令
7. rollback
8. 进入 `#153` 前的人工验收 checklist

该手册只负责“部署验收”，不替代真实 canary closeout。

## 测试策略

### Python / ops 测试

新增或补充契约测试，验证：

- compose 包含两个服务
- control-plane 命令不再使用 `python -m perp_platform`
- operator-ui 构建容器存在
- deploy/rollback 脚本改为长期运行服务模型

### 前端验证

继续复用：

- `npm --prefix apps/control-plane-ui run build`
- `npx playwright test tests/e2e`

### 远端部署验证

在 `38.60.236.47` 上验证：

1. `docker compose up -d`
2. `control-plane` 进程存活
3. `operator-ui` 进程存活
4. `/healthz` 返回 200
5. UI 页面能访问

## 风险与边界

- 本 issue 不声明真实 canary 已完成
- 本 issue 不要求真实凭证进仓库
- 即使部署栈完成，`#153` 仍然依赖真实 Bybit 凭证才能继续
- 当前 operator UI 仍然消费静态 fixture；这在 Phase 5 是允许的，只要手册明确它是人工验收入口，不是实时交易控制台
