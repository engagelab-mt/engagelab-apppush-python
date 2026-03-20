"""Example usage of the EngageLab AppPush Python SDK.

Replace ``your-app-key`` and ``your-master-secret`` with real credentials.
"""

from __future__ import annotations

import engagelab


def push_example(client: engagelab.Client) -> None:
    print("=== Push Example ===")

    result = client.push.send(engagelab.PushParam(
        from_="push",
        to="all",
        body=engagelab.PushBody(
            platform="all",
            notification=engagelab.NotificationMessage(
                alert="Hello from Python SDK!",
                android=engagelab.AndroidNotification(
                    alert="Hello Android!",
                    title="Test Push",
                ),
                ios=engagelab.IOSNotification(
                    alert="Hello iOS!",
                ),
            ),
        ),
    ))
    print(f"Push sent: msg_id={result.msg_id}")

    result = client.push.send(engagelab.PushParam(
        to="all",
        body=engagelab.PushBody(
            platform="all",
            message=engagelab.CustomMessage(
                title="Custom Message",
                msg_content="This is a passthrough message",
                extras={"key1": "value1"},
            ),
        ),
    ))
    print(f"Custom push sent: msg_id={result.msg_id}")

    result = client.push.send(engagelab.PushParam(
        to=engagelab.PushTo(
            tag=["vip", "premium"],
            alias=["user_001"],
        ),
        body=engagelab.PushBody(
            platform=["android", "ios"],
            notification=engagelab.NotificationMessage(alert="Targeted push!"),
        ),
    ))
    print(f"Targeted push sent: msg_id={result.msg_id}")

    batch_result = client.push.batch_by_regid(engagelab.BatchPushParam(
        requests=[
            engagelab.BatchPushRequest(
                target="regid_001",
                platform="android",
                notification=engagelab.NotificationMessage(alert="Hello regid_001!"),
            ),
            engagelab.BatchPushRequest(
                target="regid_002",
                platform="android",
                notification=engagelab.NotificationMessage(alert="Hello regid_002!"),
            ),
        ],
    ))
    print(f"Batch push result: {batch_result}")

    client.push.validate(engagelab.PushParam(
        to="all",
        body=engagelab.PushBody(
            platform="all",
            notification=engagelab.NotificationMessage(alert="Validation test"),
        ),
    ))
    print("Push validation passed")


def device_example(client: engagelab.Client) -> None:
    print("\n=== Device Example ===")

    device = client.device.get("registration_id_001")
    print(f"Device tags: {device.tags}, alias: {device.alias}")

    client.device.set("registration_id_001", engagelab.DeviceSetParam(
        tags=engagelab.DeviceSetTags(
            add=["new_tag"],
            remove=["old_tag"],
        ),
        alias="new_alias",
    ))

    status_list = client.device.get_status(engagelab.DeviceStatusGetParam(
        registration_ids=["regid_001", "regid_002"],
    ))
    for s in status_list:
        print(f"Device {s.get('regid')} online: {s.get('online')}")


def tag_example(client: engagelab.Client) -> None:
    print("\n=== Tag Example ===")

    tags = client.tag.list()
    print(f"Tags: {tags.tags}")

    client.tag.set("vip", engagelab.TagSetParam(
        registration_ids=engagelab.TagRegistrationIDs(
            add=["regid_001", "regid_002"],
        ),
    ))

    count = client.tag.get_count(["vip"], platforms=["android"])
    print(f"Tag counts: {count.tags_count}")

    alias_result = client.alias.get("user_001", platforms=["android", "ios"])
    print(f"Alias registration_ids: {alias_result.registration_ids}")


def schedule_example(client: engagelab.Client) -> None:
    print("\n=== Schedule Example ===")

    sched_result = client.schedule.create(engagelab.SchedulePushParam(
        name="Daily Push",
        enabled=True,
        trigger=engagelab.ScheduleTrigger(
            single=engagelab.TriggerSingle(time="2026-12-31 10:00:00"),
        ),
        push=engagelab.PushParam(
            to="all",
            body=engagelab.PushBody(
                platform="all",
                notification=engagelab.NotificationMessage(alert="Scheduled push!"),
            ),
        ),
    ))
    print(f"Schedule created: id={sched_result.schedule_id}")

    sched_list = client.schedule.list(page=1)
    print(f"Total schedules: {sched_list.total_count}")


def status_example(client: engagelab.Client) -> None:
    print("\n=== Status Example ===")

    users = client.status.users("day", "2026-03-01", 7)
    print(f"User stats: {len(users.items or [])} items")

    msg_stats = client.status.message_detail(["msg_001", "msg_002"])
    for msg_id, stat in msg_stats.items():
        print(f"Message {msg_id}: sent={stat.get('sent')} delivered={stat.get('delivered')}")


def plan_example(client: engagelab.Client) -> None:
    print("\n=== Plan Example ===")

    plan_result = client.plan.create_or_update(engagelab.PushPlanParam(
        plan_id="marketing_plan_001",
        plan_description="Spring promotion campaign",
    ))
    print(f"Plan created: id={plan_result.plan_id}")

    plan_list = client.plan.list(page_index=1, page_size=10)
    print(f"Total plans: {plan_list.total}")


def group_push_example() -> None:
    print("\n=== Group Push Example ===")

    group_client = engagelab.GroupPushClient(
        "your-group-key",
        "your-group-master-secret",
        base_url=engagelab.DataCenter.SINGAPORE,
    )

    result = group_client.send(engagelab.PushParam(
        to="all",
        body=engagelab.PushBody(
            platform="all",
            notification=engagelab.NotificationMessage(
                alert="Group push to all apps!",
            ),
        ),
    ))
    print(f"Group push sent: group_msgid={result.group_msgid}")


def main() -> None:
    client = engagelab.Client(
        "your-app-key",
        "your-master-secret",
        base_url=engagelab.DataCenter.SINGAPORE,
    )

    try:
        push_example(client)
        device_example(client)
        tag_example(client)
        schedule_example(client)
        status_example(client)
        plan_example(client)
        group_push_example()
    except engagelab.ApiError as e:
        print(f"\nAPI Error: status={e.status_code} code={e.error.code} message={e.error.message}")
    except Exception as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    main()
