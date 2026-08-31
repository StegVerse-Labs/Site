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
    input.type="file";
    input.accept="application/json,.json,text/plain";
    input.hidden=true;
    input.addEventListener("change",function(){
      var file=input.files&&input.files[0];
      input.remove();
      if(!file){reject(new Error("installation receipt selection cancelled"));return;}
      file.text().then(function(text){
        var parsed;
        try{parsed=JSON.parse(text);}catch(_error){throw new Error("selected installation receipt is not valid JSON");}
        resolve(validateReceipt(parsed));
      }).catch(reject);
    },{once:true});
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
function importAndVerify(){
  return pickReceipt().then(buildProof).then(persistProof);
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
        resident_intr_activation_observed:false,
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
  localProof:function(){return readProof();}
};
}(typeof globalThis!=="undefined"?globalThis:this));
