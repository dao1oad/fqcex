# Issue 64 Dry Run Audit Design

## Goal

补齐 dry-run operator checklist 与审计采集工具，确保演练中的人工动作和结果能被统一记录。

## Recommendation

- 新增 `scripts/capture_dry_run_audit.py`，输出结构化审计记录
- 在 `deploy.md` 中增加 dry-run preflight / operator checklist
- 在 `rollback.md` 中增加 dry-run rollback 时的审计留痕要求

## Scope

审计脚本输入：

- `--operator`
- `--stage`
- `--venue`
- `--instrument-id`
- `--action`
- `--result`
- `--evidence-path`
- `--output`

输出 JSON 审计记录，便于后续 `#65/#66` 汇总。
