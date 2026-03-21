# Issue 86 Audit Storage Boundary Implementation Plan

## Goal

补齐 audit storage 与 query boundary 文档，并用契约测试锁定。

## Steps

1. 新增失败契约测试，要求：
   - `AUDIT_LOG.md` 定义 Persistence Boundary 和 Query Boundary
   - `DATA_MODEL.md` 定义 `audit_events` 归属
   - `control-plane-api.md` 提供只读 audit query surface
2. 更新上述三份文档
3. 运行：
   - `py -m pytest tests/governance/test_audit_storage_boundary_contract.py -q`
   - `py -m pytest tests -q`
