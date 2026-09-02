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
  return {worker:new Worker("/assets/sv002-principal-worker.js?v=20260902-0935"),url:null};
}

async function fetchText(path){
  var response=await fetch(path,{cache:"no-store",credentials:"omit"});
  if(!response.ok)throw new Error("principal_resource_http_"+response.status+":"+path);
  return response.text();
}
async function fetchJson(path){
  var text=await fetchText(path);
  return {text:text,value:JSON.parse(text)};
}
async function loadPrincipalResources(){
  var values=await Promise.all([
    fetchJson("/data/sv002-principal/model-manifest.json"),
    fetchJson("/data/sv002-principal/subject-identity.json"),
    fetchJson("/data/sv002-principal/experiment-contract.json"),
    fetchJson("/data/sv002-principal/environment.json"),
    fetchJson("/data/sv002-principal/capability-snapshot.json"),
    fetchJson("/data/sv002-principal/execution-implementation-profile.json"),
    fetchText("/assets/sv002-principal-worker.js?v=20260902-0935")
  ]);
  require(values[0].value.model_id==="stegverse-sv002-evidence-principal-v1","principal_model_identity_mismatch");
  require(values[5].value.implementation_version==="v0.8-browser-resident","principal_implementation_profile_mismatch");
  return {
    model_manifest:values[0].value,
    model_digest:await sha256(values[0].text),
    implementation_profile:values[5].value,
    implementation_profile_digest:await sha256(values[5].text),
    runtime_digest:await sha256(values[6]),
    resources:{
      subject_identity:values[1].value,
      experiment_contract:values[2].value,
      environment:values[3].value,
      capability_snapshot:values[4].value
    }
  };
}

function waitMessage(worker,type,timeoutMs){
  return new Promise(function(resolve,reject){
    var t=setTimeout(function(){cleanup();reject(new Error("runtime_"+type.toLowerCase()+"_timeout"));},timeoutMs||5000);
    function handler(e){
      if(e.data&&e.data.type===type){cleanup();resolve(e.data);}
      else if(e.data&&["BLOCKED","SV002_BLOCKED"].indexOf(e.data.type)>=0){cleanup();reject(new Error(e.data.error||"runtime_blocked"));}
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
    try{active.worker.terminate();if(active.url)URL.revokeObjectURL(active.url);}catch(_e){}
    active=null;
  }
  var runtimeId=randomId("SV002-WEBRUNTIME-");
  var leaseId=randomId("SV002-LEASE-");
  var principal=await loadPrincipalResources();
  var rec=createWorker();
  await waitMessage(rec.worker,"BOOTED",5000);
  var nodeIdentity={node_id:node.registration.node_id,interlock_id:node.registration.interlock_id};
  rec.worker.postMessage({
    type:"EXECUTE_SV002",
    runtime_id:runtimeId,
    lease_id:leaseId,
    entry:entry,
    node:nodeIdentity,
    resources:principal.resources,
    model_digest:principal.model_digest,
    runtime_digest:principal.runtime_digest,
    implementation_profile_digest:principal.implementation_profile_digest
  });
  var completed=await waitMessage(rec.worker,"SV002_COMPLETE",15000);
  var execution=completed.receipt;
  require(execution&&execution.state==="COMPLETED"&&execution.principal_run_completed===true,"principal_execution_not_completed");
  var receipt={
    schema:"stegverse.sv002-browser-runtime-materialization/v2",
    state:"PRINCIPAL_COMPLETED",
    observed_at:new Date().toISOString(),
    runtime_class:"EVENT_EPHEMERAL",
    runtime_substrate:"BROWSER_WEB_WORKER_ON_VALID_STEGVERSE_NODE",
    runtime_id:runtimeId,
    lease_id:leaseId,
    node_id:node.registration.node_id,
    interlock_id:node.registration.interlock_id,
    materialization_id:execution.materialization_id,
    request_hash:execution.request_hash,
    consumer:"SV002_PUBLIC_OBSERVATION",
    principal_execution_attempted:true,
    principal_execution_state:"COMPLETED",
    principal_model_id:execution.model_id,
    principal_model_artifact_sha256:execution.model_artifact_sha256,
    principal_runtime_source_sha256:execution.runtime_source_sha256,
    principal_execution_receipt_sha256:execution.receipt_sha256,
    principal_execution_receipt:execution,
    canonical_principal_source:{
      repository:"StegVerse-002/micro-node-runtime",
      model_source_commit:"41a6bafa1ee6fd46bcf53ae16922c3984a95c544",
      worker_source_commit:"b4b9be713f74a96aaf2d7b391f1f2cb6f1fb8e0a",
      model_manifest_commit:"871d6c6ae1d45c59b246a061f9ef0e806214b760",
      implementation_profile_commit:"e3869fa700dc32f4f272c75696d258f76367a13a"
    },
    second_user_device_required:false,
    public_gateway_required_for_local_materialization:false,
    credential_authority:"TV/TVC",
    github_token_runtime_authority:"NONE",
    authority_effect:"NONE"
  };
  receipt.receipt_sha256=await sha256(receipt);
  localStorage.setItem(STORAGE_KEY,canonical(receipt));
  localStorage.setItem("stegverse.sv002.principal-execution.latest.v1",canonical(execution));
  if(typeof root.StegVerseNodeContinuity.recordStep==="function"){
    await root.StegVerseNodeContinuity.recordStep(CAPABILITY,"principal-completed","OBSERVED",receipt.receipt_sha256);
  }
  active={worker:rec.worker,url:null,receipt:receipt,execution:execution};
  root.__STEGVERSE_SV002_LOCAL_RUNTIME__=active;
  return receipt;
}

function release(){
  if(!active)return null;
  try{active.worker.terminate();if(active.url)URL.revokeObjectURL(active.url);}catch(_e){}
  var receipt=active.receipt; active=null; root.__STEGVERSE_SV002_LOCAL_RUNTIME__=null; return receipt;
}
root.StegVerseSV002LocalRuntime=Object.freeze({materialize:materialize,release:release,storage_key:STORAGE_KEY});
}(typeof globalThis!=="undefined"?globalThis:window));
