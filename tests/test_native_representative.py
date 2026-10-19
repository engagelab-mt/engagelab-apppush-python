"""Native assertions: independently runnable with Python's standard library."""
import functools
import json
import os
import unittest
from urllib.parse import urlencode

from engagelab.client import Client
from engagelab.device import DeviceTokenRegisterParam
from engagelab.group_push import GroupPushClient
from engagelab.plan import PushPlanParam
from engagelab.push import (PushParam, PushTo, PushBody, NotificationMessage,
                            AndroidNotification, Options)
from tests.support.native import Blocked, Config, Wire, check, start_fixture_server
from pathlib import Path


def payload(target='fixture-rid', request_id='native'):
    return PushParam(request_id=request_id, to=PushTo(registration_id=[target]),
        body=PushBody(platform=['android'], notification=NotificationMessage(
        android=AndroidNotification(alert='native SDK test', badge_set_num=0, is_fold=False)),
        options=Options(auto_truncation=False)))


def scenario(name):
    def decorate(fn):
        @functools.wraps(fn)
        def run(self):
            cfg = None
            self.checks = []
            try:
                cfg = self.cfg = Config()
                self.wire = Wire(cfg)
                self.client = Client(cfg.key, cfg.secret, base_url=cfg.base, timeout=cfg.timeout)
                fn(self)
                cfg.record(name, 'pass', self.checks)
            except Exception as error:
                status = 'block' if isinstance(error, Blocked) else 'no_pass'
                reason = str(error) if isinstance(error, (Blocked, AssertionError)) else type(error).__name__ + (':' + type(error.reason).__name__ + ':errno=' + str(getattr(error.reason, 'errno', None)) if hasattr(error, 'reason') else '')
                if cfg:
                    cfg.record(name, status, self.checks, reason)
                else:
                    out = Path(os.environ.get('ENGAGELAB_RESULTS_DIR', '.test-results'))
                    out.mkdir(parents=True, exist_ok=True)
                    (out / (name + '.json')).write_text(json.dumps(dict(scenario_id=name, language='Python', status=status, reason=reason)))
                raise AssertionError(status + ': ' + reason) from None
        return run
    return decorate


class NativeConfigTest(unittest.TestCase):
    def test_qa_prod_and_apns_are_independent(self):
        for target, base in [('qa', 'http://api.qa.jpushoa.com'), ('prod', 'https://pushapi-sgp.engagelab.com')]:
            e = dict(TEST_ENV=target, ENGAGELAB_BASE_URL=base, ENGAGELAB_APP_KEY='fixture',
                     ENGAGELAB_MASTER_SECRET='fixture', ENGAGELAB_HTTP_TIMEOUT='7',
                     ENGAGELAB_APNS_TOKEN='a'*64, ENGAGELAB_APNS_PRODUCTION='false', ENGAGELAB_BUNDLE_ID='fixture.app')
            cfg = Config(e)
            self.assertEqual(cfg.timeout, 7)
            self.assertFalse(cfg.apns()[1])
            with self.assertRaises(Blocked):
                cfg.write()
            e['TEST_ENV'] = 'prod' if target == 'qa' else 'qa'
            with self.assertRaises(Blocked):
                Config(e)
        for value in ('0', '-1', 'nan', 'inf', 'invalid'):
            e.update(TEST_ENV='prod', ENGAGELAB_HTTP_TIMEOUT=value)
            with self.assertRaises(Blocked):
                Config(e)


