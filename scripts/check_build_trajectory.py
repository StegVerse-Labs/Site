#!/usr/bin/env python3
"""Validate the canonical Build Trajectory record and exact public projection."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "build-trajectory.html"
NEWS = ROOT / "news-releases.html"
DATA = ROOT / "data" / "build-trajectory.json"
RENDERER = ROOT / "scripts" / "render_build_trajectory.py"
STAGE_IDS = ["IMPLEMENTATION", "VALIDATION", "RELEASE_OR_DEPLOYMENT", "RUNTIME_PROOF", "GOVERNED_ACTIVATION"]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


record = json.loads(DATA.read_text(encoding="utf-8"))
page = PAGE.read_text(encoding="utf-8")
news = NEWS.read_text(encoding="utf-8")
projection = record["projection"]
policy = record["publication_policy"]

require(record["source_of_truth"] == "data/build-trajectory.json", "canonical source changed")
require(projection == {
    "renderer": "scripts/render_build_trajectory.py",
    "generated_artifact": "build-trajectory.html",
    "manual_projection_edits_allowed": False,
    "exact_byte_reconstruction_required": True,
}, "projection contract changed")
require(policy["weekly_update_mode"] == "PULL_REQUEST_ONLY", "weekly updates must remain PR-only")
require(policy["evidence_reference_mode"] == "IMMUTABLE_COMMIT_PINNED", "evidence links must remain commit-pinned")
require(policy["direct_publication_allowed"] is False, "direct publication cannot be allowed")
require(policy["corrections_are_append_only"] is True, "corrections must remain append-only")
require(policy["silent_historical_rewrites_allowed"] is False, "silent rewrites cannot be allowed")
require(policy["deployment_is_public_observation"] is False, "deployment cannot equal observation")
require(policy["site_display_grants_authority"] is False, "Site display cannot grant authority")
require([stage["id"] for stage in record["evidence_stages"]] == STAGE_IDS, "evidence stage contract changed")

dates = [report["period_end"] for report in record["reports"]]
require(dates == sorted(dates, reverse=True), "reports are not newest-first")
require(len(dates) == len(set(dates)), "duplicate report period_end")
report_ids = [report["report_id"] for report in record["reports"]]
require(len(report_ids) == len(set(report_ids)), "duplicate report_id")

evidence_urls: list[str] = []
for report in record["reports"]:
    metrics = report["metrics"]
    require(metrics["completed_outcome_count"] == len(report["completed_outcomes"]), f'{report["report_id"]} count mismatch')
    require(metrics["authority_effect"] is False, f'{report["report_id"]} cannot grant authority')
    require(metrics["activation_effect"] is False, f'{report["report_id"]} cannot grant activation')
    require(report["not_completed"], f'{report["report_id"]} incomplete work missing')
    require(report["unproven_completion_claims"], f'{report["report_id"]} unsupported claims missing')
    for outcome in report["completed_outcomes"]:
        require(outcome["evidence"], f'{outcome["id"]} lacks evidence')
        require(set(outcome["stages"]).issubset(STAGE_IDS), f'{outcome["id"]} uses unknown stage')
        require(outcome["boundary"], f'{outcome["id"]} lacks stage boundary')
        for evidence in outcome["evidence"]:
            parsed = urlparse(evidence["url"])
            require(parsed.scheme == "https", f'{outcome["id"]} evidence is not HTTPS')
            require(parsed.netloc == "github.com", f'{outcome["id"]} evidence host is not approved')
            match = re.fullmatch(r"/[^/]+/[^/]+/blob/([0-9a-f]{40})/(.+)", parsed.path)
            require(match is not None, f'{outcome["id"]} evidence is not an immutable commit-pinned file path')
            require(re.fullmatch(r"[0-9a-f]{40}", evidence["source_commit"]) is not None, f'{outcome["id"]} source commit invalid')
            require(match.group(1) == evidence["source_commit"], f'{outcome["id"]} URL/source commit mismatch')
            require(match.group(2) == evidence["artifact"], f'{outcome["id"]} URL/artifact mismatch')
            require(evidence["artifact"], f'{outcome["id"]} artifact name missing')
            require(re.fullmatch(r"[0-9a-f]{40}", evidence["observed_blob_sha"]) is not None, f'{outcome["id"]} observed blob SHA invalid')
            require(re.fullmatch(r"\d{4}-\d{2}-\d{2}", evidence["verified_at"]) is not None, f'{outcome["id"]} verification date invalid')
            evidence_urls.append(evidence["url"])
    for correction in report["corrections"]:
        require(re.fullmatch(r"\d{4}-\d{2}-\d{2}", correction["corrected_at"]) is not None, "correction date invalid")
        require(correction["reason"] and correction["replacement"], "correction incomplete")

require(len(evidence_urls) == len(set(evidence_urls)), "duplicate evidence link")
require('href="build-trajectory.html"' in news, "Current News Releases lacks Build Trajectory link")
for heading in ("Why this log exists", "Completed outcomes", "Not completed", "Unproven completion claims", "Remaining installation or integration"):
    require(heading in page, f"projected section missing: {heading}")

result = subprocess.run([sys.executable, str(RENDERER), "--check"], cwd=ROOT, text=True, capture_output=True, check=False)
require(result.returncode == 0, result.stdout.strip() or result.stderr.strip() or "exact projection failed")
print("PASS: canonical record, policy, evidence links, ordering, and exact public projection validated")
