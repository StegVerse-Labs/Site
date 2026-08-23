from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_stegos_node_projection_contract() -> None:
    index = (ROOT / "stegos-node" / "index.html").read_text(encoding="utf-8")
    js = (ROOT / "stegos-node" / "stegos-node.js").read_text(encoding="utf-8")
    sw = (ROOT / "stegos-node" / "service-worker.js").read_text(encoding="utf-8")

    assert index.count('id="register-device"') == 1
    assert "Register Device" in index
    assert "Last StegOS Network Sync" in index
    assert "Last Personal KV Sync" in index
    assert "Local Receipt Head" in index
    assert "Device History" in index

    for marker in (
        'stegos.node_handoff_receipt.v1',
        'receipt_number: 1',
        'transition: "NODE_REGISTERED"',
        'prior_state: "UNREGISTERED"',
        'resulting_state: "REGISTERED"',
        'continuity_parent: "GENESIS"',
        'credential_authority: "TV/TVC"',
        'hardware_attestation_claimed: false',
        'last_personal_kv_sync',
        'last_stegos_network_sync',
        'section_views_are_filtered_projections: true',
        'competing_logs_allowed: false',
        'current_network_required: false',
    ):
        assert marker in js

    for marker in ("navigator.userAgent", "serialNumber", "GITHUB_TOKEN", "RENDER_API"):
        assert marker not in js

    assert './index.html' in sw
    assert './stegos-node.js' in sw
    assert './manifest.webmanifest' in sw


def test_live_observer_is_exact_https_and_non_authorizing() -> None:
    observer = (ROOT / "scripts" / "check_stegos_node_projection.py").read_text(encoding="utf-8")
    assert '--live-url' in observer
    assert 'parsed.scheme != "https"' in observer
    assert 'urljoin(base_url, "stegos-node.js")' in observer
    assert 'urljoin(base_url, "service-worker.js")' in observer
    assert 'urljoin(base_url, "manifest.webmanifest")' in observer
    assert 'AUTHORITY_EFFECT=NONE' in observer
    assert 'PHYSICAL_NODE_ACTIVATION_CLAIMED=false' in observer
    assert 'STEGOS_NODE_PUBLIC_OBSERVATION_PASS' in observer


def test_node_evidence_export_is_bounded_and_non_authorizing() -> None:
    index = (ROOT / "stegos-node" / "index.html").read_text(encoding="utf-8")
    assert 'id="export-node-evidence"' in index
    assert 'stegos.node_physical_evidence_export.v1' in index
    assert 'window.StegOSNodeProjection.historyProjection()' in index
    assert 'raw_registration_random_bytes_included: false' in index
    assert 'hardware_attestation_claimed: false' in index
    assert 'physical_activation_claimed: false' in index
    assert 'authority_effect: "NONE"' in index
    assert 'credential_authority: "TV/TVC"' in index
    assert 'heartbeat_authority: "StegVerse-Labs/.github"' in index
    assert 'Receipt #1 is required before evidence export' in index
    assert 'new Blob' in index
    assert 'link.download = "stegos-node-evidence-"' in index
