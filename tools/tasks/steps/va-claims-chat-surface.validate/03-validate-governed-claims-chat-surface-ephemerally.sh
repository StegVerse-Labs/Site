set -euo pipefail
python3 scripts/validate_va_claims_chat_surface.py
python3 - <<'PY'
import json
from pathlib import Path
receipt = json.loads(Path('data/va-claim-assistant/chat-surface-validation.json').read_text(encoding='utf-8'))
assert receipt['state'] == 'PASS', receipt
assert receipt['private_document_upload_enabled'] is False, receipt
assert receipt['automated_filing_enabled'] is False, receipt
assert receipt['veteran_submission_authority_preserved'] is True, receipt
assert receipt['authority_effect'] is False, receipt
assert receipt['activation_effect'] is False, receipt
assert receipt['errors'] == [], receipt
print('VA_CLAIMS_CHAT_SURFACE_VALIDATION=PASS')
print('VA_CLAIMS_CHAT_AUTHORITY_EFFECT=NONE')
print('VA_CLAIMS_CHAT_ACTIVATION_EFFECT=NONE')
PY
