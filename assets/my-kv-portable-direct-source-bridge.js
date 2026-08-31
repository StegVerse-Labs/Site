(function(root){
"use strict";
if(!root || root.StegVerseKVDirectSourceBridge) return;

var DB_NAME="stegverse-kv-portable-source-v1";
var DB_VERSION=1;
var STORE="staged_files";
var MAX_INLINE_BYTES=4*1024*1024;

function canon(value){
  if(value===null||typeof value!=="object") return JSON.stringify(value);
  if(Array.isArray(value)) return "["+value.map(canon).join(",")+"]";
  return "{"+Object.keys(value).sort().map(function(k){return JSON.stringify(k)+":"+canon(value[k]);}).join(",")+"}";
}
function hex(buffer){
  return Array.prototype.map.call(new Uint8Array(buffer),function(x){return x.toString(16).padStart(2,"0");}).join("");
}
function sha256Bytes(buffer){
  return crypto.subtle.digest("SHA-256",buffer).then(function(d){return "sha256:"+hex(d);});
}
function sha256Json(value){
  return crypto.subtle.digest("SHA-256",new TextEncoder().encode(canon(value))).then(function(d){return "sha256:"+hex(d);});
}
function randomId(prefix){
  var bytes=new Uint8Array(16);crypto.getRandomValues(bytes);
  return prefix+"-"+Array.prototype.map.call(bytes,function(x){return x.toString(16).padStart(2,"0");}).join("");
}
function openDb(){
  return new Promise(function(resolve,reject){
    var req=indexedDB.open(DB_NAME,DB_VERSION);
    req.onupgradeneeded=function(){
      var db=req.result;
      if(!db.objectStoreNames.contains(STORE)) db.createObjectStore(STORE,{keyPath:"key"});
    };
    req.onsuccess=function(){resolve(req.result);};
    req.onerror=function(){reject(req.error||new Error("portable direct-source storage unavailable"));};
  });
}
function persistFiles(materializationId,files,metadata){
  return openDb().then(function(db){
    return new Promise(function(resolve,reject){
      var tx=db.transaction(STORE,"readwrite"),store=tx.objectStore(STORE);
      files.forEach(function(file,index){
        store.put({
          key:materializationId+":"+index,
          schema:"stegverse.kv.portable-direct-source-file/v1",
          materialization_id:materializationId,
          index:index,
          name:metadata[index].name,
          media_type:metadata[index].media_type,
          size_bytes:metadata[index].size_bytes,
          sha256:metadata[index].sha256,
          blob:file,
          credential_material_present:false,
          authority_effect:"NONE"
        });
      });
      tx.oncomplete=function(){db.close();resolve();};
      tx.onerror=function(){db.close();reject(tx.error||new Error("portable direct-source staging failed"));};
      tx.onabort=function(){db.close();};
    });
  });
}
function pickFiles(request){
  return new Promise(function(resolve,reject){
    var input=document.createElement("input");
    input.type="file";input.multiple=true;input.hidden=true;
    if(request.directory_id==="pictures") input.accept="image/*";
    else if(request.directory_id==="email") input.accept=".eml,.mbox,.json,.txt,message/rfc822";
    else input.accept="*/*";
    input.addEventListener("change",function(){
      var files=Array.prototype.slice.call(input.files||[]);
      input.remove();
      if(!files.length){reject(new Error("direct-source file selection cancelled"));return;}
      resolve(files);
    },{once:true});
    document.body.appendChild(input);input.click();
  });
}
function bytesToBase64(buffer){
  var bytes=new Uint8Array(buffer),chunk=0x8000,out="";
  for(var i=0;i<bytes.length;i+=chunk){
    out+=String.fromCharCode.apply(null,bytes.subarray(i,Math.min(i+chunk,bytes.length)));
  }
  return btoa(out);
}
function prepareFiles(files){
  var total=files.reduce(function(sum,file){return sum+file.size;},0);
  if(total<1||total>MAX_INLINE_BYTES) return Promise.reject(new Error("portable direct-source packet exceeds 4 MiB bounded inline transport limit"));
  return Promise.all(files.map(function(file){
    return file.arrayBuffer().then(function(buffer){
      return sha256Bytes(buffer).then(function(hash){
        return {
          metadata:{
            name:file.name||"unnamed",
            media_type:file.type||"application/octet-stream",
            size_bytes:file.size,
            last_modified:Number.isFinite(file.lastModified)?new Date(file.lastModified).toISOString():null,
            sha256:hash
          },
          content_base64:bytesToBase64(buffer)
        };
      });
    });
  })).then(function(rows){
    return {
      metadata:rows.map(function(row){return row.metadata;}),
      inline_files:rows.map(function(row){
        return {
          name:row.metadata.name,
          media_type:row.metadata.media_type,
          size_bytes:row.metadata.size_bytes,
          sha256:row.metadata.sha256,
          content_base64:row.content_base64
        };
      }),
      total_bytes:total
    };
  });
}
function buildTransport(request,prepared){
  var intr=root.StegVerseGeneratedInTr;
  if(!intr||typeof intr.buildIntent!=="function"||typeof intr.buildMaterializationRequest!=="function"){
    return Promise.reject(new Error("canonical generated DEVICE_KV InTr connector unavailable"));
  }
  var metadata=prepared.metadata;
  var inlinePayload={
    schema:"stegverse.kv.portable-direct-source-inline-payload/v1",
    directory_id:request.directory_id,
    canonical_path:request.canonical_path,
    source_class:"OWNER_CONTROLLED_FILE",
    credential_requirement:"NONE",
    total_bytes:prepared.total_bytes,
    files:prepared.inline_files,
    authority_effect:"NONE"
  };
  var manifest={
    schema:"stegverse.kv.portable-direct-source-staging/v1",
    directory_id:request.directory_id,
    canonical_path:request.canonical_path,
    source_class:"OWNER_CONTROLLED_FILE",
    access:"READ_ONLY",
    minimum_necessary:true,
    owner_authorized:true,
    credential_requirement:"NONE",
    files:metadata,
    canonical_kv_persistence_observed:false,
    provider_session_observed:false,
    authority_effect:"NONE"
  };
  var operationId=randomId("KV-PORTABLE-SOURCE");
  var payloadBytes=new TextEncoder().encode(intr.canonical(inlinePayload));
  return intr.buildIntent("device-kv",payloadBytes,"REQUEST",operationId).then(function(intent){
    if(!root.StegVerseHBInTrCarrier||typeof root.StegVerseHBInTrCarrier.buildBinding!=="function"){
      throw new Error("canonical HB-derived InTr carrier client unavailable");
    }
    return root.StegVerseHBInTrCarrier.buildBinding(intent.packet_id,intent.payload_hash).then(function(carrierBinding){
      return intr.buildMaterializationRequest(
        "device-kv",
        intent,
        "inline://materialization_request.portable_payload",
        carrierBinding,
        {portable_payload:inlinePayload}
      ).then(function(materializationRequest){
        return {manifest:manifest,intent:intent,request:materializationRequest};
      });
    });
  });
}

root.StegVerseKVDirectSourceBridge={
  bridge_kind:"PORTABLE_OWNER_CONTROLLED_FILE_STAGING",
  credential_authority:"TV/TVC",
  authority_effect:"NONE",
  connectDirectSource:function(request){
    if(!request||request.schema!=="stegverse.site.my-kv.direct-source-connect-request/v1") return Promise.reject(new Error("invalid direct-source request"));
    if(request.access!=="READ_ONLY"||request.minimum_necessary!==true||request.owner_authorized!==true||request.authority_effect!=="NONE") return Promise.reject(new Error("direct-source request authority boundary mismatch"));
    if(!root.StegVerseNodeContinuity||typeof root.StegVerseNodeContinuity.queueIntrMaterializationRequest!=="function") return Promise.reject(new Error("registered StegVerse Node InTr outbox unavailable"));
    return root.StegVerseNodeContinuity.status().then(function(node){
      if(!node.registered) throw new Error("Register this device before staging a direct source");
      return pickFiles(request);
    }).then(function(files){
      return prepareFiles(files).then(function(prepared){
        return buildTransport(request,prepared).then(function(built){
          return persistFiles(built.request.materialization_id,files,prepared.metadata).then(function(){
            return root.StegVerseNodeContinuity.queueIntrMaterializationRequest(built.request).then(function(entry){
              if(root.StegVerseDeviceKVInTrSync&&typeof root.StegVerseDeviceKVInTrSync.attempt==="function"){
                Promise.resolve(root.StegVerseDeviceKVInTrSync.attempt()).catch(function(){});
              }
              return {
                schema:"stegverse.site.my-kv.portable-direct-source-result/v1",
                state:"QUEUED_FOR_KV_ADMISSION",
                direct_source_required:true,
                source_class:"OWNER_CONTROLLED_FILE",
                credential_requirement:"NONE",
                credential_boundary:"NOT_REQUIRED_OWNER_CONTROLLED_SOURCE",
                directory_id:request.directory_id,
                canonical_path:request.canonical_path,
                materialization_id:built.request.materialization_id,
                request_hash:built.request.request_hash,
                payload_hash:built.request.payload_hash,
                staged_entries:prepared.metadata,
                local_outbox_state:entry.state,
                exact_bytes_staged_locally:true,
                canonical_kv_persistence_observed:false,
                provider_session_observed:false,
                credential_material_present:false,
                provider_operation_authorized:false,
                authority_effect:"NONE",
                message:"Exact owner-controlled files are staged on this device and queued for canonical KV admission."
              };
            });
          });
        });
      });
    });
  }
};
}(typeof globalThis!=="undefined"?globalThis:this));
