const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const path = require('node:path');
const test = require('node:test');

if (!globalThis.crypto) globalThis.crypto = crypto.webcrypto;
if (!globalThis.TextEncoder) globalThis.TextEncoder = require('node:util').TextEncoder;
require(path.resolve(__dirname, '../assets/kv-ui/resident-rendezvous-client.js'));
const client = globalThis.StegVerseResidentRendezvous;

test('client exposes only the fixed admitted StegOS/KV resident chain', () => {
  const request = client.buildResidentRequest();
  assert.equal(request.schema, 'stegverse.resident-execution-request/v1');
  assert.equal(request.request_id, 'RESIDENT-EXEC-STEGOS-KV-INTR-CHAIN-003');
  assert.equal(request.task_id, 'SHWP-STEGOS-KV-INTR-CHAIN-001');
  assert.equal(request.mode, 'STEGOS_KV_INTR_CHAIN');
  assert.equal(request.entrypoint, 'scripts/refresh_and_execute_resident_task.py');
  assert.deepEqual(request.steps, [
    'SHWP-STEGOS-SOVEREIGN-RELAY-MATERIALIZATION-001',
    'SHWP-STEGOS-RELAY-NODE-KV-CONTINUITY-001',
    'SHWP-DEVICE-KV-INTR-OBSERVATION-001',
  ]);
  assert.equal(request.steps.includes('SHWP-ENDPOINT-FANOUT-SOVEREIGN-RUNTIME-001'), false);
  assert.equal(request.credential_authority, 'TV/TVC');
  assert.equal(request.github_token_required, false);
  assert.equal(request.request_granted_authority, false);
  assert.equal(request.network_source_fetch_allowed, false);
  assert.equal(request.authority_effect, 'NONE_REQUEST_ONLY');
  assert.match(request.note, /shared HB signal refs\/digests/);
  assert.equal('command' in request, false);
  assert.equal('argv' in request, false);
});

test('envelope binds exact resident request digest and one-hour lease', async () => {
  const now = new Date('2026-08-31T02:40:00Z');
  const request = await client.buildRendezvousRequest({
    targetNodeRef: 'SV-NODE-' + 'a'.repeat(24),
    authorizationRef: 'node-receipt-1-sha256:' + 'b'.repeat(64),
    leaseMs: 3600000,
    now,
  });
  assert.match(request.request_id, /^resident-rendezvous-/);
  assert.equal(request.consumer, 'stegos_kv_intr_chain');
  assert.equal(request.resident_request_sha256, await client.sha256Uri(request.resident_request));
  assert.equal(request.submitted_at, '2026-08-31T02:40:00.000Z');
  assert.equal(request.expires_at, '2026-08-31T03:40:00.000Z');
  assert.equal(request.authority_effect, 'NONE_REQUEST_ONLY');

  await assert.rejects(
    client.buildRendezvousRequest({
      targetNodeRef: 'SV-NODE-' + 'a'.repeat(24),
      authorizationRef: 'node-receipt-1-sha256:' + 'b'.repeat(64),
      leaseMs: 3600001,
      now,
    }),
    /lease/
  );
});

test('registered Node Receipt #1 becomes non-authorizing submitter provenance', async () => {
  const nodeId = 'SV-NODE-' + 'c'.repeat(24);
  const digest = 'd'.repeat(64);
  const nodeApi = {
    status: async () => ({
      registered: true,
      registration: { node_id: nodeId, receipt_sha256: digest },
      receipts: [{
        receipt_number: 1,
        transition: 'NODE_REGISTERED',
        node_id: nodeId,
        receipt_sha256: digest,
      }],
    }),
  };
  assert.equal(
    await client.resolveSubmitterProvenance(nodeApi),
    'node-receipt-1-sha256:' + digest
  );
  await assert.rejects(
    client.resolveSubmitterProvenance({ status: async () => ({ registered: false }) }),
    error => error.code === 'REGISTER_DEVICE_REQUIRED'
  );
});

test('resident discovery requires one canonical available request-003 target', async () => {
  const target = 'SV-NODE-' + 'e'.repeat(24);
  const fetchImpl = async (url, options) => {
    assert.equal(url, 'https://stegverse.org/api/resident-rendezvous/v1/discovery');
    assert.equal(options.method, 'GET');
    assert.equal(options.credentials, 'omit');
    return {
      ok: true,
      status: 200,
      headers: { get: () => 'application/json' },
      json: async () => ({
        schema: 'stegverse.resident-rendezvous.discovery/v1',
        consumer: 'stegos_kv_intr_chain',
        current_resident_request_id: 'RESIDENT-EXEC-STEGOS-KV-INTR-CHAIN-003',
        state: 'AVAILABLE',
        target_node_ref: target,
        expires_at: '2026-08-31T17:00:00Z',
        gateway_execution_authority: 'NONE',
        credential_authority: 'TV/TVC',
        discovery_grants_authority: false,
        authority_effect: 'NONE_DISCOVERY_ONLY',
      }),
    };
  };
  const result = await client.discover({
    gatewayBaseUrl: 'https://stegverse.org',
    fetchImpl,
  });
  assert.equal(result.target_node_ref, target);

  assert.throws(
    () => client.validateDiscovery({
      schema: 'stegverse.resident-rendezvous.discovery/v1',
      consumer: 'stegos_kv_intr_chain',
      current_resident_request_id: 'RESIDENT-EXEC-STEGOS-KV-INTR-CHAIN-003',
      state: 'AVAILABLE',
      target_node_ref: 'node:primary',
      gateway_execution_authority: 'NONE',
      credential_authority: 'TV/TVC',
      discovery_grants_authority: false,
      authority_effect: 'NONE_DISCOVERY_ONLY',
    }),
    /canonical sovereign resident target/
  );
});

