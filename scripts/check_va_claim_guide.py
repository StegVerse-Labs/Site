#!/usr/bin/env python3
from pathlib import Path
import re
import sys

GUIDE = Path('va-disability-claim-guide.html')
WALK = Path('va-claims-guided-workflow.html')
CHAT = Path('va-claims-chat.html')
errors = []

for path in (GUIDE, WALK, CHAT):
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
        errors.append('guide requires one help control per step')
    if 'SOURCE_GROUNDED_ASSISTANT' in text or 'Verified capability state' in text:
        errors.append('internal capability language exposed on guide')

    markers = (
        'id="step-1-email"', 'id="step-1-phone"', 'id="step-1-id"',
        'example@example.com', 'driver’s license', 'state-issued photo ID', 'U.S. passport book',
        'When all 3 boxes are checked, Step 1 is marked DONE automatically.',
        'https://www.va.gov/sign-in/', 'Login.gov', 'ID.me', 'confirmation email',
        'id="step-2-account-created"', 'id="step-2-va-login-success"',
        'https://www.va.gov/my-health/medical-records/download',
        'https://mobile.va.gov/app/va-health-and-benefits',
        'Review medical records on VA.gov',
        'Date range</strong> to <strong>All time',
        'Types of records to include</strong> to <strong>All',
        '<strong>PDF</strong> or <strong>TXT</strong>',
        '<strong>Download report</strong>',
        'Downloads</strong> folder',
        'Submit the file to VA Claims Chat',
        'only upload the medical-record file if VA Claims Chat presents an active secure document-upload control',
    )
    for marker in markers:
        if marker not in text:
            errors.append(f'guide clarity contract missing: {marker}')

    required_ids = {
        '1': ['step-1-email','step-1-phone','step-1-id'],
        '2': ['step-2-account-created','step-2-va-login-success'],
        '3': ['step-3-reached-download'],
        '4': ['step-4-downloaded'],
        '5': ['step-5-found-file'],
        '6': ['step-6-chat-open'],
    }
    for step, ids in required_ids.items():
        for item_id in ids:
            if f'id="{item_id}"' not in text:
                errors.append(f'step {step} required confirmation missing: {item_id}')
    for marker in ('const requirements={', 'function ready(step)', "if(isReady)state[step]=true", "if(!isReady)state[step]=false"):
        if marker not in text:
            errors.append(f'completion gate missing: {marker}')

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
    for marker in ('Open VA.gov Sign In','Open VA medical-record download page','All time','Download report','Find the downloaded file','Submit the file to VA Claims Chat'):
        if marker not in text:
            errors.append(f'walkthrough clarity marker missing: {marker}')

if CHAT.exists():
    text = CHAT.read_text(encoding='utf-8')
    for marker in ('Card 1 — Get ready','Card 2 — Create your VA.gov sign-in account','Card 3 — Open the medical-record download page','Card 4 — Download all available medical records','Card 5 — Find the downloaded file','Card 6 — Continue to VA Claims Chat'):
        if marker not in text:
            errors.append(f'Claims Chat guided card missing: {marker}')
    if 'Private document upload and automated claim filing remain disabled' not in text:
        errors.append('Claims Chat secure-upload boundary missing')

if errors:
    print('VA CLAIM GUIDE: FAIL')
    for error in errors:
        print(f'- {error}')
    sys.exit(1)

print('VA CLAIM GUIDE: PASS')
print('Primary instruction page: six explicit sequential steps')
print('Step 1: three-item readiness checklist auto-completes')
print('Step 2: VA.gov -> Login.gov/ID.me -> account confirmation -> VA.gov login')
print('Steps 3-5: records page -> all-record download -> locate file')
print('Step 6: VA Claims Chat handoff with secure-upload fail-closed boundary')
print('Focused walkthrough and Claims Chat cards: aligned')
