set -euo pipefail
python3 - <<'PY'
from pathlib import Path
workflow = Path('tools/tasks/folded/va-filing-integration-contract.yml').read_text(encoding='utf-8')
forbidden = [
    'schedule' + ':',
    'actions/' + 'checkout@',
    'actions/' + 'setup-python@',
    'actions/' + 'upload-artifact@',
    'git ' + 'push',
]
assert 'permissions: {}' in workflow
assert all(marker not in workflow for marker in forbidden), forbidden
print('VA_FILING_CONTRACT_HOSTED_SCHEDULE=RETIRED')
print('VA_FILING_CONTRACT_REPOSITORY_WRITEBACK=NONE')
print('VA_FILING_CONTRACT_ARTIFACT_CUSTODY=NONE')
print('VA_FILING_CONTRACT_RUNTIME_AUTHORITY=NONE')
PY
