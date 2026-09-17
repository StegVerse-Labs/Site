from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCER = (ROOT / "assets" / "stegbrowser-master-records-custody.js").read_text(encoding="utf-8")
EXTENSION = (ROOT / "intr-stegbrowser-master-records-custody-extension.js").read_text(encoding="utf-8")
ROOT_WORKER = (ROOT / "intr-service-worker.js").read_text(encoding="utf-8")
BASE_WORKER = (ROOT / "intr-service-worker-base-v1.js").read_text(encoding="utf-8")
PAGE = (ROOT / "stegos-bootstrap" / "canonical-work-runtime-consumption.html").read_text(encoding="utf-8")

NONCE = "STEG-BROWSER-MANIFEST-INTR-INGRESS-EXECUTION-001-20260915T142500Z"
SV001_SHA = "sha256:81a078eeeacffb8fc86d287d7aaa8a9904c6f53973471dad7f6d7c3fa6818a35"


def test_reuses_existing_registered_node_and_root_intr_path():
    for marker in (
        'NODE_DB="stegos-node-v1"',
        'OUTBOX="intr_outbox"',
        'STEGVERSE_INTR_LOCAL_TRIGGER',
        'stegos.node_intr_outbox_entry.v1',
        'stegos.node_intr_materialization_trigger.v1',
        'stegverse.universal-intr-materialization-request/v1',
    ):
        assert marker in PRODUCER
    assert 'importScripts("/intr-stegbrowser-master-records-custody-extension.js")' in ROOT_WORKER
    assert 'new Worker(' not in PRODUCER
    assert 'serviceWorker.register' not in PRODUCER


def test_stegbrowser_custody_identity_is_distinct_from_sv001_identity():
    for marker in (
        'stegverse.master-records.stegbrowser-readiness-custody-transition-request/v1',
        'stegverse.master-records.stegbrowser-readiness-custody-intr-admission/v1',
        'STEGBROWSER_RUNTIME_READINESS_MASTER_RECORDS_CUSTODY',
        'STEG-BROWSER-RUNTIME-CONNECTION-INGRESS-001',
        'StegBrowser:RuntimeReadinessCustody',
        NONCE,
    ):
        assert marker in EXTENSION or marker in PRODUCER
    assert 'SV001_MASTER_RECORDS_CUSTODY_AND_RECONSTRUCTION' not in EXTENSION
    assert 'MR-STEGVERSE001-BOUNDED-AUTONOMY-001' not in EXTENSION
    assert SV001_SHA not in EXTENSION


def test_sv001_handler_remains_specific_and_unchanged_in_authority_identity():
    for marker in (
        'MR_SV001_TRANSITION="SV001_MASTER_RECORDS_CUSTODY_AND_RECONSTRUCTION"',
        'MR_SV001_TASK="MR-STEGVERSE001-BOUNDED-AUTONOMY-001"',
        'MR_SV001_CANONICAL_SOURCE_SHA="' + SV001_SHA + '"',
        'stegverse.master-records.sv001-custody-intr-admission/v1',
    ):
        assert marker in BASE_WORKER


def test_exact_runtime_readiness_tuple_is_bound_and_reconstructable_at_admission():
    for marker in (
        'stegbrowser-runtime-readiness/v1',
        'runtime_readiness_receipt_sha256',
        'readiness_node_receipt_sha256',
        'invocation_request_nonce',
        'node_id',
        'interlock_id',
        'registration_receipt_sha256',
        'lease_id',
        'runtime_id',
        'exported_bundle_sha256',
    ):
        assert marker in PRODUCER
        assert marker in EXTENSION
    assert NONCE in PRODUCER
    assert NONCE in EXTENSION


def test_admission_does_not_claim_master_records_custody_or_workercoordinator():
    for marker in (
        'master_records_custody_observed:false',
        'master_records_reconstruction_observed:false',
        'workercoordinator_claim_observed:false',
        'workercoordinator_fence_observed:false',
        'authority_effect:"NONE_INGRESS_ONLY"',
    ):
        assert marker in PRODUCER or marker in EXTENSION
    assert 'INGRESS_ADMITTED_CUSTODY_RECONSTRUCTION_PENDING' in PRODUCER
    assert 'CUSTODY_RECONSTRUCTION_PENDING_A3_A4_PENDING' in PAGE


def test_ephemeral_runtime_class_survives_empty_connector_inventory():
    assert 'ephemeral_runtime_class:"ADMITTED-EPHEMERAL-STEGOS-NODE"' in PRODUCER
    assert 'list_devices' not in PRODUCER
    assert 'list_devices' not in EXTENSION


def test_page_orders_custody_after_sv002_export_and_before_a3():
    assert '../assets/stegbrowser-master-records-custody.js' in PAGE
    assert '../assets/canonical-master-records-transition-custody-browser.js' in PAGE
    assert '.then(retainRuntimeReadiness).then(exportRetainedReadiness).then(bindMasterRecordsCustody).then(submitCanonicalMasterRecordsReconstruction)' in PAGE
    assert 'WorkerCoordinator' not in PRODUCER


def test_reuses_canonical_master_records_authoritative_custody_contract():
    for marker in (
        'StegVerseCanonicalMasterRecordsBrowserCustody.Custody',
        'endpoint:"/api/master-records/state-transitions"',
        'STEGBROWSER_RUNTIME_READINESS_MASTER_RECORDS_CUSTODY',
        'RECORDED_RECONSTRUCTED_BEFORE_A3',
        'mr.state!=="RECORDED"',
        'mr.reconstruction_status!=="PASS"',
        'mr.receipt_sha256!==mr.reconstructed_receipt_sha256',
        'authority_effect:"NONE_CUSTODY_RECONSTRUCTION_ONLY"',
        'outcome:"OBSERVED"',
    ):
        assert marker in PAGE
    for tuple_field in (
        'runtime_readiness_receipt_sha256',
        'readiness_node_receipt_sha256',
        'invocation_request_nonce',
        'node_id',
        'interlock_id',
        'registration_receipt_sha256',
        'lease_id',
        'runtime_id',
        'exported_bundle_sha256',
    ):
        assert tuple_field in PAGE


def test_authoritative_master_records_reconstruction_still_stops_before_a3():
    assert 'A1_A2_MASTER_RECORDS_RECONSTRUCTED_A3_A4_PENDING' in PAGE
    assert 'workercoordinator_claim_pending:true' in PAGE
    assert 'workercoordinator_fence_pending:true' in PAGE


def test_provider_neutral_authoritative_endpoint_binding_keeps_credentials_out_of_browser():
    client = (ROOT / "assets" / "canonical-master-records-transition-custody-browser.js").read_text(encoding="utf-8")
    for marker in (
        'ADVERTISEMENT_PATH="/api/stegverse-node"',
        'stegbrowser_master_records_state_transition_endpoint',
        'VERIFIED_STEGVERSE_NODE_ADVERTISEMENT',
        'query:master_records_gateway',
        'persisted_local_configuration',
        'loopback_fallback',
        'browser_credential_material_required:false',
        'credential_authority:"TV/TVC"',
        'credentials:"omit"',
    ):
        assert marker in client
    assert 'credentials:"include"' not in client
    assert '"Authorization"' not in client
    assert '"X-StegVerse-Credential-Authority"' not in client
    assert 'outcome:"INGRESS_ADMITTED"' not in PAGE
    assert 'outcome:"OBSERVED"' in PAGE
    assert NONCE in PAGE
