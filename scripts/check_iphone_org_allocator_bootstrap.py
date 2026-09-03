#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EXPECTED={
 "stegos-node/org-allocator-portable.js":"4df48314fa6cebf96d39cb1366a275468f5a3cbc",
 "stegos-node/org-allocator-current-iphone-package.json":"e97411f7c70a9724f6d62f10899fef6ceafaeaae",
}

def git_blob_sha(path:Path)->str:
    data=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()

def verify()->dict:
    for rel,expected in EXPECTED.items():
        path=ROOT/rel
        if not path.is_file():
            raise RuntimeError(f"missing {rel}")
        actual=git_blob_sha(path)
        if actual!=expected:
            raise RuntimeError(f"{rel} blob mismatch: {actual} != {expected}")
    html=(ROOT/"stegos-node/org-allocator-bootstrap.html").read_text(encoding="utf-8")
    required=[
      'ALLOC_DB="stegos-org-allocator-v1"',
      'StegVersePortableOrgClaimAllocator.allocate',
      'atomicCompareAndSwap',
      'site_grants_claim_authority:false',
      'heartbeat_grants_claim_authority:false',
      'browser_shell_grants_claim_authority:false',
      'task_0008_granted',
      'continued_receipts:continuity.rows.slice()',
      'node:continuity.node',
      'device_continuity:continuity.device',
      'CURRENT_USER_IPHONE',
      'requires_other_machine:false',
      'credential_authority:"TV/TVC"',
      'github_token_runtime_authority:"NONE"',
    ]
    for marker in required:
        if marker not in html:
            raise RuntimeError(f"bootstrap invariant missing: {marker}")
    if "stegos-bootstrap/" in html:
        raise RuntimeError("bootstrap runner may not reference TASK-0008 gated product paths")
    pkg=json.loads((ROOT/"stegos-node/org-allocator-current-iphone-package.json").read_text(encoding="utf-8"))
    if pkg.get("canonical_authority_owner")!="StegVerse-Labs/.github organization allocator":
        raise RuntimeError("canonical allocator owner drift")
    if pkg.get("execution_surface")!="CURRENT_USER_IPHONE":
        raise RuntimeError("execution surface drift")
    if pkg.get("stegos_grants_claim_authority") is not False:
        raise RuntimeError("StegOS claim authority widening")
    return {
      "schema":"stegverse.site.iphone-org-allocator-bootstrap-validation/v1",
      "state":"PASS",
      "exact_allocator_blob":EXPECTED["stegos-node/org-allocator-portable.js"],
      "exact_package_blob":EXPECTED["stegos-node/org-allocator-current-iphone-package.json"],
      "site_product_authority":False,
      "canonical_allocator_remains_claim_authority":True,
      "task_0008_claim_observed":False,
      "physical_iphone_execution_observed":False,
      "authority_effect":"NONE_VALIDATION_ONLY",
    }

if __name__=="__main__":
    print(json.dumps(verify(),sort_keys=True))
