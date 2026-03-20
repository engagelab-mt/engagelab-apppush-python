"""EngageLab API error types."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class ErrorDetail:
    """Business-level error returned by the EngageLab API."""

    code: int = 0
    message: str = ""


@dataclass
class ApiError(Exception):
    """Raised when the EngageLab API returns a non-2xx response.

    Attributes:
        status_code: HTTP status code.
        error: Parsed business error (code + message).
    """

    status_code: int = 0
    error: ErrorDetail = field(default_factory=ErrorDetail)

    def __str__(self) -> str:
        return (
            f"engagelab api error: status={self.status_code} "
            f"code={self.error.code} message={self.error.message}"
        )


def parse_api_error(status_code: int, body: bytes) -> ApiError:
    """Parse an API error response body into an :class:`ApiError`."""
    api_err = ApiError(status_code=status_code)
    try:
        data: Dict[str, Any] = json.loads(body)
        err_data = data.get("error", {})
        api_err.error = ErrorDetail(
            code=err_data.get("code", 0),
            message=err_data.get("message", ""),
        )
    except (json.JSONDecodeError, AttributeError):
        pass
    return api_err
