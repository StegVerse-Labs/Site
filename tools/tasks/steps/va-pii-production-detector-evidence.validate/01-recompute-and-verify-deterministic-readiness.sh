set -euo pipefail
python3 scripts/observe_va_pii_production_detector_evidence.py
python3 - <<'PY'
import json
from pathlib import Path
receipt = json.loads(Path('data/va-claim-assistant/pii-production-detector-readiness.json').read_text(encoding='utf-8'))
assert receipt['state'] in {'BLOCKED', 'COMPLETE'}
assert receipt['private_document_upload_enabled'] is False
assert receipt['authority_effect'] is False
assert receipt['activation_effect'] is False
print(f"VA_PII_PRODUCTION_DETECTOR_STATE={receipt['state']}")
print('VA_PII_PRODUCTION_DETECTOR_AUTHORITY_EFFECT=NONE')
print('VA_PII_PRODUCTION_DETECTOR_ACTIVATION_EFFECT=NONE')
PY
git diff --exit-code -- data/va-claim-assistant/pii-production-detector-readiness.json
