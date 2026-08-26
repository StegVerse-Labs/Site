#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
STATE=ROOT/"data"/"ecosystem-heartbeat-response-network.json"; TARGETS=ROOT/"data"/"heartbeat-response-adapter-targets.json"; OUTBOX=ROOT/"data"/"heartbeat-response-outbox"/"bootstrap-2026-08-07.json"; RECEIPTS=ROOT/"data"/"heartbeat-response-receipts"; CLASSIFICATION=ROOT/"data"/"heartbeat-response-classification-state.json"; IMPORT_REPORT=ROOT/"data"/"heartbeat-response-import-report.json"
LIFECYCLE=["SENT","RECEIVED","RESPONDED","RECOVERED","REPEAT"]; FAILURE={"BLOCKED","FAILED","REVIEW_REQUIRED"}; DETAIL_CLASSES={"MEMORY","ACTION","AWARENESS","AUTHORITY","EVIDENCE","BLOCKER","CAPABILITY","CONTEXT"}; INSTALLED_STATES={"INSTALLED_EXISTING_HB","ADAPTER_INSTALLED"}
def load_json(path):
    with path.open(encoding="utf-8") as h:return json.load(h)
def canonical_sha256(value): return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def pct(n,d): return round((100.0*n/d),2) if d else 0.0
def authority_is_transport_only(a): return all(a.get(k) is False for k in ("execution","activation","publication","custody","release"))
def validate_receipt(r,known):
    req={"message_id","exchange_id","node_org","source_org","destination_org","stage","detail_class","authority"}; missing=req-r.keys()
    if missing: raise ValueError(f"receipt missing fields: {sorted(missing)}")
    if r["node_org"] not in known or r["source_org"] not in known or r["destination_org"] not in known: raise ValueError("receipt references unregistered organization")
    if r["node_org"]!=r["destination_org"]: raise ValueError("status receipt node_org must equal original destination_org")
    if r["stage"] not in (set(LIFECYCLE)-{"SENT"})|FAILURE: raise ValueError("invalid receipt lifecycle stage")
    if r["detail_class"] not in DETAIL_CLASSES: raise ValueError("invalid detail class")
    if not authority_is_transport_only(r["authority"]): raise ValueError("transport receipt attempts to grant authority")
    return canonical_sha256(r)
def validate_recovery_link(recovered,responded):
    if recovered.get("stage")!="RECOVERED" or responded.get("stage")!="RESPONDED": raise ValueError("invalid recovery-link stages")
    if recovered.get("exchange_id")!=responded.get("exchange_id") or recovered.get("node_org")!=responded.get("node_org"): raise ValueError("recovered receipt identity differs from responded parent")
    if recovered.get("parent_receipt_sha256")!=canonical_sha256(responded): raise ValueError("recovered receipt parent hash mismatch")
    if not authority_is_transport_only(recovered.get("authority",{})): raise ValueError("recovered receipt attempts to grant authority")
def validate_outbox(outbox,known):
    messages=outbox.get("messages",[])
    if outbox.get("message_count")!=len(messages) or len(messages)!=len(known): raise ValueError("bootstrap outbox must contain exactly one message per organization")
    destinations=[]
    for m in messages:
        req={"message_id","exchange_id","source_org","destination_org","stage","detail_class","authority","payload"}; missing=req-m.keys()
        if missing: raise ValueError(f"outbox message missing fields: {sorted(missing)}")
        if m["stage"]!="SENT": raise ValueError("bootstrap outbox contains non-SENT message")
        if m["source_org"] not in known or m["destination_org"] not in known: raise ValueError("outbox references unregistered organization")
        if m["detail_class"] not in DETAIL_CLASSES: raise ValueError("outbox message has invalid detail class")
        if not authority_is_transport_only(m["authority"]): raise ValueError("outbox transport attempts to grant authority")
        destinations.append(m["destination_org"])
    if set(destinations)!=known or len(destinations)!=len(set(destinations)): raise ValueError("bootstrap outbox destination coverage mismatch")
def validate_projection_documents(known,installed):
    c=load_json(CLASSIFICATION); orgs=[i["organization"] for i in c.get("organizations",[])]
    if set(orgs)!=known or len(orgs)!=len(set(orgs)): raise ValueError("classification-state organization inventory mismatch")
    for i in c["organizations"]:
        if i.get("action")!="NO_ACTION_ADMITTED": raise ValueError("heartbeat classification admitted action without destination authority")
    r=load_json(IMPORT_REPORT); rows=[i["organization"] for i in r.get("rows",[])]
    if set(rows)!=known or len(rows)!=len(set(rows)): raise ValueError("import-report organization inventory mismatch")
    if r.get("installed_nodes")!=installed: raise ValueError("import-report installed-node count mismatch")
    if r.get("verified_recovered")!=sum(i.get("state")=="RECOVERED" for i in r["rows"]): raise ValueError("import-report recovered count mismatch")
