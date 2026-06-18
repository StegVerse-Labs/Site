#!/usr/bin/env python3
"""Check the Site mirror evidence packet has required evidence fields.

This checker is intentionally strict about required field names but does not
require live evidence to be present yet. While activation is pending, fields may
remain PENDING. A completed activation packet must replace all PENDING values.
"""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = REPO_ROOT / "docs" / "SITE_MIRROR_EVIDENCE_PACKET.md"

REQUIRED_FIELDS = [
    "publisher_dry_run_workflow_url",
    "publisher_dry_run_receipt_commit",
    "publisher_live_dispatch_workflow_url",
    "site_mirror_workflow_url",
    "site_mirror_commit_sha",
    "manifest_source_repository",
    "manifest_source_ref",
    "manifest_source_of_truth",
    "alias_verification_results",
    "publisher_receipt_update_commit",
    "publisher_verification_tracker_commit",
    "publisher_activation_status_update_commit",
]

REQUIRED_REFERENCES = [
    "docs/SITE_MIRROR_HANDOFF.md",
    "python scripts/check_paper_display_policy.py",
    "python scripts/check_papers_manifest_metadata.py",
    "python scripts/check_paper_aliases.py",
    "valid: Site papers manifest metadata",
    "valid: Site paper aliases resolve",
]


def fail(message: str) -> int:
    print(f"site mirror evidence packet check failed: {message}")
    return 1


def main() -> int:
    if not PACKET_PATH.exists():
        return fail("missing docs/SITE_MIRROR_EVIDENCE_PACKET.md")

    text = PACKET_PATH.read_text(encoding="utf-8")

    for field in REQUIRED_FIELDS:
        if f"{field}:" not in text:
            return fail(f"missing evidence field: {field}")

    for reference in REQUIRED_REFERENCES:
        if reference not in text:
            return fail(f"missing required reference: {reference}")

    print("valid: Site mirror evidence packet structure")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
