"""Comprehensive tests for the EngageLab AppPush Python SDK.

Uses a local HTTP server (http.server) to mock API responses, mirroring the
Go SDK's httptest-based approach.  Zero external test dependencies — runs with
``python -m pytest tests/`` or ``python -m unittest discover tests``.
"""

from __future__ import annotations

import base64
import http.server
import json
import os
import tempfile
import threading
import unittest
from typing import Any, Dict

import engagelab
from engagelab._serialization import from_dict, to_dict


# ---------------------------------------------------------------------------
# Mock HTTP server
# ---------------------------------------------------------------------------

class _Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format: str, *args: Any) -> None:
        pass

    def _read_body(self) -> bytes:
        length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(length) if length else b""

    def _respond(self) -> None:
        body = self._read_body()
        server: _MockServer = self.server  # type: ignore[assignment]

        server.last_method = self.command
        server.last_path = self.path
        server.last_body = body
        server.last_headers = dict(self.headers)

        status = server.next_status or 200
        resp = server.next_response

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        if resp is not None:
            self.wfile.write(json.dumps(resp).encode())

    do_GET = _respond
    do_POST = _respond
    do_PUT = _respond
    do_DELETE = _respond


class _MockServer(http.server.HTTPServer):
    next_status: int = 200
    next_response: Any = {}
    last_method: str = ""
    last_path: str = ""
    last_body: bytes = b""
    last_headers: Dict[str, str] = {}

    def set_response(self, status: int = 200, body: Any = None) -> None:
        self.next_status = status
        self.next_response = body if body is not None else {}


def _start_mock_server() -> _MockServer:
    server = _MockServer(("127.0.0.1", 0), _Handler)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    return server


def _base_url(server: _MockServer) -> str:
    host, port = server.server_address
    return f"http://{host}:{port}"


def _client(server: _MockServer) -> engagelab.Client:
    return engagelab.Client("test-key", "test-secret", base_url=_base_url(server))


# ===================================================================
# Serialization: to_dict — every model, every field
# ===================================================================

