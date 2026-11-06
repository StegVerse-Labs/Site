set -euo pipefail
python3 - <<'PY'
from pathlib import Path
text = Path('tools/tasks/folded/va-claims-chat-surface.yml').read_text(encoding='utf-8')
forbidden = [
    'sche' + 'dule:',
    'contents:' + ' write',
    'actions/' + 'checkout@',
    'actions/' + 'setup-python@',
    'actions/' + 'upload-artifact@',
    'git ' + 'push',
    'git ' + 'commit',
    'persist-' + 'credentials',
]
found = [token for token in forbidden if token in text]
if found:
    raise SystemExit('forbidden hosted authority remains: ' + ', '.join(found))
required = [
    'workflow_dispatch:',
    'pull_request:',
    'api/va-claim-assistant/runtime-projection.json',
    'assets/va-claims-chat-runtime.js',
    'permissions: {}',
]
missing = [token for token in required if token not in text]
if missing:
    raise SystemExit('required validation containment missing: ' + ', '.join(missing))
print('VA_CLAIMS_CHAT_VALIDATION_ONLY_CONTAINMENT=PASS')
PY
