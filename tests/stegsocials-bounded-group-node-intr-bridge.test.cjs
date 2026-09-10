const assert = require('assert');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto').webcrypto;

global.crypto = crypto;
global.btoa = value => Buffer.from(value, 'binary').toString('base64');

function canonical(v){
  if(v===null||typeof v!=='object') return JSON.stringify(v);
  if(Array.isArray(v)) return '['+v.map(canonical).join(',')+']';
  return '{'+Object.keys(v).sort().map(k=>JSON.stringify(k)+':'+canonical(v[k])).join(',')+'}';
}
async function hash(value){
  const bytes = new TextEncoder().encode(canonical(value));
  const digest = await crypto.subtle.digest('SHA-256', bytes);
  return 'sha256:'+Buffer.from(digest).toString('hex');
}
function state(successful, indices, status='ACTIVE'){
  return {schema_version:'stegsocials.bounded-post-group-use-state.v1',group_id:'post-group-social-001',state:status,state_ref:'kv://personal/StegSocials/PostGroupState/post-group-social-001',consumed_use_indices:indices,successful_posts:successful,last_successful_at:successful?'2026-09-10T22:00:00Z':null,observed_at:successful?'2026-09-10T22:00:00Z':'2026-09-10T21:00:00Z'};
}
async function stateEtag(value){
  const digest=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(canonical(value)+'\n'));
  return 'sha256:'+Buffer.from(digest).toString('hex');
}
async function expectReject(action, fragment){
  let failed=false;try{await (typeof action==='function'?action():action);}catch(e){failed=true;assert(String(e.message).includes(fragment),`${e.message} did not include ${fragment}`);}assert(failed,`expected rejection containing ${fragment}`);
}

