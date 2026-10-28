(function(root){
"use strict";
if(!root)return;
// Plain-language reason per kv-bridge predicate, for the explanation contract (.github#3106). Explanatory only.
var REASONS={
 "LOCAL_REHYDRATION_INTERFACE_NOT_AVAILABLE":"the interface that restores your existing device node in this browser is not available",
 "DEVICE_KV_RESULT_NOT_YET_MATERIALIZED":"your request was accepted and is held in this device's outbox, but its result has not been produced yet, so nothing is shown until it is",
 "DEVICE_KV_REQUEST_QUEUED_NOT_DELIVERED":"your request is held in this device's outbox and has not been delivered to your KnowledgeVault yet, so nothing is shown",
 "SOVEREIGN_INTR_INGRESS_TARGET_NOT_PROJECTED":"the destination that receives requests for your KnowledgeVault has not been published to this page, so the request stays in this device's outbox",
 "DEVICE_KV_RESULT_UNAVAILABLE":"your KnowledgeVault did not return a usable result for this request, so nothing is shown; the reason it gave is kept with this refusal",
 "WORKSPACE_FAMILY_PROJECTION_SECRET_FIELD":"a delivered projection contains something shaped like a password, token or other credential, so none of the delivered projections are shown; credentials stay only in your SKAP Vault",
 "EMAIL_PROJECTION_ACCOUNT_INVALID":"an email projection does not name each account with its source and cursor, so none of the delivered projections are shown",
 "EMAIL_PROJECTION_ADMIT_RECEIPT_ABSENT":"an email account in the projection has no admission receipt from your KnowledgeVault, so none of the delivered projections are shown",
 "EMAIL_PROJECTION_ADMIT_RECEIPT_STALE":"an email account's admission receipt covers an older point in that mailbox than the one projected, so none of the delivered projections are shown",
 "EMAIL_PROJECTION_ACCOUNTS_MIXED":"an email projection mixes records between accounts or names one account twice, so none of the delivered projections are shown",
 "EMAIL_PROJECTION_RECORD_DUPLICATED":"an email account lists the same message more than once, which can mean a replay, and one copy is never chosen silently, so none of the delivered projections are shown"
};
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
// ACTIONS BY MANIFEST (Task Registry invariant NO_EXTERNAL_MACHINE_AWAITING_AS_TRANSITION_PREDICATE): the request is
// already durably queued in the node outbox, so the result is looked up exactly once. A result that is not yet
// materialized is an actionable FAIL_CLOSED disposition naming the queued materialization, never a wait or retry loop.
// Organization Role conformance standard (.github docs/ORGANIZATION_ROLE_RUNTIME_REALITY_DEPLOYMENT.md): a non-ALLOW
// result carries failure_code, failed_predicate, required_evidence_or_repair, retry_entrypoint, owning_existing_goal
// and next_attempt; a bare not-ready or unavailable is not a finding.
var OWNING_GOAL="STEGVERSE-WORKSPACE-ANY-DEVICE-KV-SURFACE-001",RETRY_ENTRYPOINT="StegVerseWorkspaceKVBridge.loadPersonalWorkspace (Site assets/workspace-kv-bridge.js)";
function actionable(predicate,repair,next,extra){return refusal(Object.assign({disposition:"FAIL_CLOSED",predicate:predicate,failure_code:predicate,failed_predicate:predicate,required_evidence_or_repair:repair,retry_entrypoint:RETRY_ENTRYPOINT,owning_existing_goal:OWNING_GOAL,next_attempt:next,authority_effect:"NONE"},extra||{}));}
function lookupResult(target,lookup){return postResult(target,lookup).then(function(r){if(r.status===200)return r.body;if(r.status===400&&r.body&&r.body.reason==="device_kv_result_not_ready")throw actionable("DEVICE_KV_RESULT_NOT_YET_MATERIALIZED","the resident DEVICE_KV consumer materializes the result of the queued request "+lookup.materialization_id,"the next WorkSpace load queues a new request and looks its result up once; nothing waits",{materialization_id:lookup.materialization_id,request_hash:lookup.request_hash});throw actionable("DEVICE_KV_RESULT_UNAVAILABLE","a result delivery for the queued request "+lookup.materialization_id+" from the DEVICE_KV result interface (it answered HTTP "+r.status+(r.body&&r.body.reason?" with reason "+r.body.reason:"")+")","the next WorkSpace load queues a new request and looks its result up once; nothing waits",{materialization_id:lookup.materialization_id,request_hash:lookup.request_hash,http_status:r.status,reason:(r.body&&typeof r.body.reason==="string")?r.body.reason:null});});}
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
// Site#1509 lane B (Goal StegVerse-org/.github#164): the consumer does not trust credential_material_present alone. Every
// key in a family delivery is checked, at any depth, for credential-shaped names, and string values for bearer or
// private-key material. The only credential-named fields allowed are the false flag and a skap:// reference (SKAP Vault
// alone holds credentials). Any hit refuses the whole delivery with the six actionable fields.
var FAMILY_RETRY_ENTRYPOINT="StegVerseWorkspaceKVBridge.loadPersonalProjections (Site assets/workspace-kv-bridge.js)",FAMILY_NEXT="the next WorkSpace load queues a new family request and evaluates the delivered projections again; nothing waits";
var SECRET_KEY=/(^|_)(password|passwd|passcode|secret|token|tokens|oauth|apikey|api_key|private_key|bearer|cookie|cookies|authorization|credential|credentials|session_key|otp|mfa_seed|totp_seed)(_|$)/;
var SECRET_VALUE=/^\s*bearer\s+\S|-----BEGIN [A-Z ]*PRIVATE KEY-----/i;
function familyExtra(extra){return Object.assign({retry_entrypoint:FAMILY_RETRY_ENTRYPOINT},extra||{});}
function keyName(k){return String(k).replace(/([a-z0-9])([A-Z])/g,"$1_$2").toLowerCase().replace(/[^a-z0-9]+/g,"_");}
function secretPath(v,path,depth){
 if(depth>32)return path+" (nesting deeper than 32)";
 if(typeof v==="string")return SECRET_VALUE.test(v)?path:null;
 if(!v||typeof v!=="object")return null;
 if(Array.isArray(v)){for(var i=0;i<v.length;i++){var hit=secretPath(v[i],path+"["+i+"]",depth+1);if(hit)return hit;}return null;}
 for(var k in v){if(!Object.prototype.hasOwnProperty.call(v,k))continue;var n=keyName(k),x=v[k];
  if(n==="credential_material_present"){if(x!==false)return path+"."+k;continue;}
  if(n==="credential_ref"){if(!(typeof x==="string"&&/^skap:\/\/[^\s]+$/.test(x)))return path+"."+k;continue;}
  if(SECRET_KEY.test(n))return path+"."+k;
  var hit2=secretPath(x,path+"."+k,depth+1);if(hit2)return hit2;}
 return null;
}
// Email-family projections (stegverse.kv.email[-*]-projection/vN) travel in the existing WORKSPACE_FAMILY_PROJECTIONS
// list; no email-specific query class exists or is needed. The consumer checks what it can check from the delivery
// alone: each account is named once with its source provider and cursor; each carries the KV ADMIT receipt (reference
// plus sha256 digest) whose cursor is the projected cursor, so an absent or stale receipt fails closed; every message
// row is bound to its own account; and no message appears twice in one account. Cross-delivery replay or cursor
// rollback needs the authenticated continuity checkpoint and stays REPLAY_STATUS_UNKNOWN here.
var EMAIL_FAMILY_SCHEMA=/^stegverse\.kv\.email(?:-[a-z0-9]+)*-projection\/v[0-9]+$/;
function isRecord(v){return !!v&&typeof v==="object"&&!Array.isArray(v);}
function nonEmpty(v){return typeof v==="string"&&v.trim().length>0;}
function validateEmailFamily(f){
 var extra={projection_schema:f.schema};
 var invalid=function(what){return actionable("EMAIL_PROJECTION_ACCOUNT_INVALID","the KV email projection producer names every account once with account_id, source.provider, source.cursor and a messages list ("+what+")",FAMILY_NEXT,familyExtra(extra));};
 if(!Array.isArray(f.accounts))throw invalid("accounts is not a list");
 var accounts={};
 for(var i=0;i<f.accounts.length;i++){var a=f.accounts[i];
  if(!isRecord(a)||!nonEmpty(a.account_id))throw invalid("account "+i+" has no account_id");
  if(Object.prototype.hasOwnProperty.call(accounts,a.account_id))throw actionable("EMAIL_PROJECTION_ACCOUNTS_MIXED","the KV email projection producer emits each account exactly once; account "+a.account_id+" appears twice",FAMILY_NEXT,familyExtra(extra));
  accounts[a.account_id]=true;
  if(!isRecord(a.source)||!nonEmpty(a.source.provider)||!nonEmpty(a.source.cursor))throw invalid("account "+a.account_id+" has no source provider or cursor");
  var r=a.admit_receipt;
  if(!isRecord(r)||!nonEmpty(r.receipt_ref)||!(typeof r.receipt_digest==="string"&&/^sha256:[0-9a-f]{64}$/.test(r.receipt_digest))||!nonEmpty(r.cursor))throw actionable("EMAIL_PROJECTION_ADMIT_RECEIPT_ABSENT","the CVK governed ADMIT receipt (receipt_ref, sha256 receipt_digest and admitted cursor) for account "+a.account_id,FAMILY_NEXT,familyExtra(extra));
  if(r.cursor!==a.source.cursor)throw actionable("EMAIL_PROJECTION_ADMIT_RECEIPT_STALE","an ADMIT receipt for account "+a.account_id+" whose cursor is the projected cursor; the receipt covers an older or different cursor",FAMILY_NEXT,familyExtra(extra));
  if(!Array.isArray(a.messages))throw invalid("account "+a.account_id+" has no messages list");
  var seen={};
  for(var j=0;j<a.messages.length;j++){var m=a.messages[j];
   if(!isRecord(m)||!nonEmpty(m.message_id))throw invalid("account "+a.account_id+" message "+j+" has no message_id");
   if(m.account_id!==a.account_id)throw actionable("EMAIL_PROJECTION_ACCOUNTS_MIXED","the KV email projection producer keeps every message under its own account; message "+j+" of account "+a.account_id+" is bound to another account",FAMILY_NEXT,familyExtra(extra));
   if(Object.prototype.hasOwnProperty.call(seen,m.message_id))throw actionable("EMAIL_PROJECTION_RECORD_DUPLICATED","the KV email projection producer emits each admitted message once per account; account "+a.account_id+" repeats a message",FAMILY_NEXT,familyExtra(extra));
   seen[m.message_id]=true;
  }
 }
}
// Family projections are returned as the list the page's capability contract evaluates; each must be a PERSONAL,
// non-authorizing projection with its own metadata, and no reserved class may hide inside the list.
function validateFamilyDelivery(p){
 requireValue(p&&p.schema===FAMILY_DELIVERY_SCHEMA,"Workspace family delivery schema invalid");
 requireValue(["KV_FAMILY_PROJECTIONS_PROJECTED","KV_FAMILY_PROJECTIONS_EMPTY"].includes(p.state),"Workspace family delivery state invalid");
 nonAuthorizing(p,"Workspace family delivery");
 requireValue(Array.isArray(p.projections),"Workspace family delivery rows invalid");
 var secret=secretPath(p,"$",0);
 if(secret)throw actionable("WORKSPACE_FAMILY_PROJECTION_SECRET_FIELD","the KV projection producer removes credential-shaped material; credentials stay in SKAP Vault and only skap:// references may be projected (found at "+secret+")",FAMILY_NEXT,familyExtra({secret_path:secret}));
 var seen={};
 for(var f of p.projections){
  requireValue(f&&typeof f==="object"&&typeof f.schema==="string"&&/^stegverse\.kv\.[a-z0-9-]+-projection\/v[0-9]+$/.test(f.schema),"Workspace family projection schema invalid");
  requireValue(!RESERVED_FAMILY_SCHEMAS.includes(f.schema),"Workspace family projection schema reserved");
  requireValue(!seen[f.schema],"Workspace family projection schema ambiguous");seen[f.schema]=true;
  requireValue(f.workspace_type==="PERSONAL"&&f.authority_effect==="NONE"&&f.credential_material_present===false&&f.provider_operation_authorized===false&&f.workspace_grants_authority===false&&f.trade_authority_granted!==true,"Workspace family projection authority invalid");
  requireValue(f.projection_metadata&&f.projection_metadata.schema==="stegverse.kv.workspace-projection-metadata/v1"&&f.projection_metadata.workspace_type==="PERSONAL","Workspace family projection metadata invalid");
  if(EMAIL_FAMILY_SCHEMA.test(f.schema))validateEmailFamily(f);
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
    // Destination existence is sufficient; destination liveness is never a predicate (Organization Role conformance
    // standard, item 2). The target must exist (a projected result locator); whether its runtime was observed is not read.
    if(!(v[1]&&v[1].state==="CONFORMING_SOVEREIGN_INTR_INGRESS"&&typeof v[1].result_url==="string"&&v[1].result_url))throw actionable("SOVEREIGN_INTR_INGRESS_TARGET_NOT_PROJECTED","the StegOS node owner projects stegos-node/device-kv-intr-sync-target.json with the existing sovereign InTr ingress and result locators","the next WorkSpace load reads the projected target; the request is already held in the node outbox",{materialization_id:m.materialization_id});
    // The delivery receipt is the egress record of this transition; without it the request is still durably queued.
    if(!(v[0]&&v[0].network_delivery_observed===true))throw actionable("DEVICE_KV_REQUEST_QUEUED_NOT_DELIVERED","the node outbox delivers the queued request "+m.materialization_id+" to the projected ingress and records its delivery receipt","the next WorkSpace load delivers from the outbox and looks the result up once; nothing waits",{materialization_id:m.materialization_id});
    var lookup={schema:RESULT_REQUEST_SCHEMA,materialization_id:m.materialization_id,request_hash:m.request_hash,node_id:nodeId,authority_effect:"NONE_RESULT_LOOKUP_ONLY"};
    return lookupResult(v[1],lookup).then(function(delivery){
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
root.StegVerseWorkspaceKVBridge=Object.freeze({reasons:Object.freeze(Object.assign({},REASONS)),bridge_kind:"DEVICE_KV_QUERY_RETURN",record_classes:Object.keys(QUERY_CLASSES),loadPersonalWorkspace:loadPersonalWorkspace,loadPersonalTasks:loadPersonalTasks,loadPersonalProjections:loadPersonalProjections,loadAssistantCheckpoint:loadAssistantCheckpoint,lastNodeBinding:function(){return lastNodeBinding;},authority_effect:"NONE"});
}(typeof globalThis!=="undefined"?globalThis:this));
