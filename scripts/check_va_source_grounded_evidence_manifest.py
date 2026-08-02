#!/usr/bin/env python3
"""Validate the Site-owned VA source-grounded cross-repository evidence manifest."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/va-claim-assistant/source-grounded-evidence-manifest.json"

EXPECTED = {
    "llm_adapter": {
        "repository": "StegVerse-org/LLM-adapter",
        "commit": "c643d13e7950d3cb14f8850b2b5b791dedc62154",
        "path": "receipts/va-claim-assistant-public-source-fixture.json",
        "answer_hash": "e68b1740b03bc0a51221cc56222fb7e5794317b26f1684572d1af5080a28aeb3",
    },
    "tvc_readiness": {
        "repository": "StegVerse-Labs/TVC",
        "commit": "f5e4b911ce46d0b3d0e10e114b05def064102d43",
        "path": "receipts/va-claim-assistant-governed-retrieval-readiness.json",
        "state": "READY",
    },
    "tvc_invocation": {
        "repository": "StegVerse-Labs/TVC",
        "commit": "0f0ecf2183e10d27a1d504bdeb30349fe7b3b806",
        "path": "receipts/va-claim-assistant-governed-retrieval-invocation-001.json",
        "state": "EXECUTED",
    },
    "master_records": {
        "repository": "master-records/orchestration",
        "commit": "477a8aee2c68fbb47a25f9ba65f3300319f96977",
        "path": "receipts/va-claim-assistant-public-source-custody.json",
        "custody": "RECORDED",
        "reconstruction": "PASS",
        "input_receipt_hash": "d6407c839b91d4b23be7a48f4dde78c3474427c2b7f28d0cfdb976505028a7ae",
        "answer_hash": "e68b1740b03bc0a51221cc56222fb7e5794317b26f1684572d1af5080a28aeb3",
    },
}


def canonical_hash(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def main() -> int:
    record = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert record["capability"] == "SOURCE_GROUNDED_ASSISTANT"
    assert record["route"] == "evidence_requirement"
    assert record["state"] == "EVIDENCE_CHAIN_VERIFIED"
    assert record["records"] == EXPECTED
    assert all(record["checks"].values())
    assert record["activation_effect"] is False
    assert record["publication_effect"] is False
    assert record["gate_effect"]["VCA-GATE-08"] == "VERIFIED"
    assert record["gate_effect"]["VCA-GATE-09"] == "UNCHANGED_REQUIRES_DEPLOYED_OBSERVATION"
    material = dict(record)
    expected_hash = material.pop("manifest_sha256")
    assert canonical_hash(material) == expected_hash
    assert EXPECTED["llm_adapter"]["answer_hash"] == EXPECTED["master_records"]["answer_hash"]
    print(json.dumps({"result": "PASS", "manifest_sha256": expected_hash}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
