// WS-TASKS delivery (Site#1509): the DEVICE_KV bridge serves the tasks projection through the same node-bound InTr
// request / HB return / exact-recovery path as the personal projection, bound to WORKSPACE_TASKS_PROJECTION with its own
// scope list and validator. The page's loadPersonalTasks seam is now implemented by the bridge; a projection that claims
// eligibility, authority or the wrong class is refused; nothing registers a device or grants authority.
const fs=require('fs');const path=require('path');const vm=require('vm');const nodeCrypto=require('crypto');
const root=path.join(__dirname,'..');
const read=f=>fs.readFileSync(path.join(root,f),'utf8');
const bridgeSrc=read('assets/workspace-kv-bridge.js'),nodeBindingSrc=read('assets/workspace-node-binding.js'),ui=read('assets/workspace.js');
function assert(ok,msg){if(!ok)throw new Error(msg)}
let n=0;const check=(ok,msg)=>{n++;assert(ok,msg)};
check(bridgeSrc.includes('loadPersonalTasks:loadPersonalTasks')&&bridgeSrc.includes('TASKS_RECORD_CLASS="WORKSPACE_TASKS_PROJECTION"'),'bridge exports loadPersonalTasks for the tasks record class');
check(!/registerDevice\(/.test(bridgeSrc.replace(/\/\/.*$/gm,''))&&!/localStorage|sessionStorage|indexedDB/.test(bridgeSrc),'bridge never registers a device or uses browser storage');
check(ui.includes('bridge.loadPersonalTasks')&&ui.includes('applyTasksProjection'),'page consumes the seam');
const REV='a'.repeat(64);
const sha=(s)=>nodeCrypto.createHash('sha256').update(s,'utf8').digest('hex');
const tasksProjection=(extra)=>Object.assign({schema:'stegverse.kv.workspace-tasks-projection/v1',state:'KV_TASKS_PROJECTED',workspace_type:'PERSONAL',
  tasks:[{task_id:'t-1',title:'Real',status:'OPEN',due_at:'2026-10-12T09:00:00Z',created_at:null,source_ref:null,action_eligible:false,execution_requires_admitted_manifest:true,authority_effect:'NONE'}],
  commitments:[],timeline:[{kind:'task',id:'t-1',label:'Real',status:'OPEN',due_at:'2026-10-12T09:00:00Z',action_eligible:false,execution_requires_admitted_manifest:true,authority_effect:'NONE'}],
  credential_material_present:false,provider_operation_authorized:false,workspace_grants_authority:false,action_authority:'NONE',
  projection_metadata:{schema:'stegverse.kv.workspace-projection-metadata/v1',observed_at:'2026-10-11T03:00:00Z',observed_at_semantics:'KV_PROJECTION_PRODUCTION_TIME',source_revision:REV,provenance_ref:'kv-workspace-tasks-source:sha256:'+REV,workspace_type:'PERSONAL',workspace_id:null,owner_principal_id:null,grant_state:'UNKNOWN',revocation_epoch:null,authority_effect:'NONE'},authority_effect:'NONE'},extra||{});
const personalProjection=()=>({schema:'stegverse.kv.personal-workspace-projection/v1',workspace_type:'PERSONAL',state:'KV_WORKSPACE_EMPTY',principals:[],organizations:[],memberships:[],feed:[],assistant:null,credential_material_present:false,provider_operation_authorized:false,workspace_grants_authority:false,authority_effect:'NONE'});
const NODE='SV-NODE-'+'a'.repeat(24);
const registered={registered:true,state:'REGISTERED',registration:{node_id:NODE,interlock_id:'SV-IL-'+'b'.repeat(24)},receipts:[{}]};
// Full-path harness: every connector is a stub that records what the bridge asked for and serves `serve(query)` back
// through the delivery/HB-return shape the bridge verifies (payload hash, exact canonical recovery, class binding).
function harness(serve,opts){
  opts=opts||{};const seen={queries:[],targets:[],materializations:[]};
  const canonical=(v)=>JSON.stringify(v);
  const ctx={crypto:globalThis.crypto,TextEncoder,TextDecoder,setTimeout,
    fetch:(url,init)=>{const lookup=JSON.parse(init.body);const m=seen.materializations.find(x=>x.materialization_id===lookup.materialization_id);const q=m.query;
      const response=Object.assign({schema:'stegverse.device-kv.query-response/v1',state:'QUERY_COMPLETE',record_class:opts.responseClass||q.record_class,query_request_id:q.request_id,request_grants_authority:false,response_grants_authority:false,authority_effect:'NONE',projection:serve(q)},opts.responsePatch||{});
      const text=canonical(response);const delivery={schema:'stegverse.device-kv.query-result-delivery/v1',state:'RESULT_AVAILABLE',materialization_id:m.materialization_id,request_hash:m.request_hash,node_id:NODE,authority_effect:'NONE_RESULT_DELIVERY_ONLY',result_lookup_grants_authority:false,response:response,response_payload_hash:sha(text),response_carrier_signal:text};
      return Promise.resolve({status:200,json:()=>Promise.resolve(delivery)});},
    StegVerseGeneratedInTr:{canonical,buildIntent:(kind,bytes,op,id)=>Promise.resolve({packet_id:'pkt-'+id,payload_hash:sha(new TextDecoder().decode(bytes))}),
      buildMaterializationRequest:(kind,intent,ref,binding,extra)=>{const q=extra.kv_request;seen.queries.push(q);const m={materialization_id:'mat-'+q.request_id,request_hash:sha(canonical(q)),query:q};seen.materializations.push(m);return Promise.resolve(m);},
      sha256Bytes:(bytes)=>Promise.resolve(sha(new TextDecoder().decode(bytes)))},
    StegVerseHBInTrCarrier:{buildBinding:()=>Promise.resolve({}),recoverSignal:(signal)=>Promise.resolve(new TextEncoder().encode(signal))},
    StegVerseNodeContinuity:{status:()=>Promise.resolve(registered),registerDevice(){throw new Error('page must not register');},queueIntrMaterializationRequest:()=>Promise.resolve()},
    StegVerseDeviceKVInTrSync:{synchronizeMaterialization:()=>Promise.resolve(),loadTarget:(cls)=>{seen.targets.push(cls);return Promise.resolve({state:'CONFORMING_SOVEREIGN_INTR_INGRESS',runtime_ingress_observed:true,result_url:'https://ingress.invalid/intr/device-kv/result'});},getDeliveryReceipt:()=>Promise.resolve({network_delivery_observed:true})}};
  vm.createContext(ctx);vm.runInContext(nodeBindingSrc,ctx);vm.runInContext(bridgeSrc,ctx);
  return {bridge:ctx.StegVerseWorkspaceKVBridge,seen};
}
(async()=>{
  // Tasks delivery through the real bridge path.
  let h=harness(q=>q.record_class==='WORKSPACE_TASKS_PROJECTION'?tasksProjection():personalProjection());
  check(JSON.stringify(h.bridge.record_classes)==='["WORKSPACE_PERSONAL_PROJECTION","WORKSPACE_TASKS_PROJECTION"]','bridge declares exactly the two admitted classes');
  const t=await h.bridge.loadPersonalTasks({recovery_result:null});
  check(t.schema==='stegverse.kv.workspace-tasks-projection/v1'&&t.tasks.length===1&&t.tasks[0].task_id==='t-1','tasks projection delivered: '+JSON.stringify(t).slice(0,200));
  const q=h.seen.queries[0];
  check(q.record_class==='WORKSPACE_TASKS_PROJECTION'&&JSON.stringify(q.requested_scope)==='["tasks","commitments","timeline"]'&&q.selector.workspace_type==='PERSONAL'&&q.authority_ref==='stegos-node://'+NODE&&q.disclosure_mode==='BOUNDED_CONTEXT'&&q.requester.component==='Workspace'&&/tasks and commitments/.test(q.purpose)&&/no execution/.test(q.minimum_necessary_justification),'tasks query shape matches the .github extension contract: '+JSON.stringify(q));
  check(h.seen.targets[0]==='WORKSPACE_TASKS_PROJECTION','sync target resolved for the tasks class');
  // Personal projection still travels under its own class and scopes.
  const p=await h.bridge.loadPersonalWorkspace({recovery_result:null});
  check(p.schema==='stegverse.kv.personal-workspace-projection/v1'&&h.seen.queries[1].record_class==='WORKSPACE_PERSONAL_PROJECTION'&&h.seen.queries[1].requested_scope.length===7,'personal query unchanged');
  // Refusals: eligibility claims, authority claims, wrong schema, class mismatch in the response, missing metadata.
  const refuses=async(serve,opts,pattern,name)=>{const hh=harness(serve,opts);const err=await hh.bridge.loadPersonalTasks({recovery_result:null}).then(()=>null,e=>e);check(err&&pattern.test(err.message),name+': '+(err&&err.message));};
  await refuses(()=>tasksProjection({tasks:[Object.assign({},tasksProjection().tasks[0],{action_eligible:true})]}),{},/claims eligibility/,'eligible row refused');
  await refuses(()=>tasksProjection({timeline:[Object.assign({},tasksProjection().timeline[0],{execution_requires_admitted_manifest:false})]}),{},/claims eligibility/,'timeline row without manifest requirement refused');
  await refuses(()=>tasksProjection({action_authority:'ALLOW'}),{},/authority invalid/,'action authority refused');
  await refuses(()=>tasksProjection({workspace_grants_authority:true}),{},/authority invalid/,'workspace authority refused');
  await refuses(()=>tasksProjection({workspace_type:'ORGANIZATIONAL'}),{},/type invalid/,'org tasks refused');
  await refuses(()=>tasksProjection({state:'KV_TASKS_EXECUTED'}),{},/state invalid/,'unknown state refused');
  await refuses(()=>personalProjection(),{},/schema invalid/,'personal projection under the tasks class refused');
  await refuses(()=>tasksProjection({projection_metadata:null}),{},/metadata invalid/,'missing metadata refused');
  await refuses(()=>tasksProjection(),{responseClass:'WORKSPACE_PERSONAL_PROJECTION'},/response invalid/,'response under another class refused');
  await refuses(()=>tasksProjection(),{responsePatch:{response_grants_authority:true}},/authority\/binding invalid/,'response claiming authority refused');
  // Empty registry is a valid delivery.
  h=harness(()=>tasksProjection({state:'KV_TASKS_EMPTY',tasks:[],commitments:[],timeline:[]}));
  const e=await h.bridge.loadPersonalTasks({recovery_result:null});check(e.state==='KV_TASKS_EMPTY'&&e.tasks.length===0,'empty tasks registry delivered');
  console.log('WORKSPACE_TASKS_DELIVERY_PASS assertions='+n);
})().catch(e=>{console.error(e.stack||e);process.exit(1)});
