"""Device service and data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

@dataclass
class DeviceStatusGetParam:
    registration_ids: List[str] = field(default_factory=list)


@dataclass
class DeviceStatusGetResult:
    regid: Optional[str] = None
    online: Optional[bool] = None
    last_online_time: Optional[str] = None


@dataclass
class DeviceGetResult:
    tags: Optional[List[str]] = None
    alias: Optional[str] = None


@dataclass
class DeviceSetTags:
    add: Optional[List[str]] = None
    remove: Optional[List[str]] = None


@dataclass
class DeviceSetParam:
    tags: Optional[DeviceSetTags] = None
    alias: Optional[str] = None


# ---------------------------------------------------------------------------
# Service
# ---------------------------------------------------------------------------

class DeviceService:
    """Device management service — ``client.device``."""

    def __init__(self, client: Any) -> None:
        self._client = client

    def get(self, registration_id: str) -> DeviceGetResult:
        """Retrieve device info (tags + alias).

        ``GET /v4/devices/{registration_id}``
        """
        return self._client._get(
            f"/v4/devices/{registration_id}",
            result_cls=DeviceGetResult,
        )

    def set(self, registration_id: str, param: DeviceSetParam) -> None:
        """Update tags and alias for a device.

        ``POST /v4/devices/{registration_id}``
        """
        self._client._post(f"/v4/devices/{registration_id}", body=param)

    def delete(self, registration_id: str) -> None:
        """Delete a device and all associated data (async, irreversible).

        ``DELETE /v4/devices/{registration_id}``
        """
        self._client._delete(f"/v4/devices/{registration_id}")

    def get_status(self, param: DeviceStatusGetParam) -> List[Dict[str, Any]]:
        """Query online status for a list of registration IDs.

        ``POST /v4/devices/status``
        """
        return self._client._post("/v4/devices/status", body=param)
