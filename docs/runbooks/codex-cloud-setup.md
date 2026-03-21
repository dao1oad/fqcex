# Codex Cloud Setup

## 目标

为 Codex cloud 和 Linux/Bash 环境提供统一的仓库 setup 与 verification 入口，不改变当前 Phase 1 的交易与恢复边界。

## Setup

优先使用仓库内 Bash 入口：

```bash
bash scripts/codex_cloud_setup.sh
```

该脚本当前只执行：

```bash
python -m pip install --upgrade pip
python -m pip install -e '.[test]'
```

## Verification

Codex cloud / Linux-Bash 默认验证命令：

```bash
python -m pytest tests -q
```

如需先做治理层快速检查，可先运行：

```bash
python -m pytest tests/governance -q
```

## Notes

- `scripts/project_context.ps1` 仍可用于本地 Windows 终端快速概览，但它不是 Codex cloud 的默认入口。
- environment、secrets 与网络访问边界见 [codex-cloud-security.md](codex-cloud-security.md)。
- 两阶段运行模型与默认网络边界见 [../architecture/CODEX_CLOUD_BOUNDARIES.md](../architecture/CODEX_CLOUD_BOUNDARIES.md)。
- 本 runbook 只覆盖 setup 与 verification 入口，不覆盖 orchestrator 云端状态模型。
