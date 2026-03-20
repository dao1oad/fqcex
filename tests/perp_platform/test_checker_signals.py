from __future__ import annotations

from decimal import Decimal

import pytest

from tests.perp_platform.support.config import import_perp_platform_module


def _policy_result(*, stale: bool, diverged: bool):
    policies_module = import_perp_platform_module("perp_platform.checker.policies")
    instruments_module = import_perp_platform_module("perp_platform.domain.instruments")

    max_divergence_bps = Decimal("6.5") if diverged else Decimal("1.5")

    return policies_module.CheckerPolicyResult(
        venue=instruments_module.Venue.BYBIT,
        instrument_id="BTC-USDT-PERP",
        age_seconds=3.5 if stale else 1.0,
        stale=stale,
        bid_divergence_bps=max_divergence_bps,
        ask_divergence_bps=max_divergence_bps,
        max_divergence_bps=max_divergence_bps,
        diverged=diverged,
    )


@pytest.mark.parametrize(
    ("stale", "diverged", "expected_state_name", "expected_reason"),
    [
        (False, False, "LIVE", "checker_healthy"),
        (True, False, "DEGRADED", "checker_stale"),
        (False, True, "RESYNCING", "checker_top_of_book_diverged"),
        (True, True, "RESYNCING", "checker_top_of_book_diverged"),
    ],
)
def test_build_checker_supervisor_signal_maps_policy_result_to_supervisor_state(
    stale: bool,
    diverged: bool,
    expected_state_name: str,
    expected_reason: str,
) -> None:
    signals_module = import_perp_platform_module("perp_platform.checker.signals")
    supervisor_module = import_perp_platform_module("perp_platform.supervisor")

    signal = signals_module.build_checker_supervisor_signal(
        _policy_result(stale=stale, diverged=diverged)
    )

    assert signal.venue.value == "BYBIT"
    assert signal.instrument_id == "BTC-USDT-PERP"
    assert signal.suggested_state == supervisor_module.SupervisorState[expected_state_name]
    assert signal.reason == expected_reason
    assert signal.stale is stale
    assert signal.diverged is diverged
