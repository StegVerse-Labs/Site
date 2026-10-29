// ACTIONS BY MANIFEST (.github data/task-registry-global-invariants.json semantics.actions_by_manifest;
// NO_DESTINATION_LIVENESS_OR_ALWAYS_ON_RECEIVER_AS_TRANSITION_PREDICATE): the MyKV instance, MyKV set-projection
// admission and cloud-KV adoption bridges queue the request durably in the Node outbox, post the trigger to the
// resident receiver without awaiting a reply, and look the persisted result up exactly once. A result that is not
// materialized is an actionable six-field FAIL_CLOSED; nothing waits on receiver activation or a receiver reply.
// The real resident receivers run in their own vm context over a shared fake IndexedDB.
const fs=require('fs');const path=require('path');const vm=require('vm');const nodeCrypto=require('crypto');
const root=path.join(__dirname,'..');
const read=f=>fs.readFileSync(path.join(root,f),'utf8');
const SIX=['failure_code','failed_predicate','required_evidence_or_repair','retry_entrypoint','owning_existing_goal','next_attempt'];
const GOAL='STEGVERSE-WORKSPACE-ANY-DEVICE-KV-SURFACE-001';
const BRIDGES={
  instance:{file:'assets/my-kv-instance-device-kv-bridge.js',receiver:'assets/my-kv-n-device-kv-receiver.js',global:'StegVerseMyKVInstanceBridge',entry:'my-kv-instances.html'},
  admission:{file:'assets/my-kv-set-projection-admission-bridge.js',receiver:'assets/my-kv-set-projection-admission-receiver.js',global:'StegVerseMyKVSetProjectionAdmissionBridge',entry:'my-kv-instances.html'},
  cloud:{file:'assets/cloud-kv-adoption-device-kv-bridge.js',receiver:'assets/cloud-kv-adoption-device-kv-receiver.js',global:'StegVerseCloudKVAdoptionTransport',entry:'cloud-kv-peers.html'}
};
const failures=[];let n=0;
const check=(ok,msg)=>{n++;if(!ok)throw new Error(msg);};
const canon=v=>{if(v===null||typeof v!=='object')return JSON.stringify(v);if(Array.isArray(v))return '['+v.map(canon).join(',')+']';return '{'+Object.keys(v).sort().map(k=>JSON.stringify(k)+':'+canon(v[k])).join(',')+'}';};
const shaUri=v=>'sha256:'+nodeCrypto.createHash('sha256').update(canon(v),'utf8').digest('hex');
const clone=v=>v==null?v:JSON.parse(JSON.stringify(v));

// Minimal IndexedDB: databases, stores with keyPath, get/put/add, upgrade (abortable), tx complete/abort.
function makeIDB(){
  const dbs=new Map();
  function connection(db){return {
    objectStoreNames:{contains:name=>db.stores.has(name)},
    createObjectStore(name,opts){db.stores.set(name,{keyPath:opts.keyPath,rows:new Map()});},
    close(){},
    transaction(name){
      const store=db.stores.get(name);if(!store){const e=new Error('One of the specified object stores was not found.');e.name='NotFoundError';throw e;}
      const ops=[];let aborted=false;
      const tx={abort(){aborted=true;},objectStore(){return {
        get(key){const r={};ops.push(()=>{r.result=clone(store.rows.get(key));if(r.onsuccess)r.onsuccess();});return r;},
        put(row){store.rows.set(row[store.keyPath],clone(row));},
        add(row){store.rows.set(row[store.keyPath],clone(row));}
      };}};
      setImmediate(()=>{for(let i=0;i<ops.length&&!aborted;i++)ops[i]();if(aborted){if(tx.onabort)tx.onabort();}else if(tx.oncomplete)tx.oncomplete();});
      return tx;
    }
  };}
  function openInto(req,name,version){
    let db=dbs.get(name);const target=version||(db?db.version:1);
    if(db&&target<db.version){req.error={name:'VersionError'};if(req.onerror)req.onerror({preventDefault(){}});return;}
    if(!db||target>db.version){
      const next={version:target,stores:db?db.stores:new Map()};let aborted=false;
      req.result=connection(next);req.transaction={abort(){aborted=true;}};
      if(req.onupgradeneeded)req.onupgradeneeded({});
      if(aborted){req.error={name:'AbortError'};if(req.onerror)req.onerror({preventDefault(){}});return;}
      dbs.set(name,next);db=next;
    }
    req.result=connection(db);if(req.onsuccess)req.onsuccess();
  }
  return {dbs,openInto,indexedDB:{open(name,version){const req={};setImmediate(()=>openInto(req,name,version));return req;}}};
}

