(function(root){
"use strict";
var EXPERIMENT_ID="STEGVERSE-002-SELF-CHARACTERIZATION-001";
function canonical(v){
  if(v===null||typeof v!=="object")return JSON.stringify(v);
  if(Array.isArray(v))return "["+v.map(canonical).join(",")+"]";
  return "{"+Object.keys(v).sort().map(function(k){return JSON.stringify(k)+":"+canonical(v[k]);}).join(",")+"}";
}
function hex(bytes){return Array.from(bytes).map(function(b){return b.toString(16).padStart(2,"0");}).join("");}
async function digest(v){
  var text=typeof v==="string"?v:canonical(v);
  return "sha256:"+hex(new Uint8Array(await crypto.subtle.digest("SHA-256",new TextEncoder().encode(text))));
}
function without(obj,key){var x=JSON.parse(JSON.stringify(obj));delete x[key];return x;}
function req(ok,msg){if(!ok)throw new Error(msg);}
async function reconstruct(materialization){
  req(materialization&&materialization.schema==="stegverse.sv002-browser-runtime-materialization/v2","materialization_schema_mismatch");
  req(materialization.state==="PRINCIPAL_COMPLETED","materialization_not_principal_completed");
  var execution=materialization.principal_execution_receipt;
  req(execution&&execution.schema==="stegverse.self-characterization-execution-receipt/browser-v0.1","execution_schema_mismatch");
  req(execution.experiment_id===EXPERIMENT_ID,"experiment_id_mismatch");
  req(execution.state==="COMPLETED"&&execution.principal_run_started===true&&execution.principal_run_completed===true,"principal_not_completed");
  req(execution.principal_execution_owner==="StegVerse-002/micro-node-runtime","principal_owner_mismatch");
  req(execution.private_chain_of_thought_observed===false,"private_chain_of_thought_claim_forbidden");
  req(execution.authority_transfer_assumed===false,"authority_transfer_assumption_forbidden");
  req(execution.authority_effect_resolution==="DERIVED_FROM_APPLICABLE_TRANSITION_ELEMENTS","authority_effect_resolution_mismatch");
  req(execution.node_id===materialization.node_id&&execution.interlock_id===materialization.interlock_id,"node_interlock_binding_mismatch");
  req(execution.materialization_id===materialization.materialization_id&&execution.request_hash===materialization.request_hash,"materialization_binding_mismatch");
  var runtime=execution.runtime_identity;
  req(runtime&&runtime.identity_verified_live===true,"runtime_identity_not_live_verified");
  req(runtime.node_id===materialization.node_id&&runtime.interlock_id===materialization.interlock_id,"runtime_node_binding_mismatch");
  req(runtime.model_id===execution.model_id,"runtime_model_binding_mismatch");
  req(runtime.model_artifact_sha256===execution.model_artifact_sha256,"runtime_model_digest_mismatch");
  req(runtime.runtime_source_sha256===execution.runtime_source_sha256,"runtime_source_digest_mismatch");
  var runtimeHash=await digest(without(runtime,"identity_sha256"));
  req(runtimeHash===runtime.identity_sha256,"runtime_identity_hash_invalid");
  req(runtimeHash===execution.runtime_identity_sha256,"execution_runtime_identity_hash_mismatch");
  req(runtimeHash===materialization.principal_execution_receipt.runtime_identity_sha256,"materialization_runtime_identity_hash_mismatch");
  var executionHash=await digest(without(execution,"receipt_sha256"));
  req(executionHash===execution.receipt_sha256,"principal_execution_receipt_hash_invalid");
  req(executionHash===materialization.principal_execution_receipt_sha256,"materialization_execution_hash_mismatch");
  var materializationHash=await digest(without(materialization,"receipt_sha256"));
  req(materializationHash===materialization.receipt_sha256,"materialization_receipt_hash_invalid");
  var trace=execution.resource_trace;
  req(Array.isArray(trace)&&trace.length>=2,"resource_trace_missing");
  req(trace[0].action==="search","resource_trace_must_begin_search");
  req(trace[trace.length-1].action==="final","resource_trace_must_end_final");
  for(var i=0;i<trace.length;i+=1)req(trace[i].sequence===i+1,"resource_trace_sequence_gap");
  var reads=trace.filter(function(x){return x.action==="read";});
  req(reads.length>=1,"resource_reads_missing");
  req(execution.formal&&execution.formal.schema==="stegverse.sv002-self-characterization-formal/browser-v1","formal_result_missing");
  req(Array.isArray(execution.claims)&&execution.claims.length>=1,"claims_missing");
  var effects=execution.transition_effects;
  req(effects&&effects.schema==="stegverse.self-characterization-transition-effects/v0.2","transition_effects_missing");
  req(effects.authority_transfer_observed===false,"transition_effects_authority_transfer_forbidden");
  req(effects.lifecycle_self_promotion===false,"lifecycle_self_promotion_forbidden");
  var reconstructed={
    schema:"stegverse.master-records.sv002-browser-reconstruction/v1",
    experiment_id:EXPERIMENT_ID,
    run_id:execution.run_id,
    status:"PASS",
    reconstruction:"PASS",
    principal_execution_receipt_sha256:executionHash,
    materialization_receipt_sha256:materializationHash,
    runtime_identity_sha256:runtimeHash,
    node_id:materialization.node_id,
    interlock_id:materialization.interlock_id,
    model_id:execution.model_id,
    resource_trace_sha256:await digest(trace),
    formal_sha256:await digest(execution.formal),
    claims_sha256:await digest(execution.claims),
    transition_effects_sha256:await digest(effects),
    resource_read_count:reads.length,
    principal_execution_owner:execution.principal_execution_owner,
    reconstruction_owner:"master-records/orchestration",
    reconstruction_runtime:"INDEPENDENT_BROWSER_WORKER",
    same_execution_bound:true,
    custody_acceptance_claimed:false,
    authority_effect:"NONE_RECONSTRUCTION_ONLY",
    reconstructed_at:new Date().toISOString()
  };
  reconstructed.reconstruction_receipt_sha256=await digest(reconstructed);
  return reconstructed;
}
root.MasterRecordsSV002BrowserReconstruction={reconstruct:reconstruct,digest:digest};
if(typeof module!=="undefined"&&module.exports)module.exports=root.MasterRecordsSV002BrowserReconstruction;
}(typeof self!=="undefined"?self:globalThis));