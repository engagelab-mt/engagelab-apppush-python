"""Native real-service orchestration and assertions; no TAPD/case-file dependency."""
import base64,contextlib,io,json,math,os,re,subprocess,tempfile,time,urllib.error,urllib.parse,urllib.request,uuid,wave,threading,zipfile,shlex
from pathlib import Path
from datetime import datetime,timedelta,timezone
from unittest.mock import patch
from engagelab.errors import ApiError
from .native import Config,Blocked,check
from .full_actions import Actions
from .full_contract import contains,save,canonical


def m(*values):return dict(zip(values[::2],values[1::2]))
def arr(*values):return list(values)
def g(value,*keys):
    for key in keys:
        if isinstance(value,dict):value=value.get(key) if key in value else next((v for k,v in value.items() if canonical(str(k))==canonical(str(key))),None)
        elif isinstance(value,list) and isinstance(key,int):value=value[key] if 0<=key<len(value) else None
        else:return None
    return value

def txt(value):return '' if value is None else str(value)
def num(value):return 0 if value is None else int(value)
def size(value):return len(value) if isinstance(value,(list,dict,str)) else 0
def eq(a,b):return a==b and not (isinstance(a,bool)^isinstance(b,bool))
def yes(v):return v is True
def no(v):return v is False
def nonempty(v):return v is not None and v not in ('',[],{})
def includes(values,v):return v in values if isinstance(values,(list,dict,str)) else False
def both(*values):return all(values)
def same(a,b):
    if isinstance(b,dict):b={k:v for k,v in b.items() if k not in ('mobile','target_converted','fileMd5','file_md5')}
    return contains(a,b)
def ids(value,key):return [g(v,key) for v in value] if isinstance(value,list) else []
def sets(a,b):return set(a or [])==set(b or [])


class QAWire:
    def __init__(self,c):self.c=c;self.original=urllib.request.urlopen;self.last=None
    def observe(self):return patch('urllib.request.urlopen',self.open)
    def open(self,req,*args,**kwargs):
        time.sleep(self.c.cfg.interval)
        sent=None
        if req.data:
            try:sent=json.loads(req.data)
            except ValueError:pass
        try:
            with self.original(req,*args,**kwargs) as r:
                raw=r.read();status=r.status
        except urllib.error.HTTPError as e:
            raw=e.read();self.last=self.capture(req,sent,e.code,raw)
            raise urllib.error.HTTPError(e.url,e.code,e.reason,e.headers,io.BytesIO(raw)) from None
        self.last=self.capture(req,sent,status,raw)
        self.last['multipart_valid']=bool(req.data and 'multipart/form-data; boundary=' in req.get_header('Content-type','') and b'name="language"' in req.data and b'name="file"' in req.data and bool(getattr(self.c,'voice_bytes',None)) and self.c.voice_bytes in req.data)
        return contextlib.closing(io.BytesIO(raw))
    @staticmethod
    def capture(req,sent,status,raw):
        try:body=json.loads(raw)
        except ValueError:body=raw.decode('utf-8','replace')
        u=urllib.parse.urlsplit(req.full_url)
        return m('status',status,'raw',body,'request',sent,'path',u.path,'query',urllib.parse.parse_qs(u.query))


