#!/usr/bin/env python3
"""Generate a fail-closed HIL pilot comparison skeleton from verified ledger entries."""
from __future__ import annotations
import argparse, json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RUBRIC = [
  {"criterion_id":"thesis_engagement","description":"Direct engagement with the HIL thesis and its falsifiable boundaries.","scale":["absent","partial","substantive"]},
  {"criterion_id":"evidence_discipline","description":"Separation of observed evidence, inference, and unsupported claims.","scale":["weak","mixed","strong"]},
  {"criterion_id":"counterexample_quality","description":"Quality of counterexamples, limitations, and alternative explanations.","scale":["absent","limited","substantive"]},
  {"criterion_id":"governance_distinctions","description":"Preservation of receipt, custody, review, publication, and endorsement boundaries.","scale":["collapsed","partial","preserved"]}
]

def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("--ledger",type=Path,default=ROOT/"data/hil-pilot-ledger.json"); ap.add_argument("--output",type=Path,required=True); args=ap.parse_args()
    ledger=json.loads(args.ledger.read_text())
    verified=[e for e in ledger["entries"] if e["verification_status"] in {"RETURN_PACKAGE_VERIFIED","MANAGED_RECEIVING_ACKNOWLEDGED","GOVERNED_RECEIVER_RECEIPT_VERIFIED"}]
    if len(verified)<2: raise SystemExit("comparison not generated: at least two verified response packages are required")
    now=datetime.now(timezone.utc).isoformat().replace("+00:00","Z")
    out={"schema_version":"HIL-PILOT-COMPARISON-v1","comparison_id":"HIL-COMP-"+now[:10].replace("-","")+"-001","generated_at":now,"canonical_primary":ledger["canonical_primary"],"canonical_prompt":ledger["canonical_prompt"],"rubric":RUBRIC,"responses":[{"submission_id":e["submission_id"],"model":e["model"],"provider":e["provider"],"response_sha256":e["response_pdf_sha256"],"verification_status":"RETURN_PACKAGE_VERIFIED"} for e in verified],"comparisons":[{"criterion_id":r["criterion_id"],"observations":[],"agreement":[],"disagreement":[],"uncertainty":["Human or governed review not yet recorded"]} for r in RUBRIC],"limitations":["Generator verifies eligibility and structure only; it does not infer response content.","Empty observations do not imply agreement or equivalence."],"claims_withheld":["scientific_validation","model_equivalence","publication_acceptance","endorsement"],"authority_effect":False,"publication_effect":False}
    args.output.write_text(json.dumps(out,indent=2)+"\n"); print(args.output); return 0
if __name__=="__main__": raise SystemExit(main())
