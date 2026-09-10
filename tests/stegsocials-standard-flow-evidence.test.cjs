const assert = require('assert');
const api = require('../assets/stegsocials-standard-flow-evidence.js');

const hash='sha256:'+'a'.repeat(64);
const preparation={
  schema:'stegverse.stegsocials.post-preparation/v1',
  task_id:'SS-EVIDENCE-COMPARISON-001',
  bundle_id:'ssprep_site_test',
  kv_context:{draft_path:'02_Research/StegSocials/Drafts/LinkedIn/ssprep_site_test.json',erl_refs:[{ref:'02_Research/ERL/article.md',authority:'ERL',sha256:null}]},
  publication_plan:'MANUAL',
  execution:{provider_call_performed:false,credential_material_present:false,publication_authority_effect:'NONE_PREPARATION_ONLY'}
};
const admission={
  schema:'stegverse.site.stegsocials-kv-draft-admission-result/v1',
  state:'KV_DRAFT_ADMITTED_HASH_READBACK',
  bundle_id:preparation.bundle_id,
  canonical_path:preparation.kv_context.draft_path,
  sha256:hash,
  size_bytes:512,
  materialization_id:'mat-1',
  request_hash:'sha256:'+'b'.repeat(64),
  canonical_kv_admission_observed:true,
  admitted_hash_readback_verified:true,
  provider_call_performed:false,
  credential_material_present:false,
  provider_operation_authorized:false
};
const readback={
  schema:'stegverse.site.stegsocials-kv-exact-content-readback/v1',
  state:'EXACT_CONTENT_BYTES_READBACK_VERIFIED',
  canonical_path:admission.canonical_path,
  sha256:hash,
  size_bytes:512,
  exact_content_bytes_readback_verified:true,
  device_local_kv_store_observed:true,
  cloud_provider_readback_observed:false,
  provider_call_performed:false,
  credential_material_present:false,
  provider_operation_authorized:false
};
const client_observation={user_agent:'SyntheticBrowser/1.0',platform:'test',language:'en',physical_device_identity_claimed:false};
function input(){return {preparation,admission,readback,client_observation,observed_at:'2026-09-10T23:45:00.000Z'};}

const evidence=api.materialize(input());
assert.equal(evidence.schema,'stegverse.site.stegsocials-standard-flow-evidence/v1');
assert.equal(evidence.state,'STANDARD_FLOW_EVIDENCE_READY');
assert.equal(evidence.task_id,'SS-EVIDENCE-COMPARISON-001');
assert.equal(evidence.bundle_id,preparation.bundle_id);
assert.equal(evidence.kv_evidence.canonical_path,admission.canonical_path);
assert.equal(evidence.kv_evidence.sha256,hash);
assert.equal(evidence.kv_evidence.size_bytes,512);
assert.equal(evidence.kv_evidence.exact_content_bytes_readback_verified,true);
assert.equal(evidence.kv_evidence.device_local_kv_store_observed,true);
assert.equal(evidence.kv_evidence.cloud_provider_readback_observed,false);
assert.equal(evidence.provider_call_performed,false);
assert.equal(evidence.credential_material_present,false);
assert.equal(evidence.provider_operation_authorized,false);
assert.equal(evidence.physical_device_identity_claimed,false);
assert.equal(api.filename(evidence),'stegsocials-standard-flow-evidence-ssprep_site_test.json');

const cases=[
  [{admission:{...admission,bundle_id:'wrong'}},/admission bundle mismatch/],
  [{admission:{...admission,canonical_path:'02_Research/StegSocials/Drafts/X/other.json'}},/admission path mismatch/],
  [{readback:{...readback,sha256:'sha256:'+'c'.repeat(64)}},/readback SHA-256 mismatch/],
  [{readback:{...readback,size_bytes:513}},/readback size mismatch/],
  [{readback:{...readback,exact_content_bytes_readback_verified:false}},/readback incomplete/],
  [{readback:{...readback,cloud_provider_readback_observed:true}},/may not be inferred/],
  [{admission:{...admission,provider_operation_authorized:true}},/provider-operation boundary invalid/],
  [{client_observation:{...client_observation,physical_device_identity_claimed:true}},/physical device identity may not be claimed/]
];
for(const [patch,pattern] of cases){
  assert.throws(()=>api.materialize({...input(),...patch}),pattern);
}
console.log(JSON.stringify({status:'PASS',standard_flow_evidence_ready:true,portable_json:true,physical_device_identity_claimed:false,provider_call_performed:false}));
