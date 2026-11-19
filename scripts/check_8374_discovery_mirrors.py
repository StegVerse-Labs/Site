#!/usr/bin/env python3
"""Verify historical discovery data without contacting the service origin."""
from __future__ import annotations
import argparse
import copy
from datetime import datetime
from functools import partial
import hashlib
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import shutil
import tempfile
from threading import Thread
from urllib.request import ProxyHandler, build_opener

ROOT = Path(__file__).resolve().parents[1]
REL = Path('0r10n15-8374/discovery')
SOURCES = {'offer.json': 'https://8374.stegverse.org/offer',
           'openapi.json': 'https://8374.stegverse.org/openapi.json',
           'x402.json': 'https://8374.stegverse.org/.well-known/x402'}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def strict_json(data):
    def pairs(items):
        out = {}
        for key, value in items:
            require(key not in out, 'duplicate JSON key: ' + key)
            out[key] = value
        return out
    def constant(value):
        raise ValueError('non-finite JSON number: ' + value)
    return json.loads(data, object_pairs_hook=pairs, parse_constant=constant)

def verify(root=ROOT):
    folder = root / REL
    manifest = strict_json((folder / 'manifest.json').read_bytes())
    require(manifest['schema'] == 'stegverse.8374.discovery-snapshot/v1', 'schema')
    require(manifest['status'] == 'CAPTURED_HISTORICAL_SNAPSHOT', 'historical status')
    require(manifest['authority_effect'] == 'NONE', 'authority')
    for field in ['payment_authority', 'runtime_authority', 'automated_failover_for_signed_operations']:
        require(manifest[field] is False, field)
    require(manifest['fresh_live_402_required'] is True, 'fresh live challenge')
    stamp = manifest['captured_at']
    require(stamp.endswith('Z') and datetime.fromisoformat(stamp.replace('Z', '+00:00')).utcoffset().total_seconds() == 0, 'capture date UTC')
    require(manifest['source_service'] == 'https://8374.stegverse.org', 'source service')
    records = manifest['files']
    require(len(records) == 3 and {r['path'] for r in records} == set(SOURCES), 'exact safe document paths')
    require(len({r['id'] for r in records}) == 3, 'unique document ids')
    payloads = {}
    for row in records:
        path = row['path']
        require(row['source_url'] == SOURCES[path], 'source URL')
        require(row['observed_http_status'] == 200, 'captured HTTP status')
        require(row['observed_content_type'].split(';')[0] == 'application/json', 'captured media type')
        require(row['wire_headers_verified'] is False, 'no invented transport verification')
        data = (folder / path).read_bytes()
        require(type(row['bytes']) is int and row['bytes'] == len(data), 'byte count')
        require(hashlib.sha256(data).hexdigest() == row['sha256'], 'SHA256')
        obj = strict_json(data)
        require(isinstance(obj, dict) and obj, 'JSON object document')
        payloads[path] = data
    require(strict_json(payloads['offer.json']).get('document') == 'OFFER__MACHINE__READABLE__01', 'offer identity')
    require(strict_json(payloads['openapi.json']).get('openapi') == '3.1.0', 'OpenAPI identity')
    require(isinstance(strict_json(payloads['x402.json']).get('resources'), list), 'x402 discovery identity')
    html = (folder / 'index.html').read_text()
    require('Historical snapshot' in html and stamp in html and 'fresh live 402' in html, 'visible capture/payment boundary')
    for path in list(SOURCES) + ['manifest.json']:
        require('href="' + path + '"' in html, 'local snapshot link ' + path)
    require('href="discovery/"' in (root / '0r10n15-8374/index.html').read_text(), 'service discovery link')
    return manifest, payloads

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass

def offline_http(root):
    verify(root)
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(root)))
    thread = Thread(target=server.serve_forever, daemon=True); thread.start()
    opener = build_opener(ProxyHandler({}))
    try:
        for path in list(SOURCES) + ['manifest.json', 'index.html']:
            url = 'http://127.0.0.1:' + str(server.server_port) + '/' + REL.as_posix() + '/' + path
            with opener.open(url, timeout=5) as response:
                require(response.status == 200, 'local HTTP status')
                require(response.read() == (root / REL / path).read_bytes(), 'full local HTTP bytes')
    finally:
        server.shutdown(); server.server_close(); thread.join(timeout=5)
    return {'local_http_documents': 5, 'origin_http_requests': 0, 'verdict': 'PASS_ORIGIN_NOT_USED'}

def negative_controls(root):
    count = 0
    with tempfile.TemporaryDirectory(prefix='8374-mirror-controls-') as directory:
        test = Path(directory); shutil.copytree(root / REL, test / REL)
        (test / '0r10n15-8374/index.html').write_bytes((root / '0r10n15-8374/index.html').read_bytes())
        folder = test / REL
        original = {p.name: p.read_bytes() for p in folder.iterdir() if p.is_file()}
        def reject(change):
            nonlocal count
            for p in folder.iterdir():
                if p.is_file(): p.unlink()
            for name, data in original.items(): (folder / name).write_bytes(data)
            change(folder)
            try:
                verify(test)
            except (ValueError, KeyError, OSError, TypeError): count += 1
            else: raise ValueError('negative control unexpectedly accepted')
        def mutate(folder, field, value):
            m = strict_json((folder / 'manifest.json').read_bytes()); m[field] = value
            (folder / 'manifest.json').write_text(json.dumps(m))
        reject(lambda f: (f / 'offer.json').write_bytes(original['offer.json'] + b' '))
        reject(lambda f: (f / 'openapi.json').unlink())
        reject(lambda f: mutate(f, 'payment_authority', True))
        reject(lambda f: mutate(f, 'source_service', 'https://unrelated.invalid'))
        m = strict_json(original['manifest.json']); bad = copy.deepcopy(m['files']); bad[0]['path'] = '../offer.json'
        reject(lambda f: mutate(f, 'files', bad))
        reject(lambda f: (f / 'manifest.json').write_text('{"schema":"one","schema":"two"}'))
        reject(lambda f: (f / 'manifest.json').write_text('{"schema":NaN}'))
        reject(lambda f: (f / 'index.html').write_text('No capture or payment boundary.'))
    return count

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--offline-http', action='store_true')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args(); manifest, payloads = verify()
    result = {'verdict': 'PASS_STATIC_DISCOVERY_SNAPSHOTS', 'documents': len(payloads), 'captured_at': manifest['captured_at'], 'payment_authority': False}
    if args.offline_http: result['offline'] = offline_http(ROOT)
    if args.self_test: result['negative_controls_rejected'] = negative_controls(ROOT)
    print(json.dumps(result, sort_keys=True))

if __name__ == '__main__': main()
