"""Complete native QA workflows; compiled business assertions, no testcase loader."""
from .full_qa import *
T=True
F=False
N=None

def devices(c):
    c.write()
    d1 = c.seedDevice()
    d2 = c.seedDevice()
    tag1 = c.prefix + "_a"
    tag2 = c.prefix + "_b"
    tag3 = c.prefix + "_del"
    alias = c.prefix + "_alias"
    c.rest("POST","/v4/devices/"+txt(d1),m("tags","","alias",""))
    c.seedTag(tag1,d1)
    c.seedAlias(alias,d1)
    r = c.sdk("device_get",arr(d1))
    raw = c.device(d1)
    c.record('qa_48e10c8c3688',m('HTTP200',eq(g(r,"status"),200),'known_tags',sets(g(r,"data","tags"),arr(tag1)),'known_alias',eq(g(r,"data","alias"),alias),'wire_fields',same(g(r,"data"),g(r,"raw"))),T,'')
    r = c.sdk("alias_get",arr(alias,arr("android")))
    c.record('qa_4228ae60b590',m('HTTP200',eq(g(r,"status"),200),'exact_binding',sets(g(r,"data","registration_ids"),arr(d1)),'wire_fields',same(g(r,"data"),g(r,"raw"))),T,'')
    r = c.sdk("alias_delete",arr(alias,arr("android")))
    raw = c.device(d1)
    binding = c.rest("GET","/v4/aliases/"+alias+"?platform=android",N)
    c.record('qa_f76445835b7d',m('SDK_success',yes(g(r,"ok")),'device_alias_empty',eq(txt(g(raw,"data","alias")),""),'alias_unbound',no(includes(g(binding,"data","registration_ids"),d1))),T,'')
    c.rest("POST","/v4/devices/"+txt(d1),m("tags",""))
    c.seedTag(tag2,d1)
    r = c.sdk("device_set",arr(d1,m("tags",m("add",arr(tag1),"remove",arr(tag2)),"alias",alias)))
    raw = c.device(d1)
    c.record('qa_3a16670b310f',m('SDK_success',yes(g(r,"ok")),'tags_add_remove',sets(g(raw,"data","tags"),arr(tag1)),'alias_written',eq(g(raw,"data","alias"),alias)),T,'')
    c.seedTag(tag2,d1)
    r = c.sdk("device_set",arr(d1,m("tags","")))
    raw = c.device(d1)
    a = c.relation(tag1,d1)
    b = c.relation(tag2,d1)
    c.record('qa_418e812084ee',m('SDK_success',yes(g(r,"ok")),'tags_empty',eq(size(g(raw,"data","tags")),0),'both_false',both(no(g(a,"data","result")),no(g(b,"data","result")))),T,'')
    c.seedTag(tag1,d1)
    c.seedTag(tag2,d2)
    r = c.sdk("tags",arr())
    c.record('qa_00cbd3d800bd',m('HTTP200',eq(g(r,"status"),200),'two_seeded_tags',both(includes(g(r,"data","tags"),tag1),includes(g(r,"data","tags"),tag2))),T,'')
    r = c.sdk("tag_status",arr(tag1,d1))
    c.record('qa_a925a3248bcd',m('HTTP200',eq(g(r,"status"),200),'typed_true',yes(g(r,"data","result"))),T,'')
    r = c.sdk("tag_count",arr(arr(tag1,tag2),"android"))
    c.record('qa_d5581d7d5601',m('HTTP200',eq(g(r,"status"),200),'two_known_single_counts',both(eq(g(r,"data","tagsCount",tag1),1),eq(g(r,"data","tagsCount",tag2),1)),'repeated_tags_query',sets(g(r,"query","tags"),arr(tag1,tag2))),T,'')
    r = c.sdk("tag_quota",arr(arr(tag1,tag2),"android"))
    c.record('qa_5f8b9b9d7f78',m('HTTP200',eq(g(r,"status"),200),'repeated_tags_query',sets(g(r,"query","tags"),arr(tag1,tag2)),'nonempty_known_quotas',both(includes(ids(g(r,"raw","data","tagUidQuotaDetail"),"tagName"),tag1),includes(ids(g(r,"raw","data","tagUidQuotaDetail"),"tagName"),tag2)),'wire_fields',same(g(r,"data"),g(r,"raw"))),T,'')
    c.rest("POST","/v4/devices/"+txt(d1),m("tags",""))
    c.rest("POST","/v4/devices/"+txt(d2),m("tags",""))
    c.seedTag(tag1,d2)
    r = c.sdk("tag_set",arr(tag1,m("registration_ids",m("add",arr(d1),"remove",arr(d2)))))
    a = c.relation(tag1,d1)
    b = c.relation(tag1,d2)
    c.record('qa_83ba432b89af',m('SDK_success',yes(g(r,"ok")),'A_true_B_false',both(yes(g(a,"data","result")),no(g(b,"data","result")))),T,'')
    c.seedTag(tag3,d1)
    r = c.sdk("tag_delete",arr(tag3,arr("android")))
    raw = c.rest("GET","/v4/tags/",N)
    a = c.relation(tag3,d1)
    c.record('qa_ff6fe44cc46d',m('SDK_success',yes(g(r,"ok")),'tag_absent',no(includes(g(raw,"data","tags"),tag3)),'relation_false',no(g(a,"data","result"))),T,'')
    r = c.sdk("device_status",arr(m("registration_ids",arr(d1,d2))))
    c.record('qa_edfec6f68242',m('HTTP200',eq(g(r,"status"),200),'two_known_offline_records',both(eq(size(g(r,"data")),2),sets(ids(g(r,"data"),"regid"),arr(d1,d2)),no(g(r,"data",0,"online")),no(g(r,"data",1,"online")))),T,'')
    r = c.sdk("device_delete",arr(d2))
    raw = c.device(d2)
    a = c.relation(tag2,d2)
    c.record('qa_42caca08cb39',m('SDK_success',yes(g(r,"ok")),'device_absent',eq(g(raw,"data","error","code"),27002),'old_relations_inaccessible',eq(g(a,"data","error","code"),27002)),T,'')

