"""Status (statistics) service and data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

@dataclass
class UserStatusPlatform:
    new: int = 0
    active: int = 0
    online: int = 0


@dataclass
class UserStatusItem:
    time: Optional[str] = None
    android: Optional[Dict[str, Any]] = None
    ios: Optional[Dict[str, Any]] = None
    hmos: Optional[Dict[str, Any]] = None


@dataclass
class UserStatusGetResult:
    time_unit: Optional[str] = None
    start: Optional[str] = None
    duration: int = 0
    items: Optional[List[Dict[str, Any]]] = None

    _FIELD_MAP = {"time_unit": "TimeUnit"}


# ---------------------------------------------------------------------------
# Service
# ---------------------------------------------------------------------------

class StatusService:
    """Statistics query service — ``client.status``."""

    def __init__(self, client: Any) -> None:
        self._client = client

    def users(
        self,
        time_unit: str,
        start: str,
        duration: int,
    ) -> UserStatusGetResult:
        """Return user statistics (new, active, online) for a time range.

        ``GET /v4/status/users``
        """
        query = {
            "time_unit": time_unit,
            "start": start,
            "duration": str(duration),
        }
        return self._client._get("/v4/status/users", query=query, result_cls=UserStatusGetResult)

    def message_detail(self, message_ids: List[str]) -> Dict[str, Any]:
        """Return delivery statistics for given message IDs.

        ``GET /v4/status/detail``
        """
        query = {"message_ids": ",".join(message_ids)}
        return self._client._get("/v4/status/detail", query=query)

    def message_lifecycle(
        self,
        message_id: str,
        registration_ids: List[str],
    ) -> Dict[str, Any]:
        """Return lifecycle status for a message on specific devices.

        ``GET /v4/status/message``
        """
        query = {
            "message_id": message_id,
            "registration_ids": ",".join(registration_ids),
        }
        return self._client._get("/v4/status/message", query=query)

    def batch_message_detail(self, message_ids: List[str]) -> List[Dict[str, Any]]:
        """Return delivery statistics for multiple messages (batch).

        ``GET /v4/status/batch/message``
        """
        query = {"message_ids": ",".join(message_ids)}
        return self._client._get("/v4/status/batch/message", query=query)

    def plan_detail(
        self,
        plan_ids: List[str],
        start_date: str,
        end_date: str,
    ) -> Dict[str, Any]:
        """Return message statistics for a push plan.

        ``GET /v4/status/plan/detail``
        """
        query: Dict[str, str] = {
            "plan_ids": ",".join(plan_ids),
            "start_date": start_date,
            "end_date": end_date,
        }
        return self._client._get("/v4/status/plan/detail", query=query)
