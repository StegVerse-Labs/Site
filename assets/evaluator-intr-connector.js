(function(root){
"use strict";
var CONFIG_KEY="__STEGVERSE_EVALUATOR_INTR_CONFIG__";
var PROJECTION_URL="data/evaluator-review/runtime-projection.json";
var PROJECTION_SCHEMA="stegverse.site.evaluator_intr_runtime_projection/v1";
var MAX_FUTURE_SKEW_MS=60000;

function canonicalBody(value){return JSON.stringify(value);}
async function sha256Hex(text){
  if(!root.crypto||!root.crypto.subtle)throw new Error("SHA-256 unavailable");
  var digest=await root.crypto.subtle.digest("SHA-256",new TextEncoder().encode(text));
  return Array.from(new Uint8Array(digest)).map(function(b){return b.toString(16).padStart(2,"0");}).join("");
}
function isSha256Uri(value){return /^sha256:[a-f0-9]{64}$/.test(String(value||""));}
function endpointUrl(value){
  try{return new URL(String(value||""));}catch(_error){return null;}
}
function validateEndpoint(url, expectedPath, allowLoopbackHttp){
  if(!url)return false;
  var loopback=["127.0.0.1","localhost","::1"].includes(url.hostname);
  if(url.protocol!=="https:"&&!(allowLoopbackHttp&&loopback&&url.protocol==="http:"))return false;
  if(url.pathname!==expectedPath||url.username||url.password||url.search||url.hash)return false;
  return true;
}
function injectedConfig(){
  var c=root[CONFIG_KEY]||{};
  if(c.mode!=="REMOTE_INTR"||typeof c.endpoint!=="string"||!c.endpoint)return null;
  var endpoint=endpointUrl(c.endpoint);
  if(!validateEndpoint(endpoint,"/intr/evaluator",true))return null;
  return {
    source:"RUNTIME_INJECTED",
    endpoint:endpoint.href,
    authority_ref:typeof c.authority_ref==="string"&&c.authority_ref?c.authority_ref:"PUBLIC_READ"
  };
}
function validateProjection(p, nowMs){
  var errors=[];
  if(!p||p.schema!==PROJECTION_SCHEMA)errors.push("projection_schema_invalid");
  if(p&&p.capability!=="EVALUATOR_READ_REVIEW_INTR")errors.push("projection_capability_invalid");
  if(p&&p.state!=="VERIFIED")errors.push("projection_state_not_verified");
  if(p&&p.active!==true)errors.push("projection_not_active");
  if(p&&p.transport!=="InTr")errors.push("projection_transport_invalid");
  if(p&&p.credential_authority!=="TV/TVC")errors.push("projection_credential_authority_invalid");
  if(p&&p.gateway_authority!=="NONE")errors.push("projection_gateway_authority_invalid");
  if(p&&p.github_token_runtime_authority!=="NONE")errors.push("projection_github_authority_invalid");
  if(p&&p.authority_effect!==false)errors.push("projection_authority_effect_invalid");
  if(p&&p.activation_effect!==false)errors.push("projection_activation_effect_invalid");
  if(p&&p.runtime_receiver_ready!==true)errors.push("projection_receiver_not_ready");
  if(p&&!isSha256Uri(p.route_observation_digest))errors.push("projection_route_digest_invalid");
  if(p&&!isSha256Uri(p.node_advertisement_sha256))errors.push("projection_node_digest_invalid");

  var endpoint=endpointUrl(p&&p.endpoint);
  var readiness=endpointUrl(p&&p.readiness_endpoint);
  if(!validateEndpoint(endpoint,"/intr/evaluator",false))errors.push("projection_endpoint_invalid");
  if(!validateEndpoint(readiness,"/intr/evaluator/readiness",false))errors.push("projection_readiness_endpoint_invalid");
  if(endpoint&&readiness&&endpoint.origin!==readiness.origin)errors.push("projection_endpoint_origin_mismatch");
  if(endpoint&&p&&p.public_route_hostname!==endpoint.hostname)errors.push("projection_hostname_binding_invalid");

  var observed=Date.parse(p&&p.public_route_observed_at);
  var readinessObserved=Date.parse(p&&p.gateway_readiness_observed_at);
  var maxAge=Number(p&&p.public_route_max_age_seconds);
  var now=Number.isFinite(nowMs)?nowMs:Date.now();
  if(!Number.isFinite(observed)||!Number.isFinite(readinessObserved)||!Number.isFinite(maxAge)||maxAge<=0){
    errors.push("projection_freshness_binding_invalid");
  }else{
    if(observed-now>MAX_FUTURE_SKEW_MS||readinessObserved-now>MAX_FUTURE_SKEW_MS)errors.push("projection_future_dated");
    if(now-observed>maxAge*1000||now-readinessObserved>maxAge*1000)errors.push("projection_stale");
  }
  return {ok:errors.length===0,errors:errors,endpoint:endpoint};
}
function installConnector(endpoint,authorityRef,source){
  var connector=Object.freeze({
    authorityRef:function(){return authorityRef;},
    projectionSource:source,
    transact:async function(request){
      var body=canonicalBody(request);
      var digest=await sha256Hex(body);
      var response=await fetch(endpoint,{
        method:"POST",
        headers:{
          "content-type":"application/json",
          "x-stegverse-transport":"InTr",
          "x-stegverse-authorization-id":authorityRef,
          "x-stegverse-payload-sha256":digest
        },
        credentials:"omit",
        cache:"no-store",
        redirect:"error",
        referrerPolicy:"no-referrer",
        body:body
      });
      if(!response.ok)throw new Error("Evaluator InTr runtime unavailable ("+response.status+")");
      return response.json();
    }
  });
  root.StegVerseInterlockConnector=connector;
  return connector;
}
async function discover(){
  var injected=injectedConfig();
  if(injected){
    root.StegVerseEvaluatorInTrDiscovery={state:"READY",source:injected.source,errors:[]};
    return installConnector(injected.endpoint,injected.authority_ref,injected.source);
  }
  try{
    var response=await fetch(PROJECTION_URL,{cache:"no-store",credentials:"same-origin",redirect:"error"});
    if(!response.ok)throw new Error("projection_http_"+response.status);
    var projection=await response.json();
    var checked=validateProjection(projection,Date.now());
    if(!checked.ok){
      root.StegVerseEvaluatorInTrDiscovery={state:"NOT_PROVISIONED",source:"SITE_RUNTIME_PROJECTION",errors:checked.errors};
      return null;
    }
    root.StegVerseEvaluatorInTrDiscovery={state:"READY",source:"SITE_RUNTIME_PROJECTION",errors:[],projection:projection};
    return installConnector(checked.endpoint.href,"PUBLIC_READ","SITE_RUNTIME_PROJECTION");
  }catch(error){
    root.StegVerseEvaluatorInTrDiscovery={state:"NOT_PROVISIONED",source:"SITE_RUNTIME_PROJECTION",errors:[String(error&&error.message||error)]};
    return null;
  }
}
root.StegVerseEvaluatorInTrProjection=Object.freeze({
  schema:PROJECTION_SCHEMA,
  projectionUrl:PROJECTION_URL,
  validateProjection:validateProjection,
  discover:discover
});
root.StegVerseInterlockConnectorReady=discover();
}(typeof globalThis!=="undefined"?globalThis:this));
