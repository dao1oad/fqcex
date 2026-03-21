# Issue 88 Audit Runbooks Design

## Goal

把前面 Phase 4 的审计设计收口成一份操作手册和验收清单，供操作员执行审计核对与 closeout。

## Scope

- 创建 `docs/runbooks/audit-checklist.md`
- 更新 `docs/runbooks/incident-template.md`
- 更新 `docs/runbooks/force-resume-policy.md`
- 新增一个 governance contract test

## Recommendation

把 `#88` 收口为四个最小操作块：

- manual unblock pre-check
- event replay
- evidence retention
- audit reconciliation / closeout
