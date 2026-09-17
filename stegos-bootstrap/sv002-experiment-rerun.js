(function(root){
"use strict";

var GOAL="STEGVERSE-002-EXPERIMENT-RERUN-001";
var COSV="50000000107000";
var NONCE="STEGVERSE-002-EXPERIMENT-RERUN-001-REQUEST-001";
var OPERATION="REQUEST_SELF_CHARACTERIZATION";
var EXPERIMENT="STEGVERSE-002-SELF-CHARACTERIZATION-001";
var OWNER="StegVerse-002/.github";
var DESTINATION={boundary:"STEGOS_ECOSYSTEM",subsystem:"stegverse-002.self-characterization"};
var MANIFEST_ID="SDK-SV002-FIRST-SELF-CHARACTERIZATION-001";
var OBJECTIVE="Determine what constitutes the entity identified as StegVerse-002 and produce a representation sufficient for another system to evaluate and reconstruct your conclusion.";
var RESPONSE_INSTRUCTION="Return your completed response through this bound Interlock using the manifest/receipt interaction contract.";
var CAPABILITY="sv002-self-characterization-rerun";
var RETAINED_KEY="stegverse.sv002.experiment-rerun.request-bound.v1";

function fail(reason){throw new Error("FAIL_CLOSED: "+reason);}
function canonical(v){
  if(v===null||typeof v!=="object")return JSON.stringify(v);
  if(Array.isArray(v))return "["+v.map(canonical).join(",")+"]";
  return "{"+Object.keys(v).sort().map(function(k){return JSON.stringify(k)+":"+canonical(v[k]);}).join(",")+"}";
}
function hex(bytes){return Array.from(new Uint8Array(bytes)).map(function(b){return b.toString(16).padStart(2,"0");}).join("");}
function shaHex(v){return crypto.subtle.digest("SHA-256",new TextEncoder().encode(canonical(v))).then(hex);}
function shaUri(v){return shaHex(v).then(function(h){return "sha256:"+h;});}
function clone(v){return JSON.parse(JSON.stringify(v));}

function buildManifest(){
  var body={
    schema:"stegverse.external_organization.interaction_manifest.v1",
    manifest_id:MANIFEST_ID,
    experiment_id:EXPERIMENT,
    source_organization:{organization_id:"StegVerse-SDK-Evaluator",role:"EXTERNAL_EVALUATOR_ORGANIZATION"},
    target:{entity_id:"StegVerse-002",relationship_at_manifest_creation:"EXTERNAL_NOT_SELF"},
    operation:OPERATION,
    objective:OBJECTIVE,
    interaction_instructions:{
      request_is_manifest_receipt_bound:true,
      transport:"InTr",
      response_instruction:RESPONSE_INSTRUCTION,
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
  return shaHex(body).then(function(d){return Object.assign({},body,{manifest_sha256:d});});
}

function buildSdkRequest(interlockId){
  return buildManifest().then(function(manifest){
    return {
      schema_version:"stegverse.external_organization.interlock_request.v1",
      request_class:"EXTERNAL_ORGANIZATION_INTERACTION",
      operation:OPERATION,
      authority_ref:interlockId,
      transport:"InTr",
      payload:{manifest:manifest},
      bindings:{
        experiment_id:EXPERIMENT,
        source_organization_id:"StegVerse-SDK-Evaluator",
        target_entity_id:"StegVerse-002",
        manifest_id:MANIFEST_ID,
        manifest_sha256:manifest.manifest_sha256
      },
      authority_transfer:false,
      sdk_mints_intr_receipt:false,
      sdk_claims_delivery:false,
      authority_effect_resolution:"DERIVED_FROM_APPLICABLE_TRANSITION_ELEMENTS"
    };
  });
}

function buildMaterialization(node){
  var reg=node&&node.registration;
  if(!node||node.registered!==true||!reg||!reg.node_id||!reg.interlock_id||!reg.receipt_sha256)fail("registered StegVerse Node Receipt #1 required");
  return buildSdkRequest(reg.interlock_id).then(function(sdkRequest){
    return Promise.all([shaUri(sdkRequest),shaUri(sdkRequest.payload.manifest)]).then(function(hashes){
      var sdkHash=hashes[0],manifestHash=hashes[1];
      var binding={
        schema:"stegverse.sv002-self-characterization-invocation-binding/v1",
        state:"BOUND_FOR_UNIVERSAL_INTR_MATERIALIZATION",
        goal_task_id:GOAL,
        cosv_task_vector:COSV,
        invocation_request_nonce:NONCE,
        requested_invocation_count:1,
        second_request_allowed:false,
        operation:OPERATION,
        execution_owner:OWNER,
        frozen_condition_version:"v0.3",
        node_id:reg.node_id,
        interlock_id:reg.interlock_id,
        registration_receipt_sha256:reg.receipt_sha256,
        manifest_sha256:manifestHash,
        sdk_request_sha256:sdkHash,
        sdk_request:sdkRequest,
        request_mutated:false,
        credential_authority:"TV/TVC",
        github_runtime_authority:"NONE",
        authority_effect:"NONE_BINDING_ONLY"
      };
      var operationId=OPERATION+":"+GOAL+":"+NONCE;
      var packetBasis={
        operation_id:operationId,
        payload_hash:sdkHash,
        source_boundary:"DEVICE_SYSTEM",
        source_subsystem:"StegVerseNode:SelfCharacterizationRequest",
        destination_boundary:DESTINATION.boundary,
        destination_subsystem:DESTINATION.subsystem,
        boundary_path:["DEVICE_SYSTEM","STEGOS_ECOSYSTEM"]
      };
      return shaHex(packetBasis).then(function(packetDigest){
        var intent={
          schema:"stegverse.universal-intr-transport/v1",
          protocol:"InTr",
          operation_id:operationId,
          packet_id:"INTR-"+packetDigest.slice(0,24),
          payload_hash:sdkHash,
          prior_transport_receipt_hash:null,
          source:{boundary:"DEVICE_SYSTEM",subsystem:"StegVerseNode:SelfCharacterizationRequest"},
          destination:DESTINATION,
          boundary_path:["DEVICE_SYSTEM","STEGOS_ECOSYSTEM"],
          interlock_required:true,
          transport_semantics:{
            event_triggered:true,
            always_on_receiver_required:false,
            second_user_device_required:false,
            receiver_unavailable_disposition:"DURABLE_QUEUE_OR_EVENT_EPHEMERAL_MATERIALIZATION",
            exact_packet_transport_retry_allowed:true,
            blind_consequence_retry_allowed:false
          },
          authority:{authority_transfer:false,transport_grants_execution_authority:false,credential_authority:"TV/TVC"},
          receipt_chain:{required:true,receipt_schema:"stegverse.intr.hop_receipt/v1",payload_plaintext_in_receipts:false,prior_hash_required_after_first_hop:true}
        };
        return shaUri(intent).then(function(intentHash){
          var basis={transport_intent_hash:intentHash,operation_id:operationId,packet_id:intent.packet_id,payload_hash:sdkHash,destination:DESTINATION};
          return shaHex(basis).then(function(materializationDigest){
            var body={
              schema:"stegverse.universal-intr-materialization-request/v1",
              materialization_id:"INTR-MAT-"+materializationDigest.slice(0,24),
              state:"QUEUED_FOR_EVENT_EPHEMERAL_MATERIALIZATION",
              transport_schema:"stegverse.universal-intr-transport/v1",
              transport_protocol:"InTr",
              transport_intent_hash:intentHash,
              operation_id:operationId,
              packet_id:intent.packet_id,
              payload_hash:sdkHash,
              payload_ref:"opaque://sv002-self-characterization/"+sdkHash.slice(7),
              destination:DESTINATION,
              boundary_path:["DEVICE_SYSTEM","STEGOS_ECOSYSTEM"],
              downstream_owner_ref:OWNER,
              event_triggered:true,
              always_on_receiver_required:false,
              second_user_device_required:false,
              receiver_unavailable_disposition:"DURABLE_QUEUE_OR_EVENT_EPHEMERAL_MATERIALIZATION",
              exact_packet_transport_retry_allowed:true,
              blind_consequence_retry_allowed:false,
              interlock_required:true,
              request_grants_execution_authority:false,
              claim_or_fence_minted:false,
              transport_grants_execution_authority:false,
              credential_authority:"TV/TVC",
              github_token_runtime_authority:"NONE",
              authority_transfer:false,
              authority_effect:"NONE_REQUEST_ONLY",
              invocation_binding:binding
            };
            return shaUri(body).then(function(requestHash){return Object.assign({},body,{request_hash:requestHash});});
          });
        });
      });
    });
  });
}

function buildTrigger(entry){
  var body={
    schema:"stegos.node_intr_materialization_trigger.v1",
    transport_origin:"STEGOS_NODE_OUTBOX",
    node_id:entry.node_id,
    interlock_id:entry.interlock_id,
    outbox_entry_hash:entry.outbox_entry_hash,
    node_outbox_entry:entry,
    request_grants_execution_authority:false,
    claim_or_fence_minted:false,
    authority_effect:"NONE_TRIGGER_ONLY"
  };
  return shaUri(body).then(function(h){return Object.assign({},body,{trigger_sha256:h});});
}

function queryProfile(worker){
  return new Promise(function(resolve,reject){
    var channel=new MessageChannel();
    var timer=setTimeout(function(){reject(new Error("root InTr profile query timed out"));},2500);
    channel.port1.onmessage=function(event){
      clearTimeout(timer);
      var data=event.data||{};
      if(!data.ok||!data.profile){reject(new Error(String(data.reason||"root InTr profile unavailable")));return;}
      resolve(data.profile);
    };
    worker.postMessage({type:"STEGVERSE_INTR_PROFILE_QUERY"},[channel.port2]);
  });
}

function profileMatches(profile){
  var b=profile&&profile.sv002_self_characterization_rerun;
  return !!(profile&&Array.isArray(profile.profiles)&&profile.profiles.indexOf("StegVerse-002:SelfCharacterization")!==-1&&
    b&&b.goal_task_id===GOAL&&b.cosv_task_vector===COSV&&b.invocation_request_nonce===NONCE&&
    b.requested_invocation_count===1&&b.second_request_allowed===false&&b.operation===OPERATION&&
    b.downstream_owner_ref===OWNER&&b.frozen_condition_version==="v0.3");
}

function installedWorker(registration){
  var deadline=Date.now()+12000;
  function probe(){
    var workers=[registration.waiting,registration.active,navigator.serviceWorker.controller].filter(Boolean);
    return workers.reduce(function(p,worker){
      return p.then(function(found){
        if(found)return found;
        return queryProfile(worker).then(function(profile){return profileMatches(profile)?worker:null;}).catch(function(){return null;});
      });
    },Promise.resolve(null)).then(function(found){
      if(found)return found;
      if(Date.now()>=deadline)fail("root Universal InTr worker has not loaded the SV002 rerun binding");
      return registration.update().catch(function(){}).then(function(){
        return new Promise(function(resolve){setTimeout(resolve,300);});
      }).then(probe);
    });
  }
  return probe();
}

function rootIngressWorker(){
  if(!navigator.serviceWorker)fail("service worker unavailable");
  return navigator.serviceWorker.register("/intr-service-worker.js",{scope:"/"}).then(function(registration){
    return registration.update().catch(function(){return registration;}).then(function(){return installedWorker(registration);});
  });
}

function sendTrigger(worker,trigger){
  return new Promise(function(resolve,reject){
    var channel=new MessageChannel();
    var timer=setTimeout(function(){reject(new Error("SV002 rerun InTr admission timed out"));},8000);
    channel.port1.onmessage=function(event){
      clearTimeout(timer);
      var data=event.data||{};
      if(!data.ok||!data.receipt){reject(new Error("SV002 rerun InTr admission denied: "+String(data.reason||"unknown")));return;}
      resolve(data.receipt);
    };
    worker.postMessage({type:"STEGVERSE_INTR_LOCAL_TRIGGER",trigger:trigger},[channel.port2]);
  });
}

function validateReceipt(r,entry){
  if(!r||r.schema!=="stegverse.sv002-self-characterization-intr-materialization-ingress/v1"||r.state!=="INGRESS_ADMITTED")fail("SV002 rerun ingress receipt invalid");
  if(r.goal_task_id!==GOAL||r.cosv_task_vector!==COSV||r.invocation_request_nonce!==NONCE||r.requested_invocation_count!==1||r.second_request_allowed!==false)fail("SV002 rerun receipt correlation invalid");
  if(r.operation!==OPERATION||r.frozen_condition_version!=="v0.3")fail("SV002 rerun receipt operation invalid");
  if(r.materialization_id!==entry.materialization_id||r.request_hash!==entry.request_hash||r.outbox_entry_hash!==entry.outbox_entry_hash)fail("SV002 rerun receipt outbox binding invalid");
  if(r.node_id!==entry.node_id||r.interlock_id!==entry.interlock_id)fail("SV002 rerun receipt Node/Interlock binding invalid");
  if(r.request_bound_observed!==true||r.registered_stegverse_node_bound_to_invocation!==true||r.interlock_bound_to_node_and_manifest!==true||r.intr_materialization_admitted!==true)fail("SV002 rerun first-seam evidence incomplete");
  ["runtime_execution_attempted","invocation_scoped_lease_established","event_ephemeral_runtime_materialized","execution_time_runtime_identity_bound","workercoordinator_claim_observed","workercoordinator_fence_observed","authentic_intr_ingress_observed","principal_execution_transitions_retained","egress_emitted","governed_return_observed","master_records_custody_observed","master_records_reconstruction_pass","origin_return_observed"].forEach(function(k){if(r[k]!==false)fail("downstream predicate promoted at request-binding seam: "+k);});
  if(r.credential_authority!=="TV/TVC"||r.github_token_runtime_authority!=="NONE"||r.claim_or_fence_minted!==false||r.authority_effect!=="NONE_INGRESS_ONLY")fail("SV002 rerun receipt authority invalid");
  return r;
}

function retainEvidence(value){
  var raw=canonical(value),prior=localStorage.getItem(RETAINED_KEY);
  if(prior&&prior!==raw)fail("retained REQUEST_BOUND evidence write-once collision");
  if(!prior)localStorage.setItem(RETAINED_KEY,raw);
  return value;
}

function loadRetainedEvidence(){
  var raw=localStorage.getItem(RETAINED_KEY);
  if(!raw)return null;
  try{return JSON.parse(raw);}catch(_e){fail("retained REQUEST_BOUND evidence invalid");}
}

function start(){
  var node,entry;
  var retained=loadRetainedEvidence();
  if(retained&&retained.goal_task_id===GOAL&&retained.cosv_task_vector===COSV&&retained.invocation_request_nonce===NONCE)return Promise.resolve(retained);
  if(!root.StegVerseNodeContinuity||typeof root.StegVerseNodeContinuity.queueIntrMaterializationRequest!=="function")return Promise.reject(new Error("canonical registered StegVerse Node outbox unavailable"));
  return root.StegVerseNodeContinuity.status().then(function(value){
    node=value;
    if(!node||node.registered!==true)fail("registered StegVerse Node required");
    return buildMaterialization(node);
  }).then(function(materialization){
    return root.StegVerseNodeContinuity.queueIntrMaterializationRequest(materialization);
  }).then(function(value){
    entry=value;
    return root.StegVerseNodeContinuity.recordStep(CAPABILITY,"request","QUEUED",entry.outbox_entry_hash).catch(function(){return null;});
  }).then(function(){
    return Promise.all([rootIngressWorker(),buildTrigger(entry)]);
  }).then(function(values){
    return sendTrigger(values[0],values[1]);
  }).then(function(receipt){
    validateReceipt(receipt,entry);
    var evidence={
      schema:"stegverse.sv002-experiment-rerun.request-bound-evidence/v1",
      state:"REQUEST_BOUND",
      goal_task_id:GOAL,
      cosv_task_vector:COSV,
      invocation_request_nonce:NONCE,
      requested_invocation_count:1,
      second_request_allowed:false,
      frozen_condition_version:"v0.3",
      node_outbox_entry_hash:entry.outbox_entry_hash,
      ingress_receipt:clone(receipt),
      request_bound:true,
      steverse_node_bound_to_invocation:true,
      interlock_bound_to_node_and_manifest:true,
      intr_materialization_admitted:true,
      downstream_execution_started:false,
      authority_effect:"NONE_EVIDENCE_ONLY"
    };
    return retainEvidence(evidence);
  });
}

root.StegVerseSV002ExperimentRerun=Object.freeze({
  start:start,
  loadRetainedEvidence:loadRetainedEvidence,
  buildManifest:buildManifest,
  buildSdkRequest:buildSdkRequest,
  taskId:GOAL,
  cosvId:COSV,
  nonce:NONCE,
  operation:OPERATION,
  authority_effect:"NONE"
});
}(window));
