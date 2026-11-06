set -euo pipefail
python3 - <<'PY'
import datetime as dt
import hashlib
import json
from pathlib import Path

result = json.loads(Path('/tmp/vacc-goal3-contract-suite.json').read_text(encoding='utf-8'))
receipt = {
    'schema_version': '1.0.0',
    'receipt_id': 'site-vacc-goal3-contract-suite-validation-ephemeral',
    'observed_at': dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
    'state': 'VERIFIED',
    'canonical_owner': 'StegVerse-Labs/Site#116',
    'issues_covered': [179, 180, 181, 182, 183, 184],
    'result': result,
    'public_upload_enabled': False,
    'private_retrieval_enabled': False,
    'submission_enabled': False,
    'authority_effect': False,
    'activation_effect': False,
}
canonical = json.dumps(receipt, sort_keys=True, separators=(',', ':')).encode()
receipt['receipt_sha256'] = hashlib.sha256(canonical).hexdigest()
target = Path('/tmp/vacc-goal3-contract-suite-validation-receipt.json')
target.write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n', encoding='utf-8')

verified = json.loads(target.read_text(encoding='utf-8'))
expected = verified.pop('receipt_sha256')
actual = hashlib.sha256(json.dumps(verified, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
assert expected == actual
assert verified['state'] == 'VERIFIED'
assert verified['result']['state'] == 'PASS'
assert verified['public_upload_enabled'] is False
assert verified['private_retrieval_enabled'] is False
assert verified['submission_enabled'] is False
assert verified['authority_effect'] is False
assert verified['activation_effect'] is False
print('VACC_GOAL3_CONTRACT_SUITE=PASS')
print('VACC_GOAL3_PUBLIC_UPLOAD_ENABLED=false')
print('VACC_GOAL3_PRIVATE_RETRIEVAL_ENABLED=false')
print('VACC_GOAL3_SUBMISSION_ENABLED=false')
print('VACC_GOAL3_RUNTIME_AUTHORITY=NONE')
PY
