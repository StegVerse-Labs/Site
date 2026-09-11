#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data" / "resident-publication-rendezvous-contract.json"
PUB = ROOT / "data" / "publication-equivalence-contract.json"
SELECTION = ROOT / "data" / "publication-origin-selection-2026-09-09.json"


def die(message: str) -> None:
    raise SystemExit("RESIDENT_PUBLICATION_RENDEZVOUS_FAIL: " + message)


def main() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    pub = json.loads(PUB.read_text(encoding="utf-8"))
    selection = json.loads(SELECTION.read_text(encoding="utf-8"))

    if contract.get("schema") != "stegverse.site.resident_publication_rendezvous.v1":
        die("unexpected schema")
    if contract.get("goal_id") != "SITE-497-THIRD-PARTY-DEPENDENCY-ERADICATION":
        die("goal mismatch")
    if contract.get("cosv_id") != "50000000102000":
        die("COSV mismatch")
    if contract.get("runtime_class") != "RESIDENT_STEGVERSE":
        die("runtime must be resident StegVerse")
    for key in ("hosted_provider_required", "hosted_provider_allowed", "render_allowed", "github_actions_runtime_allowed", "cloudflare_quick_tunnel_allowed"):
        if contract.get(key) is not False:
            die(f"forbidden runtime/provider path enabled: {key}")

    prohibited = set(contract.get("prohibited_substitutions") or [])
    required = {"RENDER", "VERCEL", "CLOUDFLARE_QUICK_TUNNEL", "GITHUB_ACTIONS_AS_RUNTIME", "SOURCE_OR_CI_ONLY_PUBLICATION_CLAIM"}
    if not required.issubset(prohibited):
        die("required hosted/runtime substitutions are not prohibited")

    obs = contract.get("current_observation", {})
    for key in ("resident_executor_observed", "resident_endpoint_identity_observed", "exact_artifact_manifest_bound", "independent_http_readback_observed", "exact_path_and_sha256_equivalence_observed", "canonical_domain_binding_observed", "tls_observed"):
        if obs.get(key) is not False:
            die(f"unproven resident/public observation claimed: {key}")
    if obs.get("state") != "AWAITING_AUTHENTIC_RESIDENT_RENDEZVOUS_EVIDENCE":
        die("unexpected current observation state")

    pub_policy = pub.get("provider_selection", {})
    if pub_policy.get("hosted_origin_allowed") is not False or pub_policy.get("render_allowed") is not False:
        die("publication-equivalence policy permits hosted/Render origin")
    if pub_policy.get("resident_rendezvous_contract") != "data/resident-publication-rendezvous-contract.json":
        die("publication-equivalence contract does not bind this resident contract")
    if selection.get("selected_origin") is not None or selection.get("selection_state") != "NO_HOSTED_ORIGIN_SELECTED":
        die("hosted origin remains selected")
    if "RENDER" not in selection.get("prohibited_providers_for_this_lane", []):
        die("Render is not explicitly prohibited")

    print("RESIDENT_PUBLICATION_RENDEZVOUS_CONTRACT=PASS")
    print("RUNTIME_CLASS=RESIDENT_STEGVERSE")
    print("HOSTED_PROVIDER_ALLOWED=false")
    print("RENDER_ALLOWED=false")
    print("AUTHENTIC_RESIDENT_RENDEZVOUS_OBSERVED=false")


if __name__ == "__main__":
    main()
