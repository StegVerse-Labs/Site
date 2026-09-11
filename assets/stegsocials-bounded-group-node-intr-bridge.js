(function(root,factory){
  "use strict";
  var api=factory(root||{});
  if(typeof module==="object"&&module.exports) module.exports=api;
  if(root) root.StegVerseStegSocialsBoundedGroupNodeInTrBridge=api;
}(typeof globalThis!=="undefined"?globalThis:this,function(root){
  "use strict";

  var RECORD_CLASS="STEGSOCIALS_BOUNDED_GROUP_USE_STATE_CAS";
  var CAS_SCHEMA="stegverse.site.stegsocials-bounded-group-kv-conditional-write/v1";
  var RECEIPT_SCHEMA="stegverse.device-kv.my-kv-n-resident-receipt/v1";
  var OBSERVATION_SCHEMA="stegverse.site.stegsocials-bounded-group-node-intr-observation/v1";
  var WORKER_URL="/assets/my-kv-n-device-kv-receiver.js";
  var WORKER_SCOPE="/assets/my-kv-n-runtime/";
  var PATH_ROOT="03_Records/StegSocials/PostGroupState/";

  function requireValue(ok,message){if(!ok)throw new Error("FAIL_CLOSED: "+message);}
  function canonical(v){
    var intr=root.StegVerseGeneratedInTr;
    requireValue(intr&&typeof intr.canonical==="function","canonical generated DEVICE_KV connector unavailable");
    return intr.canonical(v);
  }
  function randomId(prefix){
    var bytes=new Uint8Array(16);
    requireValue(root.crypto&&typeof root.crypto.getRandomValues==="function","crypto RNG unavailable");
    root.crypto.getRandomValues(bytes);
    return prefix+"-"+Array.prototype.map.call(bytes,function(x){return x.toString(16).padStart(2,"0");}).join("");
  }
  function bytesToBase64(bytes){var out="",chunk=0x8000;for(var i=0;i<bytes.length;i+=chunk)out+=String.fromCharCode.apply(null,bytes.subarray(i,Math.min(i+chunk,bytes.length)));return btoa(out);}
  function shaUriBytes(bytes){
    requireValue(root.crypto&&root.crypto.subtle,"crypto digest unavailable");
    return root.crypto.subtle.digest("SHA-256",bytes).then(function(d){return "sha256:"+Array.prototype.map.call(new Uint8Array(d),function(x){return x.toString(16).padStart(2,"0");}).join("");});
  }
  function shaUri(value){return shaUriBytes(new TextEncoder().encode(canonical(value)));}
  function rejectSensitive(value,path){
    path=path||"value";
    if(Array.isArray(value)){value.forEach(function(v,i){rejectSensitive(v,path+"["+i+"]");});return;}
    if(!value||typeof value!=="object")return;
    Object.keys(value).forEach(function(key){
      var lower=String(key).toLowerCase(),child=value[key];
      if(lower==="credential_material_present"){requireValue(child===false,"credential sentinel invalid at "+path+"."+key);return;}
      var forbidden=["password","secret","token","access_token","refresh_token","private_key","skap_credential_ref"];
      requireValue(!forbidden.some(function(part){return lower===part||lower.indexOf(part)>=0;}),"credential field prohibited at "+path+"."+key);
      rejectSensitive(child,path+"."+key);
    });
  }
  function validateCas(request){
    requireValue(request&&request.schema===CAS_SCHEMA&&request.operation==="COMPARE_AND_SWAP","bounded-group CAS request invalid");
    requireValue(typeof request.canonical_path==="string"&&request.canonical_path.indexOf(PATH_ROOT)===0,"bounded-group CAS path invalid");
    requireValue(typeof request.group_id==="string"&&request.group_id,"bounded-group id required");
    requireValue(Number.isInteger(request.consumed_use_index)&&request.consumed_use_index>=1,"bounded-group use index invalid");
    requireValue(request.credential_material_present===false&&request.provider_operation_authorized===false,"bounded-group CAS credential/provider boundary invalid");
    requireValue(request.authority_effect==="NONE_STATE_TRANSITION_REQUEST_ONLY","bounded-group CAS authority boundary invalid");
    requireValue(request.publication_proof&&request.publication_proof.publication_proven===true&&request.publication_proof.session_state_destroyed===true,"proven publication and terminal destruction required");
    rejectSensitive(request,"cas_request");
    return JSON.parse(JSON.stringify(request));
  }
  function buildEnvelope(nodeId,request){
    var valid=validateCas(request),bytes=new TextEncoder().encode(canonical(valid));
    return shaUriBytes(bytes).then(function(payloadHash){
      return {
        query:{
          schema_version:"kv.interlock.request.v1",
          operation:"COMMIT_CANDIDATE",
          request_id:randomId("SITE-STEGSOCIALS-GROUP-CAS"),
          requester:{module:"Site",component:"StegSocialsBoundedGroupNodeInTrBridge"},
          purpose:"Transport an externally admitted bounded StegSocials post-group use-state transition to the existing resident DEVICE_KV CAS receiver after proven publication and terminal browser-session destruction.",
          record_class:RECORD_CLASS,
          requested_scope:["stegsocials_bounded_group_use_state_cas"],
          minimum_necessary_justification:"Persist exactly one already-admitted bounded post-group use-state transition; no credential material or provider authority is permitted.",
          authority_ref:"stegos-node://"+nodeId,
          disclosure_mode:"BOUNDED_CONTEXT",
          group_id:valid.group_id,
          consumed_use_index:valid.consumed_use_index,
          candidate_writeback:{candidate_type:RECORD_CLASS,requested_destination:valid.canonical_path,payload_ref:"data:application/json;base64,"+bytesToBase64(bytes),payload_sha256:payloadHash,payload_size_bytes:bytes.length},
          credential_material_present:false,
          provider_operation_authorized:false,
          relationship_mutation_authorized:false,
          request_grants_authority:false,
          carrier_grants_authority:false,
          authority_effect:"NONE_REQUEST_ONLY",
          activation_effect:false
        },
        cas_request:valid,
        payload_sha256:payloadHash,
        payload_size_bytes:bytes.length
      };
    });
  }
  function buildTrigger(entry){
    var body={schema:"stegos.node_intr_materialization_trigger.v1",transport_origin:"STEGOS_NODE_OUTBOX",node_id:entry.node_id,interlock_id:entry.interlock_id,outbox_entry_hash:entry.outbox_entry_hash,node_outbox_entry:entry,request_grants_execution_authority:false,claim_or_fence_minted:false,authority_effect:"NONE_TRIGGER_ONLY"};
    return shaUri(body).then(function(hash){return Object.assign({},body,{trigger_sha256:hash});});
  }
  function waitForActive(registration){
    if(registration.active)return Promise.resolve(registration.active);
    var worker=registration.installing||registration.waiting;
    requireValue(!!worker,"existing MyKV resident worker unavailable");
    return new Promise(function(resolve,reject){var timer=setTimeout(function(){reject(new Error("FAIL_CLOSED: existing MyKV resident worker activation timeout"));},5000);function check(){if(worker.state==="activated"){clearTimeout(timer);resolve(worker);}else if(worker.state==="redundant"){clearTimeout(timer);reject(new Error("FAIL_CLOSED: existing MyKV resident worker became redundant"));}}worker.addEventListener("statechange",check);check();});
  }
  function loadResidentWorker(){
    requireValue(root.navigator&&root.navigator.serviceWorker&&root.isSecureContext!==false,"resident service worker unavailable");
    return root.navigator.serviceWorker.register(WORKER_URL,{scope:WORKER_SCOPE}).then(waitForActive);
  }
  function dispatch(worker,trigger){
    return new Promise(function(resolve,reject){
      requireValue(typeof root.MessageChannel!=="undefined"||typeof MessageChannel!=="undefined","MessageChannel unavailable");
      var Channel=root.MessageChannel||MessageChannel,channel=new Channel(),timer=setTimeout(function(){reject(new Error("FAIL_CLOSED: resident bounded-group CAS response timeout"));},5000);
      channel.port1.onmessage=function(event){clearTimeout(timer);var data=event.data||{};if(!data.ok){reject(new Error("FAIL_CLOSED: "+String(data.reason||"resident bounded-group CAS denied")));return;}resolve(data.receipt);};
      worker.postMessage({type:"STEGVERSE_MY_KV_N_LOCAL_TRIGGER",trigger:trigger},[channel.port2]);
    });
  }
  function validateReceipt(receipt,materialization,nodeId,query){
    requireValue(receipt&&receipt.schema===RECEIPT_SCHEMA&&receipt.state==="RESULT_AVAILABLE","resident bounded-group receipt invalid");
    requireValue(receipt.materialization_id===materialization.materialization_id&&receipt.request_hash===materialization.request_hash&&receipt.node_id===nodeId,"resident bounded-group receipt binding mismatch");
    requireValue(receipt.record_class===RECORD_CLASS&&receipt.local_ingress_observed===true&&receipt.resident_materialization_observed===true,"resident bounded-group materialization evidence missing");
    requireValue(receipt.provider_execution_attempted===false&&receipt.credential_material_present===false&&receipt.provider_operation_authorized===false&&receipt.authority_effect==="NONE_RESULT_DELIVERY_ONLY","resident bounded-group authority boundary invalid");
    var response=receipt.response,result=response&&response.result;
    requireValue(response&&response.state==="QUERY_COMPLETE"&&response.query_request_id===query.request_id&&response.record_class===RECORD_CLASS,"resident bounded-group response invalid");
    requireValue(result&&result.state==="GROUP_USE_STATE_COMMITTED"&&result.exact_readback_verified===true,"resident bounded-group CAS commit/readback missing");
    requireValue(result.group_id===query.group_id&&result.consumed_use_index===query.consumed_use_index,"resident bounded-group CAS result binding mismatch");
    return JSON.parse(JSON.stringify(result));
  }
  function minimizeHbBinding(binding){
    return {
      packet_id:binding&&binding.packet_id||null,
      payload_hash:binding&&binding.payload_hash||null,
      signal_ref:binding&&binding.signal_ref||binding&&binding.heartbeat_ref||null,
      carrier_grants_authority:false,
      execution_authority:false,
      authority_effect:"NONE_CORRELATION_ONLY"
    };
  }
  function performObserved(request){
    var intr=root.StegVerseGeneratedInTr,hb=root.StegVerseHBInTrCarrier,node=root.StegVerseNodeContinuity;
    requireValue(intr&&typeof intr.buildIntent==="function"&&typeof intr.buildMaterializationRequest==="function","generated InTr transport unavailable");
    requireValue(hb&&typeof hb.buildBinding==="function","HB-derived carrier unavailable");
    requireValue(node&&typeof node.status==="function"&&typeof node.queueIntrMaterializationRequest==="function","registered StegVerse Node unavailable");
    return node.status().then(function(state){
      requireValue(state&&state.registered===true&&state.registration&&state.registration.node_id,"registered StegVerse Node required");
      var nodeId=state.registration.node_id;
      return buildEnvelope(nodeId,request).then(function(built){
        var query=built.query,bytes=new TextEncoder().encode(canonical(query));
        return intr.buildIntent("device-kv",bytes,"COMMIT_CANDIDATE",query.request_id).then(function(intent){
          return hb.buildBinding(intent.packet_id,intent.payload_hash).then(function(binding){
            requireValue(binding&&binding.authority_effect!=="ALLOW"&&binding.execution_authority!==true,"HB carrier may not grant authority");
            return intr.buildMaterializationRequest("device-kv",intent,"inline://materialization_request.kv_request",binding,{kv_request:query}).then(function(materialization){
              return node.queueIntrMaterializationRequest(materialization).then(function(entry){
                return Promise.all([loadResidentWorker(),buildTrigger(entry)]).then(function(values){return dispatch(values[0],values[1]);}).then(function(receipt){
                  var result=validateReceipt(receipt,materialization,nodeId,query);
                  return shaUri(receipt).then(function(receiptHash){
                    return {
                      schema:OBSERVATION_SCHEMA,
                      state:"LOCAL_NODE_INTR_DEVICE_KV_CAS_OBSERVED",
                      node_id:nodeId,
                      interlock_id:entry.interlock_id,
                      outbox_entry_hash:entry.outbox_entry_hash,
                      query_request_id:query.request_id,
                      packet_id:intent.packet_id,
                      payload_hash:intent.payload_hash,
                      materialization_id:materialization.materialization_id,
                      materialization_request_hash:materialization.request_hash,
                      hb_binding:minimizeHbBinding(binding),
                      resident_receipt_hash:receiptHash,
                      local_node_outbox_observed:true,
                      resident_materialization_observed:true,
                      external_intr_admission_observed:false,
                      external_intr_admission_receipt_ref:null,
                      cas_result:result,
                      credential_material_present:false,
                      provider_operation_authorized:false,
                      carrier_grants_authority:false,
                      authority_effect:"NONE_EVIDENCE_ONLY"
                    };
                  });
                });
              });
            });
          });
        });
      });
    });
  }
  function perform(request){return performObserved(request).then(function(observation){return observation.cas_result;});}

  return Object.freeze({
    bridge_kind:"STEGSOCIALS_BOUNDED_GROUP_REGISTERED_NODE_INTR_DEVICE_KV_ROUTE",
    commit:perform,
    commitObserved:performObserved,
    _test:Object.freeze({buildEnvelope:buildEnvelope,buildTrigger:buildTrigger,validateCas:validateCas,validateReceipt:validateReceipt,minimizeHbBinding:minimizeHbBinding,record_class:RECORD_CLASS,worker_url:WORKER_URL,worker_scope:WORKER_SCOPE,observation_schema:OBSERVATION_SCHEMA}),
    carrier_grants_authority:false,
    authority_effect:"NONE",
    activation_effect:false
  });
}));
