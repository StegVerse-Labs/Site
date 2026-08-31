(() => {
  'use strict';

  const REQUEST_SCHEMA = 'stegverse.resident-rendezvous.request/v1';
  const RESIDENT_SCHEMA = 'stegverse.resident-execution-request/v1';
  const STORE_RESULT_SCHEMA = 'stegverse.resident-rendezvous.store-result/v1';
  const DISCOVERY_SCHEMA = 'stegverse.resident-rendezvous.discovery/v1';
  const CURRENT_REQUEST_ID = 'RESIDENT-EXEC-STEGOS-KV-INTR-CHAIN-003';
  const NODE_REF_RE = /^SV-NODE-[0-9a-f]{24}$/;
  const RECEIPT_SHA_RE = /^[0-9a-f]{64}$/;
  const PROVENANCE_RE = /^node-receipt-1-sha256:[0-9a-f]{64}$/;
  const CONSUMER = 'stegos_kv_intr_chain';
  const TASK_ID = 'SHWP-STEGOS-KV-INTR-CHAIN-001';
  const MODE = 'STEGOS_KV_INTR_CHAIN';
  const ENTRYPOINT = 'scripts/refresh_and_execute_resident_task.py';
  const STEPS = Object.freeze([
    'SHWP-STEGOS-SOVEREIGN-RELAY-MATERIALIZATION-001',
    'SHWP-STEGOS-RELAY-NODE-KV-CONTINUITY-001',
    'SHWP-DEVICE-KV-INTR-OBSERVATION-001',
  ]);
  const MAX_LEASE_MS = 60 * 60 * 1000;

  function requireWebCrypto() {
    if (!(globalThis.crypto && crypto.subtle && crypto.getRandomValues)) {
      throw new Error('FAIL_CLOSED: WebCrypto required');
    }
  }

  function canonical(value) {
    if (value === null || typeof value !== 'object') return JSON.stringify(value);
    if (Array.isArray(value)) return '[' + value.map(canonical).join(',') + ']';
    return '{' + Object.keys(value).sort().map(
      key => JSON.stringify(key) + ':' + canonical(value[key])
    ).join(',') + '}';
  }

  function randomId(prefix) {
    requireWebCrypto();
    const bytes = new Uint8Array(16);
    crypto.getRandomValues(bytes);
    return prefix + '-' + Array.from(bytes, b => b.toString(16).padStart(2, '0')).join('');
  }

  async function sha256Uri(value) {
    requireWebCrypto();
    const digest = await crypto.subtle.digest(
      'SHA-256',
      new TextEncoder().encode(canonical(value))
    );
    const hex = Array.from(new Uint8Array(digest), b => b.toString(16).padStart(2, '0')).join('');
    return 'sha256:' + hex;
  }

  function validateGatewayBaseUrl(value) {
    const url = new URL(value);
    if (url.protocol !== 'https:' || url.username || url.password || url.search || url.hash) {
      throw new Error('FAIL_CLOSED: resident rendezvous requires a clean HTTPS gateway origin');
    }
    url.pathname = '/';
    return url.origin;
  }

  function validateOpaqueRef(value, label) {
    if (typeof value !== 'string' || !value || value.length > 256 || /[\r\n]/.test(value)) {
      throw new Error('FAIL_CLOSED: invalid ' + label);
    }
    return value;
  }

  function validateTargetNodeRef(value) {
    if (typeof value !== 'string' || !NODE_REF_RE.test(value)) {
      throw new Error('FAIL_CLOSED: canonical sovereign resident target required');
    }
    return value;
  }

  function validateSubmitterProvenanceRef(value) {
    if (typeof value !== 'string' || !PROVENANCE_RE.test(value)) {
      throw new Error('FAIL_CLOSED: validated Node Receipt #1 provenance required');
    }
    return value;
  }

  async function resolveSubmitterProvenance(nodeApi = globalThis.StegVerseNodeContinuity) {
    if (!nodeApi || typeof nodeApi.status !== 'function') {
      throw new Error('FAIL_CLOSED: canonical StegVerse Node continuity unavailable');
    }
    const current = await nodeApi.status();
    if (!current || current.registered !== true || !current.registration) {
      const error = new Error('REGISTER_DEVICE_REQUIRED');
      error.code = 'REGISTER_DEVICE_REQUIRED';
      throw error;
    }
    const reg = current.registration;
    const receipts = Array.isArray(current.receipts) ? current.receipts : [];
    const genesis = receipts[0];
    if (!genesis || genesis.receipt_number !== 1 || genesis.transition !== 'NODE_REGISTERED') {
      throw new Error('FAIL_CLOSED: validated Node Receipt #1 unavailable');
    }
    if (reg.node_id !== genesis.node_id || reg.receipt_sha256 !== genesis.receipt_sha256 ||
        !RECEIPT_SHA_RE.test(String(reg.receipt_sha256 || ''))) {
      throw new Error('FAIL_CLOSED: Node registration/Receipt #1 provenance mismatch');
    }
    return 'node-receipt-1-sha256:' + reg.receipt_sha256;
  }

  function validateDiscovery(payload) {
    if (!payload || payload.schema !== DISCOVERY_SCHEMA ||
        payload.consumer !== CONSUMER ||
        payload.current_resident_request_id !== CURRENT_REQUEST_ID ||
        payload.gateway_execution_authority !== 'NONE' ||
        payload.credential_authority !== 'TV/TVC' ||
        payload.discovery_grants_authority !== false ||
        payload.authority_effect !== 'NONE_DISCOVERY_ONLY') {
      throw new Error('FAIL_CLOSED: resident discovery response invalid');
    }
    if (payload.state === 'UNAVAILABLE') {
      const error = new Error('RESIDENT_RENDEZVOUS_UNAVAILABLE');
      error.code = 'RESIDENT_RENDEZVOUS_UNAVAILABLE';
      throw error;
    }
    if (payload.state === 'AMBIGUOUS') {
      const error = new Error('RESIDENT_RENDEZVOUS_AMBIGUOUS');
      error.code = 'RESIDENT_RENDEZVOUS_AMBIGUOUS';
      throw error;
    }
    if (payload.state !== 'AVAILABLE') {
      throw new Error('FAIL_CLOSED: resident discovery state invalid');
    }
    validateTargetNodeRef(payload.target_node_ref);
    return Object.freeze({
      state: 'AVAILABLE',
      target_node_ref: payload.target_node_ref,
      expires_at: payload.expires_at || null,
      current_resident_request_id: CURRENT_REQUEST_ID,
      gateway_execution_authority: 'NONE',
      credential_authority: 'TV/TVC',
      authority_effect: 'NONE_DISCOVERY_ONLY',
    });
  }

  async function discover({
    gatewayBaseUrl,
    fetchImpl = globalThis.fetch,
  }) {
    if (typeof fetchImpl !== 'function') throw new Error('FAIL_CLOSED: fetch unavailable');
    const origin = validateGatewayBaseUrl(gatewayBaseUrl);
    let response;
    try {
      response = await fetchImpl(origin + '/api/resident-rendezvous/v1/discovery', {
        method: 'GET',
        redirect: 'error',
        credentials: 'omit',
        referrerPolicy: 'no-referrer',
        cache: 'no-store',
        headers: { 'Accept': 'application/json' },
      });
    } catch (error) {
      const unavailable = new Error('RESIDENT_RENDEZVOUS_DISCOVERY_UNREACHABLE');
      unavailable.code = 'RESIDENT_RENDEZVOUS_DISCOVERY_UNREACHABLE';
      throw unavailable;
    }
    if (!response.ok) {
      throw new Error('FAIL_CLOSED: resident discovery rejected (' + response.status + ')');
    }
    const contentType = String(response.headers?.get?.('content-type') || '').toLowerCase();
    if (contentType && !contentType.includes('application/json')) {
      throw new Error('FAIL_CLOSED: resident discovery content type invalid');
    }
    return validateDiscovery(await response.json());
  }

  function buildResidentRequest() {
    return {
      schema: RESIDENT_SCHEMA,
      request_id: CURRENT_REQUEST_ID,
      state: 'REQUESTED',
      task_id: TASK_ID,
      mode: MODE,
      entrypoint: ENTRYPOINT,
      steps: [...STEPS],
      credential_authority: 'TV/TVC',
      github_token_required: false,
      github_token_runtime_authority: 'NONE',
      heartbeat_grants_execution_authority: false,
      request_granted_authority: false,
      network_source_fetch_allowed: false,
      second_machine_required: false,
      authority_effect: 'NONE_REQUEST_ONLY',
      note: 'Advance only the already-admitted StegOS relay materialization -> Node-KV continuity -> DEVICE_KV_INTR observation chain; DEVICE_KV terminal requires authentic HB-derived carrier transport plus exact shared HB signal refs/digests and independent recovery proof.',
    };
  }

  async function buildRendezvousRequest({
    targetNodeRef,
    authorizationRef,
    leaseMs = MAX_LEASE_MS,
    now = new Date(),
  }) {
    validateTargetNodeRef(targetNodeRef);
    validateSubmitterProvenanceRef(authorizationRef);
    if (!Number.isFinite(leaseMs) || leaseMs <= 0 || leaseMs > MAX_LEASE_MS) {
      throw new Error('FAIL_CLOSED: rendezvous lease must be between 1 ms and 1 hour');
    }
    const residentRequest = buildResidentRequest();
    const submittedAt = new Date(now);
    if (!Number.isFinite(submittedAt.getTime())) throw new Error('FAIL_CLOSED: invalid submission time');
    const expiresAt = new Date(submittedAt.getTime() + leaseMs);
    return {
      schema: REQUEST_SCHEMA,
      request_id: randomId('resident-rendezvous'),
      target_node_ref: targetNodeRef,
      consumer: CONSUMER,
      resident_request: residentRequest,
      resident_request_sha256: await sha256Uri(residentRequest),
      submitted_at: submittedAt.toISOString(),
      expires_at: expiresAt.toISOString(),
      submitter_authorization_ref: authorizationRef,
      authority_effect: 'NONE_REQUEST_ONLY',
    };
  }

  function validateStoreResult(request, payload) {
    if (!payload || payload.schema !== STORE_RESULT_SCHEMA || payload.state !== 'PENDING') {
      throw new Error('FAIL_CLOSED: resident rendezvous store response invalid');
    }
    if (payload.request_id !== request.request_id ||
        payload.resident_request_sha256 !== request.resident_request_sha256) {
      throw new Error('FAIL_CLOSED: resident rendezvous response binding mismatch');
    }
    if (payload.gateway_execution_authority !== 'NONE' ||
        payload.credential_authority !== 'TV/TVC' ||
        payload.authority_effect !== 'NONE_REQUEST_ONLY') {
      throw new Error('FAIL_CLOSED: resident rendezvous response attempted authority escalation');
    }
    return Object.freeze({
      state: 'PENDING',
      request_id: payload.request_id,
      resident_request_sha256: payload.resident_request_sha256,
      gateway_execution_authority: 'NONE',
      credential_authority: 'TV/TVC',
      blind_retry_allowed: false,
      authority_effect: 'NONE_REQUEST_ONLY',
    });
  }

  async function submit({
    gatewayBaseUrl,
    targetNodeRef,
    authorizationRef,
    leaseMs = MAX_LEASE_MS,
    fetchImpl = globalThis.fetch,
  }) {
    if (typeof fetchImpl !== 'function') throw new Error('FAIL_CLOSED: fetch unavailable');
    const origin = validateGatewayBaseUrl(gatewayBaseUrl);
    const request = await buildRendezvousRequest({
      targetNodeRef,
      authorizationRef,
      leaseMs,
    });
    let response;
    try {
      response = await fetchImpl(origin + '/api/resident-rendezvous/v1/requests', {
        method: 'POST',
        redirect: 'error',
        credentials: 'omit',
        referrerPolicy: 'no-referrer',
        cache: 'no-store',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'X-StegVerse-Authorization-Id': authorizationRef,
        },
        body: JSON.stringify(request),
      });
    } catch (error) {
      const ambiguous = new Error(
        'VERIFY_EXTERNALLY: resident rendezvous submission outcome ambiguous; blind retry forbidden'
      );
      ambiguous.code = 'VERIFY_EXTERNALLY';
      ambiguous.blind_retry_allowed = false;
      throw ambiguous;
    }
    if (!response.ok) {
      throw new Error('FAIL_CLOSED: resident rendezvous request rejected (' + response.status + ')');
    }
    const contentType = String(response.headers?.get?.('content-type') || '').toLowerCase();
    if (contentType && !contentType.includes('application/json')) {
      throw new Error('FAIL_CLOSED: resident rendezvous response content type invalid');
    }
    const payload = await response.json();
    return validateStoreResult(request, payload);
  }

  async function submitDiscovered({
    gatewayBaseUrl = (globalThis.location && globalThis.location.origin) || '',
    leaseMs = MAX_LEASE_MS,
    fetchImpl = globalThis.fetch,
    nodeApi = globalThis.StegVerseNodeContinuity,
  } = {}) {
    const authorizationRef = await resolveSubmitterProvenance(nodeApi);
    const discovery = await discover({ gatewayBaseUrl, fetchImpl });
    const result = await submit({
      gatewayBaseUrl,
      targetNodeRef: discovery.target_node_ref,
      authorizationRef,
      leaseMs,
      fetchImpl,
    });
    return Object.freeze({
      ...result,
      target_node_ref: discovery.target_node_ref,
      submitter_provenance_ref: authorizationRef,
      resident_discovery_state: discovery.state,
      resident_discovery_authority_effect: 'NONE_DISCOVERY_ONLY',
    });
  }

  globalThis.StegVerseResidentRendezvous = Object.freeze({
    requestSchema: REQUEST_SCHEMA,
    residentSchema: RESIDENT_SCHEMA,
    consumer: CONSUMER,
    taskId: TASK_ID,
    mode: MODE,
    steps: STEPS,
    maxLeaseMs: MAX_LEASE_MS,
    canonical,
    sha256Uri,
    validateGatewayBaseUrl,
    validateTargetNodeRef,
    validateSubmitterProvenanceRef,
    resolveSubmitterProvenance,
    validateDiscovery,
    discover,
    buildResidentRequest,
    buildRendezvousRequest,
    validateStoreResult,
    submit,
    submitDiscovered,
  });
})();
