set -euo pipefail
python3 - <<'PY'
from pathlib import Path
workflow = Path('tools/tasks/folded/va-pii-redaction-credential-realignment.yml').read_text(encoding='utf-8')
forbidden = [
    'schedule' + ':',
    'actions/' + 'checkout@',
    'actions/' + 'setup-python@',
    'actions/' + 'upload-artifact@',
    'git ' + 'push',
]
assert 'permissions: {}' in workflow
assert all(marker not in workflow for marker in forbidden), forbidden
print('VA_PII_REALIGNMENT_HOSTED_SCHEDULE=RETIRED')
print('VA_PII_REALIGNMENT_REPOSITORY_WRITEBACK=NONE')
print('VA_PII_REALIGNMENT_ARTIFACT_CUSTODY=NONE')
print('VA_PII_REALIGNMENT_RUNTIME_AUTHORITY=NONE')
PY
