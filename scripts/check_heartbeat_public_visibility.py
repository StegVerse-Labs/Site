#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
STATUS=ROOT/"data"/"heartbeat-public-visibility.json"

def fail(msg):
    raise SystemExit("HEARTBEAT_PUBLIC_VISIBILITY_FAIL:"+msg)

def main():
    state=json.loads(STATUS.read_text(encoding="utf-8"))
    if state.get("schema")!="stegverse.site.heartbeat_public_visibility.v1":
        fail("schema")
    if state.get("heartbeat_protocol")!="HB32" or state.get("canonical_progression")!="OSCILLATOR_ONLY":
        fail("protocol")
    if state.get("period_ms")!=10 or state.get("reference_rate_hz")!=100 or state.get("continuous_reference_stream") is not True:
        fail("timing")
    if state.get("live_proof_state")!="COMPLETED" or state.get("live_proof_transition")!="INDEPENDENT_HEARTBEAT_LIVE_PROOF_VERIFIED":
        fail("live_proof")
    if state.get("authority_effect")!="NONE" or state.get("execution_authority")!="NONE" or state.get("activation_effect") is not False:
        fail("authority")

    for name,spec in state["public_surfaces"].items():
        path=ROOT/spec["path"]
        if not path.exists():
            fail(f"{name}:missing:{spec['path']}")
        text=path.read_text(encoding="utf-8")
        link=spec.get("required_link")
        if link and link not in text:
            fail(f"{name}:link_missing")
        label=spec.get("required_label")
        if label and label not in text:
            fail(f"{name}:label_missing")
        for token in spec.get("required_status_tokens",[]):
            if token not in text:
                fail(f"{name}:token_missing:{token}")

    print("HEARTBEAT_PUBLIC_VISIBILITY_PASS:HB32:HOME+VERSION+DEDICATED_STATUS:AUTHORITY_NONE")

if __name__=="__main__":
    main()
