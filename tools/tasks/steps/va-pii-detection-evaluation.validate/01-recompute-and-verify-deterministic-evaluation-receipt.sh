set -euo pipefail
python3 scripts/evaluate_va_pii_detection_fixture.py
python3 - <<'PY'
import json
from pathlib import Path
receipt = json.loads(Path('data/va-claim-assistant/pii-detection-evaluation-receipt.json').read_text(encoding='utf-8'))
assert receipt['state'] == 'PASS'
assert receipt['reference_evaluator_only'] is True
assert receipt['production_detector_ready'] is False
assert receipt['private_document_upload_enabled'] is False
assert receipt['authority_effect'] is False
assert receipt['activation_effect'] is False
print('VA_PII_DETECTION_EVALUATION=PASS')
print('VA_PII_DETECTION_PRODUCTION_READINESS=false')
print('VA_PII_DETECTION_AUTHORITY_EFFECT=NONE')
print('VA_PII_DETECTION_ACTIVATION_EFFECT=NONE')
PY
git diff --exit-code -- data/va-claim-assistant/pii-detection-evaluation-receipt.json
