// WorkSpace node-binding contract (Site#1509 WU2): stegverse.workspace.node-binding/v1.
// Decides which StegOS node the Personal KV query may be bound to on this device. A directly observed device-local
// registration binds as before. On a device that has never held one, the page never registers a new identity:
// the only other admissible input is a stegos.device_continuity_recovery_result.v1 produced by the existing
// browser-independent recovery owner (StegVerse-Labs/StegOS#347, stegos/device_continuity_recovery.py) through the
// governed path, validated here fail-closed (admitted, nothing minted, TV/TVC + Interlock/InTr, retained node with
// an exact Receipt #1). Absent that result the decision is FAIL_CLOSED with the work unit and owner named.
// No decision grants authority; node identity is a transport binding, never a user principal.
(function(root){
"use strict";
if(!root)return;
var SCHEMA="stegverse.workspace.node-binding/v1";
var RESULT_SCHEMA="stegos.device_continuity_recovery_result.v1";
var GENESIS_SCHEMA="stegos.node_handoff_receipt.v1";
var WORK_UNIT="WU2-REGISTRATION-RECOVERY-ON-A-NEW-DEVICE";
var RECOVERY_OWNER="StegVerse-Labs/StegOS#347 stegos/device_continuity_recovery.py";
// Plain-language reason per node-binding predicate, for the explanation contract
// (stegverse.user-facing-explanation/v1, .github#3106). Explanatory only: never changes a state or predicate.
var REASONS={
 "REGISTERED_NODE_DIRECTLY_OBSERVED":"this browser holds a registration for an existing device node",
 "DEVICE_CONTINUITY_RECOVERY_RESULT_NOT_OBSERVED":"this browser has no device registration, and no recovery result for your existing device has arrived",
 "RECOVERY_RESULT_SCHEMA_INVALID":"the device recovery result is not in the expected format",
 "RECOVERY_NOT_ADMITTED":"the device recovery was not admitted for use on this device",
 "RECOVERY_MINTED_IDENTITY":"the recovery would create a new device or continuity identity, which is never allowed",
 "RECOVERY_AUTHORITY_INVALID":"the recovery result names the wrong authorities or claims more than restoring this device",
 "RECOVERY_RETAINED_NODE_ABSENT":"the recovery result does not include your retained device node",
 "RECOVERY_CONTINUITY_MISMATCH":"the recovered node does not match your device continuity record",
 "RECOVERY_GENESIS_RECEIPT_INVALID":"the original registration receipt for your device is invalid",
 "RECOVERY_NODE_BINDING_MISMATCH":"the recovered node does not match its original registration",
 "RECOVERY_GENESIS_DIGEST_MISMATCH":"the original registration receipt does not match its recorded fingerprint",
 "RETAINED_NODE_REHYDRATION_ADMITTED":"your existing device node was recovered without creating a new identity"
};
function isObject(v){return !!v&&typeof v==="object"&&!Array.isArray(v);}
function nonEmpty(v){return typeof v==="string"&&v.length>0;}
function isSha256(v){return typeof v==="string"&&/^[0-9a-f]{64}$/.test(v);}
function canonical(v){if(v===null||typeof v!=="object")return JSON.stringify(v);if(Array.isArray(v))return "["+v.map(canonical).join(",")+"]";return "{"+Object.keys(v).sort().map(function(k){return JSON.stringify(k)+":"+canonical(v[k]);}).join(",")+"}";}
function sha256(v){var c=root.crypto||(typeof globalThis!=="undefined"?globalThis.crypto:null);return c.subtle.digest("SHA-256",new TextEncoder().encode(canonical(v))).then(function(d){return Array.from(new Uint8Array(d),function(b){return b.toString(16).padStart(2,"0");}).join("");});}
function decision(disposition,predicate,extra){
 return Object.assign({schema:SCHEMA,disposition:disposition,predicate:predicate,node_id:null,source:null,identity_minted_by_page:false,
  work_unit:WORK_UNIT,recovery_contract:{schema:RESULT_SCHEMA,owner:RECOVERY_OWNER},node_identity_is_user_principal:false,authority_effect:"NONE"},extra||{});
}
function genesisPredicatesHold(r){
 return isObject(r)&&r.schema===GENESIS_SCHEMA&&r.receipt_number===1&&r.transition==="NODE_REGISTERED"&&r.prior_state==="UNREGISTERED"&&r.resulting_state==="REGISTERED"&&r.continuity_parent==="GENESIS"&&r.authority_effect==="NONE"&&r.credential_authority==="TV/TVC"&&nonEmpty(r.node_id)&&nonEmpty(r.interlock_id)&&isSha256(r.device_binding_sha256)&&isSha256(r.receipt_sha256);
}
function resolve(status,recovery){
 var s=isObject(status)?status:{};
 if(s.registered===true&&isObject(s.registration)&&nonEmpty(s.registration.node_id)){
  return Promise.resolve(decision("ALLOW","REGISTERED_NODE_DIRECTLY_OBSERVED",{node_id:s.registration.node_id,source:"DEVICE_LOCAL_REGISTRATION"}));
 }
 if(recovery===null||recovery===undefined)return Promise.resolve(decision("FAIL_CLOSED","DEVICE_CONTINUITY_RECOVERY_RESULT_NOT_OBSERVED"));
 if(!isObject(recovery)||recovery.schema!==RESULT_SCHEMA)return Promise.resolve(decision("FAIL_CLOSED","RECOVERY_RESULT_SCHEMA_INVALID"));
 if(recovery.recovery_state!=="ADMITTED_FOR_LOCAL_REHYDRATION")return Promise.resolve(decision("FAIL_CLOSED","RECOVERY_NOT_ADMITTED"));
 if(recovery.new_node_minted!==false||recovery.new_continuity_root_minted!==false||recovery.browser_context_is_identity!==false)return Promise.resolve(decision("FAIL_CLOSED","RECOVERY_MINTED_IDENTITY"));
 if(recovery.credential_authority!=="TV/TVC"||recovery.transition_authority!=="Interlock/InTr"||recovery.github_token_runtime_authority!=="NONE"||recovery.authority_effect!=="LOCAL_REHYDRATION_ONLY")return Promise.resolve(decision("FAIL_CLOSED","RECOVERY_AUTHORITY_INVALID"));
 var node=recovery.retained_node;
 if(!isObject(node))return Promise.resolve(decision("FAIL_CLOSED","RECOVERY_RETAINED_NODE_ABSENT"));
 var cid=recovery.device_continuity_id;
 if(!nonEmpty(cid)||cid.indexOf("stegdevice-")!==0||node.device_continuity_id!==cid||!isSha256(recovery.capsule_sha256))return Promise.resolve(decision("FAIL_CLOSED","RECOVERY_CONTINUITY_MISMATCH"));
 var g=node.genesis_receipt;
 if(!genesisPredicatesHold(g))return Promise.resolve(decision("FAIL_CLOSED","RECOVERY_GENESIS_RECEIPT_INVALID"));
 if(node.node_id!==g.node_id||node.interlock_id!==g.interlock_id||node.device_binding_sha256!==g.device_binding_sha256||!isSha256(node.node_binding_receipt_sha256))return Promise.resolve(decision("FAIL_CLOSED","RECOVERY_NODE_BINDING_MISMATCH"));
 var body=Object.assign({},g);delete body.receipt_sha256;
 return sha256(body).then(function(actual){
  if(actual!==g.receipt_sha256)return decision("FAIL_CLOSED","RECOVERY_GENESIS_DIGEST_MISMATCH");
  return decision("ALLOW","RETAINED_NODE_REHYDRATION_ADMITTED",{node_id:node.node_id,source:"ADMITTED_DEVICE_CONTINUITY_RECOVERY",
   lineage:{device_continuity_id:cid,capsule_sha256:recovery.capsule_sha256,node_binding_receipt_sha256:node.node_binding_receipt_sha256,genesis_receipt_sha256:g.receipt_sha256}});
 });
}
root.StegVerseWorkspaceNodeBinding=Object.freeze({reasons:Object.freeze(Object.assign({},REASONS)),schema:SCHEMA,resolve:resolve,work_unit:WORK_UNIT,recovery_result_schema:RESULT_SCHEMA,authority_effect:"NONE"});
}(typeof globalThis!=="undefined"?globalThis:this));
