from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_stegos_node_projection_contract() -> None:
    index = (ROOT / "stegos-node" / "index.html").read_text(encoding="utf-8")
    js = (ROOT / "stegos-node" / "stegos-node.js").read_text(encoding="utf-8")
    sw = (ROOT / "stegos-node" / "service-worker.js").read_text(encoding="utf-8")

    assert 'id="register-device"' in index
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
