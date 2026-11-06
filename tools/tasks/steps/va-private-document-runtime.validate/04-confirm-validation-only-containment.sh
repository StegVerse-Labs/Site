set -euo pipefail
python3 - <<'PY'
from pathlib import Path

workflow = Path('tools/tasks/folded/va-private-document-runtime.yml').read_text(encoding='utf-8')
forbidden = [
    'schedule' + ':',
    'contents' + ': write',
    'github' + '.token',
    'GH_TOKEN' + ':',
    'actions/' + 'checkout@',
    'actions/' + 'setup-python@',
    'actions/' + 'upload-artifact@',
    'git ' + 'push',
    'git ' + 'commit',
]
present = [marker for marker in forbidden if marker in workflow]
if present:
    raise SystemExit(f'forbidden completed-fixture authority/custody remains: {present}')
required = ['workflow_dispatch:', 'push:', 'permissions: {}', 'cancel-in-progress: true']
missing = [marker for marker in required if marker not in workflow]
if missing:
    raise SystemExit(f'missing retained validation contract: {missing}')
print('VA_PRIVATE_DOCUMENT_HOURLY_FIXTURE_RETIRED=PASS')
print('VA_PRIVATE_DOCUMENT_GITHUB_TOKEN_AUTHORITY=NONE')
PY
