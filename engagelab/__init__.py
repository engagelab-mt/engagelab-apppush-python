"""EngageLab AppPush Python SDK — zero third-party dependencies.

Quick start::

    import engagelab

    client = engagelab.Client("app_key", "master_secret")
    result = client.push.send(engagelab.PushParam(
        to="all",
        body=engagelab.PushBody(
            platform="all",
            notification=engagelab.NotificationMessage(alert="Hello!"),
        ),
    ))
    print(result.msg_id)

For Group Push (separate authentication)::

    gc = engagelab.GroupPushClient("group_key", "group_master_secret")
    result = gc.send(engagelab.PushParam(...))
"""

from .client import Client, DataCenter
from .errors import ApiError, ErrorDetail
from .push import (
    AndroidIntent,
    AndroidNotification,
    BatchPushParam,
    BatchPushRequest,
    BatchPushSingleResult,
    CustomMessage,
    HmosIntent,
    HmosNotification,
    IOSNotification,
    LiveActivityAlert,
    LiveActivityIOS,
    LiveActivityMessage,
    NotificationMessage,
    Options,
    PushBody,
    PushParam,
    PushResult,
    PushTo,
    PushWithdrawResult,
    Seg,
)
from .device import (
    DeviceGetResult,
    DeviceSetParam,
    DeviceSetTags,
    DeviceStatusGetParam,
    DeviceStatusGetResult,
)
from .tag import (
    TagQuotaData,
    TagQuotaGetResult,
    TagRegistrationIDs,
    TagSetParam,
    TagsCountGetResult,
    TagsGetResult,
)
from .alias import AliasStatusGetResult
from .schedule import (
    SchedulePushDetailGetResult,
    SchedulePushGetResult,
    SchedulePushListResult,
    SchedulePushParam,
    SchedulePushResult,
    ScheduleTrigger,
    TriggerPeriodical,
    TriggerSingle,
)
from .status import UserStatusGetResult, UserStatusItem, UserStatusPlatform
from .plan import (
    PushPlanDeleteResult,
    PushPlanInfo,
    PushPlanListResult,
    PushPlanParam,
    PushPlanResult,
)
from .voice import VoiceListResult, VoiceParam, VoiceResult
from .image import ImageUploadResult
from .group_push import GroupPushClient, GroupPushResult

__version__ = "0.1.0"

__all__ = [
    # Core
    "Client",
    "DataCenter",
    "ApiError",
    "ErrorDetail",
    # Push
    "PushParam",
    "PushBody",
    "PushTo",
    "Seg",
    "NotificationMessage",
    "AndroidNotification",
    "AndroidIntent",
    "IOSNotification",
    "HmosNotification",
    "HmosIntent",
    "CustomMessage",
    "LiveActivityMessage",
    "LiveActivityIOS",
    "LiveActivityAlert",
    "Options",
    "PushResult",
    "PushWithdrawResult",
    "BatchPushParam",
    "BatchPushRequest",
    "BatchPushSingleResult",
    # Device
    "DeviceStatusGetParam",
    "DeviceStatusGetResult",
    "DeviceGetResult",
    "DeviceSetParam",
    "DeviceSetTags",
    # Tag
    "TagsGetResult",
    "TagSetParam",
    "TagRegistrationIDs",
    "TagsCountGetResult",
    "TagQuotaGetResult",
    "TagQuotaData",
    # Alias
    "AliasStatusGetResult",
    # Schedule
    "SchedulePushParam",
    "ScheduleTrigger",
    "TriggerSingle",
    "TriggerPeriodical",
    "SchedulePushResult",
    "SchedulePushGetResult",
    "SchedulePushListResult",
    "SchedulePushDetailGetResult",
    # Status
    "UserStatusGetResult",
    "UserStatusItem",
    "UserStatusPlatform",
    # Plan
    "PushPlanParam",
    "PushPlanResult",
    "PushPlanDeleteResult",
    "PushPlanListResult",
    "PushPlanInfo",
    # Voice
    "VoiceParam",
    "VoiceResult",
    "VoiceListResult",
    # Image
    "ImageUploadResult",
    # Group Push
    "GroupPushClient",
    "GroupPushResult",
]
