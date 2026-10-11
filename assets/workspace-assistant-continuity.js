// WorkSpace MyKV assistant continuity / evidence / consent presentation (Site#1509 WS-ASSISTANT).
// Derives stegverse.workspace.assistant-continuity/v1 from three inputs the page already holds: the session
// authentication decision (stegverse.workspace.session-authentication/v1), the assistant binding decision
// (stegverse.kv.workspace-assistant-binding/v1, the browser port of the CVK resolver) and, when the authenticated KV
// path delivers one, an earlier continuity checkpoint (stegverse.kv.workspace-continuity-checkpoint/v1, the schema the
// binding already names). The assistant is only ever the user's existing MyKV assistant: a checkpoint naming a
// different assistant fails closed instead of being adopted, nothing here invokes anything, no generic LLM exists,
// and consent is a producer-supplied record that is displayed and may be requested, never granted by this page.
(function(root){
"use strict";
if(!root)return;
var SCHEMA="stegverse.workspace.assistant-continuity/v1";
var CHECKPOINT_SCHEMA="stegverse.kv.workspace-continuity-checkpoint/v1";
var BINDING_SCHEMA="stegverse.kv.workspace-assistant-binding/v1";
var CONSENT_STATES=["GRANTED","REVOKED","NOT_SUPPLIED"];
function isObject(v){return !!v&&typeof v==="object"&&!Array.isArray(v);}
function nonEmpty(v){return typeof v==="string"&&v.length>0;}
function str(v){return typeof v==="string"?v:null;}
function row(source,label,value){return {source:source,label:label,value:value===undefined||value===null?"NOT_SUPPLIED":String(value)};}
function base(disposition,predicate){
 return {schema:SCHEMA,disposition:disposition,predicate:predicate,identity:null,
  continuity:{state:"WITHHELD",predicate:predicate,key:null,checkpoint_ref:null,checkpoint_observed_at:null,source_revision:null,provenance_ref:null,replay_status:"REPLAY_STATUS_UNKNOWN"},
  evidence:[],consent:{state:"WITHHELD",predicate:predicate,scope:[],consent_ref:null,granted_at:null,recorded_by:null,proposable_actions:[]},
  generic_llm_fallback:"FORBIDDEN",invocation_route:"NOT_AVAILABLE",ephemeral_inference:"NOT_AVAILABLE",action_eligible:false,authority_effect:"NONE"};
}
function sessionRows(sa){
 var s=isObject(sa)?sa:{};
 return [row("SESSION_AUTHENTICATION","session disposition",(s.disposition||"FAIL_CLOSED")+" · "+(s.predicate||"SESSION_AUTHENTICATION_RESOLVER_UNAVAILABLE")),
  row("SESSION_AUTHENTICATION","admission class",s.admission_class||"CALLER_SUPPLIED_FIELDS_ACCEPTED"),
  row("SESSION_AUTHENTICATION","verification",s.verification||"CALLER_SUPPLIED_NOT_PAGE_VERIFIED"),
  row("SESSION_AUTHENTICATION","runtime authentication evidence","false")];
}
function sameKey(a,b){return isObject(a)&&isObject(b)&&a.owner_principal_id===b.owner_principal_id&&a.assistant_principal_id===b.assistant_principal_id&&(a.workspace_id===undefined?null:a.workspace_id)===(b.workspace_id===undefined?null:b.workspace_id);}
function consentFrom(checkpoint){
 var out={state:"NOT_SUPPLIED",predicate:"CONSENT_RECORD_NOT_OBSERVED",scope:[],consent_ref:null,granted_at:null,recorded_by:null,proposable_actions:["ASSISTANT_CONSENT_GRANT"]};
 if(!isObject(checkpoint))return out;
 var c=checkpoint.consent;
 if(c===undefined||c===null){out.predicate="CONSENT_RECORD_ABSENT_FROM_CHECKPOINT";return out;}
 if(!isObject(c)||CONSENT_STATES.indexOf(c.state)<0)return {state:"MALFORMED",predicate:"CONSENT_RECORD_INVALID",scope:[],consent_ref:null,granted_at:null,recorded_by:null,proposable_actions:[]};
 if(c.state==="GRANTED"){
  if(!nonEmpty(c.consent_ref)||!Array.isArray(c.scope)||!c.scope.every(nonEmpty))return {state:"MALFORMED",predicate:"CONSENT_GRANT_UNREFERENCED",scope:[],consent_ref:null,granted_at:null,recorded_by:null,proposable_actions:[]};
  return {state:"GRANTED",predicate:"CONSENT_RECORD_OBSERVED",scope:c.scope.slice(),consent_ref:c.consent_ref,granted_at:str(c.granted_at),recorded_by:str(c.recorded_by),proposable_actions:["ASSISTANT_CONSENT_WITHDRAW"]};
 }
 if(c.state==="REVOKED")return {state:"REVOKED",predicate:"CONSENT_RECORD_REVOKED",scope:[],consent_ref:str(c.consent_ref),granted_at:null,recorded_by:str(c.recorded_by),proposable_actions:[]};
 out.predicate="CONSENT_RECORD_NOT_SUPPLIED";return out;
}
function build(input){
 var inp=isObject(input)?input:{},sa=inp.session_authentication,d=inp.decision,cp=inp.checkpoint;
 var out;
 if(!isObject(sa)||sa.disposition!=="ALLOW"){out=base("FAIL_CLOSED",isObject(sa)&&nonEmpty(sa.predicate)?sa.predicate:"SESSION_PRINCIPAL_UNAUTHENTICATED");out.evidence=sessionRows(sa);out.continuity.state="NOT_EVALUATED";out.consent.state="WITHHELD";return out;}
 if(!isObject(d)||d.schema!==BINDING_SCHEMA){out=base("FAIL_CLOSED","ASSISTANT_BINDING_DECISION_UNAVAILABLE");out.evidence=sessionRows(sa);return out;}
 if(d.disposition!=="ALLOW"||!isObject(d.binding)){out=base(d.disposition==="DENY"?"DENY":"FAIL_CLOSED",nonEmpty(d.predicate)?d.predicate:"ASSISTANT_BINDING_REFUSED");out.evidence=sessionRows(sa).concat([row("BINDING_DECISION","binding",d.disposition+" · "+d.predicate)]);if(d.predicate==="WORKSPACE_GRANT_REVOKED"){out.continuity.state="REVOKED";out.consent.state="REVOKED";}return out;}
 var b=d.binding,c=isObject(b.continuity)?b.continuity:{},key=isObject(c.key)?c.key:null;
 if(!key||!nonEmpty(key.owner_principal_id)||!nonEmpty(key.assistant_principal_id)||!nonEmpty(b.assistant_principal_id)){out=base("FAIL_CLOSED","BINDING_CONTINUITY_KEY_INVALID");out.evidence=sessionRows(sa);return out;}
 var evidence=sessionRows(sa).concat([
  row("BINDING_DECISION","binding","ALLOW · "+d.predicate),
  row("BINDING_DECISION","assistant",b.assistant_principal_id+(b.assistant_display_name?" ("+b.assistant_display_name+")":"")),
  row("BINDING_DECISION","owner",b.owner_principal_id),
  row("BINDING_DECISION","relationship",b.relationship_state||"NOT_SUPPLIED"),
  row("KV_PROJECTION_METADATA","source revision",c.source_revision),
  row("KV_PROJECTION_METADATA","provenance",c.provenance_ref),
  row("KV_PROJECTION_METADATA","observed at",c.observed_at),
  row("KV_PROJECTION_METADATA","grant state",b.grant_state||"UNKNOWN")]);
 var continuity={state:"CONTINUITY_UNKNOWN",predicate:"CHECKPOINT_NOT_OBSERVED",key:{owner_principal_id:key.owner_principal_id,assistant_principal_id:key.assistant_principal_id,workspace_id:key.workspace_id===undefined?null:key.workspace_id},checkpoint_ref:null,checkpoint_observed_at:null,source_revision:str(c.source_revision),provenance_ref:str(c.provenance_ref),replay_status:"REPLAY_STATUS_UNKNOWN"};
 if(cp!==undefined&&cp!==null){
  if(!isObject(cp)||cp.schema!==CHECKPOINT_SCHEMA){out=base("FAIL_CLOSED","CHECKPOINT_SCHEMA_INVALID");out.evidence=evidence;out.continuity.state="MALFORMED";return out;}
  if(cp.authority_effect!=="NONE"){out=base("FAIL_CLOSED","CHECKPOINT_AUTHORITY_INVALID");out.evidence=evidence;out.continuity.state="MALFORMED";return out;}
  if(!isObject(cp.key)){out=base("FAIL_CLOSED","CHECKPOINT_KEY_ABSENT");out.evidence=evidence;out.continuity.state="MALFORMED";return out;}
  if(cp.key.owner_principal_id!==key.owner_principal_id){out=base("FAIL_CLOSED","CHECKPOINT_OWNER_MISMATCH");out.evidence=evidence;return out;}
  if((cp.key.workspace_id===undefined?null:cp.key.workspace_id)!==(key.workspace_id===undefined?null:key.workspace_id)){out=base("FAIL_CLOSED","CHECKPOINT_WORKSPACE_MISMATCH");out.evidence=evidence;return out;}
  // The only assistant is the user's existing one: a checkpoint for another identity is never adopted or merged.
  if(cp.key.assistant_principal_id!==key.assistant_principal_id){out=base("FAIL_CLOSED","ASSISTANT_IDENTITY_CHANGED");out.evidence=evidence.concat([row("CONTINUITY_CHECKPOINT","checkpoint assistant",cp.key.assistant_principal_id)]);out.continuity.state="IDENTITY_CHANGED";return out;}
  if(cp.revoked===true||cp.grant_state==="REVOKED"){out=base("DENY","CONTINUITY_REVOKED");out.evidence=evidence.concat([row("CONTINUITY_CHECKPOINT","checkpoint",str(cp.checkpoint_ref)),row("CONTINUITY_CHECKPOINT","grant state","REVOKED")]);out.continuity.state="REVOKED";out.consent.state="REVOKED";return out;}
  if(!sameKey(cp.key,key)){out=base("FAIL_CLOSED","CHECKPOINT_KEY_MISMATCH");out.evidence=evidence;return out;}
  continuity.state="CONTINUOUS_SAME_ASSISTANT";continuity.predicate="CHECKPOINT_KEY_MATCHES_BINDING";
  continuity.checkpoint_ref=str(cp.checkpoint_ref);continuity.checkpoint_observed_at=str(cp.observed_at);
  continuity.replay_status=nonEmpty(cp.replay_status)?cp.replay_status:"REPLAY_STATUS_UNKNOWN";
  evidence=evidence.concat([row("CONTINUITY_CHECKPOINT","checkpoint",cp.checkpoint_ref),row("CONTINUITY_CHECKPOINT","checkpoint observed at",cp.observed_at),row("CONTINUITY_CHECKPOINT","checkpoint source revision",cp.source_revision),row("CONTINUITY_CHECKPOINT","replay status",continuity.replay_status)]);
 }
 var consent=consentFrom(cp);
 evidence=evidence.concat([row("CONTINUITY_CHECKPOINT","consent",consent.state+" · "+consent.predicate+(consent.scope.length?" · scope "+consent.scope.join(","):"")),row("BINDING_DECISION","invocation route","NOT_AVAILABLE"),row("BINDING_DECISION","generic LLM fallback","FORBIDDEN")]);
 out=base("ALLOW","MYKV_ASSISTANT_CONTINUITY_PRESENTED");
 out.identity={assistant_principal_id:b.assistant_principal_id,assistant_display_name:str(b.assistant_display_name),ai_label_required:true,owner_principal_id:b.owner_principal_id,same_assistant_as_checkpoint:continuity.state==="CONTINUOUS_SAME_ASSISTANT"?true:null};
 out.continuity=continuity;out.evidence=evidence;out.consent=consent;
 return out;
}
root.StegVerseWorkspaceAssistantContinuity=Object.freeze({schema:SCHEMA,checkpoint_schema:CHECKPOINT_SCHEMA,build:build,authority_effect:"NONE"});
}(typeof globalThis!=="undefined"?globalThis:this));
