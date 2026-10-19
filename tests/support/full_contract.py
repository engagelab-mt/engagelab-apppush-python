"""Native HTTP contract assertions and fixture resources; no case-document input."""
import re,contextlib,io,logging,sys
import base64,copy,hashlib,json,os,tempfile,threading,time,unittest,urllib.request,wave
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from urllib.parse import urlsplit,parse_qs
from concurrent.futures import ThreadPoolExecutor
from engagelab.client import Client,DataCenter
from engagelab.errors import ApiError
from .full_actions import Actions
from .native import check


METHOD_PATHS={'push': ('POST', '/v4/push'), 'validate': ('POST', '/v4/push/validate'), 'group': ('POST', '/v4/grouppush'), 'batch_regid': ('POST', '/v4/batch/push/regid'), 'batch_alias': ('POST', '/v4/batch/push/alias'), 'withdraw': ('DELETE', '/v4/push/withdraw/{msg_id}'), 'device_get': ('GET', '/v4/devices/{registration_id}'), 'device_set': ('POST', '/v4/devices/{registration_id}'), 'device_delete': ('DELETE', '/v4/devices/{registration_id}'), 'device_status': ('POST', '/v4/devices/status/'), 'token': ('POST', '/v4/devices/token/registration_id'), 'tags': ('GET', '/v4/tags/'), 'tag_set': ('POST', '/v4/tags/{tag}'), 'tag_delete': ('DELETE', '/v4/tags/{tag}'), 'tag_status': ('GET', '/v4/tags/{tag}/registration_ids/{registration_id}'), 'tag_count': ('GET', '/v4/tags_count'), 'tag_quota': ('GET', '/v4/tags/quota-info'), 'alias_get': ('GET', '/v4/aliases/{alias}'), 'alias_delete': ('DELETE', '/v4/aliases/{alias}'), 'schedule_create': ('POST', '/v4/schedules'), 'schedule_update': ('PUT', '/v4/schedules/{schedule_id}'), 'schedule_get': ('GET', '/v4/schedules/{schedule_id}'), 'schedule_delete': ('DELETE', '/v4/schedules/{schedule_id}'), 'schedule_list': ('GET', '/v4/schedules'), 'schedule_msgs': ('GET', '/v4/schedules/{schedule_id}/msg-ids'), 'status': ('GET', '/v4/status/detail'), 'lifecycle': ('GET', '/v4/status/message'), 'batch_lifecycle': ('GET', '/v4/status/batch/message'), 'users': ('GET', '/v4/status/users'), 'plan_status': ('GET', '/v4/status/plan/detail'), 'plan_create': ('POST', '/v4/push_plan'), 'plan_list': ('GET', '/v4/push_plan/list'), 'plan_msgs': ('GET', '/v4/status/plan/msg/'), 'plan_delete': ('DELETE', '/v4/push_plan/{plan_id}'), 'plan_batch_delete': ('DELETE', '/v4/push_plan/batch/{plan_ids}'), 'voice_create': ('POST', '/v4/voices'), 'voices': ('GET', '/v4/voices'), 'voice_get': ('GET', '/v4/voices/{language}'), 'voice_delete': ('DELETE', '/v4/voices/{language}'), 'image': ('POST', '/v4/image/oppo'), 'vip': ('GET', '/v4/app/vip/status'), 'push_raw': ('POST', '/v4/push'), 'schedule_raw': ('POST', '/v4/schedules'), 'legacy_pushbody': ('POST', '/v4/push/validate')}

def canonical(k):
    k=''.join(c for c in k.lower() if c.isalnum())
    return {'targets':'target','clicks':'click'}.get(k,k)


def contains(actual, expected):
    if isinstance(expected,dict):
        if not isinstance(actual,dict):return False
        values={canonical(k):v for k,v in actual.items()}
        return all(canonical(k) in values and contains(values[canonical(k)],v) for k,v in expected.items())
    if isinstance(expected,list):return isinstance(actual,list) and len(actual)==len(expected) and all(contains(a,b) for a,b in zip(actual,expected))
    return type(actual)==type(expected) and actual==expected


def save(sid,status,checks,reason='',layer='contract'):
    directory=Path(os.environ.get('ENGAGELAB_FULL_RESULTS_DIR','.test-results/full'))/layer
    directory.mkdir(parents=True,exist_ok=True)
    (directory/(sid+'.json')).write_text(json.dumps(dict(scenario_id=sid,language='Python',layer=layer,status=status,checks=checks,reason=reason),ensure_ascii=False,indent=2))


class ContractServer:
    def __init__(self,status,response,delay=0):
        outer=self
        self.records=[];self.status=status;self.response=response;self.delay=delay
        class Handler(BaseHTTPRequestHandler):
            def log_message(self,*args):pass
            def respond(self):
                raw=self.rfile.read(int(self.headers.get('Content-Length','0')))
                try:body=json.loads(raw)
                except ValueError:body=None
                u=urlsplit(self.path)
                outer.records.append(dict(method=self.command,path=u.path,query=parse_qs(u.query),body=body,raw=raw,
                    auth=self.headers.get('Authorization')=='Basic '+base64.b64encode(b'test-key:test-secret').decode(),
                    group_auth=self.headers.get('Authorization')=='Basic '+base64.b64encode(b'group-group-key:group-secret').decode(),
                    multipart='multipart/form-data; boundary=' in self.headers.get('Content-Type','')))
                response=outer.response
                if response=='ECHO':response={'request_id':body['request_id'],'msg_id':str(int(body['request_id'])+100)}
                data=response.encode() if isinstance(response,str) else json.dumps(response).encode()
                time.sleep(outer.delay)
                self.send_response(outer.status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(data)));self.end_headers()
                try:self.wfile.write(data)
                except (BrokenPipeError,ConnectionResetError):pass
            do_GET=do_POST=do_DELETE=do_PUT=respond
        self.server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
        self.thread=threading.Thread(target=lambda:self.server.serve_forever(poll_interval=.01),daemon=True);self.thread.start()
        self.base='http://127.0.0.1:'+str(self.server.server_port)
    def close(self):self.server.shutdown();self.server.server_close();self.thread.join(timeout=2)


