python3 - <<'PY'
from pathlib import Path
text = Path('.github/workflows/check-stegfin-phone-projection.yml').read_text(encoding='utf-8')
forbidden = [
    'contents'+': write',
    'git'+' push',
    '$'+'{{ '+'github.token'+' }}',
    'actions/'+'checkout@',
    '$'+'{{ '+'secrets.',
]
found = [value for value in forbidden if value in text]
assert not found, found
assert 'permissions: {}' in text
print('STEGFIN_PHONE_PROJECTION_WORKFLOW_NON_AUTHORIZING_PASS')
PY
