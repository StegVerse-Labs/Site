#!/usr/bin/env python3
import argparse,hashlib,json,os
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];C=json.loads((ROOT/".stegverse/transition-ledger/contract.json").read_text())
def canon(v):return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
def sha(v):return "sha256:"+hashlib.sha256(v if isinstance(v,(bytes,bytearray)) else canon(v)).hexdigest()
def lr():
 o=os.getenv("STEGVERSE_REPO_LEDGER_ROOT")
 if o:return Path(o).expanduser().resolve()
 return (Path(os.getenv("XDG_STATE_HOME",str(Path.home()/".local/state")))/"stegverse/repo-ledgers"/C["repository"]).resolve()
def main():
 p=argparse.ArgumentParser();p.add_argument("--transition-id",required=True);p.add_argument("--transition-class",required=True);p.add_argument("--predecessor-state-sha256",required=True);p.add_argument("--successor-state-sha256",required=True);p.add_argument("--evidence-json",default="{}");p.add_argument("--authority-effect",default="NONE");p.add_argument("--hb-ref");a=p.parse_args()
 root=lr();d=root/"receipts";d.mkdir(parents=True,exist_ok=True);h=root/"HEAD.json";prev=json.loads(h.read_text()).get("receipt_sha256") if h.exists() else None
 b={"schema":"stegverse.repo-transition-receipt/v1","repository":C["repository"],"transition_id":a.transition_id,"transition_class":a.transition_class,"predecessor_state_sha256":a.predecessor_state_sha256,"successor_state_sha256":a.successor_state_sha256,"evidence":json.loads(a.evidence_json),"authority_effect":a.authority_effect,"hb_reference":a.hb_ref,"observed_at":datetime.now(timezone.utc).isoformat(),"previous_receipt_sha256":prev};dg=sha(b);r={**b,"receipt_sha256":dg};fp=d/(dg.split(":",1)[1]+".json")
 if fp.exists() and json.loads(fp.read_text())!=r:raise SystemExit("receipt collision")
 if not fp.exists():fp.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
 h.write_text(json.dumps({"repository":C["repository"],"receipt_sha256":dg,"receipt_path":str(fp)},indent=2,sort_keys=True)+"\n");print(json.dumps(r,sort_keys=True))
if __name__=="__main__":main()
