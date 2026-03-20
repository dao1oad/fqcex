from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from ..domain import Venue
from .models import CheckerTopOfBook, _to_decimal

_BASIS_POINTS = Decimal("10000")


@dataclass(frozen=True)
class CheckerReferenceTopOfBook:
    venue: Venue
    instrument_id: str
    bid_price: Decimal
    ask_price: Decimal
    observed_timestamp: float

    def __post_init__(self) -> None:
        instrument_id = self.instrument_id.strip().upper()
        if not instrument_id.endswith("-USDT-PERP"):
            raise ValueError(
                "instrument_id must stay within the canonical *-USDT-PERP Phase 1 boundary"
            )
        if self.observed_timestamp <= 0:
            raise ValueError("observed_timestamp must be greater than 0")

        object.__setattr__(self, "instrument_id", instrument_id)
        object.__setattr__(
            self,
            "bid_price",
            _to_decimal(self.bid_price, field_name="bid_price"),
        )
        object.__setattr__(
            self,
            "ask_price",
            _to_decimal(self.ask_price, field_name="ask_price"),
        )


@dataclass(frozen=True)
class CheckerPolicyThresholds:
    max_staleness_seconds: float
    max_divergence_bps: Decimal

    def __post_init__(self) -> None:
        if self.max_staleness_seconds <= 0:
            raise ValueError("max_staleness_seconds must be greater than 0")

        object.__setattr__(
            self,
            "max_divergence_bps",
            _to_decimal(self.max_divergence_bps, field_name="max_divergence_bps"),
        )


DEFAULT_CHECKER_POLICY_THRESHOLDS = CheckerPolicyThresholds(
    max_staleness_seconds=3.0,
    max_divergence_bps=Decimal("5.0"),
)


@dataclass(frozen=True)
class CheckerPolicyResult:
    venue: Venue
    instrument_id: str
    age_seconds: float
    stale: bool
    bid_divergence_bps: Decimal
    ask_divergence_bps: Decimal
    max_divergence_bps: Decimal
    diverged: bool


def _basis_points_delta(left: Decimal, right: Decimal) -> Decimal:
    return abs(left - right) / right * _BASIS_POINTS


def evaluate_checker_policies(
    checker_top_of_book: CheckerTopOfBook,
    reference_top_of_book: CheckerReferenceTopOfBook,
    *,
    now_timestamp: float,
    thresholds: CheckerPolicyThresholds = DEFAULT_CHECKER_POLICY_THRESHOLDS,
) -> CheckerPolicyResult:
    if checker_top_of_book.venue.value != reference_top_of_book.venue.value:
        raise ValueError("checker and reference top-of-book must describe the same venue and instrument")
    if checker_top_of_book.instrument_id != reference_top_of_book.instrument_id:
        raise ValueError("checker and reference top-of-book must describe the same venue and instrument")
    if now_timestamp < checker_top_of_book.receipt_timestamp:
        raise ValueError("now_timestamp must not be earlier than checker receipt_timestamp")

    age_seconds = now_timestamp - checker_top_of_book.receipt_timestamp
    stale = age_seconds > thresholds.max_staleness_seconds

    bid_divergence_bps = _basis_points_delta(
        checker_top_of_book.bid_price,
        reference_top_of_book.bid_price,
    )
    ask_divergence_bps = _basis_points_delta(
        checker_top_of_book.ask_price,
        reference_top_of_book.ask_price,
    )
    max_divergence_bps = max(bid_divergence_bps, ask_divergence_bps)

    return CheckerPolicyResult(
        venue=checker_top_of_book.venue,
        instrument_id=checker_top_of_book.instrument_id,
        age_seconds=age_seconds,
        stale=stale,
        bid_divergence_bps=bid_divergence_bps,
        ask_divergence_bps=ask_divergence_bps,
        max_divergence_bps=max_divergence_bps,
        diverged=max_divergence_bps > thresholds.max_divergence_bps,
    )