def main():
    state=load_json(STATE); orgs=state["organizations"]; names=[i["organization"] for i in orgs]; known=set(names)
    if len(names)!=state["organization_count"] or len(known)!=len(names): raise SystemExit("HB_RESPONSE_NETWORK_FAIL: organization inventory count/uniqueness mismatch")
    if state["lifecycle"]!=LIFECYCLE: raise SystemExit("HB_RESPONSE_NETWORK_FAIL: lifecycle order mismatch")
    if set(state["detail_classes"])!=DETAIL_CLASSES: raise SystemExit("HB_RESPONSE_NETWORK_FAIL: detail-class contract mismatch")
    if state.get("heartbeat_model")!="TRANSITION_DRIVEN" or state.get("heartbeat_semantics")!="RESPONSE_NETWORK_LIFECYCLE_ONLY_NOT_CANONICAL_HB_TIMING" or state.get("time_role")!="WATCHDOG_AND_RETRY_ONLY": raise SystemExit("HB_RESPONSE_NETWORK_FAIL: response-network timing semantics changed")
    p=state.get("canonical_protocol_heartbeat",{}); expected={"anchor_epoch":32,"anchor_time_utc":"2026-08-23T19:00:00.000Z","period_ms":10,"reference_rate_hz":100,"progression_dependency":"OSCILLATOR_ONLY","continuous_reference_stream":True,"new_reference_every_10ms":True,"continuous_process_required":False,"resident_sampler_required_for_progression":False,"observation_is_causal":False,"live_proof_state":"COMPLETED","live_proof_transition":"INDEPENDENT_HEARTBEAT_LIVE_PROOF_VERIFIED","authority_effect":"NONE","github_runtime_authority":"NONE"}
    for k,v in expected.items():
        if p.get(k)!=v: raise SystemExit(f"HB_RESPONSE_NETWORK_FAIL: canonical protocol heartbeat {k} mismatch")
    relation=state.get("protocol_relation",{})
    if relation.get("may_observe_protocol_reference") is not True or relation.get("response_transition_causes_protocol_heartbeat") is not False or relation.get("protocol_heartbeat_causes_repeat") is not False or relation.get("repeat_is_protocol_tick") is not False: raise SystemExit("HB_RESPONSE_NETWORK_FAIL: response/protocol causality separation violated")
    targets=load_json(TARGETS); target_orgs=[i["organization"] for i in targets["targets"]]
    if targets.get("organization_count")!=len(names) or set(target_orgs)!=known or len(target_orgs)!=len(set(target_orgs)): raise SystemExit("HB_RESPONSE_NETWORK_FAIL: adapter-target inventory mismatch")
    blocked=[i for i in targets["targets"] if i["state"]=="BLOCKED_NO_REPOSITORY"]
    for i in targets["targets"]:
        if i["state"].startswith("BLOCKED") and not i.get("release_condition"): raise SystemExit("HB_RESPONSE_NETWORK_FAIL: blocked target lacks release condition")
    try: validate_outbox(load_json(OUTBOX),known)
    except ValueError as exc: raise SystemExit(f"HB_RESPONSE_NETWORK_FAIL: {exc}") from exc
    seen={n:set() for n in names}; receipt_count=0; by_exchange={}
    if RECEIPTS.exists():
        for path in sorted(RECEIPTS.glob("*.json")):
            r=load_json(path); validate_receipt(r,known); seen[r["node_org"]].add(r["stage"]); by_exchange.setdefault(r["exchange_id"],{})[r["stage"]]=r; receipt_count+=1
    for ex,stages in by_exchange.items():
        if "RECOVERED" in stages:
            if "RESPONDED" not in stages: raise SystemExit(f"HB_RESPONSE_NETWORK_FAIL: recovered exchange lacks responded parent: {ex}")
            validate_recovery_link(stages["RECOVERED"],stages["RESPONDED"])
    receive=sum("RECEIVED" in s or "RESPONDED" in s or "RECOVERED" in s for s in seen.values()); respond=sum("RESPONDED" in s or "RECOVERED" in s for s in seen.values()); recovery=sum("RECOVERED" in s for s in seen.values()); installed=sum(i["protocol_state"] in INSTALLED_STATES for i in orgs)
    expected_cov={"organizations_registered":len(names),"organizations_protocol_installed":installed,"organizations_receive_verified":receive,"organizations_respond_verified":respond,"organizations_recovery_verified":recovery,"registered_percent":pct(len(names),len(names)),"protocol_installed_percent":pct(installed,len(names)),"receive_verified_percent":pct(receive,len(names)),"respond_verified_percent":pct(respond,len(names)),"recovery_verified_percent":pct(recovery,len(names))}
    if state["coverage"]!=expected_cov: raise SystemExit(f"HB_RESPONSE_NETWORK_FAIL: coverage drift expected={expected_cov} actual={state['coverage']}")
    validate_projection_documents(known,installed)
    print(f"HB_RESPONSE_NETWORK_PASS:HB32_CONTINUOUS_SEPARATED:orgs={len(names)}:installed={installed}:blocked_no_repo={len(blocked)}:receipts={receipt_count}:receive={receive}:respond={respond}:recovered={recovery}")
if __name__=="__main__": main()
