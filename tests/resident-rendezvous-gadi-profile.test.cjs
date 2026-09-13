const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const { webcrypto } = require('node:crypto');

function loadClient() {
  const source = fs.readFileSync('assets/kv-ui/resident-rendezvous-client.js', 'utf8');
  const context = {
    console,
    URL,
    TextEncoder,
    crypto: webcrypto,
    location: { origin: 'https://stegverse.org' },
  };
  context.globalThis = context;
  vm.createContext(context);
  vm.runInContext(source, context);
  return context.StegVerseResidentRendezvous;
}

test('GADI profile builds exact non-authorizing canonical request', async () => {
  const client = loadClient();
  const inner = client.buildGadiResidentRequest();
  assert.equal(inner.request_id, 'RESIDENT-OBSERVE-GADI-RUNTIME-001');
  assert.equal(inner.task_id, 'GADI-RESIDENT-EXECUTION-001');
  assert.equal(inner.parent_task_id, 'GADI-001');
  assert.equal(inner.mode, 'GADI_RUNTIME_OBSERVATION');
  assert.equal(inner.request_granted_authority, false);
  assert.equal(inner.network_source_fetch_allowed, false);
  assert.equal(inner.second_machine_required, false);
  assert.equal(inner.workercoordinator_may_be_visited_only_after_nonclaim_readiness, true);

  const envelope = await client.buildProfileRendezvousRequest({
    targetNodeRef: 'SV-NODE-' + 'a'.repeat(24),
    consumer: client.gadiConsumer,
    now: new Date('2026-09-13T05:15:00Z'),
  });
  assert.equal(envelope.consumer, 'gadi_runtime_observation');
  assert.deepEqual(envelope.resident_request, inner);
  assert.equal(envelope.submitter_authorization_ref, 'transport-correlation:' + envelope.resident_request_sha256);
  assert.match(envelope.submitter_authorization_ref, /^transport-correlation:sha256:[0-9a-f]{64}$/);
});

test('GADI discovery is consumer-scoped and node is routing only', async () => {
  const client = loadClient();
  const target = 'SV-NODE-' + 'b'.repeat(24);
  let observedUrl = null;
  const fetchImpl = async (url, options) => {
    observedUrl = url;
    assert.equal(options.credentials, 'omit');
    return {
      ok: true,
      status: 200,
      headers: { get: () => 'application/json' },
      json: async () => ({
        schema: 'stegverse.resident-rendezvous.discovery/v1',
        consumer: 'gadi_runtime_observation',
        current_resident_request_id: 'RESIDENT-OBSERVE-GADI-RUNTIME-001',
        state: 'AVAILABLE',
        target_node_ref: target,
        expires_at: '2026-09-13T05:20:00Z',
        gateway_execution_authority: 'NONE',
        credential_authority: 'TV/TVC',
        discovery_grants_authority: false,
        authority_effect: 'NONE_DISCOVERY_ONLY',
      }),
    };
  };
  const discovery = await client.discover({
    gatewayBaseUrl: 'https://stegverse.org',
    fetchImpl,
    consumer: client.gadiConsumer,
  });
  assert.equal(observedUrl, 'https://stegverse.org/api/resident-rendezvous/v1/discovery?consumer=gadi_runtime_observation');
  assert.equal(discovery.target_node_ref, target);
  assert.equal(discovery.target_node_identity_role, 'ROUTING_ONLY');
  assert.equal(discovery.gateway_execution_authority, 'NONE');
});

test('GADI discovered submission never requests Node Receipt user verification', async () => {
  const client = loadClient();
  const target = 'SV-NODE-' + 'c'.repeat(24);
  let posted = null;
  const fetchImpl = async (url, options) => {
    if (url.includes('/discovery')) {
      return {
        ok: true, status: 200, headers: { get: () => 'application/json' },
        json: async () => ({
          schema: 'stegverse.resident-rendezvous.discovery/v1', consumer: 'gadi_runtime_observation',
          current_resident_request_id: 'RESIDENT-OBSERVE-GADI-RUNTIME-001', state: 'AVAILABLE',
          target_node_ref: target, expires_at: '2026-09-13T05:20:00Z',
          gateway_execution_authority: 'NONE', credential_authority: 'TV/TVC',
          discovery_grants_authority: false, authority_effect: 'NONE_DISCOVERY_ONLY',
        }),
      };
    }
    posted = { url, options, body: JSON.parse(options.body) };
    return {
      ok: true, status: 200, headers: { get: () => 'application/json' },
      json: async () => ({
        schema: 'stegverse.resident-rendezvous.store-result/v1', state: 'PENDING',
        request_id: posted.body.request_id,
        resident_request_sha256: posted.body.resident_request_sha256,
        gateway_execution_authority: 'NONE', credential_authority: 'TV/TVC',
        authority_effect: 'NONE_REQUEST_ONLY',
      }),
    };
  };

  const result = await client.submitConsumerDiscovered({
    consumer: client.gadiConsumer,
    gatewayBaseUrl: 'https://stegverse.org',
    fetchImpl,
  });
  assert.equal(posted.body.consumer, 'gadi_runtime_observation');
  assert.match(posted.body.submitter_authorization_ref, /^transport-correlation:sha256:/);
  assert.equal(posted.options.headers['X-StegVerse-Authorization-Id'], posted.body.submitter_authorization_ref);
  assert.equal(result.transport_correlation_only, true);
  assert.equal(result.user_verification_authority, 'KV/SKAP Vault');
  assert.equal(result.target_node_identity_role, 'ROUTING_ONLY');
});
