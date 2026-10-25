set -euo pipefail
grep -q 'credential_authority==="TV/TVC"' assets/kv-testflight-projection-entry.js
grep -q 'github_token_runtime_authority==="NONE"' assets/kv-testflight-projection-entry.js
grep -q 'browser_identity_authority:false' assets/kv-testflight-projection-entry.js
! grep -q 'navigator.userAgent' assets/kv-testflight-projection-entry.js
! grep -q 'localStorage' kv-testflight-projection.html
! grep -q 'sessionStorage' kv-testflight-projection.html
echo 'KV_TESTFLIGHT_PROJECTION_ENTRY_SOURCE_VALIDATION=PASS'
echo 'AUTHORITY_EFFECT=NONE_PROJECTION_ONLY'
