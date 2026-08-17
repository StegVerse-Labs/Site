#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "heartbeat-transition" / "index.html"
JS = ROOT / "heartbeat-transition" / "heartbeat-transition.js"
HANDOFF = ROOT / "docs" / "IPHONE_HEARTBEAT_TRANSITION_PROJECTION_MIRROR_HANDOFF.md"


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def require_markers(text: str, label: str, markers: tuple[str, ...], failures: list[str]) -> None:
    for marker in markers:
        require(marker in text, f"{label} missing marker: {marker}", failures)


def forbid_markers(text: str, label: str, markers: tuple[str, ...], failures: list[str]) -> None:
    for marker in markers:
        require(marker not in text, f"{label} contains prohibited marker: {marker}", failures)


def main() -> int:
    failures: list[str] = []
    for path in (HTML, JS, HANDOFF):
        require(path.is_file(), f"missing projection file: {path.relative_to(ROOT)}", failures)
    if failures:
        for failure in failures:
            print(f"IPHONE_HB30_PROJECTION_FAIL:{failure}")
        return 1

    html = HTML.read_text(encoding="utf-8")
    js = JS.read_text(encoding="utf-8")
    handoff = HANDOFF.read_text(encoding="utf-8")

    require_markers(html, "html", (
        "HB29 → HB30 transition capsule",
        "SHWP-IPHONE-HB30-TRANSITION-CAPSULE-001",
        "HB29 / generation 29",
        "HB30 / generation 30",
        "TV/TVC",
        "Generate portable HB30 receipt",
        "./heartbeat-transition.js",
        "independently verified",
        "WorkerCoordinator",
    ), failures)

    require_markers(js, "javascript", (
        "https://stegverse.org",
        "SHWP-IPHONE-HB30-TRANSITION-CAPSULE-001",
        "d18d57d83cf19b7799cde1a1b4487e496eca7f76",
        "stegverse.iphone-heartbeat-transition-receipt/v1",
        "CURRENT_USER_IPHONE",
        "StegVerse-Labs/.github",
        "control/heartbeat-state.json",
        "stegverse.heartbeat-carrier-runtime-state/v1",
        "heartbeat_epoch:30",
        "credential_authority: 'TV/TVC'",
        "credential_requirement: 'NONE'",
        "github_token_runtime_authority: 'NONE'",
        "non_tv_tvc_secret_or_token_used: false",
        "worker_authority: false",
        "claim_or_fence_mutation: false",
        "route_authority: false",
        "wallet_authority: false",
        "model_output_authority: 'NONE'",
        "hosted_runtime_production_authority: 'NONE'",
        "another_physical_machine_required: false",
        "navigator.userAgent.includes('iPhone')",
        "window.isSecureContext !== true",
        "crypto.subtle.digest('SHA-256'",
        "localStorage.setItem(STORAGE_KEY",
        "receipt.receipt_sha256 = await sha256Hex(canonicalize(receipt))",
    ), failures)

    # The public capsule is physical evidence generation only. It must not
    # perform network/API/runtime/wallet/credential operations.
    forbid_markers(js, "javascript", (
        "fetch(",
        "XMLHttpRequest",
        "WebSocket",
        "EventSource",
        "Authorization",
        "Bearer ",
        "GITHUB_TOKEN",
        "GH_TOKEN",
        "TVC_TOKEN",
        "private_key",
        "seed_phrase",
        "eth_sendTransaction",
        "eth_sendRawTransaction",
        "personal_sign",
        "window.ethereum",
        "github.com/api",
        "api.github.com",
        "RENDER",
    ), failures)

    require("epoch: 29" in js and "generation: 29" in js, "seed must remain exactly HB29/generation29", failures)
    require("epoch: 30" in js and "generation: 30" in js, "successor must remain exactly HB30/generation30", failures)
    require("location.origin !== EXPECTED_ORIGIN" in js, "origin must fail closed before receipt generation", failures)
    require("generateButton.disabled = false" in js, "valid physical environment must explicitly enable generation", failures)

    require_markers(handoff, "handoff", (
        "SITE-IPHONE-HB30-TRANSITION-PROJECTION-001",
        "StegVerse-Labs/Site#358",
        "StegVerse-Labs/.github#209",
        "SHWP-DURABLE-RUNTIME-ACTIVATION / G18",
        "credential_authority: TV/TVC",
        "github_token_runtime_authority: NONE",
        "non_tv_tvc_secret_or_token_allowed: false",
        "Publication alone is not HB30 activation",
        "physical iPhone receipt",
        "independent WorkerCoordinator",
    ), failures)

    if failures:
        for failure in failures:
            print(f"IPHONE_HB30_PROJECTION_FAIL:{failure}")
        return 1

    print("IPHONE_HB30_PROJECTION_PASS surface=stegverse.org/heartbeat-transition authority_effect=NONE credential_authority=TV/TVC github_token_runtime_authority=NONE physical_activation_claimed=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
