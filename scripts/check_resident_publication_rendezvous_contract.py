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

    if contract.get("schema") != "stegverse.site.resident_publication_rendezvous.v3":
        die("unexpected schema")
    if contract.get("goal_id") != "SITE-497-THIRD-PARTY-DEPENDENCY-ERADICATION":
        die("goal mismatch")
    if contract.get("cosv_id") != "50000000102000":
        die("COSV mismatch")
    if contract.get("runtime_class") != "EVENT_EPHEMERAL":
        die("runtime must use canonical EVENT_EPHEMERAL class")
    if contract.get("persistent_node_identity_required") is not True:
        die("persistent Node identity/continuity must be retained")
    for key in (
        "persistent_host_required",
        "always_on_receiver_required",
        "second_user_operated_device_required",
        "hosted_provider_required",
        "hosted_provider_allowed",
        "render_allowed",
        "github_actions_runtime_allowed",
        "cloudflare_quick_tunnel_allowed",
    ):
        if contract.get(key) is not False:
            die(f"forbidden runtime/provider requirement enabled: {key}")

    runtime = contract.get("canonical_runtime_binding", {})
    if runtime.get("semantic_source") != "StegVerse-Labs/StegOS/docs/CANONICAL_RUNTIME_LANE_MIRROR_HANDOFF.md":
        die("canonical runtime semantic source mismatch")
    if runtime.get("runtime_class") != "EVENT_EPHEMERAL" or runtime.get("canonical_lane_proven") is not True:
        die("canonical EVENT_EPHEMERAL runtime lane is not bound as proven")
    if runtime.get("first_observed_lease") != "CRL-5290a1a72febbd11bb96c119":
        die("canonical runtime proof lease mismatch")
    if runtime.get("first_observed_runtime") != "WEBWORKER-9a560504aa682d2726e98ba3":
        die("canonical runtime proof identity mismatch")
    if runtime.get("persistent_host_required") is not False or runtime.get("max_operations") != 1:
        die("canonical bounded lease semantics mismatch")
    if runtime.get("public_rendezvous_for_this_publication_required") is not True:
        die("publication must require a public rendezvous observation")
    if runtime.get("public_profile_verifier") != "StegVerse-Labs/StegOS/stegos/universal_intr_public_profile.py":
        die("public profile verifier mismatch")
    if runtime.get("public_profile_observation_origin") != "INDEPENDENT_PUBLIC_HTTPS":
        die("public profile must be independently observed over HTTPS")
    if runtime.get("credential_used_for_public_observation") is not False:
        die("public observation must be credential-free")
    if runtime.get("public_observation_authority_effect") != "NONE_OBSERVATION_ONLY":
        die("public observation cannot grant authority")

    intr = contract.get("interlock_intr_binding", {})
    if intr.get("transport_profile") != "stegverse.universal-intr.adjacent-hop/v1":
        die("unexpected Interlock/InTr transport profile")
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
        "node_continuity_identity",
        "runtime_lease_id",
        "runtime_identity",
        "interlock_endpoint_identity",
        "exchange_id",
        "source_transition_id",
        "source_transition_parent",
        "generation",
        "fencing_identity",
        "artifact_manifest_sha256",
        "intr_admission_receipt",
        "node_transport_receipt",
        "public_profile_sha256",
        "independent_http_readback_receipt",
        "exact_path_sha256_equivalence_receipt",
        "candidate_result_receipt",
        "lease_closure_receipt",
    }
    if any(evidence.get(key) is not True for key in required_evidence):
        die("required EVENT_EPHEMERAL Node/InTr exchange evidence is incomplete")

    prohibited = set(contract.get("prohibited_substitutions") or [])
    required_prohibited = {
        "RENDER",
        "VERCEL",
        "CLOUDFLARE_QUICK_TUNNEL",
        "GITHUB_ACTIONS_AS_RUNTIME",
        "PERSISTENT_HOST_AS_REQUIRED_RUNTIME",
        "ALWAYS_ON_RECEIVER_AS_REQUIRED_RUNTIME",
        "SECOND_USER_OPERATED_DEVICE_AS_REQUIRED_RUNTIME",
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
        "event_ephemeral_execution_observed",
        "node_continuity_identity_observed",
        "runtime_identity_observed",
        "interlock_endpoint_identity_observed",
        "independent_public_profile_observed",
        "exact_artifact_manifest_bound",
        "interlock_transition_admission_observed",
        "node_transport_observed",
        "independent_http_readback_observed",
        "exact_path_and_sha256_equivalence_observed",
        "candidate_result_returned_through_intr",
        "lease_closed_after_evidence_export",
        "canonical_publication_transition_admitted",
        "canonical_domain_binding_observed",
        "tls_observed",
    )
    for key in false_observations:
        if obs.get(key) is not False:
            die(f"unproven runtime/publication observation claimed: {key}")
    null_evidence = (
        "node_continuity_identity",
        "runtime_lease_id",
        "runtime_identity",
        "interlock_endpoint_identity",
        "exchange_id",
        "source_transition_id",
        "source_transition_parent",
        "generation",
        "fencing_identity",
        "artifact_manifest_sha256",
        "intr_admission_receipt",
        "node_transport_receipt",
        "public_profile_sha256",
        "independent_http_readback_receipt",
        "exact_path_sha256_equivalence_receipt",
        "candidate_result_receipt",
        "lease_closure_receipt",
    )
    for key in null_evidence:
        if obs.get(key) is not None:
            die(f"unobserved exchange evidence populated: {key}")
    if obs.get("state") != "AWAITING_AUTHENTIC_EVENT_EPHEMERAL_PUBLICATION_EXCHANGE":
        die("unexpected current observation state")

    pub_policy = pub.get("provider_selection", {})
    if pub_policy.get("hosted_origin_allowed") is not False or pub_policy.get("render_allowed") is not False:
        die("publication-equivalence policy permits hosted/Render origin")
    if pub_policy.get("resident_rendezvous_contract") != "data/resident-publication-rendezvous-contract.json":
        die("publication-equivalence contract does not bind this runtime contract")
    if selection.get("selected_origin") is not None or selection.get("selection_state") != "NO_HOSTED_ORIGIN_SELECTED":
        die("hosted origin remains selected")
    if "RENDER" not in selection.get("prohibited_providers_for_this_lane", []):
        die("Render is not explicitly prohibited")

    print("RESIDENT_PUBLICATION_RENDEZVOUS_CONTRACT=PASS")
    print("RUNTIME_CLASS=EVENT_EPHEMERAL")
    print("PERSISTENT_NODE_IDENTITY_REQUIRED=true")
    print("PERSISTENT_HOST_REQUIRED=false")
    print("ALWAYS_ON_RECEIVER_REQUIRED=false")
    print("SECOND_USER_OPERATED_DEVICE_REQUIRED=false")
    print("PUBLIC_PROFILE_OBSERVATION_ORIGIN=INDEPENDENT_PUBLIC_HTTPS")
    print("INTR_TRANSPORT_PROFILE=stegverse.universal-intr.adjacent-hop/v1")
    print("NODE_MEDIATED_TRANSPORT_REQUIRED=true")
    print("DIRECT_KV_PEER_TRANSPORT_ALLOWED=false")
    print("DIRECT_SKAP_PEER_TRANSPORT_ALLOWED=false")
    print("HEARTBEAT_AUTHORIZING=false")
    print("COMMIT_CANDIDATE_CANONICAL=false")
    print("AUTHENTIC_EVENT_EPHEMERAL_PUBLICATION_EXCHANGE_OBSERVED=false")


if __name__ == "__main__":
    main()
