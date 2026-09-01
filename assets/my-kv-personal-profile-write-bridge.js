(function(root){
"use strict";
if(!root||root.StegVerseKVPersonalInfoBridge)return;
var RECORD_CLASS="PERSONAL_CONTACT_PROFILE";
var DEST="_Entities/Self/Personal_Contact_Profile.json";
var RESULT_REQUEST_SCHEMA="stegverse.device-kv.query-result-request/v1";
var RESULT_SCHEMA="stegverse.device-kv.query-result-delivery/v1";
function requireValue(ok,msg){if(!ok)throw new Error("FAIL_CLOSED: "+msg);}
function canon(v){var intr=root.StegVerseGeneratedInTr;return intr.canonical(v);}
function randomId(){var b=new Uint8Array(16);crypto.getRandomValues(b);return "SITE-PERSONAL-PROFILE-"+Array.from(b,x=>x.toString(16).padStart(2,"0")).join("");}
function bytes64(bytes){var out="",chunk=0x8000;for(var i=0;i<bytes.length;i+=chunk)out+=String.fromCharCode.apply(null,bytes.subarray(i,Math.min(i+chunk,bytes.length)));return btoa(out);}
function delay(ms){return new Promise(r=>setTimeout(r,ms));}
function buildReadRequest(nodeId){return {
 schema_version:"kv.interlock.request.v1",operation:"REQUEST",request_id:randomId(),
 requester:{module:"Site",component:"MyKVPersonalInfo"},
 purpose:"Read the current owner's canonical Personal Contact Profile from this KnowledgeVault.",
 record_class:RECORD_CLASS,requested_scope:["personal_profile"],
 minimum_necessary_justification:"Load only the owner's Personal Information profile needed to render and edit the My KV form.",
 authority_ref:"stegos-node://"+nodeId,disclosure_mode:"BOUNDED_CONTEXT"
};}
function buildRequest(nodeId,profile){
 var api=root.StegVerseMyKVPersonalInfo;requireValue(api&&api.validateProfile(profile).length===0,"profile validation failed");
 api.assertNoForbiddenKeys(profile);
 var bytes=new TextEncoder().encode(canon(profile));
 return {
  schema_version:"kv.interlock.request.v1",operation:"COMMIT_CANDIDATE",request_id:randomId(),
  requester:{module:"Site",component:"MyKVPersonalInfo"},
  purpose:"Owner-authorized replacement of the canonical Personal Contact Profile in this KnowledgeVault.",
  record_class:RECORD_CLASS,requested_scope:["personal_profile_update"],
  minimum_necessary_justification:"Persist only the owner-entered Personal Information profile; credentials and provider secrets are prohibited.",
  authority_ref:"stegos-node://"+nodeId,disclosure_mode:"BOUNDED_CONTEXT",
  candidate_writeback:{candidate_type:"PERSONAL_CONTACT_PROFILE_REPLACE",payload_ref:"data:application/vnd.stegverse.personal-contact-profile+json;base64,"+bytes64(bytes),requested_destination:DEST}
 };
}
function postResult(target,lookup){
 var text=canon(lookup),bytes=new TextEncoder().encode(text);
 return crypto.subtle.digest("SHA-256",bytes).then(function(d){var hash=Array.from(new Uint8Array(d),x=>x.toString(16).padStart(2,"0")).join("");return fetch(target.result_url,{method:"POST",mode:"cors",cache:"no-store",credentials:"omit",headers:{"Content-Type":"application/json","X-StegVerse-Transport":"InTr","X-StegVerse-Transport-Origin":"STEGOS_NODE_OUTBOX","X-StegVerse-Payload-SHA256":hash},body:text}).then(async r=>({status:r.status,body:await r.json().catch(()=>null)}));});
}
function poll(target,lookup,n){return postResult(target,lookup).then(function(r){if(r.status===200)return r.body;if(r.status===400&&r.body&&r.body.reason==="device_kv_result_not_ready"&&n<24)return delay(250).then(()=>poll(target,lookup,n+1));throw new Error("FAIL_CLOSED: Personal KV write result unavailable"+(r.body&&r.body.reason?": "+r.body.reason:""));});}
function transactRequest(q,expectedSchema,expectedState){
 var intr=root.StegVerseGeneratedInTr,hb=root.StegVerseHBInTrCarrier,node=root.StegVerseNodeContinuity,sync=root.StegVerseDeviceKVInTrSync;
 requireValue(intr&&typeof intr.buildIntent==="function"&&typeof intr.buildMaterializationRequest==="function","generated DEVICE_KV connector unavailable");
 requireValue(hb&&typeof hb.buildBinding==="function","HB/InTr carrier unavailable");
 requireValue(node&&typeof node.status==="function"&&typeof node.queueIntrMaterializationRequest==="function","registered Node continuity unavailable");
 requireValue(sync&&typeof sync.synchronizeMaterialization==="function"&&typeof sync.loadTarget==="function","DEVICE_KV sync unavailable");
 return node.status().then(function(s){
  requireValue(s&&s.registered===true&&s.registration&&s.registration.node_id,"Register this device before accessing Personal Information");
  var nodeId=s.registration.node_id;
  requireValue(q.authority_ref==="stegos-node://"+nodeId,"Personal profile request node binding invalid");
  var payload=new TextEncoder().encode(canon(q));
  return intr.buildIntent("device-kv",payload,q.operation,q.request_id)
   .then(intent=>hb.buildBinding(intent.packet_id,intent.payload_hash).then(binding=>intr.buildMaterializationRequest("device-kv",intent,"inline://materialization_request.kv_request",binding,{kv_request:q})))
   .then(function(m){return node.queueIntrMaterializationRequest(m).then(()=>sync.synchronizeMaterialization(m.materialization_id)).then(()=>sync.loadTarget(RECORD_CLASS)).then(function(target){
    requireValue(target&&target.state==="CONFORMING_SOVEREIGN_INTR_INGRESS"&&target.runtime_ingress_observed===true,"Personal KV receiver unavailable");
    var lookup={schema:RESULT_REQUEST_SCHEMA,materialization_id:m.materialization_id,request_hash:m.request_hash,node_id:nodeId,authority_effect:"NONE_RESULT_LOOKUP_ONLY"};
    return poll(target,lookup,0).then(function(delivery){
      requireValue(delivery&&delivery.schema===RESULT_SCHEMA&&delivery.state==="RESULT_AVAILABLE","Personal KV result delivery invalid");
      var response=delivery.response;
      requireValue(response&&response.schema===expectedSchema&&response.state===expectedState,"Personal KV response invalid");
      requireValue(response.request_id===q.request_id&&response.canonical_path===DEST&&response.authority_effect==="NONE","Personal KV response binding invalid");
      return {delivery:delivery,response:response};
    });
   });});
 });
}
function transact(profile){
 return root.StegVerseNodeContinuity.status().then(function(s){
  requireValue(s&&s.registered===true&&s.registration&&s.registration.node_id,"Register this device before saving Personal Information");
  var q=buildRequest(s.registration.node_id,profile);
  return transactRequest(q,"stegverse.device-kv.profile-update-response/v1","PROFILE_PERSISTED").then(function(result){
    requireValue(result.response.exact_readback_verified===true,"Personal KV write exact readback not verified");
    return {persisted:true,state:"KV_PERSISTED",message:"Personal information saved to KnowledgeVault.",receipt_hash:result.delivery.receipt_hash||null,response:result.response};
  });
 });
}
function loadProfile(){
 return root.StegVerseNodeContinuity.status().then(function(s){
  requireValue(s&&s.registered===true&&s.registration&&s.registration.node_id,"Register this device before loading Personal Information");
  var q=buildReadRequest(s.registration.node_id);
  return transactRequest(q,"stegverse.device-kv.personal-profile-response/v1","PROFILE_READ").then(function(result){
    var profile=result.response.profile,api=root.StegVerseMyKVPersonalInfo;
    requireValue(api&&api.validateProfile(profile).length===0,"Personal KV profile validation failed");
    api.assertNoForbiddenKeys(profile);
    return profile;
  });
 });
}
root.StegVerseKVPersonalInfoBridge=Object.freeze({bridge_kind:"DEVICE_KV_PERSONAL_PROFILE_READ_WRITE",authority_effect:"NONE",saveProfile:transact,loadProfile:loadProfile});
}(typeof globalThis!=="undefined"?globalThis:this));
