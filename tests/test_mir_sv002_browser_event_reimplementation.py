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


def test_browser_activation_queues_event_then_materializes_existing_class():
    src = (ROOT / "assets/mir-roundtrip-browser-activation.js").read_text()
    assert "queueIntrMaterializationRequest(request)" in src
    assert "StegVerseMirSV002BrowserRuntime.materialize" in src
    assert "remote_host_discovery_performed:false" in src
    assert "workercoordinator_claim_required_for_event_creation:false" in src
    assert "request_grants_execution_authority:false" in src
    assert "MIR_EVENT_MATERIALIZATION_REQUEST_QUEUED" in src
    assert "consumeRetainedPacket" in src


def test_browser_runtime_is_event_ephemeral_and_canonically_custodied():
    src = (ROOT / "assets/mir-roundtrip-sv002-browser-runtime.js").read_text()
    assert "BROWSER_WEB_WORKER_ON_VALID_STEGVERSE_NODE" in src
    assert 'RUNTIME_CLASS="EVENT_EPHEMERAL"' in src
    assert "new Worker(URL.createObjectURL(new Blob([WORKER_SOURCE]" in src
    for transition in (
        "CURRENT_INTERLOCK_INTR_INGRESS_RECEIVED",
        "RTC-STEGVERSE-EGRESS-007",
        "RTC-INTERLOCK-INTR-TRANSPORT-008",
        "RTC-FARSIDE-FINAL-009",
        "MIR_DESTINATION_EVIDENCE_RETAINED",
        "EXACT_GOVERNED_RETURN_PACKET_RETAINED",
    ):
        assert transition in src
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
    assert "mir-roundtrip-sv002-browser-runtime.js" in page
    assert "canonical-master-records-transition-custody-browser.js" in page
    assert "execute_mir_event_driven_roundtrip.py" not in page
