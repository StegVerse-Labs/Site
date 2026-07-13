#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PROFILE=ROOT/'templates/sandbox-first/site.sandbox-profile.json'; RUNNER=ROOT/'scripts/run_sandbox_validation.py'; WORKFLOW=ROOT/'.github/workflows/validate.yml'; ADOPTION=ROOT/'docs/ST017_SITE_ADOPTION_HANDOFF.md'; SOURCE=ROOT/'docs/SITE_MIRROR_HANDOFF.md'
def main()->int:
 argparse.ArgumentParser().add_argument('--structural-only',action='store_true').parse_args(); errors=[]
 for p in [PROFILE,RUNNER,WORKFLOW,ADOPTION,SOURCE]:
  if not p.exists(): errors.append('missing:'+str(p.relative_to(ROOT)))
 if PROFILE.exists():
  d=json.loads(PROFILE.read_text()); ids=[x.get('id') for x in d.get('commands',[])]
  if d.get('repository')!='StegVerse-Labs/Site': errors.append('profile_repository_mismatch')
  for x in ['compile-python','write-workflow-inventory','validate-workflow-inventory','validate-application','validate-st017-adoption']:
   if x not in ids: errors.append('profile_missing:'+x)
 if WORKFLOW.exists():
  t=WORKFLOW.read_text()
  for x in ['st017-sandbox:','python scripts/run_sandbox_validation.py','site-st017-sandbox-report','needs: st017-sandbox']:
   if x not in t: errors.append('workflow_missing:'+x)
 if ADOPTION.exists():
  t=ADOPTION.read_text()
  for x in ['SANDBOX: NOT_RUN','PUBLIC_OUTPUT: NOT_VERIFIED','No release tag is authorized.']:
   if x not in t: errors.append('adoption_missing:'+x)
 if errors: print('SITE ST-017 ADOPTION: FAIL - '+', '.join(errors)); return 1
 print('SITE ST-017 ADOPTION: PASS'); return 0
if __name__=='__main__': raise SystemExit(main())