function makeWorld(opts){
  opts=opts||{};
  const idb=makeIDB(),seen={queued:0,posts:0,lookups:0,timers:0,registers:0,listeners:0},pending=[];
  const NODE='SV-NODE-'+'a'.repeat(24),IL='SV-IL-'+'b'.repeat(24);let counter=0;
  // Resident receiver in its own context, sharing only the fake IndexedDB.
  let receiverHandler=null;
  if(opts.receiver){
    const rctx={self:{addEventListener(type,fn){if(type==='message')receiverHandler=fn;},skipWaiting(){return Promise.resolve();}},crypto:globalThis.crypto,TextEncoder,TextDecoder,atob,btoa,Uint8Array,indexedDB:idb.indexedDB,console};
    vm.createContext(rctx);vm.runInContext(read(opts.receiver),rctx);
  }
  const worker={state:'installing',addEventListener(){seen.listeners++;},postMessage(msg,ports){seen.posts++;
    if(opts.persist)opts.persist(clone(msg),idb);
    if(receiverHandler)receiverHandler({data:clone(msg),ports:[{postMessage(m){if(process.env.DEBUG_RECEIVER)console.error("receiver reply",JSON.stringify(m).slice(0,200));}}],waitUntil(p){pending.push(Promise.resolve(p).catch(()=>{}));}});}};
  // The page reads the shared store; the harness lets an attached receiver finish first (materialized-before-lookup).
  const pageIDB={open(name,version){seen.lookups++;const req={};Promise.all(pending).then(()=>setImmediate(()=>idb.openInto(req,name,version)));return req;}};
  const MessageChannelFake=function(){this.port1={close(){},set onmessage(fn){seen.listeners++;}};this.port2={};};
  const ctx={crypto:globalThis.crypto,TextEncoder,TextDecoder,atob,btoa,Uint8Array,console,isSecureContext:true,
    setTimeout:()=>{seen.timers++;},setInterval:()=>{seen.timers++;},
    MessageChannel:MessageChannelFake,indexedDB:pageIDB,
    navigator:opts.noServiceWorker?{}:{serviceWorker:{register(){seen.registers++;return Promise.resolve({active:null,waiting:null,installing:worker});}}},
    StegVerseGeneratedInTr:{canonical:canon,
      buildIntent:(k,bytes,op,id)=>Promise.resolve({packet_id:'pkt-'+id,payload_hash:'sha256:'+nodeCrypto.createHash('sha256').update(Buffer.from(bytes)).digest('hex')}),
      buildMaterializationRequest:(k,intent,ref,binding,extra)=>{const req={schema:'stegverse.universal-intr-materialization-request/v1',state:'QUEUED_FOR_EVENT_EPHEMERAL_MATERIALIZATION',materialization_id:'INTR-MAT-'+String(++counter).padStart(24,'0'),destination:{boundary:'KV',subsystem:'KnowledgeVault:Interlock'},downstream_owner_ref:'StegVerse-Labs/continuity-vault-kit#79',request_grants_execution_authority:false,transport_grants_execution_authority:false,claim_or_fence_minted:false,credential_authority:'TV/TVC',github_token_runtime_authority:'NONE',kv_request:clone(extra.kv_request)};req.request_hash=shaUri(req);return Promise.resolve(req);}},
    StegVerseHBInTrCarrier:{buildBinding:()=>Promise.resolve({})},
    StegVerseNodeContinuity:{status:()=>Promise.resolve({registered:true,registration:{node_id:NODE,interlock_id:IL}}),
      queueIntrMaterializationRequest:(m)=>{seen.queued++;if(opts.legacyOutbox){const e=new Error('One of the specified object stores was not found.');e.name='NotFoundError';return Promise.reject(e);}
        const entry={schema:'stegos.node_intr_outbox_entry.v1',state:'LOCAL_OUTBOX_PENDING_NETWORK_DELIVERY',node_id:NODE,interlock_id:IL,materialization_id:m.materialization_id,materialization_request:clone(m),credential_authority:'TV/TVC',github_token_runtime_authority:'NONE',request_grants_execution_authority:false,claim_or_fence_minted:false};entry.outbox_entry_hash=shaUri(entry);return Promise.resolve(entry);}}};
  vm.createContext(ctx);
  return {ctx,idb,seen,NODE};
}
function load(world,key){vm.runInContext(read(BRIDGES[key].file),world.ctx);return world.ctx[BRIDGES[key].global];}
function assertDisposition(e,key,world){
  check(e&&typeof e.message==="string"&&/^FAIL_CLOSED: DEVICE_KV_RESULT_NOT_YET_MATERIALIZED/.test(e.message),key+': not-materialized is FAIL_CLOSED DEVICE_KV_RESULT_NOT_YET_MATERIALIZED: '+(e&&e.message));
  const d=e.actionable_disposition;
  check(d&&SIX.every(k=>typeof d[k]==='string'&&d[k].trim())&&Object.keys(d).length===6,key+': carries exactly the six actionable fields: '+JSON.stringify(d));
  check(d.failure_code==='DEVICE_KV_RESULT_NOT_YET_MATERIALIZED'&&d.failed_predicate===d.failure_code&&d.owning_existing_goal===GOAL,key+': predicate and owning goal');
  check(d.retry_entrypoint===BRIDGES[key].entry&&fs.existsSync(path.join(root,d.retry_entrypoint)),key+': retry entry point exists: '+d.retry_entrypoint);
  check(!/\bwait (for|on|until)\b/i.test(d.next_attempt+' '+d.required_evidence_or_repair)&&/nothing waits/.test(d.next_attempt),key+': nothing tells a person to wait');
  check(typeof e.materialization_id==='string'&&d.required_evidence_or_repair.includes(e.materialization_id),key+': the disposition names the durably queued materialization');
  check(world.seen.queued===1&&world.seen.lookups===1&&world.seen.timers===0&&world.seen.listeners===0,key+': queued once, looked up once, no timer, no reply listener: '+JSON.stringify(world.seen));
}
const rejectOf=p=>p.then(()=>null,e=>e);

