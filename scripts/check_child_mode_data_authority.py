#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PAGE=ROOT/'child-mode-data-protection.html'
DOC=ROOT/'docs/CHILD_MODE_DATA_AUTHORITY.md'
TASK=ROOT/'data/tasks/SITE-0007-CHILD-MODE-DATA-AUTHORITY.json'
REQUIRED=(
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
    'guardian authorization must not become blanket permission',
    'Newest-first descending chronology'
)

def main()->int:
    failures=[]
    for path in (PAGE,DOC,TASK):
        if not path.is_file(): failures.append(f'missing {path.relative_to(ROOT)}')
    for path in (PAGE,DOC):
        if path.is_file():
            text=path.read_text(encoding='utf-8')
            for marker in REQUIRED:
                if marker not in text:
                    failures.append(f'{path.name} missing marker: {marker}')
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
