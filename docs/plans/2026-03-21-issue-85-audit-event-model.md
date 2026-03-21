# Issue 85 Audit Event Model Implementation Plan

## Goal

补齐审计事件模型定义，并让 incident 模板开始引用统一的审计上下文。

## Steps

1. 新增失败契约测试，要求：
   - `AUDIT_LOG.md` 定义三类事件、最小字段和 truth boundary
   - `incident-template.md` 包含 `correlation_id` 和 `audit_event_ids`
2. 创建 `docs/architecture/AUDIT_LOG.md`
3. 更新 `docs/runbooks/incident-template.md`
4. 运行：
   - `py -m pytest tests/governance/test_audit_event_model_contract.py -q`
   - `py -m pytest tests -q`
