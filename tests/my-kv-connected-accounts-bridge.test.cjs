/*
 * StegVerseKVAccountObservationBridge.
 *
 * The page consumed this global and nothing defined it, so every run took the
 * fail-closed branch. These tests pin both halves of that: the bridge must
 * refuse without a registered Node, without the profile, and without an exact
 * TVC SKAP receipt — and must return a result the caller's own bounded-result
 * scan accepts.
 */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const accounts = require('../assets/my-kv-connected-accounts.js');

const ROOT = path.join(__dirname, '..');
function loadGlobalScript(rel) {
  // eslint-disable-next-line no-eval
  (0, eval)(fs.readFileSync(path.join(ROOT, rel), 'utf8'));
}

loadGlobalScript('assets/generated/site-browser-intr-connectors.js');
globalThis.StegVerseMyKVConnectedAccounts = accounts;

const PROFILE = 'kv-skap-account-metadata';
assert.ok(
  globalThis.StegVerseGeneratedInTr.PROFILES[PROFILE],
  'generated connector must carry the kv-skap-account-metadata profile'
);

const profile = globalThis.StegVerseGeneratedInTr.PROFILES[PROFILE];
assert.equal(profile.source.boundary, 'KV');
assert.equal(profile.destination.boundary, 'SKAP_VAULT');
assert.deepEqual(profile.operations, ['SKAP_ACCOUNT_METADATA_ADMIT']);
assert.equal(profile.downstream_owner_ref, 'StegVerse-Labs/TVC');
assert.equal(profile.custody_mode, 'REFERENCE');

/* ---- stub runtime ------------------------------------------------------ */

const NODE_ID = 'stegnode-web-testnode';
const SELECTED = {
  provider_org_ref: 'org:linkedin',
  account_ref: 'account://linkedin/stegverse-page',
  label: 'StegVerse',
  account_class: 'social',
  status: 'ACTIVE'
};

function populationRequest() {
  return {
    schema: 'stegverse.site.my-kv.connected-account-population-request/v1',
    accounts: [SELECTED],
    destination: 'SKAP_NONSECRET_ACCOUNT_METADATA',
    synthetic_input_allowed: false,
    raw_provider_identifiers_present: false,
    credential_material_present: false
  };
}

function hbCarrierStub() {
  const intr = globalThis.StegVerseGeneratedInTr;
  return {
    async buildBinding(packetId, payloadHash) {
      const body = {
        schema: 'stegverse.intr.hb-derived-carrier-binding/v1',
        carrier_profile: 'stegverse.intr.hb-derived-carrier-profile/v1',
        packet_id: packetId,
        payload_hash: payloadHash,
        credential_authority: 'TV/TVC',
        authority_effect: 'NONE_CARRIER_ONLY',
        carrier_grants_admission_authority: false,
        carrier_grants_execution_authority: false,
        carrier_grants_credential_authority: false,
        carrier_grants_routing_authority: false,
        carrier_grants_transition_authority: false,
        carrier_grants_receiving_authority: false
      };
      return Object.assign({}, body, { binding_sha256: await intr.sha256Value(body) });
    }
  };
}

function nodeStub({ registered = true, receipt = 'valid', packetRef = {} } = {}) {
  return {
    async status() {
      return registered
        ? { registered: true, registration: { node_id: NODE_ID, interlock_id: 'steginterlock-test' } }
        : { registered: false };
    },
    async queueIntrMaterializationRequest(m) {
      const packet = m.account_metadata_transfer;
      packetRef.packet = packet;
      packetRef.materialization = m;
      if (receipt === 'absent') return { tvc_receipt_observed: false };
      const base = {
        schema: 'stegverse.skap.account-metadata-admission-receipt/v1',
        materialization_id: m.materialization_id,
        request_hash: m.request_hash,
        payload_sha256: packet.payload_sha256,
        synthetic_material_only: false,
        skap_account_ref: 'skap:account:deadbeefdeadbeefdeadbeef',
        credential_authority: 'TV/TVC',
        github_token_runtime_authority: 'NONE',
        credential_material_present: false,
        authority_effect: 'NONE'
      };
      const variants = {
        valid: base,
        synthetic: Object.assign({}, base, { synthetic_material_only: true }),
        drifted: Object.assign({}, base, { payload_sha256: 'sha256:' + '0'.repeat(64) }),
        unbound: Object.assign({}, base, { materialization_id: 'INTR-MAT-OTHER' }),
        authorizing: Object.assign({}, base, { credential_authority: 'SELF' })
      };
      return { tvc_receipt_observed: true, tvc_receipt: variants[receipt] };
    }
  };
}

function install(stubs) {
  globalThis.StegVerseHBInTrCarrier = stubs.hb === undefined ? hbCarrierStub() : stubs.hb;
  globalThis.StegVerseNodeContinuity = stubs.node === undefined ? nodeStub() : stubs.node;
  globalThis.StegVerseDeviceKVInTrSync = stubs.sync === undefined
    ? { loadTarget() { return null; }, synchronizeMaterialization() { return null; } }
    : stubs.sync;
  delete globalThis.StegVerseKVAccountObservationBridge;
  loadGlobalScript('assets/my-kv-connected-accounts-bridge.js');
  return globalThis.StegVerseKVAccountObservationBridge;
}

async function refuses(promise, pattern, label) {
  await assert.rejects(promise, pattern, label);
}

