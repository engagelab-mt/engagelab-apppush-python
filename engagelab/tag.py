"""Tag service and data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

@dataclass
class TagsGetResult:
    tags: List[str] = field(default_factory=list)


@dataclass
class TagRegistrationIDs:
    add: Optional[List[str]] = None
    remove: Optional[List[str]] = None


@dataclass
class TagSetParam:
    registration_ids: Optional[TagRegistrationIDs] = None


@dataclass
class TagsCountGetResult:
    tags_count: Optional[Dict[str, int]] = None

    _FIELD_MAP = {"tags_count": "tagsCount"}


@dataclass
class TagQuotaData:
    total_tag_quota: int = 0
    use_tag_quota: int = 0
    total_alias_quota: int = 0
    use_alias_quota: int = 0
    tag_uid_quota_detail: Optional[List[Dict[str, Any]]] = None

    _FIELD_MAP = {
        "total_tag_quota": "totalTagQuota",
        "use_tag_quota": "useTagQuota",
        "total_alias_quota": "totalAliasQuota",
        "use_alias_quota": "useAliasQuota",
        "tag_uid_quota_detail": "tagUidQuotaDetail",
    }


@dataclass
class TagQuotaGetResult:
    data: Optional[Dict[str, Any]] = None


# ---------------------------------------------------------------------------
# Service
# ---------------------------------------------------------------------------

class TagService:
    """Tag management service — ``client.tag``."""

    def __init__(self, client: Any) -> None:
        self._client = client

    def list(self) -> TagsGetResult:
        """Get all tags for the application.

        ``GET /v4/tags``
        """
        return self._client._get("/v4/tags", result_cls=TagsGetResult)

    def set(self, tag: str, param: TagSetParam) -> None:
        """Add or remove registration IDs for a tag.

        ``POST /v4/tags/{tag}``
        """
        self._client._post(f"/v4/tags/{tag}", body=param)

    def delete(self, tag: str, platforms: Optional[List[str]] = None) -> None:
        """Delete a tag, optionally filtered by platforms.

        ``DELETE /v4/tags/{tag}``
        """
        query: Optional[Dict[str, str]] = None
        if platforms:
            query = {"platform": ",".join(platforms)}
        self._client._delete(f"/v4/tags/{tag}", query=query)

    def get_count(
        self,
        tags: List[str],
        platforms: Optional[List[str]] = None,
    ) -> TagsCountGetResult:
        """Return device counts for given tags and platforms.

        ``GET /v4/tags_count``
        """
        query: Dict[str, str] = {"tags": ",".join(tags)}
        if platforms:
            query["platform"] = ",".join(platforms)
        return self._client._get("/v4/tags_count", query=query, result_cls=TagsCountGetResult)

    def get_device_status(self, tag: str, registration_id: str) -> TagsGetResult:
        """Check if a registration ID has a specific tag.

        ``GET /v4/tags/{tag}/registration_ids/{registration_id}``
        """
        return self._client._get(
            f"/v4/tags/{tag}/registration_ids/{registration_id}",
            result_cls=TagsGetResult,
        )

    def get_quota(
        self,
        tags: Optional[List[str]] = None,
        platforms: Optional[List[str]] = None,
    ) -> TagQuotaGetResult:
        """Return tag / alias quota information.

        ``GET /v4/tags/quota-info``
        """
        query: Dict[str, str] = {}
        if tags:
            query["tags"] = ",".join(tags)
        if platforms:
            query["platform"] = ",".join(platforms)
        return self._client._get(
            "/v4/tags/quota-info",
            query=query or None,
            result_cls=TagQuotaGetResult,
        )
