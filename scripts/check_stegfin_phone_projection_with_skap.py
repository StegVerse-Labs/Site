#!/usr/bin/env python3
from __future__ import annotations

import json, re, subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PAGE=ROOT/'stegfin-trade.html'
LEGACY=ROOT/'scripts/check_stegfin_phone_projection.py'
SKAP='./assets/stegfin-phone/coinbase-skap-ingress.js'
SKAP_UI='./assets/stegfin-phone/coinbase-skap-ingress-ui.js'
ROUTE=ROOT/'assets/stegfin-phone/coinbase-skap-intr-route.json'


def require(ok: bool, msg: str):
    if not ok: raise SystemExit('STEGFIN_PHONE_SKAP_EXTENSION_FAIL:'+msg)


def main() -> int:
    original=PAGE.read_text(encoding='utf-8')
    scripts=re.findall(r'<script\s+src="([^"]+)"',original)
    expected=[
      './assets/stegfin-phone/rpc-resilience.js',
      './assets/stegfin-phone/phone-direct-route.js',
      './assets/stegfin-phone/stegid-device-wallet-bootstrap.js',
      './assets/stegfin-phone/device-wallet-identity.js',
      SKAP, SKAP_UI,
      './assets/stegfin-phone/app.js',
      './assets/stegfin-phone/evidence-export.js',
    ]
    require(scripts==expected,f'unexpected extended script order: {scripts}')
    ingress=(ROOT/'assets/stegfin-phone/coinbase-skap-ingress.js').read_text(encoding='utf-8')
    ui=(ROOT/'assets/stegfin-phone/coinbase-skap-ingress-ui.js').read_text(encoding='utf-8')
    for marker in (
      "config?.private_key_liveness_required !== true",
      "config.lease_expires_at",
      "lease <= Date.now()",
      "recipient_public_jwk_sha256 !== await sha256(config.recipient_public_jwk)",
      "credential_custody_target !== 'SKAP'",
      "transport_protocol !== 'InTr'",
      "private_key_present !== false",
      "recipient_runtime_instance_id: config.runtime_instance_id",
      "recipient_lease_expires_at: config.lease_expires_at",
      "const ROUTE_URL = './assets/stegfin-phone/coinbase-skap-intr-route.json'",
      "route?.status !== 'ROUTE_LIVE'",
      "route?.runtime_instance_id !== config.runtime_instance_id",
      "route?.activation_receipt_hash !== config.activation_receipt_hash",
      "route?.liveness_receipt_hash !== config.liveness_receipt_hash",
      "route?.lease_expires_at !== config.lease_expires_at",
      "origin.hostname.endsWith('.trycloudflare.com')",
      "credentials: 'omit'",
      "redirect: 'error'",
      "referrerPolicy: 'no-referrer'",
      "VERIFY_EXTERNALLY and do not retry this ingress_id",
      "decryption_performed_at_ingress !== false",
      "rewrap_performed_at_ingress !== false",
      "execution_authority !== 'NONE'",
      "may_authorize_order !== false",
      "sealAndSubmitCoinbaseCredential",
    ):
        require(marker in ingress,'missing SKAP ingress/route invariant: '+marker)
    require("'d' in config.recipient_public_jwk" in ingress,'public-only recipient JWK check missing')
    for marker in (
      'sealAndSubmitCoinbaseCredential',
      'Ciphertext admitted into SKAP custody through InTr',
      'No provider operation was authorized',
      'Do not retry an ambiguous ingress packet',
      'stegverse:coinbase-skap-ingress-admitted',
    ):
        require(marker in ui,'missing SKAP ingress UI invariant: '+marker)

    route=json.loads(ROUTE.read_text(encoding='utf-8'))
    require(route.get('schema')=='stegverse.tvc.skap_browser_intr_route/v1','route schema drift')
    require(route.get('status')=='NOT_PROVISIONED','repository route must remain fail-closed until resident projection')
    require(route.get('transport_protocol')=='InTr','route transport drift')
    require(route.get('credential_authority')=='TV/TVC' and route.get('credential_custody_target')=='SKAP','route authority drift')
    for key in ('public_route_authority','provider_operation_authorized','credential_plaintext_carried','github_token_runtime_authority','github_actions_resident_authority'):
        require(route.get(key) is False,f'route authority flag drift: {key}')
    require(route.get('public_origin') is None and route.get('public_ingress_url') is None and route.get('route_receipt_hash') is None,'unproved route must not expose endpoint')

    normalized=original
    for src in (SKAP,SKAP_UI):
        normalized=re.sub(rf'\s*<script\s+src="{re.escape(src)}"[^>]*></script>', '', normalized, count=1)
    PAGE.write_text(normalized,encoding='utf-8')
    try:
        completed=subprocess.run(['python3',str(LEGACY)],cwd=ROOT,check=False)
        require(completed.returncode==0,'legacy phone projection checker failed')
    finally:
        PAGE.write_text(original,encoding='utf-8')
    print('STEGFIN_PHONE_SKAP_EXTENSION_PASS')
    return 0

if __name__=='__main__': raise SystemExit(main())