def plans(c):
    c.write()
    first = c.seedPlans(101)
    prefix = c.prefix
    r = c.sdk("plan_list",arr(1,101,N,prefix))
    c.record('qa_bbef5f838820',m('SDK_HTTP200',eq(g(first,"status"),200),'created_readback',includes(ids(g(r,"data","push_plan_info"),"plan_id"),g(first,"data","plan_id"))),T,'')
    c.record('qa_0e01ec2f278a',m('HTTP200',eq(g(r,"status"),200),'count101',eq(g(r,"data","total"),101),'all_fields',same(g(r,"data"),g(r,"raw"))),T,'')
    c.record('qa_2d67bd95bf58',m('HTTP200',eq(g(r,"status"),200),'total101',eq(g(r,"data","total"),101),'count101',eq(size(g(r,"data","push_plan_info")),101),'owned_ids_exact',sets(ids(g(r,"data","push_plan_info"),"plan_id"),c.planIDs()),'wire_fields',same(g(r,"data"),g(r,"raw")),'query101',eq(g(r,"query","page_size",0),"101")),T,'')
    r = c.sdk("plan_list",arr(1,100,N,prefix))
    c.record('qa_452338f7f0cb',m('HTTP200',eq(g(r,"status"),200),'page100',eq(size(g(r,"data","push_plan_info")),100),'wire_fields',same(g(r,"data"),g(r,"raw"))),T,'')
    a = c.sdk("plan_list",arr(1,1,N,prefix))
    c.record('qa_d1c2dc88ee2a',m('HTTP200',eq(g(a,"status"),200),'one_item',eq(size(g(a,"data","push_plan_info")),1),'wire_fields',same(g(a,"data"),g(a,"raw"))),T,'')
    b = c.sdk("plan_list",arr(2,1,N,prefix))
    c.record('qa_1068750e639d',m('HTTP200',eq(g(b,"status"),200),'one_item',eq(size(g(b,"data","push_plan_info")),1),'different_from_first',no(eq(g(a,"data","push_plan_info",0,"plan_id"),g(b,"data","push_plan_info",0,"plan_id"))),'wire_fields',same(g(b,"data"),g(b,"raw"))),T,'')
    r = c.sdk("plan_list",arr(1,0,N,prefix))
    control = c.listPlans(prefix,0,1,N)
    c.record('qa_c32bda243404',m('SDK_rejected',no(g(r,"ok")),'HTTP_code_message_match',c.errorsEqual(r,control)),T,'')
    pid = g(first,"data","plan_id")
    description = prefix+"_更新"
    r = c.sdk("plan_create",arr(m("plan_id",pid,"plan_description",description)))
    raw = c.listPlans(description,101,1,N)
    c.record('qa_ee67b55b2f74',m('SDK_success',yes(g(r,"ok")),'single_updated',both(eq(g(raw,"data","total"),1),eq(g(raw,"data","push_plan_info",0,"plan_description"),description))),T,'')
    r = c.sdk("plan_list",arr(1,101,N,description))
    c.record('qa_3e98ca439abe',m('HTTP200',eq(g(r,"status"),200),'one_UTF8_match',both(eq(g(r,"data","total"),1),eq(g(r,"data","push_plan_info",0,"plan_description"),description)),'UTF8_query',eq(g(r,"query","search_description",0),description)),T,'')
    r = c.sdk("plan_list",arr(1,101,0,prefix))
    raw = c.listPlans(prefix,101,1,0)
    c.record('qa_a8afa2ba63c2',m('HTTP200',eq(g(r,"status"),200),'API_known_records',eq(g(r,"data","total"),101),'source_query',eq(g(r,"query","send_source",0),"0"),'REST_agrees',same(g(r,"data"),g(raw,"data"))),T,'')
    r = c.sdk("plan_list",arr(1,1,0,description))
    c.record('qa_6df4ebb6c583',m('HTTP200',eq(g(r,"status"),200),'all_four_queries',both(eq(g(r,"query","page_index",0),"1"),eq(g(r,"query","page_size",0),"1"),eq(g(r,"query","send_source",0),"0"),eq(g(r,"query","search_description",0),description)),'single_correct_item',both(eq(g(r,"data","total"),1),eq(g(r,"data","push_plan_info",0,"plan_id"),pid))),T,'')
    r = c.sdk("plan_delete",arr(pid))
    raw = c.listPlans(prefix,101,1,N)
    c.record('qa_793b07888b66',m('SDK_success',yes(g(r,"ok")),'plan_absent',no(includes(ids(g(raw,"data","push_plan_info"),"plan_id"),pid))),T,'')
    pair = c.batchPlanPair(pid)
    r = c.sdk("plan_batch_delete",arr(c.join(pair)))
    raw = c.listPlans(prefix,101,1,N)
    c.record('qa_7c9f085a13ea',m('SDK_success',yes(g(r,"ok")),'comma_path',eq(g(r,"path"),"/v4/push_plan/batch/"+c.join(pair)),'both_absent',c.noneIn(pair,ids(g(raw,"data","push_plan_info"),"plan_id"))),T,'')
    r = c.planBoundary(1)
    c.record('qa_0df5c6ed2605',m('expected_outcome',yes(g(r,"verified"))),yes(g(r,"ready")),'No unused one-character plan ID available')
    r = c.planBoundary(49)
    c.record('qa_2e34db0cb38c',m('expected_outcome',yes(g(r,"verified"))),yes(g(r,"ready")),'No unused one-character plan ID available')
    r = c.planBoundary(50)
    c.record('qa_eeb26ebb2b07',m('expected_outcome',yes(g(r,"verified"))),yes(g(r,"ready")),'No unused one-character plan ID available')
    r = c.planBoundary(51)
    c.record('qa_d71d62850538',m('expected_outcome',yes(g(r,"verified"))),yes(g(r,"ready")),'No unused one-character plan ID available')

