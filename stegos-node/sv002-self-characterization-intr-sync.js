"use strict";

(function(root){
  var TARGET_URL="/stegos-node/sv002-self-characterization-intr-sync-target.json";
  var TARGET_SCHEMA="stegos.site.sv002_self_characterization_intr_sync_target.v1";
  var TRIGGER_SCHEMA="stegos.node_intr_materialization_trigger.v1";
  var OUTBOX_SCHEMA="stegos.node_intr_outbox_entry.v1";
  var INGRESS_RECEIPT_SCHEMA="stegverse.sv002-self-characterization-intr-materialization-ingress/v1";
  var DESTINATION=JSON.stringify({boundary:"STEGOS_ECOSYSTEM",subsystem:"SV002:SelfCharacterization"});
  var OWNER="StegVerse-002/.github";
  var GOAL="STEGVERSE-002-EXPERIMENT-RERUN-001";
  var COSV="50000000107000";
  var OPERATION="REQUEST_SELF_CHARACTERIZATION";
  var CAPABILITY="sv002-experiment-rerun";

  function canonical(v){if(v===null||typeof v!=="object")return JSON.stringify(v);if(Array.isArray(v))return "["+v.map(canonical).join(",")+"]";return "{"+Object.keys(v).sort().map(function(k){return JSON.stringify(k)+":"+canonical(v[k]);}).join(",")+"}";}
  function hex(bytes){return Array.from(bytes,function(v){return v.toString(16).padStart(2,"0");}).join("");}
  function sha256Hex(v){var text=typeof v==="string"?v:canonical(v);return crypto.subtle.digest("SHA-256",new TextEncoder().encode(text)).then(function(d){return hex(new Uint8Array(d));});}
  function sha256Uri(v){return sha256Hex(v).then(function(d){return "sha256:"+d;});}
  function fail(reason){throw new Error("SV002_RERUN_SYNC_FAIL_CLOSED:"+reason);}

  function validateTarget(target){
    if(!target||target.schema!==TARGET_SCHEMA)fail("target_schema");
    if(target.transport_origin!=="STEGOS_NODE_OUTBOX"||target.required_profile!=="SV002:SelfCharacterization")fail("target_binding");
    if(target.credential_authority!=="TV/TVC"||target.credential_requirement!=="NONE"||target.github_token_runtime_authority!=="NONE"||target.execution_authority!=="NONE"||target.authority_effect!=="NONE_DISCOVERY_ONLY")fail("target_authority");
    if(target.state==="AWAITING_SOVEREIGN_INTR_INGRESS"){
      if(target.ingress_url!==null||target.runtime_ingress_observed!==false)fail("awaiting_target_exposes_ingress");
      return target;
    }
    if(target.state!=="CONFORMING_SOVEREIGN_INTR_INGRESS"||target.runtime_ingress_observed!==true)fail("target_state");
    var parsed=new URL(String(target.ingress_url||""),location.href);
    if(parsed.protocol!=="https:"||parsed.username||parsed.password||parsed.search||parsed.hash||!parsed.pathname.endsWith("/intr/materialization"))fail("target_url");
    return Object.assign({},target,{ingress_url:parsed.href});
  }

  function loadTarget(){
    return fetch(TARGET_URL,{method:"GET",cache:"no-store",credentials:"omit",headers:{Accept:"application/json"}})
      .then(function(r){if(!r.ok)fail("target_http_"+r.status);return r.json();})
      .then(validateTarget);
  }

  function validateRequest(request){
    if(!request||request.schema_version!=="stegverse.external_organization.interlock_request.v1"||request.request_class!=="EXTERNAL_ORGANIZATION_INTERACTION"||request.operation!==OPERATION||request.transport!=="InTr")fail("request_identity");
    if(request.authority_transfer!==false||request.sdk_mints_intr_receipt!==false||request.sdk_claims_delivery!==false)fail("request_authority");
    var b=request.bindings||{},m=request.payload&&request.payload.manifest;
    if(b.experiment_id!=="STEGVERSE-002-SELF-CHARACTERIZATION-001"||b.source_organization_id!=="StegVerse-SDK-Evaluator"||b.target_entity_id!=="StegVerse-002"||b.manifest_id!=="SDK-SV002-FIRST-SELF-CHARACTERIZATION-001")fail("request_bindings");
    if(!m||m.manifest_sha256!==b.manifest_sha256||m.operation!==OPERATION)fail("manifest_binding");
    return sha256Hex(canonical(request)).then(function(d){return {request:request,payload_hash:"sha256:"+d};});
  }

  function validateOutboxEntry(entry){
    if(!entry||entry.schema!==OUTBOX_SCHEMA||entry.state!=="LOCAL_OUTBOX_PENDING_NETWORK_DELIVERY")fail("outbox_entry");
    if(JSON.stringify(entry.destination)!==DESTINATION||entry.downstream_owner_ref!==OWNER)fail("outbox_destination");
    if(entry.request_grants_execution_authority!==false||entry.claim_or_fence_minted!==false||entry.credential_authority!=="TV/TVC"||entry.github_token_runtime_authority!=="NONE")fail("outbox_authority");
    var m=entry.materialization_request;
    if(!m||m.materialization_id!==entry.materialization_id||m.request_hash!==entry.request_hash)fail("outbox_materialization_binding");
    if(m.goal_task_id!==GOAL||m.cosv_task_vector!==COSV||m.invocation_count!==1)fail("goal_cosv_invocation_binding");
    return validateRequest(m.sv002_request).then(function(valid){
      if(valid.payload_hash!==m.payload_hash||valid.payload_hash!==entry.payload_hash)fail("exact_request_payload_hash");
      var body=Object.assign({},entry),claimed=body.outbox_entry_hash;delete body.outbox_entry_hash;
      return sha256Uri(body).then(function(actual){if(actual!==claimed)fail("outbox_hash");return entry;});
    });
  }

  function buildTrigger(entry){
    return validateOutboxEntry(entry).then(function(){
      var body={schema:TRIGGER_SCHEMA,transport_origin:"STEGOS_NODE_OUTBOX",node_id:entry.node_id,interlock_id:entry.interlock_id,outbox_entry_hash:entry.outbox_entry_hash,node_outbox_entry:entry,request_grants_execution_authority:false,claim_or_fence_minted:false,authority_effect:"NONE_TRIGGER_ONLY"};
      return sha256Uri(body).then(function(d){return Object.assign({},body,{trigger_sha256:d});});
    });
  }

  function validateIngressReceipt(receipt,entry,payloadSha){
    if(!receipt||receipt.schema!==INGRESS_RECEIPT_SCHEMA||receipt.state!=="INGRESS_ADMITTED")fail("ingress_receipt");
    var expected={
      goal_task_id:GOAL,cosv_task_vector:COSV,invocation_count:1,
      materialization_id:entry.materialization_id,request_hash:entry.request_hash,
      transport_intent_hash:entry.transport_intent_hash,payload_hash:entry.payload_hash,
      transport_origin:"STEGOS_NODE_OUTBOX",node_id:entry.node_id,interlock_id:entry.interlock_id,
      outbox_entry_hash:entry.outbox_entry_hash,transport_payload_sha256:payloadSha,
      exact_request_validated:true,write_once_persisted:true,runtime_execution_attempted:false,
      claim_or_fence_minted:false,credential_authority:"TV/TVC",github_token_runtime_authority:"NONE"
    };
    Object.keys(expected).forEach(function(k){if(canonical(receipt[k])!==canonical(expected[k]))fail("ingress_binding_"+k);});
    return receipt;
  }

  function postTrigger(target,entry){
    return buildTrigger(entry).then(function(trigger){
      var body=canonical(trigger);
      return sha256Hex(body).then(function(payloadSha){
        return fetch(target.ingress_url,{method:"POST",mode:"cors",cache:"no-store",credentials:"omit",headers:{"Content-Type":"application/json","X-StegVerse-Transport":"InTr","X-StegVerse-Transport-Origin":"STEGOS_NODE_OUTBOX","X-StegVerse-Payload-SHA256":payloadSha},body:body})
          .then(function(r){if(r.status!==202)fail("ingress_http_"+r.status);return r.json();})
          .then(function(receipt){return validateIngressReceipt(receipt,entry,payloadSha);})
          .then(function(receipt){
            if(root.StegVerseNodeContinuity&&typeof root.StegVerseNodeContinuity.recordStep==="function"){
              return root.StegVerseNodeContinuity.recordStep(CAPABILITY,"intr-admission","INTR_MATERIALIZATION_ADMITTED",receipt.request_hash).then(function(){return receipt;});
            }
            return receipt;
          });
      });
    });
  }

  function synchronizePending(){
    if(!root.StegVerseNodeContinuity||typeof root.StegVerseNodeContinuity.getIntrOutbox!=="function")return Promise.reject(new Error("StegVerse Node outbox API unavailable"));
    return Promise.all([loadTarget(),root.StegVerseNodeContinuity.getIntrOutbox()]).then(function(values){
      var target=values[0],entries=values[1].filter(function(e){return e&&e.state==="LOCAL_OUTBOX_PENDING_NETWORK_DELIVERY"&&JSON.stringify(e.destination)===DESTINATION&&e.downstream_owner_ref===OWNER;});
      if(entries.length>1)fail("more_than_one_pending_rerun_invocation");
      if(target.state!=="CONFORMING_SOVEREIGN_INTR_INGRESS")return {state:"AWAITING_SOVEREIGN_INTR_INGRESS",pending:entries.length,delivered:0,authority_effect:"NONE"};
      if(!entries.length)return {state:"NO_PENDING_RERUN_INVOCATION",pending:0,delivered:0,authority_effect:"NONE"};
      return postTrigger(target,entries[0]).then(function(receipt){return {state:"SYNC_ATTEMPT_COMPLETE",pending:1,delivered:1,ingress_receipt:receipt,authority_effect:"NONE"};});
    });
  }

  function attempt(){if(navigator.onLine===false)return Promise.resolve(null);return synchronizePending().catch(function(){return null;});}
  document.addEventListener("DOMContentLoaded",function(){setTimeout(attempt,0);});
  window.addEventListener("online",attempt);
  root.StegVerseSV002SelfCharacterizationInTrSync=Object.freeze({validateTarget:validateTarget,validateOutboxEntry:validateOutboxEntry,buildTrigger:buildTrigger,validateIngressReceipt:validateIngressReceipt,synchronizePending:synchronizePending,attempt:attempt,authority_effect:"NONE"});
})(typeof globalThis!=="undefined"?globalThis:window);
