#!/usr/bin/env python3
"""Validate the bounded public Build Trajectory surface."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "build-trajectory.html"
NEWS = ROOT / "news-releases.html"
DATA = ROOT / "data" / "build-trajectory.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


page = PAGE.read_text(encoding="utf-8")
news = NEWS.read_text(encoding="utf-8")
record = json.loads(DATA.read_text(encoding="utf-8"))

require('href="build-trajectory.html"' in news, "Current News Releases lacks Build Trajectory link")
require("Why this log exists" in page, "purpose explanation is missing")
for label in ("Implementation", "Validation", "Release / deployment", "Runtime proof", "Governed activation"):
    require(label in page, f"evidence stage missing: {label}")
for heading in ("Completed outcomes", "Not completed", "Unproven completion claims", "Remaining installation or integration"):
    require(heading in page, f"weekly section missing: {heading}")
require("does not establish" in page and "governed activation" in page, "authority boundary is incomplete")
require("https://github.com/" in page, "completed outcomes lack inspectable evidence links")

html_dates = re.findall(r'data-period-end="(\d{4}-\d{2}-\d{2})"', page)
require(html_dates == sorted(html_dates, reverse=True), "HTML reports are not newest-first")
json_dates = [item["period_end"] for item in record["reports"]]
require(json_dates == sorted(json_dates, reverse=True), "JSON reports are not newest-first")
require(html_dates == json_dates, "HTML and JSON report periods differ")
require(record["evidence_stages"] == [
    "IMPLEMENTATION",
    "VALIDATION",
    "RELEASE_OR_DEPLOYMENT",
    "RUNTIME_PROOF",
    "GOVERNED_ACTIVATION",
], "evidence stage contract changed")
require(all(not item["activation_effect"] for item in record["reports"]), "publication cannot grant activation")

print("PASS: Build Trajectory structure, ordering, evidence stages, and authority boundary validated")
