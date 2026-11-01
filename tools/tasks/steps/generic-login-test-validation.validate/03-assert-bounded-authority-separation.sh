python - <<'PY'
from pathlib import Path
login = Path('generic-login-test.html').read_text(encoding='utf-8')
intr = Path('assets/kv-ui/intr-auth-client.js').read_text(encoding='utf-8')
kv_intr = Path('assets/kv-ui/intr-kv-client.js').read_text(encoding='utf-8')
create = Path('create-account-test.html').read_text(encoding='utf-8')
forgot = Path('forgot-password-test.html').read_text(encoding='utf-8')
combined = login + intr + kv_intr + create + forgot
assert 'Successful Login' in login
assert 'KnowledgeVault directory projection' in login
assert 'KnowledgeVault Status' in login
assert 'Create My KnowledgeVault' in login
assert 'Attach Existing KnowledgeVault' in login
assert 'Install on This Device' in login
assert 'stegverse.intr.kv-onboarding-transition/v1' in login
assert 'production_kv_custody:false' in login
assert "authority_effect:'NONE'" in login
assert '_Vault/SKAP' in login
assert 'SKAP Step-up Validation' in login
assert 'stegverse.intr.identity-assertion/v1' in intr
assert 'stegverse.intr.step-up-assertion/v1' in intr
assert 'kv.interlock.request.v1' in kv_intr
assert 'kv.interlock.response.v1' in kv_intr
assert 'COMMIT_CANDIDATE' in kv_intr
assert 'candidate_only:true' in kv_intr
assert 'canonical_state_changed:false' in kv_intr
assert 'SCOPE_EXPANSION_REJECTED' in kv_intr
assert 'AUTHORITY_BINDING_REJECTED' in kv_intr
assert 'assets/kv-ui/intr-kv-client.js' in login
assert 'credential_disclosed: false' in intr
assert 'raw_secret_present: false' in intr
assert 'INTR_NOT_PROVISIONED' in intr
assert 'TEST_ONLY' in create and 'TEST_ONLY' in forgot
assert 'TVC_EPHEMERAL_GITHUB_TOKEN' not in combined
assert 'GITHUB_TOKEN' not in combined
assert 'document.cookie' not in combined
print('GENERIC_INTR_KV_AUTHORITY_BOUNDARY_PASS')
PY
