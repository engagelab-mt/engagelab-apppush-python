"""Push service and data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

@dataclass
class AndroidIntent:
    url: Optional[str] = None


@dataclass
class AndroidNotification:
    alert: Optional[Union[str, Dict[str, Any]]] = None
    title: Optional[str] = None
    builder_id: Optional[int] = None
    channel_id: Optional[str] = None
    priority: Optional[int] = None
    category: Optional[str] = None
    style: Optional[int] = None
    big_text: Optional[str] = None
    inbox: Optional[Dict[str, Any]] = None
    big_pic_path: Optional[str] = None
    extras: Optional[Dict[str, Any]] = None
    intent: Optional[AndroidIntent] = None
    large_icon: Optional[str] = None
    small_icon: Optional[str] = None
    sound: Optional[str] = None
    badge_add_num: Optional[int] = None
    badge_set_num: Optional[int] = None
    badge_class: Optional[str] = None
    display_foreground: Optional[str] = None
    group_id: Optional[str] = None
    is_fold: Optional[bool] = None


@dataclass
class IOSNotification:
    """iOS notification payload.

    Note: JSON keys use hyphens (e.g. ``content-available``).
    """

    alert: Optional[Any] = None
    sound: Optional[Any] = None
    badge: Optional[Any] = None
    content_available: Optional[bool] = None
    mutable_content: Optional[bool] = None
    category: Optional[str] = None
    extras: Optional[Dict[str, Any]] = None
    thread_id: Optional[str] = None
    interruption_level: Optional[str] = None

    _FIELD_MAP = {
        "content_available": "content-available",
        "mutable_content": "mutable-content",
        "thread_id": "thread-id",
        "interruption_level": "interruption-level",
    }


@dataclass
class HmosIntent:
    url: Optional[str] = None


@dataclass
class HmosNotification:
    alert: Optional[str] = None
    title: Optional[str] = None
    category: Optional[str] = None
    large_icon: Optional[str] = None
    intent: Optional[HmosIntent] = None
    badge_add_num: Optional[int] = None
    badge_set_num: Optional[int] = None
    test_message: Optional[bool] = None
    receipt_id: Optional[str] = None
    extras: Optional[Dict[str, Any]] = None
    style: Optional[int] = None
    inbox_content: Optional[List[str]] = None
    push_type: Optional[int] = None
    extra_data: Optional[str] = None
    display_foreground: Optional[str] = None


@dataclass
class NotificationMessage:
    alert: Optional[Union[str, Dict[str, Any]]] = None
    android: Optional[AndroidNotification] = None
    ios: Optional[IOSNotification] = None
    hmos: Optional[HmosNotification] = None


@dataclass
class CustomMessage:
    title: Optional[str] = None
    msg_content: Optional[Union[str, Dict[str, Any]]] = None
    content_type: Optional[str] = None
    extras: Optional[Dict[str, Any]] = None
    test_message: Optional[bool] = None
    receipt_id: Optional[str] = None


@dataclass
class LiveActivityAlert:
    sound: Optional[str] = None
    title: Optional[str] = None
    body: Optional[str] = None


@dataclass
class LiveActivityIOS:
    event: Optional[str] = None
    attributes_type: Optional[str] = None
    content_state: Optional[Dict[str, Any]] = None
    alert: Optional[LiveActivityAlert] = None
    dismissal_date: Optional[int] = None
    stale_date: Optional[int] = None
    attributes: Optional[Dict[str, Any]] = None
    relevance_score: Optional[int] = None
    apns_priority: Optional[int] = None

    _FIELD_MAP = {
        "attributes_type": "attributes-type",
        "content_state": "content-state",
        "dismissal_date": "dismissal-date",
        "stale_date": "stale-date",
        "relevance_score": "relevance-score",
        "apns_priority": "apns-priority",
    }


@dataclass
class LiveActivityMessage:
    ios: Optional[LiveActivityIOS] = None


@dataclass
class Options:
    time_to_live: Optional[int] = None
    override_msg_id: Optional[int] = None
    apns_production: Optional[bool] = None
    apns_collapse_id: Optional[str] = None
    big_push_duration: Optional[int] = None
    multi_language: Optional[Dict[str, Any]] = None
    third_party_channel: Optional[Dict[str, Any]] = None
    classification: Optional[int] = None
    voice_value: Optional[str] = None
    enhanc_message: Optional[bool] = None
    plan_id: Optional[str] = None
    cid: Optional[str] = None
    auto_truncation: Optional[bool] = None


@dataclass
class Seg:
    id: Optional[str] = None


@dataclass
class PushTo:
    registration_id: Optional[List[str]] = None
    tag: Optional[List[str]] = None
    tag_and: Optional[List[str]] = None
    tag_not: Optional[List[str]] = None
    alias: Optional[List[str]] = None
    live_activity_id: Optional[str] = None
    seg: Optional[Seg] = None


@dataclass
class PushBody:
    platform: Optional[Any] = None  # "all" or ["android", "ios", "hmos"]
    notification: Optional[NotificationMessage] = None
    message: Optional[CustomMessage] = None
    live_activity: Optional[LiveActivityMessage] = None
    voip: Optional[Dict[str, Any]] = None
    options: Optional[Options] = None


@dataclass
class PushParam:
    """Push request payload.

    ``to`` can be the string ``"all"`` or a :class:`PushTo` instance.
    """

    from_: Optional[str] = None
    to: Optional[Any] = None  # "all" or PushTo
    request_id: Optional[str] = None
    custom_args: Optional[Dict[str, Any]] = None
    body: Optional[PushBody] = None

    _FIELD_MAP = {"from_": "from"}


@dataclass
class PushResult:
    request_id: Optional[str] = None
    msg_id: str = ""


@dataclass
class PushWithdrawResult:
    request_id: Optional[str] = None
    msg_id: Optional[str] = None


@dataclass
class BatchPushRequest:
    target: Optional[str] = None
    platform: Optional[Any] = None
    notification: Optional[NotificationMessage] = None
    message: Optional[CustomMessage] = None
    options: Optional[Options] = None
    custom_args: Optional[Dict[str, Any]] = None


@dataclass
class BatchPushParam:
    requests: List[BatchPushRequest] = field(default_factory=list)


@dataclass
class BatchPushSingleResult:
    target: Optional[str] = None
    success: bool = False
    msg_id: int = 0
    error: Optional[Dict[str, Any]] = None


@dataclass
class BatchPushRateLimitInfo:
    message: Optional[str] = None
    rate_limit_occurred: bool = False


@dataclass
class BatchPushResult:
    results: Dict[str, BatchPushSingleResult] = field(default_factory=dict)
    rate_limit_info: Optional[BatchPushRateLimitInfo] = None


# ---------------------------------------------------------------------------
# Service
# ---------------------------------------------------------------------------

class PushService:
    """Push notification service — ``client.push``."""

    def __init__(self, client: Any) -> None:
        self._client = client

    def send(self, param: PushParam) -> PushResult:
        """Create and send a push notification.

        ``POST /v4/push``
        """
        return self._client._post("/v4/push", body=param, result_cls=PushResult)

    def send_raw(self, param: Any) -> PushResult:
        """Send a push with a raw dict / JSON body.

        ``POST /v4/push``
        """
        return self._client._post("/v4/push", body=param, result_cls=PushResult)

    def validate(self, param: PushParam) -> PushResult:
        """Validate a push payload without actually sending.

        ``POST /v4/push/validate``
        """
        return self._client._post("/v4/push/validate", body=param, result_cls=PushResult)

    def withdraw(self, msg_id: str) -> PushWithdrawResult:
        """Withdraw a push message (within 24 h, no duplicate withdrawal).

        ``DELETE /v4/push/withdraw/{msg_id}``
        """
        return self._client._delete(f"/v4/push/withdraw/{msg_id}", result_cls=PushWithdrawResult)

    def batch_by_regid(self, param: BatchPushParam) -> BatchPushResult:
        """Batch push by registration IDs.

        ``POST /v4/batch/push/regid``
        """
        return self._client._post("/v4/batch/push/regid", body=param, result_cls=BatchPushResult)

    def batch_by_alias(self, param: BatchPushParam) -> BatchPushResult:
        """Batch push by aliases.

        ``POST /v4/batch/push/alias``
        """
        return self._client._post("/v4/batch/push/alias", body=param, result_cls=BatchPushResult)
