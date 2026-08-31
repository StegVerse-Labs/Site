#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
STATUS=ROOT/"data"/"sv002-experiment-status.json"
PAGE=ROOT/"sv002-status"/"index.html"

def fail(msg):
    raise SystemExit("SV002_EXPERIMENT_STATUS_FAIL: "+msg)

def main():
    if not STATUS.exists(): fail("missing status manifest")
    if not PAGE.exists(): fail("missing public status page")
    s=json.loads(STATUS.read_text(encoding="utf-8"))
    if s.get("schema")!="stegverse.sv002-experiment-public-status/v1": fail("schema")
    if s.get("experiment_id")!="STEGVERSE-002-SELF-CHARACTERIZATION-001": fail("experiment id")
    if s.get("authority_effect")!="NONE_STATUS_ONLY": fail("authority effect")
    comps={c["id"]:c for c in s.get("components",[])}
    required={"experiment-static-freeze","principal-runtime","s0-binding","heartbeat-presence","principal-execution","public-intr-profile","receiver-ready","public-round-trip","master-records","system-ai-lifecycle"}
    if not required.issubset(comps): fail("missing required component")
    if comps["experiment-static-freeze"].get("current")!="COMPLETE": fail("static freeze must remain complete")
    for cid in ("principal-runtime","s0-binding","principal-execution","public-intr-profile","receiver-ready","public-round-trip","master-records"):
        if comps[cid].get("observed") is True: fail(f"{cid} cannot be promoted without new canonical evidence")
    life=s.get("adjacent_lifecycle_goal",{})
    if life.get("system_ai_active") is not False: fail("SYSTEM_AI_ACTIVE cannot be true in current source-only state")
    if life.get("heartbeat_presence_proven") is not False: fail("heartbeat presence is not yet proven")
    page=PAGE.read_text(encoding="utf-8")
    for marker in ("implemented ≠ validated ≠ merged ≠ deployed ≠ activated ≠ observed ≠ reconstructed","Completing it does not self-promote StegVerse-002","../data/sv002-experiment-status.json","../sv002-observe/"):
        if marker not in page: fail("missing page marker: "+marker)
    print("SV002_EXPERIMENT_STATUS_PASS")
if __name__=="__main__":
    main()
