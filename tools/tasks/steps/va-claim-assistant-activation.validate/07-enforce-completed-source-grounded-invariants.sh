set -euo pipefail
python3 - <<'PY'
import json
from pathlib import Path
gates = json.loads(Path('data/va-claim-assistant/activation-gates.json').read_text())
receipt = json.loads(Path('data/va-claim-assistant/source-grounded-activation-receipt.json').read_text())
manifest = json.loads(Path('data/va-claim-assistant/source-grounded-evidence-manifest.json').read_text())
governance = json.loads(Path('data/va-claim-assistant/governance-validation-receipt.json').read_text())
task = json.loads(Path('data/tasks/SITE-0001-VA-SOURCE-GROUNDED-EVIDENCE.json').read_text())
assert task['state'] == 'COMPLETE'
assert task['claim_state'] == 'COMPLETE'
assert task['claim_release_condition'] == 'SATISFIED'
assert governance['result'] == 'PASS'
assert governance['authority_effect'] is False
assert governance['activation_effect'] is False
assert manifest['state'] == 'EVIDENCE_CHAIN_VERIFIED'
assert manifest['activation_effect'] is False
assert manifest['publication_effect'] is False
gate01 = next(g for g in gates['gates'] if g['id'] == 'VCA-GATE-01')
gate02 = next(g for g in gates['gates'] if g['id'] == 'VCA-GATE-02')
gate08 = next(g for g in gates['gates'] if g['id'] == 'VCA-GATE-08')
gate09 = next(g for g in gates['gates'] if g['id'] == 'VCA-GATE-09')
assert gate01['state'] == 'VERIFIED'
assert gate02['state'] == 'VERIFIED'
assert gate08['state'] == 'VERIFIED'
if receipt['state'] == 'VERIFIED':
    assert gate09['state'] == 'VERIFIED'
else:
    assert gate09['state'] == 'BUILDING'
    assert receipt['next_action']
assert gates['anti_stall']['external_tasks_allowed'] is False
print('VA_SOURCE_GROUNDED_COMPLETED_CONTRACT=PASS')
print('VA_SOURCE_GROUNDED_PRODUCT_AUTHORITY_CHANGE=NONE')
PY
