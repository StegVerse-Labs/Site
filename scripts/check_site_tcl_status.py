#!/usr/bin/env python3
import json
from pathlib import Path

p = Path('docs/SITE_TCL_STATUS.json')
data = json.loads(p.read_text())
assert data['surface_type'] == 'status_only_display'
assert data['source_repository'] == 'StegVerse-Labs/T-CL'
assert data['manual_task_required'] is False
assert data['display_status'] == 'eligible_for_status_display_only'
blocked = set(data['blocked_claims'])
for claim in ['Site certifies T-CL', 'Site redefines T-CL semantics', 'downstream propagation is complete', 'admissibility-cost savings are measured']:
    assert claim in blocked
print(str(p) + ': pass')
