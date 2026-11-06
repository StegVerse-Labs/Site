set -euo pipefail
python3 - <<'PY'
from pathlib import Path
workflow = Path('tools/tasks/folded/va-pii-detection-evaluation.yml').read_text(encoding='utf-8')
forbidden = [
    'schedule' + ':',
    'actions/' + 'checkout@',
    'actions/' + 'setup-python@',
    'actions/' + 'upload-artifact@',
    'git ' + 'push',
]
assert 'permissions: {}' in workflow
assert all(marker not in workflow for marker in forbidden), forbidden
print('VA_PII_DETECTION_HOSTED_SCHEDULE=RETIRED')
print('VA_PII_DETECTION_REPOSITORY_WRITEBACK=NONE')
print('VA_PII_DETECTION_ARTIFACT_CUSTODY=NONE')
print('VA_PII_DETECTION_RUNTIME_AUTHORITY=NONE')
PY
