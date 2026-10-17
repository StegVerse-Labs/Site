// ACTIONS BY MANIFEST (.github data/task-registry-global-invariants.json semantics.actions_by_manifest;
// NO_EXTERNAL_MACHINE_AWAITING_AS_TRANSITION_PREDICATE, NO_DESTINATION_LIVENESS_OR_ALWAYS_ON_RECEIVER_AS_TRANSITION_PREDICATE):
// the WorkSpace DEVICE_KV bridge queues the request durably in the node outbox and looks its result up exactly once.
// A result that is not yet materialized is an actionable FAIL_CLOSED disposition, never a wait, retry or poll loop.
const fs=require('fs');const path=require('path');const vm=require('vm');const nodeCrypto=require('crypto');
const root=path.join(__dirname,'..');
const read=f=>fs.readFileSync(path.join(root,f),'utf8');
const bridgeSrc=read('assets/workspace-kv-bridge.js'),nodeBindingSrc=read('assets/workspace-node-binding.js');
let n=0;const check=(ok,msg)=>{n++;if(!ok)throw new Error(msg);};
const code=bridgeSrc.replace(/\/\/.*$/gm,'');
check(!/setTimeout|setInterval|\bdelay\(|\bpoll\(/.test(code),'bridge has no scheduler, delay or poll loop');
// The explanation contract's guidance must not tell a person to wait on a component either.
check(!/\bwait (for|on|until)\b/i.test(read('assets/workspace-explanation.js').replace(/\/\/.*$/gm,'')),'explanation guidance never tells a person to wait on a component');
const sha=(s)=>nodeCrypto.createHash('sha256').update(s,'utf8').digest('hex');
const NODE='SV-NODE-'+'a'.repeat(24);
const registered={registered:true,state:'REGISTERED',registration:{node_id:NODE,interlock_id:'SV-IL-'+'b'.repeat(24)},receipts:[{}]};
const projection={schema:'stegverse.kv.personal-workspace-projection/v1',workspace_type:'PERSONAL',state:'KV_WORKSPACE_EMPTY',principals:[],organizations:[],credential_material_present:false,provider_operation_authorized:false,workspace_grants_authority:false,authority_effect:'NONE'};
function harness(ready,opts){opts=opts||{};const seen={lookups:0,queued:0,timers:0,materializations:[]};const canonical=(v)=>JSON.stringify(v);
  const ctx={crypto:globalThis.crypto,TextEncoder,TextDecoder,setTimeout:()=>{seen.timers++;},setInterval:()=>{seen.timers++;},
    fetch:(url,init)=>{seen.lookups++;const lookup=JSON.parse(init.body);const m=seen.materializations.find(x=>x.materialization_id===lookup.materialization_id);
      if(opts.status)return Promise.resolve({status:opts.status,json:()=>Promise.resolve(opts.body||{})});
      if(!ready)return Promise.resolve({status:400,json:()=>Promise.resolve({reason:'device_kv_result_not_ready'})});
      const response={schema:'stegverse.device-kv.query-response/v1',state:'QUERY_COMPLETE',record_class:m.query.record_class,query_request_id:m.query.request_id,request_grants_authority:false,response_grants_authority:false,authority_effect:'NONE',projection};
      const text=canonical(response);return Promise.resolve({status:200,json:()=>Promise.resolve({schema:'stegverse.device-kv.query-result-delivery/v1',state:'RESULT_AVAILABLE',materialization_id:m.materialization_id,request_hash:m.request_hash,node_id:NODE,authority_effect:'NONE_RESULT_DELIVERY_ONLY',result_lookup_grants_authority:false,response,response_payload_hash:sha(text),response_carrier_signal:text})});},
    StegVerseGeneratedInTr:{canonical,buildIntent:(k,bytes,op,id)=>Promise.resolve({packet_id:'pkt-'+id,payload_hash:sha(new TextDecoder().decode(bytes))}),buildMaterializationRequest:(k,i,r,b,extra)=>{const q=extra.kv_request;const m={materialization_id:'mat-'+q.request_id,request_hash:sha(canonical(q)),query:q};seen.materializations.push(m);return Promise.resolve(m);},sha256Bytes:(bytes)=>Promise.resolve(sha(new TextDecoder().decode(bytes)))},
    StegVerseHBInTrCarrier:{buildBinding:()=>Promise.resolve({}),recoverSignal:(signal)=>Promise.resolve(new TextEncoder().encode(signal))},
    StegVerseNodeContinuity:{status:()=>Promise.resolve(registered),registerDevice(){throw new Error('page must not register');},queueIntrMaterializationRequest:()=>{seen.queued++;return Promise.resolve();}},
    StegVerseDeviceKVInTrSync:{synchronizeMaterialization:()=>Promise.resolve(),loadTarget:()=>Promise.resolve(opts.target||{state:'CONFORMING_SOVEREIGN_INTR_INGRESS',runtime_ingress_observed:true,result_url:'https://ingress.invalid/intr/device-kv/result'}),getDeliveryReceipt:()=>Promise.resolve(opts.delivery||{network_delivery_observed:true})}};
  vm.createContext(ctx);vm.runInContext(nodeBindingSrc,ctx);vm.runInContext(bridgeSrc,ctx);return {bridge:ctx.StegVerseWorkspaceKVBridge,seen};}
(async()=>{
  // Result not yet materialized: one lookup, no timer, an actionable FAIL_CLOSED decision naming the queued request.
  let h=harness(false);
  const err=await h.bridge.loadPersonalWorkspace({recovery_result:null}).then(()=>null,e=>e);
  check(err&&err.decision&&err.decision.disposition==='FAIL_CLOSED'&&err.decision.predicate==='DEVICE_KV_RESULT_NOT_YET_MATERIALIZED','not-ready result is a FAIL_CLOSED disposition: '+(err&&err.message));
  check(err.decision.materialization_id===h.seen.materializations[0].materialization_id&&err.decision.request_hash===h.seen.materializations[0].request_hash&&err.decision.authority_effect==='NONE','the disposition names the durably queued materialization');
  check(h.seen.queued===1&&h.seen.lookups===1&&h.seen.timers===0,'queued once, looked up once, never waited: '+JSON.stringify(h.seen));
  check(typeof h.bridge.reasons.DEVICE_KV_RESULT_NOT_YET_MATERIALIZED==='string','the disposition has a plain-language reason');
  // Result available: delivered on the single lookup.
  h=harness(true);
  const p=await h.bridge.loadPersonalWorkspace({recovery_result:null});
  check(p&&p.state==='KV_WORKSPACE_EMPTY'&&h.seen.lookups===1&&h.seen.timers===0,'available result delivered on one lookup');
  // Organization Role conformance: every non-ALLOW result is actionable (six fields), never a bare not-ready.
  const SIX=['failure_code','failed_predicate','required_evidence_or_repair','retry_entrypoint','owning_existing_goal','next_attempt'];
  const actionableOk=d=>d&&d.disposition==='FAIL_CLOSED'&&SIX.every(k=>typeof d[k]==='string'&&d[k].trim())&&d.failure_code===d.predicate&&d.failed_predicate===d.predicate&&d.owning_existing_goal==='STEGVERSE-WORKSPACE-ANY-DEVICE-KV-SURFACE-001'&&d.authority_effect==='NONE';
  check(actionableOk(err.decision),'not-materialized result carries the six actionable fields: '+JSON.stringify(err.decision));
  // Destination existence is sufficient; liveness is never read: a projected target whose runtime was never observed is used.
  h=harness(true,{target:{state:'CONFORMING_SOVEREIGN_INTR_INGRESS',runtime_ingress_observed:false,result_url:'https://ingress.invalid/intr/device-kv/result'}});
  check((await h.bridge.loadPersonalWorkspace({recovery_result:null})).state==='KV_WORKSPACE_EMPTY'&&h.seen.lookups===1,'an existing destination is used whether or not its runtime was observed');
  // A destination that does not exist (not projected) is an actionable refusal; the request stays queued; no lookup.
  h=harness(true,{target:{state:'AWAITING_SOVEREIGN_INTR_INGRESS',runtime_ingress_observed:false,result_url:null}});
  let e2=await h.bridge.loadPersonalWorkspace({recovery_result:null}).then(()=>null,e=>e);
  check(e2&&e2.decision&&e2.decision.predicate==='SOVEREIGN_INTR_INGRESS_TARGET_NOT_PROJECTED'&&actionableOk(e2.decision)&&h.seen.queued===1&&h.seen.lookups===0&&h.seen.timers===0,'absent destination is actionable, request queued, nothing waits: '+JSON.stringify(e2&&e2.decision));
  // Not yet delivered from the outbox: actionable, no lookup, no wait.
  h=harness(true,{delivery:{network_delivery_observed:false}});
  e2=await h.bridge.loadPersonalWorkspace({recovery_result:null}).then(()=>null,e=>e);
  check(e2&&e2.decision&&e2.decision.predicate==='DEVICE_KV_REQUEST_QUEUED_NOT_DELIVERED'&&actionableOk(e2.decision)&&h.seen.lookups===0&&h.seen.timers===0,'undelivered request is actionable and nothing waits: '+JSON.stringify(e2&&e2.decision));
  // Any other result response (D13): still actionable with all six fields, the HTTP status and reason kept, no wait.
  for(const [status,body] of [[503,{reason:'upstream_unavailable'}],[500,{}],[404,{reason:7}]]){
    h=harness(true,{status,body});
    e2=await h.bridge.loadPersonalWorkspace({recovery_result:null}).then(()=>null,e=>e);
    check(e2&&e2.decision&&e2.decision.predicate==='DEVICE_KV_RESULT_UNAVAILABLE'&&actionableOk(e2.decision)&&e2.decision.http_status===status&&e2.decision.reason===(typeof body.reason==='string'?body.reason:null)&&e2.decision.materialization_id===h.seen.materializations[0].materialization_id&&h.seen.lookups===1&&h.seen.timers===0,'HTTP '+status+' result is a six-field refusal, looked up once, nothing waits: '+JSON.stringify(e2&&e2.decision));
  }
  check(typeof h.bridge.reasons.DEVICE_KV_RESULT_UNAVAILABLE==='string','the unavailable-result disposition has a plain-language reason');
  check(!/runtime_ingress_observed/.test(code),'the bridge never reads destination liveness');
  console.log('PASS workspace KV bridge does not wait on a receiver ('+n+' checks)');
})().catch(e=>{console.error(e);process.exit(1);});
