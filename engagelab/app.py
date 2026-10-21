"""Application-level API service."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class AppVipStatusResult:
    vip_status: int = 0
    vip_end_time: int = 0


class AppService:
    """Application service — ``client.app``."""

    def __init__(self, client: Any) -> None:
        self._client = client

    def get_vip_status(self) -> AppVipStatusResult:
        """Return the application's VIP status.

        ``GET /v4/app/vip/status``
        """
        return self._client._get(
            "/v4/app/vip/status", result_cls=AppVipStatusResult
        )
