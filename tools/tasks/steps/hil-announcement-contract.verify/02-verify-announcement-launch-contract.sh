python - <<'PY'
import hashlib
import json
from pathlib import Path

status = json.loads(Path('data/hil-announcement-status.json').read_text(encoding='utf-8'))
announcement = Path('hil-study-announcement.html').read_text(encoding='utf-8')
launch = Path('hil-study-launch.html').read_text(encoding='utf-8')
paper = Path('data/HIL_Canonical_Paper_v1_1.pdf').read_bytes()

errors = []
expected = status['canonical_primary']['sha256']
actual = hashlib.sha256(paper).hexdigest()
if actual != expected:
    errors.append(f'canonical paper hash mismatch: {actual}')
if status.get('announcement_permitted') is not True:
    errors.append('announcement_permitted must be true')
intake = status.get('participant_intake_state')
if intake not in {'OPEN_MANAGED_RETURN', 'OPEN_GOVERNED_RECEIVER'}:
    errors.append(f'participant intake is not open: {intake}')
state = status.get('announcement_state')
claims = set(status.get('claims_withheld', []))
if state == 'ANNOUNCEMENT_READY_WITH_MANAGED_RETURN':
    required_claims = {
        'SERVER_SUBMISSION_COMPLETE',
        'DURABLE_CUSTODY_COMPLETE',
        'REGISTRY_COMMIT_COMPLETE',
        'PUBLICATION_COMPLETE',
    }
    if not required_claims.issubset(claims):
        errors.append('managed-return unavailable claims are not withheld')
elif state == 'ANNOUNCEMENT_READY_WITH_PRODUCTION_RECEIVER':
    if status.get('production_receiver', {}).get('ready') is not True:
        errors.append('production announcement lacks production_receiver.ready')
    if 'PUBLICATION_COMPLETE' not in claims:
        errors.append('publication claim must remain withheld')
else:
    errors.append(f'unsupported announcement state: {state}')
if status.get('derivation', {}).get('mode') != 'MACHINE_DERIVED_FAIL_CLOSED':
    errors.append('announcement status is not machine-derived fail-closed')
for phrase in ['participant-managed return', 'does not falsely claim server custody']:
    if phrase not in launch:
        errors.append(f'launch page missing boundary phrase: {phrase}')
for phrase in [
    'The study may be announced now',
    'Persistent server custody and automated publication remain intentionally unclaimed',
]:
    if phrase not in announcement:
        errors.append(f'announcement page missing phrase: {phrase}')
if errors:
    raise SystemExit('\n'.join(errors))
print(json.dumps({
    'state': 'PASS',
    'announcement_state': state,
    'participant_intake_state': intake,
    'canonical_paper_sha256': actual,
    'claims_withheld': status['claims_withheld'],
    'derivation_mode': status['derivation']['mode'],
}, indent=2))
PY
