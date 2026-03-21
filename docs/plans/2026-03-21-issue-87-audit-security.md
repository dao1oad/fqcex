# Issue 87 Audit Security Implementation Plan

## Goal

补齐审计保留、脱敏和访问控制约束文档，并用契约测试锁定。

## Steps

1. 新增失败契约测试，要求：
   - `SECURITY.md` 定义 retention/redaction/access control 约束
   - `AUDIT_LOG.md` 定义保留和脱敏规则
   - `force-resume-policy.md` 定义 operator evidence 的最小脱敏约束
2. 更新上述三份文档
3. 运行：
   - `py -m pytest tests/governance/test_audit_security_boundary_contract.py -q`
   - `py -m pytest tests -q`
