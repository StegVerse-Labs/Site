from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "assets" / "mir-accounting-return-v1.js"
SERVICE_WORKER = ROOT / "intr-service-worker.js"
GENERATED = ROOT / "assets" / "generated" / "site-browser-intr-connectors.js"
NODE = ROOT / "assets" / "stegverse-node-continuity-impl.js"
HANDOFF = ROOT / "docs" / "MIR_INTR_SDK_RETURN_PROFILE_MIRROR_HANDOFF.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_mir_return_reuses_canonical_evaluator_profile_and_node_queue():
    adapter = read(ADAPTER)
    generated = read(GENERATED)
    node = read(NODE)

    assert "evaluator-read-review" in generated
    assert "SDK:EvaluatorReviewIngress" in generated
    assert "stegverse.evaluator_review.interlock_request.v1" in generated
    assert "buildMaterializationRequest" in generated
    assert "queueIntrMaterializationRequest" in node

    assert "PROFILE_ID = 'evaluator-read-review'" in adapter
    assert "PROFILE_NAME = 'SDK:EvaluatorReviewIngress'" in adapter
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
    )
    for marker in required:
        assert marker in adapter


def test_device_local_ingress_must_advertise_sdk_evaluator_profile_before_activation():
    adapter = read(ADAPTER)
    service_worker = read(SERVICE_WORKER)

    assert "BLOCKED_PROFILE_UNAVAILABLE" in adapter
    assert "profile.profiles.includes(PROFILE_NAME)" in adapter

    # This is the activation gate for the implementation: the existing root-scoped
    # Universal InTr runtime, not a second listener, must advertise this profile.
    assert '"SDK:EvaluatorReviewIngress"' in service_worker, (
        "device-local /intr/profile does not yet advertise SDK:EvaluatorReviewIngress"
    )


def test_handoff_keeps_run2_choreography_and_no_second_transport():
    handoff = read(HANDOFF)
    assert "MIR emits source-native accounting artifact" in handoff
    assert "SDK:EvaluatorReviewIngress" in handoff
    assert "It does not create another route" in handoff
    assert "GitHub Actions runtime authority: NONE" in handoff
