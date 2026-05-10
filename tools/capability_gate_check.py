#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, zipfile
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class GateDecision:
    verdict: str
    route: str
    reason: str
    bundle_class: str
    mapped_paths: list[str]
    required_checks: list[str]

def safe_member(name: str) -> bool:
    if not name or name.endswith("/"): return False
    p=Path(name)
    return not p.is_absolute() and ".." not in p.parts

def mapped_path(name: str) -> str:
    clean=name.lstrip("/")
    if clean.startswith("github/workflows/"):
        return ".github/workflows/"+clean[len("github/workflows/"):]
    return clean

def inspect_bundle(bundle: Path) -> list[str]:
    with zipfile.ZipFile(bundle,"r") as z:
        return [n for n in sorted(z.namelist()) if safe_member(n)]

def decide(bundle: Path) -> GateDecision:
    paths=inspect_bundle(bundle)
    mapped=[mapped_path(p) for p in paths]
    if any(p.startswith(".github/workflows/") for p in mapped):
        return GateDecision("PRIVILEGED_EXECUTOR_REQUIRED","privileged_queue","Bundle contains workflow mutation paths. Ordinary ingestion cannot mutate workflow authority boundaries.","workflow_bundle",mapped,["privileged_executor_authority_receipt"])
    if any(("secret" in p.lower() or "token" in p.lower() or "credential" in p.lower() or ".env" in p.lower()) for p in mapped):
        return GateDecision("HUMAN_REVIEW_REQUIRED","failed_bundles","Bundle appears to contain authority, token, secret, env, or credential material.","authority_material_bundle",mapped,["human_review"])
    artifact_names={"page-contract-report.json","page-contract-report.md","transition-replay-report.json","transition-replay-report.md"}
    if any(Path(p).name in artifact_names for p in paths):
        return GateDecision("ALLOW","ingest","Known report artifact bundle may be routed into repo-readable evidence directories.","artifact_bundle",mapped,["selector_check"])
    if len([p for p in paths if p!="README.md"])>5 and "bundle-manifest.json" not in paths:
        return GateDecision("SANDBOX_REQUIRED","sandbox_queue","Complex bundle has more than five files and no bundle-manifest.json.","complex_unmanifested_bundle",mapped,["sandbox_review"])
    return GateDecision("ALLOW","ingest","Ordinary bundle class is allowed under current ingestion boundary threshold.","ordinary_bundle",mapped,["dependency_impact_scan","bundle_ingestion_receipt"])

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--bundle",required=True)
    ap.add_argument("--out")
    args=ap.parse_args()
    payload=asdict(decide(Path(args.bundle)))
    if args.out:
        Path(args.out).parent.mkdir(parents=True,exist_ok=True)
        Path(args.out).write_text(json.dumps(payload,indent=2),encoding="utf-8")
    else:
        print(json.dumps(payload,indent=2))
    return 0
if __name__=="__main__":
    raise SystemExit(main())