(async () => {
  /* the bridge exists at all — the original defect */
  let bridge = install({});
  assert.equal(typeof bridge.listObservedAccounts, 'function');
  assert.equal(typeof bridge.populateSelectedAccountMetadata, 'function');
  assert.equal(bridge.credential_authority, 'TV/TVC');
  assert.equal(bridge.authority_effect, 'NONE');

  /* happy path: an exact receipt is admitted */
  const seen = {};
  bridge = install({ node: nodeStub({ packetRef: seen }) });
  const result = await bridge.populateSelectedAccountMetadata(populationRequest());
  assert.equal(result.accepted, true);
  assert.equal(result.admitted.length, 1);
  assert.equal(result.admitted[0].skap_account_ref, 'skap:account:deadbeefdeadbeefdeadbeef');
  assert.equal(result.admitted[0].provider_org_ref, 'org:linkedin');
  assert.equal(result.authority_effect, 'NONE_POPULATION_RESULT_ONLY');

  /* the result must survive the caller's own bounded-result scan */
  accounts.assertBounded(result, 'population_result');

  /* the transfer packet carries the producer's non-secret assertions */
  assert.equal(seen.packet.schema, 'stegverse.kv-skap.account-metadata-transfer/v1');
  assert.equal(seen.packet.contains_secret_material, false);
  assert.equal(seen.packet.raw_provider_account_identifier_present, false);
  assert.equal(seen.packet.requested_transition, 'SKAP_ACCOUNT_METADATA_ADMIT');
  assert.equal(seen.packet.direction, 'KNOWLEDGEVAULT_TO_SKAP_VAULT');

  /* and the materialization is non-authorizing on the canonical route */
  const m = seen.materialization;
  assert.equal(m.credential_authority, 'TV/TVC');
  assert.equal(m.github_token_runtime_authority, 'NONE');
  assert.equal(m.transport_grants_execution_authority, false);
  assert.equal(m.request_grants_execution_authority, false);
  assert.equal(m.claim_or_fence_minted, false);
  assert.deepEqual(m.boundary_path, ['KV', 'SKAP_VAULT']);
  assert.equal(m.downstream_owner_ref, 'StegVerse-Labs/TVC');
  assert.ok(m.intr_boundary_envelope);
  assert.equal(m.intr_boundary_envelope.canonical_state_changed, false);
  assert.equal(m.intr_boundary_envelope.credential_material_transferred, false);

  /* fail closed: no registered Node */
  bridge = install({ node: nodeStub({ registered: false }) });
  await refuses(bridge.populateSelectedAccountMetadata(populationRequest()),
    /Register this device/, 'unregistered device must refuse');

  /* fail closed: queued but no TVC receipt — an outbox entry is not admission */
  bridge = install({ node: nodeStub({ receipt: 'absent' }) });
  await refuses(bridge.populateSelectedAccountMetadata(populationRequest()),
    /no TVC SKAP receipt observed/, 'queueing alone must not report accepted');

  /* fail closed: synthetic material cannot satisfy admission */
  bridge = install({ node: nodeStub({ receipt: 'synthetic' }) });
  await refuses(bridge.populateSelectedAccountMetadata(populationRequest()),
    /synthetic material/, 'synthetic receipt must refuse');

  /* fail closed: receipt bound to a different payload */
  bridge = install({ node: nodeStub({ receipt: 'drifted' }) });
  await refuses(bridge.populateSelectedAccountMetadata(populationRequest()),
    /payload binding invalid/, 'payload drift must refuse');

  /* fail closed: receipt bound to a different materialization */
  bridge = install({ node: nodeStub({ receipt: 'unbound' }) });
  await refuses(bridge.populateSelectedAccountMetadata(populationRequest()),
    /materialization binding invalid/, 'materialization drift must refuse');

  /* fail closed: receipt claiming non-TV/TVC credential authority */
  bridge = install({ node: nodeStub({ receipt: 'authorizing' }) });
  await refuses(bridge.populateSelectedAccountMetadata(populationRequest()),
    /credential authority invalid/, 'non TV/TVC receipt must refuse');

  /* fail closed: request boundary assertions must be present and false */
  bridge = install({});
  for (const key of ['synthetic_input_allowed', 'raw_provider_identifiers_present', 'credential_material_present']) {
    const bad = populationRequest();
    bad[key] = true;
    await refuses(bridge.populateSelectedAccountMetadata(bad),
      /boundary assertions invalid/, key + ' must be false');
  }

  /* fail closed: no accounts selected */
  const empty = populationRequest();
  empty.accounts = [];
  await refuses(bridge.populateSelectedAccountMetadata(empty),
    /at least one selected account/, 'empty selection must refuse');

  /* fail closed: observation read requires a bounded request */
  await refuses(bridge.listObservedAccounts({ include_secrets: true, include_raw_provider_ids: false }),
    /bounded observation request required/, 'secret-bearing observation request must refuse');

  /* fail closed: the generated connector must carry the profile */
  const saved = globalThis.StegVerseGeneratedInTr;
  globalThis.StegVerseGeneratedInTr = Object.assign({}, saved, {
    PROFILES: Object.fromEntries(Object.entries(saved.PROFILES).filter(([k]) => k !== PROFILE))
  });
  bridge = install({});
  await refuses(bridge.populateSelectedAccountMetadata(populationRequest()),
    /does not carry the kv-skap-account-metadata profile/, 'missing profile must refuse');
  globalThis.StegVerseGeneratedInTr = saved;

  console.log('my-kv-connected-accounts-bridge: all assertions passed');
})().catch((err) => { console.error(err); process.exit(1); });
