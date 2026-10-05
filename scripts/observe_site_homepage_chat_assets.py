#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = {
    "homepage": {
        "path": "index.html",
        "url": "https://stegverse.org/",
        "markers": (
            "assets/ecosystem-chat-runtime.js?v=20261005-runtime-split-r1",
            "assets/ecosystem-chat-va-runtime.js?v=20261005-runtime-split-r1",
            "assets/ecosystem-chat-simple.js?v=20261005-runtime-split-r1",
        ),
    },
    "ecosystem_chat_runtime": {
        "path": "assets/ecosystem-chat-runtime.js",
        "url": "https://stegverse.org/assets/ecosystem-chat-runtime.js?v=20261005-runtime-split-r1",
        "markers": (
            "canonical_product_definition_sdk",
            "window.EcosystemRuntime=api",
            "isCanonicalProductDefinitionRequest",
        ),
        "forbidden_markers": (
            "window.EcosystemVARuntime=api",
            "COORDINATED_VA_RESOURCES_LLM",
        ),
    },
    "ecosystem_chat_va_runtime": {
        "path": "assets/ecosystem-chat-va-runtime.js",
        "url": "https://stegverse.org/assets/ecosystem-chat-va-runtime.js?v=20261005-runtime-split-r1",
        "markers": (
            "window.EcosystemVARuntime=api",
            "COORDINATED_VA_RESOURCES_LLM",
            "shared.executeDeviceRaw",
        ),
        "forbidden_markers": (
            "window.EcosystemRuntime=api",
            "canonical_product_definition_sdk",
            "askGeneral",
        ),
    },
    "node_continuity_impl": {
        "path": "assets/stegverse-node-continuity-impl.js",
        "url": "https://stegverse.org/assets/stegverse-node-continuity-impl.js",
        "markers": (
            "stegverse.ecosystem-chat-registered-node-observation.v1",
            "receipt_1",
            "recordEcosystemChatObservation",
        ),
    },
    "ecosystem_chat_simple": {
        "path": "assets/ecosystem-chat-simple.js",
        "url": "https://stegverse.org/assets/ecosystem-chat-simple.js",
        "markers": (
            "Export Node observation",
            "recordEcosystemChatObservation",
            "registeredNodeObservation",
        ),
    },
}

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def fetch(url: str, attempt: int) -> tuple[int, bytes]:
    sep = "&" if "?" in url else "?"
    request = urllib.request.Request(
        f"{url}{sep}site_asset_observation={attempt}&ts={int(time.time())}",
        headers={
            "Accept": "application/javascript,text/javascript,*/*;q=0.8",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "User-Agent": "StegVerse-Site-Asset-Observer/1.0",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return int(response.status), response.read()

def validate_body(name: str, body: bytes) -> dict[str, object]:
    target = TARGETS[name]
    local = (ROOT / target["path"]).read_bytes()
    text = body.decode("utf-8", "replace")
    markers = {marker: marker in text for marker in target["markers"]}
    forbidden = {marker: marker in text for marker in target.get("forbidden_markers", ())}
    return {
        "http_body_sha256": sha256(body),
        "repository_body_sha256": sha256(local),
        "exact_repository_bytes": body == local,
        "required_markers": markers,
        "required_markers_present": all(markers.values()),
        "forbidden_markers": forbidden,
        "forbidden_markers_absent": not any(forbidden.values()),
    }

def observe(output_dir: Path, attempts: int = 12, delay_seconds: int = 10) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    last_error = None
    for attempt in range(1, attempts + 1):
        try:
            results = {}
            passed = True
            for name, target in TARGETS.items():
                status, body = fetch(target["url"], attempt)
                checks = validate_body(name, body)
                results[name] = {
                    "url": target["url"],
                    "repository_path": target["path"],
                    "http_status": status,
                    **checks,
                }
                (output_dir / f"{name}.observed").write_bytes(body)
                passed = passed and status == 200 and checks["exact_repository_bytes"] and checks["required_markers_present"] and checks["forbidden_markers_absent"]
            receipt = {
                "schema": "stegverse.site-homepage-chat-public-asset-observation/v1",
                "goal_task_id": "LIVE-SITE-REGISTERED-NODE-CONVERSATION-001",
                "cosv_id": "50000000100000",
                "observed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                "attempt": attempt,
                "targets": results,
                "result": "PASS" if passed else "FAIL",
                "observation_class": "PUBLIC_ASSET_PROPAGATION_ONLY",
                "registered_node_execution_observed": False,
                "receipt_1_bound_browser_execution_observed": False,
                "authority_effect": "NONE",
                "activation_effect": False,
                "credential_requirement": "NONE",
            }
            (output_dir / "receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            if passed:
                return receipt
            last_error = f"deployed bytes did not match repository bytes on attempt {attempt}"
        except Exception as exc:
            last_error = repr(exc)
        if attempt < attempts:
            time.sleep(delay_seconds)
    receipt = {
        "schema": "stegverse.site-homepage-chat-public-asset-observation/v1",
        "goal_task_id": "SHWP-ECOSYSTEM-CHAT-INFERENCE-001",
        "cosv_id": "50000000100000",
        "observed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "result": "FAIL",
        "error": last_error,
        "observation_class": "PUBLIC_ASSET_PROPAGATION_ONLY",
        "registered_node_execution_observed": False,
        "receipt_1_bound_browser_execution_observed": False,
        "authority_effect": "NONE",
        "activation_effect": False,
        "credential_requirement": "NONE",
    }
    (output_dir / "receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return receipt

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("evidence/site-homepage-chat-public-assets"))
    parser.add_argument("--attempts", type=int, default=12)
    parser.add_argument("--delay-seconds", type=int, default=10)
    args = parser.parse_args()
    receipt = observe(args.output_dir, args.attempts, args.delay_seconds)
    print("SITE_HOMEPAGE_CHAT_PUBLIC_ASSET_OBSERVATION_" + str(receipt["result"]))
    return 0 if receipt["result"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
