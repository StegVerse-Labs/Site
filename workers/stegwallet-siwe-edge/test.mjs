import assert from 'node:assert/strict';
import worker from './src/index.js';

const TOKEN = `edge-${'a'.repeat(40)}`;
const ENV = {SIWE_UPSTREAM_ORIGIN: 'https://stegwallet-siwe.onrender.com/', SIWE_EDGE_TOKEN: TOKEN};

async function withFetch(handler, action) {
  const previous = globalThis.fetch;
  globalThis.fetch = handler;
  try { return await action(); }
  finally { globalThis.fetch = previous; }
}

async function testProxy() {
  let observed;
  const response = await withFetch(async (url, init) => {
    observed = {url: String(url), init};
    return new Response('{"status":"READY"}\n', {
      status: 200,
      headers: {'content-type': 'application/json', 'set-cookie': '__Host-stegwallet-siwe=abc; Path=/; Secure; HttpOnly; SameSite=Strict'},
    });
  }, () => worker.fetch(new Request('https://stegverse.org/api/stegwallet/siwe/challenge', {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      'origin': 'https://stegverse.org',
      'x-stegwallet-edge-token': 'client-forgery',
      'cf-connecting-ip': '203.0.113.10',
    },
    body: '{"wallet_address":"0x1111111111111111111111111111111111111111"}',
  }), ENV));

  assert.equal(response.status, 200);
  assert.equal(observed.url, 'https://stegwallet-siwe.onrender.com/api/stegwallet/siwe/challenge');
  assert.equal(observed.init.method, 'POST');
  assert.equal(observed.init.headers.get('x-stegwallet-edge-token'), TOKEN);
  assert.equal(observed.init.headers.get('x-forwarded-host'), 'stegverse.org');
  assert.equal(observed.init.headers.get('x-forwarded-proto'), 'https');
  assert.equal(observed.init.headers.get('x-forwarded-for'), '203.0.113.10');
  assert.match(response.headers.get('set-cookie'), /__Host-stegwallet-siwe=abc/);
  assert.equal(response.headers.get('cache-control'), 'no-store');
  assert.equal(response.headers.get('x-stegwallet-edge'), 'stegwallet-siwe-v1');
}

async function testBoundaries() {
  let called = false;
  const noFetch = async () => { called = true; return new Response('unexpected'); };

  const wrongHost = await withFetch(noFetch, () => worker.fetch(new Request('https://evil.example/api/stegwallet/siwe/health'), ENV));
  assert.equal(wrongHost.status, 403);

  const unknown = await withFetch(noFetch, () => worker.fetch(new Request('https://stegverse.org/api/stegwallet/siwe/unknown'), ENV));
  assert.equal(unknown.status, 404);

  const method = await withFetch(noFetch, () => worker.fetch(new Request('https://stegverse.org/api/stegwallet/siwe/session', {method: 'POST'}), ENV));
  assert.equal(method.status, 405);

  const query = await withFetch(noFetch, () => worker.fetch(new Request('https://stegverse.org/api/stegwallet/siwe/health?bypass=1'), ENV));
  assert.equal(query.status, 400);
  assert.equal(called, false);
}

async function testConfigurationFailure() {
  const response = await worker.fetch(new Request('https://stegverse.org/api/stegwallet/siwe/health'), {
    SIWE_UPSTREAM_ORIGIN: 'https://siwe-origin.invalid/',
    SIWE_EDGE_TOKEN: 'short',
  });
  assert.equal(response.status, 503);
  const payload = await response.json();
  assert.equal(payload.status, 'CONFIGURATION_REQUIRED');
  assert.equal(payload.transaction_authority, false);
  assert.equal(payload.execution_authority, false);
  assert.equal(payload.delegation_authority, false);
  assert.equal(payload.custody_recorded, false);
}

await testProxy();
await testBoundaries();
await testConfigurationFailure();
console.log('STEGWALLET_SIWE_EDGE_BEHAVIOR_PASS');
