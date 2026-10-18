// Node-binding contract (Site#1509 WU2): on a device that has never held a node registration the WorkSpace page never
// registers an identity. It binds a directly observed registration, or an admitted StegOS device-continuity recovery
// result (stegos.device_continuity_recovery_result.v1, StegOS#347) validated fail-closed; otherwise FAIL_CLOSED with the
// work unit and owner named. WU5: storage persistence is requested as an advisory mitigation only.
const fs=require('fs');const path=require('path');const vm=require('vm');
const root=path.join(__dirname,'..');
const src=fs.readFileSync(path.join(root,'assets/workspace-node-binding.js'),'utf8');
const bridgeSrc=fs.readFileSync(path.join(root,'assets/workspace-kv-bridge.js'),'utf8');
const ui=fs.readFileSync(path.join(root,'assets/workspace.js'),'utf8');
const page=fs.readFileSync(path.join(root,'workspace.html'),'utf8');
function assert(ok,msg){if(!ok)throw new Error(msg)}
const canonical=v=>v===null||typeof v!=='object'?JSON.stringify(v):Array.isArray(v)?'['+v.map(canonical).join(',')+']':'{'+Object.keys(v).sort().map(k=>JSON.stringify(k)+':'+canonical(v[k])).join(',')+'}';
const sha256=async v=>Array.from(new Uint8Array(await globalThis.crypto.subtle.digest('SHA-256',new TextEncoder().encode(canonical(v)))),b=>b.toString(16).padStart(2,'0')).join('');
const HEX='a'.repeat(64),HEX2='b'.repeat(64),HEX3='c'.repeat(64);

