"""Push plan service and data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

@dataclass
class PushPlanParam:
    plan_id: Optional[str] = None
    plan_description: Optional[str] = None


@dataclass
class PushPlanResult:
    plan_id: Optional[str] = None


@dataclass
class PushPlanDeleteResult:
    plan_id: Optional[str] = None


@dataclass
class PushPlanInfo:
    plan_id: Optional[str] = None
    plan_description: Optional[str] = None
    count: int = 0
    create_time: int = 0
    last_used_time: int = 0
    entity_tag: Optional[str] = None


@dataclass
class PushPlanListResult:
    push_plan_info: Optional[List[Dict[str, Any]]] = None
    total: int = 0


# ---------------------------------------------------------------------------
# Service
# ---------------------------------------------------------------------------

class PlanService:
    """Push plan management service — ``client.plan``."""

    def __init__(self, client: Any) -> None:
        self._client = client

    def create_or_update(self, param: PushPlanParam) -> PushPlanResult:
        """Create a new push plan or update an existing one.

        ``POST /v4/push_plan``
        """
        return self._client._post("/v4/push_plan", body=param, result_cls=PushPlanResult)

    def list(
        self,
        page_index: int = 1,
        page_size: int = 10,
        send_source: Optional[int] = None,
        search_description: str = "",
    ) -> PushPlanListResult:
        """Return a paginated list of push plans.

        ``GET /v4/push_plan/list``
        """
        query: Dict[str, str] = {
            "page_index": str(page_index),
            "page_size": str(page_size),
        }
        if send_source is not None:
            query["send_source"] = str(send_source)
        if search_description:
            query["search_description"] = search_description
        return self._client._get("/v4/push_plan/list", query=query, result_cls=PushPlanListResult)

    def query_msg(
        self,
        plan_ids: str,
        start_date: str = "",
        end_date: str = "",
    ) -> Dict[str, Any]:
        """Query message IDs by push plan IDs within a date range.

        ``GET /v4/status/plan/msg/``
        """
        query: Dict[str, str] = {"plan_ids": plan_ids}
        if start_date:
            query["start_date"] = start_date
        if end_date:
            query["end_date"] = end_date
        return self._client._get("/v4/status/plan/msg/", query=query)

    def delete(self, plan_id: str) -> PushPlanDeleteResult:
        """Delete a push plan.

        ``DELETE /v4/push_plan/{plan_id}``
        """
        return self._client._delete(
            f"/v4/push_plan/{plan_id}",
            result_cls=PushPlanDeleteResult,
        )

    def batch_delete(self, plan_ids: str) -> None:
        """Delete multiple push plans (comma-separated IDs).

        ``DELETE /v4/push_plan/batch/{plan_ids}``
        """
        self._client._delete(f"/v4/push_plan/batch/{plan_ids}")
