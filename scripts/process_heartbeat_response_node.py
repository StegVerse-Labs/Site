#!/usr/bin/env python3
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen
ROOT=Path(__file__).resolve().parents[1]; CONFIG=ROOT/'data'/'heartbeat-response-node.json'; RECEIPTS=ROOT/'data'/'heartbeat-response-receipts'; AUTH_KEYS=('execution','activation','publication','custody','release')
def canonical_sha256(v): return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def load_json(p): return json.loads(p.read_text(encoding='utf-8'))
def authority_is_false(v): return all(v.get(k) is False for k in AUTH_KEYS)
def select_message(batch,org):
 m=[x for x in batch.get('messages',[]) if x.get('destination_org')==org]
 if len(m)!=1: raise ValueError(f'expected one canonical message for {org}, found {len(m)}')
 m=m[0]
 if m.get('stage')!='SENT': raise ValueError('canonical inbound message is not SENT')
 if not authority_is_false(m.get('authority',{})): raise ValueError('inbound heartbeat attempts to grant authority')
 return m
def make_receipts(m,c,t):
 org=c['organization']; d=canonical_sha256(m); a={k:False for k in AUTH_KEYS}; common={'schema_version':'1.0.0','exchange_id':m['exchange_id'],'node_org':org,'source_org':m['source_org'],'destination_org':org,'observed_at':t,'observed_message_sha256':d,'authority':a}
 r={**common,'message_id':m['message_id']+'-received','stage':'RECEIVED','detail_class':m['detail_class'],'classification':{'primary':m['detail_class'],'retention':m.get('retention_class','EPHEMERAL'),'action_admitted':False,'awareness_updated':True}}
 s={**common,'message_id':m['message_id']+'-responded','stage':'RESPONDED','detail_class':c.get('response_detail_class','CAPABILITY'),'classification':{'primary':c.get('response_detail_class','CAPABILITY'),'supported_detail_classes':c['supported_detail_classes'],'node_state':'RESPONSIVE','return_to':m['source_org'],'action_admitted':False},'parent_receipt_sha256':canonical_sha256(r)}
 return r,s
def validate_local(c):
 if not c.get('organization') or not c.get('outbox_url'): raise ValueError('node configuration incomplete')
 if not authority_is_false(c.get('authority',{})): raise ValueError('node configuration attempts to grant transport authority')
 if RECEIPTS.exists():
  for p in RECEIPTS.glob('*.json'):
   x=load_json(p)
   if x.get('node_org')!=c['organization'] and not x.get('central_import',False): continue
   if x.get('stage') not in {'RECEIVED','RESPONDED','RECOVERED','REPEAT','BLOCKED','FAILED','REVIEW_REQUIRED'}: raise ValueError(f'invalid receipt stage in {p}')
   if not authority_is_false(x.get('authority',{})): raise ValueError(f'receipt attempts to grant authority in {p}')
def apply(c):
 with urlopen(c['outbox_url'],timeout=20) as response: batch=json.load(response)
 m=select_message(batch,c['organization']); RECEIPTS.mkdir(parents=True,exist_ok=True); prefix=m['exchange_id'].replace('/','-'); rp=RECEIPTS/(prefix+'.received.json'); sp=RECEIPTS/(prefix+'.responded.json')
 if rp.exists() and sp.exists(): print(f"HB_NODE_CURRENT:{c['organization']}:{m['exchange_id']}"); return
 t=datetime.now(timezone.utc).isoformat().replace('+00:00','Z'); r,s=make_receipts(m,c,t); rp.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n'); sp.write_text(json.dumps(s,indent=2,sort_keys=True)+'\n'); print(f"HB_NODE_RESPONDED:{c['organization']}:{m['exchange_id']}")
def main():
 p=argparse.ArgumentParser(); p.add_argument('--apply',action='store_true'); p.add_argument('--check',action='store_true'); a=p.parse_args(); c=load_json(CONFIG); validate_local(c)
 if a.apply: apply(c); validate_local(c)
 elif a.check: print(f"HB_NODE_CHECK_PASS:{c['organization']}")
 else: p.error('choose --apply or --check')
if __name__=='__main__': main()
