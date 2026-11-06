set -euo pipefail
python3 - <<'PY'
import json
import os
from pathlib import Path

receipt = json.loads(Path(os.environ['PRIVATE_DOCUMENT_RECEIPT']).read_text(encoding='utf-8'))
assert receipt['privacy']['public_upload_enabled'] is False
assert receipt['privacy']['raw_documents_published'] is False
assert receipt['privacy']['processing_scope'] == 'REPOSITORY_FIXTURE_ONLY'
assert not any(receipt['authority_flags'].values())
assert receipt['authority_effect'] is False
assert receipt['activation_effect'] is False
assert len(receipt['assessment_hash']) == 64
assert receipt['missing_evidence']
print('VA_PRIVATE_DOCUMENT_FIXTURE_BOUNDARIES=PASS')
print('VA_PRIVATE_DOCUMENT_PUBLIC_UPLOAD_ENABLED=false')
print('VA_PRIVATE_DOCUMENT_REPOSITORY_WRITEBACK=NONE')
print('VA_PRIVATE_DOCUMENT_ARTIFACT_CUSTODY=NONE')
print('VA_PRIVATE_DOCUMENT_RUNTIME_AUTHORITY=NONE')
PY
