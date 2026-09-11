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

    if contract.get("schema") != "stegverse.site.resident_publication_rendezvous.v2":
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

    intr = contract.get("interlock_intr_binding", {})
    if intr.get("transport_profile") != "stegverse.universal-intr.adjacent-hop/v1":
        die("unexpected Interlock/InTr transport profile")
    if intr.get("candidate_protocol_ref") != "SV-INTERLOCK-v0.4-candidate":
        die("candidate protocol reference mismatch")
    if intr.get("candidate_protocol_canonical_adoption_claimed") is not False:
        die("candidate Universal Interlock protocol prematurely claimed canonical")
    if intr.get("canonical_runtime_activation_claimed") is not False:
        die("Universal Interlock runtime activation prematurely claimed")
    for key in ("transition_admission_required", "node_mediated_transport_required"):
        if intr.get(key) is not True:
            die(f"required Interlock runtime invariant missing: {key}")
    for key in (
        "direct_kv_peer_transport_allowed",
        "direct_skap_peer_transport_allowed",
        "heartbeat_authorizing",
        "endpoint_identity_grants_authority",
        "node_identity_equals_kv_identity",
        "transport_receipt_grants_transition_authority",
        "commit_candidate_changes_canonical_state",
    ):
        if intr.get(key) is not False:
            die(f"forbidden Interlock runtime implication enabled: {key}")

    evidence = contract.get("required_exchange_evidence", {})
    required_evidence = {
        "resident_node_identity",
        "interlock_endpoint_identity",
        "exchange_id",
        "source_transition_id",
        "source_transition_parent",
        "generation",
        "fencing_identity",
        "artifact_manifest_sha256",
        "intr_admission_receipt",
        "node_transport_receipt",
        "independent_http_readback_receipt",
        "exact_path_sha256_equivalence_receipt",
        "candidate_result_receipt",
    }
    if any(evidence.get(key) is not True for key in required_evidence):
        die("required Node/Interlock exchange evidence is incomplete")

    prohibited = set(contract.get("prohibited_substitutions") or [])
    required_prohibited = {
        "RENDER",
        "VERCEL",
        "CLOUDFLARE_QUICK_TUNNEL",
        "GITHUB_ACTIONS_AS_RUNTIME",
        "DIRECT_KV_TO_KV_TRANSPORT",
        "DIRECT_SKAP_TO_SKAP_TRANSPORT",
        "HEARTBEAT_AS_EXECUTION_AUTHORITY",
        "ENDPOINT_IDENTITY_AS_AUTHORITY",
        "TRANSPORT_RECEIPT_AS_TRANSITION_AUTHORITY",
        "COMMIT_CANDIDATE_AS_CANONICAL_STATE",
        "SOURCE_OR_CI_ONLY_PUBLICATION_CLAIM",
    }
    if not required_prohibited.issubset(prohibited):
        die("required runtime substitutions are not prohibited")

    obs = contract.get("current_observation", {})
    false_observations = (
        "resident_executor_observed",
        "resident_endpoint_identity_observed",
        "exact_artifact_manifest_bound",
        "interlock_transition_admission_observed",
        "node_transport_observed",
        "independent_http_readback_observed",
        "exact_path_and_sha256_equivalence_observed",
        "candidate_result_returned_through_intr",
        "canonical_publication_transition_admitted",
        "canonical_domain_binding_observed",
        "tls_observed",
    )
    for key in false_observations:
        if obs.get(key) is not False:
            die(f"unproven resident/runtime observation claimed: {key}")
    null_evidence = (
        "resident_node_identity",
        "interlock_endpoint_identity",
        "exchange_id",
        "source_transition_id",
        "source_transition_parent",
        "generation",
        "fencing_identity",
        "artifact_manifest_sha256",
        "intr_admission_receipt",
        "node_transport_receipt",
        "independent_http_readback_receipt",
        "exact_path_sha256_equivalence_receipt",
        "candidate_result_receipt",
    )
    for key in null_evidence:
        if obs.get(key) is not None:
            die(f"unobserved exchange evidence populated: {key}")
    if obs.get("state") != "AWAITING_AUTHENTIC_RESIDENT_INTR_EXCHANGE_EVIDENCE":
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
    print("INTR_TRANSPORT_PROFILE=stegverse.universal-intr.adjacent-hop/v1")
    print("NODE_MEDIATED_TRANSPORT_REQUIRED=true")
    print("DIRECT_KV_PEER_TRANSPORT_ALLOWED=false")
    print("DIRECT_SKAP_PEER_TRANSPORT_ALLOWED=false")
    print("HEARTBEAT_AUTHORIZING=false")
    print("COMMIT_CANDIDATE_CANONICAL=false")
    print("UNIVERSAL_INTERLOCK_CANDIDATE_CANONICAL_ADOPTION=false")
    print("AUTHENTIC_RESIDENT_INTR_EXCHANGE_OBSERVED=false")


if __name__ == "__main__":
    main()
