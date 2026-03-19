# #28 Instrument ID and Market Enums Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为统一模型补齐最小 `InstrumentId` 值对象和 `Venue` / `InstrumentKind` 枚举，并用测试冻结 `BASE-QUOTE-PERP` 的 canonical 形式。

**Architecture:** 在 `src/perp_platform/domain/instruments.py` 中定义最小 domain 模型，用 `StrEnum` 表达市场与合约种类，用不可变 `dataclass` 表达 `InstrumentId`。通过 `make_perp_instrument_id()` 提供显式构造入口，并用 `tests/perp_platform/test_instruments.py` 验证 canonical 字符串和输入校验。直接支持文件只包括 `src/perp_platform/domain/__init__.py`。

**Tech Stack:** Python 3.12, `dataclasses`, `enum.StrEnum`, `pytest`.

---

### Task 1: 建立 instruments 契约测试

**Files:**
- Create: `tests/perp_platform/test_instruments.py`

**Step 1: Write the failing test**

```python
def test_make_perp_instrument_id_uses_canonical_format():
    instruments = import_perp_platform_module("perp_platform.domain.instruments")
    instrument_id = instruments.make_perp_instrument_id("BTC")
    assert str(instrument_id) == "BTC-USDT-PERP"
```

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/perp_platform/test_instruments.py -q`
Expected: FAIL because `perp_platform.domain.instruments` does not exist yet.

**Step 3: Commit**

```bash
git add tests/perp_platform/test_instruments.py
git commit -m "test: add instrument model contract"
```

### Task 2: 实现最小 domain 模型

**Files:**
- Create: `src/perp_platform/domain/__init__.py`
- Create: `src/perp_platform/domain/instruments.py`
- Modify: `tests/perp_platform/test_instruments.py`

**Step 1: Write minimal implementation**

```python
class Venue(StrEnum):
    BYBIT = "BYBIT"
```

```python
@dataclass(frozen=True)
class InstrumentId:
    base: str
    quote: str
    kind: InstrumentKind
```

**Step 2: Run targeted tests**

Run: `py -m pytest tests/perp_platform/test_instruments.py -q`
Expected: PASS

**Step 3: Run full tests**

Run: `py -m pytest tests -q`
Expected: PASS

**Step 4: Commit**

```bash
git add src/perp_platform/domain/__init__.py src/perp_platform/domain/instruments.py tests/perp_platform/test_instruments.py
git commit -m "feat: add instrument id model"
```

### Task 3: 边界回归检查

**Files:**
- Verify only: `src/perp_platform/domain/instruments.py`
- Verify only: `tests/perp_platform/test_instruments.py`
- Verify only: `docs/plans/2026-03-19-issue-28-instrument-id-market-enums-design.md`
- Verify only: `docs/plans/2026-03-19-issue-28-instrument-id-market-enums.md`

**Step 1: Verify diff scope**

Run: `git diff --stat main...HEAD`
Expected: 只包含 instruments 模型、测试和设计/计划文档，不包含 `base_qty`、OKX 换算或架构文档扩展。

**Step 2: Final verification**

Run: `py -m pytest tests -q`
Expected: PASS

**Step 3: Commit**

```bash
git add docs/plans/2026-03-19-issue-28-instrument-id-market-enums-design.md docs/plans/2026-03-19-issue-28-instrument-id-market-enums.md
git commit -m "docs: add issue 28 design and plan"
```
