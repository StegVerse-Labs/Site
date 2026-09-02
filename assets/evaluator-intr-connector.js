(function(root){
"use strict";
var CONFIG_KEY="__STEGVERSE_EVALUATOR_INTR_CONFIG__";
var PROJECTION_URL="/data/evaluator-review/runtime-projection.json";
var PROJECTION_SCHEMA="stegverse.site.evaluator_intr_runtime_projection/v1";
var MAX_FUTURE_SKEW_MS=60000;
function unavailableError(message){var e=new Error(message);e.code="INTR_RUNTIME_UNAVAILABLE";return e;}
function canonicalBody(value){return JSON.stringify(value);}
function canonicalIntentOperation(request){
  if(request&&request.request_class==="EVALUATOR_REVIEW"&&request.operation==="READ_REVIEW"){
    var b=request.bindings||{};
    return {profile:"evaluator-read-review",operation:"READ_REVIEW",operationId:"EVALUATOR:READ_REVIEW:"+b.test_id+":v"+b.revision+":INGRESS"};
  }
  if(request&&request.request_class==="SV002_PUBLIC_OBSERVE"&&request.operation==="READ_OBSERVATION"){
    return {profile:"sv002-public-observe",operation:"READ_OBSERVATION",operationId:"SV002-OBSERVE-"+String(request.request_sha256||"").slice(0,16)};
  }
  throw new Error("Canonical InTr profile not available for request class/operation");
}
async function buildCanonicalIntent(request){
  var intr=root.StegVerseGeneratedInTr;
  if(!intr||typeof intr.buildIntent!=="function")throw new Error("Canonical generated InTr connector unavailable");
  var selected=canonicalIntentOperation(request);
  return intr.buildIntent(selected.profile,new TextEncoder().encode(intr.canonical(request)),selected.operation,selected.operationId);
}
async function sha256Hex(text){
  if(!root.crypto||!root.crypto.subtle)throw new Error("SHA-256 unavailable");
  var digest=await root.crypto.subtle.digest("SHA-256",new TextEncoder().encode(text));
  return Array.from(new Uint8Array(digest)).map(function(b){return b.toString(16).padStart(2,"0");}).join("");
}
function isSha256Uri(value){return /^sha256:[a-f0-9]{64}$/.test(String(value||""));}
function endpointUrl(value){try{return new URL(String(value||""));}catch(_error){return null;}}
function validateEndpoint(url,expectedPath,allowLoopbackHttp){
  if(!url)return false;
  var loopback=["127.0.0.1","localhost","::1"].includes(url.hostname);
  if(url.protocol!=="https:"&&!(allowLoopbackHttp&&loopback&&url.protocol==="http:"))return false;
  return url.pathname===expectedPath&&!url.username&&!url.password&&!url.search&&!url.hash;
}
function injectedConfig(){
  var c=root[CONFIG_KEY]||{};
  if(c.mode!=="REMOTE_INTR")return null;
  var evaluator=typeof c.endpoint==="string"&&c.endpoint?endpointUrl(c.endpoint):null;
  if(evaluator&&!validateEndpoint(evaluator,"/intr/evaluator",true))evaluator=null;
  var sv002=typeof c.sv002_observe_endpoint==="string"&&c.sv002_observe_endpoint?c.sv002_observe_endpoint:"";
  if(!evaluator&&!sv002)return null;
  return {
    source:"RUNTIME_INJECTED",
    evaluator_endpoint:evaluator?evaluator.href:"",
    sv002_observe_endpoint:sv002,
    authority_ref:typeof c.authority_ref==="string"&&c.authority_ref?c.authority_ref:"PUBLIC_READ"
  };
}
function validateProjection(p,nowMs){
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
  if(!Number.isFinite(observed)||!Number.isFinite(readinessObserved)||!Number.isFinite(maxAge)||maxAge<=0){errors.push("projection_freshness_binding_invalid");}
  else{
    if(observed-now>MAX_FUTURE_SKEW_MS||readinessObserved-now>MAX_FUTURE_SKEW_MS)errors.push("projection_future_dated");
    if(now-observed>maxAge*1000||now-readinessObserved>maxAge*1000)errors.push("projection_stale");
  }
  return {ok:errors.length===0,errors:errors,endpoint:endpoint};
}
function installConnector(evaluatorEndpoint,sv002Endpoint,authorityRef,source){
  var lastIntent=null;
  var connector=Object.freeze({
    authorityRef:function(){return authorityRef;},
    projectionSource:source,
    transportIntent:function(){return lastIntent;},
    transact:async function(request){
      var body=canonicalBody(request);
      var digest=await sha256Hex(body);
      lastIntent=await buildCanonicalIntent(request);
      var endpoint=request&&request.request_class==="SV002_PUBLIC_OBSERVE"?sv002Endpoint:evaluatorEndpoint;
      if(!endpoint)throw unavailableError("Canonical Interlock endpoint not provisioned for request class");
      var response;
      try{response=await fetch(endpoint,{
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
      });}catch(error){if(error&&error.code==="INTR_RUNTIME_UNAVAILABLE")throw error;throw unavailableError("Interlock/InTr runtime unavailable");}
      if(!response.ok)throw unavailableError("Interlock/InTr runtime unavailable ("+response.status+")");
      return response.json();
    }
  });
  root.StegVerseInterlockConnector=connector;
  return connector;
}
async function discover(){
  var injected=injectedConfig();
  if(injected&&injected.evaluator_endpoint){
    root.StegVerseEvaluatorInTrDiscovery={state:"READY",source:injected.source,errors:[]};
    return installConnector(injected.evaluator_endpoint,injected.sv002_observe_endpoint,injected.authority_ref,injected.source);
  }
  try{
    var response=await fetch(PROJECTION_URL,{cache:"no-store",credentials:"same-origin",redirect:"error"});
    if(!response.ok)throw new Error("projection_http_"+response.status);
    var projection=await response.json();
    var checked=validateProjection(projection,Date.now());
    if(!checked.ok)throw new Error(checked.errors.join(","));
    root.StegVerseEvaluatorInTrDiscovery={state:"READY",source:"SITE_RUNTIME_PROJECTION",errors:[],projection:projection};
    return installConnector(checked.endpoint.href,injected&&injected.sv002_observe_endpoint||"",injected&&injected.authority_ref||"PUBLIC_READ","SITE_RUNTIME_PROJECTION");
  }catch(error){
    var errors=[String(error&&error.message||error)];
    if(injected&&injected.sv002_observe_endpoint){
      root.StegVerseEvaluatorInTrDiscovery={state:"NOT_PROVISIONED",source:"SITE_RUNTIME_PROJECTION",errors:errors};
      return installConnector("",injected.sv002_observe_endpoint,injected.authority_ref,"RUNTIME_INJECTED_SV002_ONLY");
    }
    root.StegVerseEvaluatorInTrDiscovery={state:"NOT_PROVISIONED",source:"SITE_RUNTIME_PROJECTION",errors:errors};
    return null;
  }
}
root.StegVerseEvaluatorInTrProjection=Object.freeze({schema:PROJECTION_SCHEMA,projectionUrl:PROJECTION_URL,validateProjection:validateProjection,discover:discover});
root.StegVerseInterlockConnectorReady=discover();
}(typeof globalThis!=="undefined"?globalThis:this));
