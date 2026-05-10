#!/usr/bin/env python3
from __future__ import annotations
import argparse, fnmatch, json, zipfile
from datetime import datetime, timezone
from pathlib import Path

def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z")
def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def safe(n):
    if not n or n.endswith("/"): return False
    p=Path(n); return not p.is_absolute() and ".." not in p.parts
def mapped(n):
    c=n.lstrip("/")
    return ".github/workflows/"+c[len("github/workflows/"):] if c.startswith("github/workflows/") else c
def rule_for(path, depmap):
    for r in depmap.get("patterns",[]):
        if fnmatch.fnmatch(path,r["pattern"]): return r
    d=depmap.get("default",{})
    return {"pattern":"(default)","class":d.get("class","unknown_file"),"risk":d.get("risk","unknown"),"requires":d.get("requires",["sandbox_review","human_review"])}
def scan(bundle, depmap):
    files=[]; req=set(); risks=set(); unknown=[]
    with zipfile.ZipFile(bundle,"r") as z:
        for n in sorted(z.namelist()):
            if not safe(n) or n=="README.md": continue
            rp=mapped(n); r=rule_for(rp,depmap)
            req.update(r.get("requires",[])); risks.add(r.get("risk","unknown"))
            if r.get("class")=="unknown_file": unknown.append(rp)
            files.append({"bundle_path":n,"repo_path":rp,"class":r.get("class"),"risk":r.get("risk"),"requires":r.get("requires",[]),"matched_pattern":r.get("pattern")})
    verdict="ALLOW"
    if unknown: verdict="SANDBOX_REQUIRED"
    if "privileged" in risks: verdict="PRIVILEGED_EXECUTOR_REQUIRED"
    return {"generated_at":now(),"schema":"stegverse.dependency_impact_report.v1","bundle":str(bundle),"verdict":verdict,"required_checks":sorted(req),"risks":sorted(risks),"unknown_files":unknown,"files":files}
def md(report,path):
    lines=["# Dependency Impact Report","",f"Generated: `{report['generated_at']}`",f"Bundle: `{report['bundle']}`",f"Verdict: `{report['verdict']}`","","## Required Checks",""]
    lines += [f"- `{x}`" for x in report["required_checks"]]
    lines += ["","## Files",""]
    lines += [f"- `{i['repo_path']}` — class `{i['class']}`, risk `{i['risk']}`" for i in report["files"]]
    Path(path).write_text("\n".join(lines)+"\n",encoding="utf-8")
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--bundle",required=True); ap.add_argument("--dependency-map",default="data/dependency-map-v1.json"); ap.add_argument("--out-dir",default="dependency_reports"); args=ap.parse_args()
    out=Path(args.out_dir); out.mkdir(parents=True,exist_ok=True)
    report=scan(Path(args.bundle),load(args.dependency_map))
    (out/"dependency-impact-report.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    md(report,out/"dependency-impact-report.md")
    print(json.dumps({"verdict":report["verdict"],"required_checks":report["required_checks"]},indent=2))
if __name__=="__main__": main()
