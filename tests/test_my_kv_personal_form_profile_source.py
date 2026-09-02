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
assert "skap://signing/" not in sw  # service worker stores opaque validated profile; it is not a signer
print("MY_KV_PERSONAL_FORM_PROFILE_SOURCE_PASS")
