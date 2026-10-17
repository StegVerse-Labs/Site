from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
LAUNCHER = ROOT / "assets" / "kv-entrypoint-intr-launcher.js"
CLAIM = ROOT / "data" / "session-work-claims.d" / "site-kv-entrypoint-intr-launcher-20260914.json"
HANDOFF = ROOT / "docs" / "KV_ENTRYPOINT_INTR_LAUNCHER_MIRROR_HANDOFF.md"


def test_entrypoint_my_kv_is_governed_launcher_not_plain_direct_link():
    html = INDEX.read_text(encoding="utf-8")
    assert 'id="kv-entry-launcher"' in html
    assert '<a href="my-kv.html">My KV</a>' not in html
    assert 'id="kv-entry-launch-status"' in html
    required = [
        "assets/stegverse-node-continuity.js",
        "assets/generated/site-browser-intr-connectors.js",
        "assets/hb-intr-carrier.js",
        "stegos-node/device-kv-intr-sync.js",
        "assets/my-kv-device-kv-query-bridge.js",
        "assets/kv-entrypoint-intr-launcher.js",
    ]
    positions = [html.index(marker) for marker in required]
    assert positions == sorted(positions)


def test_launcher_reuses_existing_kv_interlock_intr_bridge_and_is_device_class_neutral():
    text = LAUNCHER.read_text(encoding="utf-8")
    for marker in (
        "StegVerseKVInstallationStatusBridge",
        'EXPECTED_BRIDGE_KIND="DEVICE_KV_QUERY_RETURN"',
        'interlock_request_schema:"kv.interlock.request.v1"',
        'protocol:"InTr"',
        'boundary:"KV",subsystem:"KnowledgeVault:Interlock"',
        'credential_authority:"TV/TVC"',
        'device_class_requirement:"NONE"',
        'github_token_runtime_authority:"NONE"',
        'authority_effect:"NONE"',
        'root.location.assign(destination.href)',
    ):
        assert marker in text
    assert "iPhone" not in text
    assert "navigator.serviceWorker.register" not in text
    assert "fetch(" not in text


def test_launcher_requires_governed_projection_before_navigation():
    text = LAUNCHER.read_text(encoding="utf-8")
    assert 'EXPECTED_PROJECTION_SCHEMA="stegverse.kv.installation-status-projection/v1"' in text
    assert "KV_INSTALLATION_VERIFIED:true" in text
    assert "KV_INSTALLATION_NOT_VERIFIED:true" in text
    assert "KV_RELATIONSHIP_NOT_ESTABLISHED:true" in text
    assert 'projection.credential_material_present===false' in text
    assert 'projection.provider_operation_authorized===false' in text
    assert 'projection.authority_effect==="NONE"' in text
    assert "getInstallationStatus()).then(validateProjection).then" in text


def test_coordination_claim_and_handoff_bind_same_goal():
    claim = CLAIM.read_text(encoding="utf-8")
    handoff = HANDOFF.read_text(encoding="utf-8")
    for text in (claim, handoff):
        assert "STEG-BROWSER-RUNTIME-CONSUMPTION-001" in text
    # The COSV is bound in the handoff. The claim never carried it (not at bc6981f9 either), and since #1469 the
    # claim is a released historical record of a retired goal whose COSV must not be reused for new claims.
    assert "COSV: `40000100100000`" in handoff
    assert '"state": "RELEASED_COMPLETE"' in claim
    assert '"historical_goal_state": "RETIRED"' in claim
    assert "SITE-KV-ENTRYPOINT-INTR-LAUNCHER-20260914" in claim
    assert "KnowledgeVault:Interlock" in handoff
    assert "device-specific" in handoff
