#!/usr/bin/env python3
"""Validate the External Chat activation-evidence builder contract."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build_external_chat_activation_evidence.py"
WORKFLOW = ROOT / ".github" / "workflows" / "site-task-runner.yml"
HANDOFF = ROOT / "docs" / "EXTERNAL_CHAT_MIRROR_HANDOFF.md"

REQUIRED_BUILDER_MARKERS = (
    "external_chat_activation_evidence",
    "OBSERVED_NON_MUTATING_PUBLIC_PATHS",
    "LIVE_EVIDENCE_NOT_AVAILABLE",
    "site-task-diagnostic.json",
    "external-chat-live-verification.json",
    "evidence_sha256",
    '"evidence_is_deployment_authority": False',
    '"evidence_is_repository_mutation_authority": False',
    '"evidence_is_publication_authority": False',
    '"evidence_is_certification": False',
    '"evidence_creates_standing": False',
    '"mutation_remains_separately_authorized": True',
)


def fail(message: str) -> int:
    print(f"EXTERNAL CHAT ACTIVATION EVIDENCE CONTRACT: FAIL - {message}")
    return 1


def main() -> int:
    for path in (BUILDER, WORKFLOW, HANDOFF):
        if not path.exists():
            return fail(f"missing {path.relative_to(ROOT)}")

    builder = BUILDER.read_text(encoding="utf-8")
    workflow = WORKFLOW.read_text(encoding="utf-8")
    handoff = HANDOFF.read_text(encoding="utf-8")

    for marker in REQUIRED_BUILDER_MARKERS:
        if marker not in builder:
            return fail(f"builder missing marker: {marker}")

    required_workflow_markers = (
        "Build External Chat activation evidence",
        "python scripts/build_external_chat_activation_evidence.py",
        "Upload External Chat activation evidence",
        "external-chat-activation-evidence-${{ github.run_id }}-${{ github.run_attempt }}",
        "site/reports/external-chat-activation-evidence.json",
        "if: always()",
    )
    for marker in required_workflow_markers:
        if marker not in workflow:
            return fail(f"workflow missing marker: {marker}")

    verify_index = workflow.index("Verify External Chat public surfaces")
    build_index = workflow.index("Build External Chat activation evidence")
    upload_index = workflow.index("Upload External Chat activation evidence")
    if not verify_index < build_index < upload_index:
        return fail("activation evidence must be built after live verification and uploaded afterward")

    for marker in (
        "external-chat-activation-evidence.json",
        "activation evidence",
        "mutation remains separately authorized",
    ):
        if marker not in handoff:
            return fail(f"handoff missing marker: {marker}")

    print("EXTERNAL CHAT ACTIVATION EVIDENCE CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
