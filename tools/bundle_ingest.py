#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, shutil, zipfile
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

@dataclass
class FileDecision:
    bundle_path: str
    repo_path: str | None
    action: str
    reason: str
    old_sha256: str | None
    new_sha256: str | None
    bytes: int

@dataclass
class PathMapping:
    bundle_path: str
    repo_path: str
    reason: str

def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z")
def sha_b(b:bytes)->str: return hashlib.sha256(b).hexdigest()
def sha_f(p:Path)->str|None: return sha_b(p.read_bytes()) if p.exists() and p.is_file() else None
def load(p:Path, default:Any=None)->Any:
    if not p.exists(): return default
    try: return json.loads(p.read_text(encoding="utf-8"))
    except Exception: return default
def append_jsonl(p:Path,obj:dict[str,Any])->None:
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open("a",encoding="utf-8") as f: f.write(json.dumps(obj,sort_keys=True)+"\n")
def tree_fp(root:Path)->str:
    skip=(".git/","ingestion_reports/","dependency_reports/","sandbox_reports/","__pycache__/")
    rows=[]
    for p in sorted(root.rglob("*")):
        if not p.is_file(): continue
        rel=p.relative_to(root).as_posix()
        if rel.startswith(skip): continue
        rows.append(f"{sha_f(p)}  {rel}")
    return sha_b("\n".join(rows).encode())
def changed_fp(decisions:list[FileDecision])->str:
    rows=[f"{d.action} {d.repo_path} {d.old_sha256}->{d.new_sha256}" for d in decisions if d.action in {"created","updated","would_created","would_updated"}]
    return sha_b("\n".join(sorted(rows)).encode())
def safe(n:str)->bool:
    if not n or n.endswith("/"): return False
    p=Path(n); return not p.is_absolute() and ".." not in p.parts
def artifact_mapping(name:str, policy:dict[str,Any])->PathMapping|None:
    clean=name.lstrip("/")
    for item in policy.get("artifact_file_mappings",[]):
        if clean==item.get("bundle_path"):
            return PathMapping(clean,str(item["repo_path"]),str(item.get("reason","known artifact report routed")))
    return None
def normalize(name:str, policy:dict[str,Any])->tuple[str,PathMapping|None]:
    clean=name.lstrip("/")
    art=artifact_mapping(clean,policy)
    if art: return art.repo_path, art
    if clean.startswith("github/workflows/"):
        mapped=".github/workflows/"+clean[len("github/workflows/"):]
        return mapped, PathMapping(clean,mapped,"mapped dotless upload-safe workflow path to GitHub Actions workflow path")
    return clean, None
def protected(path:str, prefixes:list[str])->bool:
    return any(path==p.rstrip("/") or path.startswith(p) for p in prefixes)
def inspect(bundle:Path)->list[str]:
    with zipfile.ZipFile(bundle,"r") as z:
        return [n for n in sorted(z.namelist()) if safe(n)]
def classify(bundle:Path)->dict[str,Any]:
    paths=inspect(bundle)
    mapped=[(".github/workflows/"+p[len("github/workflows/"):]) if p.startswith("github/workflows/") else p for p in paths]
    if any(p.startswith(".github/workflows/") for p in mapped):
        return {"verdict":"PRIVILEGED_EXECUTOR_REQUIRED","route":"privileged_queue","bundle_class":"workflow_bundle","reason":"workflow mutation requires privileged executor","mapped_paths":mapped}
    if any(("secret" in p.lower() or "token" in p.lower() or "credential" in p.lower() or ".env" in p.lower()) for p in mapped):
        return {"verdict":"HUMAN_REVIEW_REQUIRED","route":"failed_bundles","bundle_class":"authority_material_bundle","reason":"possible secret/authority material","mapped_paths":mapped}
    artifact_names={"page-contract-report.json","page-contract-report.md","transition-replay-report.json","transition-replay-report.md"}
    if any(Path(p).name in artifact_names for p in paths):
        return {"verdict":"ALLOW","route":"ingest","bundle_class":"artifact_bundle","reason":"known report artifact bundle","mapped_paths":mapped}
    if len([p for p in paths if p!="README.md"])>5 and "bundle-manifest.json" not in paths:
        return {"verdict":"SANDBOX_REQUIRED","route":"sandbox_queue","bundle_class":"complex_unmanifested_bundle","reason":"complex bundle lacks manifest","mapped_paths":mapped}
    return {"verdict":"ALLOW","route":"ingest","bundle_class":"ordinary_bundle","reason":"ordinary bundle allowed","mapped_paths":mapped}
