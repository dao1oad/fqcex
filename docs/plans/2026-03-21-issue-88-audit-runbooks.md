# Issue 88 Audit Runbooks Implementation Plan

## Goal

补齐审计 runbook 与验收清单，并让 incident / force-resume 两个入口都引用它。

## Steps

1. 新增失败契约测试，要求：
   - `audit-checklist.md` 存在并包含四个操作块
   - `incident-template.md` 与 `force-resume-policy.md` 都引用审计清单
2. 创建 `docs/runbooks/audit-checklist.md`
3. 更新现有两个 runbook
4. 运行：
   - `py -m pytest tests/governance/test_audit_runbook_contract.py -q`
   - `py -m pytest tests -q`
