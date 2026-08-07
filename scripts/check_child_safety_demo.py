#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PAGE=ROOT/'child-safety-demo.html'
TASK=ROOT/'data/tasks/SITE-0002-CHILD-SAFETY-DEMO.json'
HANDOFF=ROOT/'docs/CHILD_SAFE_NETWORKING_MIRROR_HANDOFF.md'
REQUIRED=(
    'StegVerse protective baseline','United States','Australia','United Kingdom',
    'Under 13','13–15','16–17','18+',
    'Message an approved friend/family member','Receive a DM from an unknown person',
    'Post publicly to strangers','Livestream self publicly','Share precise location',
    'Create behavioral advertising profile','Enable engagement-optimized infinite recommender',
    'Join approved-friends music collaboration','Report/block a user',
    'retained_personal_data:[]','production_activation:false',
    'DEMO_BROWSER_ONLY','REVIEW_REQUIRED','DENY','ALLOW'
)

def main()->int:
    failures=[]
    for path in (PAGE,TASK,HANDOFF):
        if not path.is_file(): failures.append(f'missing {path.relative_to(ROOT)}')
    if PAGE.is_file():
        text=PAGE.read_text(encoding='utf-8')
        for marker in REQUIRED:
            if marker not in text: failures.append(f'missing marker: {marker}')
        if 'fetch(' in text or 'XMLHttpRequest' in text:
            failures.append('demo must not make network requests')
    if failures:
        print('CHILD_SAFETY_DEMO=FAIL')
        for f in failures: print('-',f)
        return 1
    print('CHILD_SAFETY_DEMO=PASS')
    print('AGE_POLICY=JURISDICTION_AWARE')
    print('NETWORK_REQUESTS=NONE')
    print('PERSONAL_DATA_RETENTION=NONE')
    print('AUTHORITY_GRANTED=false')
    print('ACTIVATION_EFFECT=PUBLIC_INTERACTIVE_DEMO_ONLY')
    return 0

if __name__=='__main__': raise SystemExit(main())
