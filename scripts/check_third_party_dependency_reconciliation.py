#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CUTOVER = ROOT / "data" / "third-party-runtime-cutover-current.json"
RECON = ROOT / "data" / "third-party-dependency-reconciliation-2026-09-09.json"


def die(message: str) -> None:
    raise SystemExit(f"THIRD_PARTY_DEPENDENCY_RECONCILIATION_FAIL: {message}")


def main() -> None:
    current = json.loads(CUTOVER.read_text(encoding="utf-8"))
    recon = json.loads(RECON.read_text(encoding="utf-8"))

    if current.get("canonical_runtime") != "RESIDENT_STEGVERSE":
        die("cutover does not declare resident canonical runtime")
    if recon.get("canonical_runtime") != current.get("canonical_runtime"):
        die("reconciliation/cutover canonical runtime mismatch")

    for key in (
        "production_continuity_third_party_dependency",
        "activation_third_party_dependency",
        "automatic_third_party_runtime_selection",
    ):
        if current.get(key) is not False or recon.get(key) is not False:
            die(f"{key} must be false in current and reconciled state")

    states = current.get("provider_states", {})
    hosts = states.get("third_party_hosts", {})
    if hosts.get("required") is not False or hosts.get("role") != "RETIRED_FROM_RUNTIME_SELECTION":
        die("third-party hosts are not retired from runtime selection")

    tunnels = states.get("third_party_tunnels", {})
    if tunnels.get("required") is not False or tunnels.get("canonical_runtime_carrier") is not False:
        die("third-party tunnels remain required or canonical")

    hosted_ci = states.get("hosted_ci_runtime", {})
    if hosted_ci.get("required") is not False:
        die("hosted CI remains a required runtime")
    if hosted_ci.get("runtime_authority") != "NONE":
        die("hosted CI runtime authority must be NONE")
    if hosted_ci.get("role") != "READ_ONLY_VALIDATION_FALLBACK_ONLY":
        die("hosted CI role must be read-only validation fallback")

    print("THIRD_PARTY_DEPENDENCY_RECONCILIATION_PASS")
    print("CURRENT_PROVIDER_IDENTITIES_REQUIRED=false")
    print("THIRD_PARTY_HOST_RUNTIME_SELECTION=RETIRED")
    print("THIRD_PARTY_TUNNEL_RUNTIME_SELECTION=RETIRED")
    print("HOSTED_CI_RUNTIME_AUTHORITY=NONE")
    print("STEGGATE_CANONICAL_RUNTIME=RESIDENT_STEGVERSE")


if __name__ == "__main__":
    main()
