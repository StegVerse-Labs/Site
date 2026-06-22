#!/usr/bin/env python3
"""Validate publication micro-node workflow documentation."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "docs/PUBLICATION_MICRO_NODE_WORKFLOW.md",
    "docs/RELEASE_EVALUATOR_HANDOFF.md",
    "docs/MASTER_RECORDS_PUBLICATION_CONFIRMATION_GATE.md",
    "docs/PUBLICATION_WORKFLOW_PACKET_SCHEMA.md",
]

REQUIRED_TERMS = {
    "docs/PUBLICATION_MICRO_NODE_WORKFLOW.md": [
        "Publication Workflow Class",
        "Publication Supervisor Node",
        "Release Evaluation Node",
        "master-records Confirmation Node",
        "Final Publication Workflow Receipt",
        "Publisher must not ingest raw repository releases directly.",
    ],
    "docs/RELEASE_EVALUATOR_HANDOFF.md": [
        "Publisher must not evaluate raw releases directly.",
        "ADMIT",
        "DENY",
        "QUARANTINE",
        "master-records confirmation",
        "Publisher may ingest only packets",
    ],
    "docs/MASTER_RECORDS_PUBLICATION_CONFIRMATION_GATE.md": [
        "Evaluator approval is not publication standing.",
        "CONFIRMED",
        "UNCONFIRMED",
        "MISSING",
        "CONTRADICTED",
        "STALE",
        "Was the entire publication workflow reconstructable at confirmation time?",
    ],
    "docs/PUBLICATION_WORKFLOW_PACKET_SCHEMA.md": [
        "publication-workflow-packet/v0.1",
        "master_records_confirmation_required",
        "raw_release_publishable",
        "final_workflow_receipt_hash",
        "Ingestion, Sandbox, SV-002, and Micro-Node Architecture Update",
    ],
}


def read(path: str) -> str:
    file_path = ROOT / path
    if not file_path.exists():
        raise SystemExit(f"missing required file: {path}")
    return file_path.read_text(encoding="utf-8")


def main() -> None:
    for required_file in REQUIRED_FILES:
        content = read(required_file)
        for term in REQUIRED_TERMS[required_file]:
            if term not in content:
                raise SystemExit(f"{required_file} missing required term: {term}")

    handoff = read("docs/PUBLICATION_MICRO_NODE_WORKFLOW.md")
    if "github/workflows/...` is displayed without the leading dot" not in handoff:
        raise SystemExit("workflow handoff must preserve leading-dot display note")

    print("publication micro-node workflow documentation check passed")


if __name__ == "__main__":
    main()
