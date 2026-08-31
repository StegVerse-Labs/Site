const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');

if (!globalThis.crypto) globalThis.crypto = crypto.webcrypto;
if (!globalThis.TextEncoder) globalThis.TextEncoder = require('node:util').TextEncoder;

const root = path.resolve(__dirname, '..');
const artifactPath = path.join(root, 'assets/generated/site-browser-intr-connectors.js');
const manifest = JSON.parse(fs.readFileSync(path.join(root, 'assets/generated/site-browser-intr-connectors.manifest.json'), 'utf8'));
require(artifactPath);
const intr = globalThis.StegVerseGeneratedInTr;

function digest(raw) {
  return `sha256:${crypto.createHash('sha256').update(raw).digest('hex')}`;
}

test('generated connector is exact, offline, profile-bound source', async () => {
  const raw = fs.readFileSync(artifactPath);
  assert.equal(digest(raw), manifest.artifact_sha256);
  assert.deepEqual(Object.keys(intr.PROFILES).sort(), [...manifest.profiles].sort());
  assert.equal(intr.PROVENANCE.registry_sha256, manifest.registry_sha256);
  assert.equal(intr.PROVENANCE.credential_authority, 'TV/TVC');
  for (const key of ['pypi_dependency', 'cdn_dependency', 'github_runtime_dependency', 'third_party_package_authority']) {
    assert.equal(intr.PROVENANCE[key], false, key);
  }
  for (const [profileId, profile] of Object.entries(intr.PROFILES)) {
    assert.equal(digest(Buffer.from(intr.canonical(profile))), manifest.profile_sha256[profileId]);
  }
});

test('all four Site lane purposes are canonical profile adjustments', async () => {
  const cases = [
    ['evaluator-read-review', 'READ_REVIEW'],
    ['hil-submission', 'SUBMIT'],
    ['sv002-public-observe', 'READ_OBSERVATION'],
    ['device-kv', 'REQUEST'],
  ];
  for (const [profileId, operation] of cases) {
    const payload = new TextEncoder().encode(intr.canonical({ profileId, operation }));
    const intent = await intr.buildIntent(profileId, payload, operation, `SITE-${profileId}`);
    assert.equal(intent.protocol, 'InTr');
    assert.equal(intent.interlock_required, true);
    assert.equal(intent.authority.credential_authority, 'TV/TVC');
    assert.equal(intent.authority.authority_transfer, false);
    assert.equal(intent.transport_semantics.always_on_receiver_required, false);
    assert.equal(intent.transport_semantics.blind_consequence_retry_allowed, false);
  }
});

test('generated materialization owns carrier attachment and request hashing', async () => {
  const intent = await intr.buildIntent(
    'hil-submission',
    new TextEncoder().encode('{}'),
    'SUBMIT',
    'SITE-MAT-CARRIER'
  );
  const carrierBody = {
    schema: 'stegverse.intr.hb-derived-carrier-binding/v1',
    carrier_profile: 'stegverse.intr.hb-derived-carrier-profile/v1',
    fundamental_mode: 'HB',
    packet_id: intent.packet_id,
    payload_hash: intent.payload_hash,
    heartbeat_reference: { heartbeat_epoch: 32 },
    channel: { channel_id: 'HB:H1:P0' },
    carrier_grants_admission_authority: false,
    carrier_grants_execution_authority: false,
    carrier_grants_credential_authority: false,
    carrier_grants_routing_authority: false,
    carrier_grants_transition_authority: false,
    carrier_grants_receiving_authority: false,
    credential_authority: 'TV/TVC',
    authority_effect: 'NONE_CARRIER_ONLY'
  };
  const carrier = { ...carrierBody, binding_sha256: await intr.sha256Value(carrierBody) };
  const request = await intr.buildMaterializationRequest('hil-submission', intent, 'opaque://hil/test', carrier);
  assert.deepEqual(request.carrier_binding, carrier);
  const body = { ...request };
  delete body.request_hash;
  assert.equal(request.request_hash, await intr.sha256Value(body));
});