class QAContext:
    def __init__(self):
        self.cfg=Config()
        pair=('ENGAGELAB_LIFECYCLE_MESSAGE_ID','ENGAGELAB_LIFECYCLE_REGISTRATION_ID')
        values=[self.cfg.env.get(k,'').strip() for k in pair]
        if bool(values[0])!=bool(values[1]):raise Blocked('Provide both lifecycle message ID and registration ID')
        self.cfg.env.update(dict(zip(pair,values)))
        self.prefix=self.cfg.run_id;self.results={};self.owned=[];self.network='';self.alias_baselines={};self.wire=QAWire(self)
        self.actions=Actions(self.cfg.base,self.cfg.key,self.cfg.secret,self.cfg.timeout,
            self.cfg.env.get('ENGAGELAB_GROUP_KEY','unused'),self.cfg.env.get('ENGAGELAB_GROUP_SECRET','unused'))
    def require(self,value,why):
        if not value:raise Blocked(why)
    def write(self):self.cfg.write()
    def need(self,key):return self.cfg.need(key)
    def rest(self,method,path,body=None):
        time.sleep(self.cfg.interval)
        req=urllib.request.Request(self.cfg.base+path,method=method,data=json.dumps(body).encode() if body is not None else None,
            headers={'Authorization':'Basic '+base64.b64encode((self.cfg.key+':'+self.cfg.secret).encode()).decode(),'Content-Type':'application/json'})
        try:
            with self.wire.original(req,timeout=self.cfg.timeout) as r:raw=r.read();status=r.status
        except urllib.error.HTTPError as e:raw=e.read();status=e.code
        except (urllib.error.URLError,TimeoutError) as e:raise Blocked('QA transport unavailable: '+type(e).__name__) from None
        try:data=json.loads(raw) if raw else None
        except ValueError:data=raw.decode('utf-8','replace')
        return m('status',status,'data',data)
    def sdk(self,op,args):
        self.network='';self.wire.last=None
        try:
            with self.wire.observe():data=self.actions.call(op,args)
            return dict(self.wire.last or {},ok=True,data=data)
        except ApiError as e:
            return dict(self.wire.last or {},ok=False,error_code=e.error.code,error_message=e.error.message)
        except (urllib.error.URLError,TimeoutError) as e:
            self.network=type(e).__name__;return m('ok',False,'network',self.network)
    def wait(self,fn,reason):
        deadline=time.monotonic()+self.cfg.wait
        while True:
            if fn():return
            if time.monotonic()>=deadline:raise Blocked(reason)
            time.sleep(self.cfg.interval)
    def record(self,sid,checks,ready=True,why=''):
        status='pass' if all(checks.values()) else 'block' if self.network else 'no_pass'
        if not ready:status='block'
        self.results[sid]=m('status',status,'checks',checks,'reason',why if not ready else ('QA transport unavailable: '+self.network if self.network else ''))
    def own(self,kind,value):
        self.owned.append((kind,value))
        folder=Path(os.environ.get('ENGAGELAB_FULL_RESULTS_DIR','.test-results/full'))/'resources';folder.mkdir(parents=True,exist_ok=True)
        p=folder/(self.prefix+'.json');p.write_text(json.dumps(m('run_id',self.prefix,'owned',self.owned)));p.chmod(0o600)
    def seedDevice(self):
        self.write();self.require(self.cfg.target=='qa','Backend-only registration fixtures require QA')
        token=self.prefix+'_'+uuid.uuid4().hex
        r=self.rest('POST','/v4/devices/token/registration_id',m('platform','android','tokens',arr(token)))
        item=g(r,'data','results',0);rid=g(item,'registration_id')
        self.require(eq(g(r,'status'),200) and nonempty(rid) and yes(g(item,'is_new')),'Cannot create an exclusively owned backend device')
        self.own('device',rid);return rid
    def seedTag(self,tag,rid):
        self.own('tag',tag);r=self.rest('POST','/v4/tags/'+tag,m('registration_ids',m('add',arr(rid))));self.require(eq(g(r,'status'),200),'Cannot prepare isolated tag binding');return r
    def seedAlias(self,alias,rid):
        if not any(k=='device' and v==rid for k,v in self.owned) and rid not in self.alias_baselines:
            self.alias_baselines[rid]=txt(g(self.device(rid),'data','alias'))
        self.own('alias',alias);r=self.rest('POST','/v4/devices/'+rid,m('alias',alias));self.require(eq(g(r,'status'),200),'Cannot prepare isolated alias binding');return r
    def device(self,rid):return self.rest('GET','/v4/devices/'+rid)
    def relation(self,tag,rid):return self.rest('GET','/v4/tags/'+tag+'/registration_ids/'+rid)
    def listPlans(self,prefix,size=101,page=1,source=None):
        q=m('page_index',page,'page_size',size,'search_description',prefix)
        if source is not None:q['send_source']=source
        return self.rest('GET','/v4/push_plan/list?'+urllib.parse.urlencode(q))
    def seedPlan(self,pid,description):
        self.own('plan',pid);r=self.sdk('plan_create',arr(m('plan_id',pid,'plan_description',description)))
        self.require(yes(g(r,'ok')) and eq(g(r,'data','plan_id'),pid),'Cannot prepare an owned plan through SDK');return r
    def clean(self):
        failed=[];plans=[v for k,v in self.owned if k=='plan']
        for offset in range(0,len(plans),10):
            try:self.rest('DELETE','/v4/push_plan/batch/'+','.join(plans[offset:offset+10]))
            except Exception:failed.append('plan_delete_transport')
        if plans:
            try:self.wait(lambda:eq(g(self.listPlans(self.prefix),'data','total'),0),'Owned plans remain');
            except Exception:failed.append('plan_cleanup_readback')
        for kind,value in reversed(self.owned):
            try:
                if kind in ('alias','tag'):
                    path='/v4/'+('aliases' if kind=='alias' else 'tags')+'/'+value+'?platform=android';self.rest('DELETE',path)
                    if kind=='alias':self.wait(lambda:not g(self.rest('GET',path),'data','registration_ids'),'Owned alias remains')
                    else:self.wait(lambda:value not in (g(self.rest('GET','/v4/tags/'),'data','tags') or []),'Owned tag remains')
                elif kind=='device':
                    self.rest('DELETE','/v4/devices/'+value)
                    self.wait(lambda:eq(g(self.device(value),'data','error','code'),27002),'Owned backend device remains')
                elif kind=='schedule':
                    self.rest('DELETE','/v4/schedules/'+value)
                    self.wait(lambda:eq(g(self.rest('GET','/v4/schedules/'+value),'status'),404),'Owned schedule remains')
                elif kind=='voice':
                    self.rest('DELETE','/v4/voices/'+value)
                    self.wait(lambda:eq(g(self.rest('GET','/v4/voices/'+value),'status'),404),'Owned voice template remains')
            except Exception:failed.append(kind+'_cleanup_readback')
        for rid,alias in self.alias_baselines.items():
            try:
                self.rest('POST','/v4/devices/'+rid,m('alias',alias))
                self.wait(lambda:eq(txt(g(self.device(rid),'data','alias')),alias),'Fixture alias restore failed')
            except Exception:failed.append('fixture_alias_restore')
        for r in self.results.values():
            r['checks']['owned_resource_cleanup']=not failed
            if failed and r['status']=='pass':r['status']='no_pass';r['reason']='Cleanup not verified: '+','.join(sorted(set(failed)))
        return not failed
    def hasKeys(self,value,keys):
        def visit(v,k):
            if isinstance(v,dict):return k in v or any(visit(x,k) for x in v.values())
            if isinstance(v,list):return any(visit(x,k) for x in v)
            return False
        return all(visit(value,k) for k in keys)
    def join(self,values):return ','.join(txt(x) for x in values)
    def noneIn(self,left,right):return not set(left or [])&set(right or [])
    def errorsEqual(self,sdk,rest):
        return no(g(sdk,'ok')) and eq(g(sdk,'status'),g(rest,'status')) and eq(g(sdk,'error_code'),g(rest,'data','error','code')) and eq(g(sdk,'error_message'),g(rest,'data','error','message'))
    def seedPlans(self,count):
        self.firstPlan=None
        for i in range(count):
            r=self.seedPlan(self.prefix+'_'+str(i),self.prefix)
            if i==0:self.firstPlan=r
        self.wait(lambda:eq(g(self.listPlans(self.prefix),'data','total'),count),'101 isolated plans not queryable')
        return self.firstPlan
    def planIDs(self):return [v for k,v in self.owned if k=='plan'][:101]
    def batchPlanPair(self,exclude):return [v for v in self.planIDs() if v!=exclude][:2]
    def planBoundary(self,length):
        if length==1:
            pid=None
            for candidate in 'abcdefghijklmnopqrstuvwxyz0123456789':
                r=self.listPlans(candidate,10000,1,None)
                if size(g(r,'data','push_plan_info'))>=num(g(r,'data','total')) and candidate not in ids(g(r,'data','push_plan_info'),'plan_id'):pid=candidate;break
            if pid is None:return m('ready',False,'verified',False)
        else:pid=(self.prefix+'_'+('x'*length))[:length]
        payload=m('plan_id',pid,'plan_description',self.prefix)
        self.own('plan',pid)
        r=self.sdk('plan_create',arr(payload))
        if length==51:
            control=self.rest('POST','/v4/push_plan',payload)
            return m('ready',True,'verified',self.errorsEqual(r,control) and eq(g(r,'error_code'),27304))
        read=self.listPlans(self.prefix)
        valid=yes(g(r,'ok')) and pid in ids(g(read,'data','push_plan_info'),'plan_id') and len(pid)==length
        return m('ready',True,'verified',valid)
    def targetRID(self,index):
        if not hasattr(self,'targets'):
            provided=[x for x in self.cfg.env.get('ENGAGELAB_FIXTURE_REGISTRATION_IDS','').split(',') if x]
            self.targets=provided
        while len(self.targets)<=index:self.targets.append(self.seedDevice())
        rid=self.targets[index];self.require(eq(g(self.device(rid),'status'),200),'Declared QA target does not belong to this app');return rid
    def batchResultsValid(self,r,targets):
        results=g(r,'data','results') or {}
        return eq(set(results),set(targets)) and all(yes(g(v,'success')) and nonempty(g(v,'msg_id')) and eq(g(v,'target'),k) for k,v in results.items())
    def batch(self,op,targets):
        payload=m('requests',[m('target',t,'platform','android','notification',m('alert',self.prefix),'options',m('time_to_live',30,'third_party_channel',m('distribution_new','mtpush'))) for t in targets])
        r=self.sdk(op,arr(payload));mids=[txt(g(v,'msg_id')) for v in (g(r,'data','results') or {}).values() if yes(g(v,'success'))]
        linked=False
        if len(mids)==len(targets):
            try:
                self.wait(lambda:all(k in (g(self.rest('GET','/v4/status/detail?'+urllib.parse.urlencode(m('message_ids',self.join(mids)))),'data') or {}) for k in mids),'Batch messages are not persisted')
                linked=True
            except Blocked:pass
        r['messages_persisted']=linked;return r
    def negative(self,kind):
        base=m('to',m('registration_id',arr('sdk_full_negative_nonexistent')),'body',m('platform',arr('ios'),'options',m('apns_production',False)))
        types=m('voip',m('call_id',self.prefix),'message',m('msg_content',self.prefix),'notification',m('alert',self.prefix),'live_activity',m('ios',m('event','start','attributes-type','SdkFull','attributes',m(),'content-state',m('n',1))))
        controls=True;op='validate';path='/v4/push/validate'
        if kind=='empty':payload=m()
        elif kind=='platform':payload=m('to',m('registration_id',arr('sdk_full_negative_nonexistent')),'body',m('platform','bad-platform','notification',m('alert',self.prefix)));op='push_raw';path='/v4/push'
        else:
            base['to']['registration_id']=[self.negativeTarget()]
            for name in ['voip',kind]:
                p=json.loads(json.dumps(base));p['body'][name]=types[name];control=self.rest('POST',path,p);controls=controls and eq(g(control,'status'),200)
            payload=base;payload['body'].update(voip=types['voip'],**{kind:types[kind]})
        raw=self.rest('POST',path,payload);r=self.sdk(op,arr(payload))
        return m('verified',self.errorsEqual(r,raw) and no(g(r,'ok')),'controls_valid',controls)
    def invalidAuth(self):
        old=self.actions
        try:
            self.actions=Actions(self.cfg.base,'000000000000000000000000','invalid-sdk-secret',self.cfg.timeout)
            r=self.sdk('vip',arr())
        finally:self.actions=old
        req=urllib.request.Request(self.cfg.base+'/v4/app/vip/status',headers={'Authorization':'Basic '+base64.b64encode(b'000000000000000000000000:invalid-sdk-secret').decode()})
        try:
            with self.wire.original(req,timeout=self.cfg.timeout) as response:raw=m('status',response.status,'data',json.loads(response.read()))
        except urllib.error.HTTPError as e:raw=m('status',e.code,'data',json.loads(e.read()))
        return m('verified',self.errorsEqual(r,raw))
    def vipValid(self,r):
        return isinstance(g(r,'data','vip_status'),int) and not isinstance(g(r,'data','vip_status'),bool) and isinstance(g(r,'data','vip_end_time'),int)
    def apnsToken(self):
        token,production=self.cfg.apns();payload=m('platform','ios','tokens',arr(token),'apns_production',production)
        rid=None;created=False;baseline=None;verified=False;clean=False
        try:
            r=self.sdk('token',arr(payload));raw=g(r,'raw','results');parsed=g(r,'data','results');rid=g(raw,0,'registration_id');created=yes(g(raw,0,'is_new'))
            verified=eq(g(r,'status'),200) and size(raw)==size(parsed)==1 and nonempty(rid) and eq(g(parsed,0,'token'),token) and eq(g(parsed,0,'registration_id'),rid) and eq(g(parsed,0,'is_new'),g(raw,0,'is_new')) and g(parsed,0,'code') in (None,0) and eq(g(r,'request','apns_production'),production)
            if rid:
                self.wait(lambda:eq(g(self.device(rid),'status'),200),'Registered token mapping not queryable');baseline=self.device(rid)
                again=self.sdk('token',arr(payload));verified=verified and eq(g(again,'data','results',0,'registration_id'),rid) and no(g(again,'data','results',0,'is_new'))
        finally:
            if rid and created:
                self.rest('DELETE','/v4/devices/'+rid);self.wait(lambda:eq(g(self.device(rid),'data','error','code'),27002),'New token mapping cleanup not verified');clean=True
            elif rid and baseline:clean=eq(self.device(rid),baseline)
        return m('verified',verified,'cleanup',clean)
    def groupPush(self):
        group_key=self.need('ENGAGELAB_GROUP_KEY');self.need('ENGAGELAB_GROUP_SECRET');apps=self.need('ENGAGELAB_GROUP_APP_KEYS').split(',');alias=self.need('ENGAGELAB_GROUP_TARGET_ALIAS')
        self.require(len(set(apps))>=2 and '' not in apps,'At least two explicit group members required')
        secrets=json.loads(self.need('ENGAGELAB_GROUP_APP_SECRETS'))
        for app in apps:
            self.require(app in secrets,'Missing group-member control credential')
            request=urllib.request.Request(self.cfg.base+'/v4/aliases/'+urllib.parse.quote(alias)+'?platform=android',headers={'Authorization':'Basic '+base64.b64encode((app+':'+secrets[app]).encode()).decode()})
            with self.wire.original(request,timeout=self.cfg.timeout) as response:binding=json.loads(response.read())
            self.require(len(binding.get('registration_ids') or [])==1,'Group alias must resolve exclusively to one prepared test target per app')
        payload=m('request_id',self.prefix,'to',m('alias',arr(alias)),'body',m('platform',arr('android'),'notification',m('alert',self.prefix),'options',m('time_to_live',30,'third_party_channel',m('distribution_new','mtpush'))))
        r=self.sdk('group',arr(payload));raw=g(r,'raw') or {};parsed=g(r,'data','successes') or {}
        if any(g(v,'error','code')==21038 for v in raw.values() if isinstance(v,dict)):raise Blocked('Group member lacks push permission: 21038')
        valid=eq(g(r,'status'),200) and set(parsed)==set(apps) and size(g(r,'data','errors'))==0 and nonempty(g(r,'data','group_msgid')) and eq(g(r,'data','group_msgid'),g(r,'raw','group_msgid')) and all(nonempty(g(parsed,k,'msg_id')) and same(parsed[k],raw[k]) for k in apps)
        return m('verified',valid,'explicit_target',eq(g(r,'request','to'),m('alias',arr(alias))))
    def imageUpload(self):
        url=self.need('ENGAGELAB_OPPO_IMAGE_URL')
        with self.wire.original(url,timeout=self.cfg.timeout) as response:data=response.read();http=response.status
        valid=http==200 and data[:8]==b'\x89PNG\r\n\x1a\n' and int.from_bytes(data[16:20],'big')==984 and int.from_bytes(data[20:24],'big')==369 and len(data)<1024*1024
        self.require(valid,'Image must be a reachable 984x369 PNG smaller than 1MiB')
        r=self.sdk('image',arr(m('big_picture_url',url)));picture=g(r,'data','big_picture_id')
        return m('resource_valid',valid,'verified',eq(g(r,'status'),200) and nonempty(picture) and eq(picture,g(r,'raw','big_picture_id')),'prerequisite',eq(g(r,'status'),200))
    def prepareVoice(self):
        r=self.sdk('voices',arr());self.require(yes(g(r,'ok')),'Voice list prerequisite unavailable')
        used=ids(g(r,'data'),'language');language=self.cfg.env.get('ENGAGELAB_VOICE_LANGUAGE','en');self.require(language not in used,'Voice language is occupied; existing template will not be overwritten')
        self.voiceLanguage=language;self.own('voice',language)
        path=Path(self.cfg.env.get('ENGAGELAB_VOICE_FILE',str(Path(__file__).resolve().parents[1]/'fixtures/voice/en.zip')))
        self.require(path.is_file(),'Valid voice ZIP resource missing: ENGAGELAB_VOICE_FILE')
        with zipfile.ZipFile(path) as archive:
            entries=archive.infolist()
            self.require(len(entries)>=34 and all(x.filename.endswith('.mp3') and x.file_size>0 for x in entries),'Expected complete nonempty MP3 voice ZIP')
        self.voice_bytes=path.read_bytes()
        upload=self.sdk('voice_create',arr(language,str(path)));file_url=g(upload,'data','file_url')
        self.require(yes(g(upload,'ok')),'Valid voice ZIP rejected by QA; no owned template created')
        detail=self.sdk('voice_get',arr(language));listed=self.sdk('voices',arr())
        return m('upload_verified',eq(g(upload,'status'),200) and nonempty(file_url) and eq(file_url,g(upload,'raw','file_url')) and yes(g(upload,'multipart_valid')),'detail_verified',eq(g(detail,'status'),200) and eq(g(detail,'data','file_url'),file_url),'list_verified',eq(g(listed,'status'),200) and any(eq(g(item,'language'),language) and eq(g(item,'file_url'),file_url) for item in (g(listed,'data') or [])))
    def deleteVoice(self):
        r=self.sdk('voice_delete',arr(self.voiceLanguage));detail=self.rest('GET','/v4/voices/'+self.voiceLanguage);listed=self.sdk('voices',arr())
        return m('sdk_ok',g(r,'ok'),'verified',eq(g(detail,'status'),404) and self.voiceLanguage not in ids(g(listed,'data'),'language'))
    def payload(self,rid,marker,plan=None):
        options=m('time_to_live',30,'third_party_channel',m('distribution_new','mtpush'))
        if plan:options['plan_id']=plan
        return m('request_id',marker,'to',m('registration_id',arr(rid)),'body',m('platform',arr('android'),'notification',m('alert',marker,'android',m('title',marker)),'options',options))
    def scheduleOne(self,kind,when,rid,pid):
        trigger=m('intelligent',m('backup_time',when)) if kind=='intelligent' else m('single',m('time',when,'zone_type',0))
        push=self.payload(rid,self.prefix+'_'+kind,pid);push.pop('request_id',None)
        param=m('name',self.prefix+'_'+kind,'enabled',True,'trigger',trigger,'push',push)
        created=self.sdk('schedule_create',arr(param));sid=g(created,'data','schedule_id')
        if sid:self.own('schedule',sid)
        raw=self.rest('GET','/v4/schedules/'+txt(sid)) if sid else m('status',0,'data',None)
        detail=g(raw,'data',0) if isinstance(g(raw,'data'),list) else g(raw,'data')
        return m('sdk',created,'id',sid,'param',param,'read',raw,'detail',detail)
    def prepareSchedules(self):
        rid=self.targetRID(0);pid=self.prefix+'_schedule_plan';self.seedPlan(pid,self.prefix)
        deadline=datetime.now(timezone(timedelta(hours=8)))+timedelta(seconds=max(45,int(self.cfg.env.get('ENGAGELAB_SCHEDULE_DELAY','45'))))
        when=deadline.strftime('%Y-%m-%d %H:%M:%S');tomorrow=(deadline+timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
        positive=self.scheduleOne('positive',when,rid,pid);update=self.scheduleOne('update',when,rid,pid);delete=self.scheduleOne('delete',when,rid,pid);smart=self.scheduleOne('intelligent',tomorrow,rid,pid)
        sid=g(positive,'id');get=self.sdk('schedule_get',arr(sid)) if sid else m();listed=self.listOwnedSchedule(sid)
        update_param=json.loads(json.dumps(g(update,'param')));update_param['enabled']=False;update_param['name']+='_updated';update_param['push']['body']['notification']['alert']+='_updated'
        updated=self.sdk('schedule_update',arr(g(update,'id'),update_param)) if g(update,'id') else m();after_update=self.rest('GET','/v4/schedules/'+txt(g(update,'id'))) if g(update,'id') else m();ud=g(after_update,'data',0) if isinstance(g(after_update,'data'),list) else g(after_update,'data')
        deleted=self.sdk('schedule_delete',arr(g(delete,'id'))) if g(delete,'id') else m();after_delete=self.rest('GET','/v4/schedules/'+txt(g(delete,'id'))) if g(delete,'id') else m()
        until=deadline.timestamp()+max(15,int(self.cfg.env.get('ENGAGELAB_SCHEDULE_OBSERVATION','15')))
        while time.time()<until:time.sleep(min(2,until-time.time()))
        messages=self.sdk('schedule_msgs',arr(sid)) if sid else m()
        records=g(messages,'data','MsgIds') or [];positive_ids=self.scheduleIDs(records)
        if sid and not positive_ids:
            try:self.wait(lambda:nonempty(g(self.rest('GET','/v4/schedules/'+sid+'/msg-ids'),'data','msg_ids') or g(self.rest('GET','/v4/schedules/'+sid+'/msg-ids'),'data','msgIds')),'Positive schedule did not trigger')
            except Blocked:pass
            messages=self.sdk('schedule_msgs',arr(sid));records=g(messages,'data','MsgIds') or [];positive_ids=self.scheduleIDs(records)
        disabled_messages=self.rest('GET','/v4/schedules/'+txt(g(update,'id'))+'/msg-ids') if g(update,'id') else m()
        deleted_messages=self.rest('GET','/v4/schedules/'+txt(g(delete,'id'))+'/msg-ids') if g(delete,'id') else m()
        known={g(x,'id') for x in [positive,update,smart] if g(x,'id') and eq(g(x,'read','status'),200)}
        getdetail=g(get,'data',0) if isinstance(g(get,'data'),list) else g(get,'data')
        positive_ready=nonempty(positive_ids)
        linked=False
        if positive_ready:
            try:
                self.wait(lambda:all(txt(k) in (g(self.rest('GET','/v4/status/detail?'+urllib.parse.urlencode(m('message_ids',self.join(positive_ids)))),'data') or {}) for k in positive_ids),'Scheduled messages are not persisted')
                linked=True
            except Blocked:pass
        return m('create',yes(g(positive,'sdk','ok')) and self.scheduleMatches(g(positive,'detail'),g(positive,'param')),'create_ready',True,
            'get',yes(g(get,'ok')) and self.scheduleMatches(getdetail,g(positive,'param')),'get_ready',True,
            'list',eq(g(listed,'status'),200) and sid in set(ids(g(listed,'data','schedules'),'schedule_id')) and self.scheduleListMatches(g(listed,'data'),g(listed,'raw')),'list_ready',True,
            'intelligent',yes(g(smart,'sdk','ok')) and eq(g(smart,'detail','trigger','intelligent','backup_time'),tomorrow),'intelligent_ready',eq(g(smart,'read','status'),200),
            'messages',eq(g(messages,'status'),200) and positive_ready and num(g(messages,'data','count'))==len(records) and eq(records,g(messages,'raw','MsgIds')) and linked,'messages_ready',positive_ready,
            'update',yes(g(updated,'ok')) and self.scheduleMatches(ud,update_param) and size(g(disabled_messages,'data','msg_ids') or g(disabled_messages,'data','msgIds'))==0,'update_ready',positive_ready,
            'delete',yes(g(deleted,'ok')) and eq(g(after_delete,'status'),404) and (eq(g(deleted_messages,'status'),404) or size(g(deleted_messages,'data','msg_ids') or g(deleted_messages,'data','msgIds'))==0),'delete_ready',positive_ready)
    def prepareStatistics(self):
        rids=arr(self.targetRID(0),self.targetRID(1));pids=arr(self.prefix+'_stats_a',self.prefix+'_stats_b');mids=[]
        for i in range(2):
            self.seedPlan(pids[i],self.prefix);sent=self.sdk('push',arr(self.payload(rids[i],self.prefix+'_stats_'+str(i),pids[i])))
            self.require(yes(g(sent,'ok')) and nonempty(g(sent,'data','msg_id')),'Statistics requires two accepted isolated messages');mids.append(txt(g(sent,'data','msg_id')))
        start=(datetime.now(timezone(timedelta(hours=8)))-timedelta(days=2)).strftime('%Y-%m-%d');end=datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%d')
        try:self.wait(lambda:all(nonempty(g(self.rest('GET','/v4/status/detail?'+urllib.parse.urlencode(m('message_ids',self.join(mids)))),'data',mid)) for mid in mids),'Message statistics not persisted')
        except Blocked:pass
        message=self.sdk('status',arr(mids));lifeRID=self.cfg.env.get('ENGAGELAB_LIFECYCLE_REGISTRATION_ID') or rids[0];lifeMID=self.cfg.env.get('ENGAGELAB_LIFECYCLE_MESSAGE_ID') or mids[0];life=self.sdk('lifecycle',arr(lifeMID,arr(lifeRID)));batch=self.sdk('batch_lifecycle',arr(mids));users=self.sdk('users',arr('DAY',start,3));plan=self.sdk('plan_status',arr(pids,start,end));linked=self.sdk('plan_msgs',arr(pids[0],start,end))
        life_data=g(life,'raw') or {};batch_data=g(batch,'raw') or []
        known_life=self.lifecycleReady(g(life_data,lifeRID))
        known_batch=isinstance(batch_data,list) and len(batch_data)>0 and all(txt(g(v,'message_id')) in mids and g(v,'registration_id') in rids for v in batch_data)
        hmos=self.hmosNonzero(g(users,'raw'))
        plan_data=g(plan,'raw') or {};plan_ready=all(nonempty(g(plan_data,p)) and num(g(plan_data,p,'targets') or g(plan_data,p,'target'))>0 for p in pids)
        linked_ids=g(linked,'data',pids[0],'msg_ids') or []
        return m('message',eq(g(message,'status'),200) and all(nonempty(g(message,'data',mid)) for mid in mids) and same(g(message,'data'),g(message,'raw')),'message_ready',all(nonempty(g(message,'raw',mid)) for mid in mids),
            'lifecycle',eq(g(life,'status'),200) and same(g(life,'data'),g(life,'raw')) and self.lifecycleDefaults(g(life,'data',lifeRID),g(life,'raw',lifeRID)),'lifecycle_ready',known_life,
            'batch_lifecycle',eq(g(batch,'status'),200) and same(g(batch,'data'),g(batch,'raw')),'batch_lifecycle_ready',known_batch,
            'users',eq(g(users,'status'),200) and same(g(users,'data'),g(users,'raw')),'users_ready',hmos,
            'plan',eq(g(plan,'status'),200) and same(g(plan,'data'),g(plan,'raw')),'plan_ready',plan_ready,
            'plan_messages',eq(g(linked,'status'),200) and mids[0] in linked_ids and same(g(linked,'data'),g(linked,'raw')),'plan_messages_ready',bool(linked_ids))
    def hmosNonzero(self,value):
        if isinstance(value,dict):
            return any((str(k).lower()=='hmos' and ((isinstance(v,(int,float)) and v>0) or (isinstance(v,dict) and any(isinstance(n,(int,float)) and n>0 for n in v.values())))) or self.hmosNonzero(v) for k,v in value.items())
        return isinstance(value,list) and any(self.hmosNonzero(v) for v in value)
    def adb(self,*args):
        path=self.cfg.env.get('ENGAGELAB_ADB_PATH','adb');serial=self.need('ENGAGELAB_ADB_SERIAL')
        if args and args[0]=='shell':args=('shell',shlex.join(args[1:]))
        try:p=subprocess.run([path,'-s',serial]+list(args),capture_output=True,text=True,timeout=20)
        except (FileNotFoundError,subprocess.TimeoutExpired):raise Blocked('ADB executable/device unavailable') from None
        self.require(p.returncode==0,'ADB command failed for declared physical device');return p.stdout
    def notifications(self,marker):
        package=self.need('ENGAGELAB_ANDROID_PACKAGE');keys=[s.strip() for s in self.adb('shell','cmd','notification','list').splitlines() if '|'+package+'|' in s];found=[]
        for k in keys:
            try:record=self.adb('shell','cmd','notification','get',k)
            except Blocked:
                self.require(k not in self.adb('shell','cmd','notification','list').splitlines(),'Notification read failed while key remains');continue
            if marker in record:found.append(k)
        return found
    def physicalNotifications(self):
        self.write();rid=self.need('ENGAGELAB_TEST_REGISTRATION_ID');package=self.need('ENGAGELAB_ANDROID_PACKAGE');self.require(self.need('ENGAGELAB_DEVICE_APP_KEY')==self.cfg.key,'Physical app identity differs from SDK application')
        self.require(nonempty(self.adb('shell','pidof',package)),'Physical QA Demo is not running');self.require(eq(g(self.device(rid),'status'),200),'Physical RID is absent from QA app')
        package_info=self.adb('shell','dumpsys','package',package);uid=re.search(r'(?:userId|appId)=(\d+)',package_info)
        self.require(uid is not None,'Physical app UID could not be read')
        def logs(marker,mid=None):
            lines=self.adb('logcat','-d','--uid='+uid.group(1),'-v','epoch','-t','2000')
            return [x for x in lines.splitlines() if (marker in x or (mid and str(mid) in x)) and any(k in x for k in ('onNotification','UserReceiver','MTNotificationBusiness'))]
        marker=self.prefix+'_physical';payload=self.payload(rid,marker);mid=None;push_ok=validate_ok=withdraw_ok=False;posted=[]
        try:
            sent=self.sdk('push',arr(payload));mid=g(sent,'data','msg_id')
            if mid:
                self.wait(lambda:nonempty(self.notifications(marker)),'Positive system notification did not appear');posted=self.notifications(marker)
            persisted=self.rest('GET','/v4/status/detail?'+urllib.parse.urlencode(m('message_ids',txt(mid)))) if mid else m()
            log_control=bool(logs(marker,mid))
            push_ok=eq(g(sent,'status'),200) and nonempty(posted) and eq(mid,g(sent,'raw','msg_id')) and nonempty(g(persisted,'data',txt(mid))) and same(g(sent,'data'),g(sent,'raw'))
            control=self.sdk('device_status',arr(m('registration_ids',arr(rid))))
            valmarker=marker+'_validate';validation=self.payload(rid,valmarker);validation['body']['options']['time_to_live']=10
            validated=self.sdk('validate',arr(validation));start=time.monotonic();unexpected=False
            while time.monotonic()-start<12:
                unexpected=unexpected or nonempty(self.notifications(valmarker));time.sleep(1)
            after=self.sdk('device_status',arr(m('registration_ids',arr(rid))))
            validate_ok=eq(g(validated,'status'),200) and not unexpected and yes(g(control,'data',0,'online')) and yes(g(after,'data',0,'online')) and bool(posted) and log_control and not logs(valmarker) and txt(g(validated,'data','msg_id'))==txt(g(validated,'raw','msg_id')) and txt(g(validated,'data','request_id'))==txt(g(validated,'raw','request_id'))
            if mid and self.notifications(marker):
                withdrawn=self.sdk('withdraw',arr(txt(mid)));self.wait(lambda:not self.notifications(marker),'Original system notification remains after withdrawal');withdraw_ok=eq(g(withdrawn,'status'),200) and txt(g(withdrawn,'data','msg_id'))==txt(mid) and same(g(withdrawn,'data'),g(withdrawn,'raw'))
        finally:
            if mid:
                self.rest('DELETE','/v4/push/withdraw/'+txt(mid));self.require(not self.notifications(marker),'Owned system notification cleanup not confirmed')
        return m('push',push_ok,'push_ready',bool(posted),'validate',validate_ok,'validate_ready',bool(posted) and log_control,'withdraw',withdraw_ok,'withdraw_ready',bool(posted))

    def negativeTarget(self):
        self.write()
        if not hasattr(self,'negative_rid'):
            token,production=self.cfg.apns()
            raw=self.rest('POST','/v4/devices/token/registration_id',m('platform','ios','tokens',arr(token),'apns_production',production))
            rid=g(raw,'data','results',0,'registration_id')
            self.require(eq(g(raw,'status'),200) and nonempty(rid),'Cannot establish legal APNs sandbox validation target')
            if yes(g(raw,'data','results',0,'is_new')):self.own('device',rid)
            self.negative_rid=rid
        return self.negative_rid
    def scheduleMatches(self,actual,want):
        push=g(actual,'push') or {};audience=g(push,'to') or g(push,'audience');body=g(push,'body') or push
        return eq(g(actual,'name'),g(want,'name')) and eq(g(actual,'enabled'),g(want,'enabled')) and same(g(actual,'trigger'),g(want,'trigger')) and same(audience,g(want,'push','to')) and same(body,g(want,'push','body'))
    def scheduleListMatches(self,actual,raw):
        if not all(eq(g(actual,k),g(raw,k)) for k in ('page','total_count','total_pages')):return False
        a,b=g(actual,'schedules') or [],g(raw,'schedules') or []
        return len(a)==len(b) and all(all(same(g(x,k),g(y,k)) for k in ('schedule_id','name','enabled','trigger','push')) for x,y in zip(a,b))

    def listOwnedSchedule(self,sid):
        listed=self.sdk('schedule_list',arr(1));pages=num(g(listed,'data','total_pages'))
        if sid not in ids(g(listed,'data','schedules'),'schedule_id') and pages>1:
            listed=self.sdk('schedule_list',arr(pages))
            if sid not in ids(g(listed,'data','schedules'),'schedule_id') and pages>2:listed=self.sdk('schedule_list',arr(pages-1))
        return listed

    def scheduleIDs(self,records):
        result=[]
        for item in records:
            try:decoded=json.loads(str(item))
            except ValueError:decoded=None
            mid=g(decoded,'msg_id') if isinstance(decoded,dict) else item
            if mid and str(mid)!='0':result.append(str(mid))
        return result

    def lifecycleReady(self,record):
        if not isinstance(record,dict) or not record:return False
        return nonempty(g(record,'status')) or (num(g(record,'itime'))>0 and nonempty(g(record,'channel'))) or (num(g(record,'error_code'))>0 and g(record,'error_code') not in (21003,21061))
    def lifecycleDefaults(self,parsed,raw):
        return ('error_code' in (raw or {}) or g(parsed,'error_code') in (None,0)) and ('error_message' in (raw or {}) or txt(g(parsed,'error_message'))=='')
