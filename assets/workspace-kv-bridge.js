(function(root){
"use strict";
if(!root)return;
var RECORD_CLASS="WORKSPACE_PERSONAL_PROJECTION";
var RESULT_SCHEMA="stegverse.device-kv.query-result-delivery/v1";
var RESULT_REQUEST_SCHEMA="stegverse.device-kv.query-result-request/v1";
var PROJECTION_SCHEMA="stegverse.kv.personal-workspace-projection/v1";
function requireValue(ok,msg){if(!ok)throw new Error("FAIL_CLOSED: "+msg);}
function randomId(){var b=new Uint8Array(16);crypto.getRandomValues(b);return "SITE-WORKSPACE-KV-"+Array.from(b,x=>x.toString(16).padStart(2,"0")).join("");}
function delay(ms){return new Promise(r=>setTimeout(r,ms));}
function hex(buf){return Array.from(new Uint8Array(buf),x=>x.toString(16).padStart(2,"0")).join("");}
function shaBytes(bytes){return crypto.subtle.digest("SHA-256",bytes).then(hex);}
function buildQuery(nodeId){return {
 schema_version:"kv.interlock.request.v1",operation:"REQUEST",request_id:randomId(),
 requester:{module:"Site",component:"Workspace"},
 purpose:"Project the current owner's admitted Personal KnowledgeVault Workspace identity and relationship context.",
 record_class:RECORD_CLASS,
 requested_scope:["workspace_identity","principals","relationships","organizations","memberships","feed","assistant"],
 minimum_necessary_justification:"Return only Workspace metadata explicitly present in the current Personal KV; no credential material or provider authority.",
 authority_ref:"stegos-node://"+nodeId,disclosure_mode:"BOUNDED_CONTEXT",selector:{workspace_type:"PERSONAL"}
};}
function postResult(target,lookup){
 var intr=root.StegVerseGeneratedInTr;requireValue(intr&&typeof intr.canonical==="function","canonical InTr connector unavailable");
 var text=intr.canonical(lookup),bytes=new TextEncoder().encode(text);
 return shaBytes(bytes).then(function(hash){return fetch(target.result_url,{method:"POST",mode:"cors",cache:"no-store",credentials:"omit",headers:{"Content-Type":"application/json","X-StegVerse-Transport":"InTr","X-StegVerse-Transport-Origin":"STEGOS_NODE_OUTBOX","X-StegVerse-Payload-SHA256":hash},body:text}).then(async function(r){return {status:r.status,body:await r.json().catch(()=>null)};});});
}
function poll(target,lookup,n){return postResult(target,lookup).then(function(r){if(r.status===200)return r.body;if(r.status===400&&r.body&&r.body.reason==="device_kv_result_not_ready"&&n<20)return delay(250).then(()=>poll(target,lookup,n+1));throw new Error("FAIL_CLOSED: Workspace DEVICE_KV result unavailable"+(r.body&&r.body.reason?": "+r.body.reason:""));});}
function validateProjection(p){
 requireValue(p&&p.schema===PROJECTION_SCHEMA,"Personal Workspace projection schema invalid");
 requireValue(p.workspace_type==="PERSONAL","Personal Workspace projection type invalid");
 requireValue(["KV_WORKSPACE_PROJECTED","KV_WORKSPACE_EMPTY"].includes(p.state),"Personal Workspace projection state invalid");
 requireValue(p.credential_material_present===false&&p.provider_operation_authorized===false&&p.workspace_grants_authority===false&&p.authority_effect==="NONE","Personal Workspace projection authority invalid");
 for(var row of (p.principals||[]))requireValue(row.ai_label_required===(row.principal_type==="AI_ENTITY"),"AI label derivation mismatch");
 for(var org of (p.organizations||[]))requireValue(org.principal_type==="ORGANIZATION","organization principal type invalid");
 if(p.assistant)requireValue(p.assistant.principal_type==="AI_ENTITY"&&p.assistant.ai_label_required===true&&Array.isArray(p.assistant.roles)&&p.assistant.roles.includes("WORKSPACE_ASSISTANT"),"Workspace assistant identity invalid");
 return p;
}
function loadPersonalWorkspace(){
 var intr=root.StegVerseGeneratedInTr,hb=root.StegVerseHBInTrCarrier,node=root.StegVerseNodeContinuity,sync=root.StegVerseDeviceKVInTrSync;
 requireValue(intr&&typeof intr.buildIntent==="function"&&typeof intr.buildMaterializationRequest==="function","generated DEVICE_KV connector unavailable");
 requireValue(hb&&typeof hb.buildBinding==="function"&&typeof hb.recoverSignal==="function","HB/InTr carrier unavailable");
 requireValue(node&&typeof node.status==="function"&&typeof node.queueIntrMaterializationRequest==="function","registered Node continuity unavailable");
 requireValue(sync&&typeof sync.synchronizeMaterialization==="function"&&typeof sync.loadTarget==="function"&&typeof sync.getDeliveryReceipt==="function","DEVICE_KV sync unavailable");
 return node.status().then(function(s){
  requireValue(s&&s.registered===true&&s.registration&&s.registration.node_id,"Register this device before opening Personal Workspace KV context");
  var nodeId=s.registration.node_id,q=buildQuery(nodeId),bytes=new TextEncoder().encode(intr.canonical(q));
  return intr.buildIntent("device-kv",bytes,"REQUEST",q.request_id).then(intent=>hb.buildBinding(intent.packet_id,intent.payload_hash).then(binding=>intr.buildMaterializationRequest("device-kv",intent,"inline://materialization_request.kv_request",binding,{kv_request:q}))).then(function(m){
   return node.queueIntrMaterializationRequest(m).then(()=>sync.synchronizeMaterialization(m.materialization_id)).then(()=>Promise.all([sync.getDeliveryReceipt(m.materialization_id),sync.loadTarget(RECORD_CLASS)])).then(function(v){
    requireValue(v[0]&&v[0].network_delivery_observed===true,"Workspace DEVICE_KV ingress not observed");
    requireValue(v[1]&&v[1].state==="CONFORMING_SOVEREIGN_INTR_INGRESS"&&v[1].runtime_ingress_observed===true,"Workspace DEVICE_KV target unavailable");
    var lookup={schema:RESULT_REQUEST_SCHEMA,materialization_id:m.materialization_id,request_hash:m.request_hash,node_id:nodeId,authority_effect:"NONE_RESULT_LOOKUP_ONLY"};
    return poll(v[1],lookup,0).then(function(delivery){
     requireValue(delivery&&delivery.schema===RESULT_SCHEMA&&delivery.state==="RESULT_AVAILABLE","Workspace result delivery invalid");
     requireValue(delivery.materialization_id===m.materialization_id&&delivery.request_hash===m.request_hash&&delivery.node_id===nodeId,"Workspace result binding mismatch");
     requireValue(delivery.authority_effect==="NONE_RESULT_DELIVERY_ONLY"&&delivery.result_lookup_grants_authority===false,"Workspace result authority invalid");
     var response=delivery.response;
     requireValue(response&&response.schema==="stegverse.device-kv.query-response/v1"&&response.state==="QUERY_COMPLETE"&&response.record_class===RECORD_CLASS,"Workspace response invalid");
     requireValue(response.query_request_id===q.request_id&&response.request_grants_authority===false&&response.response_grants_authority===false&&response.authority_effect==="NONE","Workspace response authority/binding invalid");
     return hb.recoverSignal(delivery.response_carrier_signal).then(function(recovered){
      return intr.sha256Bytes(recovered).then(function(hash){requireValue(hash===delivery.response_payload_hash,"Workspace HB return payload mismatch");var decoded=JSON.parse(new TextDecoder().decode(recovered));requireValue(intr.canonical(decoded)===intr.canonical(response),"Workspace exact response recovery mismatch");return validateProjection(response.projection);});
     });
    });
   });
  });
 });
}
root.StegVerseWorkspaceKVBridge=Object.freeze({bridge_kind:"DEVICE_KV_QUERY_RETURN",loadPersonalWorkspace:loadPersonalWorkspace,authority_effect:"NONE"});
}(typeof globalThis!=="undefined"?globalThis:this));
