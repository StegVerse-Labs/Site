#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUBMIT = ROOT / 'assets/stegfin-phone/coinbase-skap-submission.js'
ROUTE = ROOT / 'assets/stegfin-phone/coinbase-skap-intr-route.json'
CONFIG = ROOT / 'assets/stegfin-phone/coinbase-skap-ingress-config.json'
HANDOFF = ROOT / 'docs/STEGFIN_SKAP_INTR_SUBMIT_MIRROR_HANDOFF.md'


def main() -> int:
    failures: list[str] = []
    js = SUBMIT.read_text(encoding='utf-8')
    route = json.loads(ROUTE.read_text(encoding='utf-8'))
    config = json.loads(CONFIG.read_text(encoding='utf-8'))
    handoff = HANDOFF.read_text(encoding='utf-8')

    # Production repository state remains deliberately unprovisioned. CI must not
    # invent a rotating TVC origin or claim a resident route exists.
    expected_route = {
        'schema': 'stegverse.tvc.skap_browser_intr_route/v1',
        'status': 'NOT_PROVISIONED',
        'transport_protocol': 'InTr',
        'credential_authority': 'TV/TVC',
        'credential_custody_target': 'SKAP',
        'public_route_authority': False,
        'provider_operation_authorized': False,
        'credential_plaintext_carried': False,
        'github_token_runtime_authority': False,
        'github_actions_resident_authority': False,
    }
    for key, value in expected_route.items():
        if route.get(key) != value: failures.append(f'route.{key} expected {value!r}, got {route.get(key)!r}')
    for key in ('public_origin','public_ingress_url','health_url','runtime_instance_id','recipient_key_id','activation_receipt_hash','liveness_receipt_hash','lease_expires_at','route_receipt_hash'):
        if route.get(key) is not None: failures.append(f'production route unexpectedly populated: {key}')
    if 'trycloudflare.com' in json.dumps(route).lower(): failures.append('production route hardcodes rotating carrier origin')

    if config.get('status') != 'NOT_PROVISIONED': failures.append('recipient config must remain NOT_PROVISIONED in repository state')
    if config.get('credential_authority') != 'TV/TVC': failures.append('recipient config credential authority drift')

    required_js = [
        "const ROUTE_URL = './assets/stegfin-phone/coinbase-skap-intr-route.json'",
        "route?.schema !== ROUTE_SCHEMA || route?.status !== 'ROUTE_LIVE'",
        "route?.transport_protocol !== 'InTr'",
        "route?.credential_authority !== 'TV/TVC'",
        "route?.credential_custody_target !== 'SKAP'",
        "route?.public_route_authority !== false",
        "route?.provider_operation_authorized !== false",
        "route?.credential_plaintext_carried !== false",
        "route?.github_token_runtime_authority !== false",
        "route?.github_actions_resident_authority !== false",
        "['runtime_instance_id', 'recipient_key_id', 'activation_receipt_hash', 'liveness_receipt_hash', 'lease_expires_at']",
        "endpoint.pathname !== ROUTE_PATH",
        "endpoint.hostname.endsWith('.trycloudflare.com')",
        "const { config, endpoint } = await loadSubmissionConfig()",
        "validatePacketAgainstCurrentRecipient(packet, config)",
        "packet.recipient_runtime_instance_id !== config.runtime_instance_id",
        "packet.recipient_lease_expires_at !== config.lease_expires_at",
        "packet.sealed_material?.recipient_key_id !== config.recipient_key_id",
        "redirect: 'error'",
        "credentials: 'omit'",
        "referrerPolicy: 'no-referrer'",
        "'Content-Type': 'application/json'",
        "'Accept': 'application/json'",
        "VERIFY_EXTERNALLY",
        "blind retry forbidden",
        "NEW_OWNER_AUTHORIZED_PACKET_REQUIRED",
        "response.execution_authority !== 'NONE'",
        "response.may_authorize_order !== false",
        "IPHONE_BROWSER_SEALED->SKAP_CIPHERTEXT_CUSTODY",
        "sealed_material_persisted_unchanged !== true",
        "decryption_performed_at_ingress !== false",
        "rewrap_performed_at_ingress !== false",
    ]
    for marker in required_js:
        if marker not in js: failures.append(f'submission invariant missing: {marker}')

    if 'X-StegVerse-Transport' in js: failures.append('submission retains custom header not admitted by TVC CORS preflight')
    for forbidden in ('console.log(', 'localStorage.setItem(', 'sessionStorage.setItem('):
        if forbidden in js: failures.append(f'submission contains forbidden persistence/logging marker: {forbidden}')

    for marker in (
        'recipient config = how/where the capsule is sealed',
        'route descriptor = where the current InTr carrier terminates',
        'Immediately before POST',
        'provider-operation authority from route availability: `NONE`',
        'Production activation remains separately open',
    ):
        if marker not in handoff: failures.append(f'handoff invariant missing: {marker}')

    if failures:
        print('STEGFIN_SKAP_INTR_SUBMIT_FAIL')
        for failure in failures: print(f'- {failure}')
        return 1
    print('STEGFIN_SKAP_INTR_SUBMIT_PASS')
    print('production_route=NOT_PROVISIONED')
    print('credential_authority=TV/TVC')
    print('site_credential_custody=NONE')
    print('provider_operation_authority=NONE')
    print('blind_retry_allowed=false')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
