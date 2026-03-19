# #83 Smoke 验证与 Rollback 设计

## 背景

当前仓库已经具备：

- 最小 Python 包与启动入口 [src/perp_platform/cli.py](D:/fqcex/.worktrees/issue-83-smoke-rollback/src/perp_platform/cli.py)
- 最小部署骨架 [deploy/Dockerfile](D:/fqcex/.worktrees/issue-83-smoke-rollback/deploy/Dockerfile)
- bootstrap / deploy 脚本 [deploy/scripts/bootstrap-server.sh](D:/fqcex/.worktrees/issue-83-smoke-rollback/deploy/scripts/bootstrap-server.sh) 与 [deploy/scripts/deploy.sh](D:/fqcex/.worktrees/issue-83-smoke-rollback/deploy/scripts/deploy.sh)
- 部署 runbook [docs/runbooks/deploy.md](D:/fqcex/.worktrees/issue-83-smoke-rollback/docs/runbooks/deploy.md)

但仍缺少：

- 一个可触发的最小 smoke workflow
- Playwright 工具基线
- 显式 tag 的 rollback 脚本
- rollback runbook

`#83` 的目标是在不引入真实交易演练、不扩成多环境矩阵的前提下，把“部署后最小可达性与最小回退路径”定义清楚。

## 目标

- 建立面向 `perp_platform` 的最小 smoke workflow
- 提供 Playwright e2e 工具基线和最小 fixture/spec
- 提供显式 previous tag 的 rollback 脚本
- 补齐 rollback runbook

## 非目标

- 不进行真实交易演练
- 不引入多环境端到端矩阵
- 不把当前 CLI 扩展成 HTTP 服务
- 不替代 Phase 3 的 dry run 或审计采集

## 方案比较

### 方案 A：shell 驱动 smoke 主链路 + Playwright 工具基线

- `cd.yml` 用 `workflow_dispatch`
- smoke 主链路先执行 `deploy/scripts/deploy.sh`
- Playwright 只验证最小 fixture/spec，作为后续更真实浏览器 smoke 的承接层
- rollback 使用显式 previous image tag

优点：

- 最符合当前应用形态
- 与 `#82` 部署骨架直接衔接
- 不会为了浏览器测试而虚构 HTTP 运行面

缺点：

- Playwright 当前验证的是工具链和 fixture，不是在线业务页面

### 方案 B：为 smoke 新增 HTTP 包装层

- 给现有 CLI 再包一层最小 HTTP health page

优点：

- Playwright 可以直接访问在线地址

缺点：

- 超出 `#83` 范围
- 等于在交付基座阶段偷带入新运行模型

### 方案 C：只写 rollback 脚本和文档，不做 Playwright

优点：

- 改动更小

缺点：

- 与 issue 明确列出的预期文件不一致
- 后续 smoke 基线仍然缺失

## 选型

采用方案 A。

理由：`#83` 的关键是定义最小 smoke 路径和回退路径，而不是为了浏览器测试改变当前产品形态。Playwright 先作为工具基线落地是最稳妥的收口方式。

## 设计

### CD Workflow

新增 [`.github/workflows/cd.yml`](D:/fqcex/.worktrees/issue-83-smoke-rollback/.github/workflows/cd.yml)：

- 只支持 `workflow_dispatch`
- 使用 `ubuntu-latest`
- 先复制 `deploy/.env.example` 到 `deploy/.env`
- 使用 `bash deploy/scripts/deploy.sh` 执行最小部署 smoke
- 使用 `actions/setup-node@v4` 和 Node `22`
- 执行 `npm ci`
- 执行 `npx playwright install chromium`
- 执行 `npm run smoke:e2e`

这里不自动绑定 `push` 或 `pull_request`。当前它是“手动触发的最小 smoke / rollback 基座”，不是持续自动部署。

### Playwright 基线

新增：

