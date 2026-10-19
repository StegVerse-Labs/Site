(function(root,factory){
  "use strict";
  var api=factory(root||{});
  if(typeof module==="object"&&module.exports) module.exports=api;
  if(root) root.StegVerseMyKVInstanceBridge=api;
}(typeof globalThis!=="undefined"?globalThis:this,function(root){
  "use strict";

  var SET_CLASS="MY_KV_INSTANCE_SET_PROJECTION";
  var PROVIDER_CLASS="MY_KV_PROVIDER_OPERATION_REQUEST";
  var RELATIONSHIP_CLASS="MY_KV_RELATIONSHIP_TRANSITION_REQUEST";
  var SET_SCHEMA="stegverse.kv.my-kv-set-projection/v1";
  var PROVIDER_SCHEMA="stegverse.site.my-kv.provider-operation-request/v1";
  var RELATIONSHIP_SCHEMA="stegverse.site.my-kv.relationship-transition-request/v1";
  var RESULT_DB="stegverse-my-kv-n-device-kv-v1";
  var RESULT_STORE="results";
  var WORKER_URL="/assets/my-kv-n-device-kv-receiver.js";
  var WORKER_SCOPE="/assets/my-kv-n-runtime/";

  function requireValue(ok,message){if(!ok) throw new Error("FAIL_CLOSED: "+message);}
  function clone(v){return JSON.parse(JSON.stringify(v));}
  function randomId(prefix){
    var bytes=new Uint8Array(16);
    requireValue(root.crypto&&typeof root.crypto.getRandomValues==="function","crypto RNG unavailable");
    root.crypto.getRandomValues(bytes);
    return prefix+"-"+Array.prototype.map.call(bytes,function(x){return x.toString(16).padStart(2,"0");}).join("");
  }
  function canonical(v){
    var intr=root.StegVerseGeneratedInTr;
    requireValue(intr&&typeof intr.canonical==="function","canonical generated DEVICE_KV connector unavailable");
    return intr.canonical(v);
  }
  function shaUri(v){
    requireValue(root.crypto&&root.crypto.subtle&&typeof root.crypto.subtle.digest==="function","crypto digest unavailable");
    var bytes=new TextEncoder().encode(canonical(v));
    return root.crypto.subtle.digest("SHA-256",bytes).then(function(d){return "sha256:"+Array.prototype.map.call(new Uint8Array(d),function(x){return x.toString(16).padStart(2,"0");}).join("");});
  }
  function buildEnvelope(nodeId,recordClass,request){
    return {
      schema_version:"kv.interlock.request.v1",
      operation:"REQUEST",
      request_id:randomId("SITE-MY-KV-N"),
      requester:{module:"Site",component:"MyKVInstanceManager"},
      purpose:recordClass===SET_CLASS
        ?"Read an already-admitted bounded KV instance-set projection."
        :recordClass===PROVIDER_CLASS
          ?"Transport a governed provider-operation request without executing provider authority."
          :"Transport a governed KV relationship-transition request without materializing relationship effects.",
      record_class:recordClass,
      requested_scope:recordClass===SET_CLASS?["kv_set_projection"]:["governance_request_status"],
      minimum_necessary_justification:"Transport only the bounded MyKV status/request object required by the selected operation.",
      authority_ref:"stegos-node://"+nodeId,
      disclosure_mode:"BOUNDED_CONTEXT",
      selector:recordClass===SET_CLASS?{kv_set_id:request.kv_set_id||"personal"}:null,
      my_kv_request:recordClass===SET_CLASS?null:clone(request),
      credential_material_present:false,
      provider_operation_authorized:false,
      relationship_mutation_authorized:false,
      authority_effect:"NONE_REQUEST_ONLY",
      activation_effect:false
    };
  }
  function validateInput(recordClass,request){
    requireValue(request&&typeof request==="object","MyKV transport request required");
    if(recordClass===SET_CLASS){
      requireValue(request.schema==="stegverse.site.my-kv.kv-set-status-request/v1","KV set status request schema invalid");
      requireValue(request.access==="READ_ONLY"&&request.authority_effect==="NONE","KV set read authority invalid");
      return;
    }
    if(recordClass===PROVIDER_CLASS){
      requireValue(request.schema===PROVIDER_SCHEMA,"provider request schema invalid");
      requireValue(request.governance_state==="PENDING_INTERLOCK_INTR","provider request must remain pending governance");
      requireValue(request.credential_material_present===false&&request.provider_operation_authorized===false,"provider authority boundary invalid");
      requireValue(request.authority_effect==="NONE_REQUEST_ONLY"&&request.activation_effect===false,"provider activation boundary invalid");
      return;
    }
    requireValue(request.schema===RELATIONSHIP_SCHEMA,"relationship request schema invalid");
    requireValue(request.governance_state==="PENDING_INTERLOCK_INTR","relationship request must remain pending governance");
    requireValue(request.data_moved===false&&request.replication_started===false&&request.ai_corpus_exposed===false,"relationship request claimed runtime effects");
    requireValue(request.relationship_mutation_authorized===false&&request.authority_effect==="NONE_REQUEST_ONLY"&&request.activation_effect===false,"relationship authority boundary invalid");
  }
  function buildTrigger(entry){
    var body={schema:"stegos.node_intr_materialization_trigger.v1",transport_origin:"STEGOS_NODE_OUTBOX",node_id:entry.node_id,interlock_id:entry.interlock_id,outbox_entry_hash:entry.outbox_entry_hash,node_outbox_entry:entry,request_grants_execution_authority:false,claim_or_fence_minted:false,authority_effect:"NONE_TRIGGER_ONLY"};
    return shaUri(body).then(function(hash){return Object.assign({},body,{trigger_sha256:hash});});
  }
  // ACTIONS BY MANIFEST (.github data/task-registry-global-invariants.json semantics.actions_by_manifest): the request is
  // queued durably in the registered Node outbox; the outbox trigger is posted to the resident receiver as an
  // event-ephemeral materialization without awaiting a reply; the receiver persists its result write-once in RESULT_DB
  // keyed by materialization_id; the page looks that result up exactly once. Absence is an actionable FAIL_CLOSED.
  function postResidentTrigger(trigger){
    if(!(root.navigator&&root.navigator.serviceWorker&&root.isSecureContext!==false&&typeof MessageChannel!=="undefined"))return Promise.resolve("resident service worker unavailable");
    return Promise.resolve().then(function(){return root.navigator.serviceWorker.register(WORKER_URL,{scope:WORKER_SCOPE});}).then(function(registration){
      var worker=registration&&(registration.active||registration.waiting||registration.installing);
      if(!worker||worker.state==="redundant")return "resident MyKV receiver registration has no worker";
      var channel=new MessageChannel();channel.port1.close();
      worker.postMessage({type:"STEGVERSE_MY_KV_N_LOCAL_TRIGGER",trigger:trigger},[channel.port2]);
      return null;
    }).catch(function(e){return "resident MyKV receiver registration failed: "+String(e&&e.message||e);});
  }
  function lookupResultOnce(key){
    var idb=root.indexedDB;
    requireValue(idb&&typeof idb.open==="function","device-local IndexedDB unavailable");
    return new Promise(function(resolve,reject){
      var r=idb.open(RESULT_DB);
      // The page never creates or upgrades the receiver's result store; an absent store is an absent result.
      r.onupgradeneeded=function(){r.transaction.abort();};
      r.onerror=function(event){if(r.error&&r.error.name==="AbortError"){if(event&&event.preventDefault)event.preventDefault();resolve(null);return;}reject(r.error||new Error("FAIL_CLOSED: MyKV result store open failed"));};
      r.onsuccess=function(){
        var db=r.result;
        if(!db.objectStoreNames.contains(RESULT_STORE)){db.close();resolve(null);return;}
        var tx=db.transaction(RESULT_STORE,"readonly"),get=tx.objectStore(RESULT_STORE).get(key),row=null;
        get.onsuccess=function(){row=get.result||null;};
        tx.oncomplete=function(){db.close();resolve(row);};
        tx.onerror=function(){db.close();reject(tx.error||new Error("FAIL_CLOSED: MyKV result lookup failed"));};
        tx.onabort=function(){db.close();reject(tx.error||new Error("FAIL_CLOSED: MyKV result lookup aborted"));};
      };
    });
  }
  function resultNotMaterialized(lookup,detail){var p="DEVICE_KV_RESULT_NOT_YET_MATERIALIZED",e=new Error("FAIL_CLOSED: "+p+(detail?": "+detail:""));e.actionable_disposition={failure_code:p,failed_predicate:p,required_evidence_or_repair:"the resident MyKV DEVICE_KV receiver materializes the durably queued request "+lookup.materialization_id+" from its Node outbox trigger and persists its result write-once",retry_entrypoint:"my-kv-instances.html",owning_existing_goal:"STEGVERSE-WORKSPACE-ANY-DEVICE-KV-SURFACE-001",next_attempt:"the next action on this page queues a new request and looks its result up once; nothing waits"};e.materialization_id=lookup.materialization_id;return e;}
  function validateResidentResult(row,built,nodeId,query,recordClass){
    requireValue(row&&row.materialization_id===built.materialization_id&&row.request_hash===built.request_hash&&row.node_id===nodeId,"resident DEVICE_KV result binding mismatch");
    var response=row.response;
    requireValue(response&&response.schema==="stegverse.device-kv.query-response/v1"&&response.state==="QUERY_COMPLETE","resident DEVICE_KV response invalid");
    requireValue(response.materialization_id===built.materialization_id&&response.request_hash===built.request_hash&&response.node_id===nodeId,"resident DEVICE_KV response binding mismatch");
    requireValue(response.record_class===recordClass&&response.query_request_id===query.request_id,"resident DEVICE_KV response request mismatch");
    requireValue(response.credential_material_present===false&&response.provider_operation_authorized===false&&response.request_grants_authority===false&&response.response_grants_authority===false&&response.authority_effect==="NONE","resident DEVICE_KV response authority invalid");
    return shaUri(response).then(function(hash){
      requireValue(hash===row.response_receipt_hash,"resident DEVICE_KV response receipt hash mismatch");
      return response.projection||response.result;
    });
  }
  function perform(recordClass,request){
    validateInput(recordClass,request);
    var intr=root.StegVerseGeneratedInTr,hb=root.StegVerseHBInTrCarrier,node=root.StegVerseNodeContinuity;
    requireValue(intr&&typeof intr.buildIntent==="function"&&typeof intr.buildMaterializationRequest==="function","generated InTr transport unavailable");
    requireValue(hb&&typeof hb.buildBinding==="function","HB-derived carrier unavailable");
    requireValue(node&&typeof node.status==="function"&&typeof node.queueIntrMaterializationRequest==="function","registered StegVerse Node unavailable");
    return node.status().then(function(state){
      requireValue(state&&state.registered===true&&state.registration&&state.registration.node_id,"Register this device before using MyKV transport");
      var nodeId=state.registration.node_id,query=buildEnvelope(nodeId,recordClass,request);
      var bytes=new TextEncoder().encode(canonical(query));
      return intr.buildIntent("device-kv",bytes,"REQUEST",query.request_id).then(function(intent){
        return hb.buildBinding(intent.packet_id,intent.payload_hash).then(function(binding){
          return intr.buildMaterializationRequest("device-kv",intent,"inline://materialization_request.kv_request",binding,{kv_request:query}).then(function(materialization){
            return node.queueIntrMaterializationRequest(materialization).then(function(entry){
              return buildTrigger(entry).then(postResidentTrigger).then(function(detail){
                var lookup={materialization_id:materialization.materialization_id,request_hash:materialization.request_hash};
                return lookupResultOnce(materialization.materialization_id).then(function(row){
                  if(!row)throw resultNotMaterialized(lookup,detail);
                  return validateResidentResult(row,materialization,nodeId,query,recordClass);
                });
              });
            });
          });
        });
      });
    });
  }

  var api={
    bridge_kind:"DEVICE_KV_MY_KV_N_RESIDENT_TRANSPORT",
    getKVSetProjection:function(request){
      return perform(SET_CLASS,request).then(function(projection){
        requireValue(projection&&projection.schema===SET_SCHEMA,"KV set projection schema invalid");
        requireValue(projection.private_content_included===false&&projection.credential_material_included===false,"KV set projection content boundary invalid");
        requireValue(projection.authority_effect==="NONE_STATUS_ONLY"&&projection.activation_effect===false,"KV set projection authority boundary invalid");
        return clone(projection);
      });
    },
    requestProviderOperation:function(request){
      return perform(PROVIDER_CLASS,request).then(function(result){
        requireValue(result&&result.request_id&&result.governance_state==="PENDING_INTERLOCK_INTR","provider request transport did not preserve pending state");
        requireValue(result.credential_material_present===false&&result.provider_operation_authorized===false,"provider request result authority invalid");
        return clone(result);
      });
    },
    requestRelationshipTransition:function(request){
      return perform(RELATIONSHIP_CLASS,request).then(function(result){
        requireValue(result&&result.request_id&&result.governance_state==="PENDING_INTERLOCK_INTR","relationship request transport did not preserve pending state");
        requireValue(result.data_moved===false&&result.replication_started===false&&result.ai_corpus_exposed===false,"relationship request result claimed runtime effects");
        return clone(result);
      });
    },
    _test:Object.freeze({buildEnvelope:buildEnvelope,validateInput:validateInput,buildTrigger:buildTrigger,classes:{set:SET_CLASS,provider:PROVIDER_CLASS,relationship:RELATIONSHIP_CLASS}}),
    authority_effect:"NONE",
    activation_effect:false
  };
  return Object.freeze(api);
}));