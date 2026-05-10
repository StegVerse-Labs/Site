#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, zipfile
from datetime import datetime, timezone
from pathlib import Path
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z")
def safe(n):
    if not n or n.endswith("/"): return False
    p=Path(n); return not p.is_absolute() and ".." not in p.parts
def review(bundle):
    with zipfile.ZipFile(bundle,"r") as z:
        names=sorted(z.namelist())
    safe_entries=[n for n in names if safe(n)]
    unsafe=[n for n in names if n not in safe_entries]
    has_manifest="bundle-manifest.json" in safe_entries
    workflow=[n for n in safe_entries if n.startswith("github/workflows/") or n.startswith(".github/workflows/")]
    root_reports=[n for n in safe_entries if n in {"page-contract-report.json","page-contract-report.md","transition-replay-report.json","transition-replay-report.md"}]
    verdict="ALLOW"; recommendation="ingest"
    if unsafe: verdict,recommendation="HUMAN_REVIEW_REQUIRED","reject_or_rebuild"
    elif workflow: verdict,recommendation="PRIVILEGED_EXECUTOR_REQUIRED","route_to_privileged_queue"
    elif len([n for n in safe_entries if n!="README.md"])>5 and not has_manifest: verdict,recommendation="SANDBOX_REQUIRED","regenerate_with_manifest"
    elif root_reports: verdict,recommendation="ALLOW_WITH_ARTIFACT_ROUTING","ingest_with_artifact_routing"
    return {"generated_at":now(),"schema":"stegverse.sandbox_bundle_review_report.v1","bundle":str(bundle),"verdict":verdict,"recommendation":recommendation,"has_manifest":has_manifest,"safe_entries":safe_entries,"unsafe_entries":unsafe,"workflow_like_entries":workflow,"root_report_artifacts":root_reports,"silent_repair_performed":False}
def write_md(r,p):
    lines=["# Sandbox Bundle Review Report","",f"Generated: `{r['generated_at']}`",f"Bundle: `{r['bundle']}`",f"Verdict: `{r['verdict']}`",f"Recommendation: `{r['recommendation']}`","","## Findings","",f"- `has_manifest`: `{str(r['has_manifest']).lower()}`",f"- `unsafe_entries`: `{len(r['unsafe_entries'])}`",f"- `workflow_like_entries`: `{len(r['workflow_like_entries'])}`",f"- `root_report_artifacts`: `{len(r['root_report_artifacts'])}`",f"- `silent_repair_performed`: `{str(r['silent_repair_performed']).lower()}`"]
    Path(p).write_text("\n".join(lines)+"\n",encoding="utf-8")
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--bundle",required=True); ap.add_argument("--out-dir",default="sandbox_reports"); args=ap.parse_args()
    out=Path(args.out_dir); out.mkdir(parents=True,exist_ok=True); r=review(Path(args.bundle))
    (out/"sandbox-review-report.json").write_text(json.dumps(r,indent=2),encoding="utf-8"); write_md(r,out/"sandbox-review-report.md")
    print(json.dumps({"verdict":r["verdict"],"recommendation":r["recommendation"]},indent=2))
if __name__=="__main__": main()
