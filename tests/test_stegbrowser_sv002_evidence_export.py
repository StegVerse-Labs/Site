from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPORTER = (ROOT / "assets" / "stegbrowser-sv002-evidence-export.js").read_text(encoding="utf-8")
PAGE = (ROOT / "stegos-bootstrap" / "canonical-work-runtime-consumption.html").read_text(encoding="utf-8")
BOOTSTRAP = (ROOT / "stegos-bootstrap" / "stegos-bootstrap-impl.js").read_text(encoding="utf-8")

NONCE = "STEG-BROWSER-MANIFEST-INTR-INGRESS-EXECUTION-001-20260915T142500Z"


def test_reuses_existing_sv002_export_component_and_registered_node_chain():
    assert 'root.StegOSWebBootstrap.exportEvidence()' in EXPORTER
    assert 'DB_NAME="stegos-node-v1"' in EXPORTER
    assert 'RECEIPTS="receipts"' in EXPORTER
    assert 'stegverse.registered-node-continuity-export/v1' in EXPORTER
    assert 'stegos.web_bootstrap_evidence_bundle.v1' in BOOTSTRAP
    assert 'function exportEvidence()' in BOOTSTRAP


def test_requires_exact_same_invocation_runtime_readiness_correlation():
    for marker in (
        NONCE,
        'stegbrowser-runtime-readiness/v1',
        'receipt_sha256=',
        'node_id=',
        'interlock_id=',
        'registration_receipt_sha256=',
        'lease_id=',
        'runtime_id=',
        'receipt.evidence_ref===expected',
        'matches.length!==1',
    ):
        assert marker in EXPORTER


def test_ephemeral_class_reused_when_device_inventory_is_not_authority():
    assert 'ephemeral_runtime_class:"ADMITTED-EPHEMERAL-STEGOS-NODE"' in EXPORTER
    assert 'list_devices' not in EXPORTER
    assert 'second_user_device' not in EXPORTER


def test_export_is_evidence_only_and_stops_before_a3():
    assert 'NONE_EVIDENCE_EXPORT_ONLY' in EXPORTER
    assert 'workercoordinator' not in EXPORTER.lower()
    assert 'claim_or_fence' not in EXPORTER.lower()
    assert 'A1_A2_EVENT_RUNTIME_READY_RETAINED_EXPORTED_A3_A4_PENDING' in PAGE
    assert '../assets/stegbrowser-sv002-evidence-export.js' in PAGE
    assert '.then(retainRuntimeReadiness).then(exportRetainedReadiness)' in PAGE
