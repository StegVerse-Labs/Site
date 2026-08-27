(() => {
  'use strict';

  const ASSERTION_SCHEMA = 'stegverse.intr.identity-assertion/v1';
  const STEP_UP_SCHEMA = 'stegverse.intr.step-up-assertion/v1';
  const KV_ONBOARDING_REQUEST_SCHEMA = 'stegverse.site.kv_onboarding_request/v1';
  const KV_ONBOARDING_STAGE_RECEIPT_SCHEMA = 'stegverse.service_gateway.kv_onboarding_stage_receipt/v1';
  const LOCAL_ACCOUNT_KEY = 'stegverse.generic-login.accounts.v1';

  function nowIso() { return new Date().toISOString(); }
  function randomId(prefix) {
    const bytes = new Uint8Array(16);
    crypto.getRandomValues(bytes);
    return `${prefix}-${Array.from(bytes, b => b.toString(16).padStart(2, '0')).join('')}`;
  }
  async function sha256(value) {
    const bytes = new TextEncoder().encode(String(value));
    const digest = await crypto.subtle.digest('SHA-256', bytes);
    return Array.from(new Uint8Array(digest), b => b.toString(16).padStart(2, '0')).join('');
  }
  function stable(value) {
    if (value === null || typeof value !== 'object') return JSON.stringify(value);
    if (Array.isArray(value)) return '[' + value.map(stable).join(',') + ']';
    return '{' + Object.keys(value).sort().map(key => JSON.stringify(key) + ':' + stable(value[key])).join(',') + '}';
  }
  async function sha256Uri(value) {
    return 'sha256:' + await sha256(typeof value === 'string' ? value : stable(value));
  }
  function loadLocalAccounts() {
    try { return JSON.parse(localStorage.getItem(LOCAL_ACCOUNT_KEY) || '{}'); }
    catch (_) { return {}; }
  }
  function config() {
    const explicit = window.__STEGVERSE_INTR_CONFIG__ || {};
    return Object.freeze({
      mode: explicit.mode === 'REMOTE_INTR' ? 'REMOTE_INTR' : 'NOT_PROVISIONED',
      endpoint: typeof explicit.endpoint === 'string' ? explicit.endpoint : '',
      kvOnboardingEndpoint: typeof explicit.kvOnboardingEndpoint === 'string' ? explicit.kvOnboardingEndpoint : '',
      audience: typeof explicit.audience === 'string' ? explicit.audience : 'stegverse-kv-ui',
    });
  }
  function boundedAssertion({ subject, audience, level, source, schema = ASSERTION_SCHEMA }) {
    const issuedAt = nowIso();
    const expiresAt = new Date(Date.now() + 5 * 60 * 1000).toISOString();
    return Object.freeze({
      schema,
      assertion_id: randomId('intr'),
      subject: String(subject),
      audience: String(audience),
      assurance_level: level,
      source,
      issued_at: issuedAt,
      expires_at: expiresAt,
      credential_disclosed: false,
      raw_secret_present: false,
      authority_effect: 'ASSERTION_ONLY',
    });
  }

  async function remoteAuthenticate(username, password) {
    const cfg = config();
    if (cfg.mode !== 'REMOTE_INTR' || !cfg.endpoint) {
      return { ok: false, state: 'INTR_NOT_PROVISIONED', assertion: null };
    }
    const response = await fetch(cfg.endpoint, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      credentials: 'omit',
      cache: 'no-store',
      body: JSON.stringify({
        operation: 'VERIFY_ACCOUNT_LOGIN',
        audience: cfg.audience,
        username: String(username),
        password: String(password),
      }),
    });
    if (!response.ok) return { ok: false, state: 'INTR_UNAVAILABLE', assertion: null };
    const payload = await response.json();
    const a = payload && payload.assertion;
    if (!a || a.schema !== ASSERTION_SCHEMA || a.credential_disclosed !== false || a.raw_secret_present !== false) {
      return { ok: false, state: 'INVALID_INTR_ASSERTION', assertion: null };
    }
    return { ok: payload.ok === true, state: payload.ok === true ? 'LOGIN_ALLOWED' : 'LOGIN_DENIED', assertion: a };
  }

  async function remoteStepUp(subject) {
    const cfg = config();
    if (cfg.mode !== 'REMOTE_INTR' || !cfg.endpoint) {
      return { ok: false, state: 'INTR_NOT_PROVISIONED', assertion: null };
    }
    const response = await fetch(cfg.endpoint, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      credentials: 'omit',
      cache: 'no-store',
      body: JSON.stringify({
        operation: 'VERIFY_SKAP_STEP_UP',
        audience: 'stegverse-skap-ui',
        subject: String(subject),
      }),
    });
    if (!response.ok) return { ok: false, state: 'INTR_UNAVAILABLE', assertion: null };
    const payload = await response.json();
    const a = payload && payload.assertion;
    if (!a || a.schema !== STEP_UP_SCHEMA || a.credential_disclosed !== false || a.raw_secret_present !== false) {
      return { ok: false, state: 'INVALID_INTR_ASSERTION', assertion: null };
    }
    return { ok: payload.ok === true, state: payload.ok === true ? 'SKAP_STEP_UP_ALLOWED' : 'SKAP_STEP_UP_DENIED', assertion: a };
  }

  function stageReceiptAuthorityValid(receipt, request) {
    return Boolean(
      receipt &&
      receipt.schema === KV_ONBOARDING_STAGE_RECEIPT_SCHEMA &&
      receipt.decision === 'STAGED_FOR_CANONICAL_KV_AUTHORITY' &&
      receipt.request_id === request.request_id &&
      receipt.operation === request.operation &&
      receipt.account_ref_sha256 === request.account_ref_sha256 &&
      receipt.identity_assertion_id === request.identity_assertion_id &&
      receipt.identity_assertion_hash === request.identity_assertion_hash &&
      receipt.request_digest &&
      receipt.transport_protocol === 'InTr' &&
      receipt.completed_boundary === 'DEVICE_TO_KV_STAGING' &&
      receipt.kv_ownership_established === false &&
      receipt.owner_binding_established === false &&
      receipt.device_registration_established === false &&
      receipt.installation_admitted === false &&
      receipt.kv_active === false &&
      receipt.skap_unlocked === false &&
      receipt.gateway_identity_authority === false &&
      receipt.gateway_kv_authority === false &&
      receipt.gateway_device_authority === false &&
      receipt.gateway_execution_authority === 'NONE' &&
      receipt.authority_transfer === false &&
      receipt.secret_plaintext_present === false &&
      receipt.credential_material_recorded === false &&
      receipt.next_required_transition === 'CANONICAL_KV_OWNERSHIP_ADMISSION' &&
      receipt.blind_retry_allowed === false
    );
  }

  async function validateStageReceipt(receipt, request) {
    if (!stageReceiptAuthorityValid(receipt, request)) return false;
    if (receipt.request_digest !== await sha256Uri(request)) return false;
    const body = { ...receipt };
    const claimed = body.receipt_hash;
    delete body.receipt_hash;
    if (typeof claimed !== 'string' || claimed !== await sha256Uri(body)) return false;
    return true;
  }

  async function stageKvOnboarding({ operation, accountRefSha256, identityAssertion, kvRef = null, deviceRef = null, priorTransitionReceiptHash = null }) {
    const cfg = config();
    if (cfg.mode !== 'REMOTE_INTR' || !cfg.kvOnboardingEndpoint) {
      return { ok: false, state: 'KV_ONBOARDING_NOT_PROVISIONED', receipt: null, blind_retry_allowed: false };
    }
    if (!identityAssertion || identityAssertion.schema !== ASSERTION_SCHEMA || identityAssertion.credential_disclosed !== false || identityAssertion.raw_secret_present !== false) {
      return { ok: false, state: 'INVALID_IDENTITY_ASSERTION', receipt: null, blind_retry_allowed: false };
    }
    if (identityAssertion.expires_at && Date.parse(identityAssertion.expires_at) <= Date.now()) {
      return { ok: false, state: 'IDENTITY_ASSERTION_EXPIRED', receipt: null, blind_retry_allowed: false };
    }
    const request = {
      schema: KV_ONBOARDING_REQUEST_SCHEMA,
      request_id: randomId('kv-onboarding'),
      operation: String(operation),
      transport_protocol: 'InTr',
      account_ref_sha256: String(accountRefSha256),
      identity_assertion_id: String(identityAssertion.assertion_id),
      identity_assertion_hash: await sha256Uri(identityAssertion),
      kv_ref: kvRef === null ? null : String(kvRef),
      device_ref: deviceRef === null ? null : String(deviceRef),
      prior_transition_receipt_hash: priorTransitionReceiptHash === null ? null : String(priorTransitionReceiptHash),
      secret_plaintext_present: false,
      credential_material_recorded: false,
      authority_effect: 'REQUEST_ONLY',
    };
    let response;
    try {
      response = await fetch(cfg.kvOnboardingEndpoint, {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        credentials: 'omit',
        redirect: 'error',
        referrerPolicy: 'no-referrer',
        cache: 'no-store',
        body: JSON.stringify(request),
      });
    } catch (_) {
      return {
        ok: false,
        state: 'VERIFY_EXTERNALLY',
        receipt: null,
        request_id: request.request_id,
        blind_retry_allowed: false,
      };
    }
    if (response.status !== 202) {
      return {
        ok: false,
        state: response.status === 409 ? 'REPLAY_OR_ALREADY_STAGED' : 'KV_ONBOARDING_REJECTED',
        receipt: null,
        request_id: request.request_id,
        blind_retry_allowed: false,
      };
    }
    const receipt = await response.json();
    if (!await validateStageReceipt(receipt, request)) {
      return { ok: false, state: 'INVALID_KV_ONBOARDING_STAGE_RECEIPT', receipt: null, request_id: request.request_id, blind_retry_allowed: false };
    }
    return {
      ok: true,
      state: 'STAGED_FOR_CANONICAL_KV_AUTHORITY',
      receipt,
      request_id: request.request_id,
      ownership_established: false,
      blind_retry_allowed: false,
    };
  }

  // Test-only verifier. It implements the same assertion contract as the remote
  // verifier but has no production authority and never returns stored credentials.
  async function testAuthenticate(username, password) {
    const account = loadLocalAccounts()[String(username).trim()];
    if (!account || typeof account.passwordDigest !== 'string') {
      return { ok: false, state: 'LOGIN_DENIED', assertion: null };
    }
    const candidate = await sha256(password);
    if (candidate !== account.passwordDigest) {
      return { ok: false, state: 'LOGIN_DENIED', assertion: null };
    }
    return {
      ok: true,
      state: 'LOGIN_ALLOWED',
      assertion: boundedAssertion({
        subject: String(username).trim(),
        audience: 'stegverse-kv-ui',
        level: 'TEST_ACCOUNT',
        source: 'TEST_ONLY_LOCAL_INTR_VERIFIER',
      }),
    };
  }

  async function testStepUp(subject, verifier) {
    if (typeof verifier !== 'function') return { ok: false, state: 'SKAP_STEP_UP_DENIED', assertion: null };
    const verified = await verifier();
    if (verified !== true) return { ok: false, state: 'SKAP_STEP_UP_DENIED', assertion: null };
    return {
      ok: true,
      state: 'SKAP_STEP_UP_ALLOWED',
      assertion: boundedAssertion({
        subject,
        audience: 'stegverse-skap-ui',
        level: 'TEST_STEP_UP',
        source: 'TEST_ONLY_LOCAL_STEP_UP_VERIFIER',
        schema: STEP_UP_SCHEMA,
      }),
    };
  }

  window.StegVerseInTrAuth = Object.freeze({
    assertionSchema: ASSERTION_SCHEMA,
    stepUpSchema: STEP_UP_SCHEMA,
    kvOnboardingRequestSchema: KV_ONBOARDING_REQUEST_SCHEMA,
    kvOnboardingStageReceiptSchema: KV_ONBOARDING_STAGE_RECEIPT_SCHEMA,
    config,
    authenticate: remoteAuthenticate,
    stepUp: remoteStepUp,
    stageKvOnboarding,
    validateKvOnboardingStageReceipt: validateStageReceipt,
    testAuthenticate,
    testStepUp,
  });
})();
