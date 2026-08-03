#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

REGISTRY = Path('data/va-claim-assistant/pii-realignment-readiness.json')
RECEIPT = Path('data/va-claim-assistant/pii-realignment-readiness-validation.json')

required_ids = {f'PII-RDY-{i:02d}' for i in range(1, 10)}
allowed_states = {'CLAIMED','BLOCKED','RETRY','REVIEW_REQUIRED','FAILED','COMPLETE','SUPERSEDED','MERGED'}

errors = []
data = json.loads(REGISTRY.read_text())
requirements = data.get('requirements', [])
ids = {item.get('id') for item in requirements}
if ids != required_ids:
    errors.append(f'requirement_ids:{sorted(ids)}')
for item in requirements:
    if item.get('state') not in allowed_states:
        errors.append(f"invalid_state:{item.get('id')}:{item.get('state')}")
    for field in ('owner','capability','release_condition'):
        if not item.get(field):
            errors.append(f"missing_{field}:{item.get('id')}")
if data.get('authority_effect') is not False:
    errors.append('authority_effect_must_be_false')
if data.get('activation_effect') is not False:
    errors.append('activation_effect_must_be_false')
if data.get('overall_state') not in allowed_states:
    errors.append('invalid_overall_state')
if data.get('machine_owner') != '.github/workflows/va-pii-realignment-readiness.yml':
    errors.append('machine_owner_mismatch')

states = {item['id']: item['state'] for item in requirements}
all_complete = all(state == 'COMPLETE' for state in states.values())
expected_overall = 'COMPLETE' if all_complete else ('REVIEW_REQUIRED' if any(state == 'REVIEW_REQUIRED' for state in states.values()) else 'BLOCKED')
if data.get('overall_state') != expected_overall:
    errors.append(f"overall_state_expected:{expected_overall}")

contract_hash = hashlib.sha256(REGISTRY.read_bytes()).hexdigest()
receipt = {
    'schema_version': '1.0.0',
    'task_id': data.get('task_id'),
    'state': 'PASS' if not errors else 'FAIL',
    'readiness_state': data.get('overall_state'),
    'requirement_count': len(requirements),
    'complete_count': sum(1 for state in states.values() if state == 'COMPLETE'),
    'blocked_count': sum(1 for state in states.values() if state == 'BLOCKED'),
    'review_required_count': sum(1 for state in states.values() if state == 'REVIEW_REQUIRED'),
    'first_blocker': next((item['id'] for item in requirements if item['state'] == 'BLOCKED'), None),
    'authority_effect': False,
    'activation_effect': False,
    'registry_sha256': contract_hash,
    'errors': errors
}
canonical = json.dumps(receipt, sort_keys=True, separators=(',', ':')).encode()
receipt['receipt_sha256'] = hashlib.sha256(canonical).hexdigest()
RECEIPT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
print(json.dumps(receipt, indent=2, sort_keys=True))
raise SystemExit(0 if not errors else 1)
