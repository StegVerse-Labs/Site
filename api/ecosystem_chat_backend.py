#!/usr/bin/env python3
"""Deterministic local backend scaffold for the StegVerse AI entry point.

This module is intentionally fixture-first and non-networked. It consumes the
same route manifest used by the Site prototype and emits the backend response
shape documented for future live handlers.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ROUTE_MANIFEST = ROOT / "data" / "ecosystem-chat-routes.json"

PROVIDERS = ("ChatGPT", "Claude", "Other LLM")


def stable_response_id(message: str, route_id: str) -> str:
    digest = hashlib.sha256(f"{route_id}\n{message}".encode("utf-8")).hexdigest()[:16]
    return f"preview-{route_id}-{digest}"


def read_manifest() -> dict[str, Any]:
    return json.loads(ROUTE_MANIFEST.read_text(encoding="utf-8"))


def classify_route(message: str, manifest: dict[str, Any] | None = None) -> dict[str, Any]:
    manifest = manifest or read_manifest()
    lower = message.lower()
    for route in manifest.get("routes", []):
        for keyword in route.get("keywords", []):
            if keyword.lower() in lower:
                return route
    default_route = manifest.get("default_route", "chat_answer")
    for route in manifest.get("routes", []):
        if route.get("id") == default_route:
            return route
    raise ValueError(f"default route not found: {default_route}")


def build_response(message: str) -> dict[str, Any]:
    manifest = read_manifest()
    route = classify_route(message, manifest)
    route_id = str(route["id"])
    label = str(route["label"])
    clean_message = message.strip()

    if not clean_message:
        return {
            "response_id": "welcome",
            "primary_route": "chat_answer",
            "stegverse_response": (
                "Welcome to StegVerse AI. I can help answer questions, explain StegVerse concepts, "
                "route ecosystem requests, describe SDK access, compare external LLM responses, and "
                "prepare governed transition candidates with clear authority and receipt boundaries."
            ),
            "route_guidance": "Enter a request to classify the route.",
            "sdk_guidance": "SDK and access guidance appears when relevant.",
            "comparison_outputs": [
                {"provider": provider, "authority": False, "response": "Comparison unavailable in local scaffold."}
                for provider in PROVIDERS
            ],
            "governance": {
                "governed_candidate": False,
                "authority_issued": False,
                "receipt_id": None,
                "reconstruction_available": False,
            },
        }

    sdk_guidance = (
        "SDK route selected: explain SDK entry points, permissions, manifests, receipts, and next steps. "
        "Do not expose credentials or imply access has been granted."
        if route_id.startswith("sdk")
        else "No SDK-specific route was selected. Ask about SDK access, API onboarding, manifests, or intake packets to open this path."
    )

    return {
        "response_id": stable_response_id(clean_message, route_id),
        "primary_route": route_id,
        "stegverse_response": (
            f"StegVerse treats this as one entry-point request. Selected route: {label} ({route_id}). "
            "A live backend would preserve the original request, apply governed route handling, check authority requirements, "
            "and return bounded output with receipt/reconstruction metadata when available."
        ),
        "route_guidance": (
            f"Route preview: {label}. {route.get('purpose', '')} "
            f"authority_required={route.get('authority_required')} execution_allowed={route.get('execution_allowed')}"
        ),
        "sdk_guidance": sdk_guidance,
        "comparison_outputs": [
            {"provider": provider, "authority": False, "response": "Comparison placeholder pending provider adapter activation."}
            for provider in PROVIDERS
        ],
        "governance": {
            "governed_candidate": True,
            "authority_issued": False,
            "receipt_id": None,
            "reconstruction_available": False,
        },
    }


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("message", nargs="*", help="Message to route")
    args = parser.parse_args()
    message = " ".join(args.message)
    print(json.dumps(build_response(message), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
