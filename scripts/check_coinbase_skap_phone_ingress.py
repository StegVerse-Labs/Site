#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JS = ROOT / "assets/stegfin-phone/coinbase-skap-ingress.js"
UI = ROOT / "assets/stegfin-phone/coinbase-skap-ingress-ui.js"
SUBMISSION = ROOT / "assets/stegfin-phone/coinbase-skap-submission.js"
CFG = ROOT / "assets/stegfin-phone/coinbase-skap-ingress-config.json"
ROUTE = ROOT / "assets/stegfin-phone/coinbase-skap-intr-route.json"
HTML = ROOT / "stegfin-trade.html"
BOOTSTRAP = ROOT / "assets/stegfin-phone/stegid-device-wallet-bootstrap.js"


def require(condition: bool, message: str) -> None:
    if not condition: raise SystemExit(message)


def main() -> int:
    js=JS.read_text(encoding='utf-8'); ui=UI.read_text(encoding='utf-8'); submission=SUBMISSION.read_text(encoding='utf-8'); html=HTML.read_text(encoding='utf-8'); bootstrap=BOOTSTRAP.read_text(encoding='utf-8')
    cfg=json.loads(CFG.read_text(encoding='utf-8')); route=json.loads(ROUTE.read_text(encoding='utf-8'))

    require(cfg.get('schema')=='stegverse.site.coinbase_skap_ingress_config/v1','config schema invalid')
    require(cfg.get('status') in {'NOT_PROVISIONED','PROVISIONED'},'config status invalid')
    require(cfg.get('endpoint_origin')=='https://api.coinbase.com','endpoint origin invalid')
    require(cfg.get('credential_authority')=='TV/TVC','credential authority invalid')
    require(cfg.get('physical_execution_surface')=='CURRENT_USER_IPHONE','physical surface invalid')
    require(cfg.get('second_machine_required') is False,'second machine must not be required')
    require(cfg.get('device_durable_secret_custody') is False,'device custody forbidden')
    require(cfg.get('kv_secret_resolution_authority') is False,'KV resolution forbidden')
    require(cfg.get('github_environment_secret_access') is False,'GitHub secret access forbidden')
    require(cfg.get('submission_redirect_policy')=='DENY_DESTINATION_CHANGE','submission redirect policy invalid')
    require(cfg.get('submission_ambiguous_policy')=='VERIFY_EXTERNALLY','ambiguous submission policy invalid')
    require(cfg.get('submission_blind_retry_allowed') is False,'blind retry must remain disabled')
    if cfg['status']=='NOT_PROVISIONED':
        require(cfg.get('recipient_key_id') is None,'unprovisioned config must not claim recipient key id')
        require(cfg.get('recipient_public_jwk') is None,'unprovisioned config must not claim recipient public key')
        require(cfg.get('submission_status')=='NOT_PROVISIONED','unprovisioned config must not claim primary Gateway readiness')
        require(cfg.get('submission_endpoint') is None,'unprovisioned config must not claim primary Gateway endpoint')
    else:
        jwk=cfg.get('recipient_public_jwk') or {}
        require(jwk.get('kty')=='EC' and jwk.get('crv')=='P-256','provisioned recipient key must be P-256 public JWK')
        require('d' not in jwk,'private JWK material forbidden')
        require(str(cfg.get('recipient_key_id') or '').startswith('tvc://skap/browser-ingress/coinbase/'),'recipient key id authority invalid')
        require(cfg.get('transport_protocol')=='InTr' and cfg.get('credential_custody_target') in {'SKAP','KV_HOSTED_SKAP_VAULT'},'provisioned recipient InTr/SKAP Vault binding invalid')
        for field in ('runtime_instance_id','activation_receipt_hash','liveness_receipt_hash','lease_expires_at'):
            require(cfg.get(field),f'provisioned recipient missing {field}')

    require(route.get('schema')=='stegverse.tvc.skap_browser_intr_route/v1','route schema invalid')
    require(route.get('status') in {'NOT_PROVISIONED','ROUTE_LIVE'},'route status invalid')
    require(route.get('transport_protocol')=='InTr','route transport invalid')
    require(route.get('credential_authority')=='TV/TVC','route credential authority invalid')
    require(route.get('credential_custody_target') in {'SKAP','KV_HOSTED_SKAP_VAULT'},'route custody target invalid')
    require(route.get('public_route_authority') is False,'route authority forbidden')
    require(route.get('provider_operation_authorized') is False,'provider authority forbidden')
    require(route.get('credential_plaintext_carried') is False,'route plaintext carriage forbidden')
    require(route.get('github_token_runtime_authority') is False,'GitHub runtime authority forbidden')
    if route['status']=='NOT_PROVISIONED':
        for field in ('public_origin','public_ingress_url','runtime_instance_id','recipient_key_id','activation_receipt_hash','liveness_receipt_hash','lease_expires_at'):
            require(route.get(field) is None,f'unprovisioned route must not claim {field}')

    # Browser sealing invariants are checked semantically against the current source,
    # not against one obsolete object-literal spelling.
    for marker in (
        'P-256','ECDH','HKDF','SHA-256','AES-GCM','https://api.coinbase.com','CURRENT_USER_IPHONE','STEGVERSE_BROWSER_CAPSULE','TV/TVC','skap://APIs/coinbase/owner/',
        'delete ephemeralPublicJwk.d',"window.StegIDDeviceWalletBootstrap",'issueCurrentPhonePrepareCapability',
        'config?.device_durable_secret_custody!==false','config?.kv_secret_resolution_authority!==false','config?.github_environment_secret_access!==false',
        'device_secret_custody_authority:false','kv_secret_resolution_authority:false','github_environment_secret_access:false','plaintext_present:false'
    ): require(marker in js,f'missing browser ingress invariant: {marker}')

    # Submission now has a primary Gateway first-hop state and a separately-proven
    # SKAP Vault admission state. Neither may confer provider operation authority.
    for marker in (
        'stegverse:coinbase-skap-ingress-sealed',
        "const PRIMARY_GATEWAY_PATH = '/api/coinbase/skap/ingress'",
        "const FALLBACK_ROUTE_PATH = '/v1/skap/coinbase/ingress'",
        "transportMode: 'PRIMARY_GATEWAY'", "transportMode: 'EXPLICIT_FALLBACK'",
        "response.schema !== 'stegverse.service_gateway.coinbase_skap_stage_receipt/v1'",
        "response.decision !== 'STAGED_FOR_TVC'",
        "response.next_required_transition !== 'KV_SKAP_VAULT_INTERLOCK_ADMISSION'",
        "response.tvc_admission_completed !== false",
        "receipt.connector !== 'InTr'", "receipt.from_boundary !== 'DEVICE'", "receipt.to_boundary !== 'KV'",
        "response.decision !== 'ADMITTED_TO_SKAP_VAULT'",
        "second.from_boundary !== 'KV'", "second.to_boundary !== 'SKAP_VAULT'",
        "second.prior_boundary_receipt_hash !== first.receipt_hash",
        "response.kv_decryption_authority !== false", "response.device_durable_secret_custody !== false",
        "response.decryption_performed !== false", "response.rewrap_performed !== false",
        "response.execution_authority !== 'NONE'", "response.may_authorize_order !== false",
        "stegverse:coinbase-skap-ingress-staged-for-tvc", "stegverse:coinbase-skap-vault-admitted",
        'SKAP Vault custody is not yet claimed',
        'coinbase-skap-intr-route.json', 'validatePacketAgainstCurrentRecipient(packet, config)',
        "redirect: 'error'","credentials: 'omit'","referrerPolicy: 'no-referrer'","cache: 'no-store'",'VERIFY_EXTERNALLY','blind retry forbidden'
    ): require(marker in submission,f'missing ciphertext submission invariant: {marker}')
    require('X-StegVerse-Transport' not in submission,'custom CORS header must remain absent')

    combined=js+'\n'+ui+'\n'+submission
    for pattern in (r'localStorage\s*\.\s*setItem\s*\(',r'sessionStorage\s*\.\s*setItem\s*\(',r'indexedDB\s*\.\s*(open|deleteDatabase)\s*\(',r'document\s*\.\s*cookie\s*=',r'console\s*\.\s*(log|debug|info|warn|error)\s*\(',r'navigator\s*\.\s*sendBeacon\s*\('):
        require(re.search(pattern,combined) is None,f'forbidden credential persistence/logging call: {pattern}')

    require('coinbaseApiKeyName' in html and 'coinbaseApiPrivateKey' in html,'credential fields missing')
    require(re.search(r'id="coinbaseApiKeyName"[^>]*\sdisabled',html) is not None,'API key input must default disabled')
    require(re.search(r'id="coinbaseApiPrivateKey"[^>]*\sdisabled',html) is not None,'private-key input must default disabled')
    require(re.search(r'id="coinbaseSealCredential"[^>]*\sdisabled',html) is not None,'seal action must default disabled')
    require('coinbase-skap-ingress.js' in html and 'coinbase-skap-ingress-ui.js' in html and 'coinbase-skap-submission.js' in html,'SKAP ingress/submission scripts not projected')
    normalized=re.sub(r'[-\u2010-\u2015]',' ',html.lower())
    require('skap public ingress key' in normalized,'fail-closed public-key explanation missing')
    require('governed stegverse' in normalized and 'receiver' in normalized,'governed receiver explanation missing')
    require('blind retries' in normalized or 'blind retry' in normalized,'blind-retry boundary explanation missing')
    require('navigator.credentials.create' in bootstrap and 'navigator.credentials.get' in bootstrap,'WebAuthn ceremony missing')
    require("userVerification: 'required'" in bootstrap,'WebAuthn user verification weakened')
    require("credential_authority: 'TV/TVC'" in bootstrap,'TV/TVC authority missing from owner authorization surface')

    print('COINBASE_SKAP_PHONE_INGRESS_SOURCE_OK')
    print(f"config_status={cfg['status']}"); print(f"route_status={route['status']}")
    print('physical_surface=CURRENT_USER_IPHONE')
    print('device_durable_secret_custody=false')
    print('ordinary_kv_decryption_authority=false')
    print('device_kv_intr_required=true')
    print('kv_skap_vault_intr_required=true')
    print('gateway_stage_is_skap_vault_admission=false')
    print('endpoint_verification_required_before_decryption=true')
    print('ambiguous_submission_policy=VERIFY_EXTERNALLY')
    print('blind_retry_allowed=false')
    return 0

if __name__=='__main__': raise SystemExit(main())
