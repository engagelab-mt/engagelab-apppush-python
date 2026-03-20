"""Alias service and data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

@dataclass
class AliasStatusGetResult:
    registration_ids: Optional[List[str]] = None


# ---------------------------------------------------------------------------
# Service
# ---------------------------------------------------------------------------

class AliasService:
    """Alias management service — ``client.alias``."""

    def __init__(self, client: Any) -> None:
        self._client = client

    def get(
        self,
        alias: str,
        platforms: Optional[List[str]] = None,
    ) -> AliasStatusGetResult:
        """Return registration IDs associated with an alias.

        ``GET /v4/aliases/{alias}``
        """
        query: Optional[Dict[str, str]] = None
        if platforms:
            query = {"platform": ",".join(platforms)}
        return self._client._get(
            f"/v4/aliases/{alias}",
            query=query,
            result_cls=AliasStatusGetResult,
        )

    def delete(
        self,
        alias: str,
        platforms: Optional[List[str]] = None,
    ) -> None:
        """Delete an alias binding for given platforms.

        ``DELETE /v4/aliases/{alias}``
        """
        query: Optional[Dict[str, str]] = None
        if platforms:
            query = {"platform": ",".join(platforms)}
        self._client._delete(f"/v4/aliases/{alias}", query=query)
