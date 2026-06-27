#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "governance-observatory.html"
STATUS_MD = ROOT / "docs" / "SITE_GOVERNANCE_OBSERVATORY_STATUS.md"
STATUS_JSON = ROOT / "docs" / "SITE_GOVERNANCE_OBSERVATORY_STATUS.json"
PUBLIC_PATHS = ROOT / "docs" / "SITE_PUBLIC_PATHS.md"

REQUIRED_TEXT = [
    "StegVerse-Labs/governance-observatory",
    "governance-observatory-v0.1-source-intake-dev",
    "DecisionAssure",
    "Morrison Runtime",
    "Site is not the source of truth",
]

PUBLIC_PATH_REQUIRED = [
    "/governance-observatory.html",
    "Governance Observatory Boundary",
    "StegVerse-Labs/governance-observatory",
    "docs/SITE_GOVERNANCE_OBSERVATORY_STATUS.md",
    "docs/SITE_GOVERNANCE_OBSERVATORY_STATUS.json",
]


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    if not path.exists():
        fail(f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def main() -> None:
    html = read(HTML)
    status_md = read(STATUS_MD)
    status_json_text = read(STATUS_JSON)
    public_paths = read(PUBLIC_PATHS)

    for phrase in REQUIRED_TEXT:
        if phrase not in html and phrase not in status_md and phrase not in status_json_text:
            fail(f"missing required phrase: {phrase}")

    for phrase in PUBLIC_PATH_REQUIRED:
        if phrase not in public_paths:
            fail(f"public path semantics missing required phrase: {phrase}")

    try:
        status = json.loads(status_json_text)
    except json.JSONDecodeError as exc:
        fail(f"invalid status JSON: {exc}")

    if status.get("schema") != "site_governance_observatory_status.v0.1":
        fail("schema mismatch")
    if status.get("repository") != "StegVerse-Labs/Site":
        fail("repository mismatch")
    if status.get("source_repository") != "StegVerse-Labs/governance-observatory":
        fail("source repository mismatch")
    if status.get("public_page") != "governance-observatory.html":
        fail("public page mismatch")
    if status.get("mirror_status") != "active_public_status_surface":
        fail("mirror status mismatch")
    if "DecisionAssure" not in status.get("deferred_sources", []):
        fail("DecisionAssure deferral missing")
    if "Morrison Runtime" not in status.get("deferred_sources", []):
        fail("Morrison Runtime deferral missing")
    if not status.get("non_claims"):
        fail("non_claims missing")

    print("OK: Site Governance Observatory status mirror validated")


if __name__ == "__main__":
    main()
