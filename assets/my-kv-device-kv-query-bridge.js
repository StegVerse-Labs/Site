(function(root){
"use strict";
if(!root) return;
var existingDirectoryBridge=root.StegVerseKVDirectoryBridge||null;
var existingHealthBridge=root.StegVerseKVConnectionHealthBridge||null;
var existingInstallationBridge=root.StegVerseKVInstallationStatusBridge||null;
if(existingDirectoryBridge&&typeof existingDirectoryBridge.listDirectory==="function"&&
   existingHealthBridge&&typeof existingHealthBridge.getDomainHealth==="function"&&
   existingInstallationBridge&&typeof existingInstallationBridge.getInstallationStatus==="function") return;

var RESULT_SCHEMA="stegverse.device-kv.query-result-delivery/v1";
var RESULT_REQUEST_SCHEMA="stegverse.device-kv.query-result-request/v1";
var DIRECTORY_CLASS="MY_KV_DIRECTORY_PROJECTION";
var HEALTH_CLASS="MY_KV_CONNECTION_HEALTH";
var INSTALLATION_CLASS="MY_KV_INSTALLATION_STATUS";
var DIRECTORY_PROJECTION_SCHEMA="stegverse.kv.portable-directory-projection/v1";
var INSTALLATION_PROJECTION_SCHEMA="stegverse.kv.installation-status-projection/v1";

function randomId(prefix){
  var bytes=new Uint8Array(16);crypto.getRandomValues(bytes);
  return prefix+"-"+Array.prototype.map.call(bytes,function(x){return x.toString(16).padStart(2,"0");}).join("");
}
function delay(ms){return new Promise(function(resolve){setTimeout(resolve,ms);});}
function hex(buffer){return Array.prototype.map.call(new Uint8Array(buffer),function(x){return x.toString(16).padStart(2,"0");}).join("");}
function sha256HexBytes(bytes){return crypto.subtle.digest("SHA-256",bytes).then(hex);}
function requireValue(ok,message){if(!ok) throw new Error("FAIL_CLOSED: "+message);}
function canonicalLookup(value){
  var intr=root.StegVerseGeneratedInTr;
  requireValue(intr&&typeof intr.canonical==="function","canonical generated DEVICE_KV connector unavailable");
  return intr.canonical(value);
}
function validateRequestShape(recordClass,request){
  requireValue(request&&typeof request==="object","My KV query request required");
  requireValue(request.access==="READ_ONLY","My KV query must remain READ_ONLY");
  requireValue(request.authority_effect==="NONE","My KV query authority boundary mismatch");
  if(recordClass===INSTALLATION_CLASS){
    requireValue(Object.keys(request).sort().join(",")==="access,authority_effect","My KV installation-status request fields invalid");
    return;
  }
  requireValue(typeof request.directory_id==="string"&&request.directory_id,"My KV directory id required");
  requireValue(typeof request.canonical_path==="string"&&request.canonical_path,"My KV canonical path required");
}
function queryRequest(nodeId,recordClass,request){
  if(recordClass===INSTALLATION_CLASS){
    return {
      schema_version:"kv.interlock.request.v1",
      operation:"REQUEST",
      request_id:randomId("SITE-MY-KV-INSTALLATION"),
      requester:{module:"Site",component:"MyKVOnboarding"},
      purpose:"Determine whether the current resident KnowledgeVault is a validated canonical installation.",
      record_class:INSTALLATION_CLASS,
      requested_scope:["installation_status"],
      minimum_necessary_justification:"Return only bounded installation status required for My KV Step 2.",
      authority_ref:"stegos-node://"+nodeId,
      disclosure_mode:"BOUNDED_CONTEXT",
      selector:{receipt_path:"_System/installation.receipt.json"}
    };
  }
  return {
    schema_version:"kv.interlock.request.v1",
    operation:"REQUEST",
    request_id:randomId("SITE-MY-KV-QUERY"),
    requester:{module:"Site",component:"MyKVDirectory"},
    purpose:recordClass===DIRECTORY_CLASS
      ?"List admitted metadata for the selected owner KnowledgeVault directory."
      :"Read bounded connection health for the selected owner KnowledgeVault directory.",
    record_class:recordClass,
    requested_scope:recordClass===DIRECTORY_CLASS?["entries","connection_health"]:["connection_health"],
    minimum_necessary_justification:recordClass===DIRECTORY_CLASS
      ?"Render only canonically admitted file metadata and bounded connection health."
      :"Render only the bounded connection-health state required by My KV.",
    authority_ref:"stegos-node://"+nodeId,
    disclosure_mode:"BOUNDED_CONTEXT",
    selector:{directory_id:request.directory_id,canonical_path:request.canonical_path}
  };
}
function postResult(target,lookup){
  var text=canonicalLookup(lookup),bytes=new TextEncoder().encode(text);
  return sha256HexBytes(bytes).then(function(payloadHash){
    return fetch(target.result_url,{
      method:"POST",mode:"cors",cache:"no-store",credentials:"omit",
      headers:{
        "Content-Type":"application/json",
        "X-StegVerse-Transport":"InTr",
        "X-StegVerse-Transport-Origin":"STEGOS_NODE_OUTBOX",
        "X-StegVerse-Payload-SHA256":payloadHash
      },
      body:text
    }).then(function(response){
      return response.json().catch(function(){return null;}).then(function(body){
        return {status:response.status,body:body};
      });
    });
  });
}
function pollResult(target,lookup,attempt){
  return postResult(target,lookup).then(function(result){
    if(result.status===200) return result.body;
    var reason=result.body&&result.body.reason;
    if(result.status===400&&reason==="device_kv_result_not_ready"&&attempt<20){
      return delay(250).then(function(){return pollResult(target,lookup,attempt+1);});
    }
    throw new Error("FAIL_CLOSED: DEVICE_KV query result unavailable"+(reason?": "+reason:""));
  });
}
function validateDelivery(delivery,built,nodeId,query){
  requireValue(delivery&&delivery.schema===RESULT_SCHEMA&&delivery.state==="RESULT_AVAILABLE","DEVICE_KV result schema/state invalid");
  requireValue(delivery.materialization_id===built.materialization_id,"DEVICE_KV result materialization mismatch");
  requireValue(delivery.request_hash===built.request_hash,"DEVICE_KV result request hash mismatch");
  requireValue(delivery.node_id===nodeId,"DEVICE_KV result Node mismatch");
  requireValue(delivery.credential_authority==="TV/TVC"&&delivery.github_token_runtime_authority==="NONE","DEVICE_KV result credential boundary mismatch");
  requireValue(delivery.credential_material_present===false&&delivery.provider_operation_authorized===false&&delivery.result_lookup_grants_authority===false,"DEVICE_KV result authority boundary mismatch");
  requireValue(delivery.authority_effect==="NONE_RESULT_DELIVERY_ONLY","DEVICE_KV result authority effect invalid");
  requireValue(delivery.response_transported_on_hb_derived_carrier===true&&delivery.exact_response_packet_recovered===true,"DEVICE_KV HB return proof missing");
  var response=delivery.response;
  requireValue(response&&response.schema==="stegverse.device-kv.query-response/v1"&&response.state==="QUERY_COMPLETE","DEVICE_KV response invalid");
  requireValue(response.materialization_id===built.materialization_id&&response.request_hash===built.request_hash,"DEVICE_KV response request binding mismatch");
  requireValue(response.node_id===nodeId,"DEVICE_KV response Node binding mismatch");
  requireValue(response.query_request_id===query.request_id,"DEVICE_KV response query id mismatch");
  requireValue(response.record_class===query.record_class,"DEVICE_KV response record class mismatch");
  if(query.record_class===INSTALLATION_CLASS){
    requireValue(response.receipt_path===query.selector.receipt_path,"DEVICE_KV installation receipt selector mismatch");
    requireValue(response.selector&&response.selector.receipt_path===query.selector.receipt_path,"DEVICE_KV installation selector projection mismatch");
    requireValue(response.directory_id==null&&response.canonical_path==null,"DEVICE_KV installation response leaked directory selector");
  }else{
    requireValue(response.directory_id===query.selector.directory_id&&response.canonical_path===query.selector.canonical_path,"DEVICE_KV response selector mismatch");
  }
  requireValue(response.credential_material_present===false&&response.provider_operation_authorized===false&&response.request_grants_authority===false&&response.response_grants_authority===false&&response.authority_effect==="NONE","DEVICE_KV response authority invalid");

  var hb=root.StegVerseHBInTrCarrier,intr=root.StegVerseGeneratedInTr;
  requireValue(hb&&typeof hb.recoverSignal==="function","canonical HB return recovery unavailable");
  requireValue(intr&&typeof intr.sha256Bytes==="function","canonical InTr hash helper unavailable");
  var signal=delivery.response_carrier_signal;
  return hb.recoverSignal(signal).then(function(bytes){
    return intr.sha256Bytes(bytes).then(function(actualPayloadHash){
      requireValue(actualPayloadHash===delivery.response_payload_hash,"DEVICE_KV recovered response payload hash mismatch");
      requireValue(signal.intr&&signal.intr.payload_hash===delivery.response_payload_hash,"DEVICE_KV carrier response payload binding mismatch");
      requireValue(signal.intr.packet_receipt_hash===String(delivery.response_receipt_hash||"").replace(/^sha256:/,""),"DEVICE_KV carrier receipt binding mismatch");
      requireValue(signal.authority&&signal.authority.authority_effect==="NONE_CARRIER_ONLY","DEVICE_KV carrier authority effect invalid");
      var decoded=new TextDecoder().decode(bytes),recovered;
      try{recovered=JSON.parse(decoded);}catch(_){throw new Error("FAIL_CLOSED: DEVICE_KV recovered response JSON invalid");}
      requireValue(intr.canonical(recovered)===intr.canonical(response),"DEVICE_KV recovered response identity mismatch");
      return response.projection;
    });
  });
}
function perform(recordClass,request){
  validateRequestShape(recordClass,request);
  var intr=root.StegVerseGeneratedInTr,hb=root.StegVerseHBInTrCarrier,node=root.StegVerseNodeContinuity,sync=root.StegVerseDeviceKVInTrSync;
  requireValue(intr&&typeof intr.buildIntent==="function"&&typeof intr.buildMaterializationRequest==="function","canonical generated DEVICE_KV connector unavailable");
  requireValue(hb&&typeof hb.buildBinding==="function","canonical HB-derived carrier client unavailable");
  requireValue(node&&typeof node.status==="function"&&typeof node.queueIntrMaterializationRequest==="function","registered StegVerse Node unavailable");
  requireValue(sync&&typeof sync.synchronizeMaterialization==="function"&&typeof sync.loadTarget==="function"&&typeof sync.getDeliveryReceipt==="function","DEVICE_KV sync/query transport unavailable");
  return node.status().then(function(state){
    requireValue(state&&state.registered===true&&state.registration&&state.registration.node_id,"Register this device before reading My KV");
    var nodeId=state.registration.node_id,query=queryRequest(nodeId,recordClass,request);
    var bytes=new TextEncoder().encode(intr.canonical(query));
    return intr.buildIntent("device-kv",bytes,"REQUEST",query.request_id).then(function(intent){
      return hb.buildBinding(intent.packet_id,intent.payload_hash).then(function(binding){
        return intr.buildMaterializationRequest(
          "device-kv",intent,"inline://materialization_request.kv_request",
          binding,{kv_request:query}
        ).then(function(materialization){
          return node.queueIntrMaterializationRequest(materialization).then(function(){
            return sync.synchronizeMaterialization(materialization.materialization_id).then(function(){
              return Promise.all([sync.getDeliveryReceipt(materialization.materialization_id),sync.loadTarget(recordClass)]);
            }).then(function(values){
              var deliveryReceipt=values[0],target=values[1];
              var localResultEligible=(recordClass===DIRECTORY_CLASS||recordClass===HEALTH_CLASS||recordClass===INSTALLATION_CLASS);requireValue(deliveryReceipt&&((deliveryReceipt.network_delivery_observed===true)||(localResultEligible&&deliveryReceipt.local_ingress_observed===true)),"DEVICE_KV query ingress delivery not observed");
              requireValue(target&&target.state==="CONFORMING_SOVEREIGN_INTR_INGRESS"&&target.runtime_ingress_observed===true,"conforming DEVICE_KV result target unavailable");
              requireValue(typeof target.result_url==="string"&&target.result_url,"DEVICE_KV result URL unavailable");
              var lookup={
                schema:RESULT_REQUEST_SCHEMA,
                materialization_id:materialization.materialization_id,
                request_hash:materialization.request_hash,
                node_id:nodeId,
                authority_effect:"NONE_RESULT_LOOKUP_ONLY"
              };
              return pollResult(target,lookup,0).then(function(result){
                return validateDelivery(result,materialization,nodeId,query);
              });
            });
          });
        });
      });
    });
  });
}

if(!(existingDirectoryBridge&&typeof existingDirectoryBridge.listDirectory==="function")){
  root.StegVerseKVDirectoryBridge=Object.freeze({
    bridge_kind:"DEVICE_KV_QUERY_RETURN",
    listDirectory:function(request){
      return perform(DIRECTORY_CLASS,request).then(function(projection){
        requireValue(projection&&projection.schema===DIRECTORY_PROJECTION_SCHEMA&&projection.state==="KV_LISTED","canonical KV directory projection invalid");
        requireValue(projection.canonical_path===request.canonical_path&&projection.directory_id===request.directory_id,"canonical KV directory projection path mismatch");
        requireValue(Array.isArray(projection.entries),"canonical KV directory entries invalid");
        requireValue(projection.credential_material_present===false&&projection.provider_operation_authorized===false&&projection.authority_effect==="NONE","canonical KV directory authority invalid");
        return {
          canonical_path:projection.canonical_path,
          entries:projection.entries,
          credential_material_present:false,
          provider_operation_authorized:false,
          authority_effect:"NONE"
        };
      });
    },
    authority_effect:"NONE"
  });
}

if(!(existingHealthBridge&&typeof existingHealthBridge.getDomainHealth==="function")){
  root.StegVerseKVConnectionHealthBridge=Object.freeze({
    bridge_kind:"DEVICE_KV_QUERY_RETURN",
    getDomainHealth:function(request){
      return perform(HEALTH_CLASS,request).then(function(health){
        requireValue(health&&health.canonical_path===request.canonical_path&&health.directory_id===request.directory_id,"canonical KV connection-health path mismatch");
        requireValue(typeof health.compatibility_state==="string","canonical KV connection-health state missing");
        requireValue(health.credential_material_present===false&&health.provider_operation_authorized===false&&health.authority_effect==="NONE","canonical KV connection-health authority invalid");
        return health;
      });
    },
    authority_effect:"NONE"
  });
}

if(!(existingInstallationBridge&&typeof existingInstallationBridge.getInstallationStatus==="function")){
  root.StegVerseKVInstallationStatusBridge=Object.freeze({
    bridge_kind:"DEVICE_KV_QUERY_RETURN",
    getInstallationStatus:function(){
      return perform(INSTALLATION_CLASS,{access:"READ_ONLY",authority_effect:"NONE"}).then(function(projection){
        requireValue(projection&&projection.schema===INSTALLATION_PROJECTION_SCHEMA,"canonical KV installation projection schema invalid");
        requireValue(projection.state==="KV_INSTALLATION_VERIFIED"||projection.state==="KV_INSTALLATION_NOT_VERIFIED","canonical KV installation projection state invalid");
        requireValue(projection.resident_kv_root_observed===true,"canonical KV resident root observation missing");
        requireValue(projection.current_cloud_provider_observation===false,"canonical KV installation projection must not claim cloud-provider observation");
        requireValue(projection.credential_material_present===false&&projection.provider_operation_authorized===false&&projection.authority_effect==="NONE","canonical KV installation projection authority invalid");
        if(projection.state==="KV_INSTALLATION_VERIFIED"){
          requireValue(projection.installation_receipt_present===true,"canonical KV installation receipt presence missing");
          requireValue(typeof projection.source_tree_sha==="string"&&/^[0-9a-f]{40}$/i.test(projection.source_tree_sha),"canonical KV installation tree SHA invalid");
          requireValue(typeof projection.receipt_sha256==="string"&&/^sha256:[0-9a-f]{64}$/i.test(projection.receipt_sha256),"canonical KV installation receipt digest invalid");
          requireValue(projection.full_template_parity==="VALIDATED","canonical KV installation parity invalid");
          requireValue(projection.source_census&&Number.isInteger(projection.source_census.files)&&projection.source_census.files>0&&Number.isInteger(projection.source_census.directories)&&projection.source_census.directories>0,"canonical KV installation source census invalid");
        }else{
          requireValue(projection.installation_receipt_present===false,"unverified KV installation must not claim receipt presence");
        }
        return projection;
      });
    },
    authority_effect:"NONE"
  });
}

root.StegVerseKVQueryBridgeModuleState=Object.freeze({
  schema:"stegverse.site.my-kv.query-bridge-module-state/v1",
  directory_bridge_ready:!!(root.StegVerseKVDirectoryBridge&&typeof root.StegVerseKVDirectoryBridge.listDirectory==="function"),
  connection_health_bridge_ready:!!(root.StegVerseKVConnectionHealthBridge&&typeof root.StegVerseKVConnectionHealthBridge.getDomainHealth==="function"),
  installation_status_bridge_ready:!!(root.StegVerseKVInstallationStatusBridge&&typeof root.StegVerseKVInstallationStatusBridge.getInstallationStatus==="function"),
  authority_effect:"NONE"
});
}(typeof globalThis!=="undefined"?globalThis:this));
