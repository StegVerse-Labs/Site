set -euo pipefail
python3 scripts/validate_va_filing_integration_contract.py
python3 - <<'PY'
import json
from pathlib import Path
receipt = json.loads(Path('data/va-claim-assistant/filing-integration-contract-validation.json').read_text(encoding='utf-8'))
assert receipt['state'] == 'PASS'
assert receipt['submission_enabled'] is False
assert receipt['active_transport'] is None
assert receipt['veteran_submission_authority_preserved'] is True
assert receipt['exact_package_authorization_required'] is True
assert receipt['duplicate_prevention_required'] is True
assert receipt['reconstruction_pass_required'] is True
assert receipt['authority_effect'] is False
assert receipt['activation_effect'] is False
print('VA_FILING_INTEGRATION_CONTRACT=PASS')
print('VA_FILING_SUBMISSION_ENABLED=false')
print('VA_FILING_AUTHORITY_EFFECT=NONE')
print('VA_FILING_ACTIVATION_EFFECT=NONE')
PY
git diff --exit-code -- data/va-claim-assistant/filing-integration-contract-validation.json
