from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAUNCHER = ROOT / "stegos-bootstrap" / "canonical-work-runtime-consumption.js"
PAGE = ROOT / "stegos-bootstrap" / "canonical-work-runtime-consumption.html"
MATERIALIZER = ROOT / "assets" / "stegbrowser-manifest-runtime-materializer.js"
SV002 = ROOT / "assets" / "sv002-observe.js"

NONCE = "STEG-BROWSER-MANIFEST-INTR-INGRESS-EXECUTION-001-20260915T142500Z"


def test_page_loads_existing_materializer_before_launcher():
    page = PAGE.read_text(encoding="utf-8")
    assert "../assets/stegbrowser-manifest-runtime-materializer.js" in page
    assert page.index("stegbrowser-manifest-runtime-materializer.js") < page.index("canonical-work-runtime-consumption.js")
    assert 'result.state==="RUNTIME_READY_FOR_WORKERCOORDINATOR"' in page
    assert 'state.textContent="A1_A2_EVENT_RUNTIME_READY_RETAINED_A3_A4_PENDING"' in page
    assert 'state.textContent="A1_A2_INGRESS_ADMITTED_A3_A4_PENDING"' in page


def test_launcher_reuses_same_outbox_and_existing_event_runtime_after_ingress():
    text = LAUNCHER.read_text(encoding="utf-8")
    for expected in (
        NONCE,
        'ROUTE_BINDING_URL = "/data/stegbrowser-manifest-runtime-binding.v1.json"',
        'readOutboxEntry(admission.materialization_id)',
        'root.StegVerseStegBrowserManifestRuntime.materialize({',
        'state: "RUNTIME_READY_FOR_WORKERCOORDINATOR"',
        'registered_node_bound_to_invocation: true',
        'interlock_bound_to_node_and_manifest: true',
        'intr_materialization_admitted: true',
        'invocation_scoped_lease_established: true',
        'event_ephemeral_runtime_materialized: true',
        'execution_time_runtime_identity_bound: true',
        'workercoordinator_claim_pending: true',
        'workercoordinator_fence_pending: true',
        'a4_ingress_pending: true',
        'round_trip_1_started: false',
        'github_token_runtime_authority: "NONE"',
        'credential_authority: "TV/TVC"',
    ):
        assert expected in text
    assert 'startIngressOnly: start' in text
    assert 'request_mutated: false' in text
    assert 'putOutboxOnce(built.entry)' in text


def test_existing_materializer_remains_non_authorizing_and_event_ephemeral():
    text = MATERIALIZER.read_text(encoding="utf-8")
    assert 'RUNTIME_CLASS="EVENT_EPHEMERAL"' in text
    assert 'claim_or_fence_minted:false' in text
    assert 'request_grants_execution_authority:false' in text
    assert 'NONE_RUNTIME_MATERIALIZATION_ONLY' in text
    assert 'claim_or_fence_minted:true' not in text
    assert 'request_grants_execution_authority:true' not in text


def test_stegbrowser_reuses_sv002_node_journal_after_runtime_readiness():
    page = PAGE.read_text(encoding="utf-8")
    sv002 = SV002.read_text(encoding="utf-8")
    assert 'StegVerseNodeContinuity.recordStep' in sv002
    assert '../assets/stegverse-node-continuity.js' in page
    assert 'StegVerseNodeContinuity.recordStep(CAPABILITY,"runtime-ready","OBSERVED",evidenceRef)' in page
    assert 'stegbrowser-runtime-readiness/v1' in page
    for correlation in (
        'receipt_sha256=',
        'nonce=',
        'node_id=',
        'interlock_id=',
        'registration_receipt_sha256=',
        'lease_id=',
        'runtime_id=',
    ):
        assert correlation in page
    assert 'state:"RETAINED_BEFORE_A3"' in page
    assert 'authority_effect:"NONE_EVIDENCE_RETENTION_ONLY"' in page


def test_node_journal_retention_does_not_expand_a3_authority():
    page = PAGE.read_text(encoding="utf-8")
    assert 'workercoordinator_claim_pending:true' in page
    assert 'workercoordinator_fence_pending:true' in page
    assert 'claim_or_fence_minted:true' not in page
    assert 'request_grants_execution_authority:true' not in page
    assert 'new Worker(' not in page
    assert 'navigator.serviceWorker.register(' not in page
