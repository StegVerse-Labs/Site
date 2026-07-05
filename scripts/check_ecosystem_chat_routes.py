#!/usr/bin/env python3
"""Validate Ecosystem Chat & LLM route manifest, static page wiring, and backend response fixture."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ROUTE_MANIFEST = ROOT / "data" / "ecosystem-chat-routes.json"
AI_ENTRY_PAGE = ROOT / "stegverse-llm-console.html"
AI_ENTRY_ADAPTER = ROOT / "assets" / "ecosystem-ai-entry-adapter.js"
AI_ENTRY_DOC = ROOT / "docs" / "STEGVERSE_AI_ENTRYPOINT.md"
ROUTE_MODEL_DOC = ROOT / "docs" / "ECOSYSTEM_CHAT_BACKEND_ROUTE_MODEL.md"
RESPONSE_SCHEMA = ROOT / "schemas" / "ecosystem-chat-backend-response.schema.json"
RESPONSE_FIXTURE = ROOT / "fixtures" / "ecosystem-chat" / "backend-response.example.json"

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
    "assets/ecosystem-ai-entry-adapter.js",
    "window.StegVerseAIEntryAdapter.buildResponse",
]

REQUIRED_ADAPTER_MARKERS = [
    "window.StegVerseAIEntryAdapter",
    "buildResponse",
    "classifyRoute",
    "authority_issued: false",
    "receipt_id: null",
    "adapter_extension",
    "adapter_status",
    "preview_marker",
    "endpoint_marker",
    "service_marker",
    "provider_calls: false",
    "provider_authority: false",
    "capture_required_before_activation: true",
    "pure_function_preview",
    "stegverse-ai-entry-interim-backend",
]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def fail(message: str) -> None:
    raise SystemExit(f"ECOSYSTEM_CHAT_ROUTES_FAIL: {message}")


def require_path(path: Path, label: str) -> None:
    if not path.exists():
        fail(f"missing {label}")


def validate_backend_fixture(schema: dict[str, Any], fixture: dict[str, Any]) -> None:
    required = schema.get("required", [])
    for key in required:
        if key not in fixture:
            fail("backend fixture missing required key: " + key)

    route_enum = set(schema["properties"]["primary_route"]["enum"])
    if fixture.get("primary_route") not in route_enum:
        fail("backend fixture primary_route is not allowed")
    if fixture.get("primary_route") not in REQUIRED_ROUTES:
        fail("backend fixture primary_route is not in manifest routes")

    comparisons = fixture.get("comparison_outputs")
    if not isinstance(comparisons, list) or not comparisons:
        fail("backend fixture must include comparison outputs")
    for comparison in comparisons:
        if comparison.get("authority") is not False:
            fail("comparison output authority must be false")
        if not comparison.get("provider"):
            fail("comparison output provider required")

    governance = fixture.get("governance")
    if not isinstance(governance, dict):
        fail("backend fixture governance must be object")
    if governance.get("authority_issued") is not False:
        fail("backend fixture must not issue authority")
    if governance.get("receipt_id") is not None:
        fail("preview fixture receipt_id must be null")


def main() -> int:
    require_path(ROUTE_MANIFEST, "route manifest")
    require_path(AI_ENTRY_PAGE, "AI entry page")
    require_path(AI_ENTRY_ADAPTER, "AI entry browser adapter")
    require_path(AI_ENTRY_DOC, "AI entry doc")
    require_path(ROUTE_MODEL_DOC, "backend route model doc")
    require_path(RESPONSE_SCHEMA, "backend response schema")
    require_path(RESPONSE_FIXTURE, "backend response fixture")

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

    adapter = AI_ENTRY_ADAPTER.read_text(encoding="utf-8")
    for marker in REQUIRED_ADAPTER_MARKERS:
        if marker not in adapter:
            fail("AI entry adapter missing marker: " + marker)
    for route_id in REQUIRED_ROUTES:
        if route_id not in adapter:
            fail("AI entry adapter missing route id marker: " + route_id)

    doc = AI_ENTRY_DOC.read_text(encoding="utf-8")
    if "ECOSYSTEM_CHAT_BACKEND_ROUTE_MODEL.md" not in doc:
        fail("AI entry doc must link backend route model")

    route_doc = ROUTE_MODEL_DOC.read_text(encoding="utf-8")
    for route_id in REQUIRED_ROUTES:
        if route_id not in route_doc:
            fail("route model doc missing route id: " + route_id)

    schema = read_json(RESPONSE_SCHEMA)
    fixture = read_json(RESPONSE_FIXTURE)
    validate_backend_fixture(schema, fixture)

    print("ECOSYSTEM_CHAT_ROUTES_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
