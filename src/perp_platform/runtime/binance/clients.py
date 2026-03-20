from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class BinanceStreamClient:
    channel: Literal["public", "private"]
    url: str
    market: str
    requires_auth: bool


@dataclass(frozen=True)
class BinanceExecutionClient:
    rest_base_url: str
    market: str
    settle_asset: str
    api_key_present: bool
    api_secret_present: bool
