// WorkSpace universal governance integration conformance (Site#1509 DEV-P6, owner-approved scope 6112777652).
// Presentation and synthetic-conformance companion to the framework-neutral contract in
// assets/workspace-governance-integration.js (StegVerseGovernanceIntegration: MODES, DISPOSITIONS, validate). The
// three developer experience modes (DIRECT_INTEGRATION default, GUIDED_INTEGRATION explicit opt-in,
// ASSISTANCE_ON_DEMAND optional) are presentation only: every mode validates an adapter descriptor through the one
// injected validator, educational completion is never an authorization, certification or prerequisite, and selecting a
// mode changes no authority and no state outside the selector. GitHub is the first conforming REFERENCE adapter; it is
// not privileged, and externally supplied descriptors go through the identical validator. The eight conformance
// fixtures are deterministic synthetic records (evidence_class SYNTHETIC_TEST); a synthetic result can never masquerade
// as an authenticated transition. Task Registry invariant: an admitted manifest is an ALLOW transition and always
// carries its receipt, and a synthetic fixture holds none, so the admitted-manifest case is explained as UNKNOWN to
// this surface (receipt not held), never as ALLOW; the run as a whole is FAIL_CLOSED, uncertified and unsubmitted. This file
// performs no I/O, touches no storage, reads nothing from the browser and executes nothing.
(function(root){
"use strict";
if(!root)return;
var SCHEMA="stegverse.workspace.integration-conformance/v1";
var DESCRIPTOR_SCHEMA="stegverse.workspace.governance-integration/v1";
var CONTRACT_REF="StegVerse-Labs/Site:assets/workspace-governance-integration.js";
var FIXTURE_REF="StegVerse-Labs/Site:assets/workspace-integration-conformance.js";
var MODES=Object.freeze(["DIRECT_INTEGRATION","GUIDED_INTEGRATION","ASSISTANCE_ON_DEMAND"]);
var DEFAULT_MODE=MODES[0];
var FRAMEWORK_ID_RE=/^[a-z][a-z0-9._-]{1,63}$/;
var VERSION_RE=/^\d+\.\d+\.\d+$/;
function isObject(v){return !!v&&typeof v==="object"&&!Array.isArray(v);}
function deepFreeze(v){if(v&&typeof v==="object"&&!Object.isFrozen(v)){Object.freeze(v);Object.keys(v).forEach(function(k){deepFreeze(v[k]);});}return v;}
// GitHub reference adapter: a conforming descriptor, nothing more. `role` is informational (the validator ignores
// unknown keys); it grants no precedence over any externally supplied adapter.
var REFERENCE_ADAPTER=deepFreeze({schema:DESCRIPTOR_SCHEMA,framework_id:"github",adapter_version:"1.0.0",capabilities:["READ_PROJECTION","SUBMIT_MANIFEST","OBSERVE_RECEIPT"],authority_effect:"NONE",governance_route:"SDK_MANIFEST_INTR",tutorial_required:false,role:"REFERENCE_ADAPTER"});
// Mode selection is presentation only. ALLOW here admits nothing but the presentation of a mode: it authorizes no
// action, certifies nothing and changes no state (state_changed false); the predicate says so verbatim.
function selectMode(mode){
 if(typeof mode!=="string"||MODES.indexOf(mode)<0)return Object.freeze({schema:SCHEMA,mode:null,requested_mode:typeof mode==="string"?mode:null,guidance_required:false,tutorial_required:false,authority_effect:"NONE",state_changed:false,disposition:"FAIL_CLOSED",predicate:"INTEGRATION_MODE_INVALID"});
 return Object.freeze({schema:SCHEMA,mode:mode,guidance_required:false,tutorial_required:false,authority_effect:"NONE",state_changed:false,disposition:"ALLOW",predicate:"INTEGRATION_MODE_PRESENTATION_ONLY"});
}
function refusal(predicate){return {schema:"stegverse.workspace.governance-integration-validation/v1",disposition:"FAIL_CLOSED",predicate:predicate,descriptor_valid:false,guidance_required:false,authority_effect:"NONE",submitted:false,certified:false,execution_observed:false};}
// The validator is injected (the framework-neutral contract) so this module stays testable and never embeds a second
// validation path; its result is returned unchanged apart from the mode_independent marker. No mode is consulted.
function validateDescriptor(descriptor,validator){
 var result;
 if(typeof validator!=="function")result=refusal("INTEGRATION_CONTRACT_UNAVAILABLE");
 else{try{result=validator(descriptor);}catch(error){result=refusal("INTEGRATION_VALIDATOR_FAILED");}}
 if(!isObject(result))result=refusal("INTEGRATION_VALIDATOR_RESULT_INVALID");
 var out={};Object.keys(result).forEach(function(k){out[k]=result[k];});
 if(out.disposition==="ALLOW")out.disposition="FAIL_CLOSED";
 if(out.descriptor_valid!==true)out.descriptor_valid=false;
 out.mode_independent=true;
 return out;
}
function sourceEvidence(id,description){return [{kind:"SOURCE_REF",ref:FIXTURE_REF+"#"+id,description:description}];}
function fixture(id,title,outcome){return {id:id,title:title,evidence_class:"SYNTHETIC_TEST",synthetic:true,authenticated_transition:false,outcome:outcome};}
function draft(id,remediation){return {schema_version:"stegverse.workspace.interaction-request.v1",action:"DEVELOPER_INTEGRATION_REMEDIATION_REQUEST",workspace_type:"DEVELOPER",fixture_id:id,remediation:remediation,interlock_required:true,intr_required:true,manifest_required:true,manifest_admitted:false,submitted:false,disposition:"FAIL_CLOSED",failing_predicate:"WORKSPACE_INTERACTION_TRANSITION_INTERFACE_NOT_BOUND",authority_effect:"NONE_REQUEST_ONLY",tutorial_required:false,guidance_required:false};}
// Synthetic conformance fixtures: one per outcome class the owner named. Every outcome is written in the
// user-facing-explanation input shape so the explanation card can explain it verbatim; none carries receipt-class
// evidence, so no fixture can ever read as a verified execution.
var FIXTURES=deepFreeze([
 fixture("CONF-ALLOW","Admitted manifest, receipt not held",{disposition:"UNKNOWN",predicate:"INTEGRATION_MANIFEST_RECEIPT_NOT_HELD",requested_action:"Submit a conforming adapter manifest through the SDK manifest/InTr governance route (synthetic fixture CONF-ALLOW)",authority_source:"MANIFEST",consequence_observation:"UNKNOWN",why:"Synthetic fixture: an admitted manifest is an ALLOW transition and always carries its receipt. A synthetic fixture holds no receipt, so this surface cannot show the ALLOW and explains the outcome as unknown to it",evidence:sourceEvidence("CONF-ALLOW","Synthetic conformance fixture source; not a receipt")}),
 fixture("CONF-DENY","Manifest denied by policy",{disposition:"DENY",predicate:"INTEGRATION_MANIFEST_DENIED_BY_POLICY",requested_action:"Submit an adapter manifest whose requested capability exceeds the capability-scoped policy (synthetic fixture CONF-DENY)",authority_source:"INTERLOCK_INTR",consequence_observation:"NOT_AUTHENTICALLY_OBSERVED",why:"Synthetic fixture: the Interlock/InTr policy predicate failed for the requested capability, so the manifest was refused and nothing executed.",evidence:sourceEvidence("CONF-DENY","Synthetic conformance fixture source; not a receipt"),remediation_draft:draft("CONF-DENY","Reduce the requested capabilities to those the capability-scoped policy admits and resubmit through the governed route")}),
 fixture("CONF-FAIL-CLOSED","Governance transition not observed",{disposition:"FAIL_CLOSED",predicate:"AUTHENTIC_MANIFEST_BOUND_GOVERNANCE_TRANSITION_NOT_OBSERVED",requested_action:"Observe an authentic manifest-bound governance transition for a validated adapter descriptor (synthetic fixture CONF-FAIL-CLOSED)",authority_source:"MANIFEST",consequence_observation:"NOT_AUTHENTICALLY_OBSERVED",why:"Synthetic fixture: the descriptor validated, but no authentic manifest-bound governance transition was observed, so the path fails closed by construction rather than guessing.",evidence:sourceEvidence("CONF-FAIL-CLOSED","Synthetic conformance fixture source; not a receipt")}),
 fixture("CONF-INVALID-MANIFEST","Adapter manifest schema invalid",{disposition:"FAIL_CLOSED",predicate:"ADAPTER_MANIFEST_SCHEMA_INVALID",requested_action:"Validate an adapter manifest that does not conform to the governance integration schema (synthetic fixture CONF-INVALID-MANIFEST)",authority_source:"MANIFEST",consequence_observation:"NOT_AUTHENTICALLY_OBSERVED",why:"Synthetic fixture: the manifest did not conform to stegverse.workspace.governance-integration/v1, so validation refused it before any governance evaluation.",evidence:sourceEvidence("CONF-INVALID-MANIFEST","Synthetic conformance fixture source; not a receipt"),remediation_draft:draft("CONF-INVALID-MANIFEST","Correct the descriptor fields named by the validator predicate and validate again; validation is free and repeatable")}),
 fixture("CONF-REVOKED-CONSENT","Integration consent revoked",{disposition:"DENY",predicate:"INTEGRATION_CONSENT_REVOKED",requested_action:"Submit an adapter manifest after the owner revoked integration consent (synthetic fixture CONF-REVOKED-CONSENT)",authority_source:"TV_TVC",consequence_observation:"NOT_AUTHENTICALLY_OBSERVED",why:"Synthetic fixture: the owner's consent for this integration was revoked, so the request was refused; revocation outranks any earlier admission.",evidence:sourceEvidence("CONF-REVOKED-CONSENT","Synthetic conformance fixture source; not a receipt"),remediation_draft:draft("CONF-REVOKED-CONSENT","Request renewed consent through the governed consent route; nothing proceeds until consent is re-granted")}),
 fixture("CONF-MISSING-CREDENTIAL","Capability-scoped material missing",{disposition:"FAIL_CLOSED",predicate:"CAPABILITY_SCOPED_CREDENTIAL_MISSING",requested_action:"Submit an adapter manifest without the capability-scoped TV/TVC material the route requires (synthetic fixture CONF-MISSING-CREDENTIAL)",authority_source:"TV_TVC",consequence_observation:"NOT_AUTHENTICALLY_OBSERVED",why:"Synthetic fixture: the capability-scoped material the governance route requires was absent, so the path failed closed; no material is ever read or shown by this page.",evidence:sourceEvidence("CONF-MISSING-CREDENTIAL","Synthetic conformance fixture source; not a receipt"),remediation_draft:draft("CONF-MISSING-CREDENTIAL","Obtain capability-scoped admission from TV/TVC through the governed route; the page holds and requests no such material")}),
 fixture("CONF-ABSENT-RECEIPT","Transition receipt absent",{disposition:"FAIL_CLOSED",predicate:"TRANSITION_RECEIPT_ABSENT",requested_action:"Read back the transition receipt for an admitted adapter manifest (synthetic fixture CONF-ABSENT-RECEIPT)",authority_source:"INTERLOCK_INTR",consequence_observation:"NOT_AUTHENTICALLY_OBSERVED",why:"Synthetic fixture: no transition receipt exists for the admitted manifest, so the consequence cannot be claimed; only a receipt from the component that performed or refused the transition counts.",evidence:sourceEvidence("CONF-ABSENT-RECEIPT","Synthetic conformance fixture source; not a receipt")}),
 fixture("CONF-UNOBSERVED-RUNTIME","Runtime not authentically observed",{disposition:"UNKNOWN",predicate:"RUNTIME_NOT_AUTHENTICALLY_OBSERVED",requested_action:"Observe the runtime state of an integrated adapter (synthetic fixture CONF-UNOBSERVED-RUNTIME)",authority_source:"NONE",consequence_observation:"UNKNOWN",why:"Synthetic fixture: no authentic runtime observation exists for the adapter, so the surface reports what it could not see rather than guessing.",evidence:sourceEvidence("CONF-UNOBSERVED-RUNTIME","Synthetic conformance fixture source; not a receipt")})
]);
function findFixture(id){for(var i=0;i<FIXTURES.length;i++)if(FIXTURES[i].id===id)return FIXTURES[i];return null;}
// The run never authorizes, certifies or submits: it lists the synthetic fixtures next to the descriptor validation.
function runConformance(descriptor,validator){
 var validation=validateDescriptor(descriptor,validator);
 return {schema:SCHEMA,disposition:"FAIL_CLOSED",predicate:"SYNTHETIC_CONFORMANCE_ONLY",descriptor_validation:validation,
  fixtures:FIXTURES.map(function(f){return {id:f.id,title:f.title,evidence_class:f.evidence_class,synthetic:true,authenticated_transition:false,disposition:f.outcome.disposition,predicate:f.outcome.predicate,consequence_observation:f.outcome.consequence_observation,outcome:f.outcome};}),
  evidence_class:"SYNTHETIC_TEST",authenticated_transition_observed:false,authority_effect:"NONE",certified:false,submitted:false};
}
// Unsubmitted manifest request draft in the page's interaction-request style. The mode is recorded for the record
// only; it is the single field that varies by mode, and it gates nothing.
function buildIntegrationDraft(descriptor,validation,mode){
 var d=isObject(descriptor)?descriptor:{},v=isObject(validation)?validation:refusal("INTEGRATION_VALIDATION_ABSENT");
 return {schema_version:"stegverse.workspace.interaction-request.v1",action:"DEVELOPER_INTEGRATION_SUBMISSION_REQUEST",workspace_type:"DEVELOPER",
  framework_id:typeof d.framework_id==="string"&&FRAMEWORK_ID_RE.test(d.framework_id)?d.framework_id:"FRAMEWORK_ID_NOT_VALID",
  adapter_version:typeof d.adapter_version==="string"&&VERSION_RE.test(d.adapter_version)?d.adapter_version:"ADAPTER_VERSION_NOT_VALID",
  mode:typeof mode==="string"&&MODES.indexOf(mode)>=0?mode:DEFAULT_MODE,descriptor_valid:v.descriptor_valid===true,descriptor_predicate:typeof v.predicate==="string"?v.predicate:"INTEGRATION_VALIDATION_ABSENT",
  governance_route:"SDK_MANIFEST_INTR",interlock_required:true,intr_required:true,manifest_required:true,manifest_admitted:false,submitted:false,disposition:"FAIL_CLOSED",failing_predicate:"WORKSPACE_INTERACTION_TRANSITION_INTERFACE_NOT_BOUND",authority_effect:"NONE_REQUEST_ONLY",tutorial_required:false,guidance_required:false};
}
root.StegVerseWorkspaceIntegrationConformance=Object.freeze({schema:SCHEMA,descriptor_schema:DESCRIPTOR_SCHEMA,contract_ref:CONTRACT_REF,authority_effect:"NONE",DEFAULT_MODE:DEFAULT_MODE,MODES:MODES,REFERENCE_ADAPTER:REFERENCE_ADAPTER,FIXTURES:FIXTURES,selectMode:selectMode,validateDescriptor:validateDescriptor,runConformance:runConformance,buildIntegrationDraft:buildIntegrationDraft,findFixture:findFixture});
}(typeof globalThis!=="undefined"?globalThis:this));
