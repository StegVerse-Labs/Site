#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
STATUS=ROOT/"data"/"sv002-experiment-status.json"
PAGE=ROOT/"sv002-status"/"index.html"
PUBLIC_CONFIG=ROOT/"data"/"stegverse-002-experiment.json"
PUBLIC_PAGE=ROOT/"stegverse-002-experiment.html"

def fail(msg):
    raise SystemExit("SV002_EXPERIMENT_STATUS_FAIL: "+msg)

def main():
    if not STATUS.exists(): fail("missing status manifest")
    if not PAGE.exists(): fail("missing public status page")
    if not PUBLIC_CONFIG.exists() or not PUBLIC_PAGE.exists(): fail("missing public experiment surface")
    s=json.loads(STATUS.read_text(encoding="utf-8"))
    if s.get("schema")!="stegverse.sv002-experiment-public-status/v1": fail("schema")
    if s.get("experiment_id")!="STEGVERSE-002-SELF-CHARACTERIZATION-001": fail("experiment id")
    if s.get("authority_effect")!="NONE_STATUS_ONLY": fail("status authority effect")
    if "EXPERIMENT_CONTRACT.v0.3.json" not in json.dumps(s): fail("canonical v0.3 contract not projected")
    if "EXPERIMENT_CONTRACT.v0.2.json" in json.dumps(s.get("principal_transition_semantics",{})): fail("stale v0.2 principal contract")
    if s.get("experiment_state")!="PRE_EXECUTION_RUNTIME_IDENTITY_PENDING": fail("v0.3 pre-execution state")
    t=s.get("principal_transition_semantics",{})
    if not str(t.get("canonical_contract") or "").endswith("EXPERIMENT_CONTRACT.v0.3.json"): fail("canonical contract must be v0.3")
    if t.get("authority_transfer_assumed") is not False: fail("authority transfer assumption")
    if t.get("authority_effect_resolution")!="DERIVED_FROM_APPLICABLE_TRANSITION_ELEMENTS": fail("transition effect resolution")
    if t.get("capability_realization_is_transition_evidence") is not True: fail("capability realization semantics")
    if t.get("capability_realization_observed") is not False: fail("capability realization cannot be preclaimed")
    if t.get("transition_effect_state")!="NOT_YET_EVALUATED": fail("transition effect state")
    comps={c["id"]:c for c in s.get("components",[])}
    required={"experiment-static-freeze","principal-runtime","s0-binding","heartbeat-presence","principal-execution","public-intr-profile","receiver-ready","public-round-trip","master-records","system-ai-lifecycle"}
    if not required.issubset(comps): fail("missing required component")
    if comps["experiment-static-freeze"].get("current")!="COMPLETE": fail("static freeze must remain complete")
    for cid in ("principal-runtime","s0-binding","principal-execution","public-intr-profile","receiver-ready","public-round-trip","master-records"):
        if comps[cid].get("observed") is True: fail(f"{cid} cannot be promoted without new canonical evidence")
    life=s.get("adjacent_lifecycle_goal",{})
    if life.get("system_ai_active") is not False: fail("SYSTEM_AI_ACTIVE cannot be true in current source-only state")
    if life.get("heartbeat_presence_proven") is not False: fail("heartbeat presence is not yet proven")
    cfg=json.loads(PUBLIC_CONFIG.read_text(encoding="utf-8"))
    if cfg.get("experiment_id")!=s.get("experiment_id"): fail("public observer experiment id mismatch")
    public_page=PUBLIC_PAGE.read_text(encoding="utf-8")
    if "frozen three-organization communication set declared at S0" in public_page: fail("stale S0 communication claim")
    if "viewer-correlation node, not a registered StegVerse communication Node" not in public_page: fail("viewer identity distinction missing")
    observer_config=json.loads((ROOT/"data"/"stegverse-002-experiment.json").read_text(encoding="utf-8"))
    if observer_config.get("experiment_id")!="STEGVERSE-002-SELF-CHARACTERIZATION-001": fail("observer experiment identity drift")
    public_page=(ROOT/"stegverse-002-experiment.html").read_text(encoding="utf-8")
    if "registered StegVerse communication Node" not in public_page: fail("viewer vs communication node boundary missing")
    for required_marker in (
        "Experiment condition: v0.3 FROZEN",
        "Implementation: v0.9 PRE-T0",
        "Expanded v0.5 protocol: NON-OPERATIVE FOR THIS RUN",
        "Open live observation window",
        "Open reconstruction view",
        "principal wall-clock bound: <strong>none in v0.3 launcher</strong>",
        "M0–M13 construction history",
        "Stage 1–31 formalism track is separate StegVerse-001 / Beta_Orionis work",
    ):
        if required_marker not in public_page: fail("public experiment alignment missing: "+required_marker)
    if "Self-Characterization Trajectory</span><strong>50%" in public_page: fail("non-operative v0.5 scoring still presented as operative")
    if "permitted reconciliation/self-repair" in public_page: fail("non-operative v0.5 self-repair path still presented as operative")
    if cfg.get("operative_experiment_condition")!="v0.3": fail("operative experiment condition")
    if cfg.get("implementation_version")!="v0.9": fail("implementation version")
    if cfg.get("principal_wall_clock_bound") is not False: fail("v0.3 principal wall-clock semantics")
    if cfg.get("canonical_live_observer_route")!="/sv002-observe/": fail("canonical live observer route")
    historical=(ROOT/"stegverse-002.html").read_text(encoding="utf-8")
    if "Historical construction boundary" not in historical or "not available to the experimental principal" not in historical:
        fail("SV002 historical/experiment boundary missing")
    formalism=(ROOT/"formalism-tests-stage-1-to-31.html").read_text(encoding="utf-8")
    if "Relationship to StegVerse-002" not in formalism or "not StegVerse-002 construction receipts" not in formalism:
        fail("Stage 1-31 relationship boundary missing")
    release_index=(ROOT/"transition-release-index.html").read_text(encoding="utf-8")
    if "Pre-existing transition research evidence surface" not in release_index or "data/transition-release-index-v1.json" not in release_index:
        fail("transition release index static boundary/machine-readable path missing")
    page=PAGE.read_text(encoding="utf-8")
    for marker in ("implemented ≠ validated ≠ merged ≠ deployed ≠ activated ≠ observed ≠ reconstructed","Completing self-characterization does not self-promote StegVerse-002","TRANSITION-ELEMENT DERIVED","../data/sv002-experiment-status.json","../sv002-observe/"):
        if marker not in page: fail("missing page marker: "+marker)
    print("SV002_EXPERIMENT_STATUS_PASS")
if __name__=="__main__":
    main()
