#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def main() -> int:
    page = (ROOT / "review-authority.html").read_text(encoding="utf-8")
    script = (ROOT / "assets/review-authority-projection.js").read_text(encoding="utf-8")
    fixture = json.loads((ROOT / "data/review-authority-projection.fixture.json").read_text(encoding="utf-8"))

    for marker in (
        "authority-projection",
        "assets/review-authority-projection.js",
        "data/review-authority-projection.fixture.json",
    ):
        require(marker in page, f"page missing {marker}")

    for marker in (
        "visibility cannot be an authority source",
        "review-only authority escalation",
        "Public visibility does not grant publication",
        "claim_authority",
        "publication_authority",
        "attribution_authority",
        "public_association_authority",
    ):
        require(marker in script, f"projection script missing {marker}")

    require(fixture["visibility_state"] == "PUBLICLY_VISIBLE", "fixture visibility state")
    require(fixture["process_state"] == "REVIEW_ONLY", "fixture process state")
    for field in (
        "claim_authority",
        "publication_authority",
        "attribution_authority",
        "public_association_authority",
    ):
        require(fixture[field] is False, f"fixture {field} must be false")
    for field in ("endorsement", "compatibility", "interoperability"):
        require(fixture[field] == "NONE", f"fixture {field} must be NONE")

    print("Site review authority projection: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
