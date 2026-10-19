"""Self-contained test support. No TAPD, case file, or external QA runner."""
import base64
import contextlib
import io
import json
import math
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path
from unittest.mock import patch


class Blocked(RuntimeError):
    pass


def check(condition, label):
    if not condition:
        raise AssertionError(label)


def required(env, name):
    value = env.get(name, '').strip()
    if not value:
        raise Blocked('Missing ' + name)
    return value


class Config:
    def __init__(self, env=None):
        self.env = dict(os.environ if env is None else env)
        e = self.env
        self.target = required(e, 'TEST_ENV')
        self.base = required(e, 'ENGAGELAB_BASE_URL').rstrip('/')
        u = urllib.parse.urlsplit(self.base)
        qa = bool(u.hostname and u.hostname.endswith(('.qa.jpushoa.com', '.txqa.jpushoa.com')))
        if (self.target not in ('qa', 'prod') or not u.hostname or u.username or u.password
                or u.path or u.query or u.fragment or u.scheme not in ('http', 'https')
                or (self.target == 'qa') != qa
                or (self.target == 'prod' and (u.scheme != 'https' or u.hostname in ('localhost', '127.0.0.1', '::1')))):
            raise Blocked('TEST_ENV and API origin mismatch')
        self.key = required(e, 'ENGAGELAB_APP_KEY')
        self.secret = required(e, 'ENGAGELAB_MASTER_SECRET')
        self.mode = e.get('ENGAGELAB_MUTATION_MODE', 'read_only')
        if self.mode not in ('read_only', 'isolated_write'):
            raise Blocked('Invalid ENGAGELAB_MUTATION_MODE')
        try:
            self.timeout = float(e.get('ENGAGELAB_HTTP_TIMEOUT', '25'))
            self.wait = float(e.get('ENGAGELAB_WAIT_TIMEOUT', '30'))
            self.interval = float(e.get('ENGAGELAB_REQUEST_INTERVAL', '1.1'))
            if not all(math.isfinite(x) and 0 < x <= 86400 for x in (self.timeout, self.wait, self.interval)):
                raise ValueError()
        except ValueError:
            raise Blocked('Timeouts and request interval must be positive finite seconds') from None
        prefix = e.get('ENGAGELAB_RESOURCE_PREFIX', 'sdknative')
        if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]{0,15}', prefix):
            raise Blocked('Invalid resource prefix')
        self.run_id = prefix + '_' + uuid.uuid4().hex[:12]

    def write(self):
        if self.mode != 'isolated_write':
            raise Blocked('This test requires isolated_write')

    def need(self, name):
        return required(self.env, name)

    def apns(self):
        token = self.need('ENGAGELAB_APNS_TOKEN')
        prod = self.need('ENGAGELAB_APNS_PRODUCTION')
        self.need('ENGAGELAB_BUNDLE_ID')
        if not re.fullmatch('[0-9a-fA-F]{64}', token) or prod not in ('true', 'false'):
            raise Blocked('Expected a real 64-hex APNs token and explicit true/false channel')
        return token, prod == 'true'

    def record(self, scenario, status, checks, reason=''):
        out = Path(self.env.get('ENGAGELAB_RESULTS_DIR', '.test-results'))
        out.mkdir(parents=True, exist_ok=True)
        value = dict(run_id=self.run_id, scenario_id=scenario, language='Python', suite='integration',
                     environment=self.target, base_url=self.base, status=status, checks=checks, reason=reason)
        (out / (scenario + '.json')).write_text(json.dumps(value, indent=2), encoding='utf-8')


class Wire:
    """Delegate to the real HTTP implementation; retain wire data only in memory."""
    def __init__(self, cfg):
        self.cfg, self.last, self.request = cfg, None, None
        self.original = urllib.request.urlopen

    def open(self, req, *args, **kwargs):
        time.sleep(self.cfg.interval)
        with self.original(req, *args, **kwargs) as response:
            raw = response.read()
            self.last = json.loads(raw) if raw else None
            self.request = json.loads(req.data) if req.data else None
            return contextlib.closing(io.BytesIO(raw))

    def observe(self):
        return patch('urllib.request.urlopen', self.open)

    def rest(self, method, path, body=None):
        time.sleep(self.cfg.interval)
        auth = base64.b64encode((self.cfg.key + ':' + self.cfg.secret).encode()).decode()
        req = urllib.request.Request(self.cfg.base + path, method=method,
              data=json.dumps(body).encode() if body is not None else None,
              headers={'Authorization': 'Basic ' + auth, 'Content-Type': 'application/json'})
        try:
            with self.original(req, timeout=self.cfg.timeout) as response:
                data = response.read()
                return response.status, json.loads(data) if data else None
        except urllib.error.HTTPError as error:
            data = error.read()
            try:
                result = json.loads(data)
            except ValueError:
                result = None
            return error.code, result

    def until(self, fn):
        deadline = time.monotonic() + self.cfg.wait
        while True:
            try:
                if fn():
                    return
            except (urllib.error.URLError, TimeoutError):
                pass  # Only callers' read-only observations are retried, within this budget.
            if time.monotonic() >= deadline:
                raise AssertionError('Readback deadline exceeded')
            time.sleep(self.cfg.interval)


def start_fixture_server():
    """Small native fixture; does not import another test module or case asset."""
    from http.server import BaseHTTPRequestHandler, HTTPServer
    import threading

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def respond(self):
            server = self.server
            server.last_path = self.path
            server.last_body = self.rfile.read(int(self.headers.get('Content-Length', '0')))
            raw = json.dumps(server.response).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        do_GET = respond
        do_POST = respond
        do_DELETE = respond

    class Server(HTTPServer):
        response = {}
        last_path = ''
        last_body = b''

        def set_response(self, body=None):
            self.response = {} if body is None else body

    server = Server(('127.0.0.1', 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server
