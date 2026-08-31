"use strict";

/*
 * Root-scoped device-local Universal InTr ingress for the registered StegVerse Node.
 * Transport/admission only. It grants no global WorkerCoordinator, provider,
 * credential, routing, heartbeat, or downstream execution authority.
 */
var PROFILE_SCHEMA="stegverse.universal-intr-profiled-ingress/v1";
var TRIGGER_SCHEMA="stegos.node_intr_materialization_trigger.v1";
var OUTBOX_SCHEMA="stegos.node_intr_outbox_entry.v1";
var MATERIALIZATION_SCHEMA="stegverse.universal-intr-materialization-request/v1";
var INGRESS_SCHEMA="stegverse.device-kv-intr-materialization-ingress/v1";
var RESULT_REQUEST_SCHEMA="stegverse.device-kv.query-result-request/v1";
var RESULT_SCHEMA="stegverse.device-kv.query-result-delivery/v1";
var RESPONSE_SCHEMA="stegverse.device-kv.query-response/v1";
var DIRECTORY_PROJECTION_SCHEMA="stegverse.kv.portable-directory-projection/v1";
var DB_NAME="stegverse-device-local-intr-v1";
var DB_VERSION=1;
var REQUESTS="requests";
var FILES="kv_files";
var RESULTS="query_results";
var DEVICE_KV_DEST='{"boundary":"KV","subsystem":"KnowledgeVault:Interlock"}';
var DEVICE_KV_OWNER="StegVerse-Labs/continuity-vault-kit#79";
var HB_ANCHOR_EPOCH=32;
var HB_ANCHOR_UNIX_MS=1787511600000;
var HB_PERIOD_MS=10;
var HB_CHANNEL_COUNT=16;

