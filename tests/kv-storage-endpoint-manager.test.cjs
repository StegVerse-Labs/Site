const assert=require('node:assert/strict');
const api=require('../assets/kv-storage-endpoint-manager.js');
const t=api._test;
const resident={installed:true,exact_readback_verified:true,instance:{instance_id:'kvi_11111111111111111111111111111111',instance_number:1,kv_set_id:'personal',storage:{medium:'device-local-browser-indexeddb'}}};

const device=t.buildCreate(resident,{storage_medium:'device-local',requested_instance_number:2,storage_locator_hint:'KnowledgeVault-2'});
assert.equal(device.schema,'stegverse.site.kv-storage-endpoint-create-request/v2');
assert.equal(device.operation,'CREATE_KV_STORAGE_ENDPOINT');
assert.equal(device.storage_endpoint.storage_class,'DEVICE');
assert.equal(device.storage_endpoint.credential_requirement,'NONE');
assert.equal(device.credential_destination,null);
assert.equal(device.initial_relationship_tier,'NOT_CONNECTED');
assert.equal(device.governance_state,'PENDING_INTERLOCK_INTR');
api.validate(device);

const nas=t.buildCreate(resident,{storage_medium:'nas',requested_instance_number:3,storage_locator_hint:'smb://nas/StegVerse/KnowledgeVault-3'});
assert.equal(nas.storage_endpoint.storage_class,'NETWORK');
assert.equal(nas.storage_endpoint.session_requirement,'ADAPTER_DEFINED');
assert.equal(nas.credential_destination,'SKAP_VAULT');
api.validate(nas);

const adopted=t.buildAdopt(resident,{storage_medium:'google-drive',requested_instance_number:2,current_instance_number:1,existing_instance_id:'kvi_a31335d2cc3745fa987b635432cfed2c',existing_receipt_sha256:'sha256:64a3af27be0bd6ae36b05b35e52894581413fff048cea237d370d0ec6248b552',existing_projection_sha256:'sha256:187ab43f0bb09d88da154af26d57e1bfe7199fd90affd2dd81af5532f0e34cf4'});
assert.equal(adopted.schema,'stegverse.site.kv-storage-endpoint-adoption-request/v2');
assert.equal(adopted.existing_kv_identity.instance_id,'kvi_a31335d2cc3745fa987b635432cfed2c');
assert.equal(adopted.private_content_rewrite_authorized,false);
assert.equal(adopted.existing_identity_rewrite_authorized,false);
api.validate(adopted);

const legacy={schema:'stegverse.site.cloud-kv-peer-adoption-request/v1',storage_medium:'google-drive',request_id:'SITE-CLOUD-KV-4347408852127319cbda574f02e03edb'};
const normalized=api.normalizeLegacyV1(legacy);
assert.equal(normalized.request_id,legacy.request_id);
assert.equal(normalized.compatibility_source_schema,legacy.schema);
assert.equal(normalized.normalized_storage_endpoint.adapter_id,'google-drive');
assert.equal(normalized.compatibility_effect,'NONE_VIEW_ONLY');

assert.throws(()=>t.buildCreate(resident,{storage_medium:'ftp',requested_instance_number:2}),/unsupported storage endpoint/);
assert.throws(()=>t.buildCreate(resident,{storage_medium:'google-drive',requested_instance_number:1}),/ordinal must be >= 2/);
assert.throws(()=>t.buildCreate(resident,{storage_medium:'nas',requested_instance_number:2,storage_locator_hint:'password=bad'}),/forbidden credential-like material/);
assert.deepEqual(api.supported_storage_media,['device-local','icloud-drive','google-drive','onedrive','dropbox','nas','removable-storage']);
console.log('KV_STORAGE_ENDPOINT_MANAGER=PASS');
console.log('LEGACY_CLOUD_V1_NORMALIZATION=PASS');
console.log('GOOGLE_DRIVE_KV2_REQUEST_LINEAGE_PRESERVED=TRUE');
console.log('KV_IDENTITY_RELATIONSHIP_GOVERNANCE_UNCHANGED=TRUE');