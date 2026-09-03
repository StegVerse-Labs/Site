from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
html=(ROOT/"my-kv.html").read_text(encoding="utf-8")
sw=(ROOT/"intr-service-worker.js").read_text(encoding="utf-8")
sync=(ROOT/"stegos-node/device-kv-intr-sync.js").read_text(encoding="utf-8")
bridge=(ROOT/"assets/my-kv-personal-form-profile-write-bridge.js").read_text(encoding="utf-8")

assert "_Entities/Self/Personal_Form_Profile.json" in html
assert "SKAP e-signature reference" in html
assert "PERSONAL_FORM_PROFILE" in sw
assert "PERSONAL_FORM_PROFILE_REPLACE" in sw
assert "personal-form-profile-update-response/v1" in sw
assert "exact_readback_verified:true" in sw
assert '"PERSONAL_FORM_PROFILE":true' in sync
assert 'record_class:RECORD_CLASS' in bridge
assert 'authority_effect:"NONE_RESULT_LOOKUP_ONLY"' in bridge
assert "personal_form_profile_auto_sign_forbidden" in sw\nassert "signature.auto_apply===false" in sw
print("MY_KV_PERSONAL_FORM_PROFILE_SOURCE_PASS")

assert 'recordStep("my-kv-personal-form-profile",step,state,evidenceRef||null)' in html
assert '"PROFILE_PERSISTED"' in html
assert '"PROFILE_READ"' in html
assert "post-write readback hash mismatch" in html
assert "loadProfileDetailed" in (ROOT/"assets/my-kv-personal-form-profile-write-bridge.js").read_text(encoding="utf-8")

bridge_text=(ROOT/"assets/my-kv-personal-form-profile-write-bridge.js").read_text(encoding="utf-8")
assert "response_receipt_hash" in bridge_text
assert "exact_response_packet_recovered" in bridge_text
assert "response_transported_on_hb_derived_carrier" in bridge_text
assert 'return "response="+receipt+";profile="+profileHash' in html

assert 'typeof node.recordPersonalKvSync!=="function"' in html
assert 'profile_class:"PERSONAL_FORM_PROFILE"' in html
assert 'resulting_state:state' in html
assert 'exact_readback_verified:true' in html
