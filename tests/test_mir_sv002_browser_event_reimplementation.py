from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def test_mir_binding_preserves_sv002_initiation_invariants():
    binding = json.loads((ROOT / "data/mir-roundtrip-browser-runtime-binding.v1.json").read_text())
    init = binding["initiation"]
    assert init["event_is_trigger"] is True
    assert init["idle_runtime_required"] is False
    assert init["remote_host_discovery_allowed"] is False
    assert init["workercoordinator_claim_required_for_event_creation"] is False
    assert init["claim_or_fence_minted"] is False
    assert init["request_grants_execution_authority"] is False
    assert binding["runtime_class"] == "EVENT_EPHEMERAL"
    assert binding["runtime_substrate"] == "BROWSER_WEB_WORKER_ON_VALID_STEGVERSE_NODE"
    custody = binding["canonical_custody"]
    assert custody["authoritative_endpoint"] == "/api/master-records/state-transitions"
    assert custody["master_records_owner"] == "master-records/orchestration"
    assert custody["local_browser_storage_role"] == "SUBORDINATE_CONTINUITY_ONLY"
    assert custody["browser_may_self_issue_custody_receipt"] is False
    assert custody["browser_secret_plaintext_allowed"] is False
    assert custody["endpoint_resolution"] == "VERIFIED_STEGVERSE_NODE_ADVERTISEMENT"
    assert custody["browser_credential_material_required"] is False
    assert custody["gateway_transport_authority"] == "NONE"


def test_browser_activation_queues_then_requires_authoritative_custody_and_current_intr_admission_before_runtime():
    src = (ROOT / "assets/mir-roundtrip-browser-activation.js").read_text()
    queue_call = "queueIntrMaterializationRequest(request)"
    first_custody = 'custody.record("MIR_EVENT_MATERIALIZATION_REQUEST_QUEUED"'
    admit_call = "synchronizeMaterialization(queued.materialization_id)"
    ingress_custody = 'custody.record("CURRENT_INTERLOCK_INTR_INGRESS_RECEIVED"'
    runtime_call = "var oneWay=await root.StegVerseMirSV002BrowserRuntime.materialize({"
    assert queue_call in src
    assert first_custody in src
    assert "StegVerseMirRoundTripInTrSync.synchronizeMaterialization" in src
    assert admit_call in src
    assert ingress_custody in src
    assert runtime_call in src
    assert src.index(queue_call) < src.index(first_custody) < src.index(admit_call) < src.index(ingress_custody) < src.index(runtime_call)
    assert "endpoint:b.canonical_custody.authoritative_endpoint" in src
    assert 'transport_schema:"stegverse.universal-intr-transport/v1"' in src
    assert 'transport_protocol:"InTr"' in src
    assert 'second_user_device_required:false' in src
    assert 'receiver_unavailable_disposition:"DURABLE_QUEUE_OR_EVENT_EPHEMERAL_MATERIALIZATION"' in src
    assert "remote_host_discovery_performed:false" in src
    assert "workercoordinator_claim_required_for_event_creation:false" in src
    assert "request_grants_execution_authority:false" in src
    assert "consumeRetainedPacket" in src


def test_mir_intr_sync_posts_exact_registered_node_outbox_trigger():
    src = (ROOT / "stegos-node/mir-roundtrip-intr-sync.js").read_text()
    assert 'TRIGGER_SCHEMA = "stegos.node_intr_materialization_trigger.v1"' in src
    assert 'OUTBOX_SCHEMA = "stegos.node_intr_outbox_entry.v1"' in src
    assert 'INGRESS_SCHEMA = "stegverse.mir-roundtrip-intr-materialization-ingress/v1"' in src
    assert 'fetch("/intr/materialization"' in src
    assert 'state !== "INGRESS_ADMITTED"' in src
    assert 'current_device_ingress_observed: true' in src
    assert 'authority_effect: "NONE_INGRESS_ONLY"' in src


def test_root_intr_service_worker_admits_mir_without_second_runtime():
    root_sw = (ROOT / "intr-service-worker.js").read_text()
    ext = (ROOT / "intr-mir-roundtrip-extension.js").read_text()
    assert 'importScripts("/intr-mir-roundtrip-extension.js")' in root_sw
    assert 'subsystem: "MIR:MirrorRoundTrip"' in ext
    assert 'DOWNSTREAM_OWNER = "MIR-ROUNDTRIP-EGRESS-AUTHENTICITY-001"' in ext
    assert 'request_grants_execution_authority === false' in ext
    assert 'transport_grants_execution_authority === false' in ext
    assert 'claim_or_fence_minted === false' in ext
    assert 'runtime_surface: "CURRENT_USER_IPHONE_SERVICE_WORKER"' in ext


