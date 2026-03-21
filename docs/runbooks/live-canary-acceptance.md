# Live Canary 部署验收手册

## 目标

这份手册只负责第 5 阶段 live deploy stack 的人工验收，不直接代表 Bybit / Binance / OKX 的真实 canary 已完成。

本手册的验收目标只有三项：

1. 目标主机上能长期运行 `control-plane`
2. 目标主机上能访问 `operator UI`
3. 进入 `#153` 前的部署前置条件都已收口

## 适用范围

- 目标主机：`38.60.236.47`
- 部署目录：`/srv/perp-platform`
- 仓库目录：`/srv/perp-platform/repo`
- env 文件：`/srv/perp-platform/deploy/.env`

## 前置条件

必须先确认：

- `docker` 可用
- `docker compose` 或 `docker-compose` 可用
- 仓库代码已同步到目标主机
- `/srv/perp-platform/state/kill-switch.flag` 存在
- `/srv/perp-platform/secrets/bybit.env` 存在
- `/srv/perp-platform/secrets/binance.env` 存在
- `/srv/perp-platform/secrets/okx.env` 存在

如果三家凭证文件缺任意一个，本手册仍可完成“部署栈验收”，但不得把结果表述为“真实 canary 已就绪可执行”。

## 环境变量最小检查

`/srv/perp-platform/deploy/.env` 至少应包含：

- `PERP_PLATFORM_ENVIRONMENT=live-canary`
- `CONTROL_PLANE_PORT=8080`
- `OPERATOR_UI_PORT=4173`
- `LIVE_CANARY_ENABLED=true`
- `LIVE_CANARY_ALLOWED_VENUES`
- `LIVE_CANARY_ALLOWED_INSTRUMENTS`
- `LIVE_CANARY_MAX_NOTIONAL_USD`
- `LIVE_CANARY_KILL_SWITCH_PATH`
- `BYBIT_CREDENTIALS_FILE`
- `BINANCE_CREDENTIALS_FILE`
- `OKX_CREDENTIALS_FILE`

## 部署步骤

在目标主机执行：

```sh
cd /srv/perp-platform/repo
sh deploy/scripts/preflight-live.sh /srv/perp-platform/deploy/.env
sh deploy/scripts/deploy.sh /srv/perp-platform/deploy/.env
```

## 健康检查

部署完成后必须逐项确认：

### 1. compose 服务状态

```sh
cd /srv/perp-platform/repo
docker-compose --env-file /srv/perp-platform/deploy/.env -f deploy/docker-compose.yml ps
```

预期：

- `control-plane` 为 `running`
- `operator-ui` 为 `running`

### 2. control-plane 健康接口

```sh
python3 - <<'PY'
import urllib.request
print(urllib.request.urlopen("http://127.0.0.1:8080/control-plane/v1/health").read().decode())
PY
```

预期：

- 返回 HTTP 200
- body 中包含健康 envelope

### 3. operator UI 可访问

```sh
python3 - <<'PY'
import urllib.request
print(urllib.request.urlopen("http://127.0.0.1:4173/").status)
PY
```

预期：

- 返回 `200`

### 4. 深链接可访问

```sh
python3 - <<'PY'
import urllib.request
print(urllib.request.urlopen("http://127.0.0.1:4173/actions").status)
PY
```

预期：

- 返回 `200`
- 证明 SPA 路由回退配置正确

## 人工验收记录

建议至少记录：

- 验收时间
- 验收人
- 当前 git commit
- `docker compose ps` 输出
- health 接口输出
- UI 首页截图或访问记录
- 当前 kill switch 状态
- 凭证文件是否到位

## 回滚

如需回滚到上一个镜像 tag：

```sh
cd /srv/perp-platform/repo
sh deploy/scripts/rollback.sh <previous-image-tag> /srv/perp-platform/deploy/.env
```

回滚后重复执行本手册中的健康检查。

## 进入 `#153` 前的最终 gate

只有下面都满足时，才允许继续 Bybit live canary：

- 部署栈已通过本手册验收
- Bybit 凭证文件已到位
- operator approval 已记录
- allowlist 只包含本轮批准范围
- kill switch 当前为 `armed=false`

如果任一条件不满足，必须停在部署验收阶段，不得声称已经进入真实 canary。