def copy_receipt(root:Path,bundle:Path,route_dir:str,receipt:dict[str,Any],suffix:str):
    d=root/route_dir; d.mkdir(parents=True,exist_ok=True)
    tgt=d/bundle.name
    if bundle.resolve()!=tgt.resolve(): shutil.copy2(bundle,tgt)
    base=d/f"{bundle.stem}.{suffix}"
    base.with_suffix(".json").write_text(json.dumps(receipt,indent=2),encoding="utf-8")
    base.with_suffix(".md").write_text(f"# Bundle {suffix}\n\nBundle: `{bundle.name}`\nVerdict: `{receipt.get('verdict')}`\nRoute: `{receipt.get('route')}`\nReason: {receipt.get('reason')}\nBundle SHA-256: `{receipt.get('bundle_sha256')}`\n",encoding="utf-8")
def seen(root:Path,bsha:str,policy:dict[str,Any],retry:bool)->bool:
    idx=load(root/policy.get("ledger_outputs",{}).get("fingerprint_index","data/bundle-fingerprint-index-v1.json"),{"receipts":[]}) or {"receipts":[]}
    for x in idx.get("receipts",[]):
        if x.get("bundle_sha256")==bsha and x.get("verdict")=="ALLOW": return True
    if retry: return False
    for folder in [policy.get("queue",{}).get("failed_dir","failed_bundles"),policy.get("queue",{}).get("privileged_dir","privileged_queue"),policy.get("queue",{}).get("sandbox_dir","sandbox_queue")]:
        for rp in (root/folder).glob("*.json"):
            if (load(rp,{}) or {}).get("bundle_sha256")==bsha: return True
    return False