class TestToDict(unittest.TestCase):
    """Verify to_dict serializes all model fields correctly."""

    # -- edge cases --

    def test_none_omitted(self) -> None:
        d = to_dict(engagelab.PushParam(to="all"))
        self.assertNotIn("from", d)
        self.assertNotIn("body", d)
        self.assertNotIn("request_id", d)
        self.assertNotIn("custom_args", d)
        self.assertEqual(d, {"to": "all"})

    def test_false_preserved(self) -> None:
        """bool False must NOT be treated as None."""
        d = to_dict(engagelab.SchedulePushParam(name="t", enabled=False))
        self.assertIn("enabled", d)
        self.assertIs(d["enabled"], False)

    def test_zero_preserved(self) -> None:
        """int 0 must NOT be treated as None."""
        d = to_dict(engagelab.Options(time_to_live=0, classification=0))
        self.assertEqual(d["time_to_live"], 0)
        self.assertEqual(d["classification"], 0)

    def test_empty_string_preserved(self) -> None:
        d = to_dict(engagelab.AndroidNotification(alert="", channel_id=""))
        self.assertEqual(d["alert"], "")
        self.assertEqual(d["channel_id"], "")

    def test_empty_list_preserved(self) -> None:
        d = to_dict(engagelab.PushTo(tag=[]))
        self.assertEqual(d["tag"], [])

    def test_empty_dict_preserved(self) -> None:
        d = to_dict(engagelab.AndroidNotification(extras={}))
        self.assertEqual(d["extras"], {})

    def test_dict_none_values_stripped(self) -> None:
        d = to_dict({"a": 1, "b": None, "c": "ok"})
        self.assertEqual(d, {"a": 1, "c": "ok"})

    def test_list_passthrough(self) -> None:
        d = to_dict([1, "two", None, 3])
        self.assertEqual(d, [1, "two", None, 3])

    def test_primitive_passthrough(self) -> None:
        self.assertEqual(to_dict(42), 42)
        self.assertEqual(to_dict("hello"), "hello")
        self.assertIs(to_dict(True), True)
        self.assertIsNone(to_dict(None))

    # -- PushParam field map --

    def test_push_param_from_field_map(self) -> None:
        d = to_dict(engagelab.PushParam(from_="push", to="all", request_id="r1",
                                         custom_args={"k": "v"}))
        self.assertEqual(d["from"], "push")
        self.assertNotIn("from_", d)
        self.assertEqual(d["to"], "all")
        self.assertEqual(d["request_id"], "r1")
        self.assertEqual(d["custom_args"], {"k": "v"})

    # -- AndroidNotification: all 19 fields --

    def test_android_notification_all_fields(self) -> None:
        n = engagelab.AndroidNotification(
            alert="a", title="t", builder_id=1, channel_id="ch",
            priority=2, category="cat", style=3, big_text="bt",
            inbox={"line1": "v1"}, big_pic_path="/img.png",
            extras={"ek": "ev"}, intent=engagelab.AndroidIntent(url="app://"),
            large_icon="li.png", small_icon="si.png", sound="ding.mp3",
            badge_add_num=5, badge_class="com.x.Main",
            display_foreground="1", group_id="g1",
        )
        d = to_dict(n)
        self.assertEqual(d["alert"], "a")
        self.assertEqual(d["title"], "t")
        self.assertEqual(d["builder_id"], 1)
        self.assertEqual(d["channel_id"], "ch")
        self.assertEqual(d["priority"], 2)
        self.assertEqual(d["category"], "cat")
        self.assertEqual(d["style"], 3)
        self.assertEqual(d["big_text"], "bt")
        self.assertEqual(d["inbox"], {"line1": "v1"})
        self.assertEqual(d["big_pic_path"], "/img.png")
        self.assertEqual(d["extras"], {"ek": "ev"})
        self.assertEqual(d["intent"], {"url": "app://"})
        self.assertEqual(d["large_icon"], "li.png")
        self.assertEqual(d["small_icon"], "si.png")
        self.assertEqual(d["sound"], "ding.mp3")
        self.assertEqual(d["badge_add_num"], 5)
        self.assertEqual(d["badge_class"], "com.x.Main")
        self.assertEqual(d["display_foreground"], "1")
        self.assertEqual(d["group_id"], "g1")
        self.assertEqual(len(d), 19)

    # -- IOSNotification: all 9 fields, 4 with FIELD_MAP --

    def test_ios_notification_all_fields(self) -> None:
        n = engagelab.IOSNotification(
            alert={"title": "T", "body": "B"},
            sound="default",
            badge=1,
            content_available=True,
            mutable_content=True,
            category="msg",
            extras={"url": "https://x"},
            thread_id="t-1",
            interruption_level="active",
        )
        d = to_dict(n)
        self.assertEqual(d["alert"], {"title": "T", "body": "B"})
        self.assertEqual(d["sound"], "default")
        self.assertEqual(d["badge"], 1)
        self.assertTrue(d["content-available"])
        self.assertTrue(d["mutable-content"])
        self.assertEqual(d["category"], "msg")
        self.assertEqual(d["extras"], {"url": "https://x"})
        self.assertEqual(d["thread-id"], "t-1")
        self.assertEqual(d["interruption-level"], "active")
        # field map keys must be hyphenated
        self.assertNotIn("content_available", d)
        self.assertNotIn("mutable_content", d)
        self.assertNotIn("thread_id", d)
        self.assertNotIn("interruption_level", d)
        self.assertEqual(len(d), 9)

    def test_ios_content_available_false(self) -> None:
        """False must serialize, not be omitted."""
        d = to_dict(engagelab.IOSNotification(content_available=False))
        self.assertIn("content-available", d)
        self.assertFalse(d["content-available"])

    # -- HmosNotification: all 15 fields --

    def test_hmos_notification_all_fields(self) -> None:
        n = engagelab.HmosNotification(
            alert="a", title="t", category="cat", large_icon="li.png",
            intent=engagelab.HmosIntent(url="hmos://"),
            badge_add_num=1, badge_set_num=5, test_message=True,
            receipt_id="rcpt", extras={"k": "v"}, style=2,
            inbox_content=["line1", "line2"], push_type=1,
            extra_data="ed", display_foreground="1",
        )
        d = to_dict(n)
        self.assertEqual(d["alert"], "a")
        self.assertEqual(d["title"], "t")
        self.assertEqual(d["category"], "cat")
        self.assertEqual(d["large_icon"], "li.png")
        self.assertEqual(d["intent"], {"url": "hmos://"})
        self.assertEqual(d["badge_add_num"], 1)
        self.assertEqual(d["badge_set_num"], 5)
        self.assertTrue(d["test_message"])
        self.assertEqual(d["receipt_id"], "rcpt")
        self.assertEqual(d["extras"], {"k": "v"})
        self.assertEqual(d["style"], 2)
        self.assertEqual(d["inbox_content"], ["line1", "line2"])
        self.assertEqual(d["push_type"], 1)
        self.assertEqual(d["extra_data"], "ed")
        self.assertEqual(d["display_foreground"], "1")
        self.assertEqual(len(d), 15)

    # -- NotificationMessage with all three platforms --

    def test_notification_message_all_platforms(self) -> None:
        d = to_dict(engagelab.NotificationMessage(
            alert="hi",
            android=engagelab.AndroidNotification(alert="android"),
            ios=engagelab.IOSNotification(alert="ios"),
            hmos=engagelab.HmosNotification(alert="hmos"),
        ))
        self.assertEqual(d["alert"], "hi")
        self.assertEqual(d["android"]["alert"], "android")
        self.assertEqual(d["ios"]["alert"], "ios")
        self.assertEqual(d["hmos"]["alert"], "hmos")

    # -- CustomMessage: all 4 fields --

    def test_custom_message_all_fields(self) -> None:
        d = to_dict(engagelab.CustomMessage(
            title="T", msg_content="body", content_type="text",
            extras={"a": 1},
        ))
        self.assertEqual(len(d), 4)
        self.assertEqual(d["msg_content"], "body")
        self.assertEqual(d["content_type"], "text")

    # -- LiveActivityIOS: all 9 fields, 6 with FIELD_MAP --

    def test_live_activity_ios_all_fields(self) -> None:
        la = engagelab.LiveActivityIOS(
            event="update",
            attributes_type="com.x.Attrs",
            content_state={"score": 10},
            alert=engagelab.LiveActivityAlert(sound="s", title="T", body="B"),
            dismissal_date=1700000000,
            stale_date=1700000001,
            attributes={"team": "A"},
            relevance_score=75,
            apns_priority=10,
        )
        d = to_dict(la)
        self.assertEqual(d["event"], "update")
        self.assertEqual(d["attributes-type"], "com.x.Attrs")
        self.assertEqual(d["content-state"], {"score": 10})
        self.assertEqual(d["alert"]["sound"], "s")
        self.assertEqual(d["dismissal-date"], 1700000000)
        self.assertEqual(d["stale-date"], 1700000001)
        self.assertEqual(d["attributes"], {"team": "A"})
        self.assertEqual(d["relevance-score"], 75)
        self.assertEqual(d["apns-priority"], 10)
        # must NOT contain snake_case keys
        for bad_key in ("attributes_type", "content_state", "dismissal_date",
                        "stale_date", "relevance_score", "apns_priority"):
            self.assertNotIn(bad_key, d)
        self.assertEqual(len(d), 9)

    # -- Options: all 12 fields --

    def test_options_all_fields(self) -> None:
        d = to_dict(engagelab.Options(
            time_to_live=86400, override_msg_id=123456,
            apns_production=True, apns_collapse_id="cid",
            big_push_duration=600,
            multi_language={"en": {"alert": "hi"}},
            third_party_channel={"xiaomi": {"importance": "NORMAL"}},
            classification=1, voice_value="voice_tpl",
            enhanc_message=False, plan_id="p1", cid="c1",
        ))
        self.assertEqual(d["time_to_live"], 86400)
        self.assertEqual(d["override_msg_id"], 123456)
        self.assertTrue(d["apns_production"])
        self.assertEqual(d["apns_collapse_id"], "cid")
        self.assertEqual(d["big_push_duration"], 600)
        self.assertIn("en", d["multi_language"])
        self.assertIn("xiaomi", d["third_party_channel"])
        self.assertEqual(d["classification"], 1)
        self.assertEqual(d["voice_value"], "voice_tpl")
        self.assertFalse(d["enhanc_message"])  # False preserved
        self.assertEqual(d["plan_id"], "p1")
        self.assertEqual(d["cid"], "c1")
        self.assertEqual(len(d), 12)

    # -- PushTo: all 7 fields with nested Seg --

    def test_push_to_all_fields(self) -> None:
        d = to_dict(engagelab.PushTo(
            registration_id=["r1", "r2"],
            tag=["t1"], tag_and=["t2"], tag_not=["t3"],
            alias=["a1"],
            live_activity_id="la_1",
            seg=engagelab.Seg(id="seg_1"),
        ))
        self.assertEqual(d["registration_id"], ["r1", "r2"])
        self.assertEqual(d["tag"], ["t1"])
        self.assertEqual(d["tag_and"], ["t2"])
        self.assertEqual(d["tag_not"], ["t3"])
        self.assertEqual(d["alias"], ["a1"])
        self.assertEqual(d["live_activity_id"], "la_1")
        self.assertEqual(d["seg"], {"id": "seg_1"})
        self.assertEqual(len(d), 7)

    # -- PushBody: all 5 fields --

    def test_push_body_all_fields(self) -> None:
        d = to_dict(engagelab.PushBody(
            platform=["android", "ios"],
            notification=engagelab.NotificationMessage(alert="n"),
            message=engagelab.CustomMessage(title="m"),
            live_activity=engagelab.LiveActivityMessage(
                ios=engagelab.LiveActivityIOS(event="end"),
            ),
            options=engagelab.Options(time_to_live=60),
        ))
        self.assertEqual(d["platform"], ["android", "ios"])
        self.assertEqual(d["notification"]["alert"], "n")
        self.assertEqual(d["message"]["title"], "m")
        self.assertEqual(d["live_activity"]["ios"]["event"], "end")
        self.assertEqual(d["options"]["time_to_live"], 60)
        self.assertEqual(len(d), 5)

    # -- BatchPushRequest: all 6 fields --

    def test_batch_push_request_all_fields(self) -> None:
        d = to_dict(engagelab.BatchPushRequest(
            target="r1", platform="android",
            notification=engagelab.NotificationMessage(alert="hi"),
            message=engagelab.CustomMessage(title="t"),
            options=engagelab.Options(cid="c"),
            custom_args={"k": "v"},
        ))
        self.assertEqual(d["target"], "r1")
        self.assertEqual(d["platform"], "android")
        self.assertIn("notification", d)
        self.assertIn("message", d)
        self.assertIn("options", d)
        self.assertEqual(d["custom_args"], {"k": "v"})
        self.assertEqual(len(d), 6)

    # -- BatchPushParam with list --

    def test_batch_push_param(self) -> None:
        d = to_dict(engagelab.BatchPushParam(requests=[
            engagelab.BatchPushRequest(target="r1"),
            engagelab.BatchPushRequest(target="r2"),
        ]))
        self.assertEqual(len(d["requests"]), 2)
        self.assertEqual(d["requests"][0]["target"], "r1")
        self.assertEqual(d["requests"][1]["target"], "r2")

    # -- DeviceSetParam nested --

    def test_device_set_param(self) -> None:
        d = to_dict(engagelab.DeviceSetParam(
            tags=engagelab.DeviceSetTags(add=["a", "b"], remove=["c"]),
            alias="u1",
        ))
        self.assertEqual(d["tags"]["add"], ["a", "b"])
        self.assertEqual(d["tags"]["remove"], ["c"])
        self.assertEqual(d["alias"], "u1")

    # -- TagSetParam nested --

    def test_tag_set_param(self) -> None:
        d = to_dict(engagelab.TagSetParam(
            registration_ids=engagelab.TagRegistrationIDs(add=["r1"], remove=["r2"]),
        ))
        self.assertEqual(d["registration_ids"]["add"], ["r1"])
        self.assertEqual(d["registration_ids"]["remove"], ["r2"])

    # -- Schedule triggers --

    def test_trigger_single_all_fields(self) -> None:
        d = to_dict(engagelab.ScheduleTrigger(
            single=engagelab.TriggerSingle(time="2026-12-31 10:00:00", zone_type=1),
        ))
        self.assertEqual(d["single"]["time"], "2026-12-31 10:00:00")
        self.assertEqual(d["single"]["zone_type"], 1)

    def test_trigger_periodical_all_fields(self) -> None:
        d = to_dict(engagelab.ScheduleTrigger(
            periodical=engagelab.TriggerPeriodical(
                start="2026-01-01 00:00:00", end="2026-12-31 23:59:59",
                time="08:00:00", frequency=1, time_unit="WEEK",
                point=["MON", "FRI"], zone_type=0,
            ),
        ))
        p = d["periodical"]
        self.assertEqual(p["start"], "2026-01-01 00:00:00")
        self.assertEqual(p["end"], "2026-12-31 23:59:59")
        self.assertEqual(p["time"], "08:00:00")
        self.assertEqual(p["frequency"], 1)
        self.assertEqual(p["time_unit"], "WEEK")
        self.assertEqual(p["point"], ["MON", "FRI"])
        self.assertEqual(p["zone_type"], 0)  # 0 preserved
        self.assertEqual(len(p), 7)

    # -- SchedulePushParam with nested PushParam --

    def test_schedule_push_param_nested(self) -> None:
        d = to_dict(engagelab.SchedulePushParam(
            name="daily",
            enabled=True,
            trigger=engagelab.ScheduleTrigger(
                single=engagelab.TriggerSingle(time="2026-12-31 10:00:00"),
            ),
            push=engagelab.PushParam(
                from_="api",
                to="all",
                body=engagelab.PushBody(platform="all"),
            ),
        ))
        self.assertEqual(d["name"], "daily")
        self.assertTrue(d["enabled"])
        self.assertIn("single", d["trigger"])
        self.assertEqual(d["push"]["from"], "api")  # FIELD_MAP applied in nested

    def test_oppo_image_param(self) -> None:
        d = to_dict(engagelab.OppoImageParam(big_picture_url="https://example.com/a.png"))
        self.assertEqual(d, {"big_picture_url": "https://example.com/a.png"})

    # -- PushPlanParam --

    def test_push_plan_param(self) -> None:
        d = to_dict(engagelab.PushPlanParam(plan_id="p1", plan_description="desc"))
        self.assertEqual(d, {"plan_id": "p1", "plan_description": "desc"})

    # -- DeviceStatusGetParam --

    def test_device_status_get_param(self) -> None:
        d = to_dict(engagelab.DeviceStatusGetParam(registration_ids=["r1", "r2"]))
        self.assertEqual(d, {"registration_ids": ["r1", "r2"]})

    # -- Deep nesting: full push payload --

    def test_full_push_payload(self) -> None:
        """Serialize a complete push payload with every nested layer."""
        param = engagelab.PushParam(
            from_="api",
            to=engagelab.PushTo(
                tag=["vip"],
                seg=engagelab.Seg(id="s1"),
            ),
            request_id="req_1",
            custom_args={"campaign": "spring"},
            body=engagelab.PushBody(
                platform=["android", "ios", "hmos"],
                notification=engagelab.NotificationMessage(
                    alert="global",
                    android=engagelab.AndroidNotification(
                        alert="android", title="T",
                        intent=engagelab.AndroidIntent(url="app://main"),
                    ),
                    ios=engagelab.IOSNotification(
                        alert="ios",
                        content_available=True,
                        mutable_content=False,
                    ),
                    hmos=engagelab.HmosNotification(
                        alert="hmos",
                        intent=engagelab.HmosIntent(url="hmos://main"),
                    ),
                ),
                options=engagelab.Options(
                    time_to_live=3600,
                    apns_production=True,
                ),
            ),
        )
        d = to_dict(param)
        # top-level
        self.assertEqual(d["from"], "api")
        self.assertEqual(d["to"]["tag"], ["vip"])
        self.assertEqual(d["to"]["seg"]["id"], "s1")
        self.assertEqual(d["request_id"], "req_1")
        # body -> notification -> android -> intent
        self.assertEqual(d["body"]["notification"]["android"]["intent"]["url"], "app://main")
        # body -> notification -> ios with hyphenated keys
        self.assertTrue(d["body"]["notification"]["ios"]["content-available"])
        self.assertFalse(d["body"]["notification"]["ios"]["mutable-content"])
        # body -> notification -> hmos -> intent
        self.assertEqual(d["body"]["notification"]["hmos"]["intent"]["url"], "hmos://main")
        # body -> options
        self.assertEqual(d["body"]["options"]["time_to_live"], 3600)


