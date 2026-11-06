set -euo pipefail
python3 - <<'PY'
from pathlib import Path
workflow = Path('tools/tasks/folded/va-claim-assistant-activation.yml').read_text(encoding='utf-8')
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
    raise SystemExit(f'forbidden completed-reconciler authority/custody remains: {present}')
required = ['workflow_dispatch:', 'push:', 'permissions: {}', 'cancel-in-progress: true']
missing = [marker for marker in required if marker not in workflow]
if missing:
    raise SystemExit(f'missing retained validation contract: {missing}')
broad_receipt_path = "data/va-claim-assistant/" + "**"
if broad_receipt_path in workflow:
    raise SystemExit('broad VA receipt/state trigger remains')
print('VA_SOURCE_GROUNDED_HOURLY_RECONCILER_RETIRED=PASS')
print('VA_SOURCE_GROUNDED_GITHUB_TOKEN_AUTHORITY=NONE')
print('VA_SOURCE_GROUNDED_RUNTIME_AUTHORITY=NONE')
PY
