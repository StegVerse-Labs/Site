(function(root){
"use strict";
var CONFIG_KEY="__STEGVERSE_EVALUATOR_INTR_CONFIG__";
function unavailableError(message){var e=new Error(message);e.code="INTR_RUNTIME_UNAVAILABLE";return e;}
function canonicalBody(value){return JSON.stringify(value);}
async function sha256Hex(text){
  if(!root.crypto||!root.crypto.subtle)throw new Error("SHA-256 unavailable");
  var digest=await root.crypto.subtle.digest("SHA-256",new TextEncoder().encode(text));
  return Array.from(new Uint8Array(digest)).map(function(b){return b.toString(16).padStart(2,"0");}).join("");
}
function config(){
  var c=root[CONFIG_KEY]||{};
  return {
    mode:c.mode==="REMOTE_INTR"?"REMOTE_INTR":"NOT_PROVISIONED",
    endpoint:typeof c.endpoint==="string"?c.endpoint:"",
    sv002_observe_endpoint:typeof c.sv002_observe_endpoint==="string"?c.sv002_observe_endpoint:"",
    authority_ref:typeof c.authority_ref==="string"&&c.authority_ref?c.authority_ref:"PUBLIC_READ"
  };
}
var cfg=config();
if(cfg.mode!=="REMOTE_INTR"||(!cfg.endpoint&&!cfg.sv002_observe_endpoint))return;
root.StegVerseInterlockConnector=Object.freeze({
  authorityRef:function(){return cfg.authority_ref;},
  transact:async function(request){
    var body=canonicalBody(request);
    var digest=await sha256Hex(body);
    var endpoint=request&&request.request_class==="SV002_PUBLIC_OBSERVE"?cfg.sv002_observe_endpoint:cfg.endpoint;
    if(!endpoint)throw unavailableError("Canonical Interlock endpoint not provisioned for request class");
    var response;
    try{response=await fetch(endpoint,{
      method:"POST",
      headers:{
        "content-type":"application/json",
        "x-stegverse-transport":"InTr",
        "x-stegverse-authorization-id":cfg.authority_ref,
        "x-stegverse-payload-sha256":digest
      },
      credentials:"omit",
      cache:"no-store",
      redirect:"error",
      referrerPolicy:"no-referrer",
      body:body
    });}catch(error){if(error&&error.code==="INTR_RUNTIME_UNAVAILABLE")throw error;throw unavailableError("Interlock/InTr runtime unavailable");}
    if(!response.ok)throw unavailableError("Interlock/InTr runtime unavailable ("+response.status+")");
    return response.json();
  }
});
}(typeof globalThis!=="undefined"?globalThis:this));
