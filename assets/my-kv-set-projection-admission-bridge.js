(function(root,factory){
  "use strict";
  var api=factory(root||{});
  if(typeof module==="object"&&module.exports) module.exports=api;
  if(root) root.StegVerseMyKVSetProjectionAdmissionBridge=api;
}(typeof globalThis!=="undefined"?globalThis:this,function(root){
  "use strict";

  var ADMISSION_CLASS="MY_KV_INSTANCE_SET_PROJECTION_ADMISSION";
  var SET_SCHEMA="stegverse.kv.my-kv-set-projection/v1";
  var RESPONSE_SCHEMA="stegverse.device-kv.my-kv-set-projection-admission-response/v1";
  var DEST="_System/my-kv-set-projection.json";
  var WORKER_URL="/assets/my-kv-set-projection-admission-receiver.js";
  var WORKER_SCOPE="/assets/my-kv-set-projection-admission-runtime/";
  var KV_DB="stegverse-device-local-intr-v1";
  var KV_FILES="kv_files";

  function requireValue(ok,message){if(!ok)throw new Error("FAIL_CLOSED: "+message);}
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
  function bytesToBase64(bytes){
    var out="",chunk=0x8000;
    for(var i=0;i<bytes.length;i+=chunk)out+=String.fromCharCode.apply(null,bytes.subarray(i,Math.min(i+chunk,bytes.length)));
    return btoa(out);
  }
  function shaUriBytes(bytes){
    requireValue(root.crypto&&root.crypto.subtle&&typeof root.crypto.subtle.digest==="function","crypto digest unavailable");
    return root.crypto.subtle.digest("SHA-256",bytes).then(function(d){return "sha256:"+Array.prototype.map.call(new Uint8Array(d),function(x){return x.toString(16).padStart(2,"0");}).join("");});
  }
  function shaUri(value){return shaUriBytes(new TextEncoder().encode(canonical(value)));}
  function rejectSensitive(value,path){
    path=path||"projection";
    if(Array.isArray(value)){value.forEach(function(v,i){rejectSensitive(v,path+"["+i+"]");});return;}
    if(!value||typeof value!=="object")return;
    Object.keys(value).forEach(function(key){
      var lower=String(key).toLowerCase();
      if(lower==="credential_material_included"||lower==="credential_material_present"){
        requireValue(value[key]===false,"credential sentinel must remain false at "+path+"."+key);return;
      }
      var forbidden=["password","secret","token","access_token","refresh_token","private_key","credential_material","skap_credential_ref","interlock_receipt_ref","intr_receipt_ref"];
      requireValue(!forbidden.some(function(part){return lower===part||lower.indexOf(part)>=0;}),"sensitive projection field prohibited at "+path+"."+key);
      rejectSensitive(value[key],path+"."+key);
    });
  }
  function validateProjection(projection,manager){
    manager=manager||root.StegVerseMyKVInstanceManager;
    requireValue(manager&&typeof manager.validateSetProjection==="function","canonical MyKV projection validator unavailable");
    var valid=manager.validateSetProjection(projection);
    requireValue(valid.schema===SET_SCHEMA&&valid.private_content_included===false&&valid.credential_material_included===false,"projection content boundary invalid");
    requireValue(valid.authority_effect==="NONE_STATUS_ONLY"&&valid.activation_effect===false,"projection authority boundary invalid");
    rejectSensitive(valid,"projection");
    return valid;
  }
  function buildEnvelope(nodeId,rawBytes,projection,manager){
    requireValue(rawBytes instanceof Uint8Array&&rawBytes.length>0,"raw projection bytes required");
    var valid=validateProjection(projection,manager);
    return shaUriBytes(rawBytes).then(function(payloadHash){
      return {
        query:{
          schema_version:"kv.interlock.request.v1",
          operation:"COMMIT_CANDIDATE",
          request_id:randomId("SITE-MY-KV-SET-ADMISSION"),
          requester:{module:"Site",component:"MyKVSetProjectionAdmission"},
          purpose:"Owner-mediated admission of an already-validated bounded MyKV set projection into this device-local KnowledgeVault.",
          record_class:ADMISSION_CLASS,
          requested_scope:["kv_set_projection_status_replace"],
          minimum_necessary_justification:"Persist only the bounded multi-instance status projection selected by the owner; no private KV content or credentials are permitted.",
          authority_ref:"stegos-node://"+nodeId,
          disclosure_mode:"BOUNDED_CONTEXT",
          kv_set_id:valid.kv_set_id,
          candidate_writeback:{
            candidate_type:"MY_KV_SET_PROJECTION_REPLACE",
            requested_destination:DEST,
            payload_ref:"data:application/json;base64,"+bytesToBase64(rawBytes),
            payload_sha256:payloadHash,
            payload_size_bytes:rawBytes.length
          },
          credential_material_present:false,
          provider_operation_authorized:false,
          relationship_mutation_authorized:false,
          request_grants_authority:false,
          authority_effect:"NONE_REQUEST_ONLY",
          activation_effect:false
        },
        validated_projection:valid,
        source_payload_sha256:payloadHash,
        source_size_bytes:rawBytes.length
      };
    });
  }
  function buildTrigger(entry){
    var body={schema:"stegos.node_intr_materialization_trigger.v1",transport_origin:"STEGOS_NODE_OUTBOX",node_id:entry.node_id,interlock_id:entry.interlock_id,outbox_entry_hash:entry.outbox_entry_hash,node_outbox_entry:entry,request_grants_execution_authority:false,claim_or_fence_minted:false,authority_effect:"NONE_TRIGGER_ONLY"};
    return shaUri(body).then(function(hash){return Object.assign({},body,{trigger_sha256:hash});});
  }
  // ACTIONS BY MANIFEST (.github data/task-registry-global-invariants.json semantics.actions_by_manifest): the admission
  // request is queued durably in the registered Node outbox; the outbox trigger is posted to the resident admission
  // receiver as an event-ephemeral materialization without awaiting a reply; the receiver writes the projection to the
  // canonical DEVICE_KV row DEST; the page reads that row exactly once and proves exact readback against the selected
  // bytes itself. A row that does not hold exactly these bytes is an actionable FAIL_CLOSED, never a wait.
  function postTrigger(trigger){
    if(!(root.navigator&&root.navigator.serviceWorker&&root.isSecureContext!==false&&typeof MessageChannel!=="undefined"))return Promise.resolve("resident service worker unavailable");
    return Promise.resolve().then(function(){return root.navigator.serviceWorker.register(WORKER_URL,{scope:WORKER_SCOPE});}).then(function(registration){
      var worker=registration&&(registration.active||registration.waiting||registration.installing);
      if(!worker||worker.state==="redundant")return "projection admission receiver registration has no worker";
      var channel=new MessageChannel();channel.port1.close();
      worker.postMessage({type:"STEGVERSE_MY_KV_SET_PROJECTION_ADMISSION_TRIGGER",trigger:trigger},[channel.port2]);
      return null;
    }).catch(function(e){return "projection admission receiver registration failed: "+String(e&&e.message||e);});
  }
  function lookupRowOnce(key){
    var idb=root.indexedDB;
    requireValue(idb&&typeof idb.open==="function","device-local IndexedDB unavailable");
    return new Promise(function(resolve,reject){
      var r=idb.open(KV_DB);
      // The page never creates or upgrades the canonical DEVICE_KV store; an absent store is an absent row.
      r.onupgradeneeded=function(){r.transaction.abort();};
      r.onerror=function(event){if(r.error&&r.error.name==="AbortError"){if(event&&event.preventDefault)event.preventDefault();resolve(null);return;}reject(r.error||new Error("FAIL_CLOSED: DEVICE_KV store open failed"));};
      r.onsuccess=function(){
        var db=r.result;
        if(!db.objectStoreNames.contains(KV_FILES)){db.close();resolve(null);return;}
        var tx=db.transaction(KV_FILES,"readonly"),get=tx.objectStore(KV_FILES).get(key),row=null;
        get.onsuccess=function(){row=get.result||null;};
        tx.oncomplete=function(){db.close();resolve(row);};
        tx.onerror=function(){db.close();reject(tx.error||new Error("FAIL_CLOSED: DEVICE_KV row lookup failed"));};
        tx.onabort=function(){db.close();reject(tx.error||new Error("FAIL_CLOSED: DEVICE_KV row lookup aborted"));};
      };
    });
  }
  function resultNotMaterialized(lookup,detail){var p="DEVICE_KV_RESULT_NOT_YET_MATERIALIZED",e=new Error("FAIL_CLOSED: "+p+(detail?": "+detail:""));e.actionable_disposition={failure_code:p,failed_predicate:p,required_evidence_or_repair:"the resident MyKV set-projection admission receiver materializes the durably queued request "+lookup.materialization_id+" so that "+DEST+" holds exactly the selected projection bytes",retry_entrypoint:"my-kv-instances.html",owning_existing_goal:"STEGVERSE-WORKSPACE-ANY-DEVICE-KV-SURFACE-001",next_attempt:"the next action on this page queues a new request and looks its result up once; nothing waits"};e.materialization_id=lookup.materialization_id;return e;}
  function rowHoldsProjection(row,sourceHash,sourceSize,contentBase64){
    return !!(row&&row.key===DEST&&row.sha256===sourceHash&&row.size_bytes===sourceSize&&row.content_base64===contentBase64);
  }
  function readbackResponse(row,materialization,nodeId,query,valid){
    requireValue(row.credential_material_present===false&&row.provider_operation_authorized===false&&row.relationship_mutation_authorized===false&&row.authority_effect==="NONE","projection admission row authority boundary invalid");
    var response={schema:RESPONSE_SCHEMA,state:"PROJECTION_ADMITTED",materialization_id:materialization.materialization_id,request_hash:materialization.request_hash,node_id:nodeId,request_id:query.request_id,record_class:ADMISSION_CLASS,canonical_path:DEST,kv_set_id:valid.kv_set_id,instance_count:valid.instance_count,projection_sha256:row.sha256,size_bytes:row.size_bytes,exact_readback_verified:true,exact_readback_observer:"SITE_PAGE_SINGLE_LOOKUP",private_content_included:false,credential_material_included:false,credential_material_present:false,provider_operation_authorized:false,relationship_mutation_authorized:false,request_grants_authority:false,response_grants_authority:false,authority_effect:"NONE",activation_effect:false};
    requireValue(response.exact_readback_verified===true&&response.authority_effect==="NONE"&&response.activation_effect===false,"projection admission response authority invalid");
    return clone(response);
  }
  function perform(rawBytes,projection,manager){
    var intr=root.StegVerseGeneratedInTr,hb=root.StegVerseHBInTrCarrier,node=root.StegVerseNodeContinuity;
    requireValue(intr&&typeof intr.buildIntent==="function"&&typeof intr.buildMaterializationRequest==="function","generated InTr transport unavailable");
    requireValue(hb&&typeof hb.buildBinding==="function","HB-derived carrier unavailable");
    requireValue(node&&typeof node.status==="function"&&typeof node.queueIntrMaterializationRequest==="function","registered StegVerse Node unavailable");
    return node.status().then(function(state){
      requireValue(state&&state.registered===true&&state.registration&&state.registration.node_id,"Register this device before admitting a KV-set projection");
      var nodeId=state.registration.node_id;
      return buildEnvelope(nodeId,rawBytes,projection,manager).then(function(built){
        var query=built.query,bytes=new TextEncoder().encode(canonical(query));
        return intr.buildIntent("device-kv",bytes,"COMMIT_CANDIDATE",query.request_id).then(function(intent){
          return hb.buildBinding(intent.packet_id,intent.payload_hash).then(function(binding){
            return intr.buildMaterializationRequest("device-kv",intent,"inline://materialization_request.kv_request",binding,{kv_request:query}).then(function(materialization){
              return node.queueIntrMaterializationRequest(materialization).then(function(entry){
                var contentBase64=query.candidate_writeback.payload_ref.slice("data:application/json;base64,".length);
                return buildTrigger(entry).then(postTrigger).then(function(detail){
                  return lookupRowOnce(DEST).then(function(row){
                    if(!rowHoldsProjection(row,built.source_payload_sha256,built.source_size_bytes,contentBase64))throw resultNotMaterialized({materialization_id:materialization.materialization_id,request_hash:materialization.request_hash},detail);
                    return readbackResponse(row,materialization,nodeId,query,built.validated_projection);
                  });
                });
              });
            });
          });
        });
      });
    });
  }
  function admitFile(file){
    requireValue(file&&typeof file.arrayBuffer==="function","owner-selected projection file required");
    return file.arrayBuffer().then(function(buffer){
      var bytes=new Uint8Array(buffer),parsed;
      try{parsed=JSON.parse(new TextDecoder().decode(bytes));}catch(_){throw new Error("FAIL_CLOSED: selected projection JSON invalid");}
      return perform(bytes,parsed).then(function(response){return {persisted:true,state:"KV_SET_PROJECTION_ADMITTED",message:"KV-set projection admitted to resident DEVICE_KV with exact readback.",response:response};});
    });
  }

  return Object.freeze({
    bridge_kind:"DEVICE_KV_MY_KV_SET_PROJECTION_ADMISSION",
    admitFile:admitFile,
    admitBytes:function(bytes,projection,manager){return perform(bytes,projection,manager);},
    _test:Object.freeze({validateProjection:validateProjection,buildEnvelope:buildEnvelope,buildTrigger:buildTrigger,record_class:ADMISSION_CLASS,destination:DEST}),
    authority_effect:"NONE",
    activation_effect:false
  });
}));
