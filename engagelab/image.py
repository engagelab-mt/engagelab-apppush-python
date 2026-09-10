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
        """Register OPPO notification image URLs.

        ``POST /v4/image/oppo``
        """
        return self._client._post(
            "/v4/image/oppo", body=param, result_cls=ImageUploadResult
        )
