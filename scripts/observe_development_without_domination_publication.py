#!/usr/bin/env python3
"""Observe and advance the Development Without Domination publication layer.

The observer converts every incomplete gate into a repository/path-bound next
action. It never reports an unowned or merely "external" blocker.
"""
from __future__ import annotations

import hashlib
import json
import os
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("papers/development-without-domination")
STATUS = ROOT / "site-publication-status.json"
PDF = ROOT / "Development_Without_Domination_Rigel_Randolph_Final.pdf"
RECEIPT = ROOT / "site-mirror-receipt.json"
EXPECTED = "c2fcb0ce76f5eaba1a6dd4ccdd358fcae29b32b3110767b5f2b5b2ffa347c29d"
PUBLISHER_MANIFEST_API = (
    "https://api.github.com/repos/GCAT-BCAT-Engine/Publisher/contents/"
    "papers/development-without-domination/publication-manifest.json"
    "?ref=publication/development-without-domination-v1"
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def publisher_manifest_observed() -> bool:
    request = urllib.request.Request(
        PUBLISHER_MANIFEST_API,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "stegverse-site-publication-observer",
            **({"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"} if os.getenv("GITHUB_TOKEN") else {}),
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return response.status == 200
    except (urllib.error.URLError, TimeoutError):
        return False


def task(repository: str, path: str, action: str, issue: str) -> dict[str, str]:
    return {"repository": repository, "path": path, "issue": issue, "action": action}


def main() -> int:
    current = json.loads(STATUS.read_text(encoding="utf-8")) if STATUS.exists() else {}
    publisher_seen = publisher_manifest_observed()
    pdf_present = PDF.exists()
    actual_hash = sha256(PDF) if pdf_present else None
    pdf_verified = actual_hash == EXPECTED
    route = current.get("public_route")
    route_verified = bool(current.get("deployed_route_verified"))

    remaining: list[dict[str, str]] = []
    if not publisher_seen:
        remaining.append(task(
            "GCAT-BCAT-Engine/Publisher",
            "papers/development-without-domination/publication-manifest.json",
            "Maintain the Publisher manifest on Publisher PR #22.",
            "GCAT-BCAT-Engine/Publisher#21",
        ))
    if not pdf_present:
        remaining.append(task(
            "StegVerse-Labs/Site",
            str(PDF),
            "Commit the exact finalized PDF bytes to Site PR #129.",
            "StegVerse-Labs/Site#128",
        ))
    elif not pdf_verified:
        remaining.append(task(
            "StegVerse-Labs/Site",
            str(PDF),
            f"Replace the PDF: observed SHA-256 {actual_hash}, expected {EXPECTED}.",
            "StegVerse-Labs/Site#128",
        ))
    if not route:
        remaining.append(task(
            "StegVerse-Labs/Site",
            "papers/development-without-domination/index.html",
            "Create the public paper landing route and bind it to the verified PDF.",
            "StegVerse-Labs/Site#128",
        ))
    if route and not route_verified:
        remaining.append(task(
            "StegVerse-Labs/Site",
            "papers/development-without-domination/site-mirror-receipt.json",
            "Verify the deployed route and record content identity.",
            "StegVerse-Labs/Site#128",
        ))

    if pdf_verified and route and route_verified:
        state = "ACTIVATED"
    elif pdf_verified and route:
        state = "ROUTE_READY"
    elif pdf_verified:
        state = "SITE_BYTES_VERIFIED"
    elif publisher_seen:
        state = "SOURCE_OBSERVED"
    else:
        state = "BUILDING"

    status = {
        "schema_version": "1.1.0",
        "paper_id": "development-without-domination-v1",
        "repository": "StegVerse-Labs/Site",
        "state": state,
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "publisher_manifest_observed": publisher_seen,
        "pdf_path": str(PDF),
        "expected_pdf_sha256": EXPECTED,
        "observed_pdf_sha256": actual_hash,
        "pdf_verified": pdf_verified,
        "public_route": route,
        "deployed_route_verified": route_verified,
        "remaining_tasks": remaining,
        "authority": {
            "publication": state == "ACTIVATED",
            "admissibility": False,
            "execution": False,
            "release": False,
        },
    }
    STATUS.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")

    if state == "ACTIVATED":
        receipt = {
            "schema_version": "1.0.0",
            "paper_id": status["paper_id"],
            "state": "ACTIVATED",
            "site_repository": "StegVerse-Labs/Site",
            "pdf_path": str(PDF),
            "pdf_sha256": actual_hash,
            "public_route": route,
            "route_verified": True,
            "generated_at": status["observed_at"],
            "publication_is_admissibility": False,
        }
        RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({"state": state, "remaining_tasks": remaining}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
