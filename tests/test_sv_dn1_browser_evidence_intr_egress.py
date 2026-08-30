import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "stegos-node/sv-dn1-resident-observation-v3.html"
SCRIPT = ROOT / "stegos-node/sv-dn1-browser-evidence-intr-egress.js"
TARGET = ROOT / "stegos-node/sv-dn1-browser-evidence-intr-target.json"


def test_observation_page_reuses_existing_bundle_and_exposes_governed_send():
    text = PAGE.read_text(encoding="utf-8")
    assert 'id="send"' in text
    assert 'sv-dn1-browser-evidence-intr-egress.js' in text
    assert 'StegVerseSVDN1BrowserEvidenceInTrEgress.send(bundleOut)' in text
    assert 'send.disabled=false' in text
    assert 'Export evidence bundle' in text
    assert 'new_node_identity_minted:false' in text
    assert 'StegVerseNodeContinuity.registerDevice' not in text


def test_target_starts_fail_closed_without_guessed_runtime_url():
    target = json.loads(TARGET.read_text(encoding="utf-8"))
    assert target == {
        "schema": "stegos.site.sv_dn1_browser_evidence_intr_target.v1",
        "state": "AWAITING_SOVEREIGN_INTR_INGRESS",
        "ingress_url": None,
        "transport_origin": "STEGOS_WEB_BOOTSTRAP_EGRESS",
        "runtime_ingress_observed": False,
        "configuration_authority": "StegVerse sovereign runtime evidence projection",
        "credential_authority": "TV/TVC",
        "credential_requirement": "NONE",
        "github_token_runtime_authority": "NONE",
        "execution_authority": "NONE",
        "authority_effect": "NONE_DISCOVERY_ONLY",
    }


def test_egress_is_exact_uncredentialed_interlock_intr_transport():
    text = SCRIPT.read_text(encoding="utf-8")
    required = [
        'stegverse.sv-dn1.browser-observation-transport/v1',
        'stegverse.sv-dn1.browser-observation-interlock-receipt/v1',
        'stegverse.sv-dn1.browser-observation-ingress-receipt/v1',
        'SV-DN1:BrowserObservation',
        'STEGOS_WEB_BOOTSTRAP_EGRESS',
        'STEGVERSE-UNIVERSAL-INTR-TRANSPORT-001',
        'stegverse.universal-intr.adjacent-hop/v1',
        'boundary_from: "DEVICE_SYSTEM"',
        'boundary_to: "STEGOS_ECOSYSTEM"',
        'role: "SOURCE_EGRESS_INTERLOCK"',
        'credentials: "omit"',
        'sdk_admitted: false',
        'governance_decision_made: false',
        'repository_writeback_performed: false',
        'deployment_performed: false',
        'publication_decision_made: false',
        'certification_claimed: false',
    ]
    for marker in required:
        assert marker in text, marker
    for forbidden in ["Authorization", "Bearer ", "GITHUB_TOKEN", "HF_TOKEN", "registerDevice("]:
        assert forbidden not in text, forbidden


def test_ingress_receipt_validation_binds_exact_evidence_and_zero_authority():
    text = SCRIPT.read_text(encoding="utf-8")
    for marker in [
        'exact_bundle_validated: true',
        'journal_replay_validated: true',
        'source_interlock_validated: true',
        'destination_validation: "PASS"',
        'lineage_verified: true',
        'write_once_persisted: true',
        'locator_persisted: true',
        'authority_effect: "NONE_INGRESS_ONLY"',
    ]:
        assert marker in text, marker
