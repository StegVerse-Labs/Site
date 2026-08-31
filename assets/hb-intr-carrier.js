(function(root){
"use strict";
if(!root || root.StegVerseHBInTrCarrier) return;

var HB_ANCHOR_EPOCH=32;
var HB_ANCHOR_UNIX_MS=1787511600000;
var HB_PERIOD_MS=10;
var HB_REFERENCE_FREQUENCY_HZ=100;
var HB_CHANNEL_COUNT=16;
var PROFILE_SCHEMA="stegverse.intr.hb-derived-carrier-profile/v1";
var BINDING_SCHEMA="stegverse.intr.hb-derived-carrier-binding/v1";

function canon(value){
  if(value===null||typeof value!=="object") return JSON.stringify(value);
  if(Array.isArray(value)) return "["+value.map(canon).join(",")+"]";
  return "{"+Object.keys(value).sort().map(function(k){return JSON.stringify(k)+":"+canon(value[k]);}).join(",")+"}";
}
function hex(buffer){
  return Array.prototype.map.call(new Uint8Array(buffer),function(x){return x.toString(16).padStart(2,"0");}).join("");
}
function sha256Json(value){
  return crypto.subtle.digest("SHA-256",new TextEncoder().encode(canon(value))).then(function(d){return "sha256:"+hex(d);});
}

function encodeHeartbeatId(epoch){
  if(!Number.isSafeInteger(epoch)||epoch<0) throw new Error("heartbeat epoch must be a non-negative safe integer");
  var body=epoch.toString(36).toUpperCase().padStart(8,"0");
  if(body.length!==8) throw new Error("heartbeat epoch exceeds canonical Base36 width");
  return "HB-"+body;
}
function deriveReference(sampledUnixMs){
  if(!Number.isSafeInteger(sampledUnixMs)||sampledUnixMs<HB_ANCHOR_UNIX_MS) throw new Error("invalid HB carrier sample");
  var elapsed=sampledUnixMs-HB_ANCHOR_UNIX_MS;
  var quanta=Math.floor(elapsed/HB_PERIOD_MS);
  var offset=elapsed%HB_PERIOD_MS;
  var epoch=HB_ANCHOR_EPOCH+quanta;
  return {
    heartbeat_epoch:epoch,
    heartbeat_id:encodeHeartbeatId(epoch),
    sampled_unix_ms:sampledUnixMs,
    phase_offset_ms:offset,
    reference_frequency_hz:HB_REFERENCE_FREQUENCY_HZ,
    progression_dependency:"OSCILLATOR_ONLY"
  };
}
function deriveChannel(payloadHash){
  if(typeof payloadHash!=="string"||!/^sha256:[a-f0-9]{64}$/.test(payloadHash)) throw new Error("payload_hash required for HB carrier channel");
  var slot=parseInt(payloadHash.charAt(22),16);
  return {
    channel_id:"HB:H1:P"+slot,
    channel_family:"H1_PHASE_SLOTS",
    frequency_ratio:1.0,
    phase_slot:slot,
    phase_slot_count:HB_CHANNEL_COUNT,
    phase_radians:Number((2*Math.PI*slot/HB_CHANNEL_COUNT).toFixed(12)),
    amplitude_ratio:1.0,
    derivation:"PAYLOAD_SHA256_FIRST64_MOD_16"
  };
}
function sha256Bytes(bytes){
  return crypto.subtle.digest("SHA-256",bytes).then(function(d){return hex(d);});
}
function base64ToBytes(value){
  if(typeof value!=="string") throw new Error("HB carrier packet missing");
  var raw=atob(value),bytes=new Uint8Array(raw.length);
  for(var i=0;i<raw.length;i++) bytes[i]=raw.charCodeAt(i);
  return bytes;
}
function validateBinding(binding,packetId,payloadHash){
  if(!binding||typeof binding!=="object"||Array.isArray(binding)) return Promise.reject(new Error("HB carrier binding object required"));
  var expected={
    schema:BINDING_SCHEMA,carrier_profile:PROFILE_SCHEMA,fundamental_mode:"HB",
    packet_id:packetId,payload_hash:payloadHash,credential_authority:"TV/TVC",
    authority_effect:"NONE_CARRIER_ONLY"
  };
  try{
    Object.keys(expected).forEach(function(k){if(binding[k]!==expected[k]) throw new Error("HB carrier binding mismatch: "+k);});
    [
      "carrier_grants_admission_authority","carrier_grants_execution_authority",
      "carrier_grants_credential_authority","carrier_grants_routing_authority",
      "carrier_grants_transition_authority","carrier_grants_receiving_authority"
    ].forEach(function(k){if(binding[k]!==false) throw new Error("HB carrier authority drift: "+k);});
    var reference=deriveReference(binding.heartbeat_reference&&binding.heartbeat_reference.sampled_unix_ms);
    if(canon(reference)!==canon(binding.heartbeat_reference)) throw new Error("HB carrier reference derivation mismatch");
    var channel=deriveChannel(payloadHash);
    if(canon(channel)!==canon(binding.channel)) throw new Error("HB carrier channel derivation mismatch");
  }catch(error){return Promise.reject(error);}
  var body=Object.assign({},binding),claimed=body.binding_sha256;delete body.binding_sha256;
  return sha256Json(body).then(function(actual){
    if(actual!==claimed) throw new Error("HB carrier binding sha256 mismatch");
    return binding;
  });
}
function recoverSignal(signal){
  if(!signal||signal.schema!=="stegverse.heartbeat-intr-derived-carrier/v1") return Promise.reject(new Error("HB derived carrier signal schema invalid"));
  var intr=signal.intr,carrier=signal.carrier,authority=signal.authority,binding=signal.carrier_binding;
  if(!intr||!carrier||!authority) return Promise.reject(new Error("HB derived carrier signal incomplete"));
  if(intr.packet_encoding!=="base64") return Promise.reject(new Error("HB carrier packet encoding invalid"));
  if(authority.authority_effect!=="NONE_CARRIER_ONLY") return Promise.reject(new Error("HB carrier authority effect invalid"));
  [
    "heartbeat_grants_admission_authority","heartbeat_grants_execution_authority",
    "heartbeat_grants_credential_authority","heartbeat_grants_routing_authority",
    "heartbeat_grants_transition_authority","heartbeat_grants_receiving_authority",
    "derived_carrier_grants_admission_authority","derived_carrier_grants_execution_authority",
    "derived_carrier_grants_credential_authority","derived_carrier_grants_routing_authority",
    "derived_carrier_grants_transition_authority","derived_carrier_grants_receiving_authority"
  ].forEach(function(k){if(authority[k]!==false) throw new Error("HB derived carrier authority drift: "+k);});
  return validateBinding(binding,intr.packet_id,intr.payload_hash).then(function(validated){
    var ref=validated.heartbeat_reference,ch=validated.channel;
    var carrierExpected={
      carrier_profile:validated.carrier_profile,
      carrier_binding_sha256:validated.binding_sha256,
      heartbeat_epoch:ref.heartbeat_epoch,
      heartbeat_reference:ref.heartbeat_id,
      sampled_unix_ms:ref.sampled_unix_ms,
      intra_reference_phase_offset_ms:ref.phase_offset_ms,
      channel_id:ch.channel_id,
      phase_slots:ch.phase_slot_count,
      channel_slot:ch.phase_slot,
      channel_derivation:ch.derivation
    };
    Object.keys(carrierExpected).forEach(function(k){if(carrier[k]!==carrierExpected[k]) throw new Error("HB derived carrier mismatch: "+k);});
    var bytes=base64ToBytes(intr.packet_base64);
    return sha256Bytes(bytes).then(function(actual){
      if(actual!==intr.packet_sha256) throw new Error("HB derived carrier packet sha256 mismatch");
      return bytes;
    });
  });
}
function buildBinding(packetId,payloadHash,sampledUnixMs){
  if(typeof payloadHash!=="string"||!/^sha256:[a-f0-9]{64}$/.test(payloadHash)) return Promise.reject(new Error("payload_hash invalid for HB carrier"));
  var sampled=sampledUnixMs===undefined?Date.now():sampledUnixMs;
  var reference;
  try{reference=deriveReference(sampled);}catch(error){return Promise.reject(error);}
  if(typeof packetId!=="string"||!packetId) return Promise.reject(new Error("packet_id required for HB carrier"));
  var channel;
  try{channel=deriveChannel(payloadHash);}catch(error){return Promise.reject(error);}
  var body={
      schema:BINDING_SCHEMA,
      carrier_profile:PROFILE_SCHEMA,
      fundamental_mode:"HB",
      packet_id:packetId,
      payload_hash:payloadHash,
      heartbeat_reference:reference,
      channel:channel,
      carrier_grants_admission_authority:false,
      carrier_grants_execution_authority:false,
      carrier_grants_credential_authority:false,
      carrier_grants_routing_authority:false,
      carrier_grants_transition_authority:false,
      carrier_grants_receiving_authority:false,
      credential_authority:"TV/TVC",
      authority_effect:"NONE_CARRIER_ONLY"
    };
  return sha256Json(body).then(function(bindingHash){return Object.assign({},body,{binding_sha256:bindingHash});});
}

root.StegVerseHBInTrCarrier=Object.freeze({
  schema:PROFILE_SCHEMA,
  binding_schema:BINDING_SCHEMA,
  fundamental_mode:"HB",
  reference_frequency_hz:HB_REFERENCE_FREQUENCY_HZ,
  heartbeat_period_ms:HB_PERIOD_MS,
  channel_family:"H1_PHASE_SLOTS",
  channel_count:HB_CHANNEL_COUNT,
  progression_dependency:"OSCILLATOR_ONLY",
  buildBinding:buildBinding,
  validateBinding:validateBinding,
  recoverSignal:recoverSignal,
  deriveReference:deriveReference,
  deriveChannel:deriveChannel,
  encodeHeartbeatId:encodeHeartbeatId,
  carrier_grants_authority:false,
  credential_authority:"TV/TVC",
  authority_effect:"NONE"
});
}(typeof globalThis!=="undefined"?globalThis:this));
