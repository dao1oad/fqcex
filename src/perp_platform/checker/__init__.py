"""Independent market data checker package."""

from .bootstrap import CheckerBootstrapResult, CheckerSubscriptionTarget, bootstrap_checker
from .config import CheckerConfig, load_checker_config
from .feeds import (
    CheckerExchangeFeed,
    CheckerFeedRuntime,
    build_checker_exchange_feeds,
    build_checker_feed_handler,
    normalize_checker_ticker,
    prime_checker_symbol_mappings,
)
from .models import CheckerTopOfBook
from .policies import (
    DEFAULT_CHECKER_POLICY_THRESHOLDS,
    CheckerPolicyResult,
    CheckerPolicyThresholds,
    CheckerReferenceTopOfBook,
    evaluate_checker_policies,
)
from .signals import (
    CHECKER_HEALTHY_REASON,
    CHECKER_STALE_REASON,
    CHECKER_TOP_OF_BOOK_DIVERGED_REASON,
    CheckerSupervisorSignal,
    build_checker_supervisor_signal,
)

__all__ = [
    "CheckerBootstrapResult",
    "CheckerConfig",
    "CheckerExchangeFeed",
    "CheckerFeedRuntime",
    "CheckerPolicyResult",
    "CheckerPolicyThresholds",
    "CheckerReferenceTopOfBook",
    "CheckerSupervisorSignal",
    "CheckerSubscriptionTarget",
    "CheckerTopOfBook",
    "CHECKER_HEALTHY_REASON",
    "CHECKER_STALE_REASON",
    "CHECKER_TOP_OF_BOOK_DIVERGED_REASON",
    "DEFAULT_CHECKER_POLICY_THRESHOLDS",
    "bootstrap_checker",
    "build_checker_supervisor_signal",
    "build_checker_exchange_feeds",
    "build_checker_feed_handler",
    "evaluate_checker_policies",
    "load_checker_config",
    "normalize_checker_ticker",
    "prime_checker_symbol_mappings",
]
