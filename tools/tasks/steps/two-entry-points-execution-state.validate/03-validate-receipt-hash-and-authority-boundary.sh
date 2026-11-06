python3 - <<'PY'
import hashlib
import json
from pathlib import Path

path = Path('reports/two-entry-points-execution-state-validation.json')
value = json.loads(path.read_text())
assert value['schema'] == 'stegverse.two_entry_points.execution_state_validation.v1'
assert value['result'] == 'PASS'
assert value['authority_granted'] is False
assert value['release_authorized'] is False
material = dict(value)
expected = material.pop('receipt_sha256')
actual = hashlib.sha256(
    json.dumps(material, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
).hexdigest()
assert expected == actual
print(f'TWO_ENTRY_VALIDATION_RECEIPT_SHA256={expected}')
print('TWO_ENTRY_VALIDATION_AUTHORITY_EFFECT=NONE')
print('TWO_ENTRY_VALIDATION_RELEASE_AUTHORITY=NONE')
PY
