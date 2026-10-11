(function(root){
"use strict";
if(!root)return;
var RECORD_CLASS="WORKSPACE_PERSONAL_PROJECTION";
var TASKS_RECORD_CLASS="WORKSPACE_TASKS_PROJECTION";
var RESULT_SCHEMA="stegverse.device-kv.query-result-delivery/v1";
var RESULT_REQUEST_SCHEMA="stegverse.device-kv.query-result-request/v1";
var PROJECTION_SCHEMA="stegverse.kv.personal-workspace-projection/v1";
var TASKS_PROJECTION_SCHEMA="stegverse.kv.workspace-tasks-projection/v1";
var FAMILY_DELIVERY_SCHEMA="stegverse.kv.workspace-family-projections/v1";
var CHECKPOINT_DELIVERY_SCHEMA="stegverse.kv.workspace-continuity-checkpoint-delivery/v1";
var CHECKPOINT_DECISION_SCHEMA="stegverse.kv.workspace-continuity-checkpoint-decision/v1";
var RESERVED_FAMILY_SCHEMAS=[PROJECTION_SCHEMA,TASKS_PROJECTION_SCHEMA,"stegverse.kv.workspace-continuity-checkpoint/v1"];
// Each record class is one bounded DEVICE_KV query: its scope list, purpose and projection validator. The same node binding,
// InTr request, HB return and exact-recovery checks apply to every class; nothing here grants authority.
var QUERY_CLASSES={
 WORKSPACE_PERSONAL_PROJECTION:{scopes:["workspace_identity","principals","relationships","organizations","memberships","feed","assistant"],purpose:"Project the current owner's admitted Personal KnowledgeVault Workspace identity and relationship context.",justification:"Return only Workspace metadata explicitly present in the current Personal KV; no credential material or provider authority.",validate:validateProjection},
 WORKSPACE_TASKS_PROJECTION:{scopes:["tasks","commitments","timeline"],purpose:"Project the current owner's admitted Personal KnowledgeVault tasks and commitments.",justification:"Return only task and commitment rows explicitly present in the current Personal KV; no execution, credential material or provider authority.",validate:validateTasksProjection},
 WORKSPACE_FAMILY_PROJECTIONS:{scopes:["projections"],purpose:"Deliver the current owner's persisted capability-family KV projections to the Workspace page.",justification:"Return only family projections explicitly persisted in the current Personal KV, each with its own metadata; no credential material, provider operation or trade authority.",validate:validateFamilyDelivery},
 WORKSPACE_CONTINUITY_CHECKPOINT:{scopes:["checkpoint","decision"],purpose:"Deliver the current owner's stored Workspace continuity checkpoint and its transition decision.",justification:"Return only the stored checkpoint and the verifier's decision; nothing is anchored, verified or executed by this page.",validate:validateCheckpointDelivery}
};
function requireValue(ok,msg){if(!ok)throw new Error("FAIL_CLOSED: "+msg);}
function randomId(){var b=new Uint8Array(16);crypto.getRandomValues(b);return "SITE-WORKSPACE-KV-"+Array.from(b,x=>x.toString(16).padStart(2,"0")).join("");}
function delay(ms){return new Promise(r=>setTimeout(r,ms));}
function hex(buf){return Array.from(new Uint8Array(buf),x=>x.toString(16).padStart(2,"0")).join("");}
function shaBytes(bytes){return crypto.subtle.digest("SHA-256",bytes).then(hex);}
function buildQuery(nodeId,recordClass){var c=QUERY_CLASSES[recordClass||RECORD_CLASS];return {
 schema_version:"kv.interlock.request.v1",operation:"REQUEST",request_id:randomId(),
 requester:{module:"Site",component:"Workspace"},
 purpose:c.purpose,
 record_class:recordClass||RECORD_CLASS,
 requested_scope:c.scopes.slice(),
 minimum_necessary_justification:c.justification,
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
function validateTasksProjection(p){
 requireValue(p&&p.schema===TASKS_PROJECTION_SCHEMA,"Workspace tasks projection schema invalid");
 requireValue(p.workspace_type==="PERSONAL","Workspace tasks projection type invalid");
 requireValue(["KV_TASKS_PROJECTED","KV_TASKS_EMPTY"].includes(p.state),"Workspace tasks projection state invalid");
 requireValue(p.credential_material_present===false&&p.provider_operation_authorized===false&&p.workspace_grants_authority===false&&p.action_authority==="NONE"&&p.authority_effect==="NONE","Workspace tasks projection authority invalid");
 requireValue(Array.isArray(p.tasks)&&Array.isArray(p.commitments)&&Array.isArray(p.timeline),"Workspace tasks projection rows invalid");
 for(var row of p.tasks.concat(p.commitments,p.timeline))requireValue(row&&typeof row==="object"&&row.action_eligible===false&&row.execution_requires_admitted_manifest===true,"Workspace tasks row claims eligibility");
 requireValue(p.projection_metadata&&p.projection_metadata.schema==="stegverse.kv.workspace-projection-metadata/v1","Workspace tasks projection metadata invalid");
 return p;
}
function nonAuthorizing(p,label){requireValue(p&&typeof p==="object"&&p.workspace_type==="PERSONAL",label+" type invalid");requireValue(p.credential_material_present===false&&p.provider_operation_authorized===false&&p.workspace_grants_authority===false&&p.action_authority==="NONE"&&p.authority_effect==="NONE",label+" authority invalid");requireValue(p.projection_metadata&&p.projection_metadata.schema==="stegverse.kv.workspace-projection-metadata/v1",label+" metadata invalid");}
// Family projections are returned as the list the page's capability contract evaluates; each must be a PERSONAL,
// non-authorizing projection with its own metadata, and no reserved class may hide inside the list.
function validateFamilyDelivery(p){
 requireValue(p&&p.schema===FAMILY_DELIVERY_SCHEMA,"Workspace family delivery schema invalid");
 requireValue(["KV_FAMILY_PROJECTIONS_PROJECTED","KV_FAMILY_PROJECTIONS_EMPTY"].includes(p.state),"Workspace family delivery state invalid");
 nonAuthorizing(p,"Workspace family delivery");
 requireValue(Array.isArray(p.projections),"Workspace family delivery rows invalid");
 var seen={};
 for(var f of p.projections){
  requireValue(f&&typeof f==="object"&&typeof f.schema==="string"&&/^stegverse\.kv\.[a-z0-9-]+-projection\/v[0-9]+$/.test(f.schema),"Workspace family projection schema invalid");
  requireValue(!RESERVED_FAMILY_SCHEMAS.includes(f.schema),"Workspace family projection schema reserved");
  requireValue(!seen[f.schema],"Workspace family projection schema ambiguous");seen[f.schema]=true;
  requireValue(f.workspace_type==="PERSONAL"&&f.authority_effect==="NONE"&&f.credential_material_present===false&&f.provider_operation_authorized===false&&f.workspace_grants_authority===false&&f.trade_authority_granted!==true,"Workspace family projection authority invalid");
  requireValue(f.projection_metadata&&f.projection_metadata.schema==="stegverse.kv.workspace-projection-metadata/v1"&&f.projection_metadata.workspace_type==="PERSONAL","Workspace family projection metadata invalid");
 }
 return p.projections;
}
// The checkpoint delivery is handed to the assistant continuity contract as {checkpoint, decision}; the page verifies
// nothing itself, and a delivery that claims verification or an ALLOW decision is refused.
function validateCheckpointDelivery(p){
 requireValue(p&&p.schema===CHECKPOINT_DELIVERY_SCHEMA,"Workspace checkpoint delivery schema invalid");
 requireValue(["KV_CHECKPOINT_PROJECTED","KV_CHECKPOINT_ABSENT"].includes(p.state),"Workspace checkpoint delivery state invalid");
 nonAuthorizing(p,"Workspace checkpoint delivery");
 requireValue(p.anchor_verified===false,"Workspace checkpoint delivery claims verification");
 if(p.state==="KV_CHECKPOINT_ABSENT"){requireValue(p.checkpoint===null&&p.decision===null,"Workspace checkpoint delivery absent state invalid");return null;}
 requireValue(p.checkpoint&&typeof p.checkpoint==="object"&&p.checkpoint.schema==="stegverse.kv.workspace-continuity-checkpoint/v1","Workspace checkpoint schema invalid");
 var d=p.decision;
 requireValue(d&&typeof d==="object"&&d.schema===CHECKPOINT_DECISION_SCHEMA&&d.authority_effect==="NONE"&&["DENY","FAIL_CLOSED"].includes(d.disposition)&&typeof d.predicate==="string"&&["UNKNOWN","REFUSED"].includes(d.replay_status),"Workspace checkpoint decision invalid");
 return {checkpoint:p.checkpoint,decision:d};
}
var lastNodeBinding=null;
function refusal(d){var e=new Error("FAIL_CLOSED: "+d.predicate);e.decision=d;return e;}
// WU2: the page never registers a device identity. A directly observed registration binds; otherwise only an admitted
// stegos.device_continuity_recovery_result.v1 (StegOS#347 owner) may rehydrate the retained node, and only through a
// node-continuity rehydration interface. Absent both, the Personal KV path fails closed with the work unit named.
function bindNode(node,options){
 var binding=root.StegVerseWorkspaceNodeBinding;requireValue(binding&&typeof binding.resolve==="function","Workspace node-binding contract unavailable");
 var recovery=options&&Object.prototype.hasOwnProperty.call(options,"recovery_result")?options.recovery_result:null;
 return node.status().then(function(s){return binding.resolve(s,recovery).then(function(d){
  lastNodeBinding=d;
  if(d.disposition!=="ALLOW")throw refusal(d);
  if(d.source==="DEVICE_LOCAL_REGISTRATION")return s;
  if(typeof node.rehydrateRegistration!=="function"){
   lastNodeBinding=Object.assign({},d,{disposition:"FAIL_CLOSED",predicate:"LOCAL_REHYDRATION_INTERFACE_NOT_AVAILABLE",rehydration_owner:"StegOS node continuity (assets/stegverse-node-continuity-impl.js)"});
   throw refusal(lastNodeBinding);
  }
  return node.rehydrateRegistration(recovery).then(function(){return node.status();}).then(function(s2){
   requireValue(s2&&s2.registered===true&&s2.registration&&s2.registration.node_id===d.node_id,"rehydrated registration does not match the admitted retained node");
   return s2;
  });
 });});
}
function loadPersonalWorkspace(options){return loadProjection(RECORD_CLASS,options);}
// WS-TASKS delivery: the same DEVICE_KV query path, bound to the WORKSPACE_TASKS_PROJECTION record class that the
// resident consumer serves from continuity-vault-kit runtime/workspace_tasks_projection.py.
function loadPersonalTasks(options){return loadProjection(TASKS_RECORD_CLASS,options);}
// P4 delivery: the list of persisted family projections (e.g. the CryptoBot portfolio) for the capability contract.
function loadPersonalProjections(options){return loadProjection("WORKSPACE_FAMILY_PROJECTIONS",options);}
// WS-ASSISTANT delivery: {checkpoint, decision} for the assistant continuity contract, or null when none is stored.
function loadAssistantCheckpoint(options){return loadProjection("WORKSPACE_CONTINUITY_CHECKPOINT",options);}
function loadProjection(recordClass,options){
 var cls=QUERY_CLASSES[recordClass];requireValue(!!cls,"Workspace record class not admitted");
 var intr=root.StegVerseGeneratedInTr,hb=root.StegVerseHBInTrCarrier,node=root.StegVerseNodeContinuity,sync=root.StegVerseDeviceKVInTrSync;
 requireValue(intr&&typeof intr.buildIntent==="function"&&typeof intr.buildMaterializationRequest==="function","generated DEVICE_KV connector unavailable");
 requireValue(hb&&typeof hb.buildBinding==="function"&&typeof hb.recoverSignal==="function","HB/InTr carrier unavailable");
 requireValue(node&&typeof node.status==="function"&&typeof node.queueIntrMaterializationRequest==="function","registered Node continuity unavailable");
 requireValue(sync&&typeof sync.synchronizeMaterialization==="function"&&typeof sync.loadTarget==="function"&&typeof sync.getDeliveryReceipt==="function","DEVICE_KV sync unavailable");
 return bindNode(node,options).then(function(s){
  var nodeId=s.registration.node_id,q=buildQuery(nodeId,recordClass),bytes=new TextEncoder().encode(intr.canonical(q));
  return intr.buildIntent("device-kv",bytes,"REQUEST",q.request_id).then(intent=>hb.buildBinding(intent.packet_id,intent.payload_hash).then(binding=>intr.buildMaterializationRequest("device-kv",intent,"inline://materialization_request.kv_request",binding,{kv_request:q}))).then(function(m){
   return node.queueIntrMaterializationRequest(m).then(()=>sync.synchronizeMaterialization(m.materialization_id)).then(()=>Promise.all([sync.getDeliveryReceipt(m.materialization_id),sync.loadTarget(recordClass)])).then(function(v){
    requireValue(v[0]&&v[0].network_delivery_observed===true,"Workspace DEVICE_KV ingress not observed");
    requireValue(v[1]&&v[1].state==="CONFORMING_SOVEREIGN_INTR_INGRESS"&&v[1].runtime_ingress_observed===true,"Workspace DEVICE_KV target unavailable");
    var lookup={schema:RESULT_REQUEST_SCHEMA,materialization_id:m.materialization_id,request_hash:m.request_hash,node_id:nodeId,authority_effect:"NONE_RESULT_LOOKUP_ONLY"};
    return poll(v[1],lookup,0).then(function(delivery){
     requireValue(delivery&&delivery.schema===RESULT_SCHEMA&&delivery.state==="RESULT_AVAILABLE","Workspace result delivery invalid");
     requireValue(delivery.materialization_id===m.materialization_id&&delivery.request_hash===m.request_hash&&delivery.node_id===nodeId,"Workspace result binding mismatch");
     requireValue(delivery.authority_effect==="NONE_RESULT_DELIVERY_ONLY"&&delivery.result_lookup_grants_authority===false,"Workspace result authority invalid");
     var response=delivery.response;
     requireValue(response&&response.schema==="stegverse.device-kv.query-response/v1"&&response.state==="QUERY_COMPLETE"&&response.record_class===recordClass,"Workspace response invalid");
     requireValue(response.query_request_id===q.request_id&&response.request_grants_authority===false&&response.response_grants_authority===false&&response.authority_effect==="NONE","Workspace response authority/binding invalid");
     return hb.recoverSignal(delivery.response_carrier_signal).then(function(recovered){
      return intr.sha256Bytes(recovered).then(function(hash){requireValue(hash===delivery.response_payload_hash,"Workspace HB return payload mismatch");var decoded=JSON.parse(new TextDecoder().decode(recovered));requireValue(intr.canonical(decoded)===intr.canonical(response),"Workspace exact response recovery mismatch");return cls.validate(response.projection);});
     });
    });
   });
  });
 });
}
root.StegVerseWorkspaceKVBridge=Object.freeze({bridge_kind:"DEVICE_KV_QUERY_RETURN",record_classes:Object.keys(QUERY_CLASSES),loadPersonalWorkspace:loadPersonalWorkspace,loadPersonalTasks:loadPersonalTasks,loadPersonalProjections:loadPersonalProjections,loadAssistantCheckpoint:loadAssistantCheckpoint,lastNodeBinding:function(){return lastNodeBinding;},authority_effect:"NONE"});
}(typeof globalThis!=="undefined"?globalThis:this));
