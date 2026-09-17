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


def test_browser_activation_queues_then_requires_current_intr_admission_before_runtime():
    src = (ROOT / "assets/mir-roundtrip-browser-activation.js").read_text()
    queue_call = "queueIntrMaterializationRequest(request)"
    admit_call = "synchronizeMaterialization(queued.materialization_id)"
    runtime_call = "var oneWay=await root.StegVerseMirSV002BrowserRuntime.materialize({"
    assert queue_call in src
    assert "StegVerseMirRoundTripInTrSync.synchronizeMaterialization" in src
    assert admit_call in src
    assert runtime_call in src
    assert "CURRENT_INTERLOCK_INTR_INGRESS_RECEIVED" in src
    assert src.index(queue_call) < src.index(admit_call) < src.index(runtime_call)
    assert 'transport_schema:"stegverse.universal-intr-transport/v1"' in src
    assert 'transport_protocol:"InTr"' in src
    assert 'second_user_device_required:false' in src
    assert 'receiver_unavailable_disposition:"DURABLE_QUEUE_OR_EVENT_EPHEMERAL_MATERIALIZATION"' in src
    assert "remote_host_discovery_performed:false" in src
    assert "workercoordinator_claim_required_for_event_creation:false" in src
    assert "request_grants_execution_authority:false" in src
    assert "MIR_EVENT_MATERIALIZATION_REQUEST_QUEUED" in src
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


def test_canonical_browser_master_records_is_not_test_probe():
    src = (ROOT / "assets/canonical-master-records-transition-custody-browser.js").read_text()
    assert "stegverse.canonical-state-transition-receipt/v1" in src
    assert "master-records/orchestration" in src
    assert "reconstruction_status:\"PASS\"" in src
    assert "master_records_grants_transition_authority:false" in src
    assert "master_records_grants_execution_authority:false" in src


def test_page_autostarts_browser_event_without_remote_host_connector():
    page = (ROOT / "mir-roundtrip/index.html").read_text()
    assert "StegVerseMirRoundTripBrowserActivation.execute()" in page
    assert 'setTimeout(run,0)' in page
    assert "mir-roundtrip-intr-sync.js" in page
    assert "mir-roundtrip-sv002-browser-runtime.js" in page
    assert "canonical-master-records-transition-custody-browser.js" in page
    assert "execute_mir_event_driven_roundtrip.py" not in page
