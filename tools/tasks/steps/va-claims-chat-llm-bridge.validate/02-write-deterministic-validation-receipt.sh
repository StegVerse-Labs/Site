mkdir -p .validation
python - <<'PY'
import hashlib, json, os
from pathlib import Path
payload = {
    'schema': 'stegverse.va_claims_chat.llm_bridge_validation.v1',
    'state': 'PASS',
    'runtime_projection_state': 'BLOCKED',
    'coordinated_llm_active': False,
    'private_document_upload_active': False,
    'private_document_retrieval_active': False,
    'filing_active': False,
    'authority_effect': False,
    'activation_effect': False,
    'repository': os.environ['GITHUB_REPOSITORY'],
    'commit': os.environ['GITHUB_SHA'],
    'workflow_run_id': os.environ['GITHUB_RUN_ID'],
    'workflow_run_attempt': os.environ['GITHUB_RUN_ATTEMPT'],
}
material=json.dumps(payload,sort_keys=True,separators=(',',':')).encode()
payload['receipt_sha256']=hashlib.sha256(material).hexdigest()
Path('.validation/va-claims-chat-llm-bridge-validation.json').write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
PY
