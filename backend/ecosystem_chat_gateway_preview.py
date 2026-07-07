#!/usr/bin/env python3
"""Preview backend contract for the future Ecosystem Chat gateway.

This module is intentionally local and deterministic. It does not contact model
providers, remote search, repositories, or math engines. It exists so the Site
repo can validate the request and response shape before live backend activation.
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from typing import Any

INTERACTION_BANDS = ["intra", "inter", "research", "provider", "solver", "receipt"]
RESTRICTED_TERMS = ["secret", "token", "credential", "delete branch", "permission", "release", "webhook"]
ROUTES = {
    "Site": ["site", "page", "html", "mirror", "public"],
    "repo-standards": ["standard", "standards", "manifest", "maintenance"],
    "Continuity": ["continuity", "receipt", "replay", "hash", "chain"],
    "Publisher": ["publisher", "paper", "publication"],
    "Solver": ["math", "solve", "equation", "calculate", "algebra", "unit"],
}
BAND_TERMS = {
    "intra": ["site", "stegverse", "repo", "wiki", "manifest", "receipt", "standard", "transition"],
    "inter": ["adapter", "api", "provider client", "partner", "connector", "node"],
    "research": ["search", "web", "online", "latest", "current", "source", "research"],
    "provider": ["llm", "model", "provider", "token", "quota", "cost", "latency"],
    "solver": ["math", "solve", "solver", "equation", "calculate", "algebra", "proof", "unit"],
    "receipt": ["receipt", "replay", "hash", "reconstruct", "authority", "admissibility", "audit"],
}


def classify_route(message: str) -> str:
    text = message.lower()
    if any(term in text for term in RESTRICTED_TERMS):
        return "Restricted admin"
    scored = []
    for route, terms in ROUTES.items():
        scored.append((sum(1 for term in terms if term in text), route))
    score, route = sorted(scored, reverse=True)[0]
    return route if score else "Unknown"


def interaction_profile(message: str) -> dict[str, int]:
    text = message.lower()
    profile: dict[str, int] = {}
    for band in INTERACTION_BANDS:
        score = sum(1 for term in BAND_TERMS[band] if term in text)
        if band == "solver" and re.search(r"\d+\s*[+\-*/=]\s*\d+", message):
            score += 2
        profile[band] = min(100, score * 20)
    return profile


def preview_receipt_hash(payload: dict[str, Any]) -> str:
    body = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(body.encode("utf-8")).hexdigest()


def handle_preview_request(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return reject("payload must be an object", "Unknown")
    message = payload.get("message")
    if not isinstance(message, str) or not message.strip():
        return reject("message must be non-empty text", "Unknown")
    route = classify_route(message)
    profile = interaction_profile(message)
    base = {
        "routed_module": route,
        "interaction_bands": INTERACTION_BANDS,
        "interaction_profile": profile,
        "math_solver_supported": True,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    if route == "Restricted admin":
        return {
            **base,
            "response": None,
            "task_status": "pending_authority",
            "receipt_id": None,
            "next_action": "Restricted administration requires a separate governed authority path before activation.",
        }
    response_text = "\n".join([
        f"Route: {route}",
        "Task status: preview_only",
        "Authority: none; preview gateway only.",
        "Receipt: not issued by Site preview.",
        "Interaction bands: " + ",".join(f"{band}:{profile[band]}" for band in INTERACTION_BANDS),
        "Math solver: preview-supported; live checked solving requires backend activation.",
    ])
    receipt_hash = preview_receipt_hash({"message": message, "route": route, "profile": profile})
    return {
        **base,
        "response": response_text,
        "task_status": "preview_only",
        "receipt_id": None,
        "local_preview_hash": receipt_hash,
        "next_action": "Submit to the governed backend only after authority, rate limit, provider, solver, and receipt paths are installed.",
    }


def reject(reason: str, route: str) -> dict[str, Any]:
    return {
        "response": None,
        "routed_module": route,
        "task_status": "rejected",
        "receipt_id": None,
        "interaction_bands": INTERACTION_BANDS,
        "interaction_profile": {band: 0 for band in INTERACTION_BANDS},
        "math_solver_supported": True,
        "next_action": reason,
    }


def main() -> int:
    import sys

    message = " ".join(sys.argv[1:]) or "summarize Site state"
    print(json.dumps(handle_preview_request({"message": message, "session_id": "local"}), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