// Fixtures.
function setProjection(){return {schema:'stegverse.kv.my-kv-set-projection/v1',kv_set_id:'personal',instances:[{schema:'stegverse.kv.my-kv-instance-projection/v1',instance_id:'kvi_test0001',instance_number:1,logical_name:'KV #1',kv_set_id:'personal',storage:{medium:'google-drive',locator:'drive-folder:test',provider_authority_effect:'NONE'},relationship:{tier:'NOT_CONNECTED',governance_state:'NOT_CONNECTED',last_admitted_request_id:null,pending_request_ids:[]},providers:{items:{},pending_requests:[],provider_mutation_authorized:false,credential_material_included:false},management:{request_connect_supported:true,request_disconnect_supported:true,request_verify_supported:true,request_read_supported:true,request_write_supported:true,request_sync_supported:true,request_tier_change_supported:true,provider_mutation_authorized:false,relationship_mutation_authorized:false},private_content_included:false,credential_material_included:false,authority_effect:'NONE_STATUS_ONLY',activation_effect:false}],instance_count:1,private_content_included:false,credential_material_included:false,authority_effect:'NONE_STATUS_ONLY',activation_effect:false};}
const providerReq={schema:'stegverse.site.my-kv.provider-operation-request/v1',kv_set_id:'personal',instance_id:'kvi_1',provider_id:'icloud',operation:'CONNECT',governance_state:'PENDING_INTERLOCK_INTR',credential_destination:'SKAP_VAULT',credential_material_present:false,provider_operation_authorized:false,authority_effect:'NONE_REQUEST_ONLY',activation_effect:false};
const relationshipReq={schema:'stegverse.site.my-kv.relationship-transition-request/v1',kv_set_id:'personal',participant_instance_ids:['kvi_1','kvi_2'],current_tier:'NOT_CONNECTED',target_tier:'CONNECTED',governance_state:'PENDING_INTERLOCK_INTR',data_moved:false,replication_started:false,ai_corpus_exposed:false,relationship_mutation_authorized:false,authority_effect:'NONE_REQUEST_ONLY',activation_effect:false};
const setReq={schema:'stegverse.site.my-kv.kv-set-status-request/v1',access:'READ_ONLY',authority_effect:'NONE',kv_set_id:'personal'};
const profile=JSON.parse(read('data/kv/google-drive-existing-peer-adoption-profile.json'));
const cloudReq={schema:'stegverse.site.cloud-kv-peer-adoption-request/v1',operation:'ADOPT_EXISTING_CLOUD_KV_PEER',purpose:'test',request_id:'SITE-CLOUD-KV-0123456789abcdef0123456789abcdef',resident_instance_id:'kvi_0d5d4cfd531db51bbcf7fdfc0311f5dc',resident_instance_number:1,kv_set_id:'personal',requested_instance_number:2,requested_logical_name:'KV #2',storage_medium:'google-drive',initial_relationship_tier:'NOT_CONNECTED',governance_state:'PENDING_INTERLOCK_INTR',credential_destination:'SKAP_VAULT',credential_material_present:false,provider_operation_authorized:false,instance_materialized:false,relationship_mutation_authorized:false,data_moved:false,replication_started:false,ai_corpus_exposed:false,authority_effect:'NONE_REQUEST_ONLY',activation_effect:false,existing_cloud_identity:{instance_id:profile.existing_instance_id,current_instance_number:1,requested_instance_number:2,installation_or_adoption_receipt_sha256:profile.existing_receipt_sha256,set_projection_sha256:profile.existing_projection_sha256},storage_locator_hint:null,ordinal_reassignment_requested:true,private_content_rewrite_authorized:false,existing_identity_rewrite_authorized:false,provenance_preservation_required:true};
function seedSetProjection(world){const b64=Buffer.from(JSON.stringify(setProjection())).toString('base64');world.idb.openInto({},'stegverse-device-local-intr-v1',1);world.idb.dbs.get('stegverse-device-local-intr-v1').stores.set('kv_files',{keyPath:'key',rows:new Map([['_System/my-kv-set-projection.json',{key:'_System/my-kv-set-projection.json',content_base64:b64}]])});}
function persistSetResult(msg,idb){
  const entry=msg.trigger.node_outbox_entry,req=entry.materialization_request,q=req.kv_request;
  const response={schema:'stegverse.device-kv.query-response/v1',state:'QUERY_COMPLETE',materialization_id:req.materialization_id,request_hash:req.request_hash,node_id:entry.node_id,query_request_id:q.request_id,record_class:q.record_class,credential_material_present:false,provider_operation_authorized:false,request_grants_authority:false,response_grants_authority:false,authority_effect:'NONE',projection:setProjection()};
  idb.openInto({},'stegverse-my-kv-n-device-kv-v1',1);const db=idb.dbs.get('stegverse-my-kv-n-device-kv-v1');if(!db.stores.has('results'))db.stores.set('results',{keyPath:'materialization_id',rows:new Map()});
  db.stores.get('results').rows.set(req.materialization_id,{materialization_id:req.materialization_id,request_hash:req.request_hash,node_id:entry.node_id,response,response_receipt_hash:shaUri(response)});
}
const manager=require('../assets/my-kv-instance-manager.js');

