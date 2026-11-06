set -euo pipefail
python3 - <<'PY'
from pathlib import Path
workflow = Path('tools/tasks/folded/va-pii-redaction-working-copy-evidence.yml').read_text(encoding='utf-8')
forbidden = [
    'schedule' + ':',
    'actions/' + 'checkout@',
    'actions/' + 'setup-python@',
    'actions/' + 'upload-artifact@',
    'git ' + 'push',
]
assert 'permissions: {}' in workflow
assert all(marker not in workflow for marker in forbidden), forbidden
print('VA_PII_REDACTION_WORKING_COPY_HOSTED_SCHEDULE=RETIRED')
print('VA_PII_REDACTION_WORKING_COPY_REPOSITORY_WRITEBACK=NONE')
print('VA_PII_REDACTION_WORKING_COPY_ARTIFACT_CUSTODY=NONE')
print('VA_PII_REDACTION_WORKING_COPY_RUNTIME_AUTHORITY=NONE')
PY
