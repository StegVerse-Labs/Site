(function(root){
"use strict";
var CAPABILITY="sv002-public-observation";
var INVARIANT_PROFILE="/data/sv002-viewer-evidence-invariants.v1.json";
function el(id){return document.getElementById(id);}
function setText(id,v){var n=el(id);if(n)n.textContent=String(v==null?"":v);}
function show(id,yes){var n=el(id);if(n)n.classList.toggle("hidden",!yes);}
function canonical(v){if(v===null||typeof v!=="object")return JSON.stringify(v);if(Array.isArray(v))return "["+v.map(canonical).join(",")+"]";return "{"+Object.keys(v).sort().map(function(k){return JSON.stringify(k)+":"+canonical(v[k]);}).join(",")+"}";}
async function sha256(v){var d=await crypto.subtle.digest("SHA-256",new TextEncoder().encode(typeof v==="string"?v:canonical(v)));return Array.from(new Uint8Array(d)).map(function(b){return b.toString(16).padStart(2,"0");}).join("");}
function validReceipt(r,dir){
  if(!r||r.schema!=="stegverse.intr.hop_receipt/v1")throw new Error("missing "+dir+" InTr receipt");
  if(r.boundary_verification!=="VERIFIED")throw new Error(dir+" boundary not verified");
  if(r.authority_transfer!==false||r.secret_plaintext_present!==false)throw new Error(dir+" authority/secret invariant failed");
  if(!/^sha256:[0-9a-f]{64}$/.test(String(r.receipt_hash||"")))throw new Error(dir+" receipt hash invalid");
  if(dir==="ingress"&&r.transition_state!=="RECEIVED")throw new Error("ingress not RECEIVED");
  if(dir==="egress"&&!["FORWARDED","RECEIVED"].includes(r.transition_state))throw new Error("egress not forwarded/received");
}
async function verifyRuntimeEvidenceProjection(p){
  var reconstruction=p&&p.reconstruction;
  if(!reconstruction||reconstruction.status!=="PASS"||reconstruction.reconstruction!=="PASS")return {state:"NOT_APPLICABLE_NONPASS_RECONSTRUCTION"};
  var a=p.artifacts||{};
  var rows=a.ordered_transition_receipts;
  var repo=a.repository_ledger_root;
  var org=a.organization_ledger_root;
  if(!Array.isArray(rows)||!rows.length)throw new Error("ordered transition receipts required for reconstructed projection");
  if(!repo||!repo.range)throw new Error("repository ledger root required for reconstructed projection");
  var members=rows.map(function(r){return {sequence:r.sequence,receipt_id:r.transition_receipt_id,receipt_hash:r.transition_receipt_sha256};});
  var ordered=await sha256(members);
  if(repo.range.ordered_root_hash!==ordered)throw new Error("repository ordered receipt root mismatch");
  var repoBody=JSON.parse(JSON.stringify(repo));var repoClaim=repoBody.root_hash;delete repoBody.root_hash;
  if(await sha256(repoBody)!==repoClaim)throw new Error("repository ledger root hash mismatch");
  if(org){
    var children=Array.isArray(org.children)?org.children:[];
    if(!children.some(function(x){return x&&x.root_hash===repoClaim;}))throw new Error("organization ledger does not include repository root");
    var orgBody=JSON.parse(JSON.stringify(org));var orgClaim=orgBody.root_hash;delete orgBody.root_hash;
    if(await sha256(orgBody)!==orgClaim)throw new Error("organization ledger root hash mismatch");
  }
  return {state:"PASS",ordered_transition_count:rows.length,repository_ledger_root_hash:repoClaim,organization_ledger_root_hash:org&&org.root_hash||null,invariant_profile:INVARIANT_PROFILE};
}
async function refreshRuntimeState(){
  try{
    var local=root.__STEGVERSE_SV002_LOCAL_RUNTIME__;
    if(local&&local.receipt){
      if(local.receipt.state==="PRINCIPAL_COMPLETED"){
        setText("runtimeState","PRINCIPAL COMPLETED / "+local.receipt.runtime_id);
        return;
      }
      if(local.receipt.state==="LOCAL_READY"){
        setText("runtimeState","LOCAL_READY / "+local.receipt.runtime_id);
        return;
      }
    }
    var response=await fetch("/intr/sv002-observe/readiness",{cache:"no-store",headers:{"Accept":"application/json"}});
    if(!response.ok){
      setText("runtimeState","PUBLIC ROUTE UNAVAILABLE / HTTP "+response.status);
      return;
    }
    var contentType=String(response.headers.get("content-type")||"").toLowerCase();
    if(contentType.indexOf("application/json")<0){
      setText("runtimeState","PUBLIC ROUTE NOT PROVISIONED");
      return;
    }
    var value=await response.json();
    var upstream=value&&value.upstream_runtime_state;
    var state=value&&value.state;
    if(state==="READY"&&upstream==="READY"){
      setText("runtimeState","ACTIVE / RECEIVER READY");
    }else if(upstream==="UNREACHABLE"){
      setText("runtimeState","NOT REACHABLE");
    }else if(value&&value.loopback_upstream_configured){
      setText("runtimeState","CONFIGURED / "+String(upstream||"NOT READY"));
    }else{
      setText("runtimeState","NOT PROVISIONED");
    }
  }catch(e){
    setText("runtimeState","NOT OBSERVED");
  }
}

async function nodeStatus(){
  if(!root.StegVerseNodeContinuity)throw new Error("Node continuity unavailable");
  return root.StegVerseNodeContinuity.status();
}
async function buildObservationRequest(node){
  var connector=root.StegVerseInterlockConnector;
  if(!connector||typeof connector.transact!=="function")throw new Error("Canonical Interlock Connector not provisioned");
  var reg=node.registration;
  var request={
    schema_version:"stegverse.sv002.public_observation.interlock_request.v1",
    request_class:"SV002_PUBLIC_OBSERVE",
    operation:"READ_OBSERVATION",
    authority_ref:connector.authorityRef(),
    transport:"InTr",
    observer:{
      node_id:reg.node_id,
      interlock_id:reg.interlock_id,
      registration_receipt_sha256:reg.receipt_sha256,
      genesis_receipt:node.receipts[0]
    },
    bindings:{
      experiment_id:"STEGVERSE-002-SELF-CHARACTERIZATION-001",
      observation_projection:"PUBLIC_READ_ONLY"
    },
    payload:{},
    authority_transfer:false
  };
  request.request_sha256=await sha256(request);
  return request;
}
async function requestObservation(node,request){
  var connector=root.StegVerseInterlockConnector;
  request=request||await buildObservationRequest(node);
  var response=await connector.transact(request);
  var reg=node.registration;
  if(!response||response.schema_version!=="stegverse.sv002.public_observation.interlock_response.v1")throw new Error("Unexpected observation response schema");
  if(response.operation!=="READ_OBSERVATION"||response.authority_effect!=="NONE"||response.authority_transfer!==false)throw new Error("Observation response authority invariant failed");
  if(!response.observer_binding||response.observer_binding.node_id!==reg.node_id||response.observer_binding.registration_receipt_sha256!==reg.receipt_sha256)throw new Error("Observer node binding mismatch");
  if(!response.transport_receipts)throw new Error("Dual transport receipts required");
  validReceipt(response.transport_receipts.ingress,"ingress");
  validReceipt(response.transport_receipts.egress,"egress");
  response.projection=response.projection||{};
  response.projection.viewer_verification=await verifyRuntimeEvidenceProjection(response.projection);
  return response;
}
async function buildTransportIntent(request){
  var intr=root.StegVerseGeneratedInTr;
  if(!intr||typeof intr.buildIntent!=="function")throw new Error("Canonical generated InTr connector unavailable");
  return intr.buildIntent(
    "sv002-public-observe",
    new TextEncoder().encode(intr.canonical(request)),
    "READ_OBSERVATION",
    "SV002-OBSERVE-"+request.request_sha256.slice(0,16)
  );
}
async function buildMaterializationRequest(request){
  var intent=await buildTransportIntent(request);
  if(!root.StegVerseHBInTrCarrier||typeof root.StegVerseHBInTrCarrier.buildBinding!=="function")throw new Error("Canonical HB-derived InTr carrier unavailable");
  var binding=await root.StegVerseHBInTrCarrier.buildBinding(intent.packet_id,intent.payload_hash);
  return root.StegVerseGeneratedInTr.buildMaterializationRequest(
    "sv002-public-observe",
    intent,
    "opaque://sv002-public-observation/"+request.request_sha256,
    binding
  );
}
async function queueMaterialization(request){
  if(!root.StegVerseNodeContinuity||typeof root.StegVerseNodeContinuity.queueIntrMaterializationRequest!=="function")throw new Error("StegVerse Node InTr outbox unavailable");
  var materialization=await buildMaterializationRequest(request);
  var entry=await root.StegVerseNodeContinuity.queueIntrMaterializationRequest(materialization);
  await root.StegVerseNodeContinuity.recordStep(CAPABILITY,"materialization","QUEUED",entry.outbox_entry_hash);
  return entry;
}

function render(response){
  var p=response.projection||{};
  setText("dataState","OBSERVED THROUGH INTERLOCK");
  setText("stateSummary",JSON.stringify(p.state||{},null,2));
  setText("topology",JSON.stringify(p.topology||{},null,2));
  setText("knowledge",JSON.stringify(p.knowledge||{},null,2));
  var events=el("events");events.innerHTML="";
  (Array.isArray(p.events)?p.events:[]).forEach(function(e){var d=document.createElement("div");d.className="event value";d.textContent=JSON.stringify(e);events.appendChild(d);});
  if(!(p.events||[]).length){events.textContent="No observed experiment events yet.";}
  setText("receipts",JSON.stringify(response.transport_receipts,null,2));
  setText("reconstruction",JSON.stringify({master_records:p.reconstruction||{state:"NOT_OBSERVED"},viewer_verification:p.viewer_verification||{state:"NOT_ATTEMPTED"}},null,2));
  show("projection",true);
  el("gate").classList.remove("blocked");el("gate").classList.add("ok");
  setText("gateMessage","Valid StegVerse Node + Interlock/InTr observation established. Observer traffic terminates at the read-only projection, not StegVerse-002.");
}
async function refresh(){
  try{
    var node=await nodeStatus();
    if(!node.registered){
      setText("nodeBadge","STEGVERSE NODE REQUIRED");setText("nodeState","NOT ESTABLISHED");setText("interlockState","NOT ATTEMPTED");setText("dataState","UNAVAILABLE");
      setText("gateMessage","No valid StegVerse Node is established on this device. Experiment data will not be fetched.");
      show("registerBtn",true);show("observeBtn",false);show("projection",false);return;
    }
    setText("nodeBadge","STEGVERSE NODE CONFIRMED");setText("nodeState","REGISTERED / "+node.registration.node_id);
    show("registerBtn",false);
    if(!root.StegVerseInterlockConnector){
      setText("interlockState","NOT PROVISIONED");setText("dataState","UNAVAILABLE");
      setText("gateMessage","Node is valid, but the canonical observation Interlock is not provisioned. No experiment data is available.");
      show("observeBtn",false);show("projection",false);return;
    }
    setText("interlockState","AVAILABLE");show("observeBtn",true);
    setText("gateMessage","Node validated. Open the read-only observation Interlock to receive the experiment projection.");
  }catch(e){setText("nodeBadge","STEGVERSE NODE CHECK FAILED");setText("nodeState","FAIL_CLOSED");setText("interlockState","FAIL_CLOSED");setText("dataState","UNAVAILABLE");setText("gateMessage",e.message||e);show("projection",false);}
}
async function register(){
  try{await root.StegVerseNodeContinuity.registerDevice();await root.StegVerseNodeContinuity.recordStep(CAPABILITY,"node","ESTABLISHED","local-node-receipt");await refresh();}
  catch(e){setText("gateMessage",e.message||e);}
}
async function observe(){
  var node=null;var request=null;
  try{
    node=await nodeStatus();request=await buildObservationRequest(node);
    var response=await requestObservation(node,request);
    await root.StegVerseNodeContinuity.recordStep(CAPABILITY,"interlock","OBSERVED",response.transport_receipts.egress.receipt_hash);
    render(response);
  }catch(e){
    if(node&&node.registered&&request&&e&&e.code==="INTR_RUNTIME_UNAVAILABLE"){
      try{
        var queued=await queueMaterialization(request);
        setText("dataState","MATERIALIZATION QUEUED");
        setText("gateMessage","Receiver unavailable. Exact non-authorizing InTr materialization request is queued on this StegVerse Node.");
        show("projection",false);
        if(root.StegVerseSV002LocalRuntime&&typeof root.StegVerseSV002LocalRuntime.materialize==="function"){
          try{
            var localRuntime=await root.StegVerseSV002LocalRuntime.materialize(queued);
            if(localRuntime.state==="PRINCIPAL_COMPLETED"){
              setText("runtimeState","PRINCIPAL COMPLETED / "+localRuntime.runtime_id);
              setText("dataState","PRINCIPAL EXECUTION OBSERVED");
              var execution=localRuntime.principal_execution_receipt||{};
              setText("stateSummary",JSON.stringify({
                experiment_id:execution.experiment_id,
                run_id:execution.run_id,
                state:execution.state,
                model_id:execution.model_id,
                runtime_identity_sha256:execution.runtime_identity_sha256,
                receipt_sha256:execution.receipt_sha256
              },null,2));
              setText("topology",JSON.stringify({
                runtime_substrate:localRuntime.runtime_substrate,
                runtime_id:localRuntime.runtime_id,
                lease_id:localRuntime.lease_id,
                node_id:localRuntime.node_id,
                interlock_id:localRuntime.interlock_id,
                principal_execution_owner:execution.principal_execution_owner
              },null,2));
              setText("knowledge",JSON.stringify(execution.formal||{},null,2));
              var events=el("events");events.innerHTML="";
              (execution.resource_trace||[]).forEach(function(event){
                var d=document.createElement("div");d.className="event value";d.textContent=JSON.stringify(event);events.appendChild(d);
              });
              setText("receipts",JSON.stringify({
                materialization_receipt_sha256:localRuntime.receipt_sha256,
                principal_execution_receipt_sha256:execution.receipt_sha256,
                runtime_identity_sha256:execution.runtime_identity_sha256
              },null,2));
              setText("reconstruction",JSON.stringify({state:"PENDING_MASTER_RECORDS_RECONSTRUCTION"},null,2));
              show("projection",true);
              el("gate").classList.remove("blocked");el("gate").classList.add("ok");
              setText("gateMessage","Authentic device-local SV002 principal execution completed on this StegVerse Node. Master Records same-execution reconstruction remains pending.");
            }else{
              setText("runtimeState","LOCAL_READY / "+localRuntime.runtime_id);
              setText("dataState","LOCAL RUNTIME MATERIALIZED");
              setText("gateMessage","Canonical event-ephemeral runtime materialized on this StegVerse Node.");
            }
          }catch(localError){
            setText("runtimeState","LOCAL MATERIALIZATION BLOCKED");
            setText("gateMessage","FAIL_CLOSED: "+(localError.message||localError));
          }
        }
        if(root.StegVerseSV002InTrSync&&typeof root.StegVerseSV002InTrSync.attempt==="function")root.StegVerseSV002InTrSync.attempt();
        return queued;
      }catch(queueError){
        setText("dataState","UNAVAILABLE");setText("gateMessage","FAIL_CLOSED: "+(queueError.message||queueError));show("projection",false);return;
      }
    }
    setText("dataState","UNAVAILABLE");setText("gateMessage","FAIL_CLOSED: "+(e.message||e));show("projection",false);
  }
}
document.addEventListener("DOMContentLoaded",async function(){
  el("registerBtn").addEventListener("click",register);
  el("observeBtn").addEventListener("click",observe);
  try{
    if(root.StegVerseInterlockConnectorReady)await root.StegVerseInterlockConnectorReady;
  }catch(_error){}
  await refresh();
  refreshRuntimeState();
  setInterval(refreshRuntimeState,1000);
  try{
    var node=await nodeStatus();
    if(node&&node.registered===true&&root.StegVerseInterlockConnector){
      setText("gateMessage","Node + Interlock confirmed. Starting SV002 observation automatically…");
      await observe();
    }
  }catch(autoError){
    setText("gateMessage","AUTO-START FAIL_CLOSED: "+(autoError&&autoError.message?autoError.message:String(autoError)));
  }
});
}(typeof globalThis!=="undefined"?globalThis:window));