def batch(c):
    c.write()
    d1 = c.targetRID(0)
    d2 = c.targetRID(1)
    alias1 = c.prefix+"_1"
    alias2 = c.prefix+"_2"
    c.seedAlias(alias1,d1)
    c.seedAlias(alias2,d2)
    r = c.batch("batch_regid",arr(d1,d2))
    c.record('qa_81f620c4cc20',m('HTTP200',eq(g(r,"status"),200),'all_target_successes',c.batchResultsValid(r,arr(d1,d2)),'wire_fields',same(g(r,"data"),g(r,"raw")),'message_linkage',yes(g(r,"messages_persisted"))),T,'')
    r = c.batch("batch_alias",arr(alias1,alias2))
    c.record('qa_d7b1b6768d39',m('HTTP200',eq(g(r,"status"),200),'all_target_successes',c.batchResultsValid(r,arr(alias1,alias2)),'wire_fields',same(g(r,"data"),g(r,"raw")),'message_linkage',yes(g(r,"messages_persisted"))),T,'')

def negative(c):
    r = c.negative("empty")
    c.record('qa_f0179b307f6b',m('rejected_like_REST',yes(g(r,"verified"))),T,'')
    r = c.negative("platform")
    c.record('qa_65322fbec684',m('legacy_error_like_REST',yes(g(r,"verified"))),T,'')
    r = c.negative("message")
    c.record('qa_a62eda72d0a4',m('single_type_controls_valid',yes(g(r,"controls_valid")),'same_HTTP_code_message',yes(g(r,"verified"))),yes(g(r,"controls_valid")),'Cannot validate mutual exclusion without accepted single-type controls')
    r = c.negative("notification")
    c.record('qa_358fd717fbad',m('single_type_controls_valid',yes(g(r,"controls_valid")),'same_HTTP_code_message',yes(g(r,"verified"))),yes(g(r,"controls_valid")),'Cannot validate mutual exclusion without accepted single-type controls')
    r = c.negative("live_activity")
    c.record('qa_f27bda2df7c2',m('single_type_controls_valid',yes(g(r,"controls_valid")),'same_HTTP_code_message',yes(g(r,"verified"))),yes(g(r,"controls_valid")),'Cannot validate mutual exclusion without accepted single-type controls')

