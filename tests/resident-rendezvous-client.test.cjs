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
  assert.equal(request.request_id, 'RESIDENT-EXEC-STEGOS-KV-INTR-CHAIN-002');
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
  assert.equal('command' in request, false);
  assert.equal('argv' in request, false);
});

test('envelope binds exact resident request digest and one-hour lease', async () => {
  const now = new Date('2026-08-31T02:40:00Z');
  const request = await client.buildRendezvousRequest({
    targetNodeRef: 'node:primary',
    authorizationRef: 'owner:opaque',
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
      targetNodeRef: 'node:primary',
      authorizationRef: 'owner:opaque',
      leaseMs: 3600001,
      now,
    }),
    /lease/
  );
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
    targetNodeRef: 'node:primary',
    authorizationRef: 'owner:opaque',
    fetchImpl,
  });
  assert.equal(seen.options.credentials, 'omit');
  assert.equal(seen.options.redirect, 'error');
  assert.equal(seen.options.headers['X-StegVerse-Authorization-Id'], 'owner:opaque');
  assert.equal(result.gateway_execution_authority, 'NONE');
  assert.equal(result.blind_retry_allowed, false);
});

test('ambiguous transport outcome forbids blind retry', async () => {
  await assert.rejects(
    client.submit({
      gatewayBaseUrl: 'https://stegverse.org',
      targetNodeRef: 'node:primary',
      authorizationRef: 'owner:opaque',
      fetchImpl: async () => { throw new Error('network'); },
    }),
    error => error.code === 'VERIFY_EXTERNALLY' && error.blind_retry_allowed === false
  );
});