const SUITES={
  async instance(){
    // (b) receiver registered but never materializes the request: one lookup, six-field refusal, no wait.
    let w=makeWorld(),api=load(w,'instance');
    assertDisposition(await rejectOf(api.requestProviderOperation(providerReq)),'instance',w);
    check(w.seen.posts===1,'instance: the outbox trigger is posted to the receiver without a reply listener');
    // (b) no service worker at all: the request is still durably queued and the refusal is actionable.
    w=makeWorld({noServiceWorker:true});api=load(w,'instance');
    assertDisposition(await rejectOf(api.requestProviderOperation(providerReq)),'instance',w);
    // (b) the real receiver denies the request (pre-existing: it treats credential_material_present as a sensitive key)
    // and persists nothing: the single lookup finds no result and the refusal is actionable.
    w=makeWorld({receiver:BRIDGES.instance.receiver});api=load(w,'instance');
    assertDisposition(await rejectOf(api.requestProviderOperation(providerReq)),'instance',w);
    // (c) materialized by the real resident receiver before the single lookup: success.
    w=makeWorld({receiver:BRIDGES.instance.receiver});api=load(w,'instance');
    const r=await api.requestRelationshipTransition(relationshipReq);
    check(r&&r.governance_state==='PENDING_INTERLOCK_INTR'&&r.data_moved===false&&r.replication_started===false&&r.ai_corpus_exposed===false&&w.seen.lookups===1&&w.seen.timers===0,'instance: materialized relationship result delivered on one lookup: '+JSON.stringify(r));
    // The real my-kv-n receiver denies every valid set projection (pre-existing: credential_material_included is treated
    // as a sensitive key), so a stand-in persists the result row in exactly the receiver's putResult row format.
    w=makeWorld({persist:persistSetResult});api=load(w,'instance');
    const p=await api.getKVSetProjection(setReq);
    check(p&&p.schema==='stegverse.kv.my-kv-set-projection/v1'&&p.instance_count===1&&w.seen.lookups===1&&w.seen.timers===0,'instance: materialized set projection delivered on one lookup');
    check(api.authority_effect==='NONE'&&api.bridge_kind==='DEVICE_KV_MY_KV_N_RESIDENT_TRANSPORT','instance: public API unchanged');
  },
  async admission(){
    const raw=new Uint8Array(Buffer.from(JSON.stringify(setProjection(),null,2)+'\n'));
    let w=makeWorld(),api=load(w,'admission');
    assertDisposition(await rejectOf(api.admitBytes(raw,setProjection(),manager)),'admission',w);
    check(w.seen.posts===1,'admission: the outbox trigger is posted to the receiver without a reply listener');
    // A different projection already at the destination is not this admission.
    w=makeWorld();seedSetProjection(w);api=load(w,'admission');
    assertDisposition(await rejectOf(api.admitBytes(raw,setProjection(),manager)),'admission',w);
    // (c) the real resident admission receiver writes the row before the single lookup: exact readback succeeds.
    w=makeWorld({receiver:BRIDGES.admission.receiver});api=load(w,'admission');
    const resp=await api.admitBytes(raw,setProjection(),manager);
    check(resp&&resp.state==='PROJECTION_ADMITTED'&&resp.exact_readback_verified===true&&resp.canonical_path==='_System/my-kv-set-projection.json'&&resp.size_bytes===raw.length&&resp.projection_sha256==='sha256:'+nodeCrypto.createHash('sha256').update(Buffer.from(raw)).digest('hex'),'admission: exact readback of the admitted bytes: '+JSON.stringify(resp));
    check(resp.authority_effect==='NONE'&&resp.activation_effect===false&&w.seen.lookups===1&&w.seen.timers===0,'admission: one lookup, no timer, no authority');
    check(api.authority_effect==='NONE'&&api.bridge_kind==='DEVICE_KV_MY_KV_SET_PROJECTION_ADMISSION','admission: public API unchanged');
  },
  async cloud(){
    let w=makeWorld(),api=load(w,'cloud');
    assertDisposition(await rejectOf(api.submit(cloudReq)),'cloud',w);
    check(w.seen.posts===1,'cloud: the outbox trigger is posted to the receiver without a reply listener');
    w=makeWorld({legacyOutbox:true});api=load(w,'cloud');
    assertDisposition(await rejectOf(api.submit(cloudReq)),'cloud',w);
    for(const legacyOutbox of [false,true]){
      w=makeWorld({receiver:BRIDGES.cloud.receiver,legacyOutbox});api=load(w,'cloud');
      const r=await api.submit(cloudReq);
      check(r&&r.request_id===cloudReq.request_id&&r.governance_state==='PENDING_INTERLOCK_INTR'&&r.instance_materialized===false&&r.resident_transport_origin===(legacyOutbox?'STEGOS_NODE_EVENT_EPHEMERAL':'STEGOS_NODE_OUTBOX')&&w.seen.lookups===1&&w.seen.timers===0,'cloud: materialized adoption result delivered on one lookup (legacy='+legacyOutbox+'): '+JSON.stringify(r));
    }
    check(api.authority_effect==='NONE'&&api.record_class==='MY_KV_CLOUD_PEER_ADOPTION_REQUEST','cloud: public API unchanged');
  }
};

