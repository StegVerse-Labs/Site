from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SYNC = ROOT / "stegos-node/stegbrowser-intr-sync.js"
LAUNCHER = ROOT / "stegos-bootstrap/canonical-work-runtime-consumption.js"
PAGE = ROOT / "stegos-bootstrap/canonical-work-runtime-consumption.html"
TARGET = ROOT / "stegos-node/stegbrowser-intr-sync-target.json"


def test_browser_builder_matches_canonical_universal_intr_request_contract():
    text = SYNC.read_text(encoding="utf-8")
    required = [
        'schema: TRANSPORT_SCHEMA',
        'protocol: "InTr"',
        'operation_id: operationId',
        'packet_id: packetId',
        'boundary_path: ["DEVICE_SYSTEM", "STEGOS_ECOSYSTEM"]',
        'event_triggered: true',
        'always_on_receiver_required: false',
        'second_user_device_required: false',
        'receiver_unavailable_disposition: "DURABLE_QUEUE_OR_EVENT_EPHEMERAL_MATERIALIZATION"',
        'exact_packet_transport_retry_allowed: true',
        'blind_consequence_retry_allowed: false',
        'interlock_required: true',
        'transport_schema: TRANSPORT_SCHEMA',
        'transport_protocol: "InTr"',
        'authority_transfer: false',
        'request_grants_execution_authority: false',
        'transport_grants_execution_authority: false',
        'credential_authority: "TV/TVC"',
        'github_token_runtime_authority: "NONE"',
        '"INTR-MAT-" + materializationBasisHash.slice(0, 24)',
        '"opaque://stegbrowser-manifest-invocation/" + payloadHash.slice(7)',
    ]
    for marker in required:
        assert marker in text, marker


def test_same_outbox_entry_is_reused_for_local_runtime_and_sovereign_delivery():
    launcher = LAUNCHER.read_text(encoding="utf-8")
    assert "StegVerseStegBrowserInTrSync.buildCanonicalEntry(registration, binding)" in launcher
    assert "retainedEntry = entry;" in launcher
    assert "StegVerseStegBrowserInTrSync.postEntry(retainedEntry)" in launcher
    assert 'state: "RUNTIME_READY_FOR_WORKERCOORDINATOR"' in launcher
    assert "round_trip_1_started: false" in launcher


def test_sync_is_transport_only_and_fail_closed_without_projected_target():
    text = SYNC.read_text(encoding="utf-8")
    target = TARGET.read_text(encoding="utf-8")
    assert 'method: "POST"' in text
    assert 'X-StegVerse-Transport": "InTr"' in text
    assert 'credentials: "omit"' in text
    assert 'claim_or_fence_minted: false' in text
    assert 'authority_effect: "NONE"' in text
    assert '"state": "AWAITING_SOVEREIGN_INTR_INGRESS"' in target
    assert '"ingress_url": null' in target


def test_page_loads_transport_adapter_before_runtime_launcher():
    page = PAGE.read_text(encoding="utf-8")
    adapter = '../stegos-node/stegbrowser-intr-sync.js'
    launcher = './canonical-work-runtime-consumption.js'
    assert adapter in page
    assert page.index(adapter) < page.index(launcher)


if __name__ == "__main__":
    test_browser_builder_matches_canonical_universal_intr_request_contract()
    test_same_outbox_entry_is_reused_for_local_runtime_and_sovereign_delivery()
    test_sync_is_transport_only_and_fail_closed_without_projected_target()
    test_page_loads_transport_adapter_before_runtime_launcher()
    print("STEGBROWSER_CANONICAL_SOVEREIGN_INGRESS_RETENTION_PASS")
