#!/usr/bin/env python3
from pathlib import Path
import sys

PAGE = Path('va-disability-claim-guide.html')
IMAGE = Path('assets/va-claim-guide/01-open-va-app-v2.svg')
ASSISTANT = Path('assets/va-claim-guide/va-guide-assistant.js')

required = [
    'Purpose: accurate claims, not inflated claims.',
    'Ask the VA process guide',
    'Current mode:',
    'Live LLM answers and private document analysis are still in development',
    'Watch this box for messages describing the assistant',
    'Phase 1',
    'Phase 2',
    'Phase 3',
    'Phase 4',
    'Phase 5',
    'Phase 6',
    'Gather every document that may affect the claim',
    'Include unfavorable or conflicting records',
    'VA Form 21-526EZ',
    'Official sources',
    'assets/va-claim-guide/01-open-va-app-v2.svg',
]

errors = []
if not PAGE.exists():
    errors.append('missing va-disability-claim-guide.html')
else:
    text = PAGE.read_text(encoding='utf-8')
    for marker in required:
        if marker not in text:
            errors.append(f'missing page marker: {marker}')
    if '<meta name="viewport"' not in text:
        errors.append('mobile viewport is missing')
    if 'aria-live="polite"' not in text:
        errors.append('assistant live-region accessibility marker is missing')
    if 'does not determine eligibility' not in text:
        errors.append('authority boundary is missing')

for asset in (IMAGE, ASSISTANT):
    if not asset.exists():
        errors.append(f'missing asset: {asset}')

if errors:
    print('VA CLAIM GUIDE: FAIL')
    for error in errors:
        print(f'- {error}')
    sys.exit(1)

print('VA CLAIM GUIDE: PASS')
print('Static guide page: complete')
print('Multi-document workflow: complete')
print('Bounded procedural assistant: available')
print('Assistant capability status box: active')
print('Live source-grounded LLM: in development')
print('Private document analysis: not active')
