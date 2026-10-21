"""Voice file service and data models."""

from __future__ import annotations

import mimetypes
import os
import uuid
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class VoiceResult:
    language: Optional[str] = None
    file_url: Optional[str] = None


class VoiceService:
    """Voice file management service — ``client.voice``."""

    def __init__(self, client: Any) -> None:
        self._client = client

    def create(self, language: str, file_path: str) -> VoiceResult:
        """Upload a voice file using multipart/form-data."""
        boundary = uuid.uuid4().hex
        filename = os.path.basename(file_path)
        mime_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        with open(file_path, "rb") as voice_file:
            file_data = voice_file.read()
        body = (
            f"--{boundary}\r\n"
            'Content-Disposition: form-data; name="language"\r\n\r\n'
            f"{language}\r\n"
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
            f"Content-Type: {mime_type}\r\n\r\n"
        ).encode("utf-8") + file_data + f"\r\n--{boundary}--\r\n".encode("utf-8")
        return self._client._request(
            "POST",
            "/v4/voices",
            result_cls=VoiceResult,
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
            raw_body=body,
        )

    def list(self) -> List[Dict[str, Any]]:
        return self._client._get("/v4/voices")

    def get(self, language: str) -> VoiceResult:
        return self._client._get(f"/v4/voices/{language}", result_cls=VoiceResult)

    def delete(self, language: str) -> None:
        self._client._delete(f"/v4/voices/{language}")
