#!/usr/bin/env python3
"""Validate the machine-readable and human/raw CACS public projection contract."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PACKET=ROOT/'data/cacs-public-projection.fixture.json'
PAGE=ROOT/'cacs-claims.html'
SCRIPT=ROOT/'assets/cacs-claims.js'

def fail(message:str)->None: raise ValueError(message)
def load(path:Path):
    if not path.is_file(): fail(f'missing {path.relative_to(ROOT)}')
    return json.loads(path.read_text(encoding='utf-8'))
def main()->int:
    try:
        p=load(PACKET)
        required={'projection_id','standard','generated_at','active_claim','historical_claims','suppressed_claims','qualification_rules','authority_effect','hash'}
        if set(p)!=required: fail('projection packet shape is not closed')
        if p['authority_effect']!='NONE': fail('authority_effect must be NONE')
        active=p['active_claim']
        if active.get('public_label')!='CURRENT_BOUNDED_CLAIM' or active.get('lifecycle_state')!='active': fail('active claim label/lifecycle invalid')
        if active.get('correspondence_status') not in {'supported','partially_supported'}: fail('current claim must be bounded support')
        if active.get('evidence_dimensions',{}).get('scope_correspondent')!='ESTABLISHED': fail('current claim must be scope correspondent')
        if not active.get('not_established') or not active.get('qualification'): fail('current claim requires non-claims and qualifications')
        historical={x['public_label'] for x in p['historical_claims']}
        suppressed={x['public_label'] for x in p['suppressed_claims']}
        if not {'SUPERSEDED_HISTORY','STALE_HISTORY'}<=historical: fail('historical lifecycle labels incomplete')
        if not {'WITHDRAWN_SUPPRESSED','OVERSTATED_QUARANTINED'}<=suppressed: fail('suppression labels incomplete')
        ids=[active['claim_id']]+[x['claim_id'] for x in p['historical_claims']]+[x['claim_id'] for x in p['suppressed_claims']]
        if len(ids)!=len(set(ids)): fail('claim appears in multiple projection classes')
        page=PAGE.read_text(encoding='utf-8'); script=SCRIPT.read_text(encoding='utf-8')
        for marker in ('human-view','raw-view','CURRENT_BOUNDED_CLAIM','data/cacs-public-projection.fixture.json'):
            if marker not in page: fail(f'page marker missing: {marker}')
        for marker in ('active_claim','historical_claims','suppressed_claims','JSON.stringify'):
            if marker not in script: fail(f'renderer marker missing: {marker}')
    except (ValueError,KeyError,json.JSONDecodeError) as exc:
        print(f'CACS_PUBLIC_PROJECTION_FAIL: {exc}'); return 1
    print('CACS_PUBLIC_PROJECTION_PASS: active, historical, suppressed, human, and raw projections verified'); return 0
if __name__=='__main__': raise SystemExit(main())
