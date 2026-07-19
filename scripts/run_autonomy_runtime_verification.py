#!/usr/bin/env python3
"""Execute Site autonomy runtime checks and persist fail-closed evidence."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "data/autonomy/runtime-checks.json"
OUT = ROOT / "data/autonomy/runtime-verification-evidence.json"


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def fetch(url: str, accept: str) -> tuple[int, str, str]:
    request = Request(url, headers={"Accept": accept, "User-Agent": "StegVerse-Site-Runtime-Verifier/1.0"})
    with urlopen(request, timeout=30) as response:
        return response.status, response.headers.get("content-type", ""), response.read().decode("utf-8")


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def main() -> None:
    spec = load(SPEC)
    evidence: list[dict[str, Any]] = []
    telemetry: dict[str, Any] | None = None

    for check in spec.get("checks", []):
        check_id = str(check.get("id"))
        result: dict[str, Any] = {"id": check_id, "required": bool(check.get("required", False)), "passed": False}
        try:
            kind = check.get("type")
            if kind == "http-json":
                status, content_type, body = fetch(str(check["url"]), "application/json")
                telemetry = json.loads(body)
                result.update(status_code=status, content_type=content_type, passed=status == 200 and isinstance(telemetry, dict))
            elif kind == "http-html":
                status, content_type, body = fetch(str(check["url"]), "text/html")
                result.update(status_code=status, content_type=content_type, passed=status == 200 and "<html" in body.lower() and len(body) > 500)
            elif kind == "json-field":
                if telemetry is None:
                    raise RuntimeError("telemetry JSON was not loaded")
                value = telemetry.get(str(check["path"]))
                if check_id == "freshness":
                    age = (datetime.now(timezone.utc) - parse_time(str(value))).total_seconds() / 60
                    result.update(value=value, age_minutes=round(age, 2), passed=0 <= age <= float(check["max_age_minutes"]))
                else:
                    allowed = check.get("allowed", [])
                    result.update(value=value, passed=value in allowed)
            elif kind == "browser":
                from playwright.sync_api import sync_playwright
                with sync_playwright() as p:
                    browser = p.chromium.launch(headless=True)
                    page = browser.new_page(viewport=check["viewport"])
                    page.goto("https://stegverse-labs.github.io/Site/autonomy-live.html", wait_until="networkidle", timeout=60000)
                    mode = page.locator("#mode").inner_text()
                    graph_text = page.locator("#graph").inner_text()
                    overflow = page.evaluate("document.documentElement.scrollWidth > document.documentElement.clientWidth")
                    result.update(mode=mode, graph_character_count=len(graph_text), horizontal_overflow=overflow, passed="TELEMETRY_UNAVAILABLE" not in mode and len(graph_text) > 40 and not overflow)
                    browser.close()
            else:
                raise ValueError(f"unsupported check type: {kind}")
        except Exception as exc:
            result["error"] = f"{type(exc).__name__}: {exc}"
        evidence.append(result)

    required = [item for item in evidence if item["required"]]
    passed = bool(required) and all(item["passed"] for item in required)
    payload = {
        "schema_version": "1.0",
        "repository": "StegVerse-Labs/Site",
        "objective_id": spec.get("objective_id"),
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "state": "PASS" if passed else "FAIL",
        "required_checks": len(required),
        "passed_required_checks": sum(1 for item in required if item["passed"]),
        "checks": evidence,
        "authority": {
            "runtime_check_pass_is_completion": False,
            "runtime_check_pass_is_release_authority": False,
            "manual_user_action_required": False
        }
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"state": payload["state"], "passed": payload["passed_required_checks"], "required": payload["required_checks"]}))
    if not passed:
        sys.exit(1)


if __name__ == "__main__":
    main()
