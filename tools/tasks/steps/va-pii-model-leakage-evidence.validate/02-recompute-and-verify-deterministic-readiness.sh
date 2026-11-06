set -euo pipefail
python3 scripts/observe_va_pii_model_leakage_evidence.py
python3 - <<'PY'
import json
from pathlib import Path
receipt = json.loads(Path('data/va-claim-assistant/pii-model-leakage-readiness.json').read_text(encoding='utf-8'))
assert receipt['state'] in {'BLOCKED', 'COMPLETE'}
assert receipt['private_document_upload_enabled'] is False
assert receipt['authority_effect'] is False
assert receipt['activation_effect'] is False
print(f"VA_PII_MODEL_LEAKAGE_STATE={receipt['state']}")
print('VA_PII_MODEL_LEAKAGE_AUTHORITY_EFFECT=NONE')
print('VA_PII_MODEL_LEAKAGE_ACTIVATION_EFFECT=NONE')
PY
git diff --exit-code -- data/va-claim-assistant/pii-model-leakage-readiness.json
