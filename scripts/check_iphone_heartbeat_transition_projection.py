#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
HTML=ROOT/'heartbeat-transition'/'index.html'; JS=ROOT/'heartbeat-transition'/'heartbeat-transition.js'; HANDOFF=ROOT/'docs'/'IPHONE_HEARTBEAT_TRANSITION_PROJECTION_MIRROR_HANDOFF.md'
def main():
 f=[]
 for p in (HTML,JS,HANDOFF):
  if not p.is_file(): f.append(f'missing projection file: {p.relative_to(ROOT)}')
 if f:
  [print('IPHONE_HB30_PROJECTION_FAIL:'+x) for x in f]; return 1
 h=HTML.read_text(); j=JS.read_text(); d=HANDOFF.read_text()
 for m in ('HB29 → HB30 transition capsule','SHWP-IPHONE-HB30-TRANSITION-CAPSULE-001','HB29 / generation 29','HB30 / generation 30','TV/TVC','Generate portable HB30 receipt','./heartbeat-transition.js','independently verified','WorkerCoordinator'):
  if m not in h:f.append('html missing marker: '+m)
 for m in ('https://stegverse.org','SHWP-IPHONE-HB30-TRANSITION-CAPSULE-001','d18d57d83cf19b7799cde1a1b4487e496eca7f76','stegverse.iphone-heartbeat-transition-receipt/v1','CURRENT_USER_IPHONE','StegVerse-Labs/.github','control/heartbeat-state.json','stegverse.heartbeat-carrier-runtime-state/v1','heartbeat_epoch:30',"credential_authority:'TV/TVC'","credential_requirement:'NONE'","github_token_runtime_authority:'NONE'",'non_tv_tvc_secret_or_token_used:false','worker_authority:false','claim_or_fence_mutation:false','route_authority:false','wallet_authority:false',"model_output_authority:'NONE'","hosted_runtime_production_authority:'NONE'",'another_physical_machine_required:false',"navigator.userAgent.includes('iPhone')",'window.isSecureContext!==true',"crypto.subtle.digest('SHA-256'",'localStorage.setItem(STORAGE_KEY','receipt.receipt_sha256=await sha256Hex(canonicalize(receipt))'):
  if m not in j:f.append('javascript missing marker: '+m)
 for m in ('fetch(','XMLHttpRequest','WebSocket','EventSource','Authorization','Bearer ','GITHUB_TOKEN','GH_TOKEN','TVC_TOKEN','private_key','seed_phrase','eth_sendTransaction','eth_sendRawTransaction','personal_sign','window.ethereum','api.github.com','RENDER'):
  if m in j:f.append('javascript contains prohibited marker: '+m)
 for m in ('SITE-IPHONE-HB30-TRANSITION-PROJECTION-001','StegVerse-Labs/Site#358','StegVerse-Labs/.github#209','SHWP-DURABLE-RUNTIME-ACTIVATION / G18','credential_authority: TV/TVC','github_token_runtime_authority: NONE','non_tv_tvc_secret_or_token_allowed: false','Publication alone is not HB30 activation','CURRENT_USER_IPHONE portable receipt','independent WorkerCoordinator'):
  if m not in d:f.append('handoff missing marker: '+m)
 if 'epoch:29,generation:29' not in j:f.append('seed must remain exactly HB29/generation29')
 if 'epoch:30,generation:30' not in j:f.append('successor must remain exactly HB30/generation30')
 if 'location.origin!==EXPECTED_ORIGIN' not in j:f.append('origin must fail closed')
 if f:
  [print('IPHONE_HB30_PROJECTION_FAIL:'+x) for x in f]; return 1
 print('IPHONE_HB30_PROJECTION_PASS surface=stegverse.org/heartbeat-transition authority_effect=NONE credential_authority=TV/TVC github_token_runtime_authority=NONE physical_activation_claimed=false'); return 0
if __name__=='__main__': raise SystemExit(main())