test('DEVICE_KV materialization admits only portable_payload before request hashing', async () => {
  const payload = { schema: 'stegverse.kv.portable-direct-source-inline-payload/v1', files: [] };
  const intent = await intr.buildIntent(
    'device-kv',
    new TextEncoder().encode(intr.canonical(payload)),
    'REQUEST',
    'SITE-DEVICE-KV-EXT'
  );
  const carrierBody = {
    schema: 'stegverse.intr.hb-derived-carrier-binding/v1',
    carrier_profile: 'stegverse.intr.hb-derived-carrier-profile/v1',
    packet_id: intent.packet_id,
    payload_hash: intent.payload_hash,
    carrier_grants_admission_authority: false,
    carrier_grants_execution_authority: false,
    carrier_grants_credential_authority: false,
    carrier_grants_routing_authority: false,
    carrier_grants_transition_authority: false,
    carrier_grants_receiving_authority: false,
    credential_authority: 'TV/TVC',
    authority_effect: 'NONE_CARRIER_ONLY'
  };
  const carrier = { ...carrierBody, binding_sha256: await intr.sha256Value(carrierBody) };
  const request = await intr.buildMaterializationRequest(
    'device-kv',
    intent,
    'inline://materialization_request.portable_payload',
    carrier,
    { portable_payload: payload }
  );
  assert.deepEqual(request.portable_payload, payload);
  const body = { ...request }; delete body.request_hash;
  assert.equal(request.request_hash, await intr.sha256Value(body));
  await assert.rejects(
    intr.buildMaterializationRequest(
      'device-kv', intent, 'inline://bad', carrier, { arbitrary_field: true }
    ),
    /materialization_extension_field_not_allowed/
  );
});

test('HIL and SV002 unavailable receivers use canonical non-authorizing materialization', async () => {
  for (const profileId of ['hil-submission', 'sv002-public-observe']) {
    const profile = intr.PROFILES[profileId];
    const operation = profile.operations[0];
    const intent = await intr.buildIntent(profileId, new TextEncoder().encode('{}'), operation, `SITE-MAT-${profileId}`);
    const request = await intr.buildMaterializationRequest(profileId, intent, `opaque://${profileId}/packet`);
    assert.equal(request.downstream_owner_ref, profile.downstream_owner_ref);
    assert.equal(request.claim_or_fence_minted, false);
    assert.equal(request.github_token_runtime_authority, 'NONE');
    assert.equal(request.request_grants_execution_authority, false);
    assert.equal(request.authority_effect, 'NONE_REQUEST_ONLY');
  }
});

test('lane sources consume generated builders instead of private transport constructors', () => {
  const hil = fs.readFileSync(path.join(root, 'assets/hil-direct-upload-v1.js'), 'utf8');
  const sv002 = fs.readFileSync(path.join(root, 'assets/sv002-observe.js'), 'utf8');
  const evaluator = fs.readFileSync(path.join(root, 'assets/evaluator-intr-connector.js'), 'utf8');
  const kv = fs.readFileSync(path.join(root, 'assets/kv-ui/intr-kv-client.js'), 'utf8');
  const portable = fs.readFileSync(path.join(root, 'assets/my-kv-portable-direct-source-bridge.js'), 'utf8');
  assert.match(hil, /buildIntent\(\s*'hil-submission'/);
  assert.match(hil, /buildMaterializationRequest\('hil-submission', intent, payloadRef, binding\)/);
  assert.doesNotMatch(hil, /delete body\.request_hash/);
  assert.match(sv002, /buildIntent\(\s*"sv002-public-observe"/);
  assert.match(sv002, /buildMaterializationRequest\(\s*"sv002-public-observe"/);
  assert.match(sv002, /binding\s*\)/);
  assert.doesNotMatch(sv002, /delete body\.request_hash/);
  assert.match(evaluator, /buildCanonicalIntent/);
  assert.match(kv, /'device-kv'/);
  assert.match(portable, /buildIntent\("device-kv"/);
  assert.match(portable, /buildMaterializationRequest\([\s\S]*"device-kv"/);
  assert.match(portable, /\{portable_payload:inlinePayload\}/);
  assert.doesNotMatch(portable, /var intent=\{/);
  assert.doesNotMatch(portable, /var body=\{/);
  assert.doesNotMatch(portable, /var matBasis=/);
  assert.doesNotMatch(portable, /var materializationId=/);
  assert.doesNotMatch(hil, /source_boundary:\s*'DEVICE_SYSTEM'/);
  assert.doesNotMatch(sv002, /source_boundary:/);
});
