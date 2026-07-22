#!/usr/bin/env python3
from __future__ import annotations
import py_compile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TEST=ROOT/'tests'/'test_stegmusic_browser.py'
WORKFLOW=ROOT/'.github'/'workflows'/'stegmusic-browser-execution.yml'
def fail(message):
    print(f'STEGMUSIC_BROWSER_AUTOMATION_FAIL: {message}')
    return 1
def main():
    for path in (TEST,WORKFLOW):
        if not path.exists(): return fail(f'missing {path.relative_to(ROOT)}')
    try: py_compile.compile(str(TEST),doraise=True)
    except py_compile.PyCompileError as error: return fail(f'browser test does not compile: {error.msg}')
    test=TEST.read_text(encoding='utf-8'); workflow=WORKFLOW.read_text(encoding='utf-8')
    for marker in ['#playPause','#adaptiveNext','#progress','playback_started','adaptive_selection_decision','playback_paused','browser_audio_execution_verified','audible_output_confirmed','activation_authority_granted','stegmusic-browser-execution.json','REPORT','event_types','page_errors']:
        if marker not in test: return fail(f'browser test missing marker: {marker}')
    for field in ['audible_output_confirmed','catalog_license_verified','custody_verified_by_this_check','activation_authority_granted']:
        if not any(token in test for token in (f"'{field}':False",f"'{field}': False",f'"{field}":False',f'"{field}": False')):
            return fail(f'browser test must keep {field}=false')
    for marker in ['StegMusic Browser Execution','python -m playwright install --with-deps chromium','python -m http.server 8000','python tests/test_stegmusic_browser.py','Upload browser execution receipt','reports/stegmusic-browser-execution.json','if: always()']:
        if marker not in workflow: return fail(f'workflow missing marker: {marker}')
    print('STEGMUSIC_BROWSER_AUTOMATION_PASS'); print('authority_effect=NONE'); return 0
if __name__=='__main__': raise SystemExit(main())
