set -euo pipefail
python3 - <<'PY'
import json
from pathlib import Path

receipt = json.loads(Path('data/va-claim-assistant/governed-product-goals-validation.json').read_text(encoding='utf-8'))
goals = json.loads(Path('data/va-claim-assistant/governed-product-goals.json').read_text(encoding='utf-8'))
states = {item['name']: item['state'] for item in goals['product_surfaces']}
expected = {
    'GOVERNED_VA_CLAIMS_GUIDE': 'CLAIMED_FOR_IMPLEMENTATION',
    'GOVERNED_VA_CLAIMS_CHAT': 'CLAIMED_FOR_IMPLEMENTATION',
    'PRIVATE_CLAIM_DOCUMENT_WORKSPACE': 'CLAIMED_FOR_IMPLEMENTATION',
    'VETERAN_APPROVED_AUTOMATED_CLAIM_FILING': 'FUTURE_GOVERNED_TARGET',
}
assert states == expected, (states, expected)
assert receipt['state'] == 'PASS'
assert receipt['required_goals_present'] is True
assert receipt['veteran_submission_authority_preserved'] is True
assert receipt['automated_filing_active'] is False
assert receipt['authority_effect'] is False
assert receipt['activation_effect'] is False
assert receipt['blockers'] == []
print('VA_GOVERNED_PRODUCT_GOALS_VALIDATION=PASS')
print('VA_GOVERNED_PRODUCT_GOALS_PRODUCT_STATE_CHANGE=NONE')
print('VA_GOVERNED_PRODUCT_GOALS_RUNTIME_AUTHORITY=NONE')
PY
