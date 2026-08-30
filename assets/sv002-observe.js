(function(root){
"use strict";
var CAPABILITY="sv002-public-observation";
function el(id){return document.getElementById(id);}
function setText(id,v){var n=el(id);if(n)n.textContent=String(v==null?"":v);}
function show(id,yes){var n=el(id);if(n)n.classList.toggle("hidden",!yes);}
function canonical(v){if(v===null||typeof v!=="object")return JSON.stringify(v);if(Array.isArray(v))return "["+v.map(canonical).join(",")+"]";return "{"+Object.keys(v).sort().map(function(k){return JSON.stringify(k)+":"+canonical(v[k]);}).join(",")+"}";}
async function sha256(v){var d=await crypto.subtle.digest("SHA-256",new TextEncoder().encode(typeof v==="string"?v:canonical(v)));return Array.from(new Uint8Array(d)).map(function(b){return b.toString(16).padStart(2,"0");}).join("");}
function validReceipt(r,dir){
  if(!r||r.schema!=="stegverse.intr.hop_receipt/v1")throw new Error("missing "+dir+" InTr receipt");
  if(r.boundary_verification!=="VERIFIED")throw new Error(dir+" boundary not verified");
  if(r.authority_transfer!==false||r.secret_plaintext_present!==false)throw new Error(dir+" authority/secret invariant failed");
  if(!/^[0-9a-f]{64}$/.test(String(r.receipt_hash||"")))throw new Error(dir+" receipt hash invalid");
  if(dir==="ingress"&&r.transition_state!=="RECEIVED")throw new Error("ingress not RECEIVED");
  if(dir==="egress"&&!["FORWARDED","RECEIVED"].includes(r.transition_state))throw new Error("egress not forwarded/received");
}
async function nodeStatus(){
  if(!root.StegVerseNodeContinuity)throw new Error("Node continuity unavailable");
  return root.StegVerseNodeContinuity.status();
}
async function requestObservation(node){
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
      registration_receipt_sha256:reg.receipt_sha256
    },
    bindings:{
      experiment_id:"STEGVERSE-002-SELF-CHARACTERIZATION-001",
      observation_projection:"PUBLIC_READ_ONLY"
    },
    payload:{},
    authority_transfer:false
  };
  request.request_sha256=await sha256(request);
  var response=await connector.transact(request);
  if(!response||response.schema_version!=="stegverse.sv002.public_observation.interlock_response.v1")throw new Error("Unexpected observation response schema");
  if(response.operation!=="READ_OBSERVATION"||response.authority_effect!=="NONE"||response.authority_transfer!==false)throw new Error("Observation response authority invariant failed");
  if(!response.observer_binding||response.observer_binding.node_id!==reg.node_id)throw new Error("Observer node binding mismatch");
  if(!response.transport_receipts)throw new Error("Dual transport receipts required");
  validReceipt(response.transport_receipts.ingress,"ingress");
  validReceipt(response.transport_receipts.egress,"egress");
  return response;
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
  setText("reconstruction",JSON.stringify(p.reconstruction||{state:"NOT_OBSERVED"},null,2));
  show("projection",true);
  el("gate").classList.remove("blocked");el("gate").classList.add("ok");
  setText("gateMessage","Valid StegVerse Node + Interlock/InTr observation established. Observer traffic terminates at the read-only projection, not StegVerse-002.");
}
async function refresh(){
  try{
    var node=await nodeStatus();
    if(!node.registered){
      setText("nodeState","NOT ESTABLISHED");setText("interlockState","NOT ATTEMPTED");setText("dataState","UNAVAILABLE");
      setText("gateMessage","No valid StegVerse Node is established on this device. Experiment data will not be fetched.");
      show("registerBtn",true);show("observeBtn",false);show("projection",false);return;
    }
    setText("nodeState","REGISTERED / "+node.registration.node_id);
    show("registerBtn",false);
    if(!root.StegVerseInterlockConnector){
      setText("interlockState","NOT PROVISIONED");setText("dataState","UNAVAILABLE");
      setText("gateMessage","Node is valid, but the canonical observation Interlock is not provisioned. No experiment data is available.");
      show("observeBtn",false);show("projection",false);return;
    }
    setText("interlockState","AVAILABLE");show("observeBtn",true);
    setText("gateMessage","Node validated. Open the read-only observation Interlock to receive the experiment projection.");
  }catch(e){setText("nodeState","FAIL_CLOSED");setText("interlockState","FAIL_CLOSED");setText("dataState","UNAVAILABLE");setText("gateMessage",e.message||e);show("projection",false);}
}
async function register(){
  try{await root.StegVerseNodeContinuity.registerDevice();await root.StegVerseNodeContinuity.recordStep(CAPABILITY,"node","ESTABLISHED","local-node-receipt");await refresh();}
  catch(e){setText("gateMessage",e.message||e);}
}
async function observe(){
  try{
    var node=await nodeStatus();var response=await requestObservation(node);
    await root.StegVerseNodeContinuity.recordStep(CAPABILITY,"interlock","OBSERVED",response.transport_receipts.egress.receipt_hash);
    render(response);
  }catch(e){setText("dataState","UNAVAILABLE");setText("gateMessage","FAIL_CLOSED: "+(e.message||e));show("projection",false);}
}
document.addEventListener("DOMContentLoaded",function(){el("registerBtn").addEventListener("click",register);el("observeBtn").addEventListener("click",observe);refresh();});
}(typeof globalThis!=="undefined"?globalThis:window));
