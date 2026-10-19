"""Complete native contract suite. Tests/inputs/assertions are versioned code, not external testcases."""
import unittest
from tests.support.full_contract import run_contract

class FullContractTest(unittest.TestCase):
    def test_contract_9cdebf8d4bd9(self):
        """删除别名结构化错误解码"""
        run_contract('contract_9cdebf8d4bd9','删除别名结构化错误解码','alias_delete',['alias', ['android']],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_f0a82aa8d813(self):
        """查询别名结构化错误解码"""
        run_contract('contract_f0a82aa8d813','查询别名结构化错误解码','alias_get',['alias', ['android']],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_5155df98938b(self):
        """批量无限流false"""
        run_contract('contract_5155df98938b','批量无限流false','batch_regid',[{'requests': []}],200,{'results': {'ridA': {'target': 'ridA', 'success': True, 'msg_id': 123}, 'ridB': {'target': 'ridB', 'success': False, 'error': {'code': 21003, 'message': 'bad-target'}}}, 'rate_limit_info': {'message': 'limited', 'rate_limit_occurred': False}},None,{'results': {'ridA': {'target': 'ridA', 'success': True, 'msg_id': 123}, 'ridB': {'target': 'ridB', 'success': False, 'error': {'code': 21003, 'message': 'bad-target'}}}, 'rate_limit_info': {'message': 'limited', 'rate_limit_occurred': False}},None,3,0)

    def test_contract_da7062b4b0b0(self):
        """批量部分失败及顶层限流"""
        run_contract('contract_da7062b4b0b0','批量部分失败及顶层限流','batch_regid',[{'requests': []}],200,{'results': {'ridA': {'target': 'ridA', 'success': True, 'msg_id': 123}, 'ridB': {'target': 'ridB', 'success': False, 'error': {'code': 21003, 'message': 'bad-target'}}}, 'rate_limit_info': {'message': 'limited', 'rate_limit_occurred': True}},None,{'results': {'ridA': {'target': 'ridA', 'success': True, 'msg_id': 123}, 'ridB': {'target': 'ridB', 'success': False, 'error': {'code': 21003, 'message': 'bad-target'}}}, 'rate_limit_info': {'message': 'limited', 'rate_limit_occurred': True}},None,3,0)

    def test_contract_ac3d49e7bc4c(self):
        """按别名批量单推结构化错误解码"""
        run_contract('contract_ac3d49e7bc4c','按别名批量单推结构化错误解码','batch_alias',[{'requests': []}],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_259297710fd6(self):
        """按注册ID批量单推结构化错误解码"""
        run_contract('contract_259297710fd6','按注册ID批量单推结构化错误解码','batch_regid',[{'requests': [{'target': 'rid', 'platform': ['android'], 'notification': {'alert': 'demo'}}]}],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_58b21ab8dfab(self):
        """PushBody旧位置参数"""
        run_contract('contract_58b21ab8dfab','PushBody旧位置参数','legacy_pushbody',[],200,{'request_id': 'r1', 'msg_id': '123'},{'body': {'options': {'auto_truncation': False}}},None,None,3,0)

    def test_contract_9d476c850990(self):
        """删除别名纯文本success"""
        run_contract('contract_9d476c850990','删除别名纯文本success','alias_delete',['alias', ['android']],200,'success',None,None,None,3,0)

    def test_contract_e78e84d2f895(self):
        """删除标签纯文本success"""
        run_contract('contract_e78e84d2f895','删除标签纯文本success','tag_delete',['tag', ['android']],200,'success',None,None,None,3,0)

    def test_contract_80e322c49254(self):
        """删除设备纯文本success"""
        run_contract('contract_80e322c49254','删除设备纯文本success','device_delete',['rid'],200,'success',None,None,None,3,0)

    def test_contract_1d9167fde601(self):
        """既有send_raw入口"""
        run_contract('contract_1d9167fde601','既有send_raw入口','push_raw',[{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}}, 'request_id': 'compat-1', 'custom_args': {'zero': 0, 'false': False, 'none': None, 'unicode': '兼容性', 'nested': [{'n': 0, 'v': None}]}}],200,{'request_id': 'r1', 'msg_id': '123'},{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}}, 'request_id': 'compat-1', 'custom_args': {'zero': 0, 'false': False, 'unicode': '兼容性', 'nested': [{'n': 0}]}},None,None,3,0)

    def test_contract_8a8904d6d83d(self):
        """设置标签纯文本success"""
        run_contract('contract_8a8904d6d83d','设置标签纯文本success','tag_set',['tag', {'registration_ids': {'add': ['rid']}}],200,'success',None,None,None,3,0)

    def test_contract_f169b2128eba(self):
        """设置设备纯文本success"""
        run_contract('contract_f169b2128eba','设置设备纯文本success','device_set',['rid', {'alias': 'demo'}],200,'success',None,None,None,3,0)

    def test_contract_dfa2046dabe5(self):
        """仅修改别名不修改标签"""
        run_contract('contract_dfa2046dabe5','仅修改别名不修改标签','device_set',['rid', {'alias': 'alias-new'}],200,'success',{'alias': 'alias-new'},None,'no-tags',3,0)

    def test_contract_dfb4e0c04755(self):
        """删除设备结构化错误解码"""
        run_contract('contract_dfb4e0c04755','删除设备结构化错误解码','device_delete',['rid'],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_72a44c83c3bf(self):
        """批量查询设备状态结构化错误解码"""
        run_contract('contract_72a44c83c3bf','批量查询设备状态结构化错误解码','device_status',[{'registration_ids': ['rid']}],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_0ecfd4e41741(self):
        """查询设备结构化错误解码"""
        run_contract('contract_0ecfd4e41741','查询设备结构化错误解码','device_get',['rid'],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_d9c339d62287(self):
        """清空标签"""
        run_contract('contract_d9c339d62287','清空标签','device_set',['rid', {'tags': ''}],200,'success',{'tags': ''},None,None,3,0)

    def test_contract_79427730138c(self):
        """设置设备结构化错误解码"""
        run_contract('contract_79427730138c','设置设备结构化错误解码','device_set',['rid', {'alias': 'demo'}],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_ebdb2613f795(self):
        """分组推送成功结构化错误解码"""
        run_contract('contract_ebdb2613f795','分组推送成功结构化错误解码','group',[{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}}}],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_2dfd142e4cb3(self):
        """动态AppKey混合结果"""
        run_contract('contract_2dfd142e4cb3','动态AppKey混合结果','group',[{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}}}],200,{'appA': {'request_id': 'r1', 'msg_id': '123'}, 'appB': {'error': {'code': 21003, 'message': 'bad'}}, 'group_msgid': 'g1'},None,{'group_msgid': 'g1', 'successes': {'appA': {'msg_id': '123'}}, 'errors': {'appB': {'code': 21003, 'message': 'bad'}}},None,3,0)

    def test_contract_687d54787e11(self):
        """独立Group认证"""
        run_contract('contract_687d54787e11','独立Group认证','group',[{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}}}],200,{'group_msgid': 'g1'},None,None,'group-auth',3,0)

    def test_contract_bf68e6a9401c(self):
        """上传OPPO大图URL结构化错误解码"""
        run_contract('contract_bf68e6a9401c','上传OPPO大图URL结构化错误解码','image',[{'big_picture_url': 'https://example.test/a.png'}],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_5eb9bfe9737c(self):
        """双URL错误透传"""
        run_contract('contract_5eb9bfe9737c','双URL错误透传','image',[{'big_picture_url': 'https://example.test/big.png', 'small_picture_url': 'https://example.test/small.png'}],400,{'error': {'code': 21003, 'message': 'two urls'}},{'big_picture_url': 'https://example.test/big.png', 'small_picture_url': 'https://example.test/small.png'},None,None,3,0)

    def test_contract_4c035e91ff51(self):
        """大图URL和大图ID"""
        run_contract('contract_4c035e91ff51','大图URL和大图ID','image',[{'big_picture_url': 'https://example.test/big.png'}],200,{'big_picture_id': 'big-1'},{'big_picture_url': 'https://example.test/big.png'},{'big_picture_id': 'big-1'},None,3,0)

    def test_contract_f8d7833139db(self):
        """小图URL和小图ID"""
        run_contract('contract_f8d7833139db','小图URL和小图ID','image',[{'small_picture_url': 'https://example.test/small.png'}],200,{'small_picture_id': 'small-1'},{'small_picture_url': 'https://example.test/small.png'},{'small_picture_id': 'small-1'},None,3,0)

    def test_contract_875843e4ebe6(self):
        """创建推送计划结构化错误解码"""
        run_contract('contract_875843e4ebe6','创建推送计划结构化错误解码','plan_create',[{'plan_description': 'sdk-demo'}],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_11805d2b6e51(self):
        """删除推送计划结构化错误解码"""
        run_contract('contract_11805d2b6e51','删除推送计划结构化错误解码','plan_delete',['p1'],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_3a07b7732ac3(self):
        """批量删除推送计划结构化错误解码"""
        run_contract('contract_3a07b7732ac3','批量删除推送计划结构化错误解码','plan_batch_delete',['p1,p2'],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_1c0f0c91c0ce(self):
        """查询推送计划列表结构化错误解码"""
        run_contract('contract_1c0f0c91c0ce','查询推送计划列表结构化错误解码','plan_list',[1, 20, None, ''],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_231ace1b89ea(self):
        """查询计划关联消息结构化错误解码"""
        run_contract('contract_231ace1b89ea','查询计划关联消息结构化错误解码','plan_msgs',['p1', '2026-10-01', '2026-10-02'],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_9edb7086dd58(self):
        """计划毫秒时间戳"""
        run_contract('contract_9edb7086dd58','计划毫秒时间戳','plan_list',[1, 20, None, ''],200,{'push_plan_info': [{'plan_id': 'p1', 'entity_tag': 'e1', 'create_time': 1750000000123, 'last_used_time': 1750000000999}], 'total': 1},None,{'push_plan_info': [{'plan_id': 'p1', 'entity_tag': 'e1', 'create_time': 1750000000123, 'last_used_time': 1750000000999}]},None,3,0)

    def test_contract_e8824fdee833(self):
        """Android alert对象"""
        run_contract('contract_e8824fdee833','Android alert对象','validate',[{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo', 'android': {'alert': {'title': '标题', 'body': '正文'}}}}}],200,{'request_id': 'r1', 'msg_id': '123'},{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo', 'android': {'alert': {'title': '标题', 'body': '正文'}}}}},None,None,3,0)

    def test_contract_be95bbb49b74(self):
        """Android徽标显式零值"""
        run_contract('contract_be95bbb49b74','Android徽标显式零值','validate',[{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo', 'android': {'badge_set_num': 0}}}}],200,{'request_id': 'r1', 'msg_id': '123'},{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo', 'android': {'badge_set_num': 0}}}},None,None,3,0)

    def test_contract_33c08308bc82(self):
        """Android徽标正值"""
        run_contract('contract_33c08308bc82','Android徽标正值','validate',[{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo', 'android': {'badge_set_num': 9}}}}],200,{'request_id': 'r1', 'msg_id': '123'},{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo', 'android': {'badge_set_num': 9}}}},None,None,3,0)

    def test_contract_a1836b411d36(self):
        """Android折叠true"""
        run_contract('contract_a1836b411d36','Android折叠true','validate',[{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo', 'android': {'is_fold': True}}}}],200,{'request_id': 'r1', 'msg_id': '123'},{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo', 'android': {'is_fold': True}}}},None,None,3,0)

    def test_contract_1678c0d073d9(self):
        """Android折叠显式false"""
        run_contract('contract_1678c0d073d9','Android折叠显式false','validate',[{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo', 'android': {'is_fold': False}}}}],200,{'request_id': 'r1', 'msg_id': '123'},{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo', 'android': {'is_fold': False}}}},None,None,3,0)

    def test_contract_59cc473e4f61(self):
        """HMOS通知字段"""
        run_contract('contract_59cc473e4f61','HMOS通知字段','validate',[{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo', 'hmos': {'alert': 'demo', 'title': 'title', 'category': 'category', 'large_icon': 'https://example.test/icon', 'intent': {'url': 'demo://open'}, 'badge_add_num': 1, 'badge_set_num': 0, 'test_message': False, 'receipt_id': 'receipt', 'extras': {'n': 0}, 'style': 1, 'inbox_content': ['a', 'b'], 'push_type': 0, 'extra_data': 'data', 'display_foreground': '1'}}}}],200,{'request_id': 'r1', 'msg_id': '123'},{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo', 'hmos': {'alert': 'demo', 'title': 'title', 'category': 'category', 'large_icon': 'https://example.test/icon', 'intent': {'url': 'demo://open'}, 'badge_add_num': 1, 'badge_set_num': 0, 'test_message': False, 'receipt_id': 'receipt', 'extras': {'n': 0}, 'style': 1, 'inbox_content': ['a', 'b'], 'push_type': 0, 'extra_data': 'data', 'display_foreground': '1'}}}},None,None,3,0)

    def test_contract_4d70e82c7224(self):
        """LiveActivity连字符和零值"""
        run_contract('contract_4d70e82c7224','LiveActivity连字符和零值','validate',[{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}, 'live_activity': {'ios': {'attributes-type': 'Demo', 'content-state': {'n': 0}, 'dismissal-date': 0, 'stale-date': 1750000000, 'relevance-score': 0, 'apns-priority': 10}}}}],200,{'request_id': 'r1', 'msg_id': '123'},{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}, 'live_activity': {'ios': {'attributes-type': 'Demo', 'content-state': {'n': 0}, 'dismissal-date': 0, 'stale-date': 1750000000, 'relevance-score': 0, 'apns-priority': 10}}}},None,None,3,0)

    def test_contract_be624be5b5d1(self):
        """VoIP任意JSON对象"""
        run_contract('contract_be624be5b5d1','VoIP任意JSON对象','validate',[{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}, 'voip': {'call_id': 'c1', 'nested': {'video': True}}}}],200,{'request_id': 'r1', 'msg_id': '123'},{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}, 'voip': {'call_id': 'c1', 'nested': {'video': True}}}},None,None,3,0)

    def test_contract_3e0616162c43(self):
        """alias目标形态"""
        run_contract('contract_3e0616162c43','alias目标形态','validate',[{'to': {'alias': ['target1']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}}}],200,{'request_id': 'r1', 'msg_id': '123'},{'to': {'alias': ['target1']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}}},None,None,3,0)

    def test_contract_89d8dd7a2551(self):
        """all目标形态"""
        run_contract('contract_89d8dd7a2551','all目标形态','validate',[{'to': 'all', 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}}}],200,{'request_id': 'r1', 'msg_id': '123'},{'to': 'all', 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}}},None,None,3,0)

    def test_contract_044219309d70(self):
        """fcm厂商配置嵌套透传"""
        run_contract('contract_044219309d70','fcm厂商配置嵌套透传','validate',[{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}, 'options': {'third_party_channel': {'fcm': {'distribution_new': 'secondary_push', 'data': {'n': 0, 'flag': False}}}}}}],200,{'request_id': 'r1', 'msg_id': '123'},{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}, 'options': {'third_party_channel': {'fcm': {'distribution_new': 'secondary_push', 'data': {'n': 0, 'flag': False}}}}}},None,None,3,0)

    def test_contract_395fa770d3d7(self):
        """hmos厂商配置嵌套透传"""
        run_contract('contract_395fa770d3d7','hmos厂商配置嵌套透传','validate',[{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}, 'options': {'third_party_channel': {'hmos': {'distribution_new': 'secondary_push', 'data': {'n': 0, 'flag': False}}}}}}],200,{'request_id': 'r1', 'msg_id': '123'},{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}, 'options': {'third_party_channel': {'hmos': {'distribution_new': 'secondary_push', 'data': {'n': 0, 'flag': False}}}}}},None,None,3,0)

    def test_contract_febbdf980a2e(self):
        """honor厂商配置嵌套透传"""
        run_contract('contract_febbdf980a2e','honor厂商配置嵌套透传','validate',[{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}, 'options': {'third_party_channel': {'honor': {'distribution_new': 'secondary_push', 'data': {'n': 0, 'flag': False}}}}}}],200,{'request_id': 'r1', 'msg_id': '123'},{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}, 'options': {'third_party_channel': {'honor': {'distribution_new': 'secondary_push', 'data': {'n': 0, 'flag': False}}}}}},None,None,3,0)

    def test_contract_31617ee7a925(self):
        """huawei厂商配置嵌套透传"""
        run_contract('contract_31617ee7a925','huawei厂商配置嵌套透传','validate',[{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}, 'options': {'third_party_channel': {'huawei': {'distribution_new': 'secondary_push', 'data': {'n': 0, 'flag': False}}}}}}],200,{'request_id': 'r1', 'msg_id': '123'},{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}, 'options': {'third_party_channel': {'huawei': {'distribution_new': 'secondary_push', 'data': {'n': 0, 'flag': False}}}}}},None,None,3,0)

    def test_contract_6ce4022da7de(self):
        """iOS连字符字段"""
        run_contract('contract_6ce4022da7de','iOS连字符字段','validate',[{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo', 'ios': {'content-available': True, 'mutable-content': True, 'thread-id': 't', 'interruption-level': 'active'}}}}],200,{'request_id': 'r1', 'msg_id': '123'},{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo', 'ios': {'content-available': True, 'mutable-content': True, 'thread-id': 't', 'interruption-level': 'active'}}}},None,None,3,0)

    def test_contract_d0836a5e1fa7(self):
        """live_activity_id目标形态"""
        run_contract('contract_d0836a5e1fa7','live_activity_id目标形态','validate',[{'to': {'live_activity_id': 'live1'}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}}}],200,{'request_id': 'r1', 'msg_id': '123'},{'to': {'live_activity_id': 'live1'}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}}},None,None,3,0)

    def test_contract_dcf476eb4731(self):
        """meizu厂商配置嵌套透传"""
        run_contract('contract_dcf476eb4731','meizu厂商配置嵌套透传','validate',[{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}, 'options': {'third_party_channel': {'meizu': {'distribution_new': 'secondary_push', 'data': {'n': 0, 'flag': False}}}}}}],200,{'request_id': 'r1', 'msg_id': '123'},{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}, 'options': {'third_party_channel': {'meizu': {'distribution_new': 'secondary_push', 'data': {'n': 0, 'flag': False}}}}}},None,None,3,0)

    def test_contract_2fa3c3093257(self):
        """oppo厂商配置嵌套透传"""
        run_contract('contract_2fa3c3093257','oppo厂商配置嵌套透传','validate',[{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}, 'options': {'third_party_channel': {'oppo': {'distribution_new': 'secondary_push', 'data': {'n': 0, 'flag': False}}}}}}],200,{'request_id': 'r1', 'msg_id': '123'},{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}, 'options': {'third_party_channel': {'oppo': {'distribution_new': 'secondary_push', 'data': {'n': 0, 'flag': False}}}}}},None,None,3,0)

    def test_contract_863a2c664451(self):
        """registration_id目标形态"""
        run_contract('contract_863a2c664451','registration_id目标形态','validate',[{'to': {'registration_id': ['target1']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}}}],200,{'request_id': 'r1', 'msg_id': '123'},{'to': {'registration_id': ['target1']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}}},None,None,3,0)

    def test_contract_0e68ba4d8b3c(self):
        """seg目标形态"""
        run_contract('contract_0e68ba4d8b3c','seg目标形态','validate',[{'to': {'seg': {'id': 'seg1'}}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}}}],200,{'request_id': 'r1', 'msg_id': '123'},{'to': {'seg': {'id': 'seg1'}}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}}},None,None,3,0)

    def test_contract_8a0c098f4fbb(self):
        """tag_and目标形态"""
        run_contract('contract_8a0c098f4fbb','tag_and目标形态','validate',[{'to': {'tag_and': ['target1']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}}}],200,{'request_id': 'r1', 'msg_id': '123'},{'to': {'tag_and': ['target1']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}}},None,None,3,0)

    def test_contract_aafabb8f0d5f(self):
        """tag_not目标形态"""
        run_contract('contract_aafabb8f0d5f','tag_not目标形态','validate',[{'to': {'tag_not': ['target1']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}}}],200,{'request_id': 'r1', 'msg_id': '123'},{'to': {'tag_not': ['target1']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}}},None,None,3,0)

    def test_contract_79b6e40c5a99(self):
        """tag目标形态"""
        run_contract('contract_79b6e40c5a99','tag目标形态','validate',[{'to': {'tag': ['target1']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}}}],200,{'request_id': 'r1', 'msg_id': '123'},{'to': {'tag': ['target1']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}}},None,None,3,0)

    def test_contract_b835b5944185(self):
        """vivo厂商配置嵌套透传"""
        run_contract('contract_b835b5944185','vivo厂商配置嵌套透传','validate',[{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}, 'options': {'third_party_channel': {'vivo': {'distribution_new': 'secondary_push', 'data': {'n': 0, 'flag': False}}}}}}],200,{'request_id': 'r1', 'msg_id': '123'},{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}, 'options': {'third_party_channel': {'vivo': {'distribution_new': 'secondary_push', 'data': {'n': 0, 'flag': False}}}}}},None,None,3,0)

    def test_contract_a11a03885d19(self):
        """xiaomi厂商配置嵌套透传"""
        run_contract('contract_a11a03885d19','xiaomi厂商配置嵌套透传','validate',[{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}, 'options': {'third_party_channel': {'xiaomi': {'distribution_new': 'secondary_push', 'data': {'n': 0, 'flag': False}}}}}}],200,{'request_id': 'r1', 'msg_id': '123'},{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}, 'options': {'third_party_channel': {'xiaomi': {'distribution_new': 'secondary_push', 'data': {'n': 0, 'flag': False}}}}}},None,None,3,0)

    def test_contract_e656c8187753(self):
        """创建通知推送结构化错误解码"""
        run_contract('contract_e656c8187753','创建通知推送结构化错误解码','push',[{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}}}],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_c903a69359a8(self):
        """可选新增字段未设置"""
        run_contract('contract_c903a69359a8','可选新增字段未设置','validate',[{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}}}],200,{'request_id': 'r1', 'msg_id': '123'},{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}}},None,None,3,0)

    def test_contract_7ac4ecc638d4(self):
        """回执ID透传"""
        run_contract('contract_7ac4ecc638d4','回执ID透传','validate',[{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}, 'message': {'receipt_id': 'receipt-contract'}}}],200,{'request_id': 'r1', 'msg_id': '123'},{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}, 'message': {'receipt_id': 'receipt-contract'}}},None,None,3,0)

    def test_contract_6e726e41edc4(self):
        """多语言嵌套透传"""
        run_contract('contract_6e726e41edc4','多语言嵌套透传','validate',[{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}, 'options': {'multi_language': {'zh': {'content': '你好', 'title': '通知', 'subtitle': '副标题'}, 'en': {'content': 'hello'}}}}}],200,{'request_id': 'r1', 'msg_id': '123'},{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}, 'options': {'multi_language': {'zh': {'content': '你好', 'title': '通知', 'subtitle': '副标题'}, 'en': {'content': 'hello'}}}}},None,None,3,0)

    def test_contract_26a01b29a803(self):
        """撤回推送结构化错误解码"""
        run_contract('contract_26a01b29a803','撤回推送结构化错误解码','withdraw',['m1'],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_f60a65daa94a(self):
        """校验推送结构化错误解码"""
        run_contract('contract_f60a65daa94a','校验推送结构化错误解码','validate',[{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}}}],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_938d0727c229(self):
        """根对象动态参数"""
        run_contract('contract_938d0727c229','根对象动态参数','validate',[{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}}, 'from': 'source', 'request_id': 'r1', 'custom_args': {'trace': 't1', 'n': 0}}],200,{'request_id': 'r1', 'msg_id': '123'},{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}}, 'from': 'source', 'request_id': 'r1', 'custom_args': {'trace': 't1', 'n': 0}},None,None,3,0)

    def test_contract_04b1a35b7394(self):
        """测试消息false"""
        run_contract('contract_04b1a35b7394','测试消息false','validate',[{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}, 'message': {'test_message': False}}}],200,{'request_id': 'r1', 'msg_id': '123'},{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}, 'message': {'test_message': False}}},None,None,3,0)

    def test_contract_25935b05f837(self):
        """测试消息true"""
        run_contract('contract_25935b05f837','测试消息true','validate',[{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}, 'message': {'test_message': True}}}],200,{'request_id': 'r1', 'msg_id': '123'},{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}, 'message': {'test_message': True}}},None,None,3,0)

    def test_contract_3d1e6a7fa88c(self):
        """自动截断false"""
        run_contract('contract_3d1e6a7fa88c','自动截断false','validate',[{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}, 'options': {'auto_truncation': False}}}],200,{'request_id': 'r1', 'msg_id': '123'},{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}, 'options': {'auto_truncation': False}}},None,None,3,0)

    def test_contract_7ecd20648db7(self):
        """自动截断true"""
        run_contract('contract_7ecd20648db7','自动截断true','validate',[{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}, 'options': {'auto_truncation': True}}}],200,{'request_id': 'r1', 'msg_id': '123'},{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}, 'options': {'auto_truncation': True}}},None,None,3,0)

    def test_contract_aeab5f3b04f3(self):
        """自定义消息字符串"""
        run_contract('contract_aeab5f3b04f3','自定义消息字符串','validate',[{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}, 'message': {'msg_content': '订单通知'}}}],200,{'request_id': 'r1', 'msg_id': '123'},{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}, 'message': {'msg_content': '订单通知'}}},None,None,3,0)

    def test_contract_e2cc1dc0f016(self):
        """自定义消息对象"""
        run_contract('contract_e2cc1dc0f016','自定义消息对象','validate',[{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}, 'message': {'msg_content': {'order': 123, 'items': ['a']}}}}],200,{'request_id': 'r1', 'msg_id': '123'},{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}, 'message': {'msg_content': {'order': 123, 'items': ['a']}}}},None,None,3,0)

    def test_contract_5c3fb99e56a3(self):
        """通知alert对象"""
        run_contract('contract_5c3fb99e56a3','通知alert对象','validate',[{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': {'title': '标题', 'body': '正文'}}}}],200,{'request_id': 'r1', 'msg_id': '123'},{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': {'title': '标题', 'body': '正文'}}}},None,None,3,0)

    def test_contract_34753ccf040e(self):
        """分页查询定时任务结构化错误解码"""
        run_contract('contract_34753ccf040e','分页查询定时任务结构化错误解码','schedule_list',[1],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_a006064310d2(self):
        """创建定时任务结构化错误解码"""
        run_contract('contract_a006064310d2','创建定时任务结构化错误解码','schedule_create',[{'name': 'sdk-demo', 'enabled': True, 'push': {'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}}}, 'trigger': {'single': {'time': '2030-01-02 12:00:00', 'zone_type': 1}}}],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_5e6a52b60549(self):
        """删除定时任务结构化错误解码"""
        run_contract('contract_5e6a52b60549','删除定时任务结构化错误解码','schedule_delete',['s1'],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_f5c3f9d7b04b(self):
        """周期定时原调用"""
        run_contract('contract_f5c3f9d7b04b','周期定时原调用','schedule_create',[{'name': 'compat-periodical', 'enabled': False, 'trigger': {'periodical': {'start': '2030-01-01 00:00:00', 'end': '2030-01-03 00:00:00', 'time': '12:00:00', 'frequency': 1, 'time_unit': 'day', 'point': ['1'], 'zone_type': 1}}, 'push': {'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}}}}],200,{'schedule_id': 's1', 'name': 'compat-periodical'},{'name': 'compat-periodical', 'enabled': False, 'trigger': {'periodical': {'start': '2030-01-01 00:00:00', 'end': '2030-01-03 00:00:00', 'time': '12:00:00', 'frequency': 1, 'time_unit': 'day', 'point': ['1'], 'zone_type': 1}}, 'push': {'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}}}},None,None,3,0)

    def test_contract_a24cb7dc7fc4(self):
        """嵌套推送新增字段"""
        run_contract('contract_a24cb7dc7fc4','嵌套推送新增字段','schedule_create',[{'name': 'sdk-demo', 'enabled': True, 'push': {'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo', 'android': {'is_fold': False, 'badge_set_num': 0}}, 'options': {'auto_truncation': False}}}, 'trigger': {'single': {'time': '2030-01-02 12:00:00', 'zone_type': 1}}}],200,{},{'name': 'sdk-demo', 'enabled': True, 'push': {'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo', 'android': {'is_fold': False, 'badge_set_num': 0}}, 'options': {'auto_truncation': False}}}, 'trigger': {'single': {'time': '2030-01-02 12:00:00', 'zone_type': 1}}},None,None,3,0)

    def test_contract_43e45479ade7(self):
        """智能定时创建备用时间"""
        run_contract('contract_43e45479ade7','智能定时创建备用时间','schedule_create',[{'name': 'sdk-demo', 'enabled': True, 'push': {'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}}}, 'trigger': {'intelligent': {'backup_time': '2030-01-02 12:00:00'}}}],200,{},{'name': 'sdk-demo', 'enabled': True, 'push': {'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}}}, 'trigger': {'intelligent': {'backup_time': '2030-01-02 12:00:00'}}},None,None,3,0)

    def test_contract_2c968bdd4735(self):
        """智能定时更新备用时间"""
        run_contract('contract_2c968bdd4735','智能定时更新备用时间','schedule_update',['s1', {'name': 'sdk-demo', 'enabled': True, 'push': {'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}}}, 'trigger': {'intelligent': {'backup_time': '2030-01-02 12:00:00'}}}],200,{},{'name': 'sdk-demo', 'enabled': True, 'push': {'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}}}, 'trigger': {'intelligent': {'backup_time': '2030-01-02 12:00:00'}}},None,None,3,0)

    def test_contract_630b72f4c210(self):
        """更新定时任务结构化错误解码"""
        run_contract('contract_630b72f4c210','更新定时任务结构化错误解码','schedule_update',['s1', {'name': 'sdk-demo', 'enabled': True, 'push': {'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}}}, 'trigger': {'single': {'time': '2030-01-02 12:00:00', 'zone_type': 1}}}],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_41157efae155(self):
        """查询定时任务详情结构化错误解码"""
        run_contract('contract_41157efae155','查询定时任务详情结构化错误解码','schedule_get',['s1'],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_f69ad479ad5f(self):
        """查询定时消息ID结构化错误解码"""
        run_contract('contract_f69ad479ad5f','查询定时消息ID结构化错误解码','schedule_msgs',['s1'],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_d63416f0611c(self):
        """批量查询生命周期结构化错误解码"""
        run_contract('contract_d63416f0611c','批量查询生命周期结构化错误解码','batch_lifecycle',[['m1', 'm2']],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_962a5def6de2(self):
        """批量生命周期数组"""
        run_contract('contract_962a5def6de2','批量生命周期数组','batch_lifecycle',[['m1', 'm2']],200,[{'message_id': 'm1', 'registration_id': 'ridA', 'error_code': 1, 'itime': 1750000000, 'channel': 'engagelab', 'status': 'sent'}, {'message_id': 'm2', 'registration_id': 'ridB', 'error_code': 21003, 'itime': 1750000001, 'channel': 'hmos', 'status': 'failed'}],None,[{'message_id': 'm1', 'registration_id': 'ridA', 'error_code': 1, 'itime': 1750000000, 'channel': 'engagelab', 'status': 'sent'}, {'message_id': 'm2', 'registration_id': 'ridB', 'error_code': 21003, 'itime': 1750000001, 'channel': 'hmos', 'status': 'failed'}],None,3,0)

    def test_contract_383f9f5e575f(self):
        """查询消息生命周期结构化错误解码"""
        run_contract('contract_383f9f5e575f','查询消息生命周期结构化错误解码','lifecycle',['m1', ['ridA', 'ridB']],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_479f6def19ca(self):
        """查询消息统计结构化错误解码"""
        run_contract('contract_479f6def19ca','查询消息统计结构化错误解码','status',[['m1']],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_213b7affc995(self):
        """查询用户统计结构化错误解码"""
        run_contract('contract_213b7affc995','查询用户统计结构化错误解码','users',['DAY', '2026-10-01', 1],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_b55f50ee284c(self):
        """查询计划统计结构化错误解码"""
        run_contract('contract_b55f50ee284c','查询计划统计结构化错误解码','plan_status',[['p1'], '2026-10-01', '2026-10-02'],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_f622e4328613(self):
        """生命周期单条动态RID"""
        run_contract('contract_f622e4328613','生命周期单条动态RID','lifecycle',['m1', ['ridA', 'ridB']],200,{'ridA': {'message_id': 'm1', 'registration_id': 'ridA', 'error_code': 1, 'itime': 1750000000, 'channel': 'engagelab', 'status': 'sent'}, 'ridB': {'message_id': 'm2', 'registration_id': 'ridB', 'error_code': 21003, 'itime': 1750000001, 'channel': 'hmos', 'status': 'failed'}},None,{'ridA': {'message_id': 'm1', 'registration_id': 'ridA', 'error_code': 1, 'itime': 1750000000, 'channel': 'engagelab', 'status': 'sent'}, 'ridB': {'message_id': 'm2', 'registration_id': 'ridB', 'error_code': 21003, 'itime': 1750000001, 'channel': 'hmos', 'status': 'failed'}},None,3,0)

    def test_contract_1f3dc13c7176(self):
        """用户TimeUnit与HMOS"""
        run_contract('contract_1f3dc13c7176','用户TimeUnit与HMOS','users',['DAY', '2026-10-01', 1],200,{'TimeUnit': 'DAY', 'items': [{'time': '2026-10-01', 'hmos': {'new': 7, 'active': 7, 'online': 7}}]},None,{'TimeUnit': 'DAY', 'items': [{'time': '2026-10-01', 'hmos': {'new': 7, 'active': 7, 'online': 7}}]},None,3,0)

    def test_contract_b41ccaa62ad8(self):
        """统计嵌套消息类型"""
        run_contract('contract_b41ccaa62ad8','统计嵌套消息类型','status',[['m1']],200,{'m1': {'plan_id': 'p1', 'pushContent': {'body': {'message': {'msg_content': 'demo'}}}, 'sub': {'live_activity': {'target': 7, 'sent': 6, 'delivered': 5, 'impressions': 4, 'click': 3, 'sub_hmos': {'engageLab_hmos': {'targets': 7, 'sent': 6}, 'harmonyos': {'targets': 7, 'sent': 6}}}, 'voip': {'target': 7, 'sent': 6, 'delivered': 5, 'impressions': 4, 'click': 3, 'sub_hmos': {'engageLab_hmos': {'targets': 7, 'sent': 6}, 'harmonyos': {'targets': 7, 'sent': 6}}}, 'inapp_message': {'target': 7, 'sent': 6, 'delivered': 5, 'impressions': 4, 'click': 3, 'sub_hmos': {'engageLab_hmos': {'targets': 7, 'sent': 6}, 'harmonyos': {'targets': 7, 'sent': 6}}}}}},None,{'m1': {'plan_id': 'p1', 'pushContent': {'body': {'message': {'msg_content': 'demo'}}}, 'sub': {'live_activity': {'target': 7, 'sent': 6, 'delivered': 5, 'impressions': 4, 'click': 3, 'sub_hmos': {'engageLab_hmos': {'targets': 7, 'sent': 6}, 'harmonyos': {'targets': 7, 'sent': 6}}}, 'voip': {'target': 7, 'sent': 6, 'delivered': 5, 'impressions': 4, 'click': 3, 'sub_hmos': {'engageLab_hmos': {'targets': 7, 'sent': 6}, 'harmonyos': {'targets': 7, 'sent': 6}}}, 'inapp_message': {'target': 7, 'sent': 6, 'delivered': 5, 'impressions': 4, 'click': 3, 'sub_hmos': {'engageLab_hmos': {'targets': 7, 'sent': 6}, 'harmonyos': {'targets': 7, 'sent': 6}}}}}},None,3,0)

    def test_contract_666ca276f3cf(self):
        """统计未知字段容忍"""
        run_contract('contract_666ca276f3cf','统计未知字段容忍','status',[['m1']],200,{'m1': {'plan_id': 'p1', 'pushContent': {'body': {'message': {'msg_content': 'demo'}}}, 'sub': {'live_activity': {'target': 7, 'sent': 6, 'delivered': 5, 'impressions': 4, 'click': 3, 'sub_hmos': {'engageLab_hmos': {'targets': 7, 'sent': 6}, 'harmonyos': {'targets': 7, 'sent': 6}}}, 'voip': {'target': 7, 'sent': 6, 'delivered': 5, 'impressions': 4, 'click': 3, 'sub_hmos': {'engageLab_hmos': {'targets': 7, 'sent': 6}, 'harmonyos': {'targets': 7, 'sent': 6}}}, 'inapp_message': {'target': 7, 'sent': 6, 'delivered': 5, 'impressions': 4, 'click': 3, 'sub_hmos': {'engageLab_hmos': {'targets': 7, 'sent': 6}, 'harmonyos': {'targets': 7, 'sent': 6}}}}, 'target_converted': 2}},None,{'m1': {'plan_id': 'p1', 'pushContent': {'body': {'message': {'msg_content': 'demo'}}}, 'sub': {'live_activity': {'target': 7, 'sent': 6, 'delivered': 5, 'impressions': 4, 'click': 3, 'sub_hmos': {'engageLab_hmos': {'targets': 7, 'sent': 6}, 'harmonyos': {'targets': 7, 'sent': 6}}}, 'voip': {'target': 7, 'sent': 6, 'delivered': 5, 'impressions': 4, 'click': 3, 'sub_hmos': {'engageLab_hmos': {'targets': 7, 'sent': 6}, 'harmonyos': {'targets': 7, 'sent': 6}}}, 'inapp_message': {'target': 7, 'sent': 6, 'delivered': 5, 'impressions': 4, 'click': 3, 'sub_hmos': {'engageLab_hmos': {'targets': 7, 'sent': 6}, 'harmonyos': {'targets': 7, 'sent': 6}}}}}},None,3,0)

    def test_contract_9844d9143c0b(self):
        """删除标签结构化错误解码"""
        run_contract('contract_9844d9143c0b','删除标签结构化错误解码','tag_delete',['tag', ['android']],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_740419533058(self):
        """未绑定布尔false"""
        run_contract('contract_740419533058','未绑定布尔false','tag_status',['tag', 'rid'],200,{'result': False},None,{'result': False},None,3,0)

    def test_contract_0e57515cd8f7(self):
        """查询全部标签结构化错误解码"""
        run_contract('contract_0e57515cd8f7','查询全部标签结构化错误解码','tags',[],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_21077ba993f8(self):
        """查询标签设备数结构化错误解码"""
        run_contract('contract_21077ba993f8','查询标签设备数结构化错误解码','tag_count',[['tagA', 'tagB'], 'android'],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_6268f5855c7b(self):
        """查询标签配额结构化错误解码"""
        run_contract('contract_6268f5855c7b','查询标签配额结构化错误解码','tag_quota',[['tagA', 'tagB'], 'android'],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_31f93b123ee7(self):
        """查询设备标签关系结构化错误解码"""
        run_contract('contract_31f93b123ee7','查询设备标签关系结构化错误解码','tag_status',['tag', 'rid'],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_7aef776a16b5(self):
        """标签重复query编码"""
        run_contract('contract_7aef776a16b5','标签重复query编码','tag_count',[['tagA', '标签 空格+&'], 'android'],200,{},None,None,['query', {'tags': ['tagA', '标签 空格+&'], 'platform': ['android']}],3,0)

    def test_contract_08e95382e910(self):
        """设置标签绑定结构化错误解码"""
        run_contract('contract_08e95382e910','设置标签绑定结构化错误解码','tag_set',['tag', {'registration_ids': {'add': ['rid']}}],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_9d690bd51b56(self):
        """配额重复query编码"""
        run_contract('contract_9d690bd51b56','配额重复query编码','tag_quota',[['tagA', 'tagB'], 'android'],200,{},None,None,['query', {'tags': ['tagA', 'tagB'], 'platform': ['android']}],3,0)

    def test_contract_d52a61f55719(self):
        """APNS条件字段缺失透传"""
        run_contract('contract_d52a61f55719','APNS条件字段缺失透传','token',[{'platform': 'ios', 'tokens': ['token0']}],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},{'platform': 'ios', 'tokens': ['token0']},None,None,3,0)

    def test_contract_83da2e7f9f33(self):
        """Token数量0透传"""
        run_contract('contract_83da2e7f9f33','Token数量0透传','token',[{'platform': 'android', 'tokens': []}],200,{'results': []},{'platform': 'android', 'tokens': []},{'results': []},None,3,0)

    def test_contract_701ddbc642e6(self):
        """Token数量1透传"""
        run_contract('contract_701ddbc642e6','Token数量1透传','token',[{'platform': 'android', 'tokens': ['token0']}],200,{'results': []},{'platform': 'android', 'tokens': ['token0']},{'results': []},None,3,0)

    def test_contract_afced1ccc342(self):
        """Token数量500透传"""
        run_contract('contract_afced1ccc342','Token数量500透传','token',[{'platform': 'android', 'tokens': ['token0', 'token1', 'token2', 'token3', 'token4', 'token5', 'token6', 'token7', 'token8', 'token9', 'token10', 'token11', 'token12', 'token13', 'token14', 'token15', 'token16', 'token17', 'token18', 'token19', 'token20', 'token21', 'token22', 'token23', 'token24', 'token25', 'token26', 'token27', 'token28', 'token29', 'token30', 'token31', 'token32', 'token33', 'token34', 'token35', 'token36', 'token37', 'token38', 'token39', 'token40', 'token41', 'token42', 'token43', 'token44', 'token45', 'token46', 'token47', 'token48', 'token49', 'token50', 'token51', 'token52', 'token53', 'token54', 'token55', 'token56', 'token57', 'token58', 'token59', 'token60', 'token61', 'token62', 'token63', 'token64', 'token65', 'token66', 'token67', 'token68', 'token69', 'token70', 'token71', 'token72', 'token73', 'token74', 'token75', 'token76', 'token77', 'token78', 'token79', 'token80', 'token81', 'token82', 'token83', 'token84', 'token85', 'token86', 'token87', 'token88', 'token89', 'token90', 'token91', 'token92', 'token93', 'token94', 'token95', 'token96', 'token97', 'token98', 'token99', 'token100', 'token101', 'token102', 'token103', 'token104', 'token105', 'token106', 'token107', 'token108', 'token109', 'token110', 'token111', 'token112', 'token113', 'token114', 'token115', 'token116', 'token117', 'token118', 'token119', 'token120', 'token121', 'token122', 'token123', 'token124', 'token125', 'token126', 'token127', 'token128', 'token129', 'token130', 'token131', 'token132', 'token133', 'token134', 'token135', 'token136', 'token137', 'token138', 'token139', 'token140', 'token141', 'token142', 'token143', 'token144', 'token145', 'token146', 'token147', 'token148', 'token149', 'token150', 'token151', 'token152', 'token153', 'token154', 'token155', 'token156', 'token157', 'token158', 'token159', 'token160', 'token161', 'token162', 'token163', 'token164', 'token165', 'token166', 'token167', 'token168', 'token169', 'token170', 'token171', 'token172', 'token173', 'token174', 'token175', 'token176', 'token177', 'token178', 'token179', 'token180', 'token181', 'token182', 'token183', 'token184', 'token185', 'token186', 'token187', 'token188', 'token189', 'token190', 'token191', 'token192', 'token193', 'token194', 'token195', 'token196', 'token197', 'token198', 'token199', 'token200', 'token201', 'token202', 'token203', 'token204', 'token205', 'token206', 'token207', 'token208', 'token209', 'token210', 'token211', 'token212', 'token213', 'token214', 'token215', 'token216', 'token217', 'token218', 'token219', 'token220', 'token221', 'token222', 'token223', 'token224', 'token225', 'token226', 'token227', 'token228', 'token229', 'token230', 'token231', 'token232', 'token233', 'token234', 'token235', 'token236', 'token237', 'token238', 'token239', 'token240', 'token241', 'token242', 'token243', 'token244', 'token245', 'token246', 'token247', 'token248', 'token249', 'token250', 'token251', 'token252', 'token253', 'token254', 'token255', 'token256', 'token257', 'token258', 'token259', 'token260', 'token261', 'token262', 'token263', 'token264', 'token265', 'token266', 'token267', 'token268', 'token269', 'token270', 'token271', 'token272', 'token273', 'token274', 'token275', 'token276', 'token277', 'token278', 'token279', 'token280', 'token281', 'token282', 'token283', 'token284', 'token285', 'token286', 'token287', 'token288', 'token289', 'token290', 'token291', 'token292', 'token293', 'token294', 'token295', 'token296', 'token297', 'token298', 'token299', 'token300', 'token301', 'token302', 'token303', 'token304', 'token305', 'token306', 'token307', 'token308', 'token309', 'token310', 'token311', 'token312', 'token313', 'token314', 'token315', 'token316', 'token317', 'token318', 'token319', 'token320', 'token321', 'token322', 'token323', 'token324', 'token325', 'token326', 'token327', 'token328', 'token329', 'token330', 'token331', 'token332', 'token333', 'token334', 'token335', 'token336', 'token337', 'token338', 'token339', 'token340', 'token341', 'token342', 'token343', 'token344', 'token345', 'token346', 'token347', 'token348', 'token349', 'token350', 'token351', 'token352', 'token353', 'token354', 'token355', 'token356', 'token357', 'token358', 'token359', 'token360', 'token361', 'token362', 'token363', 'token364', 'token365', 'token366', 'token367', 'token368', 'token369', 'token370', 'token371', 'token372', 'token373', 'token374', 'token375', 'token376', 'token377', 'token378', 'token379', 'token380', 'token381', 'token382', 'token383', 'token384', 'token385', 'token386', 'token387', 'token388', 'token389', 'token390', 'token391', 'token392', 'token393', 'token394', 'token395', 'token396', 'token397', 'token398', 'token399', 'token400', 'token401', 'token402', 'token403', 'token404', 'token405', 'token406', 'token407', 'token408', 'token409', 'token410', 'token411', 'token412', 'token413', 'token414', 'token415', 'token416', 'token417', 'token418', 'token419', 'token420', 'token421', 'token422', 'token423', 'token424', 'token425', 'token426', 'token427', 'token428', 'token429', 'token430', 'token431', 'token432', 'token433', 'token434', 'token435', 'token436', 'token437', 'token438', 'token439', 'token440', 'token441', 'token442', 'token443', 'token444', 'token445', 'token446', 'token447', 'token448', 'token449', 'token450', 'token451', 'token452', 'token453', 'token454', 'token455', 'token456', 'token457', 'token458', 'token459', 'token460', 'token461', 'token462', 'token463', 'token464', 'token465', 'token466', 'token467', 'token468', 'token469', 'token470', 'token471', 'token472', 'token473', 'token474', 'token475', 'token476', 'token477', 'token478', 'token479', 'token480', 'token481', 'token482', 'token483', 'token484', 'token485', 'token486', 'token487', 'token488', 'token489', 'token490', 'token491', 'token492', 'token493', 'token494', 'token495', 'token496', 'token497', 'token498', 'token499']}],200,{'results': []},{'platform': 'android', 'tokens': ['token0', 'token1', 'token2', 'token3', 'token4', 'token5', 'token6', 'token7', 'token8', 'token9', 'token10', 'token11', 'token12', 'token13', 'token14', 'token15', 'token16', 'token17', 'token18', 'token19', 'token20', 'token21', 'token22', 'token23', 'token24', 'token25', 'token26', 'token27', 'token28', 'token29', 'token30', 'token31', 'token32', 'token33', 'token34', 'token35', 'token36', 'token37', 'token38', 'token39', 'token40', 'token41', 'token42', 'token43', 'token44', 'token45', 'token46', 'token47', 'token48', 'token49', 'token50', 'token51', 'token52', 'token53', 'token54', 'token55', 'token56', 'token57', 'token58', 'token59', 'token60', 'token61', 'token62', 'token63', 'token64', 'token65', 'token66', 'token67', 'token68', 'token69', 'token70', 'token71', 'token72', 'token73', 'token74', 'token75', 'token76', 'token77', 'token78', 'token79', 'token80', 'token81', 'token82', 'token83', 'token84', 'token85', 'token86', 'token87', 'token88', 'token89', 'token90', 'token91', 'token92', 'token93', 'token94', 'token95', 'token96', 'token97', 'token98', 'token99', 'token100', 'token101', 'token102', 'token103', 'token104', 'token105', 'token106', 'token107', 'token108', 'token109', 'token110', 'token111', 'token112', 'token113', 'token114', 'token115', 'token116', 'token117', 'token118', 'token119', 'token120', 'token121', 'token122', 'token123', 'token124', 'token125', 'token126', 'token127', 'token128', 'token129', 'token130', 'token131', 'token132', 'token133', 'token134', 'token135', 'token136', 'token137', 'token138', 'token139', 'token140', 'token141', 'token142', 'token143', 'token144', 'token145', 'token146', 'token147', 'token148', 'token149', 'token150', 'token151', 'token152', 'token153', 'token154', 'token155', 'token156', 'token157', 'token158', 'token159', 'token160', 'token161', 'token162', 'token163', 'token164', 'token165', 'token166', 'token167', 'token168', 'token169', 'token170', 'token171', 'token172', 'token173', 'token174', 'token175', 'token176', 'token177', 'token178', 'token179', 'token180', 'token181', 'token182', 'token183', 'token184', 'token185', 'token186', 'token187', 'token188', 'token189', 'token190', 'token191', 'token192', 'token193', 'token194', 'token195', 'token196', 'token197', 'token198', 'token199', 'token200', 'token201', 'token202', 'token203', 'token204', 'token205', 'token206', 'token207', 'token208', 'token209', 'token210', 'token211', 'token212', 'token213', 'token214', 'token215', 'token216', 'token217', 'token218', 'token219', 'token220', 'token221', 'token222', 'token223', 'token224', 'token225', 'token226', 'token227', 'token228', 'token229', 'token230', 'token231', 'token232', 'token233', 'token234', 'token235', 'token236', 'token237', 'token238', 'token239', 'token240', 'token241', 'token242', 'token243', 'token244', 'token245', 'token246', 'token247', 'token248', 'token249', 'token250', 'token251', 'token252', 'token253', 'token254', 'token255', 'token256', 'token257', 'token258', 'token259', 'token260', 'token261', 'token262', 'token263', 'token264', 'token265', 'token266', 'token267', 'token268', 'token269', 'token270', 'token271', 'token272', 'token273', 'token274', 'token275', 'token276', 'token277', 'token278', 'token279', 'token280', 'token281', 'token282', 'token283', 'token284', 'token285', 'token286', 'token287', 'token288', 'token289', 'token290', 'token291', 'token292', 'token293', 'token294', 'token295', 'token296', 'token297', 'token298', 'token299', 'token300', 'token301', 'token302', 'token303', 'token304', 'token305', 'token306', 'token307', 'token308', 'token309', 'token310', 'token311', 'token312', 'token313', 'token314', 'token315', 'token316', 'token317', 'token318', 'token319', 'token320', 'token321', 'token322', 'token323', 'token324', 'token325', 'token326', 'token327', 'token328', 'token329', 'token330', 'token331', 'token332', 'token333', 'token334', 'token335', 'token336', 'token337', 'token338', 'token339', 'token340', 'token341', 'token342', 'token343', 'token344', 'token345', 'token346', 'token347', 'token348', 'token349', 'token350', 'token351', 'token352', 'token353', 'token354', 'token355', 'token356', 'token357', 'token358', 'token359', 'token360', 'token361', 'token362', 'token363', 'token364', 'token365', 'token366', 'token367', 'token368', 'token369', 'token370', 'token371', 'token372', 'token373', 'token374', 'token375', 'token376', 'token377', 'token378', 'token379', 'token380', 'token381', 'token382', 'token383', 'token384', 'token385', 'token386', 'token387', 'token388', 'token389', 'token390', 'token391', 'token392', 'token393', 'token394', 'token395', 'token396', 'token397', 'token398', 'token399', 'token400', 'token401', 'token402', 'token403', 'token404', 'token405', 'token406', 'token407', 'token408', 'token409', 'token410', 'token411', 'token412', 'token413', 'token414', 'token415', 'token416', 'token417', 'token418', 'token419', 'token420', 'token421', 'token422', 'token423', 'token424', 'token425', 'token426', 'token427', 'token428', 'token429', 'token430', 'token431', 'token432', 'token433', 'token434', 'token435', 'token436', 'token437', 'token438', 'token439', 'token440', 'token441', 'token442', 'token443', 'token444', 'token445', 'token446', 'token447', 'token448', 'token449', 'token450', 'token451', 'token452', 'token453', 'token454', 'token455', 'token456', 'token457', 'token458', 'token459', 'token460', 'token461', 'token462', 'token463', 'token464', 'token465', 'token466', 'token467', 'token468', 'token469', 'token470', 'token471', 'token472', 'token473', 'token474', 'token475', 'token476', 'token477', 'token478', 'token479', 'token480', 'token481', 'token482', 'token483', 'token484', 'token485', 'token486', 'token487', 'token488', 'token489', 'token490', 'token491', 'token492', 'token493', 'token494', 'token495', 'token496', 'token497', 'token498', 'token499']},{'results': []},None,3,0)

    def test_contract_81265228b94b(self):
        """Token数量501透传"""
        run_contract('contract_81265228b94b','Token数量501透传','token',[{'platform': 'android', 'tokens': ['token0', 'token1', 'token2', 'token3', 'token4', 'token5', 'token6', 'token7', 'token8', 'token9', 'token10', 'token11', 'token12', 'token13', 'token14', 'token15', 'token16', 'token17', 'token18', 'token19', 'token20', 'token21', 'token22', 'token23', 'token24', 'token25', 'token26', 'token27', 'token28', 'token29', 'token30', 'token31', 'token32', 'token33', 'token34', 'token35', 'token36', 'token37', 'token38', 'token39', 'token40', 'token41', 'token42', 'token43', 'token44', 'token45', 'token46', 'token47', 'token48', 'token49', 'token50', 'token51', 'token52', 'token53', 'token54', 'token55', 'token56', 'token57', 'token58', 'token59', 'token60', 'token61', 'token62', 'token63', 'token64', 'token65', 'token66', 'token67', 'token68', 'token69', 'token70', 'token71', 'token72', 'token73', 'token74', 'token75', 'token76', 'token77', 'token78', 'token79', 'token80', 'token81', 'token82', 'token83', 'token84', 'token85', 'token86', 'token87', 'token88', 'token89', 'token90', 'token91', 'token92', 'token93', 'token94', 'token95', 'token96', 'token97', 'token98', 'token99', 'token100', 'token101', 'token102', 'token103', 'token104', 'token105', 'token106', 'token107', 'token108', 'token109', 'token110', 'token111', 'token112', 'token113', 'token114', 'token115', 'token116', 'token117', 'token118', 'token119', 'token120', 'token121', 'token122', 'token123', 'token124', 'token125', 'token126', 'token127', 'token128', 'token129', 'token130', 'token131', 'token132', 'token133', 'token134', 'token135', 'token136', 'token137', 'token138', 'token139', 'token140', 'token141', 'token142', 'token143', 'token144', 'token145', 'token146', 'token147', 'token148', 'token149', 'token150', 'token151', 'token152', 'token153', 'token154', 'token155', 'token156', 'token157', 'token158', 'token159', 'token160', 'token161', 'token162', 'token163', 'token164', 'token165', 'token166', 'token167', 'token168', 'token169', 'token170', 'token171', 'token172', 'token173', 'token174', 'token175', 'token176', 'token177', 'token178', 'token179', 'token180', 'token181', 'token182', 'token183', 'token184', 'token185', 'token186', 'token187', 'token188', 'token189', 'token190', 'token191', 'token192', 'token193', 'token194', 'token195', 'token196', 'token197', 'token198', 'token199', 'token200', 'token201', 'token202', 'token203', 'token204', 'token205', 'token206', 'token207', 'token208', 'token209', 'token210', 'token211', 'token212', 'token213', 'token214', 'token215', 'token216', 'token217', 'token218', 'token219', 'token220', 'token221', 'token222', 'token223', 'token224', 'token225', 'token226', 'token227', 'token228', 'token229', 'token230', 'token231', 'token232', 'token233', 'token234', 'token235', 'token236', 'token237', 'token238', 'token239', 'token240', 'token241', 'token242', 'token243', 'token244', 'token245', 'token246', 'token247', 'token248', 'token249', 'token250', 'token251', 'token252', 'token253', 'token254', 'token255', 'token256', 'token257', 'token258', 'token259', 'token260', 'token261', 'token262', 'token263', 'token264', 'token265', 'token266', 'token267', 'token268', 'token269', 'token270', 'token271', 'token272', 'token273', 'token274', 'token275', 'token276', 'token277', 'token278', 'token279', 'token280', 'token281', 'token282', 'token283', 'token284', 'token285', 'token286', 'token287', 'token288', 'token289', 'token290', 'token291', 'token292', 'token293', 'token294', 'token295', 'token296', 'token297', 'token298', 'token299', 'token300', 'token301', 'token302', 'token303', 'token304', 'token305', 'token306', 'token307', 'token308', 'token309', 'token310', 'token311', 'token312', 'token313', 'token314', 'token315', 'token316', 'token317', 'token318', 'token319', 'token320', 'token321', 'token322', 'token323', 'token324', 'token325', 'token326', 'token327', 'token328', 'token329', 'token330', 'token331', 'token332', 'token333', 'token334', 'token335', 'token336', 'token337', 'token338', 'token339', 'token340', 'token341', 'token342', 'token343', 'token344', 'token345', 'token346', 'token347', 'token348', 'token349', 'token350', 'token351', 'token352', 'token353', 'token354', 'token355', 'token356', 'token357', 'token358', 'token359', 'token360', 'token361', 'token362', 'token363', 'token364', 'token365', 'token366', 'token367', 'token368', 'token369', 'token370', 'token371', 'token372', 'token373', 'token374', 'token375', 'token376', 'token377', 'token378', 'token379', 'token380', 'token381', 'token382', 'token383', 'token384', 'token385', 'token386', 'token387', 'token388', 'token389', 'token390', 'token391', 'token392', 'token393', 'token394', 'token395', 'token396', 'token397', 'token398', 'token399', 'token400', 'token401', 'token402', 'token403', 'token404', 'token405', 'token406', 'token407', 'token408', 'token409', 'token410', 'token411', 'token412', 'token413', 'token414', 'token415', 'token416', 'token417', 'token418', 'token419', 'token420', 'token421', 'token422', 'token423', 'token424', 'token425', 'token426', 'token427', 'token428', 'token429', 'token430', 'token431', 'token432', 'token433', 'token434', 'token435', 'token436', 'token437', 'token438', 'token439', 'token440', 'token441', 'token442', 'token443', 'token444', 'token445', 'token446', 'token447', 'token448', 'token449', 'token450', 'token451', 'token452', 'token453', 'token454', 'token455', 'token456', 'token457', 'token458', 'token459', 'token460', 'token461', 'token462', 'token463', 'token464', 'token465', 'token466', 'token467', 'token468', 'token469', 'token470', 'token471', 'token472', 'token473', 'token474', 'token475', 'token476', 'token477', 'token478', 'token479', 'token480', 'token481', 'token482', 'token483', 'token484', 'token485', 'token486', 'token487', 'token488', 'token489', 'token490', 'token491', 'token492', 'token493', 'token494', 'token495', 'token496', 'token497', 'token498', 'token499', 'token500']}],200,{'results': []},{'platform': 'android', 'tokens': ['token0', 'token1', 'token2', 'token3', 'token4', 'token5', 'token6', 'token7', 'token8', 'token9', 'token10', 'token11', 'token12', 'token13', 'token14', 'token15', 'token16', 'token17', 'token18', 'token19', 'token20', 'token21', 'token22', 'token23', 'token24', 'token25', 'token26', 'token27', 'token28', 'token29', 'token30', 'token31', 'token32', 'token33', 'token34', 'token35', 'token36', 'token37', 'token38', 'token39', 'token40', 'token41', 'token42', 'token43', 'token44', 'token45', 'token46', 'token47', 'token48', 'token49', 'token50', 'token51', 'token52', 'token53', 'token54', 'token55', 'token56', 'token57', 'token58', 'token59', 'token60', 'token61', 'token62', 'token63', 'token64', 'token65', 'token66', 'token67', 'token68', 'token69', 'token70', 'token71', 'token72', 'token73', 'token74', 'token75', 'token76', 'token77', 'token78', 'token79', 'token80', 'token81', 'token82', 'token83', 'token84', 'token85', 'token86', 'token87', 'token88', 'token89', 'token90', 'token91', 'token92', 'token93', 'token94', 'token95', 'token96', 'token97', 'token98', 'token99', 'token100', 'token101', 'token102', 'token103', 'token104', 'token105', 'token106', 'token107', 'token108', 'token109', 'token110', 'token111', 'token112', 'token113', 'token114', 'token115', 'token116', 'token117', 'token118', 'token119', 'token120', 'token121', 'token122', 'token123', 'token124', 'token125', 'token126', 'token127', 'token128', 'token129', 'token130', 'token131', 'token132', 'token133', 'token134', 'token135', 'token136', 'token137', 'token138', 'token139', 'token140', 'token141', 'token142', 'token143', 'token144', 'token145', 'token146', 'token147', 'token148', 'token149', 'token150', 'token151', 'token152', 'token153', 'token154', 'token155', 'token156', 'token157', 'token158', 'token159', 'token160', 'token161', 'token162', 'token163', 'token164', 'token165', 'token166', 'token167', 'token168', 'token169', 'token170', 'token171', 'token172', 'token173', 'token174', 'token175', 'token176', 'token177', 'token178', 'token179', 'token180', 'token181', 'token182', 'token183', 'token184', 'token185', 'token186', 'token187', 'token188', 'token189', 'token190', 'token191', 'token192', 'token193', 'token194', 'token195', 'token196', 'token197', 'token198', 'token199', 'token200', 'token201', 'token202', 'token203', 'token204', 'token205', 'token206', 'token207', 'token208', 'token209', 'token210', 'token211', 'token212', 'token213', 'token214', 'token215', 'token216', 'token217', 'token218', 'token219', 'token220', 'token221', 'token222', 'token223', 'token224', 'token225', 'token226', 'token227', 'token228', 'token229', 'token230', 'token231', 'token232', 'token233', 'token234', 'token235', 'token236', 'token237', 'token238', 'token239', 'token240', 'token241', 'token242', 'token243', 'token244', 'token245', 'token246', 'token247', 'token248', 'token249', 'token250', 'token251', 'token252', 'token253', 'token254', 'token255', 'token256', 'token257', 'token258', 'token259', 'token260', 'token261', 'token262', 'token263', 'token264', 'token265', 'token266', 'token267', 'token268', 'token269', 'token270', 'token271', 'token272', 'token273', 'token274', 'token275', 'token276', 'token277', 'token278', 'token279', 'token280', 'token281', 'token282', 'token283', 'token284', 'token285', 'token286', 'token287', 'token288', 'token289', 'token290', 'token291', 'token292', 'token293', 'token294', 'token295', 'token296', 'token297', 'token298', 'token299', 'token300', 'token301', 'token302', 'token303', 'token304', 'token305', 'token306', 'token307', 'token308', 'token309', 'token310', 'token311', 'token312', 'token313', 'token314', 'token315', 'token316', 'token317', 'token318', 'token319', 'token320', 'token321', 'token322', 'token323', 'token324', 'token325', 'token326', 'token327', 'token328', 'token329', 'token330', 'token331', 'token332', 'token333', 'token334', 'token335', 'token336', 'token337', 'token338', 'token339', 'token340', 'token341', 'token342', 'token343', 'token344', 'token345', 'token346', 'token347', 'token348', 'token349', 'token350', 'token351', 'token352', 'token353', 'token354', 'token355', 'token356', 'token357', 'token358', 'token359', 'token360', 'token361', 'token362', 'token363', 'token364', 'token365', 'token366', 'token367', 'token368', 'token369', 'token370', 'token371', 'token372', 'token373', 'token374', 'token375', 'token376', 'token377', 'token378', 'token379', 'token380', 'token381', 'token382', 'token383', 'token384', 'token385', 'token386', 'token387', 'token388', 'token389', 'token390', 'token391', 'token392', 'token393', 'token394', 'token395', 'token396', 'token397', 'token398', 'token399', 'token400', 'token401', 'token402', 'token403', 'token404', 'token405', 'token406', 'token407', 'token408', 'token409', 'token410', 'token411', 'token412', 'token413', 'token414', 'token415', 'token416', 'token417', 'token418', 'token419', 'token420', 'token421', 'token422', 'token423', 'token424', 'token425', 'token426', 'token427', 'token428', 'token429', 'token430', 'token431', 'token432', 'token433', 'token434', 'token435', 'token436', 'token437', 'token438', 'token439', 'token440', 'token441', 'token442', 'token443', 'token444', 'token445', 'token446', 'token447', 'token448', 'token449', 'token450', 'token451', 'token452', 'token453', 'token454', 'token455', 'token456', 'token457', 'token458', 'token459', 'token460', 'token461', 'token462', 'token463', 'token464', 'token465', 'token466', 'token467', 'token468', 'token469', 'token470', 'token471', 'token472', 'token473', 'token474', 'token475', 'token476', 'token477', 'token478', 'token479', 'token480', 'token481', 'token482', 'token483', 'token484', 'token485', 'token486', 'token487', 'token488', 'token489', 'token490', 'token491', 'token492', 'token493', 'token494', 'token495', 'token496', 'token497', 'token498', 'token499', 'token500']},{'results': []},None,3,0)

    def test_contract_b15101d6b2aa(self):
        """已存在映射is_new=false"""
        run_contract('contract_b15101d6b2aa','已存在映射is_new=false','token',[{'platform': 'android', 'tokens': ['token0']}],200,{'results': [{'token': 'token0', 'registration_id': 'rid', 'is_new': False}]},{'platform': 'android', 'tokens': ['token0']},{'results': [{'token': 'token0', 'registration_id': 'rid', 'is_new': False}]},None,3,0)

    def test_contract_a6d8e20902f5(self):
        """未知平台透传"""
        run_contract('contract_a6d8e20902f5','未知平台透传','token',[{'platform': 'future-platform', 'tokens': ['token0']}],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},{'platform': 'future-platform', 'tokens': ['token0']},None,None,3,0)

    def test_contract_d324af9a8d7a(self):
        """沙箱配置false"""
        run_contract('contract_d324af9a8d7a','沙箱配置false','token',[{'platform': 'ios', 'tokens': ['token0'], 'apns_production': False}],200,{'results': []},{'platform': 'ios', 'tokens': ['token0'], 'apns_production': False},{'results': []},None,3,0)

    def test_contract_0c7342223a4e(self):
        """注册单项失败混合结果"""
        run_contract('contract_0c7342223a4e','注册单项失败混合结果','token',[{'platform': 'android', 'tokens': ['token0']}],200,{'results': [{'token': 'token0', 'registration_id': 'rid', 'is_new': False}, {'token': 'bad', 'code': 21003, 'message': 'invalid token'}]},{'platform': 'android', 'tokens': ['token0']},{'results': [{'token': 'token0', 'registration_id': 'rid', 'is_new': False}, {'token': 'bad', 'code': 21003, 'message': 'invalid token'}]},None,3,0)

    def test_contract_9e76c34d12a5(self):
        """注册厂商Token结构化错误解码"""
        run_contract('contract_9e76c34d12a5','注册厂商Token结构化错误解码','token',[{'platform': 'android', 'tokens': ['tokenA']}],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_00a48e0d33e4(self):
        """Brazil数据中心"""
        run_contract('contract_00a48e0d33e4','Brazil数据中心','host',['brazil'],200,{'request_id': 'r1', 'msg_id': '123'},None,None,'host',3,0)

    def test_contract_ba12151237d3(self):
        """HTTP429错误"""
        run_contract('contract_ba12151237d3','HTTP429错误','validate',[{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}}}],429,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_93eab3c67c09(self):
        """HTTP500错误"""
        run_contract('contract_93eab3c67c09','HTTP500错误','validate',[{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}}}],500,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_c48149375f68(self):
        """Japan数据中心"""
        run_contract('contract_c48149375f68','Japan数据中心','host',['japan'],200,{'request_id': 'r1', 'msg_id': '123'},None,None,'host',3,0)

    def test_contract_5d4b8a45f876(self):
        """同客户端并发隔离"""
        run_contract('contract_5d4b8a45f876','同客户端并发隔离','concurrent',[],200,'ECHO',None,None,'concurrent',3,0)

    def test_contract_84cd3124faa6(self):
        """敏感凭据不泄露"""
        run_contract('contract_84cd3124faa6','敏感凭据不泄露','validate',[{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}}}],200,{'request_id': 'r1', 'msg_id': '123'},None,None,'logs',3,0)

    def test_contract_382a447fdc76(self):
        """未知响应字段兼容"""
        run_contract('contract_382a447fdc76','未知响应字段兼容','validate',[{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}}}],200,{'request_id': 'r1', 'msg_id': '123', 'future_field': {'x': 1}},None,{'request_id': 'r1', 'msg_id': '123'},None,3,0)

    def test_contract_d6f29da0febe(self):
        """自定义BaseURL"""
        run_contract('contract_d6f29da0febe','自定义BaseURL','validate',[{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}}}],200,{'request_id': 'r1', 'msg_id': '123'},None,None,None,3,0)

    def test_contract_bc871ae6520c(self):
        """认证编码"""
        run_contract('contract_bc871ae6520c','认证编码','validate',[{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}}}],200,{'request_id': 'r1', 'msg_id': '123'},None,None,'auth',3,0)

    def test_contract_e990cb46d18c(self):
        """超时错误"""
        run_contract('contract_e990cb46d18c','超时错误','validate',[{'to': {'registration_id': ['rid']}, 'body': {'platform': ['android'], 'notification': {'alert': 'demo'}}}],200,{'request_id': 'r1', 'msg_id': '123'},None,None,'timeout',0.1,0.7)

    def test_contract_02b13ad92165(self):
        """默认Singapore"""
        run_contract('contract_02b13ad92165','默认Singapore','host',['default'],200,{'request_id': 'r1', 'msg_id': '123'},None,None,'host',3,0)

    def test_contract_f4762dac11b5(self):
        """VIP到期时间64位"""
        run_contract('contract_f4762dac11b5','VIP到期时间64位','vip',[],200,{'vip_status': 1, 'vip_end_time': 2147483648},None,{'vip_status': 1, 'vip_end_time': 2147483648},None,3,0)

    def test_contract_7381a2144b72(self):
        """查询应用VIP状态结构化错误解码"""
        run_contract('contract_7381a2144b72','查询应用VIP状态结构化错误解码','vip',[],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_118ff86b6453(self):
        """非VIP状态零值"""
        run_contract('contract_118ff86b6453','非VIP状态零值','vip',[],200,{'vip_status': 0, 'vip_end_time': 0},None,{'vip_status': 0, 'vip_end_time': 0},None,3,0)

    def test_contract_a0fcc96cfdc2(self):
        """multipart文件字节保真"""
        run_contract('contract_a0fcc96cfdc2','multipart文件字节保真','voice_create',['en', '__NATIVE_TEMP_WAV__'],200,{'language': 'en', 'file_url': 'https://example.test/a.wav'},None,None,'multipart',3,0)

    def test_contract_96231d59a4b6(self):
        """上传语音文件结构化错误解码"""
        run_contract('contract_96231d59a4b6','上传语音文件结构化错误解码','voice_create',['en', '__NATIVE_TEMP_WAV__'],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_c7368dd7959e(self):
        """删除语音模板结构化错误解码"""
        run_contract('contract_c7368dd7959e','删除语音模板结构化错误解码','voice_delete',['en'],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_51abea20bc7a(self):
        """查询语音列表结构化错误解码"""
        run_contract('contract_51abea20bc7a','查询语音列表结构化错误解码','voices',[],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_e47b273c2502(self):
        """查询语音详情结构化错误解码"""
        run_contract('contract_e47b273c2502','查询语音详情结构化错误解码','voice_get',['en'],400,{'error': {'code': 21003, 'message': 'fixture-invalid'}},None,None,None,3,0)

    def test_contract_047f5e08356c(self):
        """语音列表直接数组"""
        run_contract('contract_047f5e08356c','语音列表直接数组','voices',[],200,[{'language': 'en', 'file_url': 'https://example.test/a.wav'}],None,[{'language': 'en', 'file_url': 'https://example.test/a.wav'}],None,3,0)

    def test_contract_8847f227b271(self):
        """语音列表空数组"""
        run_contract('contract_8847f227b271','语音列表空数组','voices',[],200,[],None,[],None,3,0)
