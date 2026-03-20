from tests.perp_platform.support.config import import_perp_platform_module


def _projection_module():
    return import_perp_platform_module("perp_platform.supervisor.projection")


def _domain_module():
    return import_perp_platform_module("perp_platform.domain.instruments")


def _make_btc_perp(domain):
    return domain.make_perp_instrument_id("BTC")


def test_venue_live_and_degraded_allow_open_and_reduce() -> None:
    projection = _projection_module()
    domain = _domain_module()

    live = projection.project_venue_tradeability(
        domain.Venue.BYBIT,
        projection.SupervisorState.LIVE,
        reason="healthy_streams",
    )
    degraded = projection.project_venue_tradeability(
        domain.Venue.BYBIT,
        projection.SupervisorState.DEGRADED,
        reason="public_stream_degraded",
    )

    assert live.allow_open is True
    assert live.allow_reduce is True
    assert degraded.allow_open is True
    assert degraded.allow_reduce is True


def test_venue_resyncing_and_reduce_only_deny_open_but_allow_reduce() -> None:
    projection = _projection_module()
    domain = _domain_module()

    resyncing = projection.project_venue_tradeability(
        domain.Venue.BINANCE,
        projection.SupervisorState.RESYNCING,
        reason="public_stream_resync_required",
    )
    reduce_only = projection.project_venue_tradeability(
        domain.Venue.BINANCE,
        projection.SupervisorState.REDUCE_ONLY,
        reason="private_stream_lagging",
    )

    assert resyncing.allow_open is False
    assert resyncing.allow_reduce is True
    assert reduce_only.allow_open is False
    assert reduce_only.allow_reduce is True


def test_venue_blocked_denies_open_and_reduce() -> None:
    projection = _projection_module()
    domain = _domain_module()

    blocked = projection.project_venue_tradeability(
        domain.Venue.OKX,
        projection.SupervisorState.BLOCKED,
        reason="reconciliation_failed",
    )

    assert blocked.allow_open is False
    assert blocked.allow_reduce is False


def test_instrument_without_override_inherits_venue_projection() -> None:
    projection = _projection_module()
    domain = _domain_module()

    venue_projection = projection.project_venue_tradeability(
        domain.Venue.BYBIT,
        projection.SupervisorState.DEGRADED,
        reason="public_stream_degraded",
    )

    instrument_projection = projection.project_instrument_tradeability(
        venue_projection,
        _make_btc_perp(domain),
    )

    assert instrument_projection.effective_state == projection.SupervisorState.DEGRADED
    assert instrument_projection.allow_open is True
    assert instrument_projection.allow_reduce is True
    assert instrument_projection.reason == "public_stream_degraded"


def test_stricter_instrument_override_takes_effect() -> None:
    projection = _projection_module()
    domain = _domain_module()

    venue_projection = projection.project_venue_tradeability(
        domain.Venue.OKX,
        projection.SupervisorState.DEGRADED,
        reason="public_stream_degraded",
    )

    instrument_projection = projection.project_instrument_tradeability(
        venue_projection,
        _make_btc_perp(domain),
        instrument_state=projection.SupervisorState.REDUCE_ONLY,
        reason="instrument_private_lagging",
    )

    assert instrument_projection.effective_state == projection.SupervisorState.REDUCE_ONLY
    assert instrument_projection.allow_open is False
    assert instrument_projection.allow_reduce is True
    assert instrument_projection.reason == "instrument_private_lagging"


def test_less_strict_instrument_override_cannot_relax_stricter_venue() -> None:
    projection = _projection_module()
    domain = _domain_module()

    venue_projection = projection.project_venue_tradeability(
        domain.Venue.BINANCE,
        projection.SupervisorState.REDUCE_ONLY,
        reason="private_stream_lagging",
    )

    instrument_projection = projection.project_instrument_tradeability(
        venue_projection,
        _make_btc_perp(domain),
        instrument_state=projection.SupervisorState.DEGRADED,
        reason="instrument_nominal",
    )

    assert instrument_projection.effective_state == projection.SupervisorState.REDUCE_ONLY
    assert instrument_projection.allow_open is False
    assert instrument_projection.allow_reduce is True
    assert instrument_projection.reason == "instrument_nominal"
