#!/usr/bin/env python3
from pathlib import Path
import sys

PAGE = Path('va-disability-claim-guide.html')
ASSET = Path('assets/va-claim-guide/01-open-va-app-safe.svg')
ASSISTANT = Path('assets/va-claim-guide/va-guide-assistant.js')

required = [
    'Ask the VA process guide',
    'Current mode:',
    'Document analysis and live LLM answers remain disabled',
    'Phase 1',
    'Phase 6',
    'VA Form 21-526EZ',
    'Official sources',
    'assets/va-claim-guide/01-open-va-app-safe.svg',
]

errors = []
if not PAGE.exists():
    errors.append('missing va-disability-claim-guide.html')
else:
    text = PAGE.read_text(encoding='utf-8')
    for marker in required:
        if marker not in text:
            errors.append(f'missing page marker: {marker}')
    if 'live LLM' not in text or 'Current mode' not in text:
        errors.append('assistant capability/completeness notice is missing')

for asset in (ASSET, ASSISTANT):
    if not asset.exists():
        errors.append(f'missing asset: {asset}')

if errors:
    print('VA CLAIM GUIDE: FAIL')
    for error in errors:
        print(f'- {error}')
    sys.exit(1)

print('VA CLAIM GUIDE: PASS')
print('Static guide: complete')
print('Bounded assistant: available')
print('Live source-grounded LLM: in development')
print('Private document analysis: not active')