# ===================================================================
# Deserialization: from_dict — all result types with FIELD_MAP
# ===================================================================

class TestFromDict(unittest.TestCase):
    """Verify from_dict correctly maps JSON keys back to Python fields."""

    def test_push_result(self) -> None:
        r = from_dict(engagelab.PushResult, {"msg_id": "m1", "request_id": "r1"})
        self.assertEqual(r.msg_id, "m1")
        self.assertEqual(r.request_id, "r1")

    def test_push_result_missing_optional(self) -> None:
        r = from_dict(engagelab.PushResult, {"msg_id": "m1"})
        self.assertEqual(r.msg_id, "m1")
        self.assertIsNone(r.request_id)

    def test_push_withdraw_result(self) -> None:
        r = from_dict(engagelab.PushWithdrawResult, {"msg_id": "w1", "request_id": "wr1"})
        self.assertEqual(r.msg_id, "w1")

    def test_device_get_result(self) -> None:
        r = from_dict(engagelab.DeviceGetResult, {"tags": ["a", "b"], "alias": "u1"})
        self.assertEqual(r.tags, ["a", "b"])
        self.assertEqual(r.alias, "u1")

    def test_tags_count_get_result_field_map(self) -> None:
        """JSON key 'tagsCount' -> Python field 'tags_count'."""
        r = from_dict(engagelab.TagsCountGetResult, {"tagsCount": {"vip": 100}})
        self.assertEqual(r.tags_count, {"vip": 100})

    def test_alias_status_get_result(self) -> None:
        r = from_dict(engagelab.AliasStatusGetResult, {"registration_ids": ["r1"]})
        self.assertEqual(r.registration_ids, ["r1"])

    def test_schedule_push_result(self) -> None:
        r = from_dict(engagelab.SchedulePushResult, {"schedule_id": "s1", "name": "n"})
        self.assertEqual(r.schedule_id, "s1")

    def test_schedule_push_detail_field_map(self) -> None:
        """JSON key 'MsgIds' -> Python field 'msg_ids'."""
        r = from_dict(engagelab.SchedulePushDetailGetResult, {"count": 3, "MsgIds": [1, 2, 3]})
        self.assertEqual(r.count, 3)
        self.assertEqual(r.msg_ids, [1, 2, 3])

    def test_schedule_push_list_result(self) -> None:
        r = from_dict(engagelab.SchedulePushListResult, {
            "total_count": 10, "total_pages": 2, "page": 1, "schedules": [{"id": "s1"}],
        })
        self.assertEqual(r.total_count, 10)
        self.assertEqual(r.total_pages, 2)
        self.assertEqual(r.page, 1)
        self.assertEqual(len(r.schedules), 1)

    def test_user_status_get_result_field_map(self) -> None:
        """JSON key 'TimeUnit' -> Python field 'time_unit'."""
        r = from_dict(engagelab.UserStatusGetResult, {
            "TimeUnit": "day", "start": "2026-01-01", "duration": 7,
            "items": [{"time": "2026-01-01"}],
        })
        self.assertEqual(r.time_unit, "day")
        self.assertEqual(r.start, "2026-01-01")
        self.assertEqual(r.duration, 7)
        self.assertEqual(len(r.items), 1)

    def test_push_plan_result(self) -> None:
        r = from_dict(engagelab.PushPlanResult, {"plan_id": "p1"})
        self.assertEqual(r.plan_id, "p1")

    def test_push_plan_list_result(self) -> None:
        r = from_dict(engagelab.PushPlanListResult, {
            "push_plan_info": [{"plan_id": "p1"}], "total": 5,
        })
        self.assertEqual(r.total, 5)
        self.assertEqual(len(r.push_plan_info), 1)

    def test_voice_result(self) -> None:
        r = from_dict(engagelab.VoiceResult, {"language": "zh", "file_url": "https://example.com/v.mp3"})
        self.assertEqual(r.language, "zh")
        self.assertEqual(r.file_url, "https://example.com/v.mp3")

    def test_image_upload_result(self) -> None:
        r = from_dict(engagelab.ImageUploadResult, {"big_picture_id": "img_1"})
        self.assertEqual(r.big_picture_id, "img_1")

    def test_tag_quota_get_result(self) -> None:
        r = from_dict(engagelab.TagQuotaGetResult, {"data": {"totalTagQuota": 1000}})
        self.assertEqual(r.data["totalTagQuota"], 1000)

    def test_extra_fields_ignored(self) -> None:
        """Unknown JSON keys should not cause errors."""
        r = from_dict(engagelab.PushResult, {"msg_id": "m1", "unknown_field": 42})
        self.assertEqual(r.msg_id, "m1")

    def test_none_returns_none(self) -> None:
        self.assertIsNone(from_dict(engagelab.PushResult, None))

    def test_non_dataclass_passthrough(self) -> None:
        data = {"key": "val"}
        result = from_dict(dict, data)
        self.assertEqual(result, data)


