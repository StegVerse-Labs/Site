from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "assets" / "mir-accounting-return-v1.js"
KV_MIRROR = ROOT / "assets" / "kv-mirror-node.js"
SERVICE_WORKER = ROOT / "intr-service-worker.js"
GENERATED = ROOT / "assets" / "generated" / "site-browser-intr-connectors.js"
NODE = ROOT / "assets" / "stegverse-node-continuity-impl.js"
HANDOFF = ROOT / "docs" / "MIR_INTR_SDK_RETURN_PROFILE_MIRROR_HANDOFF.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_mir_return_uses_generic_sdk_manifest_profile_and_node_queue():
    adapter = read(ADAPTER)
    generated = read(GENERATED)
    node = read(NODE)

    # Historical evaluator connector may remain in the generated registry, but MIR
    # source identity must not select it before the SDK manifest endpoint.
    assert "evaluator-read-review" in generated
    assert "buildMaterializationRequest" in generated
    assert "queueIntrMaterializationRequest" in node

    assert "PROFILE_ID = 'sdk-manifest-ingress'" in adapter
    assert "PROFILE_NAME = 'SDK:ManifestIngress'" in adapter
    assert "REQUEST_SCHEMA = 'stegverse.sdk-manifest.interlock_request.v1'" in adapter
    assert "OPERATION = 'SUBMIT_MANIFEST'" in adapter
    assert "processing_capability: capability" in adapter
    assert "processing_route_id: routeId" in adapter
    assert "StegVerseGeneratedInTr" in adapter
    assert "StegVerseNodeContinuity" in adapter
    assert "queueIntrMaterializationRequest" in adapter
    assert "'/intr/materialization'" in adapter
    assert "'/intr/profile'" in adapter


def test_mir_source_artifact_is_exact_bound_and_semantics_are_not_rewritten():
    adapter = read(ADAPTER)
    required = (
        "MIR_RETURN_RESPONSE_TO_REQUIRED",
        "MIR_RETURN_RESPONSE_CLASS_INVALID",
        "MIR_RETURN_ARTIFACT_HASH_MISMATCH",
        "artifactBase64",
        "sourceNativeSemanticsPreserved: true",
        "authorityTransfer: false",
        "mir_historical_accounting_claimed_by_transport: false",
        "sdk_delta_evaluation_observed: false",
    )
    for marker in required:
        assert marker in adapter


def test_complete_manifest_is_required_and_preserved_on_reentry():
    adapter = read(ADAPTER)
    required = (
        "MIR_RETURN_COMPLETE_MANIFEST_REQUIRED",
        "MIR_RETURN_MANIFEST_CONTENT_HASH_MISMATCH",
        "MIR_RETURN_MANIFEST_CONTINUATION_REQUIRED",
        "MIR_RETURN_OUTBOUND_MANIFEST_STATE_MISMATCH",
        "MIR_RETURN_CONTINUATION_HASH_MISMATCH",
        "manifestContinuityVerified: true",
        "authorityNamespaceIsolation: true",
        "manifest: clone(input.manifest)",
        "manifestContinuation",
    )
    for marker in required:
        assert marker in adapter


def test_roundtrip_requires_external_ingress_and_stegverse_return_exit_receipts():
    adapter = read(ADAPTER)
    required = (
        "EXTERNAL_FRAMEWORK_INGRESS",
        "STEGVERSE_RETURN_EXIT",
        "MIR_RETURN_EXTERNAL_INGRESS_RECEIPT_REQUIRED",
        "MIR_RETURN_EXIT_RECEIPT_REQUIREMENT_MISSING",
        "buildReturnExitReceipt",
        "stegverse_return_exit_receipt",
        "roundtrip_boundary_receipts_complete: true",
        "boundary_receipts_complete = true",
    )
    for marker in required:
        assert marker in adapter


def test_mir_return_uses_write_once_trigger_and_non_authorizing_boundaries():
    adapter = read(ADAPTER)
    required = (
        "stegos.node_intr_materialization_trigger.v1",
        "STEGOS_NODE_OUTBOX",
        "request_grants_execution_authority: false",
        "claim_or_fence_minted: false",
        "NONE_TRIGGER_ONLY",
        "credential_authority: 'TV/TVC'",
        "github_token_runtime_authority: 'NONE'",
        "governance_authority_effect: 'NONE'",
        "transport_authority_effect: 'NONE'",
        "authority_namespace_effect: 'NONE'",
    )
    for marker in required:
        assert marker in adapter


def test_kv_mirror_is_preferred_custody_anchor_not_transport_prerequisite():
    adapter = read(ADAPTER)
    kv_mirror = read(KV_MIRROR)
    required = (
        "buildPreferredKvCustodyBinding",
        "StegVerseKVMirrorNode",
        "KV_MIRROR_PREFERRED_CUSTODY_UNAVAILABLE",
        "KV_MIRROR_PREFERRED_CUSTODY_BOUND",
        "kv_entry_point_required: false",
        "kv_entry_point_preferred: true",
        "event_triggered: true",
        "persistent_receiver: false",
        "always_on_application_receiver_required: false",
        "second_user_device_required: false",
        "credential_authority: 'TV/TVC'",
        "github_runtime_authority: 'NONE'",
        "live_kv_runtime_claimed: false",
        "live_provider_write_claimed: false",
        "master_records_organization_record_claimed: false",
        "final_egress_claimed: false",
        "authentic_external_mir_endpoint_claimed: false",
        "kv_mirror_preferred_custody",
    )
    for marker in required:
        assert marker in adapter

    assert "accepted_intr_profiles: ['sdk-manifest-ingress']" in kv_mirror
    assert "accepted_intr_profiles: ['evaluator-read-review', 'SDK:EvaluatorReviewIngress']" not in kv_mirror
    assert "KV_MIRROR_MUST_NOT_REQUIRE_KV_FOR_TRANSPORT" in kv_mirror


def test_device_local_ingress_fails_closed_until_generic_sdk_manifest_profile_is_advertised():
    adapter = read(ADAPTER)
    service_worker = read(SERVICE_WORKER)

    assert "BLOCKED_PROFILE_UNAVAILABLE" in adapter
    assert "profile.profiles.includes(PROFILE_NAME)" in adapter
    assert "SDK:ManifestIngress" in adapter
    # Do not fall back to the historical evaluator route merely because it is
    # advertised. Generic SDK profile publication belongs to the existing InTr
    # registry owner; until then this adapter must fail closed.
    assert "MIR_RETURN_SDK_MANIFEST_PROFILE_UNAVAILABLE" in adapter


def test_handoff_keeps_run2_choreography_and_no_second_transport():
    handoff = read(HANDOFF)
    assert "MIR emits source-native accounting artifact" in handoff
    assert "SDK:EvaluatorReviewIngress" in handoff
    assert "It does not create another route" in handoff
    assert "GitHub Actions runtime authority: NONE" in handoff


def test_mir_identity_cannot_select_evaluator_processing():
    adapter = read(ADAPTER)
    assert "RESPONSE_CLASS = 'MIR_HISTORICAL_ACCOUNTING'" in adapter
    assert "PROFILE_ID = 'sdk-manifest-ingress'" in adapter
    assert "PROFILE_ID = 'evaluator-read-review'" not in adapter
    assert "PROFILE_NAME = 'SDK:EvaluatorReviewIngress'" not in adapter
    assert "MIR_RETURN_MANIFEST_PROCESSING_REQUIRED" in adapter
    assert "processing_capability: capability" in adapter
    assert "processing_route_id: routeId" in adapter
