#!/usr/bin/env python3
"""Apply verified source-grounded cross-repository evidence to VCA-GATE-08 only."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/va-claim-assistant/source-grounded-evidence-manifest.json"
GATES = ROOT / "data/va-claim-assistant/activation-gates.json"


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("state") != "EVIDENCE_CHAIN_VERIFIED":
        raise ValueError("source-grounded evidence chain is not verified")
    if manifest.get("gate_effect", {}).get("VCA-GATE-08") != "VERIFIED":
        raise ValueError("manifest does not authorize gate 08 evidence derivation")
    if manifest.get("activation_effect") is not False:
        raise ValueError("manifest must not grant activation")

    ledger = json.loads(GATES.read_text(encoding="utf-8"))
    for gate in ledger["gates"]:
        if gate["id"] == "VCA-GATE-08":
            gate["state"] = "VERIFIED"
            gate["evidence"] = [
                "data/va-claim-assistant/source-grounded-evidence-manifest.json",
                "data/va-claim-assistant/source-grounded-activation-receipt.json"
            ]
            gate["next_action"] = None
        elif gate["id"] == "VCA-GATE-09" and gate["state"] != "VERIFIED":
            gate["state"] = "BUILDING"
            gate["next_action"] = "Observe the deployed Site page and endpoint and require HTTP 200 plus repository-byte hash equality."

    required = {"VCA-GATE-01", "VCA-GATE-02", "VCA-GATE-03", "VCA-GATE-04", "VCA-GATE-06", "VCA-GATE-07", "VCA-GATE-08", "VCA-GATE-09"}
    source_ready = all(g["state"] == "VERIFIED" for g in ledger["gates"] if g["id"] in required)
    ledger["state"] = "SOURCE_GROUNDED_ACTIVE" if source_ready else "BUILDING"
    ledger["activation_authorized"] = source_ready
    ledger["current_public_capability"] = "SOURCE_GROUNDED_ASSISTANT" if source_ready else "BOUNDED_PROCEDURAL_ASSISTANT"
    GATES.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"gate_08": "VERIFIED", "gate_09": next(g["state"] for g in ledger["gates"] if g["id"] == "VCA-GATE-09"), "activation_authorized": source_ready}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
