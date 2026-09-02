(function(root){
"use strict";
var CAPABILITY="sv002-local-runtime-materializer";
var STORAGE_KEY="stegverse.sv002.local-runtime.latest.v1";
var active=null;

function canonical(v){
  if(v===null||typeof v!=="object")return JSON.stringify(v);
  if(Array.isArray(v))return "["+v.map(canonical).join(",")+"]";
  return "{"+Object.keys(v).sort().map(function(k){return JSON.stringify(k)+":"+canonical(v[k]);}).join(",")+"}";
}
function hex(bytes){return Array.from(bytes).map(function(b){return b.toString(16).padStart(2,"0");}).join("");}
async function sha256(v){
  var bytes=new TextEncoder().encode(typeof v==="string"?v:canonical(v));
  return "sha256:"+hex(new Uint8Array(await crypto.subtle.digest("SHA-256",bytes)));
}
function randomId(prefix){var b=new Uint8Array(12);crypto.getRandomValues(b);return prefix+hex(b);}
function require(ok,msg){if(!ok)throw new Error(msg);}

function createWorker(){
  var code=`
self.postMessage({type:"BOOTED"});
self.onmessage=async function(event){
  var m=event.data||{};
  if(m.type!=="MATERIALIZE")return;
  try{
    var e=m.entry||{}, r=e.materialization_request||{};
    function req(ok,msg){if(!ok)throw new Error(msg);}
    req(e.schema==="stegos.node_intr_outbox_entry.v1","outbox_schema_mismatch");
    req(e.state==="LOCAL_OUTBOX_PENDING_NETWORK_DELIVERY","outbox_state_mismatch");
    req(r.schema==="stegverse.universal-intr-materialization-request/v1","materialization_schema_mismatch");
    req(r.state==="QUEUED_FOR_EVENT_EPHEMERAL_MATERIALIZATION","materialization_state_mismatch");
    req(r.event_triggered===true,"event_trigger_required");
    req(r.always_on_receiver_required===false,"always_on_receiver_forbidden");
    req(r.second_user_device_required===false,"second_device_forbidden");
    req(r.request_grants_execution_authority===false,"request_authority_forbidden");
    req(r.claim_or_fence_minted===false,"claim_fence_forbidden");
    req(r.credential_authority==="TV/TVC","credential_authority_mismatch");
    req(r.github_token_runtime_authority==="NONE","github_runtime_authority_forbidden");
    req(r.destination&&r.destination.boundary==="STEGOS_ECOSYSTEM","destination_boundary_mismatch");
    req(r.destination&&r.destination.subsystem==="SV002:PublicObservation","destination_subsystem_mismatch");
    self.postMessage({
      type:"LOCAL_READY",
      runtime_id:m.runtime_id,
      lease_id:m.lease_id,
      materialization_id:r.materialization_id,
      request_hash:r.request_hash,
      state:"LOCAL_READY",
      consumer:"SV002_PUBLIC_OBSERVATION",
      principal_execution_attempted:false,
      principal_execution_state:"AWAITING_QUALIFYING_LOCAL_PRINCIPAL",
      credential_authority:"TV/TVC",
      github_token_runtime_authority:"NONE",
      authority_effect:"NONE"
    });
  }catch(err){
    self.postMessage({type:"BLOCKED",error:String(err&&err.message||err)});
  }
};
`;
  var url=URL.createObjectURL(new Blob([code],{type:"text/javascript"}));
  return {worker:new Worker(url),url:url};
}

function waitMessage(worker,type,timeoutMs){
  return new Promise(function(resolve,reject){
    var t=setTimeout(function(){cleanup();reject(new Error("runtime_"+type.toLowerCase()+"_timeout"));},timeoutMs||5000);
    function handler(e){
      if(e.data&&e.data.type===type){cleanup();resolve(e.data);}
      else if(e.data&&e.data.type==="BLOCKED"){cleanup();reject(new Error(e.data.error||"runtime_blocked"));}
    }
    function cleanup(){clearTimeout(t);worker.removeEventListener("message",handler);}
    worker.addEventListener("message",handler);
    worker.addEventListener("error",function(e){cleanup();reject(e.error||new Error("runtime_worker_error"));},{once:true});
  });
}

async function materialize(entry){
  require(root.StegVerseNodeContinuity&&typeof root.StegVerseNodeContinuity.status==="function","StegVerse Node continuity unavailable");
  var node=await root.StegVerseNodeContinuity.status();
  require(node&&node.registered===true,"valid StegVerse Node required");
  if(active&&active.worker){
    try{active.worker.terminate();URL.revokeObjectURL(active.url);}catch(_e){}
    active=null;
  }
  var runtimeId=randomId("SV002-WEBRUNTIME-");
  var leaseId=randomId("SV002-LEASE-");
  var rec=createWorker();
  await waitMessage(rec.worker,"BOOTED",5000);
  rec.worker.postMessage({type:"MATERIALIZE",runtime_id:runtimeId,lease_id:leaseId,entry:entry});
  var ready=await waitMessage(rec.worker,"LOCAL_READY",5000);
  var receipt={
    schema:"stegverse.sv002-browser-runtime-materialization/v1",
    state:"LOCAL_READY",
    observed_at:new Date().toISOString(),
    runtime_class:"EVENT_EPHEMERAL",
    runtime_substrate:"BROWSER_WEB_WORKER_ON_VALID_STEGVERSE_NODE",
    runtime_id:runtimeId,
    lease_id:leaseId,
    node_id:node.registration.node_id,
    interlock_id:node.registration.interlock_id,
    materialization_id:ready.materialization_id,
    request_hash:ready.request_hash,
    consumer:"SV002_PUBLIC_OBSERVATION",
    principal_execution_attempted:false,
    principal_execution_state:"AWAITING_QUALIFYING_LOCAL_PRINCIPAL",
    second_user_device_required:false,
    public_gateway_required_for_local_materialization:false,
    credential_authority:"TV/TVC",
    github_token_runtime_authority:"NONE",
    authority_effect:"NONE"
  };
  receipt.receipt_sha256=await sha256(receipt);
  localStorage.setItem(STORAGE_KEY,canonical(receipt));
  if(typeof root.StegVerseNodeContinuity.recordStep==="function"){
    await root.StegVerseNodeContinuity.recordStep(CAPABILITY,"runtime-local-ready","OBSERVED",receipt.receipt_sha256);
  }
  active={worker:rec.worker,url:rec.url,receipt:receipt};
  root.__STEGVERSE_SV002_LOCAL_RUNTIME__=active;
  return receipt;
}

function release(){
  if(!active)return null;
  try{active.worker.terminate();URL.revokeObjectURL(active.url);}catch(_e){}
  var receipt=active.receipt; active=null; root.__STEGVERSE_SV002_LOCAL_RUNTIME__=null; return receipt;
}
root.StegVerseSV002LocalRuntime=Object.freeze({materialize:materialize,release:release,storage_key:STORAGE_KEY});
}(typeof globalThis!=="undefined"?globalThis:window));
