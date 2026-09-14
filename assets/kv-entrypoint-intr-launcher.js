(function(root){
"use strict";

var TARGET_URL="my-kv.html";
var EXPECTED_BRIDGE_KIND="DEVICE_KV_QUERY_RETURN";
var EXPECTED_PROJECTION_SCHEMA="stegverse.kv.installation-status-projection/v1";
var ALLOWED_STATES={KV_INSTALLATION_VERIFIED:true,KV_INSTALLATION_NOT_VERIFIED:true};

function requireValue(ok,message){
  if(!ok) throw new Error("FAIL_CLOSED: "+message);
}

function validateBridge(){
  var bridge=root.StegVerseKVInstallationStatusBridge;
  requireValue(bridge&&typeof bridge.getInstallationStatus==="function","KnowledgeVault Interlock/InTr launcher unavailable");
  requireValue(bridge.bridge_kind===EXPECTED_BRIDGE_KIND,"KnowledgeVault launcher bridge kind mismatch");
  requireValue(bridge.authority_effect==="NONE","KnowledgeVault launcher bridge authority boundary mismatch");
  return bridge;
}

function validateProjection(projection){
  requireValue(projection&&projection.schema===EXPECTED_PROJECTION_SCHEMA,"KnowledgeVault installation projection schema invalid");
  requireValue(ALLOWED_STATES[projection.state]===true,"KnowledgeVault installation projection state invalid");
  requireValue(projection.credential_material_present===false,"KnowledgeVault launcher observed credential material");
  requireValue(projection.provider_operation_authorized===false,"KnowledgeVault launcher may not authorize a provider operation");
  requireValue(projection.authority_effect==="NONE","KnowledgeVault launcher projection authority mismatch");
  return projection;
}

function launch(){
  var bridge=validateBridge();
  return Promise.resolve(bridge.getInstallationStatus()).then(validateProjection).then(function(projection){
    var destination=new URL(TARGET_URL,root.location.href);
    destination.searchParams.set("entry","intr");
    destination.searchParams.set("kv_state",projection.state);
    root.location.assign(destination.href);
    return {
      schema:"stegverse.site.kv-entrypoint-launch/v1",
      state:"KV_ENTRYPOINT_LAUNCH_ADMITTED",
      kv_projection_state:projection.state,
      protocol:"InTr",
      interlock_request_schema:"kv.interlock.request.v1",
      destination:{boundary:"KV",subsystem:"KnowledgeVault:Interlock"},
      credential_authority:"TV/TVC",
      device_class_requirement:"NONE",
      github_token_runtime_authority:"NONE",
      authority_effect:"NONE"
    };
  });
}

function bind(){
  var control=document.getElementById("kv-entry-launcher");
  var status=document.getElementById("kv-entry-launch-status");
  if(!control) return;
  control.addEventListener("click",function(){
    if(control.disabled) return;
    control.disabled=true;
    if(status){status.textContent="Opening KnowledgeVault through Interlock/InTr…";status.dataset.state="running";}
    launch().catch(function(error){
      control.disabled=false;
      if(status){status.textContent=String(error&&error.message?error.message:error);status.dataset.state="blocked";}
    });
  });
}

root.StegVerseKVEntrypointLauncher=Object.freeze({
  launch:launch,
  validateProjection:validateProjection,
  protocol:"InTr",
  interlock_request_schema:"kv.interlock.request.v1",
  destination:Object.freeze({boundary:"KV",subsystem:"KnowledgeVault:Interlock"}),
  device_class_requirement:"NONE",
  authority_effect:"NONE"
});

if(document.readyState==="loading") document.addEventListener("DOMContentLoaded",bind,{once:true});
else bind();
}(typeof globalThis!=="undefined"?globalThis:this));