def ingest_one(root:Path,bundle:Path,policy_path:Path,apply:bool,retry:bool=False)->dict[str,Any]:
    policy=load(policy_path,{})
    bsha=sha_f(bundle) or ""
    gate=classify(bundle)
    base={"generated_at":now(),"schema":"stegverse.bundle_ingestion_receipt.v1","formal_milestone":"MS-012E — Strict Ingestion Threshold Gates","bundle_name":bundle.name,"bundle_path":str(bundle),"bundle_sha256":bsha,"mode":"apply" if apply else "dry_run","bundle_class":gate["bundle_class"],"verdict":gate["verdict"],"route":gate["route"],"reason":gate["reason"],"mapped_paths":gate["mapped_paths"]}
    if seen(root,bsha,policy,retry):
        rec={**base,"verdict":"SKIPPED_ALREADY_SEEN","route":"skipped","decisions":[]}
        return {"generated_at":rec["generated_at"],"schema":"stegverse.bundle_ingestion_report.v1","bundle":str(bundle),"mode":rec["mode"],"receipt":rec,"summary":{"applied":0,"skipped":1}}
    if gate["verdict"]=="PRIVILEGED_EXECUTOR_REQUIRED":
        rec={**base,"decisions":[]}
        if apply: copy_receipt(root,bundle,policy.get("queue",{}).get("privileged_dir","privileged_queue"),rec,"privileged-task")
        return {"generated_at":rec["generated_at"],"schema":"stegverse.bundle_ingestion_report.v1","bundle":str(bundle),"mode":rec["mode"],"receipt":rec,"summary":{"applied":0,"routed_privileged":1}}
    if gate["verdict"] in {"SANDBOX_REQUIRED","HUMAN_REVIEW_REQUIRED","FAIL_CLOSED"}:
        rec={**base,"decisions":[]}
        route=policy.get("queue",{}).get("sandbox_dir","sandbox_queue") if gate["verdict"]=="SANDBOX_REQUIRED" else policy.get("queue",{}).get("failed_dir","failed_bundles")
        if apply: copy_receipt(root,bundle,route,rec,"failure")
        return {"generated_at":rec["generated_at"],"schema":"stegverse.bundle_ingestion_report.v1","bundle":str(bundle),"mode":rec["mode"],"receipt":rec,"summary":{"applied":0,"routed":route}}
    before=tree_fp(root); decisions=[]; maps=[]; unsafe=0
    with zipfile.ZipFile(bundle,"r") as z:
        for name in sorted(z.namelist()):
            if not safe(name):
                unsafe+=1; decisions.append(FileDecision(name,None,"skipped","unsafe path or directory entry",None,None,0)); continue
            data=z.read(name); new=sha_b(data)
            if name=="README.md":
                decisions.append(FileDecision(name,None,"skipped","bundle root README is documentation and is not applied to repo root",None,new,len(data))); continue
            repo_rel,m=normalize(name,policy)
            if m: maps.append(m)
            old=sha_f(root/repo_rel)
            if protected(repo_rel,list(policy.get("protected_paths",[]))):
                decisions.append(FileDecision(name,repo_rel,"skipped","protected path",old,new,len(data))); continue
            if old==new:
                decisions.append(FileDecision(name,repo_rel,"unchanged","target hash already matches",old,new,len(data))); continue
            action="updated" if (root/repo_rel).exists() else "created"
            if apply:
                target=root/repo_rel; target.parent.mkdir(parents=True,exist_ok=True); target.write_bytes(data)
                decisions.append(FileDecision(name,repo_rel,action,"hash differs or target missing",old,new,len(data)))
            else:
                decisions.append(FileDecision(name,repo_rel,"would_"+action,"dry run; hash differs or target missing",old,new,len(data)))
    after=tree_fp(root); cfp=changed_fp(decisions)
    rec={**base,"verdict":"ALLOW","route":"ingest","files_seen":len(decisions),"files_created":len([d for d in decisions if d.action=="created"]),"files_updated":len([d for d in decisions if d.action=="updated"]),"files_unchanged":len([d for d in decisions if d.action=="unchanged"]),"files_skipped":len([d for d in decisions if d.action=="skipped"]),"unsafe_paths_rejected":unsafe,"path_mappings_applied":[asdict(m) for m in maps],"repo_transition":{"before_tree_fingerprint":before,"after_tree_fingerprint":after,"changed_files_fingerprint":cfp},"decisions":[asdict(d) for d in decisions]}
    if apply:
        outs=policy.get("ledger_outputs",{})
        latest=root/outs.get("latest_receipt","data/latest-bundle-ingestion-receipt-v1.json"); ledger=root/outs.get("ledger_jsonl","data/bundle-ingestion-ledger-v1.jsonl"); indexp=root/outs.get("fingerprint_index","data/bundle-fingerprint-index-v1.json")
        latest.parent.mkdir(parents=True,exist_ok=True); latest.write_text(json.dumps(rec,indent=2),encoding="utf-8")
        append_jsonl(ledger,{"generated_at":rec["generated_at"],"formal_milestone":rec["formal_milestone"],"bundle_name":rec["bundle_name"],"bundle_sha256":rec["bundle_sha256"],"bundle_class":rec["bundle_class"],"verdict":rec["verdict"],"changed_files_fingerprint":cfp})
        idx=load(indexp,{"schema":"stegverse.bundle_fingerprint_index.v1","receipts":[]}) or {"receipts":[]}
        idx.setdefault("receipts",[]).append({"generated_at":rec["generated_at"],"formal_milestone":rec["formal_milestone"],"bundle_name":rec["bundle_name"],"bundle_sha256":rec["bundle_sha256"],"bundle_class":rec["bundle_class"],"verdict":rec["verdict"],"changed_files_fingerprint":cfp})
        indexp.write_text(json.dumps(idx,indent=2),encoding="utf-8")
    return {"generated_at":rec["generated_at"],"schema":"stegverse.bundle_ingestion_report.v1","bundle":str(bundle),"policy":str(policy_path),"mode":rec["mode"],"receipt":rec,"summary":{"total_entries_seen":len(decisions),"applied":len([d for d in decisions if d.action in {'created','updated'}]),"unchanged":len([d for d in decisions if d.action=='unchanged']),"skipped":len([d for d in decisions if d.action=='skipped']),"path_mappings":len(maps),"unsafe_paths_rejected":unsafe}}