def test_browser_runtime_is_event_ephemeral_and_requires_admitted_ingress():
    src = (ROOT / "assets/mir-roundtrip-sv002-browser-runtime.js").read_text()
    assert "BROWSER_WEB_WORKER_ON_VALID_STEGVERSE_NODE" in src
    assert 'RUNTIME_CLASS="EVENT_EPHEMERAL"' in src
    assert "new Worker(URL.createObjectURL(new Blob([WORKER_SOURCE]" in src
    assert "authentic_intr_ingress_required" in src
    assert 'ingress.schema==="stegverse.mir-roundtrip-intr-materialization-ingress/v1"' in src
    assert 'ingress.state==="INGRESS_ADMITTED"' in src
    for transition in (
        "RTC-STEGVERSE-EGRESS-007",
        "RTC-INTERLOCK-INTR-TRANSPORT-008",
        "RTC-FARSIDE-FINAL-009",
        "MIR_DESTINATION_EVIDENCE_RETAINED",
        "EXACT_GOVERNED_RETURN_PACKET_RETAINED",
    ):
        assert transition in src
    assert "CURRENT_INTERLOCK_INTR_INGRESS_RECEIVED" not in src
    assert "canonical_master_records_browser_custody_unavailable" in src


def test_canonical_browser_custody_writes_authoritative_master_records_before_local_cache():
    src = (ROOT / "assets/canonical-master-records-transition-custody-browser.js").read_text()
    assert "stegverse.canonical-state-transition-receipt/v1" in src
    assert "stegverse.master-records.state-transition-submission/v1" in src
    assert 'fetch(endpoint,{method:"POST"' in src
    assert 'resolveAuthoritativeEndpoint' in src
    assert 'stegbrowser_master_records_state_transition_endpoint' in src
    assert 'endpoint_resolution:"VERIFIED_STEGVERSE_NODE_ADVERTISEMENT"' in src
    assert 'credentials:"omit"' in src
    assert 'credentials:"include"' not in src
    assert '"X-StegVerse-Credential-Authority"' not in src
    assert '"Authorization"' not in src
    assert 'browser_credential_material_required:false' in src
    assert "authoritative_master_records_not_recorded" in src
    assert "authoritative_master_records_reconstruction_not_pass" in src
    assert "authoritative_master_records_digest_mismatch" in src
    assert 'await cacheAuthoritative(receipt,mr)' in src
    assert src.index("var response=await fetch(endpoint") < src.index("await cacheAuthoritative(receipt,mr)")
    assert 'cache_role:"SUBORDINATE_CONTINUITY_ONLY"' in src
    assert 'browser_may_self_issue_custody_receipt:false' in src
    assert 'authoritative_owner:"master-records/orchestration"' in src
    assert 'state:"RECORDED"' not in src


def test_page_autostarts_browser_event_without_remote_host_connector():
    page = (ROOT / "mir-roundtrip/index.html").read_text()
    assert "StegVerseMirRoundTripBrowserActivation.execute()" in page
    assert 'setTimeout(run,0)' in page
    assert "mir-roundtrip-intr-sync.js" in page
    assert "mir-roundtrip-sv002-browser-runtime.js" in page
    assert "canonical-master-records-transition-custody-browser.js" in page
    assert "execute_mir_event_driven_roundtrip.py" not in page


def test_browser_custody_carries_and_requires_required_evidence_validation():
    src = (ROOT / "assets/canonical-master-records-transition-custody-browser.js").read_text()
    assert "required_evidence_manifest" in src
    assert "TRANSITION_EVIDENCE" in src
    assert "origin_transition_id" in src
    assert 'mr.required_evidence_validation_status==="PASS"' in src
    assert "authoritative_master_records_required_evidence_not_pass" in src


def test_browser_activation_carries_exact_node_outbox_entry_as_required_evidence():
    src = (ROOT / "assets/mir-roundtrip-browser-activation.js").read_text()
    assert '"MIR_EVENT_MATERIALIZATION_REQUEST_QUEUED:node-outbox-entry"' in src
    assert '"MIR_NODE_OUTBOX_ENTRY"' in src
    assert "required_evidence_manifest:[queuedEvidence]" in src