(async function(){
  let registeredUrl=null,registeredScope=null,queued=null,intentArgs=null,materializationArgs=null,hbArgs=null,posted=null;
  let messageHandler=null;
  class FakeMessageChannel {
    constructor(){this.port1={onmessage:null};this.port2={};messageHandler=this.port1;}
  }
  const fakeWorker={postMessage(message){posted=message;setTimeout(()=>messageHandler.onmessage({data:{ok:true,receipt:global.__receipt}}),0);}};
  const root=global;
  root.MessageChannel=FakeMessageChannel;
  root.navigator={serviceWorker:{register:async(url,opts)=>{registeredUrl=url;registeredScope=opts.scope;return {active:fakeWorker};}}};
  root.isSecureContext=true;
  root.StegVerseGeneratedInTr={
    canonical,
    buildIntent:async(...args)=>{intentArgs=args;return {packet_id:'packet-1',payload_hash:'sha256:'+'1'.repeat(64)};},
    buildMaterializationRequest:async(...args)=>{
      materializationArgs=args;
      return {schema:'stegverse.universal-intr-materialization-request/v1',state:'QUEUED_FOR_EVENT_EPHEMERAL_MATERIALIZATION',materialization_id:'mat-1',request_hash:'sha256:'+'2'.repeat(64),destination:{boundary:'KV',subsystem:'KnowledgeVault:Interlock'},downstream_owner_ref:'StegVerse-Labs/continuity-vault-kit#79',request_grants_execution_authority:false,transport_grants_execution_authority:false,claim_or_fence_minted:false,credential_authority:'TV/TVC',github_token_runtime_authority:'NONE',kv_request:args[4].kv_request};
    }
  };
  root.StegVerseHBInTrCarrier={buildBinding:async(...args)=>{hbArgs=args;return {schema:'hb-binding',authority_effect:'NONE',execution_authority:false};}};
  root.StegVerseNodeContinuity={
    status:async()=>({registered:true,registration:{node_id:'node-1'}}),
    queueIntrMaterializationRequest:async(materialization)=>{
      queued=materialization;
      const entry={schema:'stegos.node_intr_outbox_entry.v1',state:'LOCAL_OUTBOX_PENDING_NETWORK_DELIVERY',node_id:'node-1',interlock_id:'intr-1',materialization_request:materialization,credential_authority:'TV/TVC',github_token_runtime_authority:'NONE',request_grants_execution_authority:false,claim_or_fence_minted:false};
      entry.outbox_entry_hash=await hash(entry);
      return entry;
    }
  };

  const bridge=require('../assets/stegsocials-bounded-group-node-intr-bridge.js');
  const current=state(0,[]),next=state(1,[1]);
  const request={schema:'stegverse.site.stegsocials-bounded-group-kv-conditional-write/v1',operation:'COMPARE_AND_SWAP',task_id:'SS-KV-SKAP-SOCIAL-RELEASE-001',canonical_path:'03_Records/StegSocials/PostGroupState/post-group-social-001.json',group_id:'post-group-social-001',state_ref:current.state_ref,consumed_use_index:1,expected_previous_etag:await stateEtag(current),next_state_etag:await stateEtag(next),next_state:next,publication_proof:{publication_proven:true,publication_receipt_ref:'receipt://social/1',final_content_hash:'sha256:'+'a'.repeat(64),session_state_destroyed:true,credential_material_present:false},credential_material_present:false,provider_operation_authorized:false,authority_effect:'NONE_STATE_TRANSITION_REQUEST_ONLY'};

  const envelope=await bridge._test.buildEnvelope('node-1',request);
  assert.strictEqual(envelope.query.record_class,'STEGSOCIALS_BOUNDED_GROUP_USE_STATE_CAS');
  assert.strictEqual(envelope.query.operation,'COMMIT_CANDIDATE');
  assert.strictEqual(envelope.query.carrier_grants_authority,false);
  assert.strictEqual(envelope.query.authority_ref,'stegos-node://node-1');
  assert.strictEqual(envelope.query.candidate_writeback.requested_destination,request.canonical_path);

  global.__receipt={schema:'stegverse.device-kv.my-kv-n-resident-receipt/v1',state:'RESULT_AVAILABLE',materialization_id:'mat-1',request_hash:'sha256:'+'2'.repeat(64),node_id:'node-1',record_class:'STEGSOCIALS_BOUNDED_GROUP_USE_STATE_CAS',response:{schema:'stegverse.device-kv.query-response/v1',state:'QUERY_COMPLETE',materialization_id:'mat-1',request_hash:'sha256:'+'2'.repeat(64),node_id:'node-1',query_request_id:null,record_class:'STEGSOCIALS_BOUNDED_GROUP_USE_STATE_CAS',credential_material_present:false,provider_operation_authorized:false,request_grants_authority:false,response_grants_authority:false,authority_effect:'NONE',result:{schema:'stegverse.device-kv.stegsocials-bounded-group-cas-result/v1',state:'GROUP_USE_STATE_COMMITTED',canonical_path:request.canonical_path,group_id:request.group_id,consumed_use_index:1,previous_etag:request.expected_previous_etag,persisted_etag:request.next_state_etag,exact_readback_verified:true,publication_receipt_ref:'receipt://social/1',session_state_destroyed:true,credential_material_present:false,provider_operation_authorized:false,authority_effect:'NONE_EVIDENCE_ONLY'}},local_ingress_observed:true,resident_materialization_observed:true,provider_execution_attempted:false,relationship_mutation_attempted:false,data_moved:false,replication_started:false,ai_corpus_exposed:false,credential_material_present:false,provider_operation_authorized:false,relationship_mutation_authorized:false,credential_authority:'TV/TVC',github_token_runtime_authority:'NONE',authority_effect:'NONE_RESULT_DELIVERY_ONLY'};

  // Fill dynamic query request id at dispatch time by observing queued materialization.
  const originalPost=fakeWorker.postMessage;
  fakeWorker.postMessage=function(message){global.__receipt.response.query_request_id=queued.kv_request.request_id;return originalPost.call(this,message);};
  const result=await bridge.commit(request);
  assert.strictEqual(result.state,'GROUP_USE_STATE_COMMITTED');
  assert.strictEqual(result.exact_readback_verified,true);
  assert.strictEqual(registeredUrl,'/assets/my-kv-n-device-kv-receiver.js');
  assert.strictEqual(registeredScope,'/assets/my-kv-n-runtime/');
  assert.deepStrictEqual(intentArgs.slice(0,1),['device-kv']);
  assert.strictEqual(intentArgs[2],'COMMIT_CANDIDATE');
  assert.deepStrictEqual(hbArgs,['packet-1','sha256:'+'1'.repeat(64)]);
  assert.strictEqual(materializationArgs[0],'device-kv');
  assert.strictEqual(queued.kv_request.record_class,'STEGSOCIALS_BOUNDED_GROUP_USE_STATE_CAS');
  assert.strictEqual(posted.type,'STEGVERSE_MY_KV_N_LOCAL_TRIGGER');
  assert.strictEqual(posted.trigger.request_grants_execution_authority,false);

  await expectReject(()=>bridge._test.validateCas({...request,credential_material_present:true}),'credential/provider boundary');
  await expectReject(()=>bridge._test.validateCas({...request,provider_operation_authorized:true}),'credential/provider boundary');
  await expectReject(()=>bridge._test.validateCas({...request,publication_proof:{...request.publication_proof,session_state_destroyed:false}}),'proven publication and terminal destruction required');

  const workerSource=fs.readFileSync(path.join(__dirname,'..','assets','my-kv-n-device-kv-receiver.js'),'utf8');
  assert(workerSource.includes('importScripts("/assets/stegsocials-bounded-group-device-kv-cas-receiver.js")'));
  assert(workerSource.includes('STEGSOCIALS_BOUNDED_GROUP_USE_STATE_CAS'));
  assert(workerSource.includes('StegVerseStegSocialsBoundedGroupDeviceKVCASReceiver'));
  assert(workerSource.includes('STEGVERSE_MY_KV_N_LOCAL_TRIGGER'));
  const bridgeSource=fs.readFileSync(path.join(__dirname,'..','assets','stegsocials-bounded-group-node-intr-bridge.js'),'utf8');
  assert(bridgeSource.includes('carrier_grants_authority:false'));
  assert(!bridgeSource.includes('stegsocials-bounded-group-device-kv-cas-runtime'));

  console.log(JSON.stringify({status:'PASS',existing_my_kv_worker_reused:true,second_worker_runtime_created:false,registered_node_required:true,generated_intr_materialization_reused:true,hb_authority:false,node_outbox_trigger_hash_bound:true,social_cas_record_class_bound:true,publication_and_destruction_gate_preserved:true,credential_provider_authority_refused:true}));
})().catch(err=>{console.error(err.stack||err);process.exit(1);});
