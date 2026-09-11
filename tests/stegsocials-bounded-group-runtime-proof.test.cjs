const assert=require('assert');
const fs=require('fs');
const vm=require('vm');
const crypto=require('crypto').webcrypto;

function load(path,root){
  const code=fs.readFileSync(path,'utf8');
  const sandbox={globalThis:root,module:{exports:{}},exports:{},TextEncoder,TextDecoder,Uint8Array,ArrayBuffer,Buffer,setTimeout,clearTimeout,console};
  vm.runInNewContext(code,sandbox,{filename:path});
  return sandbox.module.exports;
}

(async()=>{
  const root={crypto};
  const api=load('assets/stegsocials-bounded-group-runtime-proof.js',root);
  assert.equal(api.proof_schema,'stegverse.site.stegsocials-bounded-group-runtime-observation/v1');
  assert.equal(api.goal_task_id,'SS-KV-SKAP-SOCIAL-RELEASE-001');
  assert.equal(api.cosv_id,'60000000102000');
  assert.equal(api.external_intr_admission_inferred,false);

  const request={
    schema:'stegverse.site.stegsocials-bounded-group-kv-conditional-write/v1',
    operation:'COMPARE_AND_SWAP',
    canonical_path:'03_Records/StegSocials/PostGroupState/group-1.json',
    group_id:'group-1',consumed_use_index:1,
    expected_previous_etag:'sha256:'+'1'.repeat(64),
    next_state_etag:'sha256:'+'2'.repeat(64),
    publication_proof:{publication_proven:true,session_state_destroyed:true,publication_receipt_ref:'receipt://post-1'},
    credential_material_present:false,provider_operation_authorized:false
  };
  assert.equal(api._test.validateRequest(request).group_id,'group-1');

  const observation={
    schema:'stegverse.site.stegsocials-bounded-group-node-intr-observation/v1',
    state:'LOCAL_NODE_INTR_DEVICE_KV_CAS_OBSERVED',local_node_outbox_observed:true,resident_materialization_observed:true,
    external_intr_admission_observed:false,external_intr_admission_receipt_ref:null,
    carrier_grants_authority:false,hb_binding:{carrier_grants_authority:false},
    credential_material_present:false,provider_operation_authorized:false,
    cas_result:{group_id:'group-1',consumed_use_index:1,previous_etag:request.expected_previous_etag,persisted_etag:request.next_state_etag,exact_readback_verified:true}
  };
  assert.equal(api._test.validateObservation(observation,request).external_intr_admission_observed,false);
  assert.throws(()=>api._test.validateObservation({...observation,external_intr_admission_observed:true},request),/external admission may not be inferred/);

  const bytes=Buffer.from('{"ok":true}\n');
  const hash='sha256:'+require('crypto').createHash('sha256').update(bytes).digest('hex');
  root.atob=(v)=>Buffer.from(v,'base64').toString('binary');
  const row={sha256:hash,content_base64:bytes.toString('base64')};
  const proofApi=load('assets/stegsocials-bounded-group-runtime-proof.js',root);
  const checked=await proofApi._test.verifyRow(row,hash,'post-state');
  assert.equal(checked.exact_content_hash_verified,true);
  await assert.rejects(()=>proofApi._test.verifyRow(row,'sha256:'+'0'.repeat(64),'post-state'),/etag mismatch/);

  const bridgeSrc=fs.readFileSync('assets/stegsocials-bounded-group-node-intr-bridge.js','utf8');
  assert(bridgeSrc.includes('commitObserved'));
  assert(bridgeSrc.includes('external_intr_admission_observed:false'));
  assert(bridgeSrc.includes('NONE_CORRELATION_ONLY'));
  assert(!bridgeSrc.includes('external_intr_admission_observed:true'));

  const page=fs.readFileSync('stegsocials-bounded-group-runtime-proof.html','utf8');
  assert(page.includes('Run exact runtime proof'));
  assert(page.includes('does not create external InTr admission'));
  assert(page.includes('stegsocials-bounded-group-runtime-proof.js'));
  console.log('STEGSOCIALS_BOUNDED_GROUP_RUNTIME_PROOF_PASS');
})().catch(e=>{console.error(e);process.exit(1);});
