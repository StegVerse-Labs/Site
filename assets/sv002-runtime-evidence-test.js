(function(root){
"use strict";
var PROFILE_PATH="/intr/profile";
var MATERIALIZATION_PATH="/intr/materialization";
var READINESS_PATH="/intr/sv002-observe/readiness";
var SV002_PROFILE="SV002:PublicObservation";
var TEST_SCHEMA="stegverse.sv002.authentic-runtime-evidence/v1";
var lastBundle=null;
function el(id){return document.getElementById(id);}
function text(id,v){var n=el(id);if(n)n.textContent=String(v==null?"":v);}
function canonical(v){if(v===null||typeof v!=="object")return JSON.stringify(v);if(Array.isArray(v))return "["+v.map(canonical).join(",")+"]";return "{"+Object.keys(v).sort().map(function(k){return JSON.stringify(k)+":"+canonical(v[k]);}).join(",")+"}";}
function bytesToHex(bytes){return Array.from(bytes,function(b){return b.toString(16).padStart(2,"0");}).join("");}
async function sha256(v){var raw=typeof v==="string"?v:canonical(v);var d=await crypto.subtle.digest("SHA-256",new TextEncoder().encode(raw));return bytesToHex(new Uint8Array(d));}
function require(ok,msg){if(!ok)throw new Error(msg);}
function externalContext(){return location.protocol==="https:"&&location.hostname.toLowerCase()==="stegverse.org";}
function setPhase(id,state){text(id,state);}
function setMessage(v){text("message",v);}
function render(bundle){lastBundle=bundle;el("evidence").textContent=JSON.stringify(bundle,null,2);el("copyBtn").disabled=false;el("exportBtn").disabled=false;}
function classifyError(e){return {state:"FAIL_CLOSED",reason:String(e&&e.message||e),observed_at:new Date().toISOString()};}
function validateProfile(profile){
  require(profile&&typeof profile==="object","profile object required");
  require(["stegverse.universal-intr-profiled-ingress/v1","stegverse.hil-intr-materialization-ingress-profile/v1"].includes(profile.schema),"profile schema invalid");
  var common={state:"ACTIVE_SOVEREIGN_INTR_INGRESS",protocol:"InTr",profile_path:PROFILE_PATH,materialization_path:MATERIALIZATION_PATH,event_triggered:true,second_user_device_required:false,g18_required:false,tls_enabled:true,credential_authority:"TV/TVC",github_token_runtime_authority:"NONE",execution_authority:"NONE",authority_effect:"NONE_DISCOVERY_EVIDENCE_ONLY"};
  Object.keys(common).forEach(function(k){require(canonical(profile[k])===canonical(common[k]),"profile mismatch: "+k);});
  require(Array.isArray(profile.supported_origins)&&profile.supported_origins.includes("STEGOS_NODE_OUTBOX"),"direct Node origin missing");
  if(profile.schema==="stegverse.universal-intr-profiled-ingress/v1"){
    require(profile.always_on_application_receiver_required===false,"always-on receiver must not be required");
    require(Array.isArray(profile.profiles)&&profile.profiles.includes(SV002_PROFILE),"SV002 profile not advertised");
  }else{
    require(profile.always_on_receiver_required===false,"always-on receiver must not be required");
    require(profile.direct_node_credential_requirement==="NONE"&&profile.direct_node_tvc_authorization_required===false,"direct Node credential boundary invalid");
    require(profile.exact_request_validation_required===true&&profile.write_once_queue_admission===true,"HIL compatibility profile lacks exact/write-once admission");
    require(Array.isArray(profile.additional_materialization_profiles)&&profile.additional_materialization_profiles.includes(SV002_PROFILE),"SV002 compatibility profile not advertised");
  }
  return profile;
}
async function observeProfile(runId){
  require(externalContext(),"AUTHENTIC_EXTERNAL_CONTEXT_REQUIRED: open this test at https://stegverse.org");
  var url=new URL(PROFILE_PATH,location.origin).href;
  var response=await fetch(url,{method:"GET",cache:"no-store",credentials:"omit",headers:{Accept:"application/json"}});
  require(response.status===200,"public /intr/profile HTTP "+response.status);
  var profile=validateProfile(await response.json());
  var hash=await sha256(profile);
  return {schema:"stegverse.universal-intr-ingress-observation/v1",observation_state:"OBSERVED_HTTPS_PROFILE",observed_profile_url:url,observed_at:new Date().toISOString(),https_observed:true,http_status:200,credential_used:false,profile:profile,profile_sha256:hash,evidence_ref:"observer-browser://"+runId+"/https-profile",github_token_runtime_authority:"NONE",execution_authority:"NONE",authority_effect:"NONE_OBSERVATION_ONLY"};
}
function targetFromProfile(obs){
  var target={schema:"stegos.site.sv002_intr_sync_target.v1",state:"CONFORMING_SOVEREIGN_INTR_INGRESS",ingress_url:new URL(MATERIALIZATION_PATH,obs.observed_profile_url).href,transport_origin:"STEGOS_NODE_OUTBOX",runtime_ingress_observed:true,configuration_authority:"StegVerse sovereign runtime evidence projection",credential_authority:"TV/TVC",credential_requirement:"NONE",github_token_runtime_authority:"NONE",execution_authority:"NONE",authority_effect:"NONE_DISCOVERY_ONLY"};
  return root.StegVerseSV002InTrSync.validateTarget(target);
}
async function buildObservationRequest(node){
  var connector=root.StegVerseInterlockConnector;require(connector&&typeof connector.transact==="function","canonical Interlock connector unavailable");
  var reg=node.registration;
  var req={schema_version:"stegverse.sv002.public_observation.interlock_request.v1",request_class:"SV002_PUBLIC_OBSERVE",operation:"READ_OBSERVATION",authority_ref:connector.authorityRef(),transport:"InTr",observer:{node_id:reg.node_id,interlock_id:reg.interlock_id,registration_receipt_sha256:reg.receipt_sha256,genesis_receipt:node.receipts[0]},bindings:{experiment_id:"STEGVERSE-002-SELF-CHARACTERIZATION-001",observation_projection:"PUBLIC_READ_ONLY"},payload:{},authority_transfer:false};
  req.request_sha256=await sha256(req);return req;
}
async function buildMaterializationRequest(request){
  var payloadHash="sha256:"+await sha256(request), path=["DEVICE_SYSTEM","STEGOS_ECOSYSTEM"];
  var basis={operation_id:"SV002-OBSERVE-"+request.request_sha256.slice(0,16),payload_hash:payloadHash,source_boundary:"DEVICE_SYSTEM",source_subsystem:"Site:SV002PublicObservation",destination_boundary:"STEGOS_ECOSYSTEM",destination_subsystem:"SV002:PublicObservation",boundary_path:path};
  var basisHash=await sha256(basis);
  var intent={schema:"stegverse.universal-intr-transport/v1",protocol:"InTr",operation_id:basis.operation_id,packet_id:"INTR-"+basisHash.slice(0,24),payload_hash:payloadHash,prior_transport_receipt_hash:null,source:{boundary:"DEVICE_SYSTEM",subsystem:"Site:SV002PublicObservation"},destination:{boundary:"STEGOS_ECOSYSTEM",subsystem:"SV002:PublicObservation"},boundary_path:path,interlock_required:true,transport_semantics:{event_triggered:true,always_on_receiver_required:false,second_user_device_required:false,receiver_unavailable_disposition:"DURABLE_QUEUE_OR_EVENT_EPHEMERAL_MATERIALIZATION",exact_packet_transport_retry_allowed:true,blind_consequence_retry_allowed:false},authority:{authority_transfer:false,transport_grants_execution_authority:false,credential_authority:"TV/TVC"},receipt_chain:{required:true,receipt_schema:"stegverse.intr.hop_receipt/v1",payload_plaintext_in_receipts:false,prior_hash_required_after_first_hop:true}};
  var intentHash="sha256:"+await sha256(intent);var identityHash=await sha256({transport_intent_hash:intentHash,operation_id:intent.operation_id,packet_id:intent.packet_id,payload_hash:intent.payload_hash,destination:intent.destination});
  var body={schema:"stegverse.universal-intr-materialization-request/v1",materialization_id:"INTR-MAT-"+identityHash.slice(0,24),state:"QUEUED_FOR_EVENT_EPHEMERAL_MATERIALIZATION",transport_schema:"stegverse.universal-intr-transport/v1",transport_protocol:"InTr",transport_intent_hash:intentHash,operation_id:intent.operation_id,packet_id:intent.packet_id,payload_hash:intent.payload_hash,payload_ref:"opaque://sv002-public-observation/"+request.request_sha256,destination:intent.destination,boundary_path:intent.boundary_path,downstream_owner_ref:"StegVerse-Labs/.github#493",event_triggered:true,always_on_receiver_required:false,second_user_device_required:false,receiver_unavailable_disposition:"DURABLE_QUEUE_OR_EVENT_EPHEMERAL_MATERIALIZATION",exact_packet_transport_retry_allowed:true,blind_consequence_retry_allowed:false,interlock_required:true,request_grants_execution_authority:false,claim_or_fence_minted:false,transport_grants_execution_authority:false,credential_authority:"TV/TVC",github_token_runtime_authority:"NONE",authority_transfer:false,authority_effect:"NONE_REQUEST_ONLY"};
  body.request_hash="sha256:"+await sha256(body);return body;
}
async function queueAndDeliver(target,request){
  var materialization=await buildMaterializationRequest(request);
  var entry=await root.StegVerseNodeContinuity.queueIntrMaterializationRequest(materialization);
  await root.StegVerseSV002InTrSync.validateOutboxEntry(entry);
  var trigger=await root.StegVerseSV002InTrSync.buildTrigger(entry), wire=canonical(trigger), payloadSha=await sha256(wire);
  var response=await fetch(target.ingress_url,{method:"POST",mode:"cors",cache:"no-store",credentials:"omit",headers:{"Content-Type":"application/json","X-StegVerse-Transport":"InTr","X-StegVerse-Transport-Origin":"STEGOS_NODE_OUTBOX","X-StegVerse-Payload-SHA256":payloadSha},body:wire});
  require(response.status===202,"materialization ingress HTTP "+response.status);
  var receipt=await response.json();root.StegVerseSV002InTrSync.validateIngressReceipt(receipt,entry,payloadSha);
  return {materialization_request:materialization,outbox_entry:entry,trigger_sha256:trigger.trigger_sha256,transport_payload_sha256:payloadSha,ingress_receipt:receipt};
}
async function waitForReady(target){
  var url=new URL(READINESS_PATH,target.ingress_url).href,last=null;
  for(var i=0;i<40;i++){
    try{var r=await fetch(url,{method:"GET",cache:"no-store",credentials:"omit",headers:{Accept:"application/json"}});if(r.status===200){var j=await r.json();if(j&&j.schema==="stegverse.sv002-public-observation-runtime-readiness/v1"&&j.state==="READY"&&j.transport==="InTr"&&j.credential_authority==="TV/TVC"&&j.authority_effect==="NONE")return {observed_at:new Date().toISOString(),url:url,http_status:200,readiness:j};last="invalid readiness payload";}else last="HTTP "+r.status;}catch(e){last=String(e&&e.message||e);}await new Promise(function(resolve){setTimeout(resolve,500);});
  }
  throw new Error("receiver READY not observed: "+last);
}
function validateHop(r,dir){require(r&&r.schema==="stegverse.intr.hop_receipt/v1",dir+" receipt schema invalid");require(r.boundary_verification==="VERIFIED",dir+" boundary not verified");require(r.authority_transfer===false&&r.secret_plaintext_present===false,dir+" authority/secret invariant failed");require(/^sha256:[0-9a-f]{64}$/.test(String(r.receipt_hash||"")),dir+" receipt hash invalid");require(r.transition_state===(dir==="ingress"?"RECEIVED":"FORWARDED"),dir+" transition mismatch");}
async function observeRoundTrip(node,request){var response=await root.StegVerseInterlockConnector.transact(request);require(response&&response.schema_version==="stegverse.sv002.public_observation.interlock_response.v1","observation response schema invalid");require(response.operation==="READ_OBSERVATION"&&response.authority_effect==="NONE"&&response.authority_transfer===false,"observation response authority invalid");require(response.observer_binding&&response.observer_binding.node_id===node.registration.node_id&&response.observer_binding.registration_receipt_sha256===node.registration.receipt_sha256,"observer binding mismatch");require(response.transport_receipts,"dual observation receipts required");var ingress=response.transport_receipts.ingress,egress=response.transport_receipts.egress;validateHop(ingress,"ingress");validateHop(egress,"egress");require(egress.prior_receipt_hash===ingress.receipt_hash,"egress does not bind ingress receipt");return response;}
async function run(){
  var runId="SV002-AUTH-"+(await sha256(new Date().toISOString()+":"+crypto.getRandomValues(new Uint32Array(1))[0])).slice(0,24);
  var bundle={schema:TEST_SCHEMA,run_id:runId,started_at:new Date().toISOString(),test_subject:"AUTHENTIC_SOVEREIGN_RUNTIME_TRANSPORT",device_node_revalidation_performed:false,condition_label:(el("conditionLabel").value||"").trim()||null,authority_effect:"NONE",evidence_classification:{node_proof:"NOT_OBSERVED",public_https_profile:"NOT_OBSERVED",materialization_ingress:"NOT_OBSERVED",receiver_readiness:"NOT_OBSERVED",observation_ingress:"NOT_OBSERVED",observation_egress:"NOT_OBSERVED",master_records_reconstruction:"NOT_CLAIMED",principal_experiment_execution:"NOT_CLAIMED"}};
  try{
    require(externalContext(),"AUTHENTIC_EXTERNAL_CONTEXT_REQUIRED: run from https://stegverse.org");
    var node=await root.StegVerseNodeContinuity.status();require(node&&node.registered,"VALID_NODE_REQUIRED: establish/validate the Node using the existing Node lane first");
    bundle.node_proof={node_id:node.registration.node_id,interlock_id:node.registration.interlock_id,registration_receipt_sha256:node.registration.receipt_sha256,genesis_receipt:node.receipts[0],consumed_not_reissued:true};bundle.evidence_classification.node_proof="CONSUMED_VALID_EXISTING_PROOF";setPhase("nodeState","VALID EXISTING RECEIPT #1");
    var profileObs=await observeProfile(runId);bundle.public_https_profile_observation=profileObs;bundle.evidence_classification.public_https_profile="OBSERVED";setPhase("profileState","OBSERVED / "+profileObs.profile_sha256);
    var target=targetFromProfile(profileObs);bundle.in_memory_runtime_target=target;
    var request=await buildObservationRequest(node);bundle.observation_request={request_sha256:request.request_sha256,request:request};
    var mat=await queueAndDeliver(target,request);bundle.materialization=mat;bundle.evidence_classification.materialization_ingress="OBSERVED";setPhase("materializationState","INGRESS_ADMITTED");
    var ready=await waitForReady(target);bundle.receiver_readiness=ready;bundle.evidence_classification.receiver_readiness="OBSERVED";setPhase("receiverState","READY");
    var response=await observeRoundTrip(node,request);bundle.observation_response=response;bundle.evidence_classification.observation_ingress="OBSERVED_RECEIVED";bundle.evidence_classification.observation_egress="OBSERVED_FORWARDED";setPhase("ingressState","RECEIVED");setPhase("egressState","FORWARDED");
    bundle.completed_at=new Date().toISOString();bundle.result="AUTHENTIC_RUNTIME_ROUND_TRIP_OBSERVED";bundle.bundle_sha256=await sha256(bundle);setMessage("Authentic Node-bound runtime round trip observed. This does not claim principal experiment execution or Master Records reconstruction.");el("statusCard").className="card good";render(bundle);return bundle;
  }catch(e){bundle.failed_at=new Date().toISOString();bundle.result="FAIL_CLOSED";bundle.failure=classifyError(e);bundle.bundle_sha256=await sha256(bundle);setMessage(bundle.failure.reason);el("statusCard").className="card bad";render(bundle);throw e;}
}
async function copyEvidence(){if(!lastBundle)return;await navigator.clipboard.writeText(JSON.stringify(lastBundle,null,2));setMessage("Evidence copied.");}
function exportEvidence(){if(!lastBundle)return;var blob=new Blob([JSON.stringify(lastBundle,null,2)+"\n"],{type:"application/json"}),a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download=lastBundle.run_id+".json";document.body.appendChild(a);a.click();a.remove();setTimeout(function(){URL.revokeObjectURL(a.href);},0);}
document.addEventListener("DOMContentLoaded",function(){el("runBtn").addEventListener("click",function(){el("runBtn").disabled=true;run().catch(function(){}).finally(function(){el("runBtn").disabled=false;});});el("copyBtn").addEventListener("click",function(){copyEvidence().catch(function(e){setMessage(e.message||e);});});el("exportBtn").addEventListener("click",exportEvidence);});
root.StegVerseSV002AuthenticRuntimeTest=Object.freeze({run:run,validateProfile:validateProfile,buildObservationRequest:buildObservationRequest,buildMaterializationRequest:buildMaterializationRequest,authority_effect:"NONE"});
}(typeof globalThis!=="undefined"?globalThis:window));
