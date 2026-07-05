#!/usr/bin/env python3
"""Validate Ecosystem Chat & LLM route manifest and static page wiring."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ROUTE_MANIFEST = ROOT / "data" / "ecosystem-chat-routes.json"
AI_ENTRY_PAGE = ROOT / "stegverse-llm-console.html"
AI_ENTRY_DOC = ROOT / "docs" / "STEGVERSE_AI_ENTRYPOINT.md"
ROUTE_MODEL_DOC = ROOT / "docs" / "ECOSYSTEM_CHAT_BACKEND_ROUTE_MODEL.md"

REQUIRED_ROUTES = {
    "chat_answer",
    "llm_comparison",
    "ecosystem_explanation",
    "sdk_access_guidance",
    "sdk_intake_candidate",
    "governance_review",
    "runtime_status",
    "documentation_route",
    "restricted_admin",
}

REQUIRED_PAGE_MARKERS = [
    "Welcome to StegVerse AI.",
    "Route / ecosystem essentials",
    "SDK / access guidance",
    "ChatGPT comparison",
    "Claude comparison",
    "Other LLM comparison",
    "docs/ECOSYSTEM_CHAT_BACKEND_ROUTE_MODEL.md",
]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def fail(message: str) -> None:
    raise SystemExit(f"ECOSYSTEM_CHAT_ROUTES_FAIL: {message}")


def main() -> int:
    if not ROUTE_MANIFEST.exists():
        fail("missing route manifest")
    if not AI_ENTRY_PAGE.exists():
        fail("missing AI entry page")
    if not AI_ENTRY_DOC.exists():
        fail("missing AI entry doc")
    if not ROUTE_MODEL_DOC.exists():
        fail("missing backend route model doc")

    manifest = read_json(ROUTE_MANIFEST)
    routes = manifest.get("routes")
    if not isinstance(routes, list) or not routes:
        fail("routes must be a non-empty list")

    ids = {route.get("id") for route in routes if isinstance(route, dict)}
    missing = sorted(REQUIRED_ROUTES - ids)
    extra = sorted(ids - REQUIRED_ROUTES)
    if missing:
        fail("missing required routes: " + ", ".join(missing))
    if extra:
        fail("unexpected routes: " + ", ".join(extra))

    for route in routes:
        if not isinstance(route, dict):
            fail("route must be object")
        route_id = route.get("id")
        for key in ("label", "purpose", "authority_required", "execution_allowed", "comparison_allowed", "keywords"):
            if key not in route:
                fail(f"route {route_id} missing {key}")
        if not isinstance(route["keywords"], list) or not route["keywords"]:
            fail(f"route {route_id} must declare keywords")
        if route.get("execution_allowed") is not False:
            fail(f"route {route_id} must not allow execution in Site prototype")

    page = AI_ENTRY_PAGE.read_text(encoding="utf-8")
    for marker in REQUIRED_PAGE_MARKERS:
        if marker not in page:
            fail("AI entry page missing marker: " + marker)
    for route_id in REQUIRED_ROUTES:
        if route_id not in page and route_id not in {"ecosystem_explanation", "documentation_route"}:
            fail("AI entry page missing route id marker: " + route_id)

    doc = AI_ENTRY_DOC.read_text(encoding="utf-8")
    if "ECOSYSTEM_CHAT_BACKEND_ROUTE_MODEL.md" not in doc:
        fail("AI entry doc must link backend route model")

    route_doc = ROUTE_MODEL_DOC.read_text(encoding="utf-8")
    for route_id in REQUIRED_ROUTES:
        if route_id not in route_doc:
            fail("route model doc missing route id: " + route_id)

    print("ECOSYSTEM_CHAT_ROUTES_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
