#!/usr/bin/env python3
from __future__ import annotations

import json
import socket
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "data" / "ecosystem-chat-gateway.json"
REPORT = ROOT / "reports" / "external-chat-live-verification.json"
SITE_BASE = "https://stegverse-labs.github.io/Site"


def observed_at() -> str:
    return datetime.now(timezone.utc).isoformat()


def fetch(url: str) -> dict[str, Any]:
    request = urllib.request.Request(url, headers={"User-Agent": "StegVerse-External-Chat-Live-Check"})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            body = response.read().decode("utf-8", errors="replace")
            content_type = response.headers.get("Content-Type", "")
            parsed = json.loads(body) if "json" in content_type else None
            return {
                "url": url,
                "observed_at": observed_at(),
                "reachable": True,
                "http_status": response.status,
                "content_type": content_type,
                "body_preview": body[:500],
                "json": parsed,
                "error_class": None,
                "error": None,
                "_validation_body": body,
            }
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return {
            "url": url,
            "observed_at": observed_at(),
            "reachable": True,
            "http_status": exc.code,
            "content_type": exc.headers.get("Content-Type", "") if exc.headers else "",
            "body_preview": body[:500],
            "json": None,
            "error_class": "HTTPError",
            "error": str(exc),
            "_validation_body": body,
        }
    except (urllib.error.URLError, TimeoutError, socket.timeout, OSError) as exc:
        return {
            "url": url,
            "observed_at": observed_at(),
            "reachable": False,
            "http_status": None,
            "content_type": None,
            "body_preview": None,
            "json": None,
            "error_class": type(exc).__name__,
            "error": str(exc),
            "_validation_body": "",
        }


def public_check(check: dict[str, Any]) -> dict[str, Any]:
    """Remove transient response bodies before retaining the verification receipt."""
    return {key: value for key, value in check.items() if not key.startswith("_")}


def write_report(checks: list[dict[str, Any]], passed: bool, failure: str | None) -> None:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps({
        "schema_version": "1.0.0",
        "receipt_type": "external_chat_live_verification_receipt",
        "generated_at": observed_at(),
        "passed": passed,
        "failure": failure,
        "checks": [public_check(check) for check in checks],
        "required_public_mutation_state": "DISABLED",
        "authority_boundary": {
            "live_check_is_deployment_authority": False,
            "live_check_is_mutation_authority": False,
            "live_check_is_certification": False,
            "network_resolution_failure_is_product_failure": False,
        },
    }, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    checks: list[dict[str, Any]] = []
    failure: str | None = None
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    gateway_base = config["endpoint"].removesuffix("/api/ecosystem-chat")

    pages = {
        f"{SITE_BASE}/external-chat.html": ["External Chat", "compatibility evidence only"],
        f"{SITE_BASE}/external-review.html": ["External Chat Reviewer Console", "delegated reviewer"],
    }
    for url, markers in pages.items():
        result = fetch(url)
        checks.append(result)
        if not result["reachable"]:
            failure = f"network_unresolved:{url}:{result['error_class']}"
            break
        if result["http_status"] != 200:
            failure = f"http_status:{url}:{result['http_status']}"
            break
        body = result.get("_validation_body", "")
        missing = [marker for marker in markers if marker not in body]
        if missing:
            failure = f"page_markers:{url}:{','.join(missing)}"
            break

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
            "mutation_enabled": False,
        },
    }
    if failure is None:
        for url, expected in health_routes.items():
            result = fetch(url)
            checks.append(result)
            if not result["reachable"]:
                failure = f"network_unresolved:{url}:{result['error_class']}"
                break
            payload = result.get("json")
            if result["http_status"] != 200 or not isinstance(payload, dict):
                failure = f"health_contract_unavailable:{url}:{result['http_status']}"
                break
            mismatches = {key: {"expected": value, "observed": payload.get(key)} for key, value in expected.items() if payload.get(key) != value}
            if mismatches:
                failure = f"health_contract_mismatch:{url}:{json.dumps(mismatches, sort_keys=True)}"
                break

    passed = failure is None
    write_report(checks, passed, failure)
    if passed:
        print(f"EXTERNAL CHAT LIVE ROUTES: PASS ({REPORT.relative_to(ROOT)})")
        return 0
    print(f"EXTERNAL CHAT LIVE ROUTES: FAIL - {failure} ({REPORT.relative_to(ROOT)})")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
