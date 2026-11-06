set -euo pipefail
python3 scripts/validate_va_federal_plus_security_baseline.py
python3 - <<'PY'
import json
from pathlib import Path
receipt = json.loads(Path('data/va-claim-assistant/federal-plus-security-baseline-validation.json').read_text(encoding='utf-8'))
assert receipt['state'] == 'PASS'
assert receipt['federal_floor_required'] is True
assert receipt['exceeds_floor_required'] is True
assert receipt['control_family_count'] == 20
assert receipt['plus_domain_count'] == 7
assert receipt['authority_effect'] is False
assert receipt['activation_effect'] is False
print('VA_FEDERAL_PLUS_SECURITY_BASELINE=PASS')
print('VA_FEDERAL_PLUS_AUTHORITY_EFFECT=NONE')
print('VA_FEDERAL_PLUS_ACTIVATION_EFFECT=NONE')
PY
git diff --exit-code -- data/va-claim-assistant/federal-plus-security-baseline-validation.json
