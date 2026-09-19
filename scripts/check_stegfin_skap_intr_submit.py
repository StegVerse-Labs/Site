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
    # a recipient key or primary Gateway URL.
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
        if route.get(key) is not None: failures.append(f'legacy route descriptor unexpectedly populated: {key}')

    if config.get('status') != 'NOT_PROVISIONED': failures.append('recipient config must remain NOT_PROVISIONED in repository state')
    if config.get('credential_authority') != 'TV/TVC': failures.append('recipient config credential authority drift')
    if config.get('submission_status') != 'NOT_PROVISIONED': failures.append('primary Gateway must remain NOT_PROVISIONED in repository state')
    if config.get('submission_endpoint') is not None: failures.append('production primary Gateway endpoint unexpectedly populated')

    required_js = [
        "const PRIMARY_GATEWAY_PATH = '/api/coinbase/skap/ingress'",
        "transportMode: 'PRIMARY_GATEWAY'",
        "config?.submission_status !== 'PROVISIONED'",
        "submission_allowed_origins.length !== 1",
        "submission_allowed_origins[0] !== endpoint.origin",
        "public_route_hostname !== endpoint.hostname",
        "public_route_observation_digest",
        "public_route_observed_at",
        "public_route_max_age_seconds",
        "ready_for_owner_ingress !== true",
        "provider_operation_authorized !== false",
        "provider_operation_started !== false",
        "submission_blind_retry_allowed !== false",
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
        "state: 'STAGED_FOR_TVC'",
        "stegverse:coinbase-skap-ingress-staged-for-tvc",
        "redirect: 'error'",
        "credentials: 'omit'",
        "referrerPolicy: 'no-referrer'",
        "VERIFY_EXTERNALLY",
        "blind retry forbidden",
    ]
    for marker in required_js:
        if marker not in js: failures.append(f'submission invariant missing: {marker}')

    for forbidden in ('trycloudflare.com','EXPLICIT_FALLBACK','FALLBACK_CARRIER','validateFallbackRoute','coinbase-skap-vault-admitted'):
        if forbidden in js: failures.append(f'third-party/fallback admission path remains: {forbidden}')
    if 'SKAP Vault custody is not yet claimed' not in js:
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
    print('third_party_fallback=ABSENT')
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
