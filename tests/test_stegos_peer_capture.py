from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_one_action_peer_capture_preserves_existing_node_and_export_contracts() -> None:
    index = (ROOT / "stegos-node" / "index.html").read_text(encoding="utf-8")

    assert index.count('id="register-device"') == 1
    assert index.count('id="export-node-evidence"') == 1
    assert index.count('id="capture-peer-evidence"') == 1
    assert "Register &amp; Export Evidence" in index

    # Combined flow must reuse the canonical Node API rather than invent identity.
    assert "window.StegOSNodeProjection.registerDevice()" in index
    assert "window.StegOSNodeProjection.validateGenesis" in index
    assert "window.StegOSNodeProjection.historyProjection()" in index
    assert "Receipt #1 is required before evidence export" in index

    # The one-action path emits the same bounded physical export schema.
    for marker in (
        'schema: "stegos.node_physical_evidence_export.v1"',
        'raw_registration_random_bytes_included: false',
        'hardware_attestation_claimed: false',
        'credential_authority: "TV/TVC"',
        'heartbeat_authority: "StegVerse-Labs/.github"',
        'authority_effect: "NONE"',
        'physical_activation_claimed: false',
        'network_activation_claimed: false',
        'link.download = "stegos-node-evidence-"',
    ):
        assert marker in index

    # Site must not self-admit the export as a distinct peer or Network presence.
    assert "StegOS—not this page—decides whether it is a genuinely distinct peer" in index
    assert "distinct_peer: true" not in index
    assert "network_presence_established: true" not in index
    assert "runtime_activation_claimed: true" not in index

    # Protected identity/authority material remains excluded.
    for marker in ("navigator.userAgent", "serialNumber", "GITHUB_TOKEN", "RENDER_API", "private_signing_key"):
        assert marker not in index
