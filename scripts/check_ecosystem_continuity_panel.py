#!/usr/bin/env python3
"""Validate the fail-closed user-facing ECE continuity panel source contract."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "ecosystem-continuity.html"
JS = ROOT / "assets" / "ecosystem-continuity-panel.js"


def require(ok: bool, reason: str) -> None:
    if not ok:
        raise SystemExit("ECOSYSTEM_CONTINUITY_PANEL_FAIL: " + reason)


def main() -> int:
    require(HTML.is_file(), "missing ecosystem-continuity.html")
    require(JS.is_file(), "missing assets/ecosystem-continuity-panel.js")
    html = HTML.read_text(encoding="utf-8")
    js = JS.read_text(encoding="utf-8")

    for marker in (
        "Read-only evidence projection",
        "Site does not calculate continuity",
        "No authentic retained projection is currently available",
        "assets/ecosystem-continuity-panel.js",
    ):
        require(marker in html, f"missing HTML marker:{marker}")

    for marker in (
        "data/ecosystem-continuity/current.json",
        "stegverse.site-ecosystem-continuity-projection.v1",
        "NONE_READ_ONLY_PROJECTION",
        "PROJECTION_HTTP_",
        "SOURCE_NOT_AVAILABLE",
        "UNSAFE_OR_INVALID_FINDINGS",
        "cache: 'no-store'",
    ):
        require(marker in js, f"missing JS marker:{marker}")

    prohibited = (
        "NONE_DIAGNOSTIC_ONLY",
        "raw evidence",
        "credential",
        "private KV",
    )
    # The consumer may describe prohibited concepts in explanatory copy, but it must
    # never reference raw evaluator evidence/detail fields as data properties.
    require("row.evidence" not in js, "raw evidence field referenced")
    require("row.detail" not in js, "free-form detail field referenced")
    require("evaluation.continuity_state" not in js, "panel contains evaluator logic")
    require("localStorage" not in js and "sessionStorage" not in js, "stale browser state fallback prohibited")
    require("CONTINUOUS'" in js and "INDETERMINATE'" in js, "canonical projection state vocabulary missing")
    require(all(word in html or word in js for word in prohibited), "authority-boundary explanatory markers missing")

    print("ECOSYSTEM_CONTINUITY_PANEL=PASS")
    print("ECOSYSTEM_CONTINUITY_PANEL_FAIL_CLOSED=PASS")
    print("ECOSYSTEM_CONTINUITY_PANEL_SYNTHETIC_GREEN_FALLBACK=false")
    print("ECOSYSTEM_CONTINUITY_PANEL_AUTHORITY_EFFECT=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
