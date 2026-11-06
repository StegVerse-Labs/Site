python3 - <<'PY'
from pathlib import Path
text=Path('tools/tasks/folded/check-coinbase-skap-intr-route-consumer.yml').read_text()
forbidden=['contents'+': write','git'+' push','${'+'{ secrets.','actions/'+'checkout@']
assert not [x for x in forbidden if x in text]
assert 'permissions: {}' in text
print('SITE_SKAP_INTR_ROUTE_WORKFLOW_NON_AUTHORIZING_PASS')
PY