function canon(v){
  if(v===null||typeof v!=="object") return JSON.stringify(v);
  if(Array.isArray(v)) return "["+v.map(canon).join(",")+"]";
  return "{"+Object.keys(v).sort().map(function(k){return JSON.stringify(k)+":"+canon(v[k]);}).join(",")+"}";
}
function bytesToHex(bytes){return Array.prototype.map.call(new Uint8Array(bytes),function(x){return x.toString(16).padStart(2,"0");}).join("");}
function shaHexBytes(bytes){return crypto.subtle.digest("SHA-256",bytes).then(bytesToHex);}
function shaUriBytes(bytes){return shaHexBytes(bytes).then(function(h){return "sha256:"+h;});}
function shaUri(v){return shaUriBytes(new TextEncoder().encode(canon(v)));}
function json(status,value){return new Response(JSON.stringify(value),{status:status,headers:{"Content-Type":"application/json","Cache-Control":"no-store","X-StegVerse-Runtime":"DEVICE_LOCAL_INTR"}});}
function require(ok,reason){if(!ok) throw new Error(reason);}
function openDb(){
  return new Promise(function(resolve,reject){
    var r=indexedDB.open(DB_NAME,DB_VERSION);
    r.onupgradeneeded=function(){
      var db=r.result;
      if(!db.objectStoreNames.contains(REQUESTS)) db.createObjectStore(REQUESTS,{keyPath:"materialization_id"});
      if(!db.objectStoreNames.contains(FILES)) db.createObjectStore(FILES,{keyPath:"key"});
      if(!db.objectStoreNames.contains(RESULTS)) db.createObjectStore(RESULTS,{keyPath:"materialization_id"});
    };
    r.onsuccess=function(){resolve(r.result);};
    r.onerror=function(){reject(r.error||new Error("device_local_intr_db_open_failed"));};
  });
}
function get(store,key){
  return openDb().then(function(db){return new Promise(function(resolve,reject){
    var tx=db.transaction(store,"readonly"),r=tx.objectStore(store).get(key);
    r.onsuccess=function(){resolve(r.result||null);};r.onerror=function(){reject(r.error);};tx.oncomplete=function(){db.close();};
  });});
}
function getAll(store){
  return openDb().then(function(db){return new Promise(function(resolve,reject){
    var tx=db.transaction(store,"readonly"),r=tx.objectStore(store).getAll();
    r.onsuccess=function(){resolve(r.result||[]);};r.onerror=function(){reject(r.error);};tx.oncomplete=function(){db.close();};
  });});
}
function putOnce(store,key,value){
  return openDb().then(function(db){return new Promise(function(resolve,reject){
    var tx=db.transaction(store,"readwrite"),s=tx.objectStore(store),r=s.get(key);
    r.onsuccess=function(){
      if(r.result&&canon(r.result)!==canon(value)){tx.abort();reject(new Error("write_once_collision:"+store));return;}
      if(!r.result)s.add(value);
    };
    r.onerror=function(){reject(r.error);};
    tx.oncomplete=function(){db.close();resolve(value);};
    tx.onabort=function(){db.close();};
  });});
}
function put(store,value){
  return openDb().then(function(db){return new Promise(function(resolve,reject){
    var tx=db.transaction(store,"readwrite");tx.objectStore(store).put(value);
    tx.oncomplete=function(){db.close();resolve(value);};tx.onerror=function(){db.close();reject(tx.error);};
  });});
}
function base64ToBytes(v){
  var raw=atob(v),out=new Uint8Array(raw.length);
  for(var i=0;i<raw.length;i++)out[i]=raw.charCodeAt(i);
  return out;
}
function bytesToBase64(bytes){
  var out="",chunk=0x8000;
  for(var i=0;i<bytes.length;i+=chunk)out+=String.fromCharCode.apply(null,bytes.subarray(i,Math.min(i+chunk,bytes.length)));
  return btoa(out);
}
function encodeHeartbeatId(epoch){
  var body=epoch.toString(36).toUpperCase().padStart(8,"0");
  return "HB-"+body;
}
function deriveReference(sampled){
  var elapsed=sampled-HB_ANCHOR_UNIX_MS,quanta=Math.floor(elapsed/HB_PERIOD_MS),offset=elapsed%HB_PERIOD_MS,epoch=HB_ANCHOR_EPOCH+quanta;
  return {heartbeat_epoch:epoch,heartbeat_id:encodeHeartbeatId(epoch),sampled_unix_ms:sampled,phase_offset_ms:offset,reference_frequency_hz:100,progression_dependency:"OSCILLATOR_ONLY"};
}
function deriveChannel(payloadHash){
  var slot=parseInt(payloadHash.charAt(22),16);
  return {channel_id:"HB:H1:P"+slot,channel_family:"H1_PHASE_SLOTS",frequency_ratio:1.0,phase_slot:slot,phase_slot_count:HB_CHANNEL_COUNT,phase_radians:Number((2*Math.PI*slot/HB_CHANNEL_COUNT).toFixed(12)),amplitude_ratio:1.0,derivation:"PAYLOAD_SHA256_FIRST64_MOD_16"};
}
function buildBinding(packetId,payloadHash){
  var reference=deriveReference(Date.now()),channel=deriveChannel(payloadHash);
  var body={schema:"stegverse.intr.hb-derived-carrier-binding/v1",carrier_profile:"stegverse.intr.hb-derived-carrier-profile/v1",fundamental_mode:"HB",packet_id:packetId,payload_hash:payloadHash,heartbeat_reference:reference,channel:channel,carrier_grants_admission_authority:false,carrier_grants_execution_authority:false,carrier_grants_credential_authority:false,carrier_grants_routing_authority:false,carrier_grants_transition_authority:false,carrier_grants_receiving_authority:false,credential_authority:"TV/TVC",authority_effect:"NONE_CARRIER_ONLY"};
  return shaUri(body).then(function(h){return Object.assign({},body,{binding_sha256:h});});
}
function buildCarrier(response,responseReceiptHash){
  var bytes=new TextEncoder().encode(canon(response));
  return shaUriBytes(bytes).then(function(payloadHash){
    var packetId="INTR-RETURN-"+payloadHash.slice(7,31);
    return Promise.all([buildBinding(packetId,payloadHash),shaHexBytes(bytes)]).then(function(parts){
      var binding=parts[0],packetSha=parts[1],ref=binding.heartbeat_reference,ch=binding.channel;
      return {
        response_payload_hash:payloadHash,
        signal:{
          schema:"stegverse.heartbeat-intr-derived-carrier/v1",
          intr:{packet_id:packetId,payload_hash:payloadHash,packet_encoding:"base64",packet_base64:bytesToBase64(bytes),packet_sha256:packetSha,packet_receipt_hash:String(responseReceiptHash).replace(/^sha256:/,"")},
          carrier:{carrier_profile:binding.carrier_profile,carrier_binding_sha256:binding.binding_sha256,heartbeat_epoch:ref.heartbeat_epoch,heartbeat_reference:ref.heartbeat_id,sampled_unix_ms:ref.sampled_unix_ms,intra_reference_phase_offset_ms:ref.phase_offset_ms,channel_id:ch.channel_id,phase_slots:ch.phase_slot_count,channel_slot:ch.phase_slot,channel_derivation:ch.derivation},
          carrier_binding:binding,
          authority:{heartbeat_grants_admission_authority:false,heartbeat_grants_execution_authority:false,heartbeat_grants_credential_authority:false,heartbeat_grants_routing_authority:false,heartbeat_grants_transition_authority:false,heartbeat_grants_receiving_authority:false,derived_carrier_grants_admission_authority:false,derived_carrier_grants_execution_authority:false,derived_carrier_grants_credential_authority:false,derived_carrier_grants_routing_authority:false,derived_carrier_grants_transition_authority:false,derived_carrier_grants_receiving_authority:false,credential_authority:"TV/TVC",authority_effect:"NONE_CARRIER_ONLY"}
        }
      };
    });
  });
}
function profile(){
  return {
    schema:PROFILE_SCHEMA,state:"ACTIVE_SOVEREIGN_INTR_INGRESS",protocol:"InTr",
    profile_path:"/intr/profile",materialization_path:"/intr/materialization",
    result_paths:["/intr/device-kv/result"],event_triggered:true,
    always_on_application_receiver_required:false,second_user_device_required:false,
    receiver_unavailable_disposition:"DURABLE_QUEUE_OR_EVENT_EPHEMERAL_MATERIALIZATION",
    supported_transport_origins:["STEGOS_NODE_OUTBOX"],
    profiles:["KV:KnowledgeVaultInterlock"],
    runtime_surface:"CURRENT_USER_IPHONE_SERVICE_WORKER",runtime_owner:"REGISTERED_STEGVERSE_NODE",
    tls_enabled:true,credential_authority:"TV/TVC",github_token_runtime_authority:"NONE",
    execution_authority:"NONE",authority_effect:"NONE_DISCOVERY_EVIDENCE_ONLY"
  };
}
function validateTrigger(payload){
  require(payload&&payload.schema===TRIGGER_SCHEMA,"node_trigger_schema_invalid");
  require(payload.transport_origin==="STEGOS_NODE_OUTBOX","node_trigger_origin_invalid");
  require(payload.request_grants_execution_authority===false&&payload.claim_or_fence_minted===false,"node_trigger_authority_forbidden");
  require(payload.authority_effect==="NONE_TRIGGER_ONLY","node_trigger_authority_effect_invalid");
  var entry=payload.node_outbox_entry;
  require(entry&&entry.schema===OUTBOX_SCHEMA&&entry.state==="LOCAL_OUTBOX_PENDING_NETWORK_DELIVERY","node_outbox_state_invalid");
  require(entry.credential_authority==="TV/TVC"&&entry.github_token_runtime_authority==="NONE","node_outbox_credential_boundary_invalid");
  require(entry.request_grants_execution_authority===false&&entry.claim_or_fence_minted===false,"node_outbox_authority_forbidden");
  var eb=Object.assign({},entry),eh=eb.outbox_entry_hash;delete eb.outbox_entry_hash;
  return shaUri(eb).then(function(actual){
    require(actual===eh,"node_outbox_entry_hash_mismatch");
    require(payload.node_id===entry.node_id&&payload.interlock_id===entry.interlock_id&&payload.outbox_entry_hash===eh,"node_trigger_binding_mismatch");
    var tb=Object.assign({},payload),th=tb.trigger_sha256;delete tb.trigger_sha256;
    return shaUri(tb).then(function(ta){
      require(ta===th,"node_trigger_hash_mismatch");
      var req=entry.materialization_request;
      require(req&&req.schema===MATERIALIZATION_SCHEMA&&req.state==="QUEUED_FOR_EVENT_EPHEMERAL_MATERIALIZATION","materialization_request_invalid");
      require(req.request_grants_execution_authority===false&&req.transport_grants_execution_authority===false&&req.claim_or_fence_minted===false,"materialization_authority_forbidden");
      require(req.credential_authority==="TV/TVC"&&req.github_token_runtime_authority==="NONE","materialization_credential_boundary_invalid");
      var rb=Object.assign({},req),rh=rb.request_hash;delete rb.request_hash;
      return shaUri(rb).then(function(ra){require(ra===rh,"materialization_request_hash_mismatch");return {entry:entry,request:req};});
    });
  });
}
function persistPortable(req){
  var payload=req.portable_payload;
  require(payload&&payload.schema==="stegverse.kv.portable-direct-source-inline-payload/v1","portable_payload_invalid");
  require(payload.credential_requirement==="NONE"&&payload.authority_effect==="NONE","portable_payload_authority_invalid");
  var rows=Array.isArray(payload.files)?payload.files:[];
  return rows.reduce(function(p,file,index){
    return p.then(function(){
      require(file&&typeof file.content_base64==="string","portable_file_content_missing");
      var bytes=base64ToBytes(file.content_base64);
      return shaUriBytes(bytes).then(function(actual){
        require(actual===file.sha256,"portable_file_sha256_mismatch");
        var key=String(payload.canonical_path||"").replace(/^\/+|\/+$/g,"")+"/"+String(file.name||("file-"+index));
        return putOnce(FILES,key,{key:key,directory_id:payload.directory_id,canonical_path:payload.canonical_path,name:file.name,media_type:file.media_type||"application/octet-stream",size_bytes:bytes.length,sha256:actual,content_base64:file.content_base64,admitted_at:new Date().toISOString(),credential_material_present:false,provider_operation_authorized:false,authority_effect:"NONE"});
      });
    });
  },Promise.resolve()).then(function(){return {state:"KV_MATERIALIZED_LOCAL",count:rows.length};});
}
function projectionFor(query){
  return getAll(FILES).then(function(rows){
    var selected=rows.filter(function(r){return r.directory_id===query.selector.directory_id&&r.canonical_path===query.selector.canonical_path;});
    if(query.record_class==="MY_KV_CONNECTION_HEALTH"){
      return {schema:"stegverse.kv.connection-health/v1",state:"KV_CONNECTION_HEALTH_READY",directory_id:query.selector.directory_id,canonical_path:query.selector.canonical_path,compatibility_state:"DEVICE_LOCAL_INTR_ACTIVE",entry_count:selected.length,credential_material_present:false,provider_operation_authorized:false,authority_effect:"NONE"};
    }
    return {schema:DIRECTORY_PROJECTION_SCHEMA,state:"KV_LISTED",directory_id:query.selector.directory_id,canonical_path:query.selector.canonical_path,entries:selected.map(function(r){return {name:r.name,kind:"file",media_type:r.media_type,size_bytes:r.size_bytes,sha256:r.sha256,modified_at:r.admitted_at};}),connection_health:{compatibility_state:"DEVICE_LOCAL_INTR_ACTIVE",entry_count:selected.length},credential_material_present:false,provider_operation_authorized:false,authority_effect:"NONE"};
  });
}
function persistQueryResult(req,entry){
  var q=req.kv_request;
  require(q&&q.schema_version==="kv.interlock.request.v1"&&q.operation==="REQUEST","kv_request_invalid");
  require(q.authority_ref==="stegos-node://"+entry.node_id,"kv_request_node_authority_ref_mismatch");
  return projectionFor(q).then(function(projection){
    var response={schema:RESPONSE_SCHEMA,state:"QUERY_COMPLETE",materialization_id:req.materialization_id,request_hash:req.request_hash,node_id:entry.node_id,query_request_id:q.request_id,record_class:q.record_class,directory_id:q.selector.directory_id,canonical_path:q.selector.canonical_path,projection:projection,credential_material_present:false,provider_operation_authorized:false,request_grants_authority:false,response_grants_authority:false,authority_effect:"NONE"};
    return shaUri(response).then(function(receiptHash){
      return put(RESULTS,{materialization_id:req.materialization_id,request_hash:req.request_hash,node_id:entry.node_id,response:response,response_receipt_hash:receiptHash});
    });
  });
}
function handleMaterialization(request){
  return request.arrayBuffer().then(function(buf){
    var raw=new Uint8Array(buf),claimed=String(request.headers.get("x-stegverse-payload-sha256")||"").toLowerCase();
    require(request.headers.get("x-stegverse-transport")==="InTr","transport_header_mismatch");
    require(request.headers.get("x-stegverse-transport-origin")==="STEGOS_NODE_OUTBOX","transport_origin_header_invalid");
    return shaHexBytes(raw).then(function(actual){
      require(actual===claimed,"request_payload_hash_mismatch");
      var payload=JSON.parse(new TextDecoder().decode(raw));
      return validateTrigger(payload).then(function(v){
        var entry=v.entry,req=v.request;
        require(JSON.stringify(req.destination)===DEVICE_KV_DEST&&req.downstream_owner_ref===DEVICE_KV_OWNER,"device_kv_destination_owner_mismatch");
        return putOnce(REQUESTS,req.materialization_id,{materialization_id:req.materialization_id,request_hash:req.request_hash,entry_hash:entry.outbox_entry_hash,request:req,admitted_at:new Date().toISOString()}).then(function(){
          var action=Promise.resolve({state:"INGRESS_ONLY"});
          if(req.portable_payload) action=persistPortable(req);
          else if(req.kv_request) action=persistQueryResult(req,entry);
          return action.then(function(){
            var carrier=req.carrier_binding||null;
            var receipt={schema:INGRESS_SCHEMA,state:"INGRESS_ADMITTED",materialization_id:req.materialization_id,request_hash:req.request_hash,transport_intent_hash:req.transport_intent_hash,payload_hash:req.payload_hash,transport_origin:"STEGOS_NODE_OUTBOX",transport_authorization_id:null,node_id:entry.node_id,interlock_id:entry.interlock_id,outbox_entry_hash:entry.outbox_entry_hash,transport_payload_sha256:actual,exact_request_validated:true,write_once_persisted:true,runtime_execution_attempted:false,consumer_dispatch_attempted:false,claim_or_fence_minted:false,g18_required:false,credential_authority:"TV/TVC",github_token_runtime_authority:"NONE",carrier_binding_present:!!carrier,carrier_binding_validated:!!carrier,carrier_profile:carrier?carrier.carrier_profile:"stegverse.intr.hb-derived-carrier-profile/v1",heartbeat_reference_epoch:carrier?carrier.heartbeat_reference.heartbeat_epoch:null,heartbeat_reference_id:carrier?carrier.heartbeat_reference.heartbeat_id:null,carrier_channel_id:carrier?carrier.channel.channel_id:null,carrier_binding_sha256:carrier?carrier.binding_sha256:null,carrier_binding_grants_authority:false,authority_effect:"NONE_INGRESS_ONLY",runtime_surface:"CURRENT_USER_IPHONE_SERVICE_WORKER",admitted_at:new Date().toISOString()};
            return json(202,receipt);
          });
        });
      });
    });
  }).catch(function(e){return json(400,{state:"DENIED",reason:String(e&&e.message||e),authority_effect:"NONE"});});
}
function handleResult(request){
  return request.json().then(function(q){
    require(q&&q.schema===RESULT_REQUEST_SCHEMA&&q.authority_effect==="NONE_RESULT_LOOKUP_ONLY","result_lookup_invalid");
    return get(RESULTS,q.materialization_id).then(function(row){
      require(row&&row.request_hash===q.request_hash&&row.node_id===q.node_id,"device_kv_result_not_ready");
      return buildCarrier(row.response,row.response_receipt_hash).then(function(carrier){
        return json(200,{schema:RESULT_SCHEMA,state:"RESULT_AVAILABLE",materialization_id:q.materialization_id,request_hash:q.request_hash,node_id:q.node_id,response:row.response,response_receipt_hash:row.response_receipt_hash,response_payload_hash:carrier.response_payload_hash,response_carrier_signal:carrier.signal,response_shared_hb_signal_ref:"device-local://"+q.materialization_id,response_shared_hb_signal_sha256:null,response_transported_on_hb_derived_carrier:true,exact_response_packet_recovered:true,credential_authority:"TV/TVC",github_token_runtime_authority:"NONE",credential_material_present:false,provider_operation_authorized:false,result_lookup_grants_authority:false,authority_effect:"NONE_RESULT_DELIVERY_ONLY"});
      });
    });
  }).catch(function(e){var reason=String(e&&e.message||e);return json(reason==="device_kv_result_not_ready"?400:400,{state:"NOT_READY",reason:reason,authority_effect:"NONE"});});
}
self.addEventListener("install",function(event){event.waitUntil(self.skipWaiting());});
self.addEventListener("activate",function(event){event.waitUntil(self.clients.claim());});
self.addEventListener("fetch",function(event){
  var u=new URL(event.request.url);
  if(u.origin!==self.location.origin)return;
  if(event.request.method==="GET"&&u.pathname==="/intr/profile"){event.respondWith(Promise.resolve(json(200,profile())));return;}
  if(event.request.method==="GET"&&u.pathname==="/intr/materialization/readiness"){event.respondWith(Promise.resolve(json(200,{state:"READY",runtime_surface:"CURRENT_USER_IPHONE_SERVICE_WORKER",transport:"InTr",credential_authority:"TV/TVC",execution_authority:"NONE",authority_effect:"NONE"})));return;}
  if(event.request.method==="POST"&&u.pathname==="/intr/materialization"){event.respondWith(handleMaterialization(event.request));return;}
  if(event.request.method==="POST"&&u.pathname==="/intr/device-kv/result"){event.respondWith(handleResult(event.request));return;}
});
