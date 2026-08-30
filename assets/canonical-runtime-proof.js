(function(root){
"use strict";
var CAPABILITY="canonical-runtime-proof";
var PROOF_OPERATION="CANONICAL_RUNTIME_PROOF";
var DESTINATION_SUBSYSTEM="StegOS:CanonicalRuntime";
var STORAGE_KEY="stegverse.canonical-runtime.evidence.latest.v1";

function el(id){return document.getElementById(id);}
function setText(id,v){var n=el(id);if(n)n.textContent=String(v==null?"":v);}
function canonical(v){
  if(v===null||typeof v!=="object")return JSON.stringify(v);
  if(Array.isArray(v))return "["+v.map(canonical).join(",")+"]";
  return "{"+Object.keys(v).sort().map(function(k){return JSON.stringify(k)+":"+canonical(v[k]);}).join(",")+"}";
}
function bytesToHex(bytes){return Array.from(bytes).map(function(b){return b.toString(16).padStart(2,"0");}).join("");}
async function sha256(value){
  var bytes=value instanceof Uint8Array?value:new TextEncoder().encode(typeof value==="string"?value:canonical(value));
  var digest=await crypto.subtle.digest("SHA-256",bytes);
  return bytesToHex(new Uint8Array(digest));
}
async function shaUri(value){return "sha256:"+await sha256(value);}
function require(ok,msg){if(!ok)throw new Error(msg);}
function randomHex(n){var b=new Uint8Array(n);crypto.getRandomValues(b);return bytesToHex(b);}
function now(){return new Date().toISOString();}
function operationHash(intent){return shaUri({operation_id:intent.operation_id,packet_id:intent.packet_id,payload_hash:intent.payload_hash});}

async function buildIntent(opts){
  var path=opts.source_boundary==="DEVICE_SYSTEM"&&opts.destination_boundary==="STEGOS_ECOSYSTEM"
    ?["DEVICE_SYSTEM","STEGOS_ECOSYSTEM"]
    :["STEGOS_ECOSYSTEM","DEVICE_SYSTEM"];
  var basis={
    operation_id:opts.operation_id,payload_hash:opts.payload_hash,
    source_boundary:opts.source_boundary,source_subsystem:opts.source_subsystem,
    destination_boundary:opts.destination_boundary,destination_subsystem:opts.destination_subsystem,
    boundary_path:path
  };
  var packet="INTR-"+(await sha256(basis)).slice(0,24);
  return {
    schema:"stegverse.universal-intr-transport/v1",protocol:"InTr",
    operation_id:opts.operation_id,packet_id:packet,payload_hash:opts.payload_hash,
    prior_transport_receipt_hash:opts.prior_transport_receipt_hash||null,
    source:{boundary:opts.source_boundary,subsystem:opts.source_subsystem},
    destination:{boundary:opts.destination_boundary,subsystem:opts.destination_subsystem},
    boundary_path:path,interlock_required:true,
    transport_semantics:{
      event_triggered:true,always_on_receiver_required:false,second_user_device_required:false,
      receiver_unavailable_disposition:"DURABLE_QUEUE_OR_EVENT_EPHEMERAL_MATERIALIZATION",
      exact_packet_transport_retry_allowed:true,blind_consequence_retry_allowed:false
    },
    authority:{authority_transfer:false,transport_grants_execution_authority:false,credential_authority:"TV/TVC"},
    receipt_chain:{required:true,receipt_schema:"stegverse.intr.hop_receipt/v1",payload_plaintext_in_receipts:false,prior_hash_required_after_first_hop:true}
  };
}
async function buildReceipt(intent,id,boundaryIdentity,transition,prior){
  var body={
    schema:"stegverse.intr.hop_receipt/v1",receipt_id:id,packet_id:intent.packet_id,hop_index:1,direction:"FORWARD",
    from_role:intent.boundary_path[0],to_role:intent.boundary_path[1],
    operation_hash:await operationHash(intent),payload_hash:intent.payload_hash,prior_receipt_hash:prior||null,
    boundary_identity_ref:boundaryIdentity,boundary_verification:"VERIFIED",transition_state:transition,
    secret_plaintext_present:false,authority_transfer:false,recorded_at:now()
  };
  body.receipt_hash=await shaUri(body);
  return body;
}

function transition(machine,target){
  var allowed={
    ABSENT:["REQUESTED"],REQUESTED:["ADMITTED"],ADMITTED:["PROVISIONING"],PROVISIONING:["LOCAL_READY"],
    LOCAL_READY:["LEASE_OPEN"],LEASE_OPEN:["TRANSITION_RECORDED"],TRANSITION_RECORDED:["RETURN_QUEUED"],
    RETURN_QUEUED:["EVIDENCE_EXPORTED"],EVIDENCE_EXPORTED:["RELEASING"],RELEASING:["LEASE_CLOSED"]
  };
  require((allowed[machine.state]||[]).indexOf(target)>=0,"invalid_lease_transition:"+machine.state+"->"+target);
  machine.state=target;machine.history.push(target);renderState(machine);
}
function renderState(machine){
  setText("leaseState",machine.state);
  setText("leaseHistory",machine.history.join(" → "));
}

function createWorker(){
  var code=`
self.postMessage({type:"READY"});
self.onmessage=async function(event){
  if(!event.data||event.data.type!=="EXECUTE")return;
  var bytes=new Uint8Array(event.data.payload);
  var digest=await crypto.subtle.digest("SHA-256",bytes);
  var hex=Array.from(new Uint8Array(digest)).map(function(b){return b.toString(16).padStart(2,"0");}).join("");
  var result={
    schema:"stegverse.canonical-runtime-proof-result/v1",
    operation:"CANONICAL_RUNTIME_PROOF",
    lease_id:event.data.lease_id,
    runtime_id:event.data.runtime_id,
    request_payload_hash:"sha256:"+hex,
    bounded_operations_executed:1,
    authority_effect:"NONE"
  };
  self.postMessage({type:"RESULT",response_text:JSON.stringify(result,Object.keys(result).sort())});
};
`;
  var url=URL.createObjectURL(new Blob([code],{type:"text/javascript"}));
  var worker=new Worker(url);
  return {worker:worker,url:url};
}
function waitReady(worker){
  return new Promise(function(resolve,reject){
    var timer=setTimeout(function(){reject(new Error("runtime_ready_timeout"));},5000);
    function handler(e){if(e.data&&e.data.type==="READY"){clearTimeout(timer);worker.removeEventListener("message",handler);resolve(e.data);}}
    worker.addEventListener("message",handler);
    worker.addEventListener("error",function(e){clearTimeout(timer);reject(e.error||new Error("worker_runtime_error"));},{once:true});
  });
}
function executeOnce(worker,payload,leaseId,runtimeId){
  return new Promise(function(resolve,reject){
    var timer=setTimeout(function(){reject(new Error("bounded_execution_timeout"));},5000);
    function handler(e){
      if(e.data&&e.data.type==="RESULT"){
        clearTimeout(timer);worker.removeEventListener("message",handler);resolve(e.data.response_text);
      }
    }
    worker.addEventListener("message",handler);
    worker.addEventListener("error",function(e){clearTimeout(timer);reject(e.error||new Error("worker_execution_error"));},{once:true});
    worker.postMessage({type:"EXECUTE",payload:payload.buffer,lease_id:leaseId,runtime_id:runtimeId},[payload.buffer]);
  });
}

async function retain(key,value){
  localStorage.setItem(key,canonical(value));
  var raw=localStorage.getItem(key);
  require(raw===canonical(value),"local_evidence_retention_verification_failed");
  return {storage:"localStorage",key:key,sha256:await shaUri(raw),verified:true,survives_worker_teardown:true};
}

async function run(){
  var workerRec=null;
  var machine={state:"ABSENT",history:["ABSENT"]};
  try{
    setText("resultState","RUNNING");
    require(location.protocol==="https:"&&location.hostname==="stegverse.org","AUTHENTIC_ORIGIN_REQUIRED");
    require(root.StegVerseNodeContinuity&&typeof root.StegVerseNodeContinuity.status==="function","NODE_CONTINUITY_UNAVAILABLE");
    var node=await root.StegVerseNodeContinuity.status();
    require(node&&node.registered===true&&node.receipts&&node.receipts[0],"VALID_NODE_REQUIRED");
    var genesis=node.receipts[0];
    var nodeId=node.registration.node_id;
    setText("nodeState","VALID / "+nodeId);

    var runId="CRL-"+randomHex(12);
    var runtimeId="WEBWORKER-"+(await sha256(nodeId+"|"+runId)).slice(0,24);
    var leaseId="CRL-"+(await sha256(runId+"|"+genesis.receipt_sha256)).slice(0,24);
    var payloadText="stegverse-canonical-runtime-proof-v1|"+runId+"|"+nodeId;
    var payload=new TextEncoder().encode(payloadText);
    var payloadHash=await shaUri(payload);
    var requestIntent=await buildIntent({
      operation_id:PROOF_OPERATION,payload_hash:payloadHash,
      source_boundary:"DEVICE_SYSTEM",source_subsystem:"Site:CanonicalRuntimeProof",
      destination_boundary:"STEGOS_ECOSYSTEM",destination_subsystem:DESTINATION_SUBSYSTEM
    });

    transition(machine,"REQUESTED");
    transition(machine,"ADMITTED");
    transition(machine,"PROVISIONING");

    workerRec=createWorker();
    await waitReady(workerRec.worker);
    transition(machine,"LOCAL_READY");
    setText("runtimeState","READY / "+runtimeId);
    transition(machine,"LEASE_OPEN");

    var ingress=await buildReceipt(requestIntent,leaseId+"-INGRESS",nodeId,"RECEIVED",null);
    setText("ingressState","RECEIVED / "+ingress.receipt_hash);

    var responseText=await executeOnce(workerRec.worker,payload,leaseId,runtimeId);
    var responseBytes=new TextEncoder().encode(responseText);
    var response=JSON.parse(responseText);
    require(response.bounded_operations_executed===1,"bounded_execution_count_invalid");
    require(response.request_payload_hash===payloadHash,"bounded_execution_payload_binding_mismatch");
    transition(machine,"TRANSITION_RECORDED");
    setText("executionState","EXECUTED ONCE");

    var responseIntent=await buildIntent({
      operation_id:PROOF_OPERATION,payload_hash:await shaUri(responseBytes),
      source_boundary:"STEGOS_ECOSYSTEM",source_subsystem:DESTINATION_SUBSYSTEM,
      destination_boundary:"DEVICE_SYSTEM",destination_subsystem:"Site:CanonicalRuntimeProof",
      prior_transport_receipt_hash:ingress.receipt_hash
    });
    var egress=await buildReceipt(responseIntent,leaseId+"-EGRESS",runtimeId,"FORWARDED",ingress.receipt_hash);
    require(egress.prior_receipt_hash===ingress.receipt_hash,"receipt_chain_not_linked");
    setText("egressState","FORWARDED / "+egress.receipt_hash);

    transition(machine,"RETURN_QUEUED");
    var evidence={
      schema:"stegverse.canonical-runtime-browser-evidence/v1",
      state:"EVIDENCE_RETAINED_PRE_RELEASE",
      authentic_runtime_observation:true,
      observation_origin:location.origin,
      run_id:runId,lease_id:leaseId,runtime_id:runtimeId,
      runtime_substrate:"BROWSER_WEB_WORKER_ON_VALID_STEGVERSE_NODE",
      runtime_class:"EVENT_EPHEMERAL",lease_profile:"INTAKE",rendezvous_requirement:"NOT_REQUIRED",
      node_id:nodeId,interlock_id:node.registration.interlock_id,
      genesis_receipt_sha256:genesis.receipt_sha256,
      request_intent:requestIntent,request_ingress_receipt:ingress,
      bounded_execution_observed:true,bounded_operations_executed:1,
      response_payload_hash:responseIntent.payload_hash,response_egress_receipt:egress,
      receipt_chain_linked:true,lease_history:machine.history.slice(),
      credential_authority:"TV/TVC",github_token_runtime_authority:"NONE",
      authority_effect:"NONE",public_server_rendezvous_claimed:false,
      master_records_custody_claimed:false,observed_at:now()
    };
    var preReleaseRetention=await retain(STORAGE_KEY+".pre-release",evidence);
    evidence.return_queue_receipt=preReleaseRetention;
    transition(machine,"EVIDENCE_EXPORTED");

    transition(machine,"RELEASING");
    workerRec.worker.terminate();
    URL.revokeObjectURL(workerRec.url);
    workerRec=null;
    transition(machine,"LEASE_CLOSED");

    var closure={
      schema:"stegverse.canonical-runtime-browser-closure/v1",state:"LEASE_CLOSED",
      authentic_runtime_observation:true,run_id:runId,lease_id:leaseId,runtime_id:runtimeId,
      evidence_retained_before_release:true,pre_release_evidence_sha256:preReleaseRetention.sha256,
      request_ingress_receipt_hash:ingress.receipt_hash,response_egress_receipt_hash:egress.receipt_hash,
      receipt_chain_linked:true,worker_terminated:true,lease_history:machine.history.slice(),
      credential_authority:"TV/TVC",github_token_runtime_authority:"NONE",authority_effect:"NONE",closed_at:now()
    };
    var closureRetention=await retain(STORAGE_KEY,closure);
    closure.closure_retention_receipt=closureRetention;
    localStorage.setItem(STORAGE_KEY,canonical(closure));

    var closureHash=await shaUri(closure);
    var nodeReceipt=await root.StegVerseNodeContinuity.recordStep(CAPABILITY,"lease-closed","OBSERVED",closureHash);
    var bundle={schema:"stegverse.canonical-runtime-proof-bundle/v1",state:"CANONICAL_RUNTIME_LANE_OBSERVED",evidence:evidence,closure:closure,node_capability_receipt:nodeReceipt};
    localStorage.setItem(STORAGE_KEY+".bundle",canonical(bundle));

    setText("resultState","CANONICAL_RUNTIME_LANE_OBSERVED");
    setText("message","Canonical runtime lane observed end-to-end on this existing StegVerse Node.");
    setText("bundle",JSON.stringify(bundle,null,2));
    el("copyBtn").disabled=false;el("exportBtn").disabled=false;
    root.__STEGVERSE_CANONICAL_RUNTIME_PROOF__=bundle;
    return bundle;
  }catch(err){
    if(workerRec){try{workerRec.worker.terminate();URL.revokeObjectURL(workerRec.url);}catch(_e){}}
    setText("resultState","FAIL_CLOSED");
    setText("message","FAIL_CLOSED: "+(err&&err.message?err.message:String(err)));
    throw err;
  }
}
async function copy(){
  var b=root.__STEGVERSE_CANONICAL_RUNTIME_PROOF__;if(!b)return;
  await navigator.clipboard.writeText(JSON.stringify(b,null,2));
  setText("message","Evidence copied.");
}
function exportJson(){
  var b=root.__STEGVERSE_CANONICAL_RUNTIME_PROOF__;if(!b)return;
  var url=URL.createObjectURL(new Blob([JSON.stringify(b,null,2)+"\n"],{type:"application/json"}));
  var a=document.createElement("a");a.href=url;a.download="stegverse-canonical-runtime-proof-"+b.evidence.run_id+".json";a.click();
  setTimeout(function(){URL.revokeObjectURL(url);},1000);
}

document.addEventListener("DOMContentLoaded",function(){
  el("runBtn").addEventListener("click",function(){run().catch(function(){});});
  el("copyBtn").addEventListener("click",function(){copy().catch(function(){});});
  el("exportBtn").addEventListener("click",exportJson);
  run().catch(function(){});
});
}(typeof globalThis!=="undefined"?globalThis:window));
