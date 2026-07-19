#!/usr/bin/env python3
"""Execute Site autonomy runtime checks and persist fail-closed evidence."""
from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "data/autonomy/runtime-checks.json"
OUT = ROOT / "data/autonomy/runtime-verification-evidence.json"
LIVE = ROOT / "data/autonomy/live-status.json"


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def write(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def fetch(url: str, accept: str, attempts: int = 3) -> tuple[int, str, str, int]:
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        request = Request(url, headers={"Accept": accept, "User-Agent": "StegVerse-Site-Runtime-Verifier/1.2"})
        try:
            with urlopen(request, timeout=30) as response:
                return response.status, response.headers.get("content-type", ""), response.read().decode("utf-8"), attempt
        except (HTTPError, URLError, TimeoutError) as exc:
            last_error = exc
            if attempt < attempts:
                time.sleep(attempt * 2)
    raise RuntimeError(f"request failed after {attempts} attempts: {last_error}")


def parse_time(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamp must include a timezone")
    return parsed


def bind_live_status(payload: dict[str, Any]) -> None:
    live = load(LIVE)
    generated_at = str(payload["generated_at"])
    failed_ids = list(payload.get("failed_required_check_ids", []))
    state = str(payload.get("state", "FAIL"))
    graph = live.setdefault("task_graph", {})
    nodes = graph.setdefault("nodes", [])
    nodes = [node for node in nodes if node.get("id") != "site-runtime-verification"]
    nodes.append({
        "id": "site-runtime-verification",
        "title": "Verify public autonomy runtime",
        "status": "COMPLETE" if state == "PASS" else "BLOCKED_BY_RUNTIME_EVIDENCE",
        "result": (
            f"All {payload['required_checks']} required runtime checks passed."
            if state == "PASS"
            else f"{payload['passed_required_checks']} of {payload['required_checks']} required runtime checks passed; failed: {', '.join(failed_ids)}."
        ),
        "owner": "StegVerse-Labs/Site",
        "updated_at": generated_at,
        "depends_on": ["site-runtime-check-spec"],
        "evidence_path": "data/autonomy/runtime-verification-evidence.json",
    })
    graph["nodes"] = nodes
    edges = graph.setdefault("edges", [])
    edge = {"from": "site-runtime-check-spec", "to": "site-runtime-verification", "type": "sequence"}
    if not any(all(item.get(key) == value for key, value in edge.items()) for item in edges):
        edges.append(edge)

    corrective = [item for item in live.setdefault("corrective_actions", []) if item.get("id") != "site-runtime-verification-failure"]
    if state != "PASS":
        corrective.append({
            "id": "site-runtime-verification-failure",
            "action": "Repair failed public autonomy runtime checks and rerun automatically",
            "status": "AUTOMATIC_REPAIR_REQUIRED",
            "reason": f"Failed required checks: {', '.join(failed_ids)}",
            "evidence_path": "data/autonomy/runtime-verification-evidence.json",
        })
    live["corrective_actions"] = corrective
    live["runtime_verification"] = {
        "state": state,
        "generated_at": generated_at,
        "required_checks": payload["required_checks"],
        "passed_required_checks": payload["passed_required_checks"],
        "failed_required_check_ids": failed_ids,
        "evidence_path": "data/autonomy/runtime-verification-evidence.json",
        "completion_effect": "NONE_OUTSIDE_RUNTIME_PHASE",
    }
    live["generated_at"] = generated_at
    write(LIVE, live)


def main() -> None:
    spec = load(SPEC)
    checks = spec.get("checks", [])
    if spec.get("schema_version") != "1.1" or not isinstance(checks, list) or not checks:
        raise ValueError("runtime check specification is invalid")

    evidence: list[dict[str, Any]] = []
    telemetry: dict[str, Any] | None = None

    for check in checks:
        check_id = str(check.get("id"))
        result: dict[str, Any] = {
            "id": check_id,
            "type": check.get("type"),
            "required": bool(check.get("required", False)),
            "passed": False,
        }
        try:
            kind = check.get("type")
            if kind == "http-json":
                status, content_type, body, attempts = fetch(str(check["url"]), "application/json")
                telemetry = json.loads(body)
                result.update(url=check["url"], status_code=status, content_type=content_type, attempts=attempts, passed=status == 200 and isinstance(telemetry, dict))
            elif kind == "http-html":
                status, content_type, body, attempts = fetch(str(check["url"]), "text/html")
                result.update(url=check["url"], status_code=status, content_type=content_type, attempts=attempts, body_character_count=len(body), passed=status == 200 and "<html" in body.lower() and len(body) > 500)
            elif kind == "json-field":
                if telemetry is None:
                    raise RuntimeError("telemetry JSON was not loaded")
                value = telemetry.get(str(check["path"]))
                if check_id == "freshness":
                    age = (datetime.now(timezone.utc) - parse_time(str(value))).total_seconds() / 60
                    result.update(value=value, age_minutes=round(age, 2), passed=0 <= age <= float(check["max_age_minutes"]))
                else:
                    allowed = check.get("allowed", [])
                    result.update(value=value, allowed=allowed, passed=value in allowed)
            elif kind == "browser":
                from playwright.sync_api import sync_playwright
                with sync_playwright() as playwright:
                    browser = playwright.chromium.launch(headless=True)
                    page = browser.new_page(viewport=check["viewport"])
                    console_errors: list[str] = []
                    page.on("console", lambda message: console_errors.append(message.text) if message.type == "error" else None)
                    response = page.goto(str(check["url"]), wait_until="networkidle", timeout=60000)
                    selector = str(check["ready_selector"])
                    page.locator(selector).wait_for(state="visible", timeout=30000)
                    text = page.locator(selector).inner_text()
                    mode_text = page.locator("#mode").inner_text() if page.locator("#mode").count() else ""
                    overflow = page.evaluate("document.documentElement.scrollWidth > document.documentElement.clientWidth")
                    minimum = int(check.get("minimum_text_characters", 40))
                    result.update(url=check["url"], status_code=response.status if response else None, selector=selector, text_character_count=len(text), horizontal_overflow=overflow, mode=mode_text, console_errors=console_errors, passed=bool(response and response.ok and len(text) >= minimum and not overflow and "TELEMETRY_UNAVAILABLE" not in mode_text and not console_errors))
                    browser.close()
            else:
                raise ValueError(f"unsupported check type: {kind}")
        except Exception as exc:
            result["error"] = f"{type(exc).__name__}: {exc}"
        evidence.append(result)

    required = [item for item in evidence if item["required"]]
    passed = bool(required) and all(item["passed"] for item in required)
    failed_ids = [item["id"] for item in required if not item["passed"]]
    payload = {
        "schema_version": "1.2",
        "repository": "StegVerse-Labs/Site",
        "objective_id": spec.get("objective_id"),
        "specification_path": str(SPEC.relative_to(ROOT)),
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "state": "PASS" if passed else "FAIL",
        "required_checks": len(required),
        "passed_required_checks": sum(1 for item in required if item["passed"]),
        "failed_required_check_ids": failed_ids,
        "checks": evidence,
        "authority": {
            "runtime_check_pass_is_completion": False,
            "runtime_check_pass_is_release_authority": False,
            "runtime_check_pass_is_admissibility_authority": False,
            "manual_user_action_required": False,
        },
    }
    write(OUT, payload)
    bind_live_status(payload)
    print(json.dumps({"state": payload["state"], "passed": payload["passed_required_checks"], "required": payload["required_checks"], "failed": failed_ids}))
    if not passed:
        sys.exit(1)


if __name__ == "__main__":
    main()
