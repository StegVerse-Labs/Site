#!/usr/bin/env python3
import json
from pathlib import Path

p = Path('docs/SITE_TCL_PROPAGATION_RECEIPT.json')
data = json.loads(p.read_text())
assert data['source_repository'] == 'StegVerse-Labs/T-CL'
assert data['destination_repository'] == 'StegVerse-Labs/Site'
assert data['destination_handoff_checked'] == 'docs/SITE_MIRROR_HANDOFF.md'
assert data['intake_record'] == 'docs/SITE_TCL_PROPAGATION_INTAKE.json'
assert data['manual_task_required'] is False
b = data['site_boundary']
assert b['display_surface_only'] is True
assert b['no_semantic_redefinition'] is True
assert b['no_downstream_completion_claim'] is True
assert b['no_measured_savings_claim'] is True
print(str(p) + ': pass')
