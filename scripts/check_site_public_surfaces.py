#!/usr/bin/env python3
"""Check Site public path and ingestion surface documentation.

This checker keeps public-path hardening explicit without claiming live mirror
activation. It verifies that the public path and ingestion docs exist and keep
traffic, upload, workflow, and mirror semantics bounded.
"""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PUBLIC_PATHS = REPO_ROOT / "docs" / "SITE_PUBLIC_PATHS.md"
INGESTION_SURFACES = REPO_ROOT / "docs" / "SITE_INGESTION_SURFACES.md"

PUBLIC_REQUIRED = [
    "docs/SITE_MIRROR_HANDOFF.md",
    "docs/SITE_TRAFFIC_AND_INGESTION_SIGNAL.md",
    "GCAT-BCAT-Engine/Publisher",
    "adoption",
    "activation",
    "endorsement",
    "/upload",
    "/tree/main/incoming",
    "/tree/main/tools",
    "/tree/main/data",
    "/actions",
    "/papers",
]

INGESTION_REQUIRED = [
    "Ingestion is not authority.",
    "accepted for display ≠ source of truth",
    "workflow ran ≠ activation complete",
    "candidate",
    "sandbox_only",
    "mirrored_display_artifact",
    "evidence_pending",
    "activation_supporting",
    "source_repository",
    "source_ref",
    "source_path",
    "source_of_truth",
    "python scripts/check_papers_manifest_metadata.py",
    "python scripts/check_site_mirror_live_evidence_state.py",
    "ready_for_live_mirror_verification",
]


def fail(message: str) -> int:
    print(f"site public surfaces check failed: {message}")
    return 1


def require_file(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(str(path.relative_to(REPO_ROOT)))
    return path.read_text(encoding="utf-8")


def check_required(name: str, text: str, required: list[str]) -> int:
    for item in required:
        if item not in text:
            return fail(f"{name} missing required text: {item}")
    return 0


def main() -> int:
    try:
        public_text = require_file(PUBLIC_PATHS)
        ingestion_text = require_file(INGESTION_SURFACES)
    except FileNotFoundError as exc:
        return fail(f"missing {exc}")

    public_result = check_required("docs/SITE_PUBLIC_PATHS.md", public_text, PUBLIC_REQUIRED)
    if public_result:
        return public_result

    ingestion_result = check_required(
        "docs/SITE_INGESTION_SURFACES.md",
        ingestion_text,
        INGESTION_REQUIRED,
    )
    if ingestion_result:
        return ingestion_result

    if "Status: public_path_semantics_documented" not in public_text:
        return fail("public path semantics status is missing")

    if "Status: ingestion_surface_semantics_documented" not in ingestion_text:
        return fail("ingestion surface semantics status is missing")

    print("valid: Site public path and ingestion surface semantics")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
