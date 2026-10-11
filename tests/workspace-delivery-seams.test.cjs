// Family projections and continuity checkpoint delivery (Site#1509 P4 / WS-ASSISTANT delivery): the bridge serves both
// through the same node-bound DEVICE_KV path with class-bound scopes and strict validators; the page verifies nothing
// itself and refuses deliveries that claim verification, authority, reserved schemas or ambiguity.
const fs=require('fs');const path=require('path');const vm=require('vm');const nodeCrypto=require('crypto');
const root=path.join(__dirname,'..');
const read=f=>fs.readFileSync(path.join(root,f),'utf8');
const bridgeSrc=read('assets/workspace-kv-bridge.js'),nodeBindingSrc=read('assets/workspace-node-binding.js'),ui=read('assets/workspace.js');
function assert(ok,msg){if(!ok)throw new Error(msg)}
let n=0;const check=(ok,msg)=>{n++;assert(ok,msg)};
check(bridgeSrc.includes('loadPersonalProjections:loadPersonalProjections')&&bridgeSrc.includes('loadAssistantCheckpoint:loadAssistantCheckpoint'),'bridge exports both seams');
check(!/registerDevice\(/.test(bridgeSrc.replace(/\/\/.*$/gm,''))&&!/localStorage|sessionStorage|indexedDB/.test(bridgeSrc),'no registration or storage');
check(ui.includes('bridge.loadPersonalProjections')&&ui.includes('bridge.loadAssistantCheckpoint'),'page consumes both seams');
const REV='a'.repeat(64);const sha=(s)=>nodeCrypto.createHash('sha256').update(s,'utf8').digest('hex');
const meta=()=>({schema:'stegverse.kv.workspace-projection-metadata/v1',observed_at:'2026-10-11T15:00:00Z',observed_at_semantics:'KV_PROJECTION_PRODUCTION_TIME',source_revision:REV,provenance_ref:'x:sha256:'+REV,workspace_type:'PERSONAL',workspace_id:null,owner_principal_id:null,grant_state:'UNKNOWN',revocation_epoch:null,authority_effect:'NONE'});
const portfolio=(extra)=>Object.assign({schema:'stegverse.kv.cryptobot-portfolio-projection/v1',workspace_type:'PERSONAL',portfolio:{positions:[],total_value_usd:0,drawdown_percent:null,source_observed_at:'2026-10-11T14:59:00Z',provider:'coinbase',unavailable_fields:{}},source:{authority:'StegVerse-Labs/TVC'},credential_material_present:false,provider_operation_authorized:false,trade_authority_granted:false,workspace_grants_authority:false,projection_metadata:meta(),authority_effect:'NONE'},extra||{});
const familyDelivery=(extra)=>Object.assign({schema:'stegverse.kv.workspace-family-projections/v1',state:'KV_FAMILY_PROJECTIONS_PROJECTED',workspace_type:'PERSONAL',projections:[portfolio()],projection_schemas:['stegverse.kv.cryptobot-portfolio-projection/v1'],credential_material_present:false,provider_operation_authorized:false,workspace_grants_authority:false,action_authority:'NONE',projection_metadata:meta(),authority_effect:'NONE'},extra||{});
const checkpoint={schema:'stegverse.kv.workspace-continuity-checkpoint/v1',principal_id:'user:owner',workspace_type:'PERSONAL',workspace_id:'ws:personal:owner',grant_epoch:0,source_epoch:0,sequence:0,source_revision:REV,previous_checkpoint_digest:null,observed_at:'2026-10-10T12:00:00Z',anchor:{kind:'RECEIPT_REF',ref:'receipt:0:0'},authority_effect:'NONE',checkpoint_digest:'b'.repeat(64)};
const decision=(disposition,predicate,replay)=>({schema:'stegverse.kv.workspace-continuity-checkpoint-decision/v1',disposition,predicate,replay_status:replay,authority_effect:'NONE'});
const checkpointDelivery=(extra)=>Object.assign({schema:'stegverse.kv.workspace-continuity-checkpoint-delivery/v1',state:'KV_CHECKPOINT_PROJECTED',workspace_type:'PERSONAL',checkpoint:checkpoint,decision:decision('FAIL_CLOSED','CHECKPOINT_ANCHOR_VERIFIER_UNAVAILABLE:FIRST_CHECKPOINT','UNKNOWN'),anchor_verified:false,credential_material_present:false,provider_operation_authorized:false,workspace_grants_authority:false,action_authority:'NONE',projection_metadata:meta(),authority_effect:'NONE'},extra||{});
const NODE='SV-NODE-'+'a'.repeat(24);
const registered={registered:true,state:'REGISTERED',registration:{node_id:NODE,interlock_id:'SV-IL-'+'b'.repeat(24)},receipts:[{}]};
function harness(serve,opts){opts=opts||{};const seen={queries:[],targets:[],materializations:[]};const canonical=(v)=>JSON.stringify(v);
  const ctx={crypto:globalThis.crypto,TextEncoder,TextDecoder,setTimeout,
    fetch:(url,init)=>{const lookup=JSON.parse(init.body);const m=seen.materializations.find(x=>x.materialization_id===lookup.materialization_id);const q=m.query;
      const response={schema:'stegverse.device-kv.query-response/v1',state:'QUERY_COMPLETE',record_class:opts.responseClass||q.record_class,query_request_id:q.request_id,request_grants_authority:false,response_grants_authority:false,authority_effect:'NONE',projection:serve(q)};
      const text=canonical(response);return Promise.resolve({status:200,json:()=>Promise.resolve({schema:'stegverse.device-kv.query-result-delivery/v1',state:'RESULT_AVAILABLE',materialization_id:m.materialization_id,request_hash:m.request_hash,node_id:NODE,authority_effect:'NONE_RESULT_DELIVERY_ONLY',result_lookup_grants_authority:false,response,response_payload_hash:sha(text),response_carrier_signal:text})});},
    StegVerseGeneratedInTr:{canonical,buildIntent:(k,bytes,op,id)=>Promise.resolve({packet_id:'pkt-'+id,payload_hash:sha(new TextDecoder().decode(bytes))}),buildMaterializationRequest:(k,i,r,b,extra)=>{const q=extra.kv_request;seen.queries.push(q);const m={materialization_id:'mat-'+q.request_id,request_hash:sha(canonical(q)),query:q};seen.materializations.push(m);return Promise.resolve(m);},sha256Bytes:(bytes)=>Promise.resolve(sha(new TextDecoder().decode(bytes)))},
    StegVerseHBInTrCarrier:{buildBinding:()=>Promise.resolve({}),recoverSignal:(signal)=>Promise.resolve(new TextEncoder().encode(signal))},
    StegVerseNodeContinuity:{status:()=>Promise.resolve(registered),registerDevice(){throw new Error('page must not register');},queueIntrMaterializationRequest:()=>Promise.resolve()},
    StegVerseDeviceKVInTrSync:{synchronizeMaterialization:()=>Promise.resolve(),loadTarget:(cls)=>{seen.targets.push(cls);return Promise.resolve({state:'CONFORMING_SOVEREIGN_INTR_INGRESS',runtime_ingress_observed:true,result_url:'https://ingress.invalid/intr/device-kv/result'});},getDeliveryReceipt:()=>Promise.resolve({network_delivery_observed:true})}};
  vm.createContext(ctx);vm.runInContext(nodeBindingSrc,ctx);vm.runInContext(bridgeSrc,ctx);return {bridge:ctx.StegVerseWorkspaceKVBridge,seen};}
(async()=>{
  let h=harness(q=>q.record_class==='WORKSPACE_FAMILY_PROJECTIONS'?familyDelivery():checkpointDelivery());
  check(JSON.stringify(h.bridge.record_classes)==='["WORKSPACE_PERSONAL_PROJECTION","WORKSPACE_TASKS_PROJECTION","WORKSPACE_FAMILY_PROJECTIONS","WORKSPACE_CONTINUITY_CHECKPOINT"]','four admitted classes');
  const list=await h.bridge.loadPersonalProjections({recovery_result:null});
  check(Array.isArray(list)&&list.length===1&&list[0].schema==='stegverse.kv.cryptobot-portfolio-projection/v1','family list delivered: '+JSON.stringify(list).slice(0,120));
  let q=h.seen.queries[0];check(q.record_class==='WORKSPACE_FAMILY_PROJECTIONS'&&JSON.stringify(q.requested_scope)==='["projections"]'&&q.selector.workspace_type==='PERSONAL'&&q.authority_ref==='stegos-node://'+NODE&&/no credential material, provider operation or trade authority/.test(q.minimum_necessary_justification),'family query shape: '+JSON.stringify(q));
  const cp=await h.bridge.loadAssistantCheckpoint({recovery_result:null});
  check(cp&&cp.checkpoint.checkpoint_digest===checkpoint.checkpoint_digest&&cp.decision.disposition==='FAIL_CLOSED'&&cp.decision.replay_status==='UNKNOWN','checkpoint delivered: '+JSON.stringify(cp).slice(0,160));
  q=h.seen.queries[1];check(q.record_class==='WORKSPACE_CONTINUITY_CHECKPOINT'&&JSON.stringify(q.requested_scope)==='["checkpoint","decision"]'&&/nothing is anchored, verified or executed/.test(q.minimum_necessary_justification),'checkpoint query shape: '+JSON.stringify(q));
  check(h.seen.targets.join()==='WORKSPACE_FAMILY_PROJECTIONS,WORKSPACE_CONTINUITY_CHECKPOINT','sync targets per class');
  // Absent checkpoint → null; DENY decision delivered as-is.
  h=harness(()=>checkpointDelivery({state:'KV_CHECKPOINT_ABSENT',checkpoint:null,decision:null}));check((await h.bridge.loadAssistantCheckpoint({recovery_result:null}))===null,'absent checkpoint yields null');
  h=harness(()=>checkpointDelivery({decision:decision('DENY','CHECKPOINT_FORK','REFUSED')}));check((await h.bridge.loadAssistantCheckpoint({recovery_result:null})).decision.predicate==='CHECKPOINT_FORK','DENY decision passed to the consumer');
  h=harness(()=>familyDelivery({state:'KV_FAMILY_PROJECTIONS_EMPTY',projections:[],projection_schemas:[]}));check((await h.bridge.loadPersonalProjections({recovery_result:null})).length===0,'empty family list delivered');
  // Refusals.
  const refuses=async(method,serve,opts,pattern,name)=>{const hh=harness(serve,opts);const err=await hh.bridge[method]({recovery_result:null}).then(()=>null,e=>e);check(err&&pattern.test(err.message),name+': '+(err&&err.message));};
  await refuses('loadPersonalProjections',()=>familyDelivery({projections:[portfolio({schema:'stegverse.kv.personal-workspace-projection/v1'})]}),{},/schema reserved/,'reserved schema in family list');
  await refuses('loadPersonalProjections',()=>familyDelivery({projections:[portfolio(),portfolio()]}),{},/schema ambiguous/,'duplicate family schema');
  await refuses('loadPersonalProjections',()=>familyDelivery({projections:[portfolio({trade_authority_granted:true})]}),{},/authority invalid/,'trade authority in family projection');
  await refuses('loadPersonalProjections',()=>familyDelivery({projections:[portfolio({projection_metadata:null})]}),{},/metadata invalid/,'family projection without metadata');
  await refuses('loadPersonalProjections',()=>familyDelivery({projections:[portfolio({workspace_type:'ORGANIZATIONAL'})]}),{},/authority invalid/,'org family projection');
  await refuses('loadPersonalProjections',()=>familyDelivery({projections:'x'}),{},/rows invalid/,'non-list family payload');
  await refuses('loadPersonalProjections',()=>familyDelivery({action_authority:'ALLOW'}),{},/authority invalid/,'family delivery claiming authority');
  await refuses('loadPersonalProjections',()=>familyDelivery({schema:'other/v1'}),{},/schema invalid/,'wrong family delivery schema');
  await refuses('loadAssistantCheckpoint',()=>checkpointDelivery({anchor_verified:true}),{},/claims verification/,'anchor_verified true');
  await refuses('loadAssistantCheckpoint',()=>checkpointDelivery({decision:decision('ALLOW','FIRST_CHECKPOINT','VERIFIED')}),{},/decision invalid/,'ALLOW decision from the reader');
  await refuses('loadAssistantCheckpoint',()=>checkpointDelivery({decision:decision('FAIL_CLOSED','X','VERIFIED')}),{},/decision invalid/,'VERIFIED replay without ALLOW');
  await refuses('loadAssistantCheckpoint',()=>checkpointDelivery({checkpoint:null}),{},/checkpoint schema invalid/,'present state without checkpoint');
  await refuses('loadAssistantCheckpoint',()=>checkpointDelivery({state:'KV_CHECKPOINT_ABSENT',checkpoint:checkpoint,decision:null}),{},/absent state invalid/,'absent state carrying a checkpoint');
  await refuses('loadAssistantCheckpoint',()=>checkpointDelivery(),{responseClass:'WORKSPACE_FAMILY_PROJECTIONS'},/response invalid/,'class mismatch');
  await refuses('loadAssistantCheckpoint',()=>familyDelivery(),{},/schema invalid/,'family delivery under the checkpoint class');
  console.log('WORKSPACE_DELIVERY_SEAMS_PASS assertions='+n);
})().catch(e=>{console.error(e.stack||e);process.exit(1)});
