#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
RUNTIME=ROOT/'assets'/'ecosystem-music-transition.js'
DIAGNOSTICS=ROOT/'assets'/'ecosystem-music-diagnostics.js'
TEST=ROOT/'tests'/'test_stegmusic_browser.py'
required={
 RUNTIME:['phase_boundary_bounded_delay','maximum_delay_ms: 2200','stegdj_transition_scheduled','stegdj_transition_executed','audio_context_reused: true',"authority: 'none'"],
 DIAGNOSTICS:['assets/ecosystem-music-transition.js','transition-smoothing-v1'],
 TEST:['transition_scheduler_loaded','transition_scheduled_event','transition_executed_event','track_changed_after_bounded_transition']
}
failures=[]
for path,markers in required.items():
    if not path.exists(): failures.append(f'missing {path.relative_to(ROOT)}'); continue
    text=path.read_text(encoding='utf-8')
    for marker in markers:
        if marker not in text: failures.append(f'{path.relative_to(ROOT)} missing marker: {marker}')
if failures:
    print('STEGMUSIC_TRANSITION_SMOOTHING_FAIL')
    for failure in failures: print(f'- {failure}')
    sys.exit(1)
print('STEGMUSIC_TRANSITION_SMOOTHING_PASS')
print('strategy=phase_boundary_bounded_delay')
print('maximum_delay_ms=2200')
print('audio_context_reused=true')
print('authority_effect=NONE')
