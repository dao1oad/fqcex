# #82 Minimal Deploy Scripts Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 `perp_platform` 建立单机、单环境、单服务的最小容器化与部署脚本骨架，并补齐最小部署 runbook。

**Architecture:** 通过 `deploy/` 目录集中放置 `.env` 示例、Dockerfile、compose 文件和 shell 脚本；部署流程由 `bootstrap-server.sh` 做前置检查，由 `deploy.sh` 调用 `docker compose build` 与 `docker compose run --rm` 执行最小启动。使用治理测试验证文件和关键命令契约，不引入真实生产发布或回滚逻辑。

**Tech Stack:** Docker, Docker Compose, POSIX shell, Markdown, Python 3.12, `pytest`.

---

### Task 1: 建立部署契约测试

**Files:**
- Create: `tests/governance/test_deploy_contract.py`

**Step 1: Write the failing test**

```python
from pathlib import Path


def test_deploy_files_exist():
    assert Path("deploy/Dockerfile").exists()
```

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/governance/test_deploy_contract.py -q`
Expected: FAIL because the `deploy/` scaffold does not exist yet.

**Step 3: Commit**

```bash
git add tests/governance/test_deploy_contract.py
git commit -m "test: add deploy contract"
```

### Task 2: 落地最小部署骨架

**Files:**
- Create: `deploy/.env.example`
- Create: `deploy/Dockerfile`
- Create: `deploy/docker-compose.yml`
- Create: `deploy/scripts/bootstrap-server.sh`
- Create: `deploy/scripts/deploy.sh`
- Create: `docs/runbooks/deploy.md`
- Modify: `tests/governance/test_deploy_contract.py`

**Step 1: Write minimal implementation**

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . /app
RUN python -m pip install --upgrade pip && python -m pip install .
CMD ["python", "-m", "perp_platform"]
```

```sh
docker compose --env-file deploy/.env -f deploy/docker-compose.yml build
docker compose --env-file deploy/.env -f deploy/docker-compose.yml run --rm perp-platform
```

**Step 2: Run targeted tests**

Run: `py -m pytest tests/governance/test_deploy_contract.py -q`
Expected: PASS

**Step 3: Run full tests**

Run: `py -m pytest tests -q`
Expected: PASS

**Step 4: Commit**

```bash
git add deploy/.env.example deploy/Dockerfile deploy/docker-compose.yml deploy/scripts/bootstrap-server.sh deploy/scripts/deploy.sh docs/runbooks/deploy.md tests/governance/test_deploy_contract.py
git commit -m "ops: add minimal deploy scaffold"
```

### Task 3: 做本地部署配置验证

**Files:**
- Verify only: `deploy/docker-compose.yml`
- Verify only: `deploy/scripts/bootstrap-server.sh`
- Verify only: `deploy/scripts/deploy.sh`
- Verify only: `docs/runbooks/deploy.md`

**Step 1: Check whether Docker is available**

Run: `docker --version`
Expected: Either a version string or a clear "command not found" style failure.

**Step 2: If Docker is available, validate compose config**

Run: `docker compose -f deploy/docker-compose.yml --env-file deploy/.env.example config`
Expected: Valid rendered config.

**Step 3: Re-run full tests**

Run: `py -m pytest tests -q`
Expected: PASS

**Step 4: Commit**

```bash
git add docs/plans/2026-03-19-issue-82-minimal-deploy-scripts-design.md docs/plans/2026-03-19-issue-82-minimal-deploy-scripts.md
git commit -m "docs: add issue 82 design and plan"
```