def auth(c):
    r = c.sdk("vip",arr())
    c.record('qa_861607f5c661',m('HTTP200',eq(g(r,"status"),200),'integer_status_and_64bit_expiry',c.vipValid(r),'wire_fields',same(g(r,"data"),g(r,"raw"))),T,'')
    r = c.invalidAuth()
    c.record('qa_99b351df6c47',m('REST_and_SDK_reject',yes(g(r,"verified"))),T,'')

def token(c):
    c.write()
    r = c.apnsToken()
    c.record('qa_113173a66889',m('fields_match_wire',yes(g(r,"verified")),'mapping_preserved_or_cleaned',yes(g(r,"cleanup"))),T,'')

def group(c):
    c.write()
    r = c.groupPush()
    c.record('qa_992ab0e0747a',m('two_dynamic_members',yes(g(r,"verified")),'explicit_alias_only',yes(g(r,"explicit_target"))),T,'')

def image(c):
    c.write()
    r = c.imageUpload()
    c.record('qa_b0478ec2b424',m('eligible_984x369_resource',yes(g(r,"resource_valid")),'HTTP_and_picture_ID_exact',yes(g(r,"verified"))),yes(g(r,"prerequisite")),'QA/vendor image capability unavailable; inspect native response code')

def voice(c):
    c.write()
    r = c.prepareVoice()
    c.record('qa_bd03c2bacf73',m('multipart_and_fields',yes(g(r,"upload_verified")),'detail_matches_upload',yes(g(r,"detail_verified"))),T,'')
    c.record('qa_a4be39a4d66b',m('direct_array_and_known_template',yes(g(r,"list_verified"))),T,'')
    c.record('qa_c7377d6722fc',m('file_url_matches',yes(g(r,"detail_verified"))),T,'')
    r = c.deleteVoice()
    c.record('qa_95007431d632',m('SDK_success',yes(g(r,"sdk_ok")),'list_and_detail_absent',yes(g(r,"verified"))),T,'')

