"""Image upload service."""

from __future__ import annotations

import io
import json
import mimetypes
import os
import uuid
from dataclasses import dataclass
from typing import Any, BinaryIO, Dict, Optional

from .errors import parse_api_error


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

@dataclass
class ImageUploadResult:
    """Result of an image upload."""

    media_id: str = ""


# ---------------------------------------------------------------------------
# Service
# ---------------------------------------------------------------------------

class ImageService:
    """Image upload service — ``client.image``."""

    def __init__(self, client: Any) -> None:
        self._client = client

    def upload_oppo(self, file_path: str) -> ImageUploadResult:
        """Upload an image for OPPO push big picture (from file path).

        ``POST /v4/image/oppo`` (multipart/form-data)
        """
        with open(file_path, "rb") as f:
            return self.upload_oppo_from_reader(os.path.basename(file_path), f)

    def upload_oppo_from_reader(
        self,
        filename: str,
        reader: BinaryIO,
    ) -> ImageUploadResult:
        """Upload an image for OPPO push big picture (from a file-like object).

        ``POST /v4/image/oppo`` (multipart/form-data)
        """
        import urllib.error
        import urllib.request

        boundary = uuid.uuid4().hex
        content_type = f"multipart/form-data; boundary={boundary}"

        file_data = reader.read()
        mime_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"

        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
            f"Content-Type: {mime_type}\r\n\r\n"
        ).encode("utf-8") + file_data + f"\r\n--{boundary}--\r\n".encode("utf-8")

        return self._client._request(
            "POST",
            "/v4/image/oppo",
            result_cls=ImageUploadResult,
            headers={"Content-Type": content_type},
            raw_body=body,
        )
