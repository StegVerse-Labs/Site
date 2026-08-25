#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / 'stegfin-trade.html'
SKAP = './assets/stegfin-phone/coinbase-skap-ingress.js'
SUBMIT = './assets/stegfin-phone/coinbase-skap-submission.js'
SKAP_UI = './assets/stegfin-phone/coinbase-skap-ingress-ui.js'
ROUTE = ROOT / 'assets/stegfin-phone/coinbase-skap-intr-route.json'
CONFIG = ROOT / 'assets/stegfin-phone/coinbase-skap-ingress-config.json'


def require(ok: bool, msg: str) -> None:
    if not ok:
        raise SystemExit('STEGFIN_PHONE_SKAP_EXTENSION_FAIL:' + msg)


def run_checker(path: str) -> None:
    completed = subprocess.run(['python3', path], cwd=ROOT, check=False)
    require(completed.returncode == 0, f'successor dependency failed: {path}')


def main() -> int:
    page = PAGE.read_text(encoding='utf-8')
    scripts = re.findall(r'<script\s+src="([^"]+)"', page)
    expected = [
        './assets/stegfin-phone/rpc-resilience.js',
        './assets/stegfin-phone/phone-direct-route.js',
        './assets/stegfin-phone/stegid-device-wallet-bootstrap.js',
        './assets/stegfin-phone/device-wallet-identity.js',
        SKAP,
        SUBMIT,
        SKAP_UI,
        './assets/stegfin-phone/app.js',
        './assets/stegfin-phone/evidence-export.js',
    ]
    require(scripts == expected, f'unexpected extended script order: {scripts}')
    require(not any(src.startswith(('http://', 'https://')) for src in scripts), 'remote executable script dependency prohibited')

    ingress = (ROOT / 'assets/stegfin-phone/coinbase-skap-ingress.js').read_text(encoding='utf-8')
    submit = (ROOT / 'assets/stegfin-phone/coinbase-skap-submission.js').read_text(encoding='utf-8')
    ui = (ROOT / 'assets/stegfin-phone/coinbase-skap-ingress-ui.js').read_text(encoding='utf-8')

    for marker in (
        "config?.private_key_liveness_required!==true",
        "config.lease_expires_at",
        "liveness_receipt_hash",
        "['SKAP','KV_HOSTED_SKAP_VAULT'].includes(config?.credential_custody_target)",
        "transport_protocol!=='InTr'",
        "private_key_present!==false",
        "recipient_runtime_instance_id:config.runtime_instance_id",
        "recipient_lease_expires_at:config.lease_expires_at",
        "'d' in config.recipient_public_jwk",
        "sealCoinbaseCredential",
        "device_secret_custody_authority:false",
        "kv_secret_resolution_authority:false",
    ):
        require(marker in ingress, 'missing SKAP sealing invariant: ' + marker)

    for marker in (
        "const PRIMARY_GATEWAY_PATH = '/api/coinbase/skap/ingress'",
        "const FALLBACK_ROUTE_PATH = '/v1/skap/coinbase/ingress'",
        "transportMode: 'PRIMARY_GATEWAY'",
        "transportMode: 'EXPLICIT_FALLBACK'",
        "response.decision !== 'STAGED_FOR_TVC'",
        "response.next_required_transition !== 'KV_SKAP_VAULT_INTERLOCK_ADMISSION'",
        "response.tvc_admission_completed !== false",
        "receipt.from_boundary !== 'DEVICE'",
        "receipt.to_boundary !== 'KV'",
        "response.decision !== 'ADMITTED_TO_SKAP_VAULT'",
        "second.from_boundary !== 'KV'",
        "second.to_boundary !== 'SKAP_VAULT'",
        "second.prior_boundary_receipt_hash !== first.receipt_hash",
        "response.kv_decryption_authority !== false",
        "response.device_durable_secret_custody !== false",
        "credentials: 'omit'",
        "redirect: 'error'",
        "referrerPolicy: 'no-referrer'",
        "VERIFY_EXTERNALLY",
        "blind retry forbidden",
        "execution_authority !== 'NONE'",
        "may_authorize_order !== false",
        "stegverse:coinbase-skap-ingress-staged-for-tvc",
        "stegverse:coinbase-skap-vault-admitted",
        "SKAP Vault custody is not yet claimed",
    ):
        require(marker in submit, 'missing SKAP submission invariant: ' + marker)

    for marker in (
        'StegFinCoinbaseSkapSubmission',
        'loadSubmissionConfig',
        'sealCoinbaseCredential',
        'stegverse:coinbase-skap-ingress-sealed',
        'ciphertext submission revalidates the route again',
    ):
        require(marker in ui, 'missing SKAP ingress UI invariant: ' + marker)

    route = json.loads(ROUTE.read_text(encoding='utf-8'))
    config = json.loads(CONFIG.read_text(encoding='utf-8'))
    require(route.get('schema') == 'stegverse.tvc.skap_browser_intr_route/v1', 'route schema drift')
    require(route.get('status') == 'NOT_PROVISIONED', 'repository fallback route must remain fail-closed')
    require(route.get('transport_protocol') == 'InTr', 'route transport drift')
    require(route.get('credential_authority') == 'TV/TVC', 'route credential authority drift')
    require(route.get('credential_custody_target') in {'SKAP', 'KV_HOSTED_SKAP_VAULT'}, 'route custody target drift')
    for key in ('public_route_authority','provider_operation_authorized','credential_plaintext_carried','github_token_runtime_authority','github_actions_resident_authority'):
        require(route.get(key) is False, f'route authority flag drift: {key}')
    require(route.get('public_origin') is None and route.get('public_ingress_url') is None and route.get('route_receipt_hash') is None, 'unproved fallback route must not expose endpoint')

    require(config.get('status') == 'NOT_PROVISIONED', 'repository recipient config must remain fail-closed')
    require(config.get('submission_status') == 'NOT_PROVISIONED', 'repository primary Gateway must remain fail-closed')
    require(config.get('submission_endpoint') is None, 'unproved primary Gateway must not expose endpoint')
    require(config.get('credential_authority') == 'TV/TVC', 'recipient credential authority drift')

    # Reuse current behavior-oriented validators instead of the obsolete pre-SKAP
    # page-order/historical-marker checker. This is the canonical extended surface.
    run_checker('scripts/check_coinbase_skap_phone_ingress.py')
    run_checker('scripts/check_stegfin_skap_intr_submit.py')

    # Retain core pre-SKAP wallet authority invariants directly on the extended page.
    app = (ROOT / 'assets/stegfin-phone/app.js').read_text(encoding='utf-8')
    bootstrap = (ROOT / 'assets/stegfin-phone/stegid-device-wallet-bootstrap.js').read_text(encoding='utf-8')
    evidence = (ROOT / 'assets/stegfin-phone/evidence-export.js').read_text(encoding='utf-8')
    for marker in ('automatic_signing', 'automatic_broadcast', 'USER_ONLY', 'TV/TVC'):
        require(marker in app or marker in evidence, 'core wallet authority invariant missing: ' + marker)
    require('navigator.credentials.create' in bootstrap and 'navigator.credentials.get' in bootstrap, 'WebAuthn ceremony missing')
    require("userVerification: 'required'" in bootstrap, 'WebAuthn user verification weakened')
    require('GITHUB_TOKEN' not in ingress + submit + ui, 'SKAP browser surface contains GitHub token authority marker')

    print('STEGFIN_PHONE_SKAP_EXTENSION_PASS')
    print('canonical_credential_topology=DEVICE_INTR_KV_INTR_SKAP_VAULT')
    print('primary_gateway_stage_is_skap_vault_admission=false')
    print('production_recipient=NOT_PROVISIONED')
    print('production_primary_gateway=NOT_PROVISIONED')
    print('production_fallback_route=NOT_PROVISIONED')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