def schedule(c):
    c.write()
    r = c.prepareSchedules()
    c.record('qa_cc992174acf7',m('native_business_assertions',yes(g(r,"create"))),yes(g(r,"create_ready")),'Scheduled task, timezone/activity, or positive trigger prerequisite not established')
    c.record('qa_fbe62ef8b3e7',m('native_business_assertions',yes(g(r,"get"))),yes(g(r,"get_ready")),'Scheduled task, timezone/activity, or positive trigger prerequisite not established')
    c.record('qa_c69b89ef022d',m('native_business_assertions',yes(g(r,"list"))),yes(g(r,"list_ready")),'Scheduled task, timezone/activity, or positive trigger prerequisite not established')
    c.record('qa_f47503d90583',m('native_business_assertions',yes(g(r,"intelligent"))),yes(g(r,"intelligent_ready")),'Scheduled task, timezone/activity, or positive trigger prerequisite not established')
    c.record('qa_b1336ed19443',m('native_business_assertions',yes(g(r,"messages"))),yes(g(r,"messages_ready")),'Scheduled task, timezone/activity, or positive trigger prerequisite not established')
    c.record('qa_0359444e46a9',m('native_business_assertions',yes(g(r,"update"))),yes(g(r,"update_ready")),'Scheduled task, timezone/activity, or positive trigger prerequisite not established')
    c.record('qa_cbbfd7d59d01',m('native_business_assertions',yes(g(r,"delete"))),yes(g(r,"delete_ready")),'Scheduled task, timezone/activity, or positive trigger prerequisite not established')

def stats(c):
    c.write()
    r = c.prepareStatistics()
    c.record('qa_06327bbf436b',m('nonempty_known_business_data_and_fields',yes(g(r,"message"))),yes(g(r,"message_ready")),'Known message/RID/plan relation or nonzero HMOS statistics not available in bounded observation window')
    c.record('qa_cc281fbd1340',m('nonempty_known_business_data_and_fields',yes(g(r,"lifecycle"))),yes(g(r,"lifecycle_ready")),'Known message/RID/plan relation or nonzero HMOS statistics not available in bounded observation window')
    c.record('qa_6f9ed781a410',m('nonempty_known_business_data_and_fields',yes(g(r,"batch_lifecycle"))),yes(g(r,"batch_lifecycle_ready")),'Known message/RID/plan relation or nonzero HMOS statistics not available in bounded observation window')
    c.record('qa_0c64e79794cc',m('nonempty_known_business_data_and_fields',yes(g(r,"users"))),yes(g(r,"users_ready")),'Known message/RID/plan relation or nonzero HMOS statistics not available in bounded observation window')
    c.record('qa_29349c0683f5',m('nonempty_known_business_data_and_fields',yes(g(r,"plan"))),yes(g(r,"plan_ready")),'Known message/RID/plan relation or nonzero HMOS statistics not available in bounded observation window')
    c.record('qa_cb8dc4d08772',m('nonempty_known_business_data_and_fields',yes(g(r,"plan_messages"))),yes(g(r,"plan_messages_ready")),'Known message/RID/plan relation or nonzero HMOS statistics not available in bounded observation window')