def run_contract(sid,label,op,args,status,response,body,expected,extra=None,timeout=3,delay=0):
    checks=[];server=None;voice=None
    def ok(value,name):check(value,name);checks.append(name)
    try:
        if op=='voice_create':
            fd,voice=tempfile.mkstemp(suffix='.wav');os.close(fd)
            with wave.open(voice,'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(8000);w.writeframes(b'\x00\x00'*800)
            args=[args[0],voice]
        server=ContractServer(status,response,delay)
        actions=Actions(server.base,timeout=timeout)
        if extra=='host':
            dc=args[0];wanted={'default':DataCenter.SINGAPORE,'japan':DataCenter.JAPAN,'brazil':DataCenter.BRAZIL}[dc];captured=[];original=urllib.request.urlopen
            def redirect(req,*a,**kw):
                captured.append(req.full_url);req.full_url=server.base+'/v4/push/validate';return original(req,*a,**kw)
            from unittest.mock import patch
            with patch('urllib.request.urlopen',redirect):
                opts={} if dc=='default' else {'base_url':wanted}
                Client('test-key','test-secret',**opts).push.validate({'to':{'registration_id':['rid']},'body':{'platform':['android'],'notification':{'alert':'demo'}}})
            ok(captured==[wanted+'/v4/push/validate'],'configured_datacenter_request');save(sid,'pass',checks);return
        if extra=='concurrent':
            def send(i):return actions.call('validate',[{'request_id':str(i),'to':{'registration_id':['rid'+str(i)]},'body':{'platform':['android'],'notification':{'alert':'body'+str(i)}}}])
            with ThreadPoolExecutor(max_workers=20) as pool:actual=list(pool.map(send,range(20)))
            ok(len(server.records)==20,'twenty_real_requests')
            ok(all(r['auth'] and r['body']['to']=={'registration_id':['rid'+r['body']['request_id']]} and r['body']['body']['notification']['alert']=='body'+r['body']['request_id'] for r in server.records),'concurrent_request_isolation')
            ok(all(contains(x,{'request_id':str(i),'msg_id':str(i+100)}) for i,x in enumerate(actual)),'concurrent_response_isolation');save(sid,'pass',checks);return
        if extra=='logs':
            stdout,stderr=io.StringIO(),io.StringIO();root=logging.getLogger();handler=logging.StreamHandler(stderr);root.addHandler(handler)
            failure=None
            try:
                with contextlib.redirect_stdout(stdout),contextlib.redirect_stderr(stderr):
                    print('capture-active-stdout');print('capture-active-stderr',file=sys.stderr)
                    successful=actions.call(op,args)
                    server.status=400;server.response={'error':{'code':21003,'message':'fixture-invalid'}}
                    try:actions.call(op,args)
                    except ApiError as err:failure=err
            finally:root.removeHandler(handler);handler.close()
            ok(failure is not None and failure.status_code==400 and failure.error.code==21003,'success_and_error_controls')
            ok('capture-active-stdout' in stdout.getvalue() and 'capture-active-stderr' in stderr.getvalue(),'stdout_stderr_observers_active')
            rendered=stdout.getvalue()+stderr.getvalue()+str(failure)+repr(failure)+json.dumps(successful)
            ok('test-secret' not in rendered and base64.b64encode(b'test-key:test-secret').decode() not in rendered,'default_logs_and_exceptions_credentials_redacted')
            ok(len(server.records)==2 and all(r['auth'] and r['method']=='POST' and r['path']=='/v4/push/validate' for r in server.records),'two_authenticated_public_API_requests')
            save(sid,'pass',checks);return
        error=None;actual=None;start=time.monotonic()
        try:actual=actions.call(op,args)
        except Exception as e:error=e
        if extra=='timeout':ok(error is not None,'timeout_error');ok(time.monotonic()-start<.65,'bounded_timeout');save(sid,'pass',checks);return
        if status>=400:
            ok(isinstance(error,ApiError),'structured_api_error')
            ok(error.status_code==status,'error_http_status')
            ok(error.error.code==response['error']['code'] and error.error.message==response['error']['message'],'business_code_and_message')
        else:ok(error is None,'SDK_success')
        ok(bool(server.records),'HTTP_observed');record=server.records[-1]
        ok(record['group_auth'] if op=='group' else record['auth'],'authentication')
        method,path=METHOD_PATHS[op]
        pattern=re.sub(r'\{[^}]+\}',r'[^/]+',path).rstrip('/')
        ok(record['method']==method and re.fullmatch(pattern,record['path'].rstrip('/')) is not None,'method_and_path')
        if body is not None:ok(contains(record['body'],body),'request_fields_exact')
        if expected is not None:ok(contains(actual,expected),'parsed_fields_exact')
        if extra=='no-tags':ok(record['body'].get('tags') is None,'no_tag_clearing_instruction')
        if isinstance(extra,list) and extra[0]=='query':ok(contains(record['query'],extra[1]),'query_values')
        if extra=='multipart':ok(record['multipart'] and Path(voice).read_bytes() in record['raw'] and b'en' in record['raw'],'multipart_file_bytes')
        save(sid,'pass',checks)
    except Exception as error:
        save(sid,'no_pass',checks,str(error) if isinstance(error,AssertionError) else type(error).__name__)
        raise
    finally:
        if server:server.close()
        if voice:Path(voice).unlink(missing_ok=True)
