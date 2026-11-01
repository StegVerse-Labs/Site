set -euo pipefail
python3 - <<'PY'
from pathlib import Path
workflow = Path('tools/tasks/folded/math-solver-public-activation.yml').read_text(encoding='utf-8')
forbidden = [
    'contents' + ': write',
    'schedule' + ':',
    'git ' + 'push',
    'git ' + 'commit',
    'persist-' + 'credentials: true',
]
assert 'permissions: {}' in workflow
assert all(marker not in workflow for marker in forbidden), forbidden
print('MATH_SOLVER_ACTIVATION_VALIDATION_AUTHORITY=NONE')
print('MATH_SOLVER_REPOSITORY_MUTATION_AUTHORITY=NONE')
print('MATH_SOLVER_RUNTIME_AUTHORITY=NONE')
PY
