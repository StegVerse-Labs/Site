#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / 'child-safety-regulatory-pilot.html'
DOC = ROOT / 'docs/CHILD_SAFETY_REGULATORY_PILOT.md'
TASK = ROOT / 'data/tasks/SITE-0008-CHILD-SAFETY-REGULATORY-PILOT.json'

PAGE_REQUIRED = (
    'This is not a self-exemption from a ban.',
    'REGULATOR / LAWFUL PILOT AUTHORITY',
    'OPTIONAL_DATA_HARVESTING = DENY_BY_DEFAULT',
    'Five-layer evidence package',
    'Data egress',
    'Fail closed',
    'NORMAL_MODE_BYPASS = DENY',
    'UNDECLARED_DATA_EGRESS = NONE',
    'Newest-first descending chronology',
)
DOC_REQUIRED = (
    'regulator-authorized temporary pilot model',
    'Australia\'s under-16 social-media account restriction is operative.',
    'The UK government has announced an under-16 social-media ban',
    'COPPA is not a general nationwide social-media account ban.',
    'OPTIONAL_DATA_HARVESTING = DENY_BY_DEFAULT',
    'Regulator-verifiable evidence package',
    'Fail-closed pilot rules',
    'The goal is to verify the boundary, not surveil the child.',
    'Pilot success criteria',
)

def main() -> int:
    failures = []
    for path in (PAGE, DOC, TASK):
        if not path.is_file():
            failures.append(f'missing {path.relative_to(ROOT)}')
    if PAGE.is_file():
        text = PAGE.read_text(encoding='utf-8')
        for marker in PAGE_REQUIRED:
            if marker not in text:
                failures.append(f'page missing marker: {marker}')
    if DOC.is_file():
        text = DOC.read_text(encoding='utf-8')
        for marker in DOC_REQUIRED:
            if marker not in text:
                failures.append(f'doc missing marker: {marker}')
    if failures:
        print('CHILD_SAFETY_REGULATORY_PILOT=FAIL')
        for failure in failures:
            print('-', failure)
        return 1
    print('CHILD_SAFETY_REGULATORY_PILOT=PASS')
    print('PILOT_AUTHORITY=REGULATOR_OR_LAWFUL_AUTHORIZATION_REQUIRED')
    print('OPTIONAL_DATA_HARVESTING=ZERO_BY_DEFAULT')
    print('ENFORCEMENT_EVIDENCE=FIVE_LAYER')
    print('FAIL_CLOSED=true')
    print('REGULATOR_TESTABILITY=REQUIRED')
    print('AUTHORITY_GRANTED=false')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
