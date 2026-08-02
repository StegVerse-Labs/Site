#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

ALLOWED_STATES={"RECONSTRUCTED_HASH_VERIFIED","PRIVATE_REVIEW_ACCEPTED","QUARANTINE","REJECT","MASTER_RECORD_CANDIDATE_VALIDATED","ACTIVATED"}

def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def fail(m): raise ValueError(m)

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("projection"); ap.add_argument("--expected-response-sha256"); a=ap.parse_args()
    p=load(a.projection)
    if p.get("schema_version")!="HIL-SITE-LIFECYCLE-PROJECTION-RECEIPT-v1": fail("schema")
    if p.get("state") not in ALLOWED_STATES: fail("state")
    if not p.get("submission_id") or not p.get("response_sha256"): fail("identity_missing")
    if a.expected_response_sha256 and p["response_sha256"]!=a.expected_response_sha256: fail("response_hash_mismatch")
    if p.get("publication_authorized") is True and not p.get("publication_decision_id"): fail("publication_without_decision")
    if p.get("release_authorized") is True and not p.get("release_decision_id"): fail("release_without_decision")
    if p.get("state")=="ACTIVATED" and not p.get("stegcore_activation_receipt_id"): fail("activation_without_stegcore_receipt")
    if p.get("contract_test_only") is True and (p.get("publication_authorized") or p.get("release_authorized")): fail("fixture_authority")
    out={"schema_version":"HIL-SITE-LIFECYCLE-PROJECTION-VALIDATION-v1","valid":True,"submission_id":p["submission_id"],"response_sha256":p["response_sha256"],"state":p["state"],"display_safe":True,"publication_authorized":bool(p.get("publication_authorized",False)),"release_authorized":bool(p.get("release_authorized",False)),"next_internal_action":"IMPORT_NEXT_VALIDATED_RECEIPT" if p["state"]!="ACTIVATED" else "NONE"}
    print(json.dumps(out,indent=2)); return 0

if __name__=="__main__":
    try: raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({"schema_version":"HIL-SITE-LIFECYCLE-PROJECTION-VALIDATION-v1","valid":False,"error":str(exc),"next_internal_action":"REPAIR_OR_REPLACE_PROJECTION_RECEIPT"},indent=2)); raise SystemExit(1)
