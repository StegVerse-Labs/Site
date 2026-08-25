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

    # Production repository state stays fail-closed. CI must not fabricate either
    # a recipient key, primary Gateway URL, or rotating fallback route.
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
        if route.get(key) is not None: failures.append(f'production fallback route unexpectedly populated: {key}')
    if 'trycloudflare.com' in json.dumps(route).lower(): failures.append('production fallback route hardcodes rotating carrier origin')

    if config.get('status') != 'NOT_PROVISIONED': failures.append('recipient config must remain NOT_PROVISIONED in repository state')
    if config.get('credential_authority') != 'TV/TVC': failures.append('recipient config credential authority drift')
    if config.get('submission_status') != 'NOT_PROVISIONED': failures.append('primary Gateway must remain NOT_PROVISIONED in repository state')
    if config.get('submission_endpoint') is not None: failures.append('production primary Gateway endpoint unexpectedly populated')

    required_js = [
        "const PRIMARY_GATEWAY_PATH = '/api/coinbase/skap/ingress'",
        "const FALLBACK_ROUTE_PATH = '/v1/skap/coinbase/ingress'",
        "transportMode: 'PRIMARY_GATEWAY'",
        "transportMode: 'EXPLICIT_FALLBACK'",
        "config?.submission_status !== 'PROVISIONED'",
        "['stegverse.org', 'www.stegverse.org'].includes(endpoint.hostname)",
        "route?.schema !== ROUTE_SCHEMA || route?.status !== 'ROUTE_LIVE'",
        "route?.carrier !== FALLBACK_CARRIER",
        "route?.public_route_authority !== false",
        "route?.provider_operation_authorized !== false",
        "packet.recipient_runtime_instance_id !== config.runtime_instance_id",
        "packet.recipient_lease_expires_at !== config.lease_expires_at",
        "packet.sealed_material?.recipient_key_id !== config.recipient_key_id",
        "response.schema !== 'stegverse.service_gateway.coinbase_skap_stage_receipt/v1'",
        "response.decision !== 'STAGED_FOR_TVC'",
        "response.next_required_transition !== 'KV_SKAP_VAULT_INTERLOCK_ADMISSION'",
        "response.tvc_admission_completed !== false",
        "receipt.from_boundary !== 'DEVICE'",
        "receipt.to_boundary !== 'KV'",
        "receipt.connector !== 'InTr'",
        "response.decision !== 'ADMITTED_TO_SKAP_VAULT'",
        "second.from_boundary !== 'KV'",
        "second.to_boundary !== 'SKAP_VAULT'",
        "second.prior_boundary_receipt_hash !== first.receipt_hash",
        "response.kv_decryption_authority !== false",
        "response.device_durable_secret_custody !== false",
        "response.execution_authority !== 'NONE'",
        "response.may_authorize_order !== false",
        "state: 'STAGED_FOR_TVC'",
        "state: 'ADMITTED_TO_SKAP_VAULT'",
        "stegverse:coinbase-skap-ingress-staged-for-tvc",
        "stegverse:coinbase-skap-vault-admitted",
        "redirect: 'error'",
        "credentials: 'omit'",
        "referrerPolicy: 'no-referrer'",
        "VERIFY_EXTERNALLY",
        "blind retry forbidden",
    ]
    for marker in required_js:
        if marker not in js: failures.append(f'submission invariant missing: {marker}')

    # A Gateway stage response must never be translated into the admitted event.
    gateway_branch = js[js.find("if (result.state === 'STAGED_FOR_TVC')"):js.find("} else {", js.find("if (result.state === 'STAGED_FOR_TVC')"))]
    if 'coinbase-skap-vault-admitted' in gateway_branch:
        failures.append('Gateway STAGED_FOR_TVC branch emits SKAP Vault admission event')
    if 'SKAP Vault custody is not yet claimed' not in gateway_branch:
        failures.append('Gateway staging UI does not explicitly deny SKAP Vault custody claim')

    if 'X-StegVerse-Transport' in js: failures.append('submission retains custom header not admitted by TVC CORS preflight')
    for forbidden in ('console.log(', 'localStorage.setItem(', 'sessionStorage.setItem('):
        if forbidden in js: failures.append(f'submission contains forbidden persistence/logging marker: {forbidden}')

    for marker in (
        'Device <-InTr-> KV <-InTr-> SKAP Vault',
        'STAGED_FOR_TVC',
        'ADMITTED_TO_SKAP_VAULT',
        'first interlock complete',
        'KV/SKAP_VAULT receipt whose prior hash binds the first receipt',
        'ordinary KV decryption authority: `NONE`',
        'Production activation remains open',
    ):
        if marker not in handoff: failures.append(f'handoff invariant missing: {marker}')

    if failures:
        print('STEGFIN_SKAP_INTR_SUBMIT_FAIL')
        for failure in failures: print(f'- {failure}')
        return 1
    print('STEGFIN_SKAP_INTR_SUBMIT_PASS')
    print('production_recipient=NOT_PROVISIONED')
    print('production_primary_gateway=NOT_PROVISIONED')
    print('production_fallback_route=NOT_PROVISIONED')
    print('credential_authority=TV/TVC')
    print('site_credential_custody=NONE')
    print('ordinary_kv_decryption_authority=NONE')
    print('device_kv_intr_required=true')
    print('kv_skap_vault_intr_required=true')
    print('gateway_stage_is_skap_vault_admission=false')
    print('blind_retry_allowed=false')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
