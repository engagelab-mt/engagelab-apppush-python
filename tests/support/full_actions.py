import sys,json,os,dataclasses,typing

import engagelab

from engagelab.client import Client

from engagelab.group_push import GroupPushClient

from engagelab import push,device,tag,schedule,plan,image

from engagelab._serialization import to_dict

MODELS={'push':push.PushParam,'validate':push.PushParam,'push_raw':None,'batch_regid':push.BatchPushParam,'batch_alias':push.BatchPushParam,'device_set':device.DeviceSetParam,'device_status':device.DeviceStatusGetParam,'token':device.DeviceTokenRegisterParam,'tag_set':tag.TagSetParam,'schedule_create':schedule.SchedulePushParam,'schedule_update':schedule.SchedulePushParam,'plan_create':plan.PushPlanParam,'image':image.OppoImageParam,'group':push.PushParam}

METHODS={'push':('push','send'),'validate':('push','validate'),'push_raw':('push','send_raw'),'batch_regid':('push','batch_by_regid'),'batch_alias':('push','batch_by_alias'),'withdraw':('push','withdraw'),'device_get':('device','get'),'device_set':('device','set'),'device_delete':('device','delete'),'device_status':('device','get_status'),'token':('device','register_token'),'tags':('tag','list'),'tag_status':('tag','get_device_status'),'tag_set':('tag','set'),'tag_delete':('tag','delete'),'tag_count':('tag','get_count'),'tag_quota':('tag','get_quota'),'alias_get':('alias','get'),'alias_delete':('alias','delete'),'schedule_create':('schedule','create'),'schedule_update':('schedule','update'),'schedule_delete':('schedule','delete'),'schedule_get':('schedule','get'),'schedule_list':('schedule','list'),'schedule_msgs':('schedule','get_msg_ids'),'status':('status','message_detail'),'users':('status','users'),'lifecycle':('status','message_lifecycle'),'batch_lifecycle':('status','batch_message_detail'),'plan_status':('status','plan_detail'),'plan_create':('plan','create_or_update'),'plan_list':('plan','list'),'plan_msgs':('plan','query_msg'),'plan_delete':('plan','delete'),'plan_batch_delete':('plan','batch_delete'),'voice_create':('voice','create'),'voices':('voice','list'),'voice_get':('voice','get'),'voice_delete':('voice','delete'),'image':('image','upload_oppo'),'vip':('app','get_vip_status')}

def model(cls,data):
    if not dataclasses.is_dataclass(cls) or not isinstance(data,dict):return data
    hints=typing.get_type_hints(cls);maps=getattr(cls,'_FIELD_MAP',{});kw={}
    for f in dataclasses.fields(cls):
        key=maps.get(f.name,f.name)
        if key not in data:continue
        typ=hints[f.name];v=data[key];opts=typing.get_args(typ)
        if typing.get_origin(typ) is typing.Union:
            typ=next((t for t in opts if dataclasses.is_dataclass(t) and isinstance(v,dict)),next((t for t in opts if t is not type(None)),typing.Any))
        if dataclasses.is_dataclass(typ):v=model(typ,v)
        elif typing.get_origin(typ) is list and typing.get_args(typ):v=[model(typing.get_args(typ)[0],i) for i in v]
        kw[f.name]=v
    return cls(**kw)

def serial(v):
    if dataclasses.is_dataclass(v):
        names=getattr(type(v),'_FIELD_MAP',{})
        return {names.get(f.name,f.name):serial(getattr(v,f.name)) for f in dataclasses.fields(v)}
    if isinstance(v,dict):return {k:serial(x) for k,x in v.items()}
    if isinstance(v,list):return [serial(x) for x in v]
    if hasattr(v,'__dict__'):return serial(v.__dict__)
    return v


class Actions:
    def __init__(self, base, key='test-key', secret='test-secret', timeout=3, group_key='group-key', group_secret='group-secret'):
        self.client = Client(key, secret, base_url=base, timeout=timeout)
        self.group = GroupPushClient(group_key, group_secret, base_url=base, timeout=timeout)
    def call(self, op, args):
        import copy
        args = copy.deepcopy(args)
        if op == 'schedule_raw':
            return serial(self.client.schedule.create(args[0]))
        if op == 'legacy_pushbody':
            return serial(self.client.push.validate(push.PushParam(to={'registration_id':['rid']}, body=push.PushBody(['android'],None,None,None,push.Options(auto_truncation=False)))))
        if op in MODELS and MODELS[op] and args:
            args[-1] = model(MODELS[op], args[-1])
        if op == 'group':
            return serial(self.group.send(args[0]))
        service, method = METHODS[op]
        return serial(getattr(getattr(self.client,service),method)(*args))
