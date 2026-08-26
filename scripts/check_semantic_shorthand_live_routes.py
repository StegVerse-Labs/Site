#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import socket
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "semantic-shorthand-live-verification.json"
BASE = os.environ.get("STEGVERSE_SEMANTIC_PUBLIC_BASE", "https://stegverse.org").rstrip("/")

TARGETS = {
    "ecosystem-chat.html": (
        "assets/semantic-command-router.js",
        "assets/ecosystem-chat-semantic-commands.js",
        "assets/ecosystem-chat-simple.js",
    ),
    "assets/semantic-command-router.js": (
        "disability:{",
        "VA disability topics",
        "commit_intent:false",
        "authority_effect:false",
        "activation_effect:false",
    ),
    "assets/ecosystem-chat-semantic-commands.js": (
        "resolve(value,'ECOSYSTEM_CHAT')",
        "semantic_command=/",
        "provider_call=false",
    ),
    "va-claims-chat.html": (
        "assets/va-claims-chat-runtime.js",
    ),
    "assets/va-claims-chat-runtime.js": (
        "interceptSemanticCommand",
        "resolve(q,'VA_CLAIMS_CHAT')",
        "No intent was inferred and no action was taken.",
    ),
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fetch(url: str) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "StegVerse-Semantic-Shorthand-Live-Verification/1.0",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            body = response.read()
            return {
                "requested_url": url,
                "final_url": response.geturl(),
                "http_status": response.status,
                "content_type": response.headers.get("Content-Type", ""),
                "reachable": True,
                "body": body,
                "error": None,
            }
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, socket.timeout, OSError) as exc:
        code = getattr(exc, "code", None)
        return {
            "requested_url": url,
            "final_url": None,
            "http_status": code,
            "content_type": None,
            "reachable": code is not None,
            "body": b"",
            "error": f"{type(exc).__name__}: {exc}",
        }


def public_observation(item: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in item.items() if key != "body"}


def main() -> int:
    observations: list[dict[str, Any]] = []
    blockers: list[str] = []

    for relative, markers in TARGETS.items():
        local_path = ROOT / relative
        if not local_path.is_file():
            blockers.append(f"local_missing:{relative}")
            continue

        local_bytes = local_path.read_bytes()
        url = f"{BASE}/{relative}"
        result = fetch(url)
        body = result["body"]
        text = body.decode("utf-8", errors="replace")
        result.update(
            {
                "relative_path": relative,
                "observed_at": now(),
                "local_sha256": sha256(local_bytes),
                "remote_sha256": sha256(body) if body else None,
                "exact_source_match": bool(body) and body == local_bytes,
                "markers": {marker: marker in text for marker in markers},
            }
        )

        if not result["reachable"]:
            blockers.append(f"network_unresolved:{relative}:{result['error']}")
        elif result["http_status"] != 200:
            blockers.append(f"http_status:{relative}:{result['http_status']}")
        elif not result["exact_source_match"]:
            blockers.append(f"source_mismatch:{relative}")
        else:
            missing = [marker for marker, present in result["markers"].items() if not present]
            if missing:
                blockers.append(f"markers_missing:{relative}:{','.join(missing)}")

        observations.append(public_observation(result))

    eco = next((x for x in observations if x.get("relative_path") == "ecosystem-chat.html"), None)
    ordering_pass = False
    if eco and eco.get("exact_source_match"):
        live_html = (ROOT / "ecosystem-chat.html").read_text(encoding="utf-8")
        router_pos = live_html.find('<script src="assets/semantic-command-router.js"></script>')
        bridge_pos = live_html.find('<script src="assets/ecosystem-chat-semantic-commands.js"></script>')
        chat_pos = live_html.find('<script src="assets/ecosystem-chat-simple.js"></script>')
        ordering_pass = min(router_pos, bridge_pos, chat_pos) >= 0 and router_pos < bridge_pos < chat_pos
        if not ordering_pass:
            blockers.append("ecosystem_script_order_invalid")

    passed = not blockers and len(observations) == len(TARGETS)
    payload = {
        "schema_version": "1.0.0",
        "receipt_type": "semantic_shorthand_live_verification",
        "generated_at": now(),
        "public_base": BASE,
        "state": "VERIFIED_PUBLIC_SOURCE" if passed else "BLOCKED",
        "passed": passed,
        "observations": observations,
        "ecosystem_script_order_verified": ordering_pass,
        "deterministic_command_behavior_validation": "SEPARATE_CANONICAL_NODE_TEST",
        "browser_interaction_execution_observed": False,
        "provider_call_required": False,
        "credential_required": False,
        "authority_effect": False,
        "activation_effect": False,
        "blockers": blockers,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    if passed:
        print("SEMANTIC_SHORTHAND_LIVE_VERIFICATION=PASS")
        print(f"public_base={BASE}")
        print("exact_public_source_match=true")
        print("browser_interaction_execution_observed=false")
        print("authority_effect=false")
        return 0

    print("SEMANTIC_SHORTHAND_LIVE_VERIFICATION=BLOCKED")
    for blocker in blockers:
        print(f"- {blocker}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
