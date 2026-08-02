#!/usr/bin/env python3
from __future__ import annotations
import argparse, datetime as dt, hashlib, json
from pathlib import Path

REQUIRED_TOP={"schema","experiment_id","case_id","actor","policy","delegation","evidence","request","boundary"}
def canonical_bytes(v): return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
def sha256_bytes(b): return hashlib.sha256(b).hexdigest()
def parse_time(v):
    if not isinstance(v,str): raise ValueError("timestamp_missing")
    return dt.datetime.fromisoformat(v.replace("Z","+00:00"))
def extra(actual,declared): return sorted(set(actual)-set(declared))

def evaluate(case):
    missing=sorted(REQUIRED_TOP-set(case))
    if missing: return "FAIL_CLOSED",["REQUIRED_FIELD_MISSING:"+x for x in missing]
    try: commit=parse_time(case["request"]["commit_time"])
    except Exception: return "FAIL_CLOSED",["COMMIT_TIME_UNRESOLVED"]
    required=[("actor",["id","identity_binding"]),("policy",["proposal_version","commit_version","allowed"]),("delegation",["subject","identity_binding","valid_from","valid_until","actions","targets","scopes"]),("evidence",["observed_at","max_age_seconds","integrity"]),("request",["action","target","scope","commit_time"]),("boundary",["declared_network_sinks","actual_network_sinks","declared_credentials","actual_credentials","declared_filesystem_writes","actual_filesystem_writes","declared_external_side_effects","actual_external_side_effects"])]
    nm=[]
    for parent,fields in required:
        if not isinstance(case.get(parent),dict): nm.append(parent); continue
        nm += [f"{parent}.{f}" for f in fields if f not in case[parent]]
    if nm: return "FAIL_CLOSED",["REQUIRED_FIELD_MISSING:"+x for x in sorted(nm)]
    p=case["policy"]
    if p["proposal_version"]!=p["commit_version"] or p["allowed"] is not True: return "DENY",["POLICY_NOT_VALID_AT_COMMIT"]
    d=case["delegation"]; a=case["actor"]; r=case["request"]
    try:
        if not(parse_time(d["valid_from"])<=commit<=parse_time(d["valid_until"])): return "DENY",["DELEGATION_EXPIRED"]
    except Exception: return "FAIL_CLOSED",["DELEGATION_TIME_UNRESOLVED"]
    if d["subject"]!=a["id"] or d["identity_binding"]!=a["identity_binding"]: return "DENY",["IDENTITY_BINDING_CHANGED"]
    if r["action"] not in d["actions"] or r["target"] not in d["targets"] or r["scope"] not in d["scopes"]: return "DENY",["DELEGATION_SCOPE_MISMATCH"]
    e=case["evidence"]
    try:
        observed=parse_time(e["observed_at"]); age=(commit-observed).total_seconds()
        if age<0 or age>int(e["max_age_seconds"]) or e["integrity"]!="verified": return "FAIL_CLOSED",["EVIDENCE_FRESHNESS_UNRESOLVED"]
    except Exception: return "FAIL_CLOSED",["EVIDENCE_FRESHNESS_UNRESOLVED"]
    b=case["boundary"]
    if any([extra(b["actual_network_sinks"],b["declared_network_sinks"]),extra(b["actual_credentials"],b["declared_credentials"]),extra(b["actual_filesystem_writes"],b["declared_filesystem_writes"]),extra(b["actual_external_side_effects"],b["declared_external_side_effects"])]): return "DENY",["EXECUTION_BOUNDARY_EXCEEDED"]
    return "ALLOW",[]

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root",default=str(Path(__file__).resolve().parents[1])); ap.add_argument("--repeat",type=int,default=2); ap.add_argument("--write",action="store_true"); args=ap.parse_args()
    root=Path(args.root); manifest=json.loads((root/"manifest.json").read_text()); expected=json.loads((root/manifest["expected_outcomes"]).read_text())["outcomes"]
    source_hash=sha256_bytes(Path(__file__).read_bytes()); summary={"schema":"stegverse.governance.experiment.summary.v1","experiment_id":manifest["experiment_id"],"results":[]}; failures=0
    for cid in manifest["required_cases"]:
        path=root/"cases"/f"{cid}.json"; case=json.loads(path.read_text()); runs=[]
        for _ in range(args.repeat):
            decision,reasons=evaluate(case); post=sha256_bytes(canonical_bytes({"case_id":cid,"decision":decision,"reason_codes":reasons})); runs.append((decision,reasons,post))
        deterministic=all(x==runs[0] for x in runs); exp=expected[cid]; matches=runs[0][0]==exp["decision"] and runs[0][1]==exp["reason_codes"]
        receipt={"schema":"stegverse.governance.experiment.receipt.v1","experiment_id":manifest["experiment_id"],"case_id":cid,"run_id":cid+"-deterministic","canonicalization":{"spec":manifest["canonicalization"]},"input_hashes":{"case_sha256":sha256_bytes(path.read_bytes())},"verifier":{"name":"sv-ttu-mre-verifier","version":"1.0.0","source_sha256":source_hash},"decision":runs[0][0],"reason_codes":runs[0][1],"expected_decision":exp["decision"],"matches_expected":matches,"deterministic":deterministic,"authority_reconstructed":True,"runtime_assertion_trusted":False,"execution_boundary_checked":True,"post_state_sha256":runs[0][2]}
        if args.write: (root/"receipts").mkdir(exist_ok=True); (root/"receipts"/f"{cid}.receipt.json").write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
        summary["results"].append(receipt); failures += 0 if matches and deterministic else 1
    summary["status"]="PASS" if failures==0 else "FAIL"; summary["failures"]=failures
    if args.write: (root/"reports").mkdir(exist_ok=True); (root/"reports"/"summary.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n")
    print(json.dumps(summary,indent=2,sort_keys=True)); return 0 if failures==0 else 1
if __name__=="__main__": raise SystemExit(main())
