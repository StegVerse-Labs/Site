#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
html=(ROOT/"sv002-observe/index.html").read_text()
js=(ROOT/"assets/sv002-observe.js").read_text()
handoff=(ROOT/"docs/SV002_PUBLIC_OBSERVATION_MIRROR_HANDOFF.md").read_text()
required_html=["STEGVERSE NODE REQUIRED","Open observation Interlock","assets/stegverse-node-continuity.js","assets/evaluator-intr-connector.js","stegos-node/sv002-intr-sync.js","assets/sv002-observe.js"]
required_js=["SV002_PUBLIC_OBSERVE","READ_OBSERVATION","StegVerseNodeContinuity.status","StegVerseInterlockConnector","transport_receipts.ingress","transport_receipts.egress","No experiment data","QUEUED_FOR_EVENT_EPHEMERAL_MATERIALIZATION","DURABLE_QUEUE_OR_EVENT_EPHEMERAL_MATERIALIZATION","queueIntrMaterializationRequest","always_on_receiver_required:false","StegVerse-Labs/.github#493"]
for x in required_html:
    assert x in html, x
for x in required_js:
    assert x in js, x
assert "static JSON" not in js
assert "no experiment data" in handoff.lower()
assert "observer does not gain an interaction edge" in handoff
print("SV002 PUBLIC OBSERVATION SURFACE: PASS")
