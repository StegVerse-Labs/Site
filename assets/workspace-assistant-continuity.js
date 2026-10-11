// WorkSpace MyKV assistant continuity / evidence / consent presentation (Site#1509 WS-ASSISTANT).
// Derives stegverse.workspace.assistant-continuity/v1 from inputs the page already holds: the session authentication
// decision (stegverse.workspace.session-authentication/v1), the assistant binding decision
// (stegverse.kv.workspace-assistant-binding/v1, the browser port of the CVK resolver), the assistant identity this
// page last presented (in memory only), and, when the authenticated KV path delivers them, a continuity checkpoint
// (stegverse.kv.workspace-continuity-checkpoint/v1, exactly the field set continuity-vault-kit
// runtime/workspace_continuity_checkpoint.py validates) with the producer's transition decision
// (stegverse.kv.workspace-continuity-checkpoint-decision/v1). The assistant is only ever the user's existing MyKV
// assistant: a change of presented identity fails closed instead of being adopted. This page verifies no digest or
// anchor (replay status is the producer decision's or UNKNOWN), invokes nothing, has no generic LLM, and records no
// consent: no consent contract is published, so consent is NOT_SUPPLIED and can only be requested as a draft.
(function(root){
"use strict";
if(!root)return;
var SCHEMA="stegverse.workspace.assistant-continuity/v1";
var CHECKPOINT_SCHEMA="stegverse.kv.workspace-continuity-checkpoint/v1";
var DECISION_SCHEMA="stegverse.kv.workspace-continuity-checkpoint-decision/v1";
var BINDING_SCHEMA="stegverse.kv.workspace-assistant-binding/v1";
var CHECKPOINT_FIELDS=["schema","principal_id","workspace_type","workspace_id","grant_epoch","source_epoch","sequence","source_revision","previous_checkpoint_digest","observed_at","anchor","checkpoint_digest","authority_effect"];
var WORKSPACE_TYPES=["PERSONAL","ORGANIZATIONAL"],ANCHOR_KINDS=["RECEIPT_REF","SIGNATURE"],DISPOSITIONS=["ALLOW","DENY","FAIL_CLOSED"],REPLAY=["VERIFIED","UNKNOWN","REFUSED"];
var HEX64=/^[0-9a-f]{64}$/;
function isObject(v){return !!v&&typeof v==="object"&&!Array.isArray(v);}
function nonEmpty(v){return typeof v==="string"&&v.length>0;}
function str(v){return typeof v==="string"?v:null;}
function nonNegInt(v){return typeof v==="number"&&isFinite(v)&&Math.floor(v)===v&&v>=0;}
function row(source,label,value){return {source:source,label:label,value:value===undefined||value===null?"NOT_SUPPLIED":String(value)};}
function consentWithheld(){return {state:"WITHHELD",predicate:"ASSISTANT_NOT_PRESENTED",contract:null,consent_ref:null,scope:[],recorded_by_page:false,proposable_actions:[]};}
function base(disposition,predicate){
 return {schema:SCHEMA,disposition:disposition,predicate:predicate,identity:null,
  continuity:{state:"WITHHELD",predicate:predicate,key:null,checkpoint:null,source_revision:null,provenance_ref:null,replay_status:"REPLAY_STATUS_UNKNOWN",digest_verified_by_page:false,anchor_verified_by_page:false},
  evidence:[],consent:consentWithheld(),
  generic_llm_fallback:"FORBIDDEN",invocation_route:"NOT_AVAILABLE",ephemeral_inference:"NOT_AVAILABLE",action_eligible:false,authority_effect:"NONE"};
}
function sessionRows(sa){
 var s=isObject(sa)?sa:{};
 return [row("SESSION_AUTHENTICATION","session disposition",(s.disposition||"FAIL_CLOSED")+" · "+(s.predicate||"SESSION_AUTHENTICATION_RESOLVER_UNAVAILABLE")),
  row("SESSION_AUTHENTICATION","admission class",s.admission_class||"CALLER_SUPPLIED_FIELDS_ACCEPTED"),
  row("SESSION_AUTHENTICATION","verification",s.verification||"CALLER_SUPPLIED_NOT_PAGE_VERIFIED"),
  row("SESSION_AUTHENTICATION","runtime authentication evidence","false")];
}
// Structural mirror of continuity-vault-kit validate_checkpoint (same reasons, same order); the digest itself is not recomputed here.
function checkpointProblem(cp){
 if(!isObject(cp))return "checkpoint_object_required";
 var keys=Object.keys(cp).filter(function(k){return CHECKPOINT_FIELDS.indexOf(k)<0;}).sort();
 if(keys.length)return "checkpoint_field_forbidden:"+keys[0];
 if(cp.schema!==CHECKPOINT_SCHEMA)return "checkpoint_schema_invalid";
 if(cp.authority_effect!=="NONE")return "checkpoint_authority_invalid";
 if(!nonEmpty(cp.principal_id))return "checkpoint_principal_required";
 if(WORKSPACE_TYPES.indexOf(cp.workspace_type)<0)return "checkpoint_workspace_type_invalid";
 if(cp.workspace_id!==null&&!nonEmpty(cp.workspace_id))return "checkpoint_workspace_id_invalid";
 var ints=["grant_epoch","source_epoch","sequence"];
 for(var i=0;i<ints.length;i++){if(!nonNegInt(cp[ints[i]]))return "checkpoint_"+ints[i]+"_invalid";}
 if(!(typeof cp.source_revision==="string"&&HEX64.test(cp.source_revision)))return "checkpoint_source_revision_invalid";
 if(cp.previous_checkpoint_digest!==null&&!(typeof cp.previous_checkpoint_digest==="string"&&HEX64.test(cp.previous_checkpoint_digest)))return "checkpoint_previous_digest_invalid";
 if(!nonEmpty(cp.observed_at))return "checkpoint_observed_at_required";
 var a=cp.anchor;
 if(!isObject(a)||ANCHOR_KINDS.indexOf(a.kind)<0||!nonEmpty(a.ref))return "checkpoint_anchor_invalid";
 if(!(typeof cp.checkpoint_digest==="string"&&HEX64.test(cp.checkpoint_digest)))return "checkpoint_digest_invalid";
 return null;
}
function decisionProblem(d){
 if(!isObject(d)||d.schema!==DECISION_SCHEMA)return "CHECKPOINT_DECISION_SCHEMA_INVALID";
 if(d.authority_effect!=="NONE")return "CHECKPOINT_DECISION_AUTHORITY_INVALID";
 if(DISPOSITIONS.indexOf(d.disposition)<0||!nonEmpty(d.predicate)||REPLAY.indexOf(d.replay_status)<0)return "CHECKPOINT_DECISION_INVALID";
 if(d.disposition==="ALLOW"&&d.replay_status!=="VERIFIED")return "CHECKPOINT_DECISION_ALLOW_UNVERIFIED";
 return null;
}
function build(input){
 var inp=isObject(input)?input:{},sa=inp.session_authentication,d=inp.decision,cp=inp.checkpoint,cd=inp.checkpoint_decision,prev=inp.previous_identity;
 var out;
 if(!isObject(sa)||sa.disposition!=="ALLOW"){out=base("FAIL_CLOSED",isObject(sa)&&nonEmpty(sa.predicate)?sa.predicate:"SESSION_PRINCIPAL_UNAUTHENTICATED");out.evidence=sessionRows(sa);out.continuity.state="NOT_EVALUATED";return out;}
 if(!isObject(d)||d.schema!==BINDING_SCHEMA){out=base("FAIL_CLOSED","ASSISTANT_BINDING_DECISION_UNAVAILABLE");out.evidence=sessionRows(sa);return out;}
 if(d.disposition!=="ALLOW"||!isObject(d.binding)){out=base(d.disposition==="DENY"?"DENY":"FAIL_CLOSED",nonEmpty(d.predicate)?d.predicate:"ASSISTANT_BINDING_REFUSED");out.evidence=sessionRows(sa).concat([row("BINDING_DECISION","binding",d.disposition+" · "+d.predicate)]);if(d.predicate==="WORKSPACE_GRANT_REVOKED")out.continuity.state="REVOKED";return out;}
 var b=d.binding,c=isObject(b.continuity)?b.continuity:{},key=isObject(c.key)?c.key:null;
 if(!key||!nonEmpty(key.owner_principal_id)||!nonEmpty(key.assistant_principal_id)||!nonEmpty(b.assistant_principal_id)||key.assistant_principal_id!==b.assistant_principal_id){out=base("FAIL_CLOSED","BINDING_CONTINUITY_KEY_INVALID");out.evidence=sessionRows(sa);return out;}
 var workspaceId=key.workspace_id===undefined?null:key.workspace_id;
 var evidence=sessionRows(sa).concat([
  row("BINDING_DECISION","binding","ALLOW · "+d.predicate),
  row("BINDING_DECISION","assistant",b.assistant_principal_id+(b.assistant_display_name?" ("+b.assistant_display_name+")":"")),
  row("BINDING_DECISION","owner",b.owner_principal_id),
  row("BINDING_DECISION","relationship",b.relationship_state||"NOT_SUPPLIED"),
  row("KV_PROJECTION_METADATA","source revision",c.source_revision),
  row("KV_PROJECTION_METADATA","provenance",c.provenance_ref),
  row("KV_PROJECTION_METADATA","observed at",c.observed_at),
  row("KV_PROJECTION_METADATA","grant state",b.grant_state||"UNKNOWN")]);
 // Same assistant identity: the identity this page already presented in this session may not change under the user.
 if(isObject(prev)&&nonEmpty(prev.assistant_principal_id)&&prev.assistant_principal_id!==b.assistant_principal_id){out=base("FAIL_CLOSED","ASSISTANT_IDENTITY_CHANGED");out.evidence=evidence.concat([row("PAGE_SESSION","previously presented assistant",prev.assistant_principal_id)]);out.continuity.state="IDENTITY_CHANGED";return out;}
 var continuity={state:"CONTINUITY_UNKNOWN",predicate:"CHECKPOINT_NOT_OBSERVED",key:{owner_principal_id:key.owner_principal_id,assistant_principal_id:key.assistant_principal_id,workspace_id:workspaceId},checkpoint:null,source_revision:str(c.source_revision),provenance_ref:str(c.provenance_ref),replay_status:"REPLAY_STATUS_UNKNOWN",digest_verified_by_page:false,anchor_verified_by_page:false};
 var sameRevision=null;
 if(cp!==undefined&&cp!==null){
  var problem=checkpointProblem(cp);
  if(problem){out=base("FAIL_CLOSED","CHECKPOINT_MALFORMED:"+problem);out.evidence=evidence;out.continuity.state="MALFORMED";return out;}
  // Mirrors verify_transition's context check: the chain belongs to (principal, workspace_type, workspace_id).
  if(cp.principal_id!==key.owner_principal_id||cp.workspace_type!=="PERSONAL"||cp.workspace_id!==workspaceId){out=base("DENY","CHECKPOINT_CONTEXT_MISMATCH");out.evidence=evidence.concat([row("CONTINUITY_CHECKPOINT","checkpoint context",cp.principal_id+" / "+cp.workspace_type+" / "+cp.workspace_id)]);out.continuity.state="REFUSED";return out;}
  continuity.checkpoint={checkpoint_digest:cp.checkpoint_digest,previous_checkpoint_digest:cp.previous_checkpoint_digest,grant_epoch:cp.grant_epoch,source_epoch:cp.source_epoch,sequence:cp.sequence,source_revision:cp.source_revision,observed_at:cp.observed_at,anchor_kind:cp.anchor.kind,anchor_ref:cp.anchor.ref};
  sameRevision=cp.source_revision===c.source_revision;
  evidence=evidence.concat([row("CONTINUITY_CHECKPOINT","checkpoint digest",cp.checkpoint_digest),row("CONTINUITY_CHECKPOINT","chain position","grant_epoch "+cp.grant_epoch+" · source_epoch "+cp.source_epoch+" · sequence "+cp.sequence),row("CONTINUITY_CHECKPOINT","checkpoint source revision",cp.source_revision+(sameRevision?" (same as projection)":" (differs from projection)")),row("CONTINUITY_CHECKPOINT","checkpoint observed at",cp.observed_at),row("CONTINUITY_CHECKPOINT","anchor",cp.anchor.kind+" "+cp.anchor.ref+" (not verified by this page)")]);
  if(cd===undefined||cd===null){continuity.state="CHECKPOINT_OBSERVED_UNVERIFIED";continuity.predicate="CHECKPOINT_DECISION_NOT_OBSERVED";}
  else{
   var dp=decisionProblem(cd);
   if(dp){out=base("FAIL_CLOSED",dp);out.evidence=evidence;out.continuity.state="MALFORMED";return out;}
   evidence=evidence.concat([row("CONTINUITY_CHECKPOINT","producer decision",cd.disposition+" · "+cd.predicate+" · replay "+cd.replay_status+" (delivered by the KV path; not page-verified)")]);
   if(cd.predicate==="CHECKPOINT_GRANT_REVOKED"){out=base("DENY","CONTINUITY_REVOKED");out.evidence=evidence;out.continuity.state="REVOKED";return out;}
   if(cd.disposition==="DENY"){out=base("DENY",cd.predicate);out.evidence=evidence;out.continuity.state="REFUSED";return out;}
   continuity.replay_status=cd.replay_status;
   if(cd.disposition==="ALLOW"){continuity.state="CONTINUOUS_VERIFIED_BY_PRODUCER";continuity.predicate=cd.predicate;}
   else{continuity.state="CHECKPOINT_UNVERIFIED";continuity.predicate=cd.predicate;}
  }
 }
 evidence=evidence.concat([row("CONSENT","consent","NOT_SUPPLIED · CONSENT_CONTRACT_NOT_PUBLISHED"),row("BINDING_DECISION","invocation route","NOT_AVAILABLE"),row("BINDING_DECISION","generic LLM fallback","FORBIDDEN")]);
 out=base("ALLOW","MYKV_ASSISTANT_CONTINUITY_PRESENTED");
 out.identity={assistant_principal_id:b.assistant_principal_id,assistant_display_name:str(b.assistant_display_name),ai_label_required:true,owner_principal_id:b.owner_principal_id,same_assistant_as_checkpoint_revision:sameRevision};
 out.continuity=continuity;out.evidence=evidence;
 out.consent={state:"NOT_SUPPLIED",predicate:"CONSENT_CONTRACT_NOT_PUBLISHED",contract:null,consent_ref:null,scope:[],recorded_by_page:false,proposable_actions:["ASSISTANT_CONSENT_GRANT"]};
 return out;
}
root.StegVerseWorkspaceAssistantContinuity=Object.freeze({schema:SCHEMA,checkpoint_schema:CHECKPOINT_SCHEMA,checkpoint_decision_schema:DECISION_SCHEMA,checkpoint_fields:CHECKPOINT_FIELDS.slice(),build:build,authority_effect:"NONE"});
}(typeof globalThis!=="undefined"?globalThis:this));
