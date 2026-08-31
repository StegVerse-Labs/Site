#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sv=(ROOT/"assets/sv002-observe.js").read_text()
sv_page=(ROOT/"sv002-observe/index.html").read_text()
hil=(ROOT/"assets/hil-direct-upload-v1.js").read_text()
hil_page=(ROOT/"humans-as-interoperability-layer.html").read_text()

for name,text in (("SV002",sv),("HIL",hil)):
    if "StegVerseHBInTrCarrier" not in text:
        raise SystemExit(name+" does not use shared HB InTr carrier")
    if "carrier_binding" not in text:
        raise SystemExit(name+" materialization lacks carrier binding")
    if "request_hash" not in text:
        raise SystemExit(name+" does not rehash complete materialization")

if sv_page.index("../assets/hb-intr-carrier.js") > sv_page.index("../assets/sv002-observe.js"):
    raise SystemExit("SV002 carrier client must load before observation client")
if hil_page.index("assets/hb-intr-carrier.js") > hil_page.index("assets/hil-direct-upload-v1.js"):
    raise SystemExit("HIL carrier client must load before upload client")

for marker in (
    "carrier_grants_admission_authority:false",
    "carrier_grants_execution_authority:false",
    "carrier_grants_credential_authority:false",
    "carrier_grants_routing_authority:false",
    "carrier_grants_transition_authority:false",
    "carrier_grants_receiving_authority:false",
):
    carrier=(ROOT/"assets/hb-intr-carrier.js").read_text()
    if marker not in carrier:
        raise SystemExit("shared HB carrier authority invariant missing: "+marker)

print("Site SV002/HIL HB InTr carrier migration: PASS")
