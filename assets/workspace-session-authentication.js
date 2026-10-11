// WorkSpace session-authentication contract (Site#1509 W4): stegverse.workspace.session-authentication/v1.
// Decides whether this page holds an authenticated session principal that may be handed to the MyKV assistant
// binding resolver. It takes the page session only, never the KV projection: KV ownership data
// (projection_metadata.owner_principal_id, workspace.owner_principal_id, principals[]) describes whose data was
// projected and is never who the caller is. Device registration proves a node, browser storage proves nothing,
// and a bare principal_id without a caller-authentication receipt is refused. ALLOW here means only that the
// principal was admitted from a declared caller-authentication receipt; the page does not verify the receipt
// (verification: CALLER_SUPPLIED_NOT_PAGE_VERIFIED) and the decision grants no action or execution authority.
(function(root){
"use strict";
if(!root)return;
var SCHEMA="stegverse.workspace.session-authentication/v1";
var RECEIPT_SOURCE_CLASS="CALLER_AUTHENTICATION_RECEIPT";
var CREDENTIAL_AUTHORITY="TV/TVC";
// Source classes that are never authentication, each with the predicate that names why.
var NON_AUTHENTICATION_SOURCES={
 NO_AUTHENTICATED_SESSION_PRINCIPAL:"SESSION_PRINCIPAL_UNAUTHENTICATED",
 KV_PROJECTION_OWNER:"KV_OWNERSHIP_IS_NOT_AUTHENTICATION",
 KV_PROJECTION_METADATA:"KV_OWNERSHIP_IS_NOT_AUTHENTICATION",
 KV_PROJECTION_PRINCIPAL:"KV_OWNERSHIP_IS_NOT_AUTHENTICATION",
 KV_WORKSPACE_CONTEXT:"KV_OWNERSHIP_IS_NOT_AUTHENTICATION",
 DEVICE_REGISTRATION:"DEVICE_REGISTRATION_IS_NOT_AUTHENTICATION",
 STEGOS_NODE_REGISTRATION:"DEVICE_REGISTRATION_IS_NOT_AUTHENTICATION",
 BROWSER_STORAGE:"BROWSER_STATE_IS_NOT_AUTHENTICATION",
 PAGE_STATE:"BROWSER_STATE_IS_NOT_AUTHENTICATION",
 URL_PARAMETER:"BROWSER_STATE_IS_NOT_AUTHENTICATION",
 BOOTSTRAP_DATA:"BROWSER_STATE_IS_NOT_AUTHENTICATION"
};
// Plain-language reason per predicate, identical to continuity-vault-kit runtime/workspace_decision_reasons.py
// SESSION_REASONS. Explanatory only: a reason never changes a disposition or predicate.
var REASONS={
 "SESSION_PRINCIPAL_UNAUTHENTICATED":"this page has no signed-in identity for you, so it cannot tell who is asking",
 "KV_OWNERSHIP_IS_NOT_AUTHENTICATION":"holding or owning a KnowledgeVault projection does not prove who is signed in; only a sign-in receipt does",
 "DEVICE_REGISTRATION_IS_NOT_AUTHENTICATION":"a registered device or node shows which machine is connected, not which person is signed in",
 "BROWSER_STATE_IS_NOT_AUTHENTICATION":"values kept in the browser, the page address or startup data can be changed by anyone, so they never prove who is signed in",
 "SESSION_PRINCIPAL_SOURCE_NOT_AUTHENTICATION":"the identity offered to this page did not come from a sign-in receipt, which is the only accepted source",
 "SESSION_AUTHENTICATION_RECEIPT_ABSENT":"the sign-in did not include its authentication receipt",
 "SESSION_NOT_AUTHENTICATED":"the sign-in receipt says the sign-in did not succeed",
 "SESSION_CREDENTIAL_AUTHORITY_INVALID":"the sign-in receipt was not issued by TV/TVC, the only credential authority this ecosystem accepts",
 "SESSION_AUTHENTICATION_RECEIPT_REF_ABSENT":"the sign-in receipt has no locator, so nobody can check it later",
 "SESSION_AUTHENTICATION_PRINCIPAL_MISMATCH":"the sign-in receipt belongs to a different identity than the one making this request",
 "SESSION_AUTHENTICATION_CLAIMS_AUTHORITY":"the sign-in receipt claims the power to authorize, execute or delegate actions, and a sign-in can never grant that",
 "CALLER_AUTHENTICATION_RECEIPT_PRESENT":"a sign-in receipt from TV/TVC naming you was supplied; it is accepted as reported, and this check does not verify it itself"
};
function explanationRecord(disposition,predicate){
 // Input for the explanation contract (stegverse.user-facing-explanation/v1, .github#3106): never verified here.
 var r={disposition:disposition,predicate:predicate,requested_action:"Sign in to this WorkSpace",authority_source:"NONE",consequence_observation:"NOT_AUTHENTICALLY_OBSERVED"};
 if(Object.prototype.hasOwnProperty.call(REASONS,predicate))r.why=REASONS[predicate];
 return r;
}
function isObject(v){return !!v&&typeof v==="object"&&!Array.isArray(v);}
function nonEmpty(v){return typeof v==="string"&&v.length>0;}
function decision(disposition,predicate,session){
 // ALLOW is an informational acceptance of caller-supplied receipt fields. The page performs no TV/TVC
 // verification, so no decision here is runtime authentication evidence and none may raise action eligibility.
 return {schema:SCHEMA,disposition:disposition,predicate:predicate,session:session||null,
  admission_class:"CALLER_SUPPLIED_FIELDS_ACCEPTED",verification:"CALLER_SUPPLIED_NOT_PAGE_VERIFIED",
  runtime_authentication_evidence:false,identity_from_projection:false,action_eligible:false,authority_effect:"NONE",
  explanation_record:explanationRecord(disposition,predicate)};
}
function resolve(session){
 var s=isObject(session)?session:{};
 var sourceClass=typeof s.source_class==="string"?s.source_class:null;
 if(!nonEmpty(s.principal_id)&&(sourceClass===null||sourceClass==="NO_AUTHENTICATED_SESSION_PRINCIPAL"))return decision("FAIL_CLOSED","SESSION_PRINCIPAL_UNAUTHENTICATED");
 if(sourceClass!==null&&Object.prototype.hasOwnProperty.call(NON_AUTHENTICATION_SOURCES,sourceClass))return decision("FAIL_CLOSED",NON_AUTHENTICATION_SOURCES[sourceClass]);
 if(sourceClass!==RECEIPT_SOURCE_CLASS)return decision("FAIL_CLOSED","SESSION_PRINCIPAL_SOURCE_NOT_AUTHENTICATION");
 if(!nonEmpty(s.principal_id))return decision("FAIL_CLOSED","SESSION_PRINCIPAL_UNAUTHENTICATED");
 var a=s.authentication;
 if(!isObject(a))return decision("FAIL_CLOSED","SESSION_AUTHENTICATION_RECEIPT_ABSENT");
 if(a.authenticated!==true)return decision("FAIL_CLOSED","SESSION_NOT_AUTHENTICATED");
 if(a.credential_authority!==CREDENTIAL_AUTHORITY)return decision("FAIL_CLOSED","SESSION_CREDENTIAL_AUTHORITY_INVALID");
 if(!nonEmpty(a.receipt_ref))return decision("FAIL_CLOSED","SESSION_AUTHENTICATION_RECEIPT_REF_ABSENT");
 if(a.principal_id!==s.principal_id)return decision("FAIL_CLOSED","SESSION_AUTHENTICATION_PRINCIPAL_MISMATCH");
 if(a.transaction_authority===true||a.execution_authority===true||a.delegation_authority===true||(a.authority_effect!==undefined&&a.authority_effect!=="NONE"))return decision("FAIL_CLOSED","SESSION_AUTHENTICATION_CLAIMS_AUTHORITY");
 return decision("ALLOW","CALLER_AUTHENTICATION_RECEIPT_PRESENT",{
  principal_id:s.principal_id,
  workspace_id:s.workspace_id===undefined?null:s.workspace_id,
  source_class:RECEIPT_SOURCE_CLASS,
  receipt_ref:a.receipt_ref,
  credential_authority:CREDENTIAL_AUTHORITY
 });
}
root.StegVerseWorkspaceSessionAuthentication=Object.freeze({reasons:Object.freeze(Object.assign({},REASONS)),schema:SCHEMA,resolve:resolve,receipt_source_class:RECEIPT_SOURCE_CLASS,authority_effect:"NONE"});
}(typeof globalThis!=="undefined"?globalThis:this));