- [package.json](D:/fqcex/.worktrees/issue-83-smoke-rollback/package.json)
- [package-lock.json](D:/fqcex/.worktrees/issue-83-smoke-rollback/package-lock.json)
- [playwright.config.ts](D:/fqcex/.worktrees/issue-83-smoke-rollback/playwright.config.ts)
- [tests/e2e/fixtures/index.html](D:/fqcex/.worktrees/issue-83-smoke-rollback/tests/e2e/fixtures/index.html)
- [tests/e2e/smoke.spec.ts](D:/fqcex/.worktrees/issue-83-smoke-rollback/tests/e2e/smoke.spec.ts)

Playwright 只验证一个本地 `file://` fixture：

- 页面可以加载
- 标题和关键文本可见
- fixture 明确表述“deploy scaffold ready”

这不是线上业务 smoke，而是为后续真正的浏览器 smoke 留下最小可执行工具链。

### Git Ignore

更新 [`.gitignore`](D:/fqcex/.worktrees/issue-83-smoke-rollback/.gitignore)：

- `node_modules/`
- `playwright-report/`
- `test-results/`

这是 `#83` 的必要直接支持改动，避免 Node/Playwright 产物污染仓库。

### Rollback 脚本

新增 [deploy/scripts/rollback.sh](D:/fqcex/.worktrees/issue-83-smoke-rollback/deploy/scripts/rollback.sh)：

- 必须显式传入 previous image tag
- 允许可选 env 文件路径
- 读取当前 `deploy/.env`
- 生成临时 env，将 `PERP_PLATFORM_IMAGE_TAG` 替换为 previous tag
- 校验目标镜像在本地可用
- 使用 `docker compose ... run --rm --no-build perp-platform`

这里刻意避免自动推断 last-known-good。最小 rollback 必须是显式、可审计、可复核的。

### Rollback Runbook

新增 [docs/runbooks/rollback.md](D:/fqcex/.worktrees/issue-83-smoke-rollback/docs/runbooks/rollback.md)：

- 适用场景
- 回滚前提
- 如何执行 `rollback.sh <previous-tag>`
- 成功信号
- 回滚失败后的处置

### 测试策略

先写失败测试，验证稳定契约：

- `cd.yml` 存在 `workflow_dispatch`
- `cd.yml` 调用 `deploy.sh` 和 Playwright
- `package.json` 定义 `smoke:e2e`
- `playwright.config.ts` 指向 `tests/e2e`
- fixture/spec 存在
- `rollback.sh` 要求显式 tag，并使用 `--no-build`
- `rollback.md` 说明显式 previous tag 和失败处理
- `.gitignore` 包含 Node/Playwright 产物忽略项

如果本机 npm/Node 可用，则额外执行：

- `npm ci`
- `npx playwright install chromium`
- `npx playwright test tests/e2e/smoke.spec.ts`

如果 Docker 可用，则额外执行：

- `Copy-Item deploy/.env.example deploy/.env`
- `bash deploy/scripts/bootstrap-server.sh`
- `docker compose -f deploy/docker-compose.yml config`

`rollback.sh` 只做契约验证和脚本 review，不强制在本地真实回滚，因为当前并没有稳定的 previous image tag 基线。

## 风险与控制

- 风险：把 Playwright 误用成真实业务 smoke
  - 控制：fixture/spec 明确标注为 smoke tooling baseline
- 风险：rollback 脚本隐式修改主 env
  - 控制：使用临时 env 文件，不直接改写 `deploy/.env`
- 风险：自动化范围过大
  - 控制：只用 `workflow_dispatch`，不自动挂到 `push` 或 `pull_request`

## 验证

- `py -m pytest tests/governance/test_smoke_rollback_contract.py -q`
- `py -m pytest tests -q`
- `npm ci`
- `npx playwright install chromium`
- `npx playwright test tests/e2e/smoke.spec.ts`
- 如果 Docker 可用：`docker compose -f deploy/docker-compose.yml config`
