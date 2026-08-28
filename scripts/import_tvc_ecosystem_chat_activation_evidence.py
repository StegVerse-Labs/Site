#!/usr/bin/env python3
"""Import a verified TVC Ecosystem Chat activation-evidence packet locally.

No network access, credentials, provider execution, publication, or activation
authority is used or granted. This is a Site-side evidence persistence seam.
"""
from __future__ import annotations

import argparse, hashlib, json
from pathlib import Path
from typing import Any

OUTPUT_REL = Path("data/ecosystem-chat-tvc-activation-evidence.json")

def canonical_hash(value: dict[str, Any], omit: str | None = None) -> str:
    body=dict(value)
    if omit:
        body.pop(omit,None)
    return hashlib.sha256(json.dumps(body,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()

def load(path: Path) -> dict[str, Any]:
    value=json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value,dict):
        raise ValueError("packet_not_object")
    return value

def verify(packet: dict[str, Any]) -> None:
    errors=[]
    if packet.get("schema")!="stegverse.tvc.ecosystem-chat-activation-evidence/v1": errors.append("schema")
    if packet.get("state")!="READY_FOR_SITE_IMPORT": errors.append("state")
    expected=packet.get("packet_sha256")
    if not isinstance(expected,str) or canonical_hash(packet,"packet_sha256")!=expected: errors.append("packet_hash")
    for key in ("same_execution","persistent_conversational_runtime_ready"):
        if packet.get(key) is not True: errors.append(key)
    if packet.get("credential_authority")!="TV/TVC": errors.append("credential_authority")
    if packet.get("credential_requirement")!="NONE": errors.append("credential_requirement")
    if packet.get("credential_material_present") is not False: errors.append("credential_material_present")
    if packet.get("github_token_required") is not False: errors.append("github_token_required")
    if packet.get("github_runtime_authority")!="NONE": errors.append("github_runtime_authority")
    for key in ("route_authority_granted","execution_authority_granted","custody_authority_granted","publication_authority_granted","site_mutation_authority_granted","site_mutation_performed","publication_performed","third_party_runtime_required"):
        if packet.get(key) is not False: errors.append(key)
    if packet.get("authority_effect")!="NONE_EVIDENCE_PERSISTENCE_ONLY": errors.append("authority_effect")
    if errors:
        raise ValueError("packet_rejected:"+",".join(sorted(set(errors))))

def import_packet(packet_path: Path, site_root: Path) -> dict[str, Any]:
    packet=load(packet_path)
    verify(packet)
    output=site_root.resolve()/OUTPUT_REL
    output.parent.mkdir(parents=True,exist_ok=True)
    record={
        "schema":"stegverse.site.ecosystem-chat-tvc-evidence-import/v1",
        "state":"IMPORTED_NON_AUTHORIZING_EVIDENCE",
        "source_packet_sha256":packet["packet_sha256"],
        "source_projection_sha256":packet.get("source_projection_sha256"),
        "source_task_id":packet.get("source_task_id"),
        "fencing_token":packet.get("fencing_token"),
        "same_execution":True,
        "persistent_conversational_runtime_ready":True,
        "credential_authority":"TV/TVC",
        "credential_material_present":False,
        "github_runtime_authority":"NONE",
        "activation_authority_granted":False,
        "publication_authority_granted":False,
        "authority_effect":"NONE_EVIDENCE_IMPORT_ONLY"
    }
    record["record_sha256"]=canonical_hash(record)
    if output.exists():
        existing=load(output)
        if existing!=record:
            raise ValueError("immutable_site_import_conflict")
        write_result="UNCHANGED"
    else:
        output.write_text(json.dumps(record,indent=2,sort_keys=True)+"\n",encoding="utf-8")
        write_result="CREATED"
    return {"state":record["state"],"write_result":write_result,"output":str(output),"record_sha256":record["record_sha256"]}

def main()->int:
    p=argparse.ArgumentParser()
    p.add_argument("--packet",type=Path,required=True)
    p.add_argument("--site-root",type=Path,default=Path(__file__).resolve().parents[1])
    a=p.parse_args()
    print(json.dumps(import_packet(a.packet.expanduser().resolve(),a.site_root.expanduser().resolve()),sort_keys=True))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
