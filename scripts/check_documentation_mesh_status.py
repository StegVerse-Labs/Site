#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "ecosystem-documentation-endpoints.json"
HEALTH = ROOT / "data" / "cross-wiki-health-status.json"
EXPECTED_ENDPOINTS = {
    "stegverse-site": ("StegVerse-Labs/Site", "https://stegverse-labs.github.io/Site/"),
    "admissibility-wiki": ("StegVerse-Labs/admissibility-wiki", "https://stegverse-labs.github.io/admissibility-wiki/"),
    "stegguardian-wiki": ("StegVerse-002/stegguardian-wiki", "https://stegverse-002.github.io/stegguardian-wiki/"),
    "stegtalk-wiki": ("StegVerse-Labs/stegtalk-wiki", "https://stegverse-labs.github.io/stegtalk-wiki/"),
}


def load_json(path: Path, failures: list[str], label: str) -> dict[str, Any]:
    if not path.exists():
        failures.append(f"missing {label}: {path.relative_to(ROOT)}")
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        failures.append(f"invalid {label} json: {exc}")
        return {}


def main() -> int:
    failures: list[str] = []
    registry = load_json(REGISTRY, failures, "endpoint registry")
    health = load_json(HEALTH, failures, "cross-wiki health status")

    if registry.get("record_type") != "stegverse_ecosystem_documentation_endpoints":
        failures.append("endpoint registry record type mismatch")
    endpoints = {item.get("id"): item for item in registry.get("endpoints", []) if isinstance(item, dict)}
    for endpoint_id, (repo, url) in EXPECTED_ENDPOINTS.items():
        item = endpoints.get(endpoint_id)
        if not item:
            failures.append(f"missing endpoint: {endpoint_id}")
            continue
        if item.get("repo") != repo:
            failures.append(f"endpoint repo mismatch: {endpoint_id}")
        if item.get("url") != url:
            failures.append(f"endpoint url mismatch: {endpoint_id}")
        if not item.get("role"):
            failures.append(f"endpoint role missing: {endpoint_id}")

    if health.get("record_type") != "site_cross_wiki_health_status":
        failures.append("health record type mismatch")
    if health.get("repo") != "StegVerse-Labs/Site":
        failures.append("health repo mismatch")
    if health.get("origin_public_url") != "https://stegverse-labs.github.io/Site/":
        failures.append("health origin url mismatch")
    if health.get("peer_registry") != "data/ecosystem-documentation-endpoints.json":
        failures.append("health peer registry mismatch")
    if health.get("status") != "pending_live_peer_checks":
        failures.append("health state must remain pending until live peer checks complete")

    checks = health.get("checks", {})
    if checks.get("peer_urls_declared") is not True:
        failures.append("peer urls declared must be true")
    if checks.get("origin_records_declared") is not True:
        failures.append("origin records declared must be true")
    for key in (
        "live_peer_http_confirmed",
        "peer_machine_records_confirmed",
        "cross_wiki_schema_consistency_confirmed",
    ):
        if checks.get(key) is not False:
            failures.append(f"{key} must remain false until verified")

    print("SITE DOCUMENTATION MESH:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
