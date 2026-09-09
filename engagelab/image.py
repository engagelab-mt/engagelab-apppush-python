"""OPPO notification image URL service."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class OppoImageParam:
    big_picture_url: Optional[str] = None
    small_picture_url: Optional[str] = None


@dataclass
class ImageUploadResult:
    big_picture_id: Optional[str] = None
    small_picture_id: Optional[str] = None


class ImageService:
    """OPPO notification image service — ``client.image``."""

    def __init__(self, client: Any) -> None:
        self._client = client

    def upload_oppo(self, param: OppoImageParam) -> ImageUploadResult:
        """Register exactly one big- or small-picture URL.

        ``POST /v4/image/oppo``
        """
        if bool(param.big_picture_url) == bool(param.small_picture_url):
            raise ValueError(
                "exactly one of big_picture_url and small_picture_url is required"
            )
        return self._client._post(
            "/v4/image/oppo", body=param, result_cls=ImageUploadResult
        )
