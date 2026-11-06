set -euo pipefail
python3 - <<'PY'
import hashlib, json, os
from pathlib import Path
overlay = Path('data/conectrr-security-overlay.json').read_bytes()
receipt = {
    'schema': 'stegverse.conectrr.security-overlay.receipt.v1',
    'goal_id': 'SV-SITE-CONECTRR-SEC-001',
    'repository': os.environ.get('SOURCE_REPOSITORY'),
    'commit': os.environ.get('SOURCE_SHA'),
    'overlay_sha256': hashlib.sha256(overlay).hexdigest(),
    'validation_state': 'PASS',
    'persistence': 'EPHEMERAL_ONLY',
    'authority_effect': 'none',
    'claims_not_created': ['certification', 'authorization_to_operate', 'agency_approval'],
}
print(json.dumps(receipt, sort_keys=True))
print('CONECTRR_SECURITY_OVERLAY_VALIDATION=PASS')
print('repository_writeback_authority=false')
print('artifact_custody=false')
print('runtime_authority_effect=false')
PY
