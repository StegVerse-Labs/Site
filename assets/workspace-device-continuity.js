// WorkSpace device-replacement continuity acceptance (Site#1509, owner acceptance case 6104569407).
// Derives stegverse.workspace.device-replacement-acceptance/v1 from decisions the page already holds: the session
// authentication decision, the node-binding decision recorded by the DEVICE_KV bridge, the outcome of the Personal KV
// ingress attempt, and the assistant continuity output. Each of the owner's five acceptance checks is presented as its
// own row with the exact predicate and the owner that can move it. The page can never certify the case: receipts and
// Master Records readback are not page-observable, so the bundle is never ALLOW from here. No row requires a local KV
// installation, a second device or a newly minted node; a newly minted node fails the case.
(function(root){
"use strict";
if(!root)return;
var SCHEMA="stegverse.workspace.device-replacement-acceptance/v1";
var INGRESS_PREDICATE="AUTHORIZED_DEVICE_INDEPENDENT_KV_INGRESS_NOT_BOUND_TO_WORKSPACE";
var UNKNOWN="UNKNOWN_NOT_AUTHENTICALLY_OBSERVED";
var OWNERS={
 kv_custody:"continuity-vault-kit runtime/personal_provider_binding.py (GOOGLE_DRIVE binding, TV/TVC broker materialization, scope _System/Workspace/**) + TVC-PERSONAL-KV-GOOGLE-DRIVE-SESSION-037A",
 principal:"TV/TVC caller-authentication receipt issuer",
 ingress:"StegOS DEVICE_KV sovereign InTr ingress (Site stegos-node/device-kv-intr-sync-target.json projector) + StegOS node continuity recovery (StegOS#347/#351)",
 assistant:"continuity-vault-kit workspace_assistant_binding / workspace_continuity_checkpoint producers",
 receipts:"Interlock/InTr transition receipts and Master Records readback (owner runtime)"
};
// Plain-language reason per device-continuity check predicate, for the explanation contract
// (stegverse.user-facing-explanation/v1, .github#3106). Explanatory only: never changes a state or predicate.
var REASONS={
 "KV_CUSTODY_MANIFEST_NOT_DELIVERED_TO_PAGE":"your Personal KnowledgeVault has not reached this page through the authenticated path, so its custody cannot be shown",
 "PERSONAL_KV_PROJECTION_ADMITTED_THROUGH_AUTHENTICATED_PATH":"your Personal KnowledgeVault reached this page through the authenticated path",
 "NODE_BINDING_NOT_EVALUATED":"this device's node binding has not been checked, and your KnowledgeVault has not arrived",
 "NEW_NODE_MINTED_FORBIDDEN":"a new device identity was created instead of recovering your existing one, and that is never accepted",
 "NODE_BINDING_REFUSED":"this device's node binding was refused",
 "PERSONAL_KV_PROJECTION_ADMITTED":"this device is bound and your KnowledgeVault arrived through the authenticated path",
 "AUTHORIZED_DEVICE_INDEPENDENT_KV_INGRESS_NOT_BOUND_TO_WORKSPACE":"no authorized route yet delivers your KnowledgeVault to this workspace independently of a particular device",
 "ASSISTANT_CONTINUITY_NOT_EVALUATED":"continuity of your MyKV assistant has not been checked",
 "ASSISTANT_CONTINUITY_REFUSED":"the continuity check for your MyKV assistant was refused",
 "TRANSITION_RECEIPTS_AND_MASTER_RECORDS_READBACK_NOT_PAGE_OBSERVABLE":"receipts for a device change are recorded and read back by the owner's runtime, which this page cannot see"
};
function isObject(v){return !!v&&typeof v==="object"&&!Array.isArray(v);}
function nonEmpty(v){return typeof v==="string"&&v.length>0;}
function check(id,title,state,predicate,owner,extra){return Object.assign({id:id,title:title,state:state,predicate:predicate,owner:owner,evidence_class:"SOURCE_DERIVED_NOT_RUNTIME_CERTIFIED",notes:[]},extra||{});}
function build(input){
 var inp=isObject(input)?input:{},sa=inp.session_authentication,nb=inp.node_binding,kv=inp.kv_ingress,ac=inp.assistant_continuity;
 var checks=[],gaps=[];
 // DR1 — KV custody and recovery manifest for the Google Drive held Personal KV.
 var kvAllow=isObject(kv)&&kv.disposition==="ALLOW";
 var dr1=check("DR1","KV custody and recovery manifest",kvAllow?"PROJECTED":"NOT_OBSERVED",kvAllow?"PERSONAL_KV_PROJECTION_ADMITTED_THROUGH_AUTHENTICATED_PATH":"KV_CUSTODY_MANIFEST_NOT_DELIVERED_TO_PAGE",OWNERS.kv_custody);
 dr1.notes.push("Google Drive is storage, not authentication or sovereign ingress; provider credentials exist only inside the TV/TVC broker; this page never reads Drive.");
 dr1.notes.push("No KV installation on this device is required: the DEVICE_KV consumer resolves the KV root from the provider binding (materialize_personal_kv_provider_root).");
 if(kvAllow&&nonEmpty(kv.provenance_ref))dr1.notes.push("projection provenance "+kv.provenance_ref);
 checks.push(dr1);
 // DR2 — authenticated principal continuity (caller-supplied receipt; never page-verified).
 var saAllow=isObject(sa)&&sa.disposition==="ALLOW";
 var dr2=check("DR2","Authenticated TV/TVC principal continuity",saAllow?"ALLOW":"FAIL_CLOSED",saAllow?(sa.predicate||"CALLER_AUTHENTICATION_RECEIPT_PRESENT"):(isObject(sa)&&nonEmpty(sa.predicate)?sa.predicate:"SESSION_PRINCIPAL_UNAUTHENTICATED"),OWNERS.principal,{verification:"CALLER_SUPPLIED_NOT_PAGE_VERIFIED",runtime_authentication_evidence:false});
 if(saAllow)dr2.notes.push("principal accepted from the caller's receipt; the page verifies nothing");
 checks.push(dr2);
 // DR3 — device-independent ingress binding without a newly minted node.
 var dr3;
 var minted=isObject(nb)&&(nb.identity_minted_by_page===true||nb.new_node_minted===true);
 if(!isObject(nb))dr3=check("DR3","Node binding and KV ingress on this device",kvAllow?"ALLOW":"FAIL_CLOSED",kvAllow?"PERSONAL_KV_PROJECTION_ADMITTED":"NODE_BINDING_NOT_EVALUATED",OWNERS.ingress);
 else if(minted)dr3=check("DR3","Node binding and KV ingress on this device","FAIL_CLOSED","NEW_NODE_MINTED_FORBIDDEN",OWNERS.ingress);
 else if(nb.disposition!=="ALLOW")dr3=check("DR3","Node binding and KV ingress on this device",nb.disposition==="DENY"?"DENY":"FAIL_CLOSED",nonEmpty(nb.predicate)?nb.predicate:"NODE_BINDING_REFUSED",OWNERS.ingress);
 else if(!kvAllow)dr3=check("DR3","Node binding and KV ingress on this device",isObject(kv)&&kv.disposition==="DENY"?"DENY":"FAIL_CLOSED",isObject(kv)&&nonEmpty(kv.predicate)?kv.predicate:INGRESS_PREDICATE,OWNERS.ingress);
 else dr3=check("DR3","Node binding and KV ingress on this device","ALLOW","PERSONAL_KV_PROJECTION_ADMITTED",OWNERS.ingress);
 if(isObject(nb)&&nb.disposition==="ALLOW"){dr3.notes.push(nb.source==="ADMITTED_DEVICE_CONTINUITY_RECOVERY"?"retained node rehydrated from an admitted recovery result (new_node_minted: false)":"registration observed in this browser container; browser context is provenance, not device identity");if(nonEmpty(nb.node_id))dr3.node_id=nb.node_id;}
 if(isObject(kv)&&!kvAllow&&nonEmpty(kv.detail))dr3.notes.push(kv.detail);
 dr3.notes.push("no local KV installation, second device or newly minted node is required or accepted by this page");
 checks.push(dr3);
 // A replacement phone cannot use the same-device cross-browser carrier; the retained-node capsule needs owner custody.
 gaps.push({id:"G1",predicate:"RETAINED_NODE_CAPSULE_CUSTODY_FOR_DEVICE_REPLACEMENT_NOT_DEFINED",finding:"StegOS#351's carrier serves the retained envelope from the same iPhone's App Group (127.0.0.1); continuity-vault-kit holds no node-continuity material; no source path delivers stegos.device_continuity_recovery_capsule.v1 to a replacement device.",owner:"StegOS node continuity (StegOS#347 owner) with TV/TVC admission; custody location decision with the CVK/KV owner"});
 gaps.push({id:"G2",predicate:"TVC_PERSONAL_KV_GOOGLE_DRIVE_SESSION_NOT_IMPLEMENTED",finding:"TVC task TVC-PERSONAL-KV-GOOGLE-DRIVE-SESSION-037A is EXACT_CLASS_ADMITTED_FOR_IMPLEMENTATION_SOURCE_NOT_IMPLEMENTED_RUNTIME_NOT_ACTIVATED; without it the Drive-held KV root cannot be materialized for the DEVICE_KV consumer.",owner:"TVC owner"});
 gaps.push({id:"G3",predicate:"SOVEREIGN_INTR_INGRESS_TARGET_NOT_PROJECTED",finding:"stegos-node/device-kv-intr-sync-target.json is AWAITING_SOVEREIGN_INTR_INGRESS (runtime_ingress_observed false); the projector requires authentic HTTPS ingress evidence.",owner:"StegOS sovereign resident runtime / Site target projector (scripts/project_device_kv_intr_sync_target.py)"});
 // DR4 — same assistant principal and KV provenance/continuity/revocation.
 var dr4;
 if(!isObject(ac))dr4=check("DR4","Same MyKV assistant principal and continuity","FAIL_CLOSED","ASSISTANT_CONTINUITY_NOT_EVALUATED",OWNERS.assistant);
 else if(ac.disposition!=="ALLOW")dr4=check("DR4","Same MyKV assistant principal and continuity",ac.disposition==="DENY"?"DENY":"FAIL_CLOSED",nonEmpty(ac.predicate)?ac.predicate:"ASSISTANT_CONTINUITY_REFUSED",OWNERS.assistant);
 else{var cs=isObject(ac.continuity)?ac.continuity:{};var verified=cs.state==="CONTINUOUS_VERIFIED_BY_PRODUCER";dr4=check("DR4","Same MyKV assistant principal and continuity",verified?"ALLOW":"FAIL_CLOSED",verified?cs.predicate:(nonEmpty(cs.predicate)?cs.predicate:"CHECKPOINT_NOT_OBSERVED"),OWNERS.assistant);if(isObject(ac.identity)&&nonEmpty(ac.identity.assistant_principal_id)){dr4.assistant_principal_id=ac.identity.assistant_principal_id;dr4.notes.push("bound assistant "+ac.identity.assistant_principal_id+"; identity change fails closed (ASSISTANT_IDENTITY_CHANGED)");}if(nonEmpty(cs.provenance_ref))dr4.notes.push("projection provenance "+cs.provenance_ref);dr4.notes.push("replay status "+(cs.replay_status||"REPLAY_STATUS_UNKNOWN"));}
 checks.push(dr4);
 // DR5 — transition receipts and Master Records readback are never observable from this page.
 var dr5=check("DR5","Transition receipts and Master Records readback",UNKNOWN,"TRANSITION_RECEIPTS_AND_MASTER_RECORDS_READBACK_NOT_PAGE_OBSERVABLE",OWNERS.receipts);
 dr5.notes.push("ALLOW/DENY/FAIL_CLOSED receipts for the device change must be recorded by the owner runtime and read back from Master Records; this page cannot produce or verify them");
 checks.push(dr5);
 var failing=checks.filter(function(c){return c.state!=="ALLOW"&&c.state!=="PROJECTED";});
 var disposition=minted?"FAIL_CLOSED":(failing.some(function(c){return c.state==="DENY";})?"DENY":"FAIL_CLOSED");
 var predicate=minted?"NEW_NODE_MINTED_FORBIDDEN":(failing.length?failing[0].predicate:"TRANSITION_RECEIPTS_AND_MASTER_RECORDS_READBACK_NOT_PAGE_OBSERVABLE");
 return {schema:SCHEMA,disposition:disposition,predicate:predicate,acceptance_case:"iPhone replacement without re-creating the Google Drive held Personal KV",
  local_kv_installation_required:false,second_device_required:false,new_node_minted_by_page:false,page_certifies_runtime:false,
  checks:checks,gaps:gaps,evidence_class:"SOURCE_DERIVED_NOT_RUNTIME_CERTIFIED",action_eligible:false,authority_effect:"NONE"};
}
root.StegVerseWorkspaceDeviceContinuity=Object.freeze({reasons:Object.freeze(Object.assign({},REASONS)),schema:SCHEMA,ingress_predicate:INGRESS_PREDICATE,build:build,authority_effect:"NONE"});
}(typeof globalThis!=="undefined"?globalThis:this));
