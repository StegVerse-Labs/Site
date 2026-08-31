#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, ssl, urllib.error, urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
CONFIG=ROOT/"data/ecosystem-chat-gateway.json"
REPORT=ROOT/"reports/evaluator-intr-public-route-observation.json"
NODE_PATH="/api/stegverse-node"
READINESS_PATH="/intr/evaluator/readiness"
EVALUATOR_PATH="/intr/evaluator"

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):
        raise urllib.error.HTTPError(args[0].full_url,args[0].code,"redirect_forbidden",args[0].headers,None)

def canonical(v): return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
def sha256(v): return hashlib.sha256(canonical(v)).hexdigest()

def fetch(url,expected_path):
    p=urlparse(url)
    if p.scheme!="https" or p.path!=expected_path or p.username or p.password or p.query or p.fragment:
        raise ValueError(f"url_invalid:{url}")
    req=urllib.request.Request(url,headers={"Accept":"application/json","User-Agent":"StegVerse-Site-Evaluator-Observer/1"})
    opener=urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl.create_default_context()),NoRedirect())
    with opener.open(req,timeout=20) as r:
        raw=r.read(65537)
        if r.status!=200: raise ValueError(f"http_status:{r.status}")
        if len(raw)>65536: raise ValueError("response_too_large")
    obj=json.loads(raw.decode())
    if not isinstance(obj,dict): raise ValueError("response_object_required")
    return obj

def main():
    cfg=json.loads(CONFIG.read_text())
    candidates=[x for x in cfg.get("discovery",{}).get("advertisement_endpoints",[]) if str(x).startswith("https://")]
    result={"schema":"stegverse.site.evaluator_intr_public_route_observation/v1","observed_at":datetime.now(timezone.utc).isoformat(),"authority_effect":"NONE","credential_material_present":False,"github_runtime_authority":"NONE","candidates":candidates}
    if not candidates:
        result.update(state="BLOCKED",reason="no_https_advertisement_candidate")
        code=2
    else:
        node_url=candidates[0]
        try:
            node=fetch(node_url,NODE_PATH)
            expected={
              "schema":"stegverse.node.endpoint-advertisement.v1",
              "health_bound":True,
              "credential_authority":"TV/TVC",
              "github_token_runtime_authority":"NONE",
              "authority_granted":False,
              "publication_authority":False,
              "execution_authority":False,
              "evaluator_intr_transport":"InTr",
              "evaluator_intr_gateway_authority":"NONE",
            }
            mismatches={k:{"expected":v,"observed":node.get(k)} for k,v in expected.items() if node.get(k)!=v}
            claimed=node.get("advertisement_sha256")
            material={k:v for k,v in node.items() if k!="advertisement_sha256"}
            if not isinstance(claimed,str) or claimed!=sha256(material):
                mismatches["advertisement_sha256"]="invalid"
            readiness_url=str(node.get("evaluator_intr_readiness_endpoint") or "")
            endpoint=str(node.get("evaluator_intr_endpoint") or "")
            np=urlparse(node_url); rp=urlparse(readiness_url); ep=urlparse(endpoint)
            origin=(np.scheme,np.hostname,np.port)
            if (rp.scheme,rp.hostname,rp.port)!=origin or rp.path!=READINESS_PATH: mismatches["readiness_origin"]="invalid"
            if (ep.scheme,ep.hostname,ep.port)!=origin or ep.path!=EVALUATOR_PATH: mismatches["endpoint_origin"]="invalid"
            if mismatches: raise ValueError("node_contract:"+json.dumps(mismatches,sort_keys=True))
            readiness=fetch(readiness_url,READINESS_PATH)
            rex={
              "schema":"stegverse.service-gateway.evaluator-intr-readiness/v1",
              "enabled":True,
              "loopback_upstream_configured":True,
              "runtime_receiver_ready":True,
              "state":"READY",
              "transport":"InTr",
              "credential_authority":"TV/TVC",
              "gateway_receipt_authority":False,
              "gateway_evaluator_authority":False,
              "authority_effect":"NONE",
            }
            rm={k:{"expected":v,"observed":readiness.get(k)} for k,v in rex.items() if readiness.get(k)!=v}
            if rm: raise ValueError("readiness_contract:"+json.dumps(rm,sort_keys=True))
            result.update(state="OBSERVED",node_url=node_url,node_id=node.get("node_id"),endpoint=endpoint,readiness_endpoint=readiness_url,node_advertisement_sha256="sha256:"+claimed,readiness_sha256="sha256:"+sha256(readiness),runtime_receiver_ready=True,transport="InTr",credential_authority="TV/TVC",gateway_authority="NONE")
            code=0
        except Exception as e:
            result.update(state="BLOCKED",node_url=node_url,reason=str(e))
            code=2
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    REPORT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,sort_keys=True))
    return code

if __name__=="__main__": raise SystemExit(main())
