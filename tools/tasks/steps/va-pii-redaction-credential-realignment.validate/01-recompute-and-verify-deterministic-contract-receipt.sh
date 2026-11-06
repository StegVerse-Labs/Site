set -euo pipefail
python3 scripts/validate_va_pii_redaction_credential_realignment.py
python3 - <<'PY'
import json
from pathlib import Path
receipt = json.loads(Path('data/va-claim-assistant/pii-redaction-credential-realignment-validation.json').read_text(encoding='utf-8'))
assert receipt['state'] == 'PASS'
assert receipt['authority_effect'] is False
assert receipt['activation_effect'] is False
print('VA_PII_REALIGNMENT_VALIDATION=PASS')
print('VA_PII_REALIGNMENT_AUTHORITY_EFFECT=NONE')
print('VA_PII_REALIGNMENT_ACTIVATION_EFFECT=NONE')
PY
git diff --exit-code -- data/va-claim-assistant/pii-redaction-credential-realignment-validation.json
