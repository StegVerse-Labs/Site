#!/usr/bin/env python3
"""Validate Site public path and ingestion-surface documentation contracts.

This check keeps the Site repository legible as a public artifact endpoint without
letting traffic, uploads, workflow visibility, or mirrored files imply authority.
"""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

PUBLIC_PATHS = REPO_ROOT / "docs" / "SITE_PUBLIC_PATHS.md"
INGESTION_SURFACES = REPO_ROOT / "docs" / "SITE_INGESTION_SURFACES.md"
HARDENING_PACKET = REPO_ROOT / "docs" / "SITE_PUBLIC_PATH_AND_INGESTION_SURFACE_HARDENING.md"
TRAFFIC_SIGNAL = REPO_ROOT / "docs" / "SITE_TRAFFIC_AND_INGESTION_SIGNAL.md"
HANDOFF = REPO_ROOT / "docs" / "SITE_MIRROR_HANDOFF.md"

REQUIRED_FILES = [
    PUBLIC_PATHS,
    INGESTION_SURFACES,
    HARDENING_PACKET,
    TRAFFIC_SIGNAL,
    HANDOFF,
]

PUBLIC_PATH_FRAGMENTS = [
    "/upload",
    "/upload/main",
    "/upload/main/incoming",
    "/upload/main/tools",
    "/tree/main/incoming",
    "/tree/main/tools",
    "/tree/main/data",
    "/actions",
    "papers",
]

BOUNDARY_FRAGMENTS = [
    "traffic from adoption",
    "workflow visibility from activation evidence",
    "display from source of truth",
    "upload from validation",
    "ingestion from authority",
]

NON_AUTHORITY_FRAGMENTS = [
    "not adoption",
    "not activation",
    "not authority",
    "not source of truth",
]

HANDOFF_REFERENCES = [
    "docs/SITE_PUBLIC_PATHS.md",
    "docs/SITE_INGESTION_SURFACES.md",
    "docs/SITE_PUBLIC_PATH_AND_INGESTION_SURFACE_HARDENING.md",
    "docs/SITE_TRAFFIC_AND_INGESTION_SIGNAL.md",
]


def normalized(text: str) -> str:
    return " ".join(text.lower().split())


def fail(message: str) -> int:
    print(f"site public ingestion contract check failed: {message}")
    return 1


def require_file(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(str(path.relative_to(REPO_ROOT)))
    return path.read_text(encoding="utf-8")


def require_fragments(label: str, text: str, fragments: list[str]) -> int:
    text_norm = normalized(text)
    for fragment in fragments:
        if normalized(fragment) not in text_norm:
            return fail(f"{label} missing required fragment: {fragment}")
    return 0


def main() -> int:
    try:
        contents = {path: require_file(path) for path in REQUIRED_FILES}
    except FileNotFoundError as exc:
        return fail(f"missing required file: {exc}")

    public_text = contents[PUBLIC_PATHS]
    ingestion_text = contents[INGESTION_SURFACES]
    hardening_text = contents[HARDENING_PACKET]
    traffic_text = contents[TRAFFIC_SIGNAL]
    handoff_text = contents[HANDOFF]

    checks = [
        ("public paths", public_text, PUBLIC_PATH_FRAGMENTS),
        ("ingestion surfaces", ingestion_text, PUBLIC_PATH_FRAGMENTS),
        ("hardening packet boundaries", hardening_text, BOUNDARY_FRAGMENTS),
        ("traffic signal boundaries", traffic_text, NON_AUTHORITY_FRAGMENTS),
        ("handoff references", handoff_text, HANDOFF_REFERENCES),
    ]

    for label, text, fragments in checks:
        result = require_fragments(label, text, fragments)
        if result:
            return result

    print("valid: Site public path and ingestion-surface contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