class NativeContractTest(unittest.TestCase):
    def setUp(self):
        self.server = start_fixture_server()
        self.base = 'http://127.0.0.1:' + str(self.server.server_port)
        self.client = Client('fixture-key', 'fixture-secret', base_url=self.base)

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()

    def test_field_passthrough(self):
        self.server.set_response(body={'msg_id': 'fixture-message'})
        self.assertEqual(self.client.push.validate(payload()).msg_id, 'fixture-message')
        b = json.loads(self.server.last_body)['body']
        self.assertIs(b['options']['auto_truncation'], False)
        self.assertIs(b['notification']['android']['is_fold'], False)
        self.assertEqual(b['notification']['android']['badge_set_num'], 0)
        self.assertEqual(self.server.last_path, '/v4/push/validate')

    def test_page_101(self):
        self.server.set_response(body={'total': 101, 'push_plan_info': [{'plan_id': str(i)} for i in range(101)]})
        result = self.client.plan.list(1, 101, search_description='fixture')
        self.assertEqual(result.total, 101)
        self.assertEqual(len(result.push_plan_info), 101)
        self.assertIn('page_size=101', self.server.last_path)

    def test_group_dynamic_keys(self):
        self.server.set_response(body={'group_msgid': 'g1', 'app-a': {'msg_id': 'm1'}, 'app-b': {'msg_id': 'm2'}})
        result = GroupPushClient('group', 'secret', base_url=self.base).send(payload())
        self.assertEqual(set(result.successes), {'app-a', 'app-b'})
        self.assertEqual(result.group_msgid, 'g1')
        self.assertFalse(result.errors)
        self.assertEqual(self.server.last_path, '/v4/grouppush')

    def test_token_sandbox(self):
        token = 'a'*64
        self.server.set_response(body={'results': [{'token': token, 'registration_id': 'r1', 'is_new': False, 'code': 0}]})
        result = self.client.device.register_token(DeviceTokenRegisterParam('ios', [token], False))
        self.assertEqual(result.results[0].registration_id, 'r1')
        self.assertIs(result.results[0].is_new, False)
        self.assertIs(json.loads(self.server.last_body)['apns_production'], False)


