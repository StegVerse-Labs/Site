#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "data" / "ecosystem-chat-gateway.json"
SITE_BASE = "https://stegverse-labs.github.io/Site"


def fetch(url: str) -> tuple[int, str, dict | None]:
    request = urllib.request.Request(url, headers={"User-Agent": "StegVerse-External-Chat-Live-Check"})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            body = response.read().decode("utf-8", errors="replace")
            content_type = response.headers.get("Content-Type", "")
            parsed = json.loads(body) if "json" in content_type else None
            return response.status, body, parsed
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return exc.code, body, None


def fail(message: str) -> int:
    print(f"EXTERNAL CHAT LIVE ROUTES: FAIL - {message}")
    return 1


def main() -> int:
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    gateway_base = config["endpoint"].removesuffix("/api/ecosystem-chat")

    pages = {
        f"{SITE_BASE}/external-chat.html": ["External Chat", "compatibility evidence only"],
        f"{SITE_BASE}/external-review.html": ["External Chat Reviewer Console", "delegated reviewer"],
    }
    for url, markers in pages.items():
        status, body, _ = fetch(url)
        if status != 200:
            return fail(f"{url} returned HTTP {status}")
        for marker in markers:
            if marker not in body:
                return fail(f"{url} missing marker: {marker}")

    health_routes = {
        f"{gateway_base}/api/external-review/health": {
            "service": "stegverse-external-review",
            "package_only_storage": True,
            "raw_artifact_storage_allowed": False,
            "publication_authority": False,
        },
        f"{gateway_base}/api/external-review/repository-mutation/health": {
            "service": "stegverse-external-publication-mutation",
            "allowed_repository": "StegVerse-Labs/admissibility-wiki",
            "allowed_path_prefix": "docs/external-frameworks/",
            "commit_time_revalidation_required": True,
            "publication_transition_is_mutation_authority": False,
        },
    }
    for url, expected in health_routes.items():
        status, _, payload = fetch(url)
        if status != 200 or not isinstance(payload, dict):
            return fail(f"{url} did not return JSON HTTP 200")
        for key, value in expected.items():
            if payload.get(key) != value:
                return fail(f"{url} contract mismatch for {key}: {payload.get(key)!r}")

    mutation = health_routes[f"{gateway_base}/api/external-review/repository-mutation/health"]
    _, _, mutation_payload = fetch(f"{gateway_base}/api/external-review/repository-mutation/health")
    if mutation_payload.get("mutation_enabled") is not False:
        return fail("public verification requires repository mutation disabled")

    print("EXTERNAL CHAT LIVE ROUTES: PASS (pages, review health, mutation health disabled)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
