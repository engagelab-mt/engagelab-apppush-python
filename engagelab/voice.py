"""Voice / TTS template service and data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

@dataclass
class VoiceParam:
    language: Optional[str] = None
    content: Optional[str] = None
    tts_type: Optional[str] = None


@dataclass
class VoiceResult:
    language: Optional[str] = None
    content: Optional[str] = None
    tts_type: Optional[str] = None


@dataclass
class VoiceListResult:
    voices: Optional[List[Dict[str, Any]]] = None


# ---------------------------------------------------------------------------
# Service
# ---------------------------------------------------------------------------

class VoiceService:
    """Voice / TTS template management service — ``client.voice``."""

    def __init__(self, client: Any) -> None:
        self._client = client

    def create(self, param: VoiceParam) -> VoiceResult:
        """Create a new voice / TTS template.

        ``POST /v4/voices``
        """
        return self._client._post("/v4/voices", body=param, result_cls=VoiceResult)

    def list(self) -> VoiceListResult:
        """Return all voice / TTS templates.

        ``GET /v4/voices``
        """
        return self._client._get("/v4/voices", result_cls=VoiceListResult)

    def get(self, language: str) -> VoiceResult:
        """Retrieve a voice / TTS template by language.

        ``GET /v4/voices/{language}``
        """
        return self._client._get(f"/v4/voices/{language}", result_cls=VoiceResult)

    def delete(self, language: str) -> None:
        """Delete a voice / TTS template by language.

        ``DELETE /v4/voices/{language}``
        """
        self._client._delete(f"/v4/voices/{language}")