class NativeIntegration(unittest.TestCase):
    __test__ = os.environ.get("ENGAGELAB_TEST_SUITE") == "integration"
    def ok(self, value, label):
        check(value, label)
        self.checks.append(label)

    @scenario('field_passthrough')
    def test_field_passthrough(self):
        p = payload(self.cfg.need('ENGAGELAB_TEST_REGISTRATION_ID'), self.cfg.run_id)
        with self.wire.observe():
            result = self.client.push.validate(p)
        raw, sent = self.wire.last, self.wire.request
        self.ok(bool(result.msg_id) and result.msg_id == raw.get('msg_id'), 'validate_result_matches_wire')
        self.ok(sent['body']['options']['auto_truncation'] is False, 'false_option_preserved')
        self.ok(sent['body']['notification']['android']['badge_set_num'] == 0, 'zero_badge_preserved')
        self.ok(sent['body']['notification']['android']['is_fold'] is False, 'false_fold_preserved')

    @scenario('pagination_101')
    def test_pagination_101(self):
        self.cfg.write()
        prefix, owned = self.cfg.run_id, []
        query = '/v4/push_plan/list?' + urlencode(dict(page_index=1, page_size=101, search_description=prefix))
        try:
            for i in range(101):
                pid = prefix + '_' + str(i)
                owned.append(pid)  # register intent before sending, including ambiguous transport failures
                ledger = Path(self.cfg.env.get('ENGAGELAB_RESULTS_DIR', '.test-results')) / 'resources'
                ledger.mkdir(parents=True, exist_ok=True)
                (ledger / (prefix + '.json')).write_text(json.dumps(dict(run_id=prefix, owned_plan_ids=owned)))
                with self.wire.observe():
                    created = self.client.plan.create_or_update(PushPlanParam(pid, prefix))
                self.ok(created.plan_id == pid, 'created_plan_' + str(i))
            self.wire.until(lambda: self.wire.rest('GET', query)[1].get('total') == 101)
            with self.wire.observe():
                first = self.client.plan.list(1, 100, search_description=prefix)
                second = self.client.plan.list(2, 100, search_description=prefix)
                result = self.client.plan.list(1, 101, search_description=prefix)
            raw = self.wire.last
            self.ok(len(first.push_plan_info) == 100 and len(second.push_plan_info) == 1, '100_plus_1_pages')
            self.ok(result.total == 101 and len(result.push_plan_info) == 101, '101_returned')
            self.ok({x['plan_id'] for x in result.push_plan_info} == set(owned), 'owned_ids_exact')
            self.ok(result.push_plan_info == raw['push_plan_info'], 'parsed_fields_match_wire')
        finally:
            cleanup_errors = []
            for i in range(0, len(owned), 10):
                try:
                    with self.wire.observe():
                        self.client.plan.batch_delete(','.join(owned[i:i+10]))
                except Exception as error:
                    cleanup_errors.append(type(error).__name__)
            if cleanup_errors:
                self.checks.append('cleanup_transport_errors_requiring_readback')
            self.wire.until(lambda: self.wire.rest('GET', query)[1].get('total') == 0)
            self.ok(True, 'cleanup_zero_remaining')

    @scenario('group_push')
    def test_group_push(self):
        self.cfg.write()
        expected = set(self.cfg.need('ENGAGELAB_GROUP_APP_KEYS').split(','))
        self.ok(len(expected) >= 2 and '' not in expected, 'two_explicit_members')
        alias = self.cfg.need('ENGAGELAB_GROUP_TARGET_ALIAS')
        p = payload(request_id=self.cfg.run_id)
        p.to = PushTo(alias=[alias])
        p.body.options = Options(time_to_live=60, third_party_channel={'distribution_new': 'mtpush'})
        group = GroupPushClient(self.cfg.need('ENGAGELAB_GROUP_KEY'), self.cfg.need('ENGAGELAB_GROUP_SECRET'),
                               base_url=self.cfg.base, timeout=self.cfg.timeout)
        with self.wire.observe():
            result = group.send(p)
        raw = self.wire.last
        self.ok(bool(result.group_msgid) and result.group_msgid == raw.get('group_msgid'), 'group_id_matches_wire')
        self.ok(set(result.successes) == expected and not result.errors, 'dynamic_members_all_succeeded')
        self.ok(all(x.get('msg_id') and x == raw[k] for k, x in result.successes.items()), 'per_app_results_match_wire')
        self.ok(self.wire.request['to'] == {'alias': [alias]}, 'explicit_alias_only')

    def deleted(self, rid):
        status, body = self.wire.rest('GET', '/v4/devices/' + rid)
        return status == 400 and (body or {}).get('error', {}).get('code') == 27002

    @scenario('apns_token')
    def test_apns_token(self):
        self.cfg.write()
        token, prod = self.cfg.apns()
        p = DeviceTokenRegisterParam('ios', [token], prod)
        rid, created = None, False
        baseline = None
        try:
            with self.wire.observe():
                result = self.client.device.register_token(p)
            raw = self.wire.last['results']
            if len(raw) == 1:
                rid, created = raw[0].get('registration_id'), raw[0].get('is_new') is True
            self.ok(len(result.results) == len(raw) == 1, 'one_token_result')
            item = result.results[0]
            self.ok(bool(rid) and item.token == token and item.registration_id == rid and item.code == 0, 'registered_token_fields')
            self.ok(type(raw[0].get('is_new')) is bool and item.is_new == raw[0]['is_new'], 'is_new_matches_wire')
            self.ok(self.wire.request['apns_production'] is prod, 'explicit_apns_channel')
            self.wire.until(lambda: self.wire.rest('GET', '/v4/devices/' + rid)[0] == 200)
            baseline = self.wire.rest('GET', '/v4/devices/' + rid)
            with self.wire.observe():
                again = self.client.device.register_token(p)
            self.ok(again.results[0].registration_id == rid and again.results[0].is_new is False, 'same_mapping_reused')
        finally:
            if rid and created:
                self.wire.rest('DELETE', '/v4/devices/' + rid)
                self.wire.until(lambda: self.deleted(rid))
                self.ok(True, 'new_mapping_deleted')
            elif rid and baseline:
                self.ok(self.wire.rest('GET', '/v4/devices/' + rid) == baseline, 'existing_mapping_preserved')


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    for cls in (NativeConfigTest, NativeContractTest):
        suite.addTests(loader.loadTestsFromTestCase(cls))
    if os.environ.get('ENGAGELAB_TEST_SUITE') == 'integration':
        suite.addTests(loader.loadTestsFromTestCase(NativeIntegration))
    return suite
