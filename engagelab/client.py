"""Core HTTP client for the EngageLab AppPush REST API."""

from __future__ import annotations

import base64
import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, BinaryIO, Dict, Optional, Tuple, Type, TypeVar

from ._serialization import from_dict, to_dict
from .errors import ApiError, parse_api_error

T = TypeVar("T")


class DataCenter:
    """Pre-defined API base URLs for each data-center region."""

    SINGAPORE = "https://pushapi-sgp.engagelab.com"
    HONG_KONG = "https://pushapi-hk.engagelab.com"
    VIRGINIA = "https://pushapi-usva.engagelab.com"
    FRANKFURT = "https://pushapi-defra.engagelab.com"


def _basic_auth(username: str, password: str) -> str:
    token = base64.b64encode(f"{username}:{password}".encode()).decode()
    return f"Basic {token}"


class Client:
    """EngageLab AppPush API client.

    Parameters:
        app_key: Application key.
        master_secret: Master secret.
        base_url: API base URL. Defaults to :pyattr:`DataCenter.SINGAPORE`.
        timeout: HTTP request timeout in seconds. Defaults to ``30``.
    """

    def __init__(
        self,
        app_key: str,
        master_secret: str,
        *,
        base_url: str = DataCenter.SINGAPORE,
        timeout: int = 30,
    ) -> None:
        self._base_url = base_url
        self._timeout = timeout
        self._auth_header = _basic_auth(app_key, master_secret)

        from .alias import AliasService
        from .device import DeviceService
        from .image import ImageService
        from .plan import PlanService
        from .push import PushService
        from .schedule import ScheduleService
        from .status import StatusService
        from .tag import TagService
        from .voice import VoiceService

        self.push = PushService(self)
        self.device = DeviceService(self)
        self.tag = TagService(self)
        self.alias = AliasService(self)
        self.schedule = ScheduleService(self)
        self.status = StatusService(self)
        self.plan = PlanService(self)
        self.voice = VoiceService(self)
        self.image = ImageService(self)

    # -- internal HTTP helpers ------------------------------------------------

    def _request(
        self,
        method: str,
        path: str,
        body: Any = None,
        result_cls: Optional[Type[T]] = None,
        *,
        headers: Optional[Dict[str, str]] = None,
        raw_body: Optional[bytes] = None,
    ) -> Any:
        url = self._base_url + path

        data: Optional[bytes] = None
        if raw_body is not None:
            data = raw_body
        elif body is not None:
            data = json.dumps(to_dict(body)).encode("utf-8")

        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Authorization", self._auth_header)
        if headers:
            for k, v in headers.items():
                req.add_header(k, v)
        else:
            req.add_header("Content-Type", "application/json; charset=utf-8")
        req.add_header("Accept", "application/json")

        try:
            with urllib.request.urlopen(req, timeout=self._timeout) as resp:
                resp_body = resp.read()
        except urllib.error.HTTPError as exc:
            resp_body = exc.read()
            raise parse_api_error(exc.code, resp_body) from None

        if not resp_body:
            return None

        resp_data = json.loads(resp_body)
        if result_cls is not None:
            return from_dict(result_cls, resp_data)
        return resp_data

    def _get(
        self,
        path: str,
        query: Optional[Dict[str, str]] = None,
        result_cls: Optional[Type[T]] = None,
    ) -> Any:
        if query:
            path = path + "?" + urllib.parse.urlencode(query)
        return self._request("GET", path, result_cls=result_cls)

    def _post(
        self,
        path: str,
        body: Any = None,
        result_cls: Optional[Type[T]] = None,
    ) -> Any:
        return self._request("POST", path, body=body, result_cls=result_cls)

    def _put(
        self,
        path: str,
        body: Any = None,
        result_cls: Optional[Type[T]] = None,
    ) -> Any:
        return self._request("PUT", path, body=body, result_cls=result_cls)

    def _delete(
        self,
        path: str,
        query: Optional[Dict[str, str]] = None,
        result_cls: Optional[Type[T]] = None,
    ) -> Any:
        if query:
            path = path + "?" + urllib.parse.urlencode(query)
        return self._request("DELETE", path, result_cls=result_cls)
