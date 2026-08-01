#!/usr/bin/env python3
"""Observe and advance the Development Without Domination publication layer."""
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
PUBLISHER_MANIFEST_API = "https://api.github.com/repos/GCAT-BCAT-Engine/Publisher/contents/papers/development-without-domination/publication-manifest.json?ref=publication/development-without-domination-v1"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def publisher_manifest_observed() -> bool:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "stegverse-site-publication-observer"}
    if os.getenv("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    try:
        with urllib.request.urlopen(urllib.request.Request(PUBLISHER_MANIFEST_API, headers=headers), timeout=20) as response:
            return response.status == 200
    except (urllib.error.URLError, TimeoutError):
        return False


def task(path: str, action: str) -> dict[str, str]:
    return {"repository": "StegVerse-Labs/Site", "path": path, "issue": "StegVerse-Labs/Site#128", "action": action}


def main() -> int:
    ROOT.mkdir(parents=True, exist_ok=True)
    current = json.loads(STATUS.read_text(encoding="utf-8")) if STATUS.exists() else {}
    publisher_seen = publisher_manifest_observed()
    actual_hash = sha256(PDF) if PDF.exists() else None
    pdf_verified = actual_hash == EXPECTED
    landing_present = (ROOT / "index.html").exists()
    route = current.get("public_route") or ("/papers/development-without-domination/" if landing_present else None)
    route_verified = bool(current.get("deployed_route_verified"))

    remaining = []
    if not PDF.exists():
        remaining.append(task(str(PDF), "Commit the exact finalized PDF bytes."))
    elif not pdf_verified:
        remaining.append(task(str(PDF), f"Replace PDF with expected SHA-256 {EXPECTED}; observed {actual_hash}."))
    if not landing_present:
        remaining.append(task(str(ROOT / "index.html"), "Create the public paper landing page."))
    if route and not route_verified:
        remaining.append(task(str(RECEIPT), "Verify the deployed route and record its content identity."))

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
        "schema_version": "1.2.0",
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
        "authority": {"publication": state == "ACTIVATED", "admissibility": False, "execution": False, "release": False}
    }
    STATUS.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")

    if state == "ACTIVATED":
        RECEIPT.write_text(json.dumps({
            "schema_version": "1.0.0",
            "paper_id": status["paper_id"],
            "state": "ACTIVATED",
            "site_repository": "StegVerse-Labs/Site",
            "pdf_path": str(PDF),
            "pdf_sha256": actual_hash,
            "public_route": route,
            "route_verified": True,
            "generated_at": status["observed_at"],
            "publication_is_admissibility": False
        }, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({"state": state, "remaining_tasks": remaining}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
