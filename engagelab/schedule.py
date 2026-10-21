"""Schedule service and data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

@dataclass
class TriggerSingle:
    time: Optional[str] = None  # "yyyy-MM-dd HH:mm:ss"
    zone_type: Optional[int] = None


@dataclass
class TriggerPeriodical:
    start: Optional[str] = None
    end: Optional[str] = None
    time: Optional[str] = None  # "HH:mm:ss"
    frequency: Optional[int] = None
    time_unit: Optional[str] = None  # "day", "WEEK", "MONTH"
    point: Optional[List[str]] = None
    zone_type: Optional[int] = None


@dataclass
class TriggerIntelligent:
    backup_time: Optional[str] = None


@dataclass
class ScheduleTrigger:
    single: Optional[TriggerSingle] = None
    periodical: Optional[TriggerPeriodical] = None
    intelligent: Optional[TriggerIntelligent] = None


@dataclass
class SchedulePushParam:
    name: Optional[str] = None
    enabled: Optional[bool] = None
    trigger: Optional[ScheduleTrigger] = None
    push: Optional[Any] = None  # PushParam


@dataclass
class SchedulePushResult:
    schedule_id: Optional[str] = None
    name: Optional[str] = None


@dataclass
class SchedulePushGetResult:
    schedule_id: Optional[str] = None
    name: Optional[str] = None
    enabled: Optional[bool] = None
    trigger: Optional[Dict[str, Any]] = None
    push: Optional[Dict[str, Any]] = None


@dataclass
class SchedulePushListResult:
    total_count: int = 0
    total_pages: int = 0
    page: int = 0
    schedules: Optional[List[Dict[str, Any]]] = None


@dataclass
class SchedulePushDetailGetResult:
    count: int = 0
    msg_ids: Optional[List[Any]] = None

    _FIELD_MAP = {"msg_ids": "MsgIds"}


# ---------------------------------------------------------------------------
# Service
# ---------------------------------------------------------------------------

class ScheduleService:
    """Scheduled push management service — ``client.schedule``."""

    def __init__(self, client: Any) -> None:
        self._client = client

    def create(self, param: SchedulePushParam) -> SchedulePushResult:
        """Create a new scheduled push task.

        ``POST /v4/schedules``
        """
        return self._client._post("/v4/schedules", body=param, result_cls=SchedulePushResult)

    def update(self, schedule_id: str, param: SchedulePushParam) -> SchedulePushGetResult:
        """Update an existing scheduled push task.

        ``PUT /v4/schedules/{schedule_id}``
        """
        return self._client._put(
            f"/v4/schedules/{schedule_id}",
            body=param,
            result_cls=SchedulePushGetResult,
        )

    def delete(self, schedule_id: str) -> None:
        """Delete a scheduled push task.

        ``DELETE /v4/schedules/{schedule_id}``
        """
        self._client._delete(f"/v4/schedules/{schedule_id}")

    def get(self, schedule_id: str) -> List[Dict[str, Any]]:
        """Retrieve a scheduled push task by ID.

        ``GET /v4/schedules/{schedule_id}``
        """
        return self._client._get(f"/v4/schedules/{schedule_id}")

    def list(self, page: int = 1) -> SchedulePushListResult:
        """Return a paginated list of scheduled push tasks.

        ``GET /v4/schedules``
        """
        return self._client._get(
            "/v4/schedules",
            query={"page": str(page)},
            result_cls=SchedulePushListResult,
        )

    def get_msg_ids(self, schedule_id: str) -> SchedulePushDetailGetResult:
        """Retrieve message IDs for a scheduled push.

        ``GET /v4/schedules/{schedule_id}/msg-ids``
        """
        return self._client._get(
            f"/v4/schedules/{schedule_id}/msg-ids",
            result_cls=SchedulePushDetailGetResult,
        )
