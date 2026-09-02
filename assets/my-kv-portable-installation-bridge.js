(function(root){
"use strict";
if(!root || root.StegVerseKVInstallationBridge) return;

var STORAGE_KEY="stegverse.kv.portable-installation-proof.v1";

function canon(value){
  if(value===null||typeof value!=="object") return JSON.stringify(value);
  if(Array.isArray(value)) return "["+value.map(canon).join(",")+"]";
  return "{"+Object.keys(value).sort().map(function(k){return JSON.stringify(k)+":"+canon(value[k]);}).join(",")+"}";
}
function hex(buffer){
  return Array.prototype.map.call(new Uint8Array(buffer),function(x){return x.toString(16).padStart(2,"0");}).join("");
}
function sha256(value){
  return crypto.subtle.digest("SHA-256",new TextEncoder().encode(canon(value))).then(hex);
}
function sha256Bytes(bytes){
  return crypto.subtle.digest("SHA-256",bytes).then(function(d){return "sha256:"+hex(d);});
}
function bytesToBase64(bytes){
  var out="",chunk=0x8000;
  for(var i=0;i<bytes.length;i+=chunk) out+=String.fromCharCode.apply(null,bytes.subarray(i,Math.min(i+chunk,bytes.length)));
  return btoa(out);
}
function randomId(prefix){
  var bytes=new Uint8Array(16);crypto.getRandomValues(bytes);
  return prefix+"-"+Array.prototype.map.call(bytes,function(x){return x.toString(16).padStart(2,"0");}).join("");
}
function rejectSecretLike(value,path){
  path=path||"receipt";
  if(Array.isArray(value)){value.forEach(function(v,i){rejectSecretLike(v,path+"["+i+"]");});return;}
  if(!value||typeof value!=="object") return;
  Object.keys(value).forEach(function(key){
    var lower=key.toLowerCase();
    if(["password","secret","token","private_key","recovery_code","access_key"].some(function(part){return lower.indexOf(part)!==-1;})){
      throw new Error("secret-bearing installation receipt field prohibited at "+path+"."+key);
    }
    rejectSecretLike(value[key],path+"."+key);
  });
}
function validateReceipt(receipt){
  if(!receipt||typeof receipt!=="object") throw new Error("installation receipt JSON object required");
  rejectSecretLike(receipt);
  if(receipt.schema_version!=="1.1") throw new Error("unsupported KnowledgeVault installation receipt schema");
  if(typeof receipt.source!=="string"||receipt.source.indexOf("continuity-vault-kit:vault_template/KnowledgeVault")===-1) throw new Error("canonical KnowledgeVault source binding missing");
  if(typeof receipt.current_verified_source_tree_sha!=="string"||!/^[0-9a-f]{40}$/i.test(receipt.current_verified_source_tree_sha)) throw new Error("verified KnowledgeVault tree SHA missing");
  if(typeof receipt.destination!=="string"||!/\/KnowledgeVault$/.test(receipt.destination)) throw new Error("canonical KnowledgeVault destination missing");
  if(!receipt.verification||receipt.verification.full_recursive_source_path_presence!==true||receipt.verification.source_defined_directories_present!==true||receipt.verification.source_defined_files_present!==true||receipt.verification.full_template_parity!=="VALIDATED") throw new Error("full canonical KnowledgeVault installation parity not verified");
  if(receipt.authority_effect!=="NONE"||receipt.activation_effect!==false) throw new Error("installation receipt authority boundary mismatch");
  if(!receipt.source_census||!Number.isInteger(receipt.source_census.files)||receipt.source_census.files<1||!Number.isInteger(receipt.source_census.directories)||receipt.source_census.directories<1) throw new Error("KnowledgeVault source census missing");
  return receipt;
}
function pickReceipt(){
  return new Promise(function(resolve,reject){
    var input=document.createElement("input");
    var settled=false,openedAt=Date.now(),sawHidden=false,returnTimer=null;
    input.type="file";
    input.accept="application/json,.json,text/plain";
    input.hidden=true;

    function cleanup(){
      if(returnTimer!==null) clearTimeout(returnTimer);
      window.removeEventListener("focus",onFocus);
      document.removeEventListener("visibilitychange",onVisibility);
      input.removeEventListener("change",onChange);
      input.removeEventListener("cancel",onCancel);
      if(input.parentNode) input.remove();
    }
    function fail(message){
      if(settled) return;
      settled=true;cleanup();reject(new Error(message));
    }
    function acceptFile(file){
      if(settled) return;
      if(!file){fail("installation receipt selection cancelled; no installation state changed");return;}
      settled=true;cleanup();
      file.text().then(function(text){
        var parsed;
        try{parsed=JSON.parse(text);}catch(_error){throw new Error("selected installation receipt is not valid JSON");}
        return validateReceipt(parsed);
      }).then(resolve).catch(reject);
    }
    function onChange(){acceptFile(input.files&&input.files[0]);}
    function returnedWithoutSelection(){
      if(settled) return;
      if(returnTimer!==null) clearTimeout(returnTimer);
      returnTimer=setTimeout(function(){
        if(settled) return;
        var file=input.files&&input.files[0];
        if(file){acceptFile(file);return;}
        fail("installation receipt selection cancelled; no installation state changed");
      },2500);
    }
    function onCancel(){
      var file=input.files&&input.files[0];
      if(file){acceptFile(file);return;}
      returnedWithoutSelection();
    }
    function onFocus(){
      if(Date.now()-openedAt<500&&!sawHidden) return;
      returnedWithoutSelection();
    }
    function onVisibility(){
      if(document.visibilityState==="hidden"){sawHidden=true;return;}
      if(document.visibilityState==="visible"&&sawHidden) returnedWithoutSelection();
    }

    input.addEventListener("change",onChange);
    input.addEventListener("cancel",onCancel);
    window.addEventListener("focus",onFocus);
    document.addEventListener("visibilitychange",onVisibility);
    document.body.appendChild(input);
    input.click();
  });
}
function buildProof(receipt){
  return sha256(receipt).then(function(hash){
    var destinationKind=String(receipt.destination||"").split(":")[0]||"OWNER_CONTROLLED_STORAGE";
    return {
      schema:"stegverse.site.kv-portable-installation-proof/v1",
      source_tree_sha:receipt.current_verified_source_tree_sha,
      receipt_sha256:"sha256:"+hash,
      receipt_verified_utc:receipt.verified_utc||null,
      imported_at:new Date().toISOString(),
      destination_kind:destinationKind,
      full_template_parity:"VALIDATED",
      provider_specific_identifier_persisted:false,
      credential_material_present:false,
      kv_mutation_performed:false,
      interlock_activation_claimed:false,
      authority_effect:"NONE"
    };
  });
}
function persistProof(proof){
  localStorage.setItem(STORAGE_KEY,JSON.stringify(proof));
  return proof;
}
function readProof(){
  var raw=localStorage.getItem(STORAGE_KEY);
  if(!raw) return null;
  try{
    var proof=JSON.parse(raw);
    if(!proof||proof.schema!=="stegverse.site.kv-portable-installation-proof/v1"||proof.full_template_parity!=="VALIDATED"||proof.provider_specific_identifier_persisted!==false||proof.credential_material_present!==false||proof.authority_effect!=="NONE") return null;
    return proof;
  }catch(_error){return null;}
}
function materializeReceipt(receipt){
  var intr=root.StegVerseGeneratedInTr,node=root.StegVerseNodeContinuity,hb=root.StegVerseHBInTrCarrier,sync=root.StegVerseDeviceKVInTrSync;
  if(!intr||typeof intr.buildIntent!=="function"||typeof intr.buildMaterializationRequest!=="function") return Promise.reject(new Error("canonical DEVICE_KV InTr connector unavailable"));
  if(!node||typeof node.status!=="function"||typeof node.queueIntrMaterializationRequest!=="function") return Promise.reject(new Error("registered StegVerse Node InTr outbox unavailable"));
  if(!hb||typeof hb.buildBinding!=="function") return Promise.reject(new Error("canonical HB-derived InTr carrier unavailable"));
  var bytes=new TextEncoder().encode(canon(receipt));
  return Promise.all([node.status(),sha256Bytes(bytes)]).then(function(parts){
    var state=parts[0],fileHash=parts[1];
    if(!state||state.registered!==true) throw new Error("Register this device before admitting the installation receipt");
    var payload={
      schema:"stegverse.kv.portable-direct-source-inline-payload/v1",
      directory_id:"system",
      canonical_path:"_System",
      source_class:"OWNER_CONTROLLED_FILE",
      credential_requirement:"NONE",
      total_bytes:bytes.length,
      files:[{name:"installation.receipt.json",media_type:"application/json",size_bytes:bytes.length,sha256:fileHash,content_base64:bytesToBase64(bytes)}],
      authority_effect:"NONE"
    };
    var operationId=randomId("KV-INSTALLATION-RECEIPT");
    var payloadBytes=new TextEncoder().encode(intr.canonical(payload));
    return intr.buildIntent("device-kv",payloadBytes,"REQUEST",operationId).then(function(intent){
      return hb.buildBinding(intent.packet_id,intent.payload_hash).then(function(binding){
        return intr.buildMaterializationRequest("device-kv",intent,"inline://materialization_request.portable_payload",binding,{portable_payload:payload}).then(function(request){
          return node.queueIntrMaterializationRequest(request).then(function(){
            if(sync&&typeof sync.synchronizeMaterialization==="function"){
              return sync.synchronizeMaterialization(request.materialization_id).then(function(){
                return sync.getDeliveryReceipt(request.materialization_id);
              }).then(function(delivery){
                if(!delivery||(!delivery.local_ingress_observed&&!delivery.network_delivery_observed)) throw new Error("installation receipt DEVICE_KV admission not observed");
                return {materialization_id:request.materialization_id,request_hash:request.request_hash,payload_hash:request.payload_hash,delivery_receipt:delivery};
              });
            }
            return {materialization_id:request.materialization_id,request_hash:request.request_hash,payload_hash:request.payload_hash,delivery_receipt:null};
          });
        });
      });
    });
  });
}
function importAndVerify(){
  var selected;
  return pickReceipt().then(function(receipt){
    selected=receipt;
    return materializeReceipt(receipt);
  }).then(function(admission){
    return buildProof(selected).then(function(proof){
      proof.device_local_kv_materialization_observed=!!(admission&&admission.delivery_receipt);
      proof.device_local_materialization_id=admission&&admission.materialization_id||null;
      proof.kv_mutation_performed=proof.device_local_kv_materialization_observed;
      return persistProof(proof);
    });
  });
}

root.StegVerseKVInstallationBridge={
  bridge_kind:"PORTABLE_OWNER_SELECTED_CANONICAL_RECEIPT",
  live_resident_bridge:false,
  credential_authority:"TV/TVC",
  authority_effect:"NONE",
  installAndVerify:function(){
    return importAndVerify().then(function(proof){
      return {
        device_installed:true,
        cloud_installed:true,
        receipt_ref:proof.receipt_sha256,
        source_tree_sha:proof.source_tree_sha,
        portable_receipt_binding:true,
        resident_intr_activation_observed:proof.device_local_kv_materialization_observed===true,
        device_local_kv_materialization_observed:proof.device_local_kv_materialization_observed===true,
        device_local_materialization_id:proof.device_local_materialization_id||null,
        credential_material_present:false,
        authority_effect:"NONE"
      };
    });
  },
  verifyCloud:function(){
    return importAndVerify().then(function(proof){
      return {
        verified:true,
        receipt_ref:proof.receipt_sha256,
        source_tree_sha:proof.source_tree_sha,
        verification_mode:"OWNER_SELECTED_CANONICAL_INSTALLATION_RECEIPT",
        resident_intr_activation_observed:false,
        credential_material_present:false,
        authority_effect:"NONE"
      };
    });
  },
  existingInstallation:function(){
    var proof=readProof();
    if(!proof) return null;
    return {
      device_installed:true,
      cloud_installed:true,
      receipt_ref:proof.receipt_sha256,
      source_tree_sha:proof.source_tree_sha,
      portable_receipt_binding:true,
      reused_prior_validated_proof:true,
      current_cloud_observation:false,
      resident_intr_activation_observed:false,
      credential_material_present:false,
      authority_effect:"NONE"
    };
  },
  localProof:function(){return readProof();}
};
}(typeof globalThis!=="undefined"?globalThis:this));
