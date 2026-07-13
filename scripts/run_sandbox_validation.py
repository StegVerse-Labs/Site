#!/usr/bin/env python3
from __future__ import annotations
import json, shutil, subprocess, tempfile, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PROFILE=ROOT/'templates/sandbox-first/site.sandbox-profile.json'
REPORT=ROOT/'reports/sandbox-first-validation.report.json'
def main()->int:
 p=json.loads(PROFILE.read_text())
 REPORT.parent.mkdir(parents=True,exist_ok=True)
 results=[]; status='PASS'
 with tempfile.TemporaryDirectory(prefix='site-st017-') as td:
  sb=Path(td)/'repo'; shutil.copytree(ROOT,sb,ignore=shutil.ignore_patterns(*p.get('exclude',[]))); (sb/'reports').mkdir(exist_ok=True)
  for c in p['commands']:
   t=time.monotonic()
   try:
    r=subprocess.run(c['argv'],cwd=sb,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=p.get('timeout_seconds',600),check=False)
    code=r.returncode; out=r.stdout[-5000:]; err=r.stderr[-5000:]; timed=False
   except subprocess.TimeoutExpired as e:
    code=None; out=''; err=str(e); timed=True
   ok=(not timed and code==c.get('expected_exit',0)); results.append({'id':c['id'],'argv':c['argv'],'actual_exit':code,'passed':ok,'timed_out':timed,'duration_seconds':round(time.monotonic()-t,3),'stdout_tail':out,'stderr_tail':err})
   if not ok: status='FAIL'; break
 report={'schema_version':'1.0.0','record_type':'sandbox_validation_report','repository':p['repository'],'profile_id':p['profile_id'],'sandbox_status':status,'github_actions_status':'NOT_OBSERVED','public_output_status':'NOT_VERIFIED','results':results,'non_claims':{'deployment_authority':False,'transport_activation':False,'custody_recorded':False,'release_authority':False,'admissibility':False}}
 REPORT.write_text(json.dumps(report,indent=2)+'\n')
 print('SITE ST-017 SANDBOX:',status)
 for x in results: print(x['id']+':', 'PASS' if x['passed'] else 'FAIL')
 return 0 if status=='PASS' else 1
if __name__=='__main__': raise SystemExit(main())
