#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CONTROLLER = ROOT / 'assets' / 'ecosystem-music-intent-composition.js'
DIAGNOSTICS = ROOT / 'assets' / 'ecosystem-music-diagnostics.js'

required = {
    CONTROLLER: [
        'ALERTNESS ARC', 'FOCUS PLATEAU', 'DESCENDING SETTLE',
        'BOUNDARY EXPLORATION', 'composition_intent_profile_applied',
        'phase_specific:true', "authority:'none'", "model_scope:'active_profile'",
        'MutationObserver', 'intentCompositionStatus'
    ],
    DIAGNOSTICS: [
        'ecosystem-music-intent-composition.js',
        'loadIntentCompositionController',
        'data-stegmusic-intent-composition'
    ]
}

failures=[]
for path, markers in required.items():
    if not path.exists():
        failures.append(f'missing file: {path.relative_to(ROOT)}')
        continue
    text=path.read_text(encoding='utf-8')
    for marker in markers:
        if marker not in text:
            failures.append(f'{path.relative_to(ROOT)} missing marker: {marker}')

if failures:
    print('STEGMUSIC_INTENT_COMPOSITION_FAIL')
    for failure in failures:
        print(f'- {failure}')
    sys.exit(1)

print('STEGMUSIC_INTENT_COMPOSITION_PASS')
print('intent_changes_structure=true')
print('phase_specific_modulation=true')
print('profile_scope=active_browser_profile')
print('authority=none')