# ===================================================================
# Client: auth, config, error handling
# ===================================================================

class TestClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.server = _start_mock_server()

    def test_auth_header(self) -> None:
        client = _client(self.server)
        expected = "Basic " + base64.b64encode(b"test-key:test-secret").decode()
        self.server.set_response(body={"msg_id": "1"})
        client.push.send(engagelab.PushParam(to="all"))
        self.assertEqual(self.server.last_headers.get("Authorization"), expected)

    def test_data_center_constants(self) -> None:
        self.assertEqual(engagelab.DataCenter.SINGAPORE, "https://pushapi-sgp.engagelab.com")
        self.assertEqual(engagelab.DataCenter.HONG_KONG, "https://pushapi-hk.engagelab.com")
        self.assertEqual(engagelab.DataCenter.VIRGINIA, "https://pushapi-usva.engagelab.com")
        self.assertEqual(engagelab.DataCenter.FRANKFURT, "https://pushapi-defra.engagelab.com")

    def test_custom_base_url(self) -> None:
        client = engagelab.Client("k", "s", base_url=_base_url(self.server))
        self.server.set_response(body={"msg_id": "1"})
        client.push.send(engagelab.PushParam(to="all"))
        self.assertIn("/v4/push", self.server.last_path)

    def test_custom_timeout(self) -> None:
        client = engagelab.Client("k", "s", base_url=_base_url(self.server), timeout=5)
        self.assertEqual(client._timeout, 5)

    def test_content_type_json(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={"msg_id": "1"})
        client.push.send(engagelab.PushParam(to="all"))
        ct = self.server.last_headers.get("Content-Type", "")
        self.assertIn("application/json", ct)

    def test_accept_header(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={"msg_id": "1"})
        client.push.send(engagelab.PushParam(to="all"))
        self.assertEqual(self.server.last_headers.get("Accept"), "application/json")

    def test_api_error_parsed(self) -> None:
        client = _client(self.server)
        self.server.set_response(status=401, body={"error": {"code": 1001, "message": "Unauthorized"}})
        with self.assertRaises(engagelab.ApiError) as ctx:
            client.push.send(engagelab.PushParam(to="all"))
        err = ctx.exception
        self.assertEqual(err.status_code, 401)
        self.assertEqual(err.error.code, 1001)
        self.assertEqual(err.error.message, "Unauthorized")

    def test_api_error_str(self) -> None:
        err = engagelab.ApiError(
            status_code=403,
            error=engagelab.ErrorDetail(code=2003, message="Forbidden"),
        )
        self.assertIn("403", str(err))
        self.assertIn("2003", str(err))
        self.assertIn("Forbidden", str(err))

    def test_api_error_malformed_json(self) -> None:
        """Non-JSON error body should not crash, just yield empty error detail."""
        client = _client(self.server)
        # Return non-JSON body to simulate server error
        self.server.set_response(status=500, body="Internal Server Error")
        with self.assertRaises(engagelab.ApiError) as ctx:
            client.push.send(engagelab.PushParam(to="all"))
        err = ctx.exception
        self.assertEqual(err.status_code, 500)

    def test_api_error_no_error_key(self) -> None:
        """Error body without 'error' key."""
        client = _client(self.server)
        self.server.set_response(status=400, body={"detail": "bad request"})
        with self.assertRaises(engagelab.ApiError) as ctx:
            client.push.send(engagelab.PushParam(to="all"))
        err = ctx.exception
        self.assertEqual(err.status_code, 400)
        self.assertEqual(err.error.code, 0)
        self.assertEqual(err.error.message, "")

    def test_empty_response_body(self) -> None:
        """200 with empty body should not crash for void operations."""
        client = _client(self.server)
        self.server.next_status = 200
        self.server.next_response = None  # handler sends empty body
        client.device.delete("r1")  # void operation, should not crash


