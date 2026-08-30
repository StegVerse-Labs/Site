const assert=require("node:assert/strict");
const fs=require("node:fs");
const vm=require("node:vm");
const {webcrypto}=require("node:crypto");
const {TextEncoder}=require("node:util");

const source=fs.readFileSync(require("node:path").join(__dirname,"../assets/evaluator-intr-connector.js"),"utf8");

function projection(overrides={}){
  const now=new Date().toISOString();
  return {
    schema:"stegverse.site.evaluator_intr_runtime_projection/v1",
    capability:"EVALUATOR_READ_REVIEW_INTR",
    state:"VERIFIED",
    active:true,
    transport:"InTr",
    endpoint:"https://gateway.example/intr/evaluator",
    readiness_endpoint:"https://gateway.example/intr/evaluator/readiness",
    endpoint_method:"POST",
    runtime_receiver_ready:true,
    route_observation_digest:"sha256:"+"a".repeat(64),
    node_advertisement_sha256:"sha256:"+"b".repeat(64),
    gateway_readiness_observed_at:now,
    public_route_observed_at:now,
    public_route_max_age_seconds:300,
    public_route_hostname:"gateway.example",
    credential_authority:"TV/TVC",
    gateway_authority:"NONE",
    github_token_runtime_authority:"NONE",
    authority_effect:false,
    activation_effect:false,
    ...overrides
  };
}

async function boot(value,injected){
  const calls=[];
  const context={
    URL,Date,Promise,Object,Array,String,Number,RegExp,TextEncoder,
    crypto:webcrypto,
    fetch:async(url,options)=>{
      calls.push({url,options});
      if(url==="data/evaluator-review/runtime-projection.json")return {ok:true,status:200,json:async()=>value};
      return {ok:true,status:200,json:async()=>({schema_version:"stegverse.evaluator_review.interlock_response.v1"})};
    }
  };
  if(injected)context.__STEGVERSE_EVALUATOR_INTR_CONFIG__=injected;
  context.globalThis=context;
  vm.runInNewContext(source,context,{filename:"evaluator-intr-connector.js"});
  await context.StegVerseInterlockConnectorReady;
  return {context,calls};
}

(async()=>{
  const good=await boot(projection());
  assert.equal(good.context.StegVerseEvaluatorInTrDiscovery.state,"READY");
  assert.equal(good.context.StegVerseEvaluatorInTrDiscovery.source,"SITE_RUNTIME_PROJECTION");
  assert.equal(typeof good.context.StegVerseInterlockConnector.transact,"function");
  assert.equal(good.context.StegVerseInterlockConnector.authorityRef(),"PUBLIC_READ");

  const blocked=await boot(projection({state:"BLOCKED",active:false,endpoint:null,readiness_endpoint:null,runtime_receiver_ready:false}));
  assert.equal(blocked.context.StegVerseEvaluatorInTrDiscovery.state,"NOT_PROVISIONED");
  assert.equal(blocked.context.StegVerseInterlockConnector,undefined);

  const remoteAuthority=await boot(projection({gateway_authority:"EXECUTE"}));
  assert.equal(remoteAuthority.context.StegVerseEvaluatorInTrDiscovery.state,"NOT_PROVISIONED");
  assert.equal(remoteAuthority.context.StegVerseInterlockConnector,undefined);

  const stale=await boot(projection({public_route_observed_at:"2026-01-01T00:00:00Z",gateway_readiness_observed_at:"2026-01-01T00:00:00Z",public_route_max_age_seconds:60}));
  assert.equal(stale.context.StegVerseEvaluatorInTrDiscovery.state,"NOT_PROVISIONED");

  const mismatched=await boot(projection({readiness_endpoint:"https://other.example/intr/evaluator/readiness"}));
  assert.equal(mismatched.context.StegVerseEvaluatorInTrDiscovery.state,"NOT_PROVISIONED");

  const sv002Only=await boot(projection({state:"BLOCKED",active:false,endpoint:null,readiness_endpoint:null,runtime_receiver_ready:false}),{
    mode:"REMOTE_INTR",
    sv002_observe_endpoint:"https://gateway.example/intr/sv002-observe",
    authority_ref:"PUBLIC_READ"
  });
  assert.equal(typeof sv002Only.context.StegVerseInterlockConnector.transact,"function");
  assert.equal(sv002Only.context.StegVerseInterlockConnector.projectionSource,"RUNTIME_INJECTED_SV002_ONLY");

  console.log("EVALUATOR_INTR_RUNTIME_PROJECTION_PASS");
})().catch(error=>{console.error(error);process.exit(1);});
