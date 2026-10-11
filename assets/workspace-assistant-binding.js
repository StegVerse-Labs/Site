// WorkSpace -> MyKV AI Assistant identity binding, consumer side (Site#1509 W4).
// Browser port of continuity-vault-kit runtime/workspace_assistant_binding.py: the same predicates, in the same
// order, producing stegverse.kv.workspace-assistant-binding/v1. The WorkSpace assistant IS the user's existing MyKV
// assistant: the single AI_ENTITY with role WORKSPACE_ASSISTANT carried by the authenticated Personal KV projection.
// This module never creates, renames or substitutes an assistant and never falls back to a generic LLM. ALLOW means
// only that this session may show that assistant: action_eligible is always false and no invocation route exists.
// The session principal must come from the caller's own authentication; projection fields never establish who the
// user is, and browser storage is never an identity source.
(function(root){
"use strict";
if(!root)return;
var BINDING_SCHEMA="stegverse.kv.workspace-assistant-binding/v1";
var PROJECTION_SCHEMA="stegverse.kv.personal-workspace-projection/v1";
var METADATA_SCHEMA="stegverse.kv.workspace-projection-metadata/v1";
var CHECKPOINT_SCHEMA="stegverse.kv.workspace-continuity-checkpoint/v1";
var ASSISTANT_ROLE="WORKSPACE_ASSISTANT";
// Plain-language reason per predicate, identical to continuity-vault-kit runtime/workspace_decision_reasons.py
// BINDING_REASONS (the relationship reasons apply where the producer resolves a relationship declaration).
// Explanatory only: a reason never changes a disposition or predicate.
var REASONS={
 "SESSION_PRINCIPAL_UNAUTHENTICATED":"there is no signed-in identity, so there is nobody whose assistant could be shown",
 "ORG_KV_ASSISTANT_CONTEXT_NOT_OBSERVED":"an organization workspace needs that organization's own KnowledgeVault projection, which has not been observed, and your personal one is never reused for it",
 "PROJECTION_SCHEMA_INVALID":"the KnowledgeVault projection is missing or is not in the personal workspace format",
 "PROJECTION_AUTHORITY_INVALID":"the projection claims to be something other than a read-only personal workspace view",
 "PROJECTION_METADATA_INVALID":"the projection lacks the details that say whose it is and when it was observed",
 "WORKSPACE_GRANT_REVOKED":"access to this workspace has been revoked",
 "PROJECTION_OWNER_UNBOUND":"the projection does not say who owns it",
 "PROJECTION_OWNER_MISMATCH":"the projection belongs to someone other than the signed-in person",
 "PROJECTION_WORKSPACE_MISMATCH":"the projection is for a different workspace than the one you opened",
 "MYKV_ASSISTANT_BINDING_ABSENT":"your KnowledgeVault has no MyKV assistant recorded, and a generic assistant is never put in its place",
 "MYKV_ASSISTANT_RECORD_INVALID":"the assistant recorded in your KnowledgeVault is incomplete or is not marked as your workspace assistant",
 "MYKV_ASSISTANT_IS_SESSION_PRINCIPAL":"the assistant record names you yourself, and a person cannot be their own assistant",
 "PROJECTION_PRINCIPALS_INVALID":"the list of people and entities in the projection is malformed",
 "MYKV_ASSISTANT_AMBIGUOUS":"more than one assistant is recorded for you, and one is never chosen silently",
 "RELATIONSHIP_DECLARATION_INVALID":"the declared relationship between you and your assistant is malformed",
 "RELATIONSHIP_PARTIES_MISMATCH":"the declared relationship names a different person or assistant",
 "RELATIONSHIP_NOT_ACTIVE":"the declared relationship between you and your assistant is not active",
 "MYKV_ASSISTANT_BOUND":"this session resolved to your one MyKV assistant; that lets the page show it, not invoke it or act for you"
};
function explanationRecord(disposition,predicate){
 // Input for the explanation contract (stegverse.user-facing-explanation/v1, .github#3106): never verified here.
 var r={disposition:disposition,predicate:predicate,requested_action:"Show your MyKV assistant in this WorkSpace",authority_source:"NONE",consequence_observation:"NOT_AUTHENTICALLY_OBSERVED"};
 if(Object.prototype.hasOwnProperty.call(REASONS,predicate))r.why=REASONS[predicate];
 return r;
}
function isObject(v){return !!v&&typeof v==="object"&&!Array.isArray(v);}
function nonEmpty(v){return typeof v==="string"&&v.length>0;}
function decision(disposition,predicate,binding){
 return {schema:BINDING_SCHEMA,disposition:disposition,predicate:predicate,binding:binding||null,generic_llm_fallback:"FORBIDDEN",action_eligible:false,authority_effect:"NONE",explanation_record:explanationRecord(disposition,predicate)};
}
function isAssistant(row){return isObject(row)&&row.principal_type==="AI_ENTITY"&&Array.isArray(row.roles)&&row.roles.indexOf(ASSISTANT_ROLE)>=0;}
function resolve(projection,session){
 var s=isObject(session)?session:{};
 if(!nonEmpty(s.principal_id))return decision("FAIL_CLOSED","SESSION_PRINCIPAL_UNAUTHENTICATED");
 // Org context changes data and action scope, never assistant identity; it needs a distinct Org-KV projection.
 if(s.workspace_type!=="PERSONAL")return decision("FAIL_CLOSED","ORG_KV_ASSISTANT_CONTEXT_NOT_OBSERVED");
 if(!isObject(projection)||projection.schema!==PROJECTION_SCHEMA)return decision("FAIL_CLOSED","PROJECTION_SCHEMA_INVALID");
 if(projection.workspace_type!=="PERSONAL"||projection.authority_effect!=="NONE"||projection.workspace_grants_authority!==false)return decision("FAIL_CLOSED","PROJECTION_AUTHORITY_INVALID");
 var meta=projection.projection_metadata;
 if(!isObject(meta)||meta.schema!==METADATA_SCHEMA)return decision("FAIL_CLOSED","PROJECTION_METADATA_INVALID");
 if(meta.grant_state==="REVOKED")return decision("DENY","WORKSPACE_GRANT_REVOKED");
 var owner=meta.owner_principal_id;
 if(!nonEmpty(owner))return decision("FAIL_CLOSED","PROJECTION_OWNER_UNBOUND");
 if(owner!==s.principal_id)return decision("DENY","PROJECTION_OWNER_MISMATCH");
 var workspaceId=s.workspace_id===undefined?null:s.workspace_id;
 if((meta.workspace_id===undefined?null:meta.workspace_id)!==workspaceId)return decision("DENY","PROJECTION_WORKSPACE_MISMATCH");
 var assistant=projection.assistant;
 if(assistant===null||assistant===undefined)return decision("FAIL_CLOSED","MYKV_ASSISTANT_BINDING_ABSENT");
 if(!isAssistant(assistant)||!nonEmpty(assistant.principal_id))return decision("FAIL_CLOSED","MYKV_ASSISTANT_RECORD_INVALID");
 var assistantId=assistant.principal_id;
 if(assistantId===s.principal_id)return decision("FAIL_CLOSED","MYKV_ASSISTANT_IS_SESSION_PRINCIPAL");
 var principals=projection.principals===undefined||projection.principals===null?[]:projection.principals;
 if(!Array.isArray(principals))return decision("FAIL_CLOSED","PROJECTION_PRINCIPALS_INVALID");
 // One user, one assistant identity: a second candidate is never silently chosen.
 for(var i=0;i<principals.length;i++){if(isAssistant(principals[i])&&principals[i].principal_id!==assistantId)return decision("FAIL_CLOSED","MYKV_ASSISTANT_AMBIGUOUS");}
 return decision("ALLOW","MYKV_ASSISTANT_BOUND",{
  assistant_principal_id:assistantId,
  assistant_display_name:typeof assistant.display_name==="string"?assistant.display_name:null,
  ai_label_required:true,
  owner_principal_id:owner,
  workspace_type:"PERSONAL",
  workspace_id:workspaceId,
  // Continuity is keyed by (owner, assistant, workspace), never by device or page session.
  continuity:{key:{owner_principal_id:owner,assistant_principal_id:assistantId,workspace_id:workspaceId},
   source_revision:typeof meta.source_revision==="string"?meta.source_revision:null,
   provenance_ref:typeof meta.provenance_ref==="string"?meta.provenance_ref:null,
   observed_at:typeof meta.observed_at==="string"?meta.observed_at:null,
   checkpoint_schema:CHECKPOINT_SCHEMA,replay_status:"UNKNOWN"},
  grant_state:typeof meta.grant_state==="string"?meta.grant_state:"UNKNOWN",
  // A mutual relationship declaration is not delivered to the browser; it is never assumed.
  relationship_state:"NOT_SUPPLIED",relationship_id:null,
  invocation_route:"NOT_AVAILABLE",ephemeral_inference:"NOT_AVAILABLE"
 });
}
root.StegVerseWorkspaceAssistantBinding=Object.freeze({reasons:Object.freeze(Object.assign({},REASONS)),schema:BINDING_SCHEMA,resolve:resolve,authority_effect:"NONE"});
}(typeof globalThis!=="undefined"?globalThis:this));
