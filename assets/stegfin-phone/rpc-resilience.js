(() => {
  'use strict';

  const ORIGINAL_FETCH = window.fetch.bind(window);
  const PRIMARY = 'https://mainnet.base.org';
  const ENDPOINTS = Object.freeze([
    Object.freeze({ id: 'base-public', url: PRIMARY, authority: 'PUBLIC_BOOTSTRAP', credential_requirement: 'NONE' }),
    Object.freeze({ id: 'publicnode-base', url: 'https://base-rpc.publicnode.com', authority: 'CREDENTIAL_FREE_FALLBACK', credential_requirement: 'NONE' }),
  ]);
  const EXPECTED_CHAIN_ID = '0x2105';
  const MAX_ATTEMPTS_PER_ENDPOINT = 2;
  const RETRYABLE_HTTP = new Set([408, 425, 429, 500, 502, 503, 504]);
  const MAX_EVENTS = 64;
  const STORAGE_KEY = 'stegfin:rpc-resilience:v1';
  const verified = new Map();
  let probeId = 900000000;

  function sleep(ms) { return new Promise((resolve) => setTimeout(resolve, ms)); }
  function retryDelay(attempt) { return attempt === 0 ? 250 : 750; }
  function now() { return new Date().toISOString(); }
  function record(event) {
    const row = { at: now(), ...event, credential_authority: 'TV/TVC', non_tv_tvc_secret_or_token_used: false };
    try {
      const prior = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
      const rows = Array.isArray(prior) ? prior.slice(-(MAX_EVENTS - 1)) : [];
      rows.push(row);
      localStorage.setItem(STORAGE_KEY, JSON.stringify(rows));
    } catch (_) { /* evidence persistence failure must not alter RPC semantics */ }
    return row;
  }

  function requestBody(init) {
    if (!init || typeof init.body !== 'string') return null;
    try { return JSON.parse(init.body); } catch (_) { return null; }
  }

  function isRpcRequest(input, init) {
    const url = typeof input === 'string' ? input : input?.url;
    return url === PRIMARY && String(init?.method || 'GET').toUpperCase() === 'POST' && !!requestBody(init);
  }

  async function post(endpoint, body, init) {
    return ORIGINAL_FETCH(endpoint.url, {
      ...init,
      method: 'POST',
      credentials: 'omit',
      cache: 'no-store',
      headers: { ...(init?.headers || {}), 'content-type': 'application/json' },
      body: JSON.stringify(body),
    });
  }

  async function verifyEndpoint(endpoint, init) {
    if (verified.get(endpoint.id) === true) return;
    probeId += 1;
    const id = probeId;
    const response = await post(endpoint, { jsonrpc: '2.0', id, method: 'eth_chainId', params: [] }, init);
    if (!response.ok) throw new Error(`HTTP_${response.status}`);
    const payload = await response.clone().json();
    if (payload?.id !== id || payload?.error || String(payload?.result || '').toLowerCase() !== EXPECTED_CHAIN_ID) {
      record({ state: 'REJECTED', endpoint: endpoint.id, reason: 'CHAIN_ID_MISMATCH_OR_INVALID_PROBE' });
      throw new Error('CHAIN_ID_MISMATCH_OR_INVALID_PROBE');
    }
    verified.set(endpoint.id, true);
    record({ state: 'VERIFIED', endpoint: endpoint.id, chain_id: EXPECTED_CHAIN_ID });
  }

  async function resilientFetch(input, init) {
    if (!isRpcRequest(input, init)) return ORIGINAL_FETCH(input, init);
    const body = requestBody(init);
    const failures = [];

    for (const endpoint of ENDPOINTS) {
      for (let attempt = 0; attempt < MAX_ATTEMPTS_PER_ENDPOINT; attempt += 1) {
        try {
          if (endpoint.url !== PRIMARY) await verifyEndpoint(endpoint, init);
          const response = await post(endpoint, body, init);
          if (response.ok) {
            record({ state: 'SUCCESS', endpoint: endpoint.id, method: body.method, attempt: attempt + 1, failover: endpoint.url !== PRIMARY });
            return response;
          }
          failures.push(`${endpoint.id}:HTTP_${response.status}`);
          record({ state: 'RETRYABLE_FAILURE', endpoint: endpoint.id, method: body.method, attempt: attempt + 1, http_status: response.status });
          if (!RETRYABLE_HTTP.has(response.status)) break;
        } catch (error) {
          failures.push(`${endpoint.id}:${String(error?.message || error)}`);
          record({ state: 'TRANSPORT_FAILURE', endpoint: endpoint.id, method: body.method, attempt: attempt + 1, reason: String(error?.message || error) });
        }
        if (attempt + 1 < MAX_ATTEMPTS_PER_ENDPOINT) await sleep(retryDelay(attempt));
      }
    }

    record({ state: 'FAIL_CLOSED', method: body.method, failures });
    throw new Error(`Base RPC unavailable across admitted credential-free endpoints: ${failures.join(' | ')}`);
  }

  window.fetch = resilientFetch;
  window.StegFinRpcResilience = Object.freeze({
    schema: 'stegverse.stegfin.rpc_resilience.v1',
    expected_chain_id: EXPECTED_CHAIN_ID,
    endpoints: ENDPOINTS,
    credential_authority: 'TV/TVC',
    credential_requirement: 'NONE',
    non_tv_tvc_secret_or_token_used: false,
    hosted_runtime_required: false,
    render_required: false,
    getEvidence: () => {
      try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'); } catch (_) { return []; }
    },
  });
})();
