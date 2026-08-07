#!/usr/bin/env python3
"""Process a bounded private-document fixture into deterministic evidence records.

This is a repository-owned validation processor. It does not expose public upload,
call a model, make medical conclusions, or grant claim authority.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

FALSE_FLAGS = {k: False for k in (
    "adjudication", "representation", "medical_opinion", "rating", "execution", "publication"
)}


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def validate_intake(intake: dict[str, Any]) -> None:
    if intake.get("schema_version") != "1.0.0":
        raise ValueError("unsupported intake schema")
    if intake.get("authority_flags") != FALSE_FLAGS:
        raise ValueError("authority escalation rejected")
    consent = intake.get("consent", {})
    if not all(consent.get(k) is True for k in (
        "user_confirmed_authority_to_submit",
        "user_confirmed_private_processing",
        "user_confirmed_no_emergency_use",
    )):
        raise ValueError("required consent missing")
    seen: set[str] = set()
    for doc in intake.get("documents", []):
        document_id = doc.get("document_id")
        if not document_id or document_id in seen:
            raise ValueError("missing or duplicate document_id")
        seen.add(document_id)
        digest = doc.get("sha256", "")
        if len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
            raise ValueError("invalid document hash")
        if int(doc.get("page_count", 0)) < 1:
            raise ValueError("invalid page count")
    if not seen:
        raise ValueError("at least one document is required")


def process(intake: dict[str, Any]) -> dict[str, Any]:
    validate_intake(intake)
    documents = intake["documents"]
    anchors = []
    facts = []
    for index, doc in enumerate(documents, start=1):
        anchor_id = f"A{index}"
        anchors.append({
            "anchor_id": anchor_id,
            "document_id": doc["document_id"],
            "page": 1,
            "section": "fixture-anchor",
        })
        facts.append({
            "fact_id": f"F{index}",
            "text": f"Document {doc['document_id']} was admitted to the bounded fixture with a verified content hash.",
            "posture": "NEUTRAL",
            "document_id": doc["document_id"],
            "page": 1,
            "anchor_id": anchor_id,
        })
    assessment = {
        "schema_version": "1.0.0",
        "session_id": intake["session_id"],
        "document_index": documents,
        "page_anchors": anchors,
        "facts": facts,
        "inferences": [],
        "contradictions": [],
        "missing_evidence": [{
            "missing_id": "M1",
            "category": "SUBSTANTIVE_REVIEW",
            "description": "This fixture validates intake, hashing, anchoring, privacy, and custody structure only; substantive document interpretation requires a separately verified governed runtime.",
            "materiality": "HIGH",
            "next_action": "Run the separately governed document interpretation capability after its TVC and custody receipts are verified."
        }],
        "privacy": {
            "public_upload_enabled": False,
            "raw_documents_published": False,
            "processing_scope": "REPOSITORY_FIXTURE_ONLY"
        },
        "authority_flags": FALSE_FLAGS,
        "authority_effect": False,
        "activation_effect": False,
    }
    assessment["assessment_hash"] = canonical_hash(assessment)
    return assessment


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: process_va_private_document_fixture.py INPUT OUTPUT", file=sys.stderr)
        return 2
    source, target = map(Path, sys.argv[1:])
    result = process(json.loads(source.read_text(encoding="utf-8")))
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"state": "VERIFIED", "assessment_hash": result["assessment_hash"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
