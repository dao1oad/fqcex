# #29 Quantity Normalization Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为统一模型补齐 `base_qty` 真相字段的最小代码表达，覆盖 Bybit / Binance 直通和 OKX 张数到 `base_qty` 的换算。

**Architecture:** 在 `src/perp_platform/domain/quantity.py` 中定义最小 `ExchangeQtyKind` 枚举、`NormalizedQuantity` 值对象和两个数量函数，全部使用 `Decimal`，并显式拒绝 `float`。测试集中在 `tests/perp_platform/test_quantity.py`，只冻结文档中已经明确的数量语义，不扩展到文档更新或运行时接线。

**Tech Stack:** Python 3.12, `decimal.Decimal`, `dataclasses`, `enum.StrEnum`, `pytest`.

---

### Task 1: 建立数量归一化契约测试

**Files:**
- Create: `tests/perp_platform/test_quantity.py`

**Step 1: Write the failing test**

```python
def test_bybit_quantity_normalizes_to_base_qty():
    quantity = import_perp_platform_module("perp_platform.domain.quantity")
    normalized = quantity.normalize_quantity(Venue.BYBIT, "1.5")
    assert normalized.base_qty == Decimal("1.5")
```

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/perp_platform/test_quantity.py -q`
Expected: FAIL because `perp_platform.domain.quantity` does not exist yet.

**Step 3: Commit**

```bash
git add tests/perp_platform/test_quantity.py
git commit -m "test: add quantity normalization contract"
```

### Task 2: 实现最小数量模型

**Files:**
- Create: `src/perp_platform/domain/quantity.py`
- Modify: `src/perp_platform/domain/__init__.py`
- Modify: `tests/perp_platform/test_quantity.py`

**Step 1: Write minimal implementation**

```python
class ExchangeQtyKind(StrEnum):
    BASE = "BASE"
    CONTRACTS = "CONTRACTS"
```

```python
@dataclass(frozen=True)
class NormalizedQuantity:
    base_qty: Decimal
```

**Step 2: Run targeted tests**

Run: `py -m pytest tests/perp_platform/test_quantity.py -q`
Expected: PASS

**Step 3: Run full tests**

Run: `py -m pytest tests -q`
Expected: PASS

**Step 4: Commit**

```bash
git add src/perp_platform/domain/__init__.py src/perp_platform/domain/quantity.py tests/perp_platform/test_quantity.py
git commit -m "feat: add quantity normalization model"
```

### Task 3: 边界回归检查

**Files:**
- Verify only: `src/perp_platform/domain/quantity.py`
- Verify only: `tests/perp_platform/test_quantity.py`
- Verify only: `docs/plans/2026-03-19-issue-29-quantity-normalization-design.md`
- Verify only: `docs/plans/2026-03-19-issue-29-quantity-normalization.md`

**Step 1: Verify diff scope**

Run: `git diff --stat main...HEAD`
Expected: 只包含 quantity 模型、测试和设计/计划文档，不包含 `DATA_MODEL.md` 或 runtime 接线。

**Step 2: Final verification**

Run: `py -m pytest tests -q`
Expected: PASS

**Step 3: Commit**

```bash
git add docs/plans/2026-03-19-issue-29-quantity-normalization-design.md docs/plans/2026-03-19-issue-29-quantity-normalization.md
git commit -m "docs: add issue 29 design and plan"
```
