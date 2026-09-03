#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from typing import Any

TARGET_TASK="TASK-2026-0008"
TARGET_SURFACE="site:stegos-de006-bound-inference-publication"

def canonical(value:Any)->bytes:
    return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")

def sha(value:Any)->str:
    return hashlib.sha256(canonical(value)).hexdigest()

def require(condition:bool,message:str)->None:
    if not condition: raise RuntimeError(message)

def replay(rows:list[dict[str,Any]])->dict[str,Any]:
    previous=None
    for index,row in enumerate(rows,1):
        require(row.get("schema")=="stegos.web_bootstrap_journal_entry.v1","journal schema mismatch")
        require(row.get("sequence")==index,"journal sequence mismatch")
        require(row.get("previous_entry_sha256")==previous,"journal previous hash mismatch")
        require(row.get("receipt_sha256")==sha(row.get("receipt")),"journal receipt hash mismatch")
        body={k:v for k,v in row.items() if k!="entry_sha256"}
        require(row.get("entry_sha256")==sha(body),"journal entry hash mismatch")
        previous=row["entry_sha256"]
    return {"state":"PASS","entries":len(rows),"tail_sha256":previous}

def verify(path:Path)->dict[str,Any]:
    evidence=json.loads(path.read_text(encoding="utf-8"))
    require(evidence.get("schema")=="stegverse.device-org-allocator-execution-evidence/v1","evidence schema mismatch")
    require(evidence.get("state")=="CANONICAL_ALLOCATION_EXECUTED","evidence state mismatch")
    require(evidence.get("same_device") is True,"same-device proof missing")
    require(evidence.get("requires_other_machine") is False,"other-machine dependency present")
    require(evidence.get("credential_authority")=="TV/TVC","credential authority mismatch")
    require(evidence.get("authority_effect")=="NONE_EVIDENCE_ONLY","evidence authority widening")

    node=evidence.get("node") or {}
    device=evidence.get("device_continuity") or {}
    rows=evidence.get("continued_receipts")
    require(isinstance(rows,list) and rows,"continued node receipts missing")
    require(node.get("schema")=="stegos.web_node.v1","node schema mismatch")
    require(device.get("schema")=="stegos.web_device_continuity_root.v1","device continuity schema mismatch")
    require(evidence.get("node_id")==node.get("node_id"),"node identity mismatch")
    require(evidence.get("device_continuity_id")==device.get("device_continuity_id"),"device continuity identity mismatch")
    require(any((r.get("receipt") or {}).get("schema")=="stegos.web_device_node_binding_receipt.v1"
                and (r.get("receipt") or {}).get("node_id")==node.get("node_id")
                and (r.get("receipt") or {}).get("device_continuity_id")==device.get("device_continuity_id")
                for r in rows),"node/device binding receipt missing")

    report=replay(rows)
    projected=evidence.get("node_journal_replay") or {}
    require(projected.get("state")=="PASS","projected journal replay not PASS")
    require(projected.get("entries")==report["entries"],"journal entry count mismatch")
    require(projected.get("tail_sha256")==report["tail_sha256"],"journal tail mismatch")

    entry=evidence.get("node_journal_entry") or {}
    require(entry==rows[-1],"allocator node journal entry is not chain tail")
    execution_receipt=entry.get("receipt") or {}
    require(execution_receipt.get("schema")=="stegos.org_allocator_same_device_execution_receipt/v1","allocator execution receipt schema mismatch")
    require(execution_receipt.get("node_id")==node.get("node_id"),"allocator execution node mismatch")
    require(execution_receipt.get("device_continuity_id")==device.get("device_continuity_id"),"allocator execution device mismatch")
    require(execution_receipt.get("allocator_remains_claim_authority") is True,"allocator authority missing")
    require(execution_receipt.get("site_grants_claim_authority") is False,"Site claim authority widening")
    require(execution_receipt.get("heartbeat_grants_claim_authority") is False,"HB claim authority widening")
    require(execution_receipt.get("browser_shell_grants_claim_authority") is False,"browser claim authority widening")
    require(execution_receipt.get("requires_other_machine") is False,"execution receipt other-machine dependency")

    receipt=evidence.get("allocator_receipt") or {}
    require(receipt==execution_receipt.get("canonical_allocator_receipt"),"allocator receipt projection mismatch")
    require(receipt.get("schema")=="stegverse.org-allocator-portable-receipt/v1","allocator receipt schema mismatch")
    claimed_hash=receipt.get("receipt_sha256")
    require(isinstance(claimed_hash,str) and claimed_hash.startswith("sha256:"),"allocator receipt self-hash missing")
    require(claimed_hash=="sha256:"+sha({k:v for k,v in receipt.items() if k!="receipt_sha256"}),"allocator receipt self-hash mismatch")
    require(receipt.get("canonical_authority_owner")=="StegVerse-Labs/.github organization allocator","canonical allocator owner mismatch")
    require(receipt.get("execution_surface")=="CURRENT_USER_IPHONE","allocator execution surface mismatch")
    require(receipt.get("credential_authority")=="TV/TVC","allocator credential authority mismatch")
    require(receipt.get("heartbeat_grants_claim_authority") is False,"allocator HB authority widening")
    require(receipt.get("request_grants_claim_authority") is False,"allocator request authority widening")
    require(receipt.get("stegos_grants_claim_authority") is False,"allocator StegOS authority widening")
    require(receipt.get("github_token_runtime_authority")=="NONE","GitHub runtime authority present")
    require(receipt.get("requires_other_machine") is False,"allocator requires other machine")

    obs=evidence.get("claim_observation")
    selected=receipt.get("selected")
    target=False
    fences=[]
    if selected:
        require(isinstance(obs,dict),"selected task lacks claim observation")
        require(obs==execution_receipt.get("claim_observation"),"claim observation projection mismatch")
        require(obs.get("schema")=="stegverse.org-claim-grant-observation/v1","claim observation schema mismatch")
        require(obs.get("state")=="CLAIM_GRANT_OBSERVED","claim observation state mismatch")
        require(obs.get("task_id")==selected,"claim observation task mismatch")
        require(obs.get("allocator_remains_claim_authority") is True,"claim observation allocator authority mismatch")
        require(obs.get("observation_grants_claim_authority") is False,"observation authority widening")
        require(obs.get("heartbeat_grants_claim_authority") is False,"observation HB authority widening")
        snapshot={"task_id":obs.get("task_id"),"claim_registry_generation":obs.get("claim_registry_generation"),"claims":obs.get("claims")}
        require(obs.get("claim_snapshot_sha256")==sha(snapshot),"claim snapshot hash mismatch")
        fences=obs.get("fencing_tokens") or []
        for claim in obs.get("claims") or []:
            require(claim.get("task_id")==selected,"granted claim task mismatch")
            fence=(claim.get("lease") or {}).get("fencing_token")
            require(isinstance(fence,int) and fence>0,"claim fencing token invalid")
        if selected==TARGET_TASK:
            require(TARGET_SURFACE in (obs.get("dependency_surfaces") or []),"TASK-0008 dependency surface missing")
            require(evidence.get("task_0008_granted") is True,"TASK-0008 grant flag mismatch")
            target=True
        else:
            require(evidence.get("task_0008_granted") is False,"non-target allocation claims TASK-0008")
    else:
        require(obs is None,"no-selection allocation unexpectedly contains claim observation")

    require(evidence.get("selected_task_id")==selected,"selected task projection mismatch")
    require(evidence.get("claim_registry_generation")==receipt.get("claim_registry_generation"),"claim generation projection mismatch")
    return {
      "schema":"stegverse.device-org-allocator-evidence-verification/v1",
      "state":"PASS",
      "selected_task_id":selected,
      "claim_registry_generation":receipt.get("claim_registry_generation"),
      "fencing_tokens":fences,
      "task_0008_grant_verified":target,
      "node_id":node.get("node_id"),
      "device_continuity_id":device.get("device_continuity_id"),
      "journal_entries":report["entries"],
      "journal_tail_sha256":report["tail_sha256"],
      "canonical_allocator_authority_verified":True,
      "same_device_verified":True,
      "authority_effect":"NONE_VERIFICATION_ONLY",
    }

def main()->int:
    parser=argparse.ArgumentParser()
    parser.add_argument("evidence",type=Path)
    args=parser.parse_args()
    print(json.dumps(verify(args.evidence),sort_keys=True))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
