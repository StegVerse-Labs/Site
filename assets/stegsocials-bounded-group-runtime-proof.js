(function(root,factory){
  "use strict";
  var api=factory(root||{});
  if(typeof module==="object"&&module.exports) module.exports=api;
  if(root) root.StegVerseStegSocialsBoundedGroupRuntimeProof=api;
}(typeof globalThis!=="undefined"?globalThis:this,function(root){
  "use strict";

  var DB_NAME="stegverse-device-local-intr-v1";
  var DB_VERSION=1;
  var STORE="kv_files";
  var PATH_ROOT="03_Records/StegSocials/PostGroupState/";
  var CAS_SCHEMA="stegverse.site.stegsocials-bounded-group-kv-conditional-write/v1";
  var OBSERVATION_SCHEMA="stegverse.site.stegsocials-bounded-group-node-intr-observation/v1";
  var PROOF_SCHEMA="stegverse.site.stegsocials-bounded-group-runtime-observation/v1";
  var GOAL_TASK_ID="SS-KV-SKAP-SOCIAL-RELEASE-001";
  var COSV_ID="60000000102000";

  function requireValue(ok,message){if(!ok)throw new Error("FAIL_CLOSED: "+message);}
  function bytesToHex(bytes){return Array.prototype.map.call(new Uint8Array(bytes),function(x){return x.toString(16).padStart(2,"0");}).join("");}
  function base64ToBytes(value){
    requireValue(typeof root.atob==="function","base64 decoder unavailable");
    var raw=root.atob(value),out=new Uint8Array(raw.length);
    for(var i=0;i<raw.length;i++)out[i]=raw.charCodeAt(i);
    return out;
  }
  function shaUriBytes(bytes){requireValue(root.crypto&&root.crypto.subtle,"WebCrypto unavailable");return root.crypto.subtle.digest("SHA-256",bytes).then(function(d){return "sha256:"+bytesToHex(d);});}
  function openDb(){return new Promise(function(resolve,reject){
    requireValue(root.indexedDB,"IndexedDB unavailable");
    var req=root.indexedDB.open(DB_NAME,DB_VERSION);
    req.onupgradeneeded=function(){var db=req.result;if(!db.objectStoreNames.contains(STORE))db.createObjectStore(STORE,{keyPath:"key"});};
    req.onsuccess=function(){resolve(req.result);};req.onerror=function(){reject(req.error||new Error("device_kv_open_failed"));};
  });}
  function readRow(path){
    requireValue(typeof path==="string"&&path.indexOf(PATH_ROOT)===0,"bounded-group path invalid");
    return openDb().then(function(db){return new Promise(function(resolve,reject){
      requireValue(db.objectStoreNames.contains(STORE),"canonical DEVICE_KV store unavailable");
      var tx=db.transaction(STORE,"readonly"),get=tx.objectStore(STORE).get(path);
      get.onsuccess=function(){resolve(get.result||null);};get.onerror=function(){reject(get.error||new Error("device_kv_read_failed"));};tx.oncomplete=function(){db.close();};
    });});
  }
  function verifyRow(row,expectedEtag,label){
    requireValue(row&&typeof row.content_base64==="string",label+" row missing");
    requireValue(row.sha256===expectedEtag,label+" etag mismatch");
    var bytes=base64ToBytes(row.content_base64);
    return shaUriBytes(bytes).then(function(actual){
      requireValue(actual===expectedEtag,label+" exact content hash mismatch");
      return {etag:expectedEtag,size_bytes:bytes.length,exact_content_hash_verified:true};
    });
  }
  function validateRequest(request){
    requireValue(request&&request.schema===CAS_SCHEMA&&request.operation==="COMPARE_AND_SWAP","CAS request invalid");
    requireValue(typeof request.canonical_path==="string"&&request.canonical_path.indexOf(PATH_ROOT)===0,"CAS path invalid");
    requireValue(/^sha256:[0-9a-f]{64}$/.test(String(request.expected_previous_etag||"")),"expected previous etag invalid");
    requireValue(/^sha256:[0-9a-f]{64}$/.test(String(request.next_state_etag||"")),"next state etag invalid");
    requireValue(request.publication_proof&&request.publication_proof.publication_proven===true,"publication proof required");
    requireValue(request.publication_proof.session_state_destroyed===true,"terminal browser destruction proof required");
    requireValue(request.credential_material_present===false&&request.provider_operation_authorized===false,"credential/provider boundary invalid");
    return JSON.parse(JSON.stringify(request));
  }
  function validateObservation(observation,request){
    requireValue(observation&&observation.schema===OBSERVATION_SCHEMA,"Node/InTr observation invalid");
    requireValue(observation.state==="LOCAL_NODE_INTR_DEVICE_KV_CAS_OBSERVED","Node/InTr observation state invalid");
    requireValue(observation.local_node_outbox_observed===true&&observation.resident_materialization_observed===true,"local materialization evidence missing");
    requireValue(observation.external_intr_admission_observed===false&&observation.external_intr_admission_receipt_ref===null,"external admission may not be inferred from local materialization");
    requireValue(observation.carrier_grants_authority===false&&observation.hb_binding&&observation.hb_binding.carrier_grants_authority===false,"HB authority drift");
    requireValue(observation.credential_material_present===false&&observation.provider_operation_authorized===false,"observation credential/provider authority drift");
    var result=observation.cas_result;
    requireValue(result&&result.group_id===request.group_id&&result.consumed_use_index===request.consumed_use_index,"CAS result binding mismatch");
    requireValue(result.previous_etag===request.expected_previous_etag&&result.persisted_etag===request.next_state_etag&&result.exact_readback_verified===true,"CAS result etag/readback mismatch");
    return observation;
  }
  function run(request){
    var valid=validateRequest(request),bridge=root.StegVerseStegSocialsBoundedGroupNodeInTrBridge;
    requireValue(bridge&&typeof bridge.commitObserved==="function","bounded-group Node/InTr observation bridge unavailable");
    return readRow(valid.canonical_path).then(function(preRow){return verifyRow(preRow,valid.expected_previous_etag,"pre-state");}).then(function(pre){
      return bridge.commitObserved(valid).then(function(observation){
        validateObservation(observation,valid);
        return readRow(valid.canonical_path).then(function(postRow){return verifyRow(postRow,valid.next_state_etag,"post-state");}).then(function(post){
          return {
            schema:PROOF_SCHEMA,
            state:"LOCAL_RUNTIME_PROOF_COMPLETE_EXTERNAL_INTR_ADMISSION_PENDING",
            goal_task_id:GOAL_TASK_ID,
            cosv_id:COSV_ID,
            observed_at:new Date().toISOString(),
            group_id:valid.group_id,
            consumed_use_index:valid.consumed_use_index,
            canonical_path:valid.canonical_path,
            publication_receipt_ref:valid.publication_proof.publication_receipt_ref||null,
            session_state_destroyed:true,
            node_id:observation.node_id,
            interlock_id:observation.interlock_id,
            outbox_entry_hash:observation.outbox_entry_hash,
            query_request_id:observation.query_request_id,
            packet_id:observation.packet_id,
            payload_hash:observation.payload_hash,
            materialization_id:observation.materialization_id,
            materialization_request_hash:observation.materialization_request_hash,
            resident_receipt_hash:observation.resident_receipt_hash,
            pre_state:pre,
            post_state:post,
            cas_result:observation.cas_result,
            local_node_outbox_observed:true,
            resident_materialization_observed:true,
            external_intr_admission_observed:false,
            external_intr_admission_receipt_ref:null,
            heartbeat_observation:observation.hb_binding,
            credential_material_present:false,
            provider_operation_authorized:false,
            carrier_grants_authority:false,
            authority_effect:"NONE_EVIDENCE_ONLY"
          };
        });
      });
    });
  }
  function parseFile(file){
    requireValue(file&&typeof file.text==="function","CAS request file required");
    return file.text().then(function(text){var parsed;try{parsed=JSON.parse(text);}catch(_){throw new Error("FAIL_CLOSED: CAS request JSON invalid");}return parsed;});
  }
  function downloadProof(proof,filename){
    requireValue(root.Blob&&root.URL&&typeof root.URL.createObjectURL==="function","browser download API unavailable");
    var blob=new root.Blob([JSON.stringify(proof,null,2)+"\n"],{type:"application/json"}),url=root.URL.createObjectURL(blob),a=root.document.createElement("a");
    a.href=url;a.download=filename||("stegsocials-runtime-proof-"+proof.group_id+"-use-"+proof.consumed_use_index+".json");a.click();setTimeout(function(){root.URL.revokeObjectURL(url);},0);
  }

  return Object.freeze({
    proof_schema:PROOF_SCHEMA,
    goal_task_id:GOAL_TASK_ID,
    cosv_id:COSV_ID,
    run:run,
    parseFile:parseFile,
    downloadProof:downloadProof,
    _test:Object.freeze({validateRequest:validateRequest,validateObservation:validateObservation,verifyRow:verifyRow,readRow:readRow}),
    external_intr_admission_inferred:false,
    authority_effect:"NONE"
  });
}));
