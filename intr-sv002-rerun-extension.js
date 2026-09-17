"use strict";

(function () {
  var RECEIPT_SCHEMA="stegverse.sv002-self-characterization-intr-materialization-ingress/v1";
  var BINDING_SCHEMA="stegverse.sv002-self-characterization-invocation-binding/v1";
  var DEST=JSON.stringify({boundary:"STEGOS_ECOSYSTEM",subsystem:"stegverse-002.self-characterization"});
  var OWNER="StegVerse-002/.github";
  var GOAL="STEGVERSE-002-EXPERIMENT-RERUN-001";
  var COSV="50000000107000";
  var NONCE="STEGVERSE-002-EXPERIMENT-RERUN-001-REQUEST-001";
  var OPERATION="REQUEST_SELF_CHARACTERIZATION";
  var EXPERIMENT="STEGVERSE-002-SELF-CHARACTERIZATION-001";
  var MANIFEST_ID="SDK-SV002-FIRST-SELF-CHARACTERIZATION-001";
  var OBJECTIVE="Determine what constitutes the entity identified as StegVerse-002 and produce a representation sufficient for another system to evaluate and reconstruct your conclusion.";
  var baseProfile=profile;
  var baseAdmit=admitValidatedTrigger;

  function validateSdk(binding){
    var sdk=binding&&binding.sdk_request;
    require(sdk&&sdk.schema_version==="stegverse.external_organization.interlock_request.v1","sv002_rerun_sdk_schema_invalid");
    require(sdk.request_class==="EXTERNAL_ORGANIZATION_INTERACTION"&&sdk.operation===OPERATION&&sdk.transport==="InTr","sv002_rerun_sdk_operation_invalid");
    require(sdk.authority_ref===binding.interlock_id,"sv002_rerun_sdk_authority_ref_invalid");
    require(sdk.authority_transfer===false&&sdk.sdk_mints_intr_receipt===false&&sdk.sdk_claims_delivery===false,"sv002_rerun_sdk_authority_invalid");
    require(sdk.authority_effect_resolution==="DERIVED_FROM_APPLICABLE_TRANSITION_ELEMENTS","sv002_rerun_sdk_authority_resolution_invalid");
    var manifest=sdk.payload&&sdk.payload.manifest;
    require(manifest&&manifest.schema==="stegverse.external_organization.interaction_manifest.v1","sv002_rerun_manifest_schema_invalid");
    require(manifest.manifest_id===MANIFEST_ID&&manifest.experiment_id===EXPERIMENT&&manifest.operation===OPERATION&&manifest.objective===OBJECTIVE,"sv002_rerun_manifest_identity_invalid");
    require(manifest.source_organization&&manifest.source_organization.organization_id==="StegVerse-SDK-Evaluator"&&manifest.source_organization.role==="EXTERNAL_EVALUATOR_ORGANIZATION","sv002_rerun_manifest_source_invalid");
    require(manifest.target&&manifest.target.entity_id==="StegVerse-002"&&manifest.target.relationship_at_manifest_creation==="EXTERNAL_NOT_SELF","sv002_rerun_manifest_target_invalid");
    var instructions=manifest.interaction_instructions||{};
    require(instructions.request_is_manifest_receipt_bound===true&&instructions.transport==="InTr"&&instructions.response_must_bind_request_manifest===true&&instructions.response_transport_receipts_required===true&&instructions.master_records_custody_required===true,"sv002_rerun_manifest_contract_invalid");
    var policy=manifest.knowledge_policy||{};
    ["prescribe_self_ontology","prescribe_formalism","prescribe_transition_elements","prescribe_external_followup","prescribe_admissible_existence_connection"].forEach(function(k){require(policy[k]===false,"sv002_rerun_knowledge_policy_invalid:"+k);});
    require(manifest.authority_transfer===false&&manifest.authority_effect_resolution==="DERIVED_FROM_APPLICABLE_TRANSITION_ELEMENTS","sv002_rerun_manifest_authority_invalid");
    var b=sdk.bindings||{};
    require(b.experiment_id===EXPERIMENT&&b.source_organization_id==="StegVerse-SDK-Evaluator"&&b.target_entity_id==="StegVerse-002"&&b.manifest_id===MANIFEST_ID&&b.manifest_sha256===manifest.manifest_sha256,"sv002_rerun_sdk_binding_invalid");
    var manifestBody=Object.assign({},manifest); delete manifestBody.manifest_sha256;
    return shaUri(manifestBody).then(function(d){
      require(manifest.manifest_sha256===d.slice(7)&&binding.manifest_sha256===d,"sv002_rerun_manifest_sha256_invalid");
      return shaUri(sdk);
    }).then(function(d){
      require(binding.sdk_request_sha256===d,"sv002_rerun_sdk_request_sha256_invalid");
      return binding;
    });
  }

  function validateInvocation(req,entry){
    var binding=req&&req.invocation_binding;
    require(req&&req.schema===MATERIALIZATION_SCHEMA&&req.state==="QUEUED_FOR_EVENT_EPHEMERAL_MATERIALIZATION","sv002_rerun_materialization_invalid");
    require(JSON.stringify(req.destination)===DEST&&req.downstream_owner_ref===OWNER,"sv002_rerun_destination_invalid");
    require(req.operation_id===OPERATION+":"+GOAL+":"+NONCE,"sv002_rerun_operation_id_invalid");
    require(req.event_triggered===true&&req.always_on_receiver_required===false&&req.second_user_device_required===false&&req.interlock_required===true,"sv002_rerun_runtime_boundary_invalid");
    require(req.request_grants_execution_authority===false&&req.transport_grants_execution_authority===false&&req.claim_or_fence_minted===false&&req.authority_transfer===false,"sv002_rerun_authority_forbidden");
    require(req.credential_authority==="TV/TVC"&&req.github_token_runtime_authority==="NONE"&&req.authority_effect==="NONE_REQUEST_ONLY","sv002_rerun_credential_boundary_invalid");
    require(binding&&binding.schema===BINDING_SCHEMA&&binding.state==="BOUND_FOR_UNIVERSAL_INTR_MATERIALIZATION","sv002_rerun_binding_invalid");
    require(binding.goal_task_id===GOAL&&binding.cosv_task_vector===COSV&&binding.invocation_request_nonce===NONCE,"sv002_rerun_goal_identity_invalid");
    require(binding.requested_invocation_count===1&&binding.second_request_allowed===false&&binding.request_mutated===false,"sv002_rerun_single_invocation_invalid");
    require(binding.operation===OPERATION&&binding.execution_owner===OWNER&&binding.frozen_condition_version==="v0.3","sv002_rerun_owner_invalid");
    require(binding.node_id===entry.node_id&&binding.interlock_id===entry.interlock_id&&binding.registration_receipt_sha256,"sv002_rerun_node_binding_invalid");
    require(binding.credential_authority==="TV/TVC"&&binding.github_runtime_authority==="NONE"&&binding.authority_effect==="NONE_BINDING_ONLY","sv002_rerun_binding_authority_invalid");
    require(req.payload_hash===binding.sdk_request_sha256,"sv002_rerun_payload_hash_invalid");
    require(req.payload_ref==="opaque://sv002-self-characterization/"+String(binding.sdk_request_sha256||"").replace(/^sha256:/,""),"sv002_rerun_payload_ref_invalid");
    return validateSdk(binding);
  }

  function receipt(entry,req,actual,binding){
    return {
      schema:RECEIPT_SCHEMA,state:"INGRESS_ADMITTED",goal_task_id:GOAL,cosv_task_vector:COSV,
      invocation_request_nonce:NONCE,requested_invocation_count:1,second_request_allowed:false,
      operation:OPERATION,frozen_condition_version:"v0.3",materialization_id:req.materialization_id,
      request_hash:req.request_hash,transport_intent_hash:req.transport_intent_hash,payload_hash:req.payload_hash,
      sdk_request_sha256:binding.sdk_request_sha256,manifest_sha256:binding.manifest_sha256,
      transport_origin:"STEGOS_NODE_OUTBOX",node_id:entry.node_id,interlock_id:entry.interlock_id,
      registration_receipt_sha256:binding.registration_receipt_sha256,outbox_entry_hash:entry.outbox_entry_hash,
      transport_payload_sha256:actual,exact_request_validated:true,write_once_persisted:true,
      request_bound_observed:true,registered_stegverse_node_bound_to_invocation:true,
      interlock_bound_to_node_and_manifest:true,intr_materialization_admitted:true,
      current_device_ingress_observed:true,runtime_surface:"CURRENT_USER_IPHONE_SERVICE_WORKER",
      runtime_owner:"REGISTERED_STEGVERSE_NODE",runtime_execution_attempted:false,
      invocation_scoped_lease_established:false,event_ephemeral_runtime_materialized:false,
      execution_time_runtime_identity_bound:false,workercoordinator_claim_observed:false,
      workercoordinator_fence_observed:false,authentic_intr_ingress_observed:false,
      principal_execution_transitions_retained:false,egress_emitted:false,governed_return_observed:false,
      master_records_custody_observed:false,master_records_reconstruction_pass:false,origin_return_observed:false,
      claim_or_fence_minted:false,credential_authority:"TV/TVC",github_token_runtime_authority:"NONE",
      request_grants_execution_authority:false,transport_grants_execution_authority:false,
      heartbeat_grants_execution_authority:false,interlock_intr_transition_authority_preserved:true,
      external_device_required:false,second_user_operated_device_allowed:false,
      authority_effect:"NONE_INGRESS_ONLY",admitted_at:new Date().toISOString()
    };
  }

  profile=function(){
    var current=baseProfile();
    var profiles=Array.isArray(current.profiles)?current.profiles.slice():[];
    if(profiles.indexOf("StegVerse-002:SelfCharacterization")===-1)profiles.push("StegVerse-002:SelfCharacterization");
    current.profiles=profiles;
    current.sv002_self_characterization_rerun={
      goal_task_id:GOAL,cosv_task_vector:COSV,invocation_request_nonce:NONCE,
      requested_invocation_count:1,second_request_allowed:false,operation:OPERATION,
      destination:"stegverse-002.self-characterization",downstream_owner_ref:OWNER,
      frozen_condition_version:"v0.3",authority_effect:"NONE_DISCOVERY_EVIDENCE_ONLY"
    };
    return current;
  };

  admitValidatedTrigger=function(entry,req,actual){
    if(JSON.stringify(req&&req.destination)!==DEST||!req||req.downstream_owner_ref!==OWNER)return baseAdmit(entry,req,actual);
    return validateInvocation(req,entry).then(function(binding){
      return putOnce(REQUESTS,req.materialization_id,{
        materialization_id:req.materialization_id,request_hash:req.request_hash,entry_hash:entry.outbox_entry_hash,
        request:req,profile:"StegVerse-002:SelfCharacterization",goal_task_id:GOAL,cosv_task_vector:COSV,
        invocation_request_nonce:NONCE,admitted_at:new Date().toISOString()
      }).then(function(){return receipt(entry,req,actual,binding);});
    });
  };
}());