def physical(c):
    r = c.physicalNotifications()
    c.record('qa_e9617155db83',m('native_API_and_physical_notification_assertions',yes(g(r,"push"))),yes(g(r,"push_ready")),'Matching QA application and physical notification observation are required')
    c.record('qa_f5308cfc2d09',m('native_API_and_physical_notification_assertions',yes(g(r,"validate"))),yes(g(r,"validate_ready")),'Matching QA application and physical notification observation are required')
    c.record('qa_db1a22ee70da',m('native_API_and_physical_notification_assertions',yes(g(r,"withdraw"))),yes(g(r,"withdraw_ready")),'Matching QA application and physical notification observation are required')

GROUPS={'devices':devices,'plans':plans,'batch':batch,'negative':negative,'auth':auth,'token':token,'group':group,'image':image,'voice':voice,'schedule':schedule,'stats':stats,'physical':physical}
GROUP_IDS={'devices': ['qa_48e10c8c3688', 'qa_4228ae60b590', 'qa_f76445835b7d', 'qa_3a16670b310f', 'qa_418e812084ee', 'qa_00cbd3d800bd', 'qa_a925a3248bcd', 'qa_d5581d7d5601', 'qa_5f8b9b9d7f78', 'qa_83ba432b89af', 'qa_ff6fe44cc46d', 'qa_edfec6f68242', 'qa_42caca08cb39'], 'plans': ['qa_bbef5f838820', 'qa_0e01ec2f278a', 'qa_2d67bd95bf58', 'qa_452338f7f0cb', 'qa_d1c2dc88ee2a', 'qa_1068750e639d', 'qa_c32bda243404', 'qa_ee67b55b2f74', 'qa_3e98ca439abe', 'qa_a8afa2ba63c2', 'qa_6df4ebb6c583', 'qa_793b07888b66', 'qa_7c9f085a13ea', 'qa_0df5c6ed2605', 'qa_2e34db0cb38c', 'qa_eeb26ebb2b07', 'qa_d71d62850538'], 'batch': ['qa_81f620c4cc20', 'qa_d7b1b6768d39'], 'negative': ['qa_f0179b307f6b', 'qa_65322fbec684', 'qa_a62eda72d0a4', 'qa_358fd717fbad', 'qa_f27bda2df7c2'], 'auth': ['qa_861607f5c661', 'qa_99b351df6c47'], 'token': ['qa_113173a66889'], 'group': ['qa_992ab0e0747a'], 'image': ['qa_b0478ec2b424'], 'voice': ['qa_bd03c2bacf73', 'qa_a4be39a4d66b', 'qa_c7377d6722fc', 'qa_95007431d632'], 'schedule': ['qa_cc992174acf7', 'qa_fbe62ef8b3e7', 'qa_c69b89ef022d', 'qa_f47503d90583', 'qa_b1336ed19443', 'qa_0359444e46a9', 'qa_cbbfd7d59d01'], 'stats': ['qa_06327bbf436b', 'qa_cc281fbd1340', 'qa_6f9ed781a410', 'qa_0c64e79794cc', 'qa_29349c0683f5', 'qa_cb8dc4d08772'], 'physical': ['qa_e9617155db83', 'qa_f5308cfc2d09', 'qa_db1a22ee70da']}
CACHE={}
def execute(group,sid):
    if group not in CACHE:
        ctx=None;results={}
        try:
            ctx=QAContext()
            GROUPS[group](ctx)
        except Exception as error:
            status='block' if isinstance(error,Blocked) else 'no_pass'
            reason=str(error) if isinstance(error,Blocked) else 'Native workflow exception: '+type(error).__name__
            for key in GROUP_IDS[group]:
                if ctx is None or key not in ctx.results:results[key]=dict(status=status,reason=reason,checks={})
        finally:
            if ctx is not None:
                ctx.clean()
                results.update(ctx.results)
        CACHE[group]=results
    result=CACHE[group][sid]
    save(sid,result['status'],result['checks'],result.get('reason',''),'integration')
    if result['status']!='pass':raise AssertionError(result['status']+': '+result.get('reason','business assertion failed'))
