#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def require(ok,msg):
    if not ok: raise SystemExit('SITE_SKAP_INTR_ROUTE_FAIL:'+msg)

def main():
    ingress=(ROOT/'assets/stegfin-phone/coinbase-skap-ingress.js').read_text()
    submit=(ROOT/'assets/stegfin-phone/coinbase-skap-submission.js').read_text()
    ui=(ROOT/'assets/stegfin-phone/coinbase-skap-ingress-ui.js').read_text()
    route=json.loads((ROOT/'assets/stegfin-phone/coinbase-skap-intr-route.json').read_text())
    for marker in ("!['SKAP','KV_HOSTED_SKAP_VAULT'].includes(config?.credential_custody_target)","transport_protocol!=='InTr'","liveness_receipt_hash","recipient_runtime_instance_id:config.runtime_instance_id","recipient_lease_expires_at:config.lease_expires_at","'d' in config.recipient_public_jwk","sealCoinbaseCredential"):
        require(marker in ingress,'missing sealing invariant '+marker)
    for marker in ("route?.status !== 'ROUTE_LIVE'","route?.[field] !== config?.[field]","endpoint.hostname.endsWith('.trycloudflare.com')","submission_allowed_origins.length !== 1","submission_allowed_origins[0] !== endpoint.origin","public_route_hostname !== endpoint.hostname","public_route_observation_digest","public_route_observed_at","public_route_max_age_seconds","ready_for_owner_ingress !== true","provider_operation_authorized !== false","provider_operation_started !== false","submission_blind_retry_allowed !== false","credentials: 'omit'","redirect: 'error'","referrerPolicy: 'no-referrer'","VERIFY_EXTERNALLY","blind retry forbidden","execution_authority !== 'NONE'","may_authorize_order !== false","sealed_material_persisted_unchanged !== true"):
        require(marker in submit,'missing submission invariant '+marker)
    for marker in ('StegFinCoinbaseSkapSubmission','loadSubmissionConfig','sealCoinbaseCredential','stegverse:coinbase-skap-ingress-sealed'):
        require(marker in ui,'missing UI invariant '+marker)
    require(route.get('schema')=='stegverse.tvc.skap_browser_intr_route/v1','route schema')
    require(route.get('status')=='NOT_PROVISIONED','repository route must remain fail closed')
    require(route.get('transport_protocol')=='InTr','transport')
    require(route.get('credential_authority')=='TV/TVC' and route.get('credential_custody_target')=='SKAP','authority/custody')
    for key in ('public_route_authority','provider_operation_authorized','credential_plaintext_carried','github_token_runtime_authority','github_actions_resident_authority'):
        require(route.get(key) is False,key)
    require(route.get('public_origin') is None and route.get('public_ingress_url') is None and route.get('route_receipt_hash') is None,'unproved route exposed')
    require("!['stegverse.org', 'www.stegverse.org'].includes(endpoint.hostname)" not in submit,'primary route must be receipt-bound, not hard-coded to a hostname list')
    print('SITE_SKAP_INTR_ROUTE_PASS')
    return 0
if __name__=='__main__': raise SystemExit(main())
