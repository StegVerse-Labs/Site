#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("papers/development-without-domination")
PARTS = ROOT / ".pdf-parts"
STATUS = ROOT / "site-publication-status.json"
PDF = ROOT / "Development_Without_Domination_Rigel_Randolph_Final.pdf"
RECEIPT = ROOT / "site-mirror-receipt.json"
EXPECTED = "c2fcb0ce76f5eaba1a6dd4ccdd358fcae29b32b3110767b5f2b5b2ffa347c29d"
ROUTE = "/papers/development-without-domination/"
EXPECTED_PARTS = [PARTS / f"part-{i:04d}.b64" for i in range(1, 5)]


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def task(path: Path, action: str) -> dict[str, str]:
    return {
        "repository": "StegVerse-Labs/Site",
        "path": str(path),
        "issue": "StegVerse-Labs/Site#128",
        "action": action,
    }


def main() -> int:
    current = json.loads(STATUS.read_text())
    actual = digest(PDF) if PDF.exists() else None
    verified = actual == EXPECTED
    deployed = bool(current.get("deployed_route_verified"))
    missing_parts = [part for part in EXPECTED_PARTS if not part.exists()]

    remaining = []
    for part in missing_parts:
        remaining.append(task(part, "Commit the exact base64 transport segment for deterministic PDF reconstruction."))

    if not verified:
        if not missing_parts:
            remaining.append(task(
                PDF,
                "Run scripts/reconstruct_development_without_domination_pdf.py and commit the exact reconstructed PDF after SHA-256 verification.",
            ))
        elif PDF.exists():
            remaining.append(task(PDF, f"Replace invalid PDF bytes; observed SHA-256 {actual}, expected {EXPECTED}."))

    if not deployed:
        remaining.append(task(RECEIPT, "Verify the deployed route and record content identity."))

    if verified and deployed:
        state = "ACTIVATED"
    elif verified:
        state = "ROUTE_READY"
    elif missing_parts:
        state = f"TRANSPORT_{4-len(missing_parts)}_OF_4"
    else:
        state = "RECONSTRUCTION_READY"

    status = {
        **current,
        "state": state,
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "observed_pdf_sha256": actual,
        "pdf_verified": verified,
        "public_route": ROUTE,
        "transport_parts_expected": 4,
        "transport_parts_present": 4 - len(missing_parts),
        "remaining_tasks": remaining,
    }
    status["authority"] = {
        "publication": state == "ACTIVATED",
        "admissibility": False,
        "execution": False,
        "release": False,
    }
    STATUS.write_text(json.dumps(status, indent=2) + "\n")

    if state == "ACTIVATED":
        RECEIPT.write_text(json.dumps({
            "schema_version": "1.0.0",
            "paper_id": status["paper_id"],
            "state": "ACTIVATED",
            "site_repository": "StegVerse-Labs/Site",
            "pdf_path": str(PDF),
            "pdf_sha256": actual,
            "public_route": ROUTE,
            "route_verified": True,
            "generated_at": status["observed_at"],
            "publication_is_admissibility": False,
        }, indent=2) + "\n")

    print(json.dumps({"state": state, "remaining_tasks": remaining}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
