set -euo pipefail
python3 - <<'PY'
from pathlib import Path
workflow = Path('tools/tasks/folded/va-pii-model-leakage-evidence.yml').read_text(encoding='utf-8')
forbidden = [
    'schedule' + ':',
    'actions/' + 'checkout@',
    'actions/' + 'setup-python@',
    'actions/' + 'upload-artifact@',
    'git ' + 'push',
    'permissions:' + '\n  contents: write',
]
assert 'permissions: {}' in workflow
assert all(marker not in workflow for marker in forbidden), forbidden
print('VA_PII_MODEL_LEAKAGE_HOSTED_SCHEDULE=RETIRED')
print('VA_PII_MODEL_LEAKAGE_REPOSITORY_WRITEBACK=NONE')
print('VA_PII_MODEL_LEAKAGE_ARTIFACT_CUSTODY=NONE')
print('VA_PII_MODEL_LEAKAGE_RUNTIME_AUTHORITY=NONE')
PY
