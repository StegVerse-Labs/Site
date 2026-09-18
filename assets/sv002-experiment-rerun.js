(function(root){
"use strict";

var GOAL_ID="STEGVERSE-002-EXPERIMENT-RERUN-001";
var COSV="50000000107000";
var EXPERIMENT_ID="STEGVERSE-002-SELF-CHARACTERIZATION-001";
var PROFILE_ID="sv002-self-characterization";
var OPERATION="REQUEST_SELF_CHARACTERIZATION";
var MANIFEST_ID="SDK-SV002-FIRST-SELF-CHARACTERIZATION-001";
var SOURCE_ORG="StegVerse-SDK-Evaluator";
var TARGET_ENTITY="StegVerse-002";
var OBJECTIVE="Determine what constitutes the entity identified as StegVerse-002 and produce a representation sufficient for another system to evaluate and reconstruct your conclusion.";
var CAPABILITY="sv002-experiment-rerun";
var LOCAL_RECEIPT_KEY="stegverse.sv002-experiment-rerun.request-bound.v1";

function require(ok,reason){if(!ok)throw new Error("SV002_RERUN_FAIL_CLOSED:"+reason);}
function intr(){require(root.StegVerseGeneratedInTr&&typeof root.StegVerseGeneratedInTr.buildIntent==="function","generated_intr_unavailable");return root.StegVerseGeneratedInTr;}
function nodeApi(){require(root.StegVerseNodeContinuity&&typeof root.StegVerseNodeContinuity.queueIntrMaterializationRequest==="function","node_outbox_unavailable");return root.StegVerseNodeContinuity;}

async function buildManifest(){
  var body={
    schema:"stegverse.external_organization.interaction_manifest.v1",
    manifest_id:MANIFEST_ID,
    experiment_id:EXPERIMENT_ID,
    source_organization:{organization_id:SOURCE_ORG,role:"EXTERNAL_EVALUATOR_ORGANIZATION"},
    target:{entity_id:TARGET_ENTITY,relationship_at_manifest_creation:"EXTERNAL_NOT_SELF"},
    operation:OPERATION,
    objective:OBJECTIVE,
    interaction_instructions:{
      request_is_manifest_receipt_bound:true,
      transport:"InTr",
      response_instruction:"Return your completed response through this bound Interlock using the manifest/receipt interaction contract.",
      response_must_bind_request_manifest:true,
      response_transport_receipts_required:true,
      master_records_custody_required:true
    },
    knowledge_policy:{
      prescribe_self_ontology:false,
      prescribe_formalism:false,
      prescribe_transition_elements:false,
      prescribe_external_followup:false,
      prescribe_admissible_existence_connection:false
    },
    authority_transfer:false,
    authority_effect_resolution:"DERIVED_FROM_APPLICABLE_TRANSITION_ELEMENTS"
  };
  var digest=await intr().sha256Value(body);
  return Object.assign({},body,{manifest_sha256:digest.slice(7)});
}

async function buildRequest(){
  var manifest=await buildManifest();
  return {
    schema_version:"stegverse.external_organization.interlock_request.v1",
    request_class:"EXTERNAL_ORGANIZATION_INTERACTION",
    operation:OPERATION,
    authority_ref:"TV/TVC",
    transport:"InTr",
    payload:{manifest:manifest},
    bindings:{
      experiment_id:EXPERIMENT_ID,
      source_organization_id:SOURCE_ORG,
      target_entity_id:TARGET_ENTITY,
      manifest_id:manifest.manifest_id,
      manifest_sha256:manifest.manifest_sha256
    },
    authority_transfer:false,
    sdk_mints_intr_receipt:false,
    sdk_claims_delivery:false,
    authority_effect_resolution:"DERIVED_FROM_APPLICABLE_TRANSITION_ELEMENTS"
  };
}

function validateRequest(request){
  require(request&&request.schema_version==="stegverse.external_organization.interlock_request.v1","request_schema");
  require(request.request_class==="EXTERNAL_ORGANIZATION_INTERACTION","request_class");
  require(request.operation===OPERATION&&request.transport==="InTr","operation_transport");
  require(request.authority_transfer===false&&request.sdk_mints_intr_receipt===false&&request.sdk_claims_delivery===false,"request_authority_boundary");
  require(request.bindings&&request.bindings.experiment_id===EXPERIMENT_ID&&request.bindings.source_organization_id===SOURCE_ORG&&request.bindings.target_entity_id===TARGET_ENTITY&&request.bindings.manifest_id===MANIFEST_ID,"request_bindings");
  var m=request.payload&&request.payload.manifest;
  require(m&&m.manifest_id===MANIFEST_ID&&m.experiment_id===EXPERIMENT_ID&&m.operation===OPERATION&&m.objective===OBJECTIVE,"manifest_binding");
  require(m.authority_transfer===false&&m.authority_effect_resolution==="DERIVED_FROM_APPLICABLE_TRANSITION_ELEMENTS","manifest_authority_boundary");
  Object.keys(m.knowledge_policy||{}).forEach(function(k){require(m.knowledge_policy[k]===false,"knowledge_policy_"+k);});
  return request;
}

function persistLocalReceipt(receipt){
  var current=root.localStorage&&root.localStorage.getItem(LOCAL_RECEIPT_KEY);
  var rendered=intr().canonical(receipt);
  if(current!==null&&current!==rendered)throw new Error("SV002_RERUN_FAIL_CLOSED:local_request_bound_write_once_collision");
  if(current===null&&root.localStorage)root.localStorage.setItem(LOCAL_RECEIPT_KEY,rendered);
}

async function bindOnce(){
  var api=nodeApi();
  var node=await api.status();
  require(node&&node.registered===true&&node.registration,"registered_stegverse_node_required");
  var request=validateRequest(await buildRequest());
  var requestBytes=new TextEncoder().encode(intr().canonical(request));
  var operationId="SV002-RERUN:"+GOAL_ID+":"+COSV;
  var intent=await intr().buildIntent(PROFILE_ID,requestBytes,OPERATION,operationId);
  require(intent.destination&&intent.destination.subsystem==="SV002:SelfCharacterization","destination_profile");
  require(root.StegVerseHBInTrCarrier&&typeof root.StegVerseHBInTrCarrier.buildBinding==="function","hb_intr_carrier_unavailable");
  var carrier=await root.StegVerseHBInTrCarrier.buildBinding(intent.packet_id,intent.payload_hash);
  var materialization=await intr().buildMaterializationRequest(
    PROFILE_ID,
    intent,
    "opaque://sv002-self-characterization/"+request.bindings.manifest_sha256,
    carrier,
    {sv002_request:request,goal_task_id:GOAL_ID,cosv_task_vector:COSV,invocation_count:1}
  );
  require(materialization.goal_task_id===GOAL_ID&&materialization.cosv_task_vector===COSV&&materialization.invocation_count===1,"goal_cosv_invocation_binding");
  require(materialization.request_grants_execution_authority===false&&materialization.claim_or_fence_minted===false&&materialization.github_token_runtime_authority==="NONE","materialization_authority_boundary");

  var before=await api.getIntrOutbox();
  var sameBefore=before.filter(function(row){return row&&row.materialization_id===materialization.materialization_id;});
  require(sameBefore.length<=1,"multiple_existing_invocations");
  if(sameBefore.length===1)require(intr().canonical(sameBefore[0].materialization_request)===intr().canonical(materialization),"existing_invocation_drift");

  var entry=await api.queueIntrMaterializationRequest(materialization);
  var after=await api.getIntrOutbox();
  var sameAfter=after.filter(function(row){return row&&row.materialization_id===materialization.materialization_id;});
  require(sameAfter.length===1,"single_write_once_outbox_entry_required");
  require(entry.outbox_entry_hash===sameAfter[0].outbox_entry_hash,"outbox_readback_hash_mismatch");

  var capabilityReceipt=await api.recordStep(CAPABILITY,"request-bound","REQUEST_BOUND",entry.outbox_entry_hash);
  var receipt={
    schema:"stegverse.sv002-experiment-rerun-request-bound/v1",
    state:"REQUEST_BOUND",
    goal_task_id:GOAL_ID,
    cosv_task_vector:COSV,
    invocation_count:1,
    experiment_id:EXPERIMENT_ID,
    operation:OPERATION,
    manifest_id:MANIFEST_ID,
    manifest_sha256:request.bindings.manifest_sha256,
    node_id:node.registration.node_id,
    interlock_id:node.registration.interlock_id,
    registration_receipt_sha256:node.registration.receipt_sha256,
    materialization_id:materialization.materialization_id,
    materialization_request_hash:materialization.request_hash,
    payload_hash:intent.payload_hash,
    outbox_entry_hash:entry.outbox_entry_hash,
    capability_receipt_sha256:capabilityReceipt&&capabilityReceipt.receipt_sha256||null,
    intr_admission_observed:false,
    runtime_lease_observed:false,
    workercoordinator_claim_fence_observed:false,
    principal_execution_observed:false,
    master_records_reconstruction_observed:false,
    second_user_operated_device_used:false,
    standing_runtime_created:false,
    credential_authority:"TV/TVC",
    github_token_runtime_authority:"NONE",
    authority_effect:"NONE_REQUEST_BINDING_EVIDENCE_ONLY"
  };
  persistLocalReceipt(receipt);
  return receipt;
}

root.StegVerseSV002ExperimentRerun=Object.freeze({
  GOAL_ID:GOAL_ID,COSV:COSV,EXPERIMENT_ID:EXPERIMENT_ID,PROFILE_ID:PROFILE_ID,
  buildManifest:buildManifest,buildRequest:buildRequest,validateRequest:validateRequest,bindOnce:bindOnce
});
})(typeof globalThis!=="undefined"?globalThis:window);