// A bridge promise that never settles is waiting on a receiver (the fake setTimeout never fires): fail, never exit 0.
let current=null,done=false;
process.on('exit',()=>{if(!done){console.error('FAIL '+current+': a bridge promise never settled; it waits on receiver activation or a receiver reply');process.exitCode=1;}});
(async()=>{
  for(const key of Object.keys(BRIDGES)){
    current=key;
    try{
      // (a) static: no timer-based wait, no activation wait, no reply listener remains in the bridge.
      const code=read(BRIDGES[key].file).replace(/\/\/.*$/gm,'').replace(/\/\*[\s\S]*?\*\//g,'');
      check(!/setTimeout|setInterval|waitForActive|statechange|\.onmessage\b|\bdelay\(|\bpoll\(/.test(code),key+': no timer, activation wait, reply listener, delay or poll in '+BRIDGES[key].file);
      const m=code.match(/function resultNotMaterialized\(lookup,detail\)\{[^\n]*\}/);
      check(m,key+': defines the actionable refusal');
      await SUITES[key]();
      console.log('PASS '+key+' bridge does not wait on a receiver');
    }catch(e){failures.push(e.message);console.error('FAIL '+key+': '+e.message);}
  }
  done=true;
  if(failures.length){console.error('mykv-bridges-no-receiver-wait: '+failures.length+' bridge(s) failed');process.exit(1);}
  console.log('mykv-bridges-no-receiver-wait: '+n+' checks passed');
})();
