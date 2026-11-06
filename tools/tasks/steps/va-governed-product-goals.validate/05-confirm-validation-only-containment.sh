set -euo pipefail
python3 - <<'PY'
from pathlib import Path

workflow = Path('tools/tasks/folded/va-governed-product-goals.yml').read_text(encoding='utf-8')
forbidden = [
    'sched' + 'ule:',
    'contents:' + ' write',
    'github.' + 'token',
    'actions/' + 'checkout@',
    'actions/' + 'setup-python@',
    'actions/' + 'upload-artifact@',
    'git ' + 'push',
    'git ' + 'commit',
]
present = [marker for marker in forbidden if marker in workflow]
if present:
    raise SystemExit(f'forbidden governed-product-goals authority/custody remains: {present}')
required = ['workflow_dispatch:', 'pull_request:', 'push:', 'permissions: {}', 'cancel-in-progress: true']
missing = [marker for marker in required if marker not in workflow]
if missing:
    raise SystemExit(f'missing retained validation contract: {missing}')
print('VA_GOVERNED_PRODUCT_GOALS_SCHEDULE_RETIRED=PASS')
print('VA_GOVERNED_PRODUCT_GOALS_GITHUB_TOKEN_AUTHORITY=NONE')
PY
