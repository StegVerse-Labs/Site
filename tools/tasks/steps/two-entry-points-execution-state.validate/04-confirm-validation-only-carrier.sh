python3 - <<'PY'
from pathlib import Path
workflow = Path('tools/tasks/folded/two-entry-points-execution-state.yml').read_text(encoding='utf-8')
forbidden = [
    'schedule' + ':',
    'actions/' + 'checkout@',
    'actions/' + 'setup-python@',
    'actions/' + 'upload-artifact@',
    'persist-' + 'credentials',
    'git ' + 'push',
    'permissions:\n  contents: write',
]
assert 'permissions: {}' in workflow
assert 'workflow_dispatch:' in workflow
assert 'push:' in workflow
assert 'pull_request:' in workflow
assert all(marker not in workflow for marker in forbidden), forbidden
print('TWO_ENTRY_VALIDATION_HOSTED_SCHEDULE=RETIRED')
print('TWO_ENTRY_VALIDATION_REPOSITORY_WRITEBACK=NONE')
print('TWO_ENTRY_VALIDATION_ARTIFACT_CUSTODY=NONE')
print('TWO_ENTRY_VALIDATION_RUNTIME_AUTHORITY=NONE')
PY
