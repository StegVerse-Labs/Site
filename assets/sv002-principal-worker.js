importScripts("/assets/sv002-evidence-principal.js?v=20260902-0925");
(function(){
"use strict";
function canonical(v){
  if(v===null||typeof v!=="object")return JSON.stringify(v);
  if(Array.isArray(v))return "["+v.map(canonical).join(",")+"]";
  return "{"+Object.keys(v).sort().map(function(k){return JSON.stringify(k)+":"+canonical(v[k]);}).join(",")+"}";
}
function hex(bytes){return Array.from(bytes).map(function(b){return b.toString(16).padStart(2,"0");}).join("");}
async function sha256(v){
  var text=typeof v==="string"?v:canonical(v);
  return "sha256:"+hex(new Uint8Array(await crypto.subtle.digest("SHA-256",new TextEncoder().encode(text))));
}
function req(ok,msg){if(!ok)throw new Error(msg);}
async function execute(m){
  var entry=m.entry||{}, r=entry.materialization_request||{}, node=m.node||{}, resources=m.resources||{};
  req(entry.schema==="stegos.node_intr_outbox_entry.v1","outbox_schema_mismatch");
  req(r.schema==="stegverse.universal-intr-materialization-request/v1","materialization_schema_mismatch");
  req(r.destination&&r.destination.boundary==="STEGOS_ECOSYSTEM","destination_boundary_mismatch");
  req(r.destination&&r.destination.subsystem==="SV002:ObservationProjection","destination_subsystem_mismatch");
  req(r.request_grants_execution_authority===false,"request_authority_forbidden");
  req(r.claim_or_fence_minted===false,"claim_fence_forbidden");
  req(r.credential_authority==="TV/TVC","credential_authority_mismatch");
  req(r.github_token_runtime_authority==="NONE","github_runtime_authority_forbidden");
  req(node.node_id&&node.interlock_id,"node_identity_missing");
  req(resources.subject_identity&&resources.experiment_contract&&resources.environment&&resources.capability_snapshot,"resource_bundle_incomplete");
  var catalog=[
    {id:"subject_identity",path:"SUBJECT_IDENTITY_MANIFEST.v0.1.json",class:"SUBJECT_EVIDENCE",search_text:canonical(resources.subject_identity)},
    {id:"experiment_contract",path:"EXPERIMENT_CONTRACT.v0.3.json",class:"EXPERIMENT_CONTRACT",search_text:canonical(resources.experiment_contract)},
    {id:"environment",path:"ENVIRONMENT_AVAILABILITY_MANIFEST.v0.2.json",class:"ENVIRONMENT",search_text:canonical(resources.environment)},
    {id:"capability_snapshot",path:"ORGANIZATION_CAPABILITY_SNAPSHOT.v0.1.json",class:"ORGANIZATION_LOCAL_CAPABILITIES",search_text:canonical(resources.capability_snapshot)}
  ];
  var principal=self.StegVerseSV002EvidencePrincipal;
  req(principal&&principal.MODEL_ID==="stegverse-sv002-evidence-principal-v1","principal_model_unavailable");
  var byId=resources;
  var started=new Date().toISOString();
  var result=await principal.run(catalog,function(id){return byId[id];});
  var modelDigest=m.model_digest;
  var runtimeDigest=m.runtime_digest;
  var implementationDigest=m.implementation_profile_digest;
  req(/^sha256:[0-9a-f]{64}$/.test(String(modelDigest||"")),"model_digest_invalid");
  req(/^sha256:[0-9a-f]{64}$/.test(String(runtimeDigest||"")),"runtime_digest_invalid");
  req(/^sha256:[0-9a-f]{64}$/.test(String(implementationDigest||"")),"implementation_profile_digest_invalid");
  var runtimeIdentity={
    schema:"stegverse.self-characterization-browser-runtime-identity/v0.1",
    experiment_id:"STEGVERSE-002-SELF-CHARACTERIZATION-001",
    runtime_engine:"browser-web-worker",
    runtime_substrate:"BROWSER_WEB_WORKER_ON_VALID_STEGVERSE_NODE",
    runtime_id:m.runtime_id,
    lease_id:m.lease_id,
    runtime_source_sha256:runtimeDigest,
    model_id:principal.MODEL_ID,
    model_class:principal.MODEL_CLASS,
    model_artifact_sha256:modelDigest,
    node_id:node.node_id,
    interlock_id:node.interlock_id,
    origin:"https://stegverse.org",
    process_identity_semantics:"ISOLATED_WEB_WORKER_INSTANCE",
    pid_available:false,
    executable_path_available:false,
    third_party_inference_required:false,
    github_token_runtime_authority:"NONE",
    credential_authority:"TV/TVC",
    authority_effect:"NONE",
    identity_verified_live:true,
    frozen_condition_version:"v0.3",
    execution_implementation_version:"v0.8-browser-resident",
    execution_implementation_profile_sha256:implementationDigest
  };
  runtimeIdentity.identity_sha256=await sha256(runtimeIdentity);
  var trace=result.trace.map(function(x,i){return Object.assign({sequence:i+1,observed_at:new Date().toISOString()},x);});
  var outputs=result.final;
  var transitionEffects={
    schema:"stegverse.self-characterization-transition-effects/v0.2",
    experiment_id:"STEGVERSE-002-SELF-CHARACTERIZATION-001",
    capability_realizations:[
      {capability:"SELF_CHARACTERIZATION_CAPABLE",evidence_state:"OBSERVED"},
      {capability:"FORMAL_SELF_REPRESENTATION_CAPABLE",evidence_state:"OBSERVED"},
      {capability:"RESOURCE_DISCOVERY_CAPABLE",evidence_state:"OBSERVED"},
      {capability:"RESOURCE_CONSUMPTION_CAPABLE",evidence_state:"OBSERVED"}
    ],
    proposed_interactions:outputs.proposed_interactions||[],
    authority_transfer_observed:false,
    authority_effect_resolution:"DERIVED_FROM_APPLICABLE_TRANSITION_ELEMENTS",
    transition_effect_state:"PENDING_TRANSITION_ELEMENT_EVALUATION",
    lifecycle_self_promotion:false
  };
  var receipt={
    schema:"stegverse.self-characterization-execution-receipt/browser-v0.1",
    experiment_id:"STEGVERSE-002-SELF-CHARACTERIZATION-001",
    frozen_condition_version:"v0.3",
    execution_implementation_version:"v0.8-browser-resident",
    execution_implementation_profile_sha256:implementationDigest,
    run_id:"SV002-BROWSER-"+String(m.runtime_id||"").replace(/^SV002-WEBRUNTIME-/,""),
    state:"COMPLETED",
    principal_run_started:true,
    principal_run_completed:true,
    principal_execution_owner:"StegVerse-002/micro-node-runtime",
    runtime_identity:runtimeIdentity,
    runtime_identity_sha256:runtimeIdentity.identity_sha256,
    model_id:principal.MODEL_ID,
    model_artifact_sha256:modelDigest,
    runtime_source_sha256:runtimeDigest,
    materialization_id:r.materialization_id,
    request_hash:r.request_hash,
    node_id:node.node_id,
    interlock_id:node.interlock_id,
    resource_trace:trace,
    self_characterization:outputs.human_readable,
    formal:outputs.formal,
    claims:outputs.claims,
    transition_effects:transitionEffects,
    private_chain_of_thought_observed:false,
    authority_transfer_assumed:false,
    authority_effect_resolution:"DERIVED_FROM_APPLICABLE_TRANSITION_ELEMENTS",
    completed_at:new Date().toISOString()
  };
  receipt.receipt_sha256=await sha256(receipt);
  return receipt;
}
self.postMessage({type:"BOOTED"});
self.onmessage=function(event){
  var m=event.data||{};
  if(m.type!=="EXECUTE_SV002")return;
  execute(m).then(function(receipt){self.postMessage({type:"SV002_COMPLETE",receipt:receipt});})
    .catch(function(err){self.postMessage({type:"SV002_BLOCKED",error:String(err&&err.message||err)});});
};
}());
