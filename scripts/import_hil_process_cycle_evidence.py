#!/usr/bin/env python3
"""Validate and append a bounded HIL real-process cycle observation."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "hil-process-cycle-promotion-policy.json"
DEST = ROOT / "data" / "hil-process-cycle-observations"


def fail(message: str) -> None:
    raise SystemExit(f"HIL process-cycle import failed: {message}")


def canonical_hash(payload: dict) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("evidence", type=Path)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    policy = json.loads(POLICY.read_text(encoding="utf-8"))
    evidence = json.loads(args.evidence.read_text(encoding="utf-8"))
    claimed = evidence.get("evidence_sha256")
    unsigned = dict(evidence)
    unsigned.pop("evidence_sha256", None)
    require(isinstance(claimed, str) and len(claimed) == 64, "missing evidence hash")
    require(canonical_hash(unsigned) == claimed, "evidence hash mismatch")
    require(evidence.get("schema_version") == policy["accepted_evidence_schema"], "schema mismatch")
    require(evidence.get("observation_scope") == policy["accepted_scope"], "scope mismatch")

    before = evidence.get("readiness_before", {})
    after = evidence.get("readiness_after", {})
    require(before.get("state") == "READY", "pre-restart readiness not READY")
    require(after.get("state") == "READY", "post-restart readiness not READY")
    for readiness in (before, after):
        require(readiness.get("primary_sha256") == policy["required_primary_sha256"], "Primary hash mismatch")
        require(readiness.get("prompt_sha256") == policy["required_prompt_sha256"], "prompt hash mismatch")

    receiver = evidence.get("receiver_receipt", {})
    review = evidence.get("private_review_receipt", {})
    publication = evidence.get("publication_record", {})
    lookup = evidence.get("stable_public_lookup", {})
    require(receiver.get("schema_version") == "HIL-RECEIVER-RECEIPT-v2", "receiver receipt missing")
    require(evidence.get("restart_performed") is True, "real process restart not established")
    require(evidence.get("credential_separation_verified") is True, "credential separation missing")
    require(evidence.get("exact_byte_persistence_verified") is True, "exact-byte persistence missing")
    require(evidence.get("provenance_persistence_verified") is True, "provenance persistence missing")
    require(review.get("schema_version") == "HIL-PRIVATE-REVIEW-RECEIPT-v1", "private review receipt missing")
    require(publication.get("schema_version") == "HIL-PUBLICATION-RECORD-v1", "publication record missing")
    require(lookup.get("publication_record_sha256") == publication.get("publication_record_sha256"), "stable lookup mismatch")

    for field in (
        "production_deployment_claimed", "site_import_authorized",
        "master_record_append_authorized", "public_acquisition_authorized", "authority_granted",
    ):
        require(evidence.get(field) is False, f"{field} must remain false")

    promoted = {
        "schema_version": "HIL-PROCESS-CYCLE-PROMOTED-OBSERVATION-v1",
        "source_evidence_sha256": claimed,
        "source_scope": evidence["observation_scope"],
        "source_commit_sha": evidence.get("commit_sha"),
        "source_run_id": evidence.get("run_id"),
        "established": policy["may_establish"],
        "not_established": policy["may_not_establish"],
        "authority_effect": "NONE",
    }
    promoted["promotion_sha256"] = canonical_hash(promoted)
    destination = DEST / f"{claimed}.json"
    if args.apply:
        DEST.mkdir(parents=True, exist_ok=True)
        require(not destination.exists(), "observation already imported")
        destination.write_text(json.dumps(promoted, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"HIL_PROCESS_CYCLE_OBSERVATION_IMPORTED={destination.relative_to(ROOT)}")
    else:
        print(json.dumps(promoted, indent=2, sort_keys=True))
        print("HIL_PROCESS_CYCLE_IMPORT=DRY_RUN")
    print("HIL_AUTHORITY=NONE")


if __name__ == "__main__":
    main()
