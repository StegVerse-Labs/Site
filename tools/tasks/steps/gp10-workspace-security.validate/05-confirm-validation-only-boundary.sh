set -euo pipefail
ROOT="."
cd "$ROOT"
python3 - <<'PY'
from pathlib import Path
workflow = Path('tools/tasks/folded/gp10-workspace-security.yml').read_text(encoding='utf-8')
forbidden = [
    'permissions:' + '\n  contents: ' + 'write',
    'actions/' + 'checkout@',
    'actions/' + 'setup-python@',
    'actions/' + 'upload-artifact@',
    'issues:' + ' write',
    'GH_' + 'TOKEN:',
    '$' + '{{ github.' + 'token }}',
    'git ' + 'push',
    'git ' + 'commit',
]
hits = [marker for marker in forbidden if marker in workflow]
if hits:
    raise SystemExit(f'forbidden GP10 hosted authority marker(s): {hits}')
assert 'permissions: {}' in workflow
assert 'Refuse credential-bearing GP10 validation configuration' in workflow
print('GP10_VALIDATION_ONLY=PASS')
print('GP10_REPOSITORY_WRITEBACK=NONE')
print('GP10_ARTIFACT_CUSTODY=NONE')
print('GP10_RUNTIME_CONTROL_PLANE_AUTHORITY=NONE')
PY