def write_report(report:dict[str,Any],out:Path):
    out.mkdir(parents=True,exist_ok=True)
    (out/"bundle-ingestion-report.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    (out/"latest-bundle-ingestion-receipt-v1.json").write_text(json.dumps(report["receipt"],indent=2),encoding="utf-8")
    r=report["receipt"]
    lines=["# Bundle Ingestion Report","",f"Generated: `{report['generated_at']}`",f"Mode: `{report['mode']}`",f"Bundle: `{report['bundle']}`",f"Verdict: `{r['verdict']}`",f"Route: `{r.get('route')}`",f"Bundle class: `{r.get('bundle_class')}`","","## Summary",""]
    for k,v in report.get("summary",{}).items(): lines.append(f"- `{k}`: `{v}`")
    if "decisions" in r:
        lines+=["","## File Decisions",""]
        for row in r.get("decisions",[]): lines.append(f"- `{row.get('action')}` `{row.get('bundle_path')}` → `{row.get('repo_path')}` — {row.get('reason')}")
    (out/"bundle-ingestion-report.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
def process_queue(root:Path,policy_path:Path,apply:bool,retry:bool)->dict[str,Any]:
    policy=load(policy_path,{})
    incoming=root/policy.get("queue",{}).get("incoming_dir","incoming")
    reports=[]
    for b in sorted(incoming.glob("*.zip"), key=lambda p:p.name):
        try: reports.append(ingest_one(root,b,policy_path,apply,retry))
        except Exception as e:
            rec={"generated_at":now(),"schema":"stegverse.bundle_ingestion_receipt.v1","formal_milestone":"MS-012E — Strict Ingestion Threshold Gates","bundle_name":b.name,"bundle_path":str(b),"bundle_sha256":sha_f(b),"verdict":"FAIL_CLOSED","route":"failed_bundles","reason":f"Unhandled ingestion exception: {e}","decisions":[]}
            if apply: copy_receipt(root,b,policy.get("queue",{}).get("failed_dir","failed_bundles"),rec,"failure")
            reports.append({"generated_at":rec["generated_at"],"schema":"stegverse.bundle_ingestion_report.v1","bundle":str(b),"mode":"apply" if apply else "dry_run","receipt":rec,"summary":{"failed":1}})
    return {"generated_at":now(),"schema":"stegverse.bundle_queue_report.v1","bundles_seen":len(reports),"reports":reports}
def write_queue(report:dict[str,Any],out:Path):
    out.mkdir(parents=True,exist_ok=True)
    (out/"bundle-queue-report.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    lines=["# Bundle Queue Report","",f"Generated: `{report['generated_at']}`",f"Bundles seen: `{report['bundles_seen']}`","","## Results",""]
    for item in report["reports"]:
        r=item["receipt"]; lines.append(f"- `{r.get('bundle_name')}` → `{r.get('verdict')}` / `{r.get('route')}` — {r.get('reason')}")
    (out/"bundle-queue-report.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
def find_bundle(root:Path, explicit:str|None)->Path:
    if explicit:
        p=root/explicit
        if not p.exists(): raise SystemExit(f"Bundle not found: {p}")
        return p
    bundles=sorted((root/"incoming").glob("*.zip"), key=lambda p:p.stat().st_mtime, reverse=True)
    if not bundles: raise SystemExit("No bundle found. Commit a .zip file under incoming/ or pass --bundle.")
    return bundles[0]
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--repo-root",default="."); ap.add_argument("--bundle"); ap.add_argument("--policy",default="data/bundle-ingestion-policy-v1.json"); ap.add_argument("--out-dir",default="ingestion_reports"); ap.add_argument("--apply",action="store_true"); ap.add_argument("--process-queue",action="store_true"); ap.add_argument("--retry-failed",action="store_true"); args=ap.parse_args()
    root=Path(args.repo_root).resolve(); policy_path=root/args.policy; out=root/args.out_dir
    if args.process_queue:
        qr=process_queue(root,policy_path,args.apply,args.retry_failed); write_queue(qr,out)
        if qr["reports"]: write_report(qr["reports"][-1],out)
        print(json.dumps({"bundles_seen":qr["bundles_seen"]},indent=2)); return
    report=ingest_one(root,find_bundle(root,args.bundle),policy_path,args.apply,args.retry_failed); write_report(report,out); print(json.dumps(report.get("summary",{}),indent=2))
if __name__=="__main__": main()
