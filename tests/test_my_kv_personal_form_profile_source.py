"""My KV personal-form-profile source contract.

Every assertion below is unchanged from the original file. They were written
as bare module-level statements, which meant any one of them failing raised
during import rather than failing a test -- and a raise during import aborts
collection for the whole repository, not just this file. Grouping them into
test functions keeps each assertion exactly as written while letting a drifted
marker be reported as the single failing test it is.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / "my-kv.html").read_text(encoding="utf-8")
sw = (ROOT / "intr-service-worker.js").read_text(encoding="utf-8")
sync = (ROOT / "stegos-node/device-kv-intr-sync.js").read_text(encoding="utf-8")
bridge = (ROOT / "assets/my-kv-personal-form-profile-write-bridge.js").read_text(encoding="utf-8")


def test_personal_form_profile_surface_declared_in_my_kv():
    assert "_Entities/Self/Personal_Form_Profile.json" in html
    assert "SKAP e-signature reference" in html


def test_root_intr_worker_declares_personal_form_profile_contract():
    assert "PERSONAL_FORM_PROFILE" in sw
    assert "PERSONAL_FORM_PROFILE_REPLACE" in sw
    assert "personal-form-profile-update-response/v1" in sw
    assert "exact_readback_verified:true" in sw


def test_auto_signing_is_forbidden():
    assert "personal_form_profile_auto_sign_forbidden" in sw
    assert "signature.auto_apply===false" in sw


def test_device_kv_sync_and_write_bridge_contract():
    assert '"PERSONAL_FORM_PROFILE":true' in sync
    assert 'record_class:RECORD_CLASS' in bridge
    assert 'authority_effect:"NONE_RESULT_LOOKUP_ONLY"' in bridge


def test_my_kv_records_profile_steps_and_readback():
    assert 'recordStep("my-kv-personal-form-profile",step,state,evidenceRef||null)' in html
    assert '"PROFILE_PERSISTED"' in html
    assert '"PROFILE_READ"' in html
    assert "post-write readback hash mismatch" in html
    assert "loadProfileDetailed" in bridge


def test_write_bridge_retains_exact_response_evidence():
    assert "response_receipt_hash" in bridge
    assert "exact_response_packet_recovered" in bridge
    assert "response_transported_on_hb_derived_carrier" in bridge
    assert 'return "response="+receipt+";profile="+profileHash' in html


def test_personal_kv_sync_observation_is_exact_and_fail_closed():
    assert 'typeof node.recordPersonalKvSync!=="function"' in html
    assert 'profile_class:"PERSONAL_FORM_PROFILE"' in html
    assert 'resulting_state:state' in html
    assert 'exact_readback_verified:true' in html
