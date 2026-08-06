#!/usr/bin/env python3
from pathlib import Path
import re
import sys

GUIDE = Path('va-disability-claim-guide.html')
WALK = Path('va-claims-guided-workflow.html')
errors = []

for path in (GUIDE, WALK):
    if not path.exists():
        errors.append(f'missing {path}')

if GUIDE.exists():
    text = GUIDE.read_text(encoding='utf-8')
    if '<meta name="viewport"' not in text:
        errors.append('guide mobile viewport missing')
    cards = re.findall(r'<section class="step-card" data-step="(\d+)"', text)
    if cards != ['1','2','3','4','5','6']:
        errors.append(f'guide requires six ordered steps: {cards}')
    for marker in ('DONE','Help me with this','vaClaimsStepStateV1','0 of 6 done','Reset'):
        if marker not in text:
            errors.append(f'guide missing marker: {marker}')
    if text.count('class="done-button"') != 6:
        errors.append('guide requires one DONE button per step')
    if text.count('class="sv-btn sv-btn-secondary help-link"') != 6:
        errors.append('guide requires one focused-help link per step')
    if 'SOURCE_GROUNDED_ASSISTANT' in text or 'Verified capability state' in text:
        errors.append('internal capability language exposed on guide')

if WALK.exists():
    text = WALK.read_text(encoding='utf-8')
    if '<meta name="viewport"' not in text:
        errors.append('walkthrough mobile viewport missing')
    cards = re.findall(r'<section class="card(?: active)?" data-card="(\d+)"', text)
    if cards != ['1','2','3','4','5','6']:
        errors.append(f'walkthrough requires six ordered steps: {cards}')
    for marker in ('Return to Instruction Page','Continue with help me complete this','vaClaimsStepStateV1','URLSearchParams'):
        if marker not in text:
            errors.append(f'walkthrough missing marker: {marker}')
    if text.count('Mark step DONE') != 6:
        errors.append('walkthrough requires one shared completion control per step')

if errors:
    print('VA CLAIM GUIDE: FAIL')
    for error in errors:
        print(f'- {error}')
    sys.exit(1)

print('VA CLAIM GUIDE: PASS')
print('Primary instruction page: six persistent steps')
print('Focused walkthrough: step-addressable')
print('Shared completion state: active')
print('Focused help handoff: active')
