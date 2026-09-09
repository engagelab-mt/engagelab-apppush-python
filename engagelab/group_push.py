"""Group Push client — uses separate authentication from the main Client."""

from __future__ import annotations

import base64
import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, Optional

from ._serialization import from_dict, to_dict
from .client import DataCenter
from .errors import parse_api_error
from .push import PushParam


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class GroupPushErrorDetail:
    def __init__(self, code: int = 0, message: str = "") -> None:
        self.code = code
        self.message = message


class GroupPushResult:
    """Result of a group push request."""

    def __init__(
        self,
        group_msgid: str = "",
        successes: Optional[Dict[str, Any]] = None,
        errors: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.group_msgid = group_msgid
        self.successes = successes
        self.errors = errors

    def __repr__(self) -> str:
        return f"GroupPushResult(group_msgid={self.group_msgid!r})"


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------

class GroupPushClient:
    """Standalone client for the EngageLab Group Push API.

    Authentication: ``Basic group-{group_key}:{group_master_secret}``

    Parameters:
        group_key: Group key (without the ``group-`` prefix).
        group_master_secret: Group master secret.
        base_url: API base URL. Defaults to :pyattr:`DataCenter.SINGAPORE`.
        timeout: HTTP request timeout in seconds. Defaults to ``30``.
    """

    def __init__(
        self,
        group_key: str,
        group_master_secret: str,
        *,
        base_url: str = DataCenter.SINGAPORE,
        timeout: int = 30,
    ) -> None:
        self._base_url = base_url
        self._timeout = timeout
        auth_str = f"group-{group_key}:{group_master_secret}"
        self._auth_header = "Basic " + base64.b64encode(auth_str.encode()).decode()

    def send(self, param: PushParam) -> GroupPushResult:
        """Send a group push to multiple apps.

        ``POST /v4/grouppush``
        """
        url = self._base_url + "/v4/grouppush"
        data = json.dumps(to_dict(param)).encode("utf-8")

        req = urllib.request.Request(url, data=data, method="POST")
        req.add_header("Authorization", self._auth_header)
        req.add_header("Content-Type", "application/json; charset=utf-8")
        req.add_header("Accept", "application/json")

        try:
            with urllib.request.urlopen(req, timeout=self._timeout) as resp:
                resp_body = resp.read()
        except urllib.error.HTTPError as exc:
            resp_body = exc.read()
            raise parse_api_error(exc.code, resp_body) from None

        resp_data: Dict[str, Any] = json.loads(resp_body) if resp_body else {}
        successes: Dict[str, Any] = {}
        errors: Dict[str, Any] = {}
        for app_key, item in resp_data.items():
            if app_key == "group_msgid":
                continue
            if isinstance(item, dict) and "error" in item:
                errors[app_key] = item["error"]
            elif isinstance(item, dict) and "msg_id" in item:
                successes[app_key] = item
        return GroupPushResult(
            group_msgid=resp_data.get("group_msgid", ""),
            successes=successes,
            errors=errors,
        )