# ===================================================================
# Push service — full request/response verification
# ===================================================================

class TestPush(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.server = _start_mock_server()

    def test_send_full_body(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={"msg_id": "12345", "request_id": "req_001"})
        result = client.push.send(engagelab.PushParam(
            from_="push",
            to="all",
            body=engagelab.PushBody(
                platform="all",
                notification=engagelab.NotificationMessage(
                    alert="Hello!",
                    android=engagelab.AndroidNotification(alert="A", title="T"),
                    ios=engagelab.IOSNotification(alert="I", mutable_content=True),
                ),
                options=engagelab.Options(time_to_live=3600, apns_production=True),
            ),
        ))
        self.assertEqual(result.msg_id, "12345")
        self.assertEqual(result.request_id, "req_001")
        self.assertEqual(self.server.last_method, "POST")
        self.assertIn("/v4/push", self.server.last_path)

        body = json.loads(self.server.last_body)
        self.assertEqual(body["from"], "push")
        self.assertEqual(body["to"], "all")
        self.assertEqual(body["body"]["platform"], "all")
        self.assertEqual(body["body"]["notification"]["android"]["title"], "T")
        self.assertTrue(body["body"]["notification"]["ios"]["mutable-content"])
        self.assertEqual(body["body"]["options"]["time_to_live"], 3600)

    def test_send_raw(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={"msg_id": "raw_001"})
        result = client.push.send_raw({"to": "all", "body": {"platform": "all"}})
        self.assertEqual(result.msg_id, "raw_001")
        body = json.loads(self.server.last_body)
        self.assertEqual(body["to"], "all")

    def test_validate(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={"msg_id": "val_001"})
        result = client.push.validate(engagelab.PushParam(to="all"))
        self.assertEqual(result.msg_id, "val_001")
        self.assertIn("/v4/push/validate", self.server.last_path)

    def test_withdraw(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={"msg_id": "w_001", "request_id": "wr1"})
        result = client.push.withdraw("msg_123")
        self.assertEqual(result.msg_id, "w_001")
        self.assertEqual(result.request_id, "wr1")
        self.assertEqual(self.server.last_method, "DELETE")
        self.assertIn("/v4/push/withdraw/msg_123", self.server.last_path)

    def test_batch_by_regid_body(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={
            "rate_limit_info": {
                "message": "Some requests were rate limited during batch processing",
                "rate_limit_occurred": True,
            },
            "results": {"r1": {"target": "r1", "success": False, "error": {
                "code": 23008, "message": "Rate limit exceeded for the API",
            }}},
        })
        result = client.push.batch_by_regid(engagelab.BatchPushParam(
            requests=[
                engagelab.BatchPushRequest(
                    target="r1", platform="android",
                    notification=engagelab.NotificationMessage(alert="hi"),
                    options=engagelab.Options(classification=1),
                    custom_args={"k": "v"},
                ),
            ],
        ))
        self.assertIn("/v4/batch/push/regid", self.server.last_path)
        body = json.loads(self.server.last_body)
        req0 = body["requests"][0]
        self.assertEqual(req0["target"], "r1")
        self.assertEqual(req0["platform"], "android")
        self.assertEqual(req0["notification"]["alert"], "hi")
        self.assertEqual(req0["options"]["classification"], 1)
        self.assertEqual(req0["custom_args"]["k"], "v")
        self.assertIsInstance(result.results, dict)
        self.assertIsInstance(result.results["r1"], engagelab.BatchPushSingleResult)
        self.assertEqual(result.results["r1"].error["code"], 23008)
        self.assertTrue(result.rate_limit_info.rate_limit_occurred)

    def test_batch_by_alias(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={"results": {}})
        client.push.batch_by_alias(engagelab.BatchPushParam(
            requests=[engagelab.BatchPushRequest(target="a1", platform="ios")],
        ))
        self.assertIn("/v4/batch/push/alias", self.server.last_path)

    def test_push_to_targets_body(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={"msg_id": "t_001"})
        client.push.send(engagelab.PushParam(
            to=engagelab.PushTo(
                registration_id=["r1"],
                tag=["vip"],
                tag_and=["premium"],
                tag_not=["banned"],
                alias=["user_001"],
            ),
            body=engagelab.PushBody(platform=["android", "ios"]),
        ))
        body = json.loads(self.server.last_body)
        to = body["to"]
        self.assertEqual(to["registration_id"], ["r1"])
        self.assertEqual(to["tag"], ["vip"])
        self.assertEqual(to["tag_and"], ["premium"])
        self.assertEqual(to["tag_not"], ["banned"])
        self.assertEqual(to["alias"], ["user_001"])

    def test_push_with_custom_message(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={"msg_id": "cm_001"})
        client.push.send(engagelab.PushParam(
            to="all",
            body=engagelab.PushBody(
                platform="all",
                message=engagelab.CustomMessage(
                    title="T", msg_content="body", content_type="text",
                    extras={"url": "https://x"},
                ),
            ),
        ))
        body = json.loads(self.server.last_body)
        msg = body["body"]["message"]
        self.assertEqual(msg["title"], "T")
        self.assertEqual(msg["msg_content"], "body")
        self.assertEqual(msg["content_type"], "text")
        self.assertEqual(msg["extras"]["url"], "https://x")

    def test_push_with_live_activity(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={"msg_id": "la_001"})
        client.push.send(engagelab.PushParam(
            to=engagelab.PushTo(live_activity_id="la_token_1"),
            body=engagelab.PushBody(
                platform="ios",
                live_activity=engagelab.LiveActivityMessage(
                    ios=engagelab.LiveActivityIOS(
                        event="update",
                        content_state={"score": 42},
                        alert=engagelab.LiveActivityAlert(title="Score!", body="42"),
                        stale_date=1700000000,
                        relevance_score=80,
                    ),
                ),
            ),
        ))
        body = json.loads(self.server.last_body)
        la = body["body"]["live_activity"]["ios"]
        self.assertEqual(la["event"], "update")
        self.assertEqual(la["content-state"]["score"], 42)
        self.assertEqual(la["alert"]["title"], "Score!")
        self.assertEqual(la["stale-date"], 1700000000)
        self.assertEqual(la["relevance-score"], 80)

    def test_push_with_hmos(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={"msg_id": "hm_001"})
        client.push.send(engagelab.PushParam(
            to="all",
            body=engagelab.PushBody(
                platform="hmos",
                notification=engagelab.NotificationMessage(
                    hmos=engagelab.HmosNotification(
                        alert="hi", title="T",
                        badge_add_num=1, badge_set_num=10,
                        test_message=False,
                        intent=engagelab.HmosIntent(url="hmos://app"),
                        inbox_content=["l1", "l2"],
                        push_type=0,
                    ),
                ),
            ),
        ))
        body = json.loads(self.server.last_body)
        hmos = body["body"]["notification"]["hmos"]
        self.assertEqual(hmos["badge_add_num"], 1)
        self.assertEqual(hmos["badge_set_num"], 10)
        self.assertFalse(hmos["test_message"])
        self.assertEqual(hmos["intent"]["url"], "hmos://app")
        self.assertEqual(hmos["inbox_content"], ["l1", "l2"])
        self.assertEqual(hmos["push_type"], 0)  # 0 preserved


# ===================================================================
# Device service
# ===================================================================

class TestDevice(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.server = _start_mock_server()

    def test_get(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={"tags": ["vip", "test"], "alias": "u001"})
        result = client.device.get("reg_001")
        self.assertEqual(result.tags, ["vip", "test"])
        self.assertEqual(result.alias, "u001")
        self.assertEqual(self.server.last_method, "GET")
        self.assertIn("/v4/devices/reg_001", self.server.last_path)

    def test_get_empty(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={"tags": [], "alias": ""})
        result = client.device.get("reg_002")
        self.assertEqual(result.tags, [])
        self.assertEqual(result.alias, "")

    def test_set_full_body(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={})
        client.device.set("reg_001", engagelab.DeviceSetParam(
            tags=engagelab.DeviceSetTags(add=["new_tag"], remove=["old_tag"]),
            alias="new_alias",
        ))
        self.assertEqual(self.server.last_method, "POST")
        body = json.loads(self.server.last_body)
        self.assertEqual(body["tags"]["add"], ["new_tag"])
        self.assertEqual(body["tags"]["remove"], ["old_tag"])
        self.assertEqual(body["alias"], "new_alias")

    def test_set_tags_only(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={})
        client.device.set("r1", engagelab.DeviceSetParam(
            tags=engagelab.DeviceSetTags(add=["t1"]),
        ))
        body = json.loads(self.server.last_body)
        self.assertIn("tags", body)
        self.assertNotIn("alias", body)

    def test_clear_tags(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={})
        client.device.set("r1", engagelab.DeviceSetParam(tags=""))
        body = json.loads(self.server.last_body)
        self.assertIn("tags", body)
        self.assertEqual(body["tags"], "")

    def test_delete(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={})
        client.device.delete("reg_001")
        self.assertEqual(self.server.last_method, "DELETE")
        self.assertIn("/v4/devices/reg_001", self.server.last_path)

    def test_get_status_body(self) -> None:
        client = _client(self.server)
        self.server.set_response(body=[
            {"regid": "r1", "online": True, "last_online_time": "2026-03-20 10:00"},
            {"regid": "r2", "online": False},
        ])
        result = client.device.get_status(engagelab.DeviceStatusGetParam(
            registration_ids=["r1", "r2"],
        ))
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["regid"], "r1")
        self.assertTrue(result[0]["online"])
        self.assertFalse(result[1]["online"])
        body = json.loads(self.server.last_body)
        self.assertEqual(body["registration_ids"], ["r1", "r2"])


# ===================================================================
# Tag service
# ===================================================================

class TestTag(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.server = _start_mock_server()

    def test_list(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={"tags": ["vip", "test"]})
        result = client.tag.list()
        self.assertEqual(result.tags, ["vip", "test"])
        self.assertEqual(self.server.last_method, "GET")

    def test_set_add_and_remove(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={})
        client.tag.set("vip", engagelab.TagSetParam(
            registration_ids=engagelab.TagRegistrationIDs(
                add=["r1", "r2"],
                remove=["r3"],
            ),
        ))
        self.assertIn("/v4/tags/vip", self.server.last_path)
        body = json.loads(self.server.last_body)
        self.assertEqual(body["registration_ids"]["add"], ["r1", "r2"])
        self.assertEqual(body["registration_ids"]["remove"], ["r3"])

    def test_delete_with_platforms(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={})
        client.tag.delete("old_tag", platforms=["android", "ios"])
        self.assertEqual(self.server.last_method, "DELETE")
        self.assertIn("/v4/tags/old_tag", self.server.last_path)
        self.assertIn("platform=", self.server.last_path)

    def test_delete_without_platforms(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={})
        client.tag.delete("tag1")
        self.assertEqual(self.server.last_method, "DELETE")
        self.assertNotIn("platform=", self.server.last_path)

    def test_get_count(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={"tagsCount": {"vip": 100, "test": 50}})
        result = client.tag.get_count(["vip", "test"], platform="android")
        self.assertEqual(result.tags_count, {"vip": 100, "test": 50})
        self.assertIn("tags=vip", self.server.last_path)
        self.assertIn("platform=android", self.server.last_path)

    def test_get_device_status(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={"result": True})
        result = client.tag.get_device_status("vip", "reg_001")
        self.assertTrue(result.result)
        self.assertIn("/v4/tags/vip/registration_ids/reg_001", self.server.last_path)

    def test_get_quota(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={"data": {
            "totalTagQuota": 1000, "useTagQuota": 50,
            "totalAliasQuota": 500, "useAliasQuota": 10,
        }})
        result = client.tag.get_quota(tags=["vip"], platform="android")
        self.assertIn("/v4/tags/quota-info", self.server.last_path)
        self.assertEqual(result.data["totalTagQuota"], 1000)


# ===================================================================
# Alias service
# ===================================================================

class TestAlias(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.server = _start_mock_server()

    def test_get_with_platforms(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={"registration_ids": ["r1", "r2"]})
        result = client.alias.get("user_001", platforms=["android"])
        self.assertEqual(result.registration_ids, ["r1", "r2"])
        self.assertIn("/v4/aliases/user_001", self.server.last_path)
        self.assertIn("platform=android", self.server.last_path)

    def test_get_without_platforms(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={"registration_ids": ["r1"]})
        result = client.alias.get("user_002")
        self.assertEqual(result.registration_ids, ["r1"])
        self.assertNotIn("platform=", self.server.last_path)

    def test_delete_with_platforms(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={})
        client.alias.delete("user_001", platforms=["android", "ios"])
        self.assertEqual(self.server.last_method, "DELETE")
        self.assertIn("platform=", self.server.last_path)

    def test_delete_without_platforms(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={})
        client.alias.delete("user_001")
        self.assertEqual(self.server.last_method, "DELETE")
        self.assertNotIn("platform=", self.server.last_path)


# ===================================================================
# Schedule service
# ===================================================================

class TestSchedule(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.server = _start_mock_server()

    def test_create_single_trigger(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={"schedule_id": "s_001", "name": "test"})
        result = client.schedule.create(engagelab.SchedulePushParam(
            name="Daily Push",
            enabled=True,
            trigger=engagelab.ScheduleTrigger(
                single=engagelab.TriggerSingle(time="2026-12-31 10:00:00", zone_type=1),
            ),
            push=engagelab.PushParam(to="all", body=engagelab.PushBody(platform="all")),
        ))
        self.assertEqual(result.schedule_id, "s_001")
        body = json.loads(self.server.last_body)
        self.assertEqual(body["trigger"]["single"]["time"], "2026-12-31 10:00:00")
        self.assertEqual(body["trigger"]["single"]["zone_type"], 1)
        self.assertEqual(body["push"]["to"], "all")

    def test_create_periodical_trigger(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={"schedule_id": "s_002"})
        client.schedule.create(engagelab.SchedulePushParam(
            name="Weekly Push",
            enabled=True,
            trigger=engagelab.ScheduleTrigger(
                periodical=engagelab.TriggerPeriodical(
                    start="2026-01-01 00:00:00", end="2026-12-31 23:59:59",
                    time="08:00:00", frequency=1, time_unit="WEEK",
                    point=["MON", "FRI"], zone_type=0,
                ),
            ),
        ))
        body = json.loads(self.server.last_body)
        p = body["trigger"]["periodical"]
        self.assertEqual(p["start"], "2026-01-01 00:00:00")
        self.assertEqual(p["end"], "2026-12-31 23:59:59")
        self.assertEqual(p["time"], "08:00:00")
        self.assertEqual(p["frequency"], 1)
        self.assertEqual(p["time_unit"], "WEEK")
        self.assertEqual(p["point"], ["MON", "FRI"])
        self.assertEqual(p["zone_type"], 0)

    def test_create_disabled(self) -> None:
        """enabled=False must be serialized, not omitted."""
        client = _client(self.server)
        self.server.set_response(body={"schedule_id": "s_003"})
        client.schedule.create(engagelab.SchedulePushParam(
            name="Disabled", enabled=False,
        ))
        body = json.loads(self.server.last_body)
        self.assertFalse(body["enabled"])

    def test_update(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={"schedule_id": "s_001", "name": "Updated"})
        result = client.schedule.update("s_001", engagelab.SchedulePushParam(name="Updated"))
        self.assertEqual(self.server.last_method, "PUT")
        self.assertEqual(result.schedule_id, "s_001")

    def test_delete(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={})
        client.schedule.delete("s_001")
        self.assertEqual(self.server.last_method, "DELETE")
        self.assertIn("/v4/schedules/s_001", self.server.last_path)

    def test_get(self) -> None:
        client = _client(self.server)
        self.server.set_response(body=[{"schedule_id": "s_001", "name": "test"}])
        result = client.schedule.get("s_001")
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]["schedule_id"], "s_001")

    def test_list(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={
            "total_count": 5, "total_pages": 1, "page": 1,
            "schedules": [{"schedule_id": "s1"}, {"schedule_id": "s2"}],
        })
        result = client.schedule.list(page=1)
        self.assertEqual(result.total_count, 5)
        self.assertEqual(result.page, 1)
        self.assertEqual(len(result.schedules), 2)
        self.assertIn("page=1", self.server.last_path)

    def test_get_msg_ids(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={"count": 3, "MsgIds": ["m1", "m2", "m3"]})
        result = client.schedule.get_msg_ids("s_001")
        self.assertEqual(result.count, 3)
        self.assertEqual(result.msg_ids, ["m1", "m2", "m3"])
        self.assertIn("/v4/schedules/s_001/msg-ids", self.server.last_path)


# ===================================================================
# Status service
# ===================================================================

class TestStatus(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.server = _start_mock_server()

    def test_users(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={
            "TimeUnit": "day", "start": "2026-03-01", "duration": 7,
            "items": [{"time": "2026-03-01", "android": {"new": 10, "active": 100, "online": 50}}],
        })
        result = client.status.users("day", "2026-03-01", 7)
        self.assertEqual(result.time_unit, "day")
        self.assertEqual(result.start, "2026-03-01")
        self.assertEqual(result.duration, 7)
        self.assertEqual(len(result.items), 1)
        self.assertEqual(result.items[0]["android"]["new"], 10)
        self.assertIn("time_unit=day", self.server.last_path)
        self.assertIn("duration=7", self.server.last_path)

    def test_message_detail(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={
            "msg_001": {"targets": 1000, "sent": 900, "delivered": 800},
        })
        result = client.status.message_detail(["msg_001", "msg_002"])
        self.assertIn("msg_001", result)
        self.assertEqual(result["msg_001"]["sent"], 900)
        self.assertIn("message_ids=msg_001", self.server.last_path)

    def test_message_lifecycle(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={
            "r1": {"status": "delivered"},
            "r2": {"status": "failed", "error_message": "offline"},
        })
        result = client.status.message_lifecycle("msg_001", ["r1", "r2"])
        self.assertEqual(result["r1"]["status"], "delivered")
        self.assertEqual(result["r2"]["error_message"], "offline")
        self.assertIn("message_id=msg_001", self.server.last_path)

    def test_batch_message_detail(self) -> None:
        client = _client(self.server)
        self.server.set_response(body=[{"message_id": "msg_001", "status": "sent"}])
        result = client.status.batch_message_detail(["msg_001"])
        self.assertEqual(result[0]["message_id"], "msg_001")
        self.assertIn("/v4/status/batch/message", self.server.last_path)

    def test_plan_detail(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={"plan_001": {"sent": 200}})
        result = client.status.plan_detail(["plan_001"], "2026-01-01", "2026-01-31")
        self.assertIn("plan_001", result)
        self.assertIn("plan_ids=plan_001", self.server.last_path)
        self.assertIn("start_date=2026-01-01", self.server.last_path)


# ===================================================================
# Plan service
# ===================================================================

class TestPlan(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.server = _start_mock_server()

    def test_create_or_update(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={"plan_id": "p_001"})
        result = client.plan.create_or_update(engagelab.PushPlanParam(
            plan_id="p_001", plan_description="Spring campaign",
        ))
        self.assertEqual(result.plan_id, "p_001")
        body = json.loads(self.server.last_body)
        self.assertEqual(body["plan_id"], "p_001")
        self.assertEqual(body["plan_description"], "Spring campaign")

    def test_list_with_all_params(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={
            "push_plan_info": [{"push_id": "p1", "count": 5, "create_time": 1000}],
            "total": 1,
        })
        result = client.plan.list(
            page_index=2, page_size=20,
            send_source=1, search_description="spring",
        )
        self.assertEqual(result.total, 1)
        self.assertIn("page_index=2", self.server.last_path)
        self.assertIn("page_size=20", self.server.last_path)
        self.assertIn("send_source=1", self.server.last_path)
        self.assertIn("search_description=spring", self.server.last_path)

    def test_list_minimal(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={"push_plan_info": [], "total": 0})
        client.plan.list()
        self.assertNotIn("send_source=", self.server.last_path)
        self.assertNotIn("search_description=", self.server.last_path)

    def test_query_msg(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={"p1": {"msg_ids": ["m1", "m2"]}})
        result = client.plan.query_msg("p1", start_date="2026-01-01", end_date="2026-03-01")
        self.assertIn("p1", result)
        self.assertEqual(result["p1"]["msg_ids"], ["m1", "m2"])
        self.assertIn("plan_ids=p1", self.server.last_path)
        self.assertIn("start_date=2026-01-01", self.server.last_path)

    def test_query_msg_minimal(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={})
        client.plan.query_msg("p1")
        self.assertNotIn("start_date=", self.server.last_path)
        self.assertNotIn("end_date=", self.server.last_path)

    def test_delete(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={"plan_id": "p_001"})
        result = client.plan.delete("p_001")
        self.assertEqual(result.plan_id, "p_001")
        self.assertEqual(self.server.last_method, "DELETE")

    def test_batch_delete(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={})
        client.plan.batch_delete("p_001,p_002")
        self.assertEqual(self.server.last_method, "DELETE")
        self.assertIn("/v4/push_plan/batch/p_001,p_002", self.server.last_path)


# ===================================================================
# Voice service
# ===================================================================

class TestVoice(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.server = _start_mock_server()

    def test_create_full_body(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={"language": "zh", "file_url": "https://example.com/v.mp3"})
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as voice_file:
            voice_file.write(b"voice-data")
            file_path = voice_file.name
        try:
            result = client.voice.create("zh", file_path)
        finally:
            os.unlink(file_path)
        self.assertEqual(result.file_url, "https://example.com/v.mp3")
        self.assertIn("multipart/form-data", self.server.last_headers.get("Content-Type", ""))
        self.assertIn(b'name="language"', self.server.last_body)
        self.assertIn(b'name="file"', self.server.last_body)

    def test_list(self) -> None:
        client = _client(self.server)
        self.server.set_response(body=[
            {"language": "en", "file_url": "u1"},
            {"language": "zh", "file_url": "u2"},
        ])
        result = client.voice.list()
        self.assertEqual(len(result), 2)

    def test_get(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={"language": "en", "file_url": "u"})
        result = client.voice.get("en")
        self.assertEqual(result.language, "en")
        self.assertIn("/v4/voices/en", self.server.last_path)

    def test_delete(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={})
        client.voice.delete("en")
        self.assertEqual(self.server.last_method, "DELETE")
        self.assertIn("/v4/voices/en", self.server.last_path)


# ===================================================================
# Image service
# ===================================================================

class TestImage(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.server = _start_mock_server()

    def test_upload_oppo_big_picture(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={"big_picture_id": "img_001"})
        result = client.image.upload_oppo(engagelab.OppoImageParam(
            big_picture_url="https://example.com/big.png",
        ))
        self.assertEqual(result.big_picture_id, "img_001")
        self.assertEqual(self.server.last_method, "POST")
        self.assertIn("/v4/image/oppo", self.server.last_path)
        self.assertIn("application/json", self.server.last_headers.get("Content-Type", ""))
        self.assertEqual(json.loads(self.server.last_body), {
            "big_picture_url": "https://example.com/big.png",
        })

# ===================================================================
# Group Push client
# ===================================================================

class TestGroupPush(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.server = _start_mock_server()

    def test_auth_header(self) -> None:
        gc = engagelab.GroupPushClient("gk", "gs", base_url=_base_url(self.server))
        self.server.set_response(body={"group_msgid": "g_001"})
        gc.send(engagelab.PushParam(to="all"))
        expected = "Basic " + base64.b64encode(b"group-gk:gs").decode()
        self.assertEqual(self.server.last_headers.get("Authorization"), expected)

    def test_send_full_body(self) -> None:
        gc = engagelab.GroupPushClient("gk", "gs", base_url=_base_url(self.server))
        self.server.set_response(body={
            "group_msgid": "g_002",
            "app1": {"request_id": "r1", "msg_id": "m1"},
            "app2": {"error": {"code": 1001, "message": "fail"}},
        })
        result = gc.send(engagelab.PushParam(
            from_="api",
            to="all",
            body=engagelab.PushBody(
                platform="all",
                notification=engagelab.NotificationMessage(alert="Group push!"),
            ),
        ))
        self.assertEqual(result.group_msgid, "g_002")
        self.assertIn("app1", result.successes)
        self.assertIn("app2", result.errors)
        self.assertIn("/v4/grouppush", self.server.last_path)
        body = json.loads(self.server.last_body)
        self.assertEqual(body["from"], "api")

    def test_custom_data_center(self) -> None:
        gc = engagelab.GroupPushClient("gk", "gs", base_url=_base_url(self.server), timeout=10)
        self.assertEqual(gc._timeout, 10)

    def test_api_error(self) -> None:
        gc = engagelab.GroupPushClient("gk", "gs", base_url=_base_url(self.server))
        self.server.set_response(status=403, body={"error": {"code": 2001, "message": "Forbidden"}})
        with self.assertRaises(engagelab.ApiError) as ctx:
            gc.send(engagelab.PushParam(to="all"))
        self.assertEqual(ctx.exception.status_code, 403)
        self.assertEqual(ctx.exception.error.code, 2001)


# ===================================================================
# Error parsing edge cases
# ===================================================================

class TestNewApiContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.server = _start_mock_server()

    def test_device_token_register(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={"results": [{
            "token": "t1", "registration_id": "r1", "is_new": True, "code": 0,
        }, {
            "token": "", "is_new": False, "code": 21003,
            "message": "invalid fcm token format",
        }]})
        result = client.device.register_token(engagelab.DeviceTokenRegisterParam(
            platform="android", tokens=["t1"],
        ))
        self.assertEqual(result.results[0].registration_id, "r1")
        self.assertEqual(result.results[1].code, 21003)
        self.assertEqual(result.results[1].message, "invalid fcm token format")
        self.assertEqual(self.server.last_method, "POST")
        self.assertIn("/v4/devices/token/registration_id", self.server.last_path)

    def test_app_vip_status(self) -> None:
        client = _client(self.server)
        self.server.set_response(body={"vip_status": 1, "vip_end_time": 1775059200})
        result = client.app.get_vip_status()
        self.assertEqual(result.vip_status, 1)
        self.assertEqual(result.vip_end_time, 1775059200)

    def test_data_center_constants(self) -> None:
        self.assertEqual(engagelab.DataCenter.JAPAN, "https://pushapi-jpn.engagelab.com")
        self.assertEqual(engagelab.DataCenter.BRAZIL, "https://pushapi-bra.engagelab.com")


class TestErrorParsing(unittest.TestCase):
    def test_parse_valid_error(self) -> None:
        from engagelab.errors import parse_api_error
        err = parse_api_error(400, b'{"error": {"code": 1003, "message": "Invalid param"}}')
        self.assertEqual(err.status_code, 400)
        self.assertEqual(err.error.code, 1003)
        self.assertEqual(err.error.message, "Invalid param")

    def test_parse_empty_body(self) -> None:
        from engagelab.errors import parse_api_error
        err = parse_api_error(500, b"")
        self.assertEqual(err.status_code, 500)
        self.assertEqual(err.error.code, 0)

    def test_parse_non_json_body(self) -> None:
        from engagelab.errors import parse_api_error
        err = parse_api_error(502, b"<html>Bad Gateway</html>")
        self.assertEqual(err.status_code, 502)
        self.assertEqual(err.error.code, 0)

    def test_parse_json_without_error_key(self) -> None:
        from engagelab.errors import parse_api_error
        err = parse_api_error(400, b'{"detail": "bad"}')
        self.assertEqual(err.status_code, 400)
        self.assertEqual(err.error.code, 0)
        self.assertEqual(err.error.message, "")

    def test_api_error_is_exception(self) -> None:
        err = engagelab.ApiError(status_code=500)
        self.assertIsInstance(err, Exception)
        with self.assertRaises(engagelab.ApiError):
            raise err


# ===================================================================
# __init__ exports
# ===================================================================

class TestExports(unittest.TestCase):
    def test_version(self) -> None:
        self.assertEqual(engagelab.__version__, "0.1.0")

    def test_all_exports_importable(self) -> None:
        for name in engagelab.__all__:
            self.assertTrue(hasattr(engagelab, name), f"{name} not exported")


if __name__ == "__main__":
    unittest.main()