// The page and the bridge never register a device identity, and nothing reads identity from storage or the URL.
assert(page.indexOf('assets/workspace-node-binding.js')>=0&&page.indexOf('assets/workspace-node-binding.js')<page.indexOf('assets/workspace-kv-bridge.js'),'page must load the node-binding contract before the bridge');
for(const [name,text] of [['bridge',bridgeSrc],['page',ui],['contract',src]])assert(!/registerDevice\s*\(/.test(text),name+' must never register a device identity');
assert(!/localStorage|sessionStorage|indexedDB|location\.(search|hash)|URLSearchParams/.test(src+bridgeSrc+ui),'no identity or recovery input from browser storage or the URL');
assert(ui.includes('loadPersonalWorkspace({recovery_result:null})'),'page supplies no recovery result; it has no authorized channel for one yet');
assert(!/"Register this device before opening Personal Workspace KV context"/.test(bridgeSrc),'bare registration gate string must be gone');

const sandbox={crypto:globalThis.crypto,TextEncoder};vm.createContext(sandbox);vm.runInContext(src,sandbox);
const B=sandbox.StegVerseWorkspaceNodeBinding;
assert(B.schema==='stegverse.workspace.node-binding/v1'&&B.work_unit==='WU2-REGISTRATION-RECOVERY-ON-A-NEW-DEVICE'&&B.recovery_result_schema==='stegos.device_continuity_recovery_result.v1'&&B.authority_effect==='NONE','module identity');

const registered={registered:true,state:'REGISTERED',registration:{schema:'stegos.node_registration_projection.v1',node_id:'node-1',interlock_id:'il-1'},receipts:[{}]};
const unregistered={registered:false,state:'UNREGISTERED',registration:null,receipts:[]};
async function genesis(over){const body=Object.assign({schema:'stegos.node_handoff_receipt.v1',receipt_number:1,transition:'NODE_REGISTERED',prior_state:'UNREGISTERED',resulting_state:'REGISTERED',continuity_parent:'GENESIS',node_id:'node-r',interlock_id:'il-r',device_binding_sha256:HEX,authority_effect:'NONE',heartbeat_authority:'StegVerse-Labs/.github',credential_authority:'TV/TVC'},over||{});return Object.assign({},body,{receipt_sha256:await sha256(body)});}
async function recovery(over,nodeOver,genesisOver){const g=await genesis(genesisOver);const node=Object.assign({node_id:'node-r',interlock_id:'il-r',device_binding_sha256:HEX,device_continuity_id:'stegdevice-abc',genesis_receipt:g,node_binding_receipt_sha256:HEX2},nodeOver||{});
 return Object.assign({schema:'stegos.device_continuity_recovery_result.v1',recovery_state:'ADMITTED_FOR_LOCAL_REHYDRATION',device_continuity_id:'stegdevice-abc',device_continuity_root_sha256:HEX3,continuity_head_sha256:HEX3,capsule_sha256:HEX3,retained_node:node,new_node_minted:false,new_continuity_root_minted:false,browser_context_is_identity:false,credential_authority:'TV/TVC',transition_authority:'Interlock/InTr',github_token_runtime_authority:'NONE',authority_effect:'LOCAL_REHYDRATION_ONLY',network_presence_proven:false,device_kv_runtime_completed:false},over||{});}

(async()=>{
  // Registered-node regression: direct binding, no recovery consulted.
  let d=await B.resolve(registered,null);
  assert(d.disposition==='ALLOW'&&d.predicate==='REGISTERED_NODE_DIRECTLY_OBSERVED'&&d.node_id==='node-1'&&d.source==='DEVICE_LOCAL_REGISTRATION'&&d.identity_minted_by_page===false&&d.node_identity_is_user_principal===false&&d.authority_effect==='NONE','registered node binds directly');
  // New device, no recovery result: fail closed, nothing created, owner and work unit named.
  d=await B.resolve(unregistered,null);
  assert(d.disposition==='FAIL_CLOSED'&&d.predicate==='DEVICE_CONTINUITY_RECOVERY_RESULT_NOT_OBSERVED'&&d.node_id===null&&d.identity_minted_by_page===false,'unregistered device fails closed');
  assert(d.work_unit==='WU2-REGISTRATION-RECOVERY-ON-A-NEW-DEVICE'&&d.recovery_contract.schema==='stegos.device_continuity_recovery_result.v1'&&/StegOS#347/.test(d.recovery_contract.owner),'refusal names the work unit and recovery owner');
  assert(JSON.stringify(await B.resolve(null,undefined))===JSON.stringify(d),'absent status is the same refusal');
  // Admitted recovery with an exact Receipt #1 binds the retained node without minting.
  const good=await recovery();
  d=await B.resolve(unregistered,good);
  assert(d.disposition==='ALLOW'&&d.predicate==='RETAINED_NODE_REHYDRATION_ADMITTED'&&d.node_id==='node-r'&&d.source==='ADMITTED_DEVICE_CONTINUITY_RECOVERY'&&d.identity_minted_by_page===false,'admitted recovery binds: '+d.predicate);
  assert(JSON.stringify(d.lineage)===JSON.stringify({device_continuity_id:'stegdevice-abc',capsule_sha256:HEX3,node_binding_receipt_sha256:HEX2,genesis_receipt_sha256:good.retained_node.genesis_receipt.receipt_sha256}),'lineage carried');
  // A directly observed registration wins over any recovery input.
  assert((await B.resolve(registered,good)).predicate==='REGISTERED_NODE_DIRECTLY_OBSERVED','direct registration precedes recovery');
  // Denied, revoked, stale, tampered or authority-claiming recovery results are non-ALLOW with no side effects.
  const cases=[
    ['schema','RECOVERY_RESULT_SCHEMA_INVALID',await recovery({schema:'other'})],
    ['string','RECOVERY_RESULT_SCHEMA_INVALID','recovered'],
    ['denied','RECOVERY_NOT_ADMITTED',await recovery({recovery_state:'DENIED'})],
    ['revoked','RECOVERY_NOT_ADMITTED',await recovery({recovery_state:'REVOKED'})],
    ['stale','RECOVERY_NOT_ADMITTED',await recovery({recovery_state:'STALE'})],
    ['minted node','RECOVERY_MINTED_IDENTITY',await recovery({new_node_minted:true})],
    ['minted root','RECOVERY_MINTED_IDENTITY',await recovery({new_continuity_root_minted:true})],
    ['browser identity','RECOVERY_MINTED_IDENTITY',await recovery({browser_context_is_identity:true})],
    ['credential authority','RECOVERY_AUTHORITY_INVALID',await recovery({credential_authority:'GITHUB_TOKEN'})],
    ['transition authority','RECOVERY_AUTHORITY_INVALID',await recovery({transition_authority:'NONE'})],
    ['github runtime','RECOVERY_AUTHORITY_INVALID',await recovery({github_token_runtime_authority:'ALLOW'})],
    ['authority effect','RECOVERY_AUTHORITY_INVALID',await recovery({authority_effect:'ACTIVATE'})],
    ['no retained node','RECOVERY_RETAINED_NODE_ABSENT',await recovery({retained_node:null})],
    ['continuity mismatch','RECOVERY_CONTINUITY_MISMATCH',await recovery({},{device_continuity_id:'stegdevice-other'})],
    ['bad continuity id','RECOVERY_CONTINUITY_MISMATCH',await recovery({device_continuity_id:'device-1'},{device_continuity_id:'device-1'})],
    ['genesis schema','RECOVERY_GENESIS_RECEIPT_INVALID',await recovery({},{},{schema:'other'})],
    ['genesis receipt number','RECOVERY_GENESIS_RECEIPT_INVALID',await recovery({},{},{receipt_number:2})],
    ['genesis authority','RECOVERY_GENESIS_RECEIPT_INVALID',await recovery({},{},{authority_effect:'ALLOW'})],
    ['node id mismatch','RECOVERY_NODE_BINDING_MISMATCH',await recovery({},{node_id:'node-x'})],
    ['device binding mismatch','RECOVERY_NODE_BINDING_MISMATCH',await recovery({},{device_binding_sha256:HEX2})],
  ];
  for(const [name,pred,input] of cases){const r=await B.resolve(unregistered,input);assert(r.disposition==='FAIL_CLOSED'&&r.predicate===pred&&r.node_id===null,name+': expected '+pred+' got '+r.disposition+'/'+r.predicate);}
  // Tampered genesis receipt body: digest mismatch.
  const tampered=await recovery();tampered.retained_node.genesis_receipt.heartbeat_authority='attacker';
  assert((await B.resolve(unregistered,tampered)).predicate==='RECOVERY_GENESIS_DIGEST_MISMATCH','tampered genesis receipt must fail the digest check');
  assert(JSON.stringify(await B.resolve(unregistered,good))===JSON.stringify(await B.resolve(unregistered,JSON.parse(JSON.stringify(good)))),'deterministic');

  // Bridge harness: a node continuity stub whose registerDevice must never be called.
  function bridgeCtx(status,extra){
    const calls={register:0,rehydrate:0,queue:0};
    const node=Object.assign({status:()=>Promise.resolve(status),registerDevice(){calls.register++;throw new Error('page must not register');},queueIntrMaterializationRequest(){calls.queue++;return Promise.resolve();}},extra||{});
    const ctx={crypto:globalThis.crypto,TextEncoder,TextDecoder,fetch:()=>Promise.reject(new Error('no network')),setTimeout,
      StegVerseGeneratedInTr:{buildIntent:()=>Promise.reject(new Error('STOP_AT_INTENT')),buildMaterializationRequest:()=>Promise.reject(new Error('x')),canonical:JSON.stringify,sha256Bytes:()=>Promise.resolve('')},
      StegVerseHBInTrCarrier:{buildBinding:()=>Promise.resolve({}),recoverSignal:()=>Promise.resolve(new Uint8Array())},
      StegVerseNodeContinuity:node,
      StegVerseDeviceKVInTrSync:{synchronizeMaterialization:()=>Promise.resolve(),loadTarget:()=>Promise.resolve(),getDeliveryReceipt:()=>Promise.resolve()}};
    vm.createContext(ctx);vm.runInContext(src,ctx);vm.runInContext(bridgeSrc,ctx);
    return {ctx,calls,bridge:ctx.StegVerseWorkspaceKVBridge};
  }
  // Registered device: proceeds past node binding to the connector (regression).
  let h=bridgeCtx(registered);let err=await h.bridge.loadPersonalWorkspace({recovery_result:null}).then(()=>null,e=>e);
  assert(err&&err.message==='STOP_AT_INTENT'&&h.bridge.lastNodeBinding().predicate==='REGISTERED_NODE_DIRECTLY_OBSERVED'&&h.calls.register===0,'registered path proceeds to the connector: '+(err&&err.message));
  // Unregistered device, no recovery: structured refusal, no registration, no queueing.
  h=bridgeCtx(unregistered);err=await h.bridge.loadPersonalWorkspace({recovery_result:null}).then(()=>null,e=>e);
  assert(err&&err.decision&&err.decision.disposition==='FAIL_CLOSED'&&err.decision.predicate==='DEVICE_CONTINUITY_RECOVERY_RESULT_NOT_OBSERVED'&&err.message==='FAIL_CLOSED: DEVICE_CONTINUITY_RECOVERY_RESULT_NOT_OBSERVED','unregistered refusal: '+(err&&err.message));
  assert(h.calls.register===0&&h.calls.queue===0&&h.calls.rehydrate===0,'no side effects on refusal');
  // Omitting options is the same as no recovery.
  h=bridgeCtx(unregistered);err=await h.bridge.loadPersonalWorkspace().then(()=>null,e=>e);
  assert(err&&err.decision&&err.decision.predicate==='DEVICE_CONTINUITY_RECOVERY_RESULT_NOT_OBSERVED','no options is no recovery');
  // Admitted recovery but the node continuity has no rehydration interface: fail closed, owner named, nothing minted.
  h=bridgeCtx(unregistered);err=await h.bridge.loadPersonalWorkspace({recovery_result:good}).then(()=>null,e=>e);
  assert(err&&err.decision&&err.decision.predicate==='LOCAL_REHYDRATION_INTERFACE_NOT_AVAILABLE'&&err.decision.node_id==='node-r'&&/stegverse-node-continuity-impl/.test(err.decision.rehydration_owner)&&h.calls.register===0,'rehydration seam absent: '+(err&&err.message));
  // The refusal carries the six actionable fields (Organization Role item 5).
  ['failure_code','failed_predicate','required_evidence_or_repair','retry_entrypoint','owning_existing_goal','next_attempt'].forEach(function(k){assert(typeof err.decision[k]==='string'&&err.decision[k].length>0,'rehydration refusal lacks '+k);});
  assert(err.decision.failed_predicate===err.decision.predicate&&err.decision.owning_existing_goal==='STEGVERSE-WORKSPACE-ANY-DEVICE-KV-SURFACE-001','rehydration refusal fields consistent');
  // Denied recovery with a rehydration interface present: refused before the interface is touched.
  let rehydrated=false;
  h=bridgeCtx(unregistered,{rehydrateRegistration(){rehydrated=true;return Promise.resolve();}});
  err=await h.bridge.loadPersonalWorkspace({recovery_result:await recovery({recovery_state:'DENIED'})}).then(()=>null,e=>e);
  assert(err&&err.decision&&err.decision.predicate==='RECOVERY_NOT_ADMITTED'&&rehydrated===false&&h.calls.register===0,'denied recovery never rehydrates');
  // Admitted recovery with a rehydration interface: rehydrate, re-read status, require the same retained node, then proceed.
  let statusNow=unregistered;
  h=bridgeCtx(unregistered,{status:()=>Promise.resolve(statusNow),rehydrateRegistration(r){rehydrated=true;statusNow={registered:true,registration:{node_id:r.retained_node.node_id,interlock_id:r.retained_node.interlock_id}};return Promise.resolve();}});
  err=await h.bridge.loadPersonalWorkspace({recovery_result:good}).then(()=>null,e=>e);
  assert(rehydrated===true&&err&&err.message==='STOP_AT_INTENT'&&h.bridge.lastNodeBinding().predicate==='RETAINED_NODE_REHYDRATION_ADMITTED'&&h.calls.register===0,'admitted recovery proceeds through rehydration: '+(err&&err.message));
  // A rehydration that yields a different node than admitted fails closed.
  statusNow=unregistered;
  h=bridgeCtx(unregistered,{status:()=>Promise.resolve(statusNow),rehydrateRegistration(){statusNow={registered:true,registration:{node_id:'node-other'}};return Promise.resolve();}});
  err=await h.bridge.loadPersonalWorkspace({recovery_result:good}).then(()=>null,e=>e);
  assert(err&&/rehydrated registration does not match/.test(err.message),'mismatched rehydration must fail closed: '+(err&&err.message));

  // Page: runtime state and KV gate show the structured refusal; WU5 persistence is advisory and tolerant of absence.
  const ids=['workspaceSwitch','workspaceRuntimeState','contextTitle','assistant','search','feed','contacts','organizations','memberships','kvGate','intentDraft','capabilities'];
  function uiHarness(bridge,navigator){const els={};ids.forEach(i=>els[i]={id:i,innerHTML:'',textContent:'',className:'',value:'',dataset:{},attrs:{},setAttribute(k,v){this.attrs[k]=v},removeAttribute(k){delete this.attrs[k]},classList:{add(){},remove(){}},listeners:{},addEventListener(t,f){this.listeners[t]=f},scrollIntoView(){}});
    const ctx={document:{body:{dataset:{}},querySelector:s=>els[s.replace('#','')]||null,querySelectorAll:()=>[],getElementById:i=>els[i]||null,addEventListener(){}},console,fetch:()=>Promise.resolve({json:()=>Promise.resolve({})}),window:{StegVerseWorkspaceKVBridge:bridge,navigator}};
    vm.createContext(ctx);vm.runInContext(ui,ctx);return els;}
  const refusal=Object.assign(new Error('FAIL_CLOSED: DEVICE_CONTINUITY_RECOVERY_RESULT_NOT_OBSERVED'),{decision:await B.resolve(unregistered,null)});
  let els=uiHarness({loadPersonalWorkspace:()=>Promise.reject(refusal),lastNodeBinding:()=>refusal.decision},{storage:{persist:()=>Promise.resolve(false)}});
  await new Promise(r=>setTimeout(r,10));
  assert(els.workspaceRuntimeState.textContent.includes('FAIL_CLOSED · DEVICE_CONTINUITY_RECOVERY_RESULT_NOT_OBSERVED')&&els.workspaceRuntimeState.textContent.includes('no device identity was registered'),'runtime state must show the structured refusal: '+els.workspaceRuntimeState.textContent);
  assert(els.kvGate.innerHTML.includes('Node binding: FAIL_CLOSED')&&els.kvGate.innerHTML.includes('WU2-REGISTRATION-RECOVERY-ON-A-NEW-DEVICE')&&els.kvGate.innerHTML.includes('StegOS#347'),'KV gate must name the work unit and owner: '+els.kvGate.innerHTML);
  assert(els.kvGate.innerHTML.includes('PERSISTENT_STORAGE_REFUSED')&&els.kvGate.innerHTML.includes('never the projection'),'refused persistence is shown as advisory');
  els=uiHarness({loadPersonalWorkspace:()=>Promise.reject(refusal),lastNodeBinding:()=>refusal.decision},undefined);
  await new Promise(r=>setTimeout(r,10));
  assert(els.kvGate.innerHTML.includes('PERSISTENCE_API_UNAVAILABLE'),'absent persistence API is reported, not fatal');
  els=uiHarness({loadPersonalWorkspace:()=>Promise.resolve({schema:'stegverse.kv.personal-workspace-projection/v1',state:'KV_WORKSPACE_EMPTY',workspace_type:'PERSONAL',principals:[],relationships:[],organizations:[],memberships:[],feed:[],assistant:null,projection_metadata:null}),lastNodeBinding:()=>({disposition:'ALLOW',predicate:'REGISTERED_NODE_DIRECTLY_OBSERVED',node_id:'node-1',source:'DEVICE_LOCAL_REGISTRATION',work_unit:'WU2-REGISTRATION-RECOVERY-ON-A-NEW-DEVICE',recovery_contract:{schema:'x',owner:'y'}})},{storage:{persist:()=>Promise.resolve(true)}});
  await new Promise(r=>setTimeout(r,10));
  assert(els.kvGate.innerHTML.includes('Node binding: ALLOW · REGISTERED_NODE_DIRECTLY_OBSERVED · node node-1')&&els.kvGate.innerHTML.includes('PERSISTENT_STORAGE_GRANTED'),'registered path renders: '+els.kvGate.innerHTML);
  console.log('WORKSPACE_NODE_BINDING_PASS');
})().catch(e=>{console.error(e);process.exit(1)});
