# 回滚 Runbook

## 适用场景

- 最小 deploy smoke 失败
- 新的 `PERP_PLATFORM_IMAGE_TAG` 无法稳定启动
- 需要切回一个已知可用的 previous image tag

## 回滚前提

- 已安装 `docker`
- 已安装 `docker compose`
- `deploy/.env` 已存在
- previous image tag 对应镜像已在本地可用
- 已确认当前失败的 image tag 不应继续使用

## 执行步骤

运行：

```sh
deploy/scripts/rollback.sh <previous-image-tag>
```

如果需要显式传入 env 文件路径：

```sh
deploy/scripts/rollback.sh <previous-image-tag> deploy/.env
```

该脚本会：

- 读取当前 env
- 生成临时 env 并覆盖 `PERP_PLATFORM_IMAGE_TAG`
- 校验 previous image tag 对应镜像已在本地存在
- 通过 `docker compose ... run --rm --no-build perp-platform` 执行最小回退

## 成功信号

最小成功信号是容器以退出码 `0` 结束，并输出类似：

```text
perp-platform bootstrap ready [dev]
```

## 失败处置

- 如果脚本提示目标镜像不存在，先停止继续 rollout，不要强行回滚到未知镜像
- 如果回滚执行失败，保留日志并升级为人工处置
- 在失败原因未解释清楚前，不继续 smoke 或任何后续交付动作
