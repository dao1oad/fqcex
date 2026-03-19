# #82 最小容器化与部署脚本设计

## 背景

当前仓库已经具备：

- 最小 Python 包与入口点 [pyproject.toml](D:/fqcex/.worktrees/issue-82-minimal-deploy-scripts/pyproject.toml)
- 可执行 CLI 入口 [src/perp_platform/cli.py](D:/fqcex/.worktrees/issue-82-minimal-deploy-scripts/src/perp_platform/cli.py)
- 配置加载契约 [src/perp_platform/config.py](D:/fqcex/.worktrees/issue-82-minimal-deploy-scripts/src/perp_platform/config.py)
- 最小 CI 护栏 [ci.yml](D:/fqcex/.worktrees/issue-82-minimal-deploy-scripts/.github/workflows/ci.yml)

但仓库仍没有任何部署骨架：

- 没有 `deploy/` 目录
- 没有 `.env` 示例
- 没有 Docker 构建入口
- 没有最小部署脚本或部署 runbook

`#82` 的目标是补齐这些最小交付基座，为后续 `#83` 的 smoke / rollback 提供前置条件。

## 目标

- 建立单机、单环境、单服务的最小容器化骨架
- 提供最小部署所需的环境变量说明
- 提供可审计、可重复运行的 bootstrap / deploy 脚本
- 通过 runbook 固定最小部署步骤与回退前置说明

## 非目标

- 不引入 HA、多环境编排或多账户部署策略
- 不把当前 CLI 包装成虚假的长驻 HTTP 服务
- 不实现正式生产发布流水线
- 不引入交易所特定参数、账号密钥或 venue 配置

## 方案比较

### 方案 A：单次运行型容器 + `docker compose run`

- 使用 `deploy/Dockerfile` 构建镜像
- 使用 `deploy/docker-compose.yml` 定义单个 `perp-platform` 服务
- 默认命令为 `python -m perp_platform`
- `deploy/scripts/deploy.sh` 执行 `docker compose build` 和 `docker compose run --rm`

优点：

- 完全符合当前应用形态
- 不需要额外引入并不存在的服务层
- 能直接作为 `#83` smoke 的真实前置

缺点：

- 部署成功信号是“成功启动并 0 退出”，不是长驻存活

### 方案 B：强制包装成长驻服务

- 例如外加循环脚本或伪 HTTP health server

优点：

- 表面上更接近传统容器部署

缺点：

- 明显改变当前应用运行模型
- 会把 `#82` 扩展成“新增服务接口”

### 方案 C：只交文档和空脚本

优点：

- 改动最小

缺点：

- 不能真实支撑后续 smoke / dry run
- 验收信号过弱

## 选型

采用方案 A。

理由：当前应用只有最小 CLI 启动链路，最合理的“部署”定义是把这个链路容器化并脚本化，而不是提前发明新的服务模型。

## 设计

### 容器模型

新增 [deploy/Dockerfile](D:/fqcex/.worktrees/issue-82-minimal-deploy-scripts/deploy/Dockerfile)：

- 基于 Python `3.12-slim`
- 工作目录设为 `/app`
- 复制仓库内容
- 使用 `python -m pip install --upgrade pip`
- 使用 `python -m pip install .`
- 默认命令为 `python -m perp_platform`

这里刻意使用 `pip install .`，而不是 `-e .`。CI 已覆盖 editable 安装；部署镜像应验证可构建的发布安装链路。

### Compose 模型

新增 [deploy/docker-compose.yml](D:/fqcex/.worktrees/issue-82-minimal-deploy-scripts/deploy/docker-compose.yml)：

- 定义单个服务 `perp-platform`
- 读取 `deploy/.env`
- 使用镜像名 `PERP_PLATFORM_IMAGE_REPO:PERP_PLATFORM_IMAGE_TAG`
- `build` 指向 `deploy/Dockerfile`
- 默认执行 `python -m perp_platform`

不使用 `up -d` 作为主路径。当前最小进程是“启动后输出 bootstrap 并退出”，所以推荐运行方式由 `deploy.sh` 驱动 `docker compose run --rm perp-platform`。

### 环境变量契约

新增 [deploy/.env.example](D:/fqcex/.worktrees/issue-82-minimal-deploy-scripts/deploy/.env.example)：

- `PERP_PLATFORM_APP_NAME`
- `PERP_PLATFORM_ENVIRONMENT`
- `PERP_PLATFORM_LOG_LEVEL`
- `PERP_PLATFORM_IMAGE_REPO`
- `PERP_PLATFORM_IMAGE_TAG`

只保留应用启动和镜像标识所需的最小变量，不提前引入 venue/account/secrets。

### 脚本职责

新增 [deploy/scripts/bootstrap-server.sh](D:/fqcex/.worktrees/issue-82-minimal-deploy-scripts/deploy/scripts/bootstrap-server.sh)：

- 校验 `docker` 与 `docker compose` 可用
- 创建最小目录，例如 `deploy/state`
- 检查 `deploy/.env` 是否存在；若不存在则提示从 `.env.example` 复制

新增 [deploy/scripts/deploy.sh](D:/fqcex/.worktrees/issue-82-minimal-deploy-scripts/deploy/scripts/deploy.sh)：

- 调用 `bootstrap-server.sh`
- 基于 `deploy/docker-compose.yml` 执行 `docker compose build`
- 执行 `docker compose run --rm perp-platform`
- 输出清晰的启动/失败提示

脚本目标是显式、幂等、可审计，不负责系统级依赖安装。

### Runbook

新增 [docs/runbooks/deploy.md](D:/fqcex/.worktrees/issue-82-minimal-deploy-scripts/docs/runbooks/deploy.md)：

- 部署前提
- `.env` 配置方法
- bootstrap 步骤
- deploy 步骤
- 成功信号
- 失败时的最小回退前置说明

这里的回退说明只做前置约束，例如保留上一个 image tag，真正的 rollback 脚本留给 `#83`。

### 测试策略

先写失败测试，验证稳定契约：

- `deploy/` 预期文件存在
- `.env.example` 包含约定的环境变量
- `Dockerfile` 安装并运行 `perp_platform`
- `docker-compose.yml` 定义 `perp-platform` 服务和 env 文件
- `bootstrap-server.sh` / `deploy.sh` 包含关键命令
- `docs/runbooks/deploy.md` 说明部署前提、步骤和成功信号

如果本机 Docker 可用，再额外执行：

- `docker compose -f deploy/docker-compose.yml config`

如果 Docker 不可用，保留为人工/CI 后续验证项，不阻塞本 issue。

## 风险与控制

- 风险：部署模型和实际应用形态不一致
  - 控制：坚持单次运行型容器，不发明长驻服务
- 风险：脚本不可审计或隐式过多
  - 控制：只做显式检查、构建和运行，不自动安装系统依赖
- 风险：把 `#83` 的 rollback 逻辑偷渡进来
  - 控制：本 issue 只写最小回退前置说明，不实现 rollback 脚本

## 验证

- `py -m pytest tests/governance/test_deploy_contract.py -q`
- `py -m pytest tests -q`
- 如果本机 Docker 可用：`docker compose -f deploy/docker-compose.yml config`