test('submitDiscovered performs discovery then exact request-003 submit from Receipt #1 provenance', async () => {
  const target = 'SV-NODE-' + 'f'.repeat(24);
  const digest = '1'.repeat(64);
  const nodeId = 'SV-NODE-' + '2'.repeat(24);
  const nodeApi = {
    status: async () => ({
      registered: true,
      registration: { node_id: nodeId, receipt_sha256: digest },
      receipts: [{
        receipt_number: 1,
        transition: 'NODE_REGISTERED',
        node_id: nodeId,
        receipt_sha256: digest,
      }],
    }),
  };
  let posted;
  const fetchImpl = async (url, options) => {
    if (options.method === 'GET') {
      return {
        ok: true,
        status: 200,
        headers: { get: () => 'application/json' },
        json: async () => ({
          schema: 'stegverse.resident-rendezvous.discovery/v1',
          consumer: 'stegos_kv_intr_chain',
          current_resident_request_id: 'RESIDENT-EXEC-STEGOS-KV-INTR-CHAIN-003',
          state: 'AVAILABLE',
          target_node_ref: target,
          expires_at: '2026-08-31T17:00:00Z',
          gateway_execution_authority: 'NONE',
          credential_authority: 'TV/TVC',
          discovery_grants_authority: false,
          authority_effect: 'NONE_DISCOVERY_ONLY',
        }),
      };
    }
    posted = { url, options, request: JSON.parse(options.body) };
    return {
      ok: true,
      status: 200,
      headers: { get: () => 'application/json' },
      json: async () => ({
        schema: 'stegverse.resident-rendezvous.store-result/v1',
        state: 'PENDING',
        request_id: posted.request.request_id,
        resident_request_sha256: posted.request.resident_request_sha256,
        gateway_execution_authority: 'NONE',
        credential_authority: 'TV/TVC',
        authority_effect: 'NONE_REQUEST_ONLY',
      }),
    };
  };
  const result = await client.submitDiscovered({
    gatewayBaseUrl: 'https://stegverse.org',
    fetchImpl,
    nodeApi,
  });
  assert.equal(posted.request.target_node_ref, target);
  assert.equal(
    posted.request.submitter_authorization_ref,
    'node-receipt-1-sha256:' + digest
  );
  assert.equal(
    posted.options.headers['X-StegVerse-Authorization-Id'],
    'node-receipt-1-sha256:' + digest
  );
  assert.equal(posted.request.resident_request.request_id, 'RESIDENT-EXEC-STEGOS-KV-INTR-CHAIN-003');
  assert.equal(result.target_node_ref, target);
  assert.equal(result.blind_retry_allowed, false);
});

test('gateway must be clean HTTPS', () => {
  assert.equal(client.validateGatewayBaseUrl('https://stegverse.org'), 'https://stegverse.org');
  assert.throws(() => client.validateGatewayBaseUrl('http://stegverse.org'), /HTTPS/);
  assert.throws(() => client.validateGatewayBaseUrl('https://user:pass@stegverse.org'), /HTTPS/);
});

test('submit omits credentials and rejects authority escalation', async () => {
  let seen;
  const fetchImpl = async (url, options) => {
    seen = { url, options, request: JSON.parse(options.body) };
    return {
      ok: true,
      status: 200,
      headers: { get: () => 'application/json' },
      json: async () => ({
        schema: 'stegverse.resident-rendezvous.store-result/v1',
        state: 'PENDING',
        request_id: seen.request.request_id,
        resident_request_sha256: seen.request.resident_request_sha256,
        gateway_execution_authority: 'NONE',
        credential_authority: 'TV/TVC',
        authority_effect: 'NONE_REQUEST_ONLY',
      }),
    };
  };
  const result = await client.submit({
    gatewayBaseUrl: 'https://stegverse.org',
    targetNodeRef: 'SV-NODE-' + 'a'.repeat(24),
    authorizationRef: 'node-receipt-1-sha256:' + 'b'.repeat(64),
    fetchImpl,
  });
  assert.equal(seen.options.credentials, 'omit');
  assert.equal(seen.options.redirect, 'error');
  assert.equal(seen.options.headers['X-StegVerse-Authorization-Id'], 'node-receipt-1-sha256:' + 'b'.repeat(64));
  assert.equal(result.gateway_execution_authority, 'NONE');
  assert.equal(result.blind_retry_allowed, false);
});

test('ambiguous transport outcome forbids blind retry', async () => {
  await assert.rejects(
    client.submit({
      gatewayBaseUrl: 'https://stegverse.org',
      targetNodeRef: 'SV-NODE-' + 'a'.repeat(24),
      authorizationRef: 'node-receipt-1-sha256:' + 'b'.repeat(64),
      fetchImpl: async () => { throw new Error('network'); },
    }),
    error => error.code === 'VERIFY_EXTERNALLY' && error.blind_retry_allowed === false
  );
});
