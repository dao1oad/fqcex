# `#170` live deploy 硬化设计

## 目标

在不扩大到真实 canary 执行范围的前提下，修复 `#168` 合并后暴露出的部署安全与宿主兼容问题，使 live deploy stack 可以作为 `#153` 之前的稳定 gate。

## 已确认问题

1. `deploy/docker-compose.yml` 默认把 `control-plane` 与 `operator-ui` 暴露到宿主所有网卡，而 `control-plane` 当前存在未认证的 operator write API。
2. 常驻服务没有重启策略，不满足长期运行部署口径。
3. `rollback.sh` 只校验 Python 镜像，不校验 UI 镜像，回滚不完整。
4. `deploy.sh` / `rollback.sh` 依赖宿主 `python3`，但 bootstrap 阶段没有提前校验。
5. 在目标主机 `38.60.236.47` 上，独立版 `docker-compose 1.29.2` 对现有容器执行 `up -d --force-recreate` 会触发 `KeyError: 'ContainerConfig'`；先删除旧容器再 `up` 可成功，说明根因是 legacy compose 的 recreate 路径，而不是镜像或服务本身。
6. 验收手册把 compose 变体和端口写死，和脚本支持的可配置行为不一致。

## 设计决策

### 1. 默认仅绑定回环地址

- 为两个服务增加：
  - `CONTROL_PLANE_BIND_ADDRESS`
  - `OPERATOR_UI_BIND_ADDRESS`
- 默认值都设为 `127.0.0.1`
- 容器内应用仍监听 `0.0.0.0`，仅限制宿主端口暴露范围

### 2. 常驻服务增加重启策略

- `control-plane` / `operator-ui` 都使用 `restart: unless-stopped`
- 让主机重启或 Docker 守护进程重启后服务自动恢复

### 3. legacy compose 路径先删除旧容器再启动

- 保持 `docker compose` 插件路径不变
- 对 `docker-compose` 独立版路径，在 `up -d --force-recreate` 前执行：
  - `rm -sf control-plane operator-ui || true`
- 同样逻辑应用到 `rollback.sh`

### 4. 回滚同时校验 UI 镜像

- 回滚前同时校验：
  - `${IMAGE_REPO}:${PREVIOUS_TAG}`
  - `${IMAGE_REPO}-ui:${PREVIOUS_TAG}`

### 5. bootstrap 提前校验 `python3`

- `bootstrap-server.sh` 增加 `python3` 前置检查
- 文档把 `python3` 列入前置条件

### 6. 手册改成脚本口径

- 不再写死 `docker-compose`
- 明确 “`docker compose` 或 `docker-compose` 均可”
- 不再写死 `8080/4173`
- 用 env 读取后的端口举例

## 非目标

- 不给 control-plane 增加认证网关
- 不引入公网反向代理
- 不执行真实交易所 canary
- 不修改 `#153` 到 `#156` 的 live 验收逻辑

## 预期结果

- 远端主机 `38.60.236.47` 可基于 `main` 成功部署双服务
- 默认部署不会把未认证 write API 暴露到公网
- 验收手册可以直接用于人工部署验收
- `#153` 的 blocker 收敛为“真实凭证与 live 证据”，不再包含 deploy stack 缺陷
