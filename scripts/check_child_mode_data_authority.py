#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PAGE=ROOT/'child-mode-data-protection.html'
DOC=ROOT/'docs/CHILD_MODE_DATA_AUTHORITY.md'
TASK=ROOT/'data/tasks/SITE-0007-CHILD-MODE-DATA-AUTHORITY.json'
PAGE_REQUIRED=(
    'OPTIONAL_DATA_HARVESTING = DENY_BY_DEFAULT',
    'contacts / address book',
    'Photos / videos / files',
    'Precise or background location',
    'Microphone / camera-derived data',
    'Clipboard',
    'Advertising identifiers',
    'Cross-app / cross-service identifiers',
    'Behavioral profile / inferred interests',
    'Child Mode does not encode the claim that every person under 18 is legally incapable of every form of consent',
    'guardian consent only authorizes the exact scoped purpose',
    'Newest changes first; older history remains below.'
)
DOC_REQUIRED=(
    'OPTIONAL_DATA_HARVESTING = DENY_BY_DEFAULT',
    'child-visible click, tap, toggle, or acceptance flow',
    'contacts and address book',
    'photos, videos and files',
    'precise and background location',
    'microphone and camera-derived data',
    'clipboard contents',
    'advertising identifiers',
    'cross-app and cross-service identifiers',
    'behavioral profiles and inferred interests',
    'Guardian authorization must not become blanket permission.',
    'Newest-first descending chronology.'
)

def check(path: Path, markers: tuple[str,...], failures: list[str]) -> None:
    if not path.is_file():
        failures.append(f'missing {path.relative_to(ROOT)}')
        return
    text=path.read_text(encoding='utf-8')
    for marker in markers:
        if marker not in text:
            failures.append(f'{path.name} missing marker: {marker}')

def main()->int:
    failures=[]
    check(PAGE,PAGE_REQUIRED,failures)
    check(DOC,DOC_REQUIRED,failures)
    if not TASK.is_file(): failures.append(f'missing {TASK.relative_to(ROOT)}')
    if failures:
        print('CHILD_MODE_DATA_AUTHORITY=FAIL')
        for f in failures: print('-',f)
        return 1
    print('CHILD_MODE_DATA_AUTHORITY=PASS')
    print('OPTIONAL_DATA_HARVESTING=DENY_BY_DEFAULT')
    print('CHILD_UI_CONSENT=NOT_SUFFICIENT_HARVESTING_AUTHORITY')
    print('GUARDIAN_AUTHORIZATION=PURPOSE_SCOPED')
    print('DEVICE_DATA_BOUNDARY=PROTECTED')
    print('AUTHORITY_GRANTED=false')
    return 0

if __name__=='__main__': raise SystemExit(main())
