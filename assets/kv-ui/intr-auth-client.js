(() => {
  'use strict';

  const ASSERTION_SCHEMA = 'stegverse.intr.identity-assertion/v1';
  const STEP_UP_SCHEMA = 'stegverse.intr.step-up-assertion/v1';
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
  function loadLocalAccounts() {
    try { return JSON.parse(localStorage.getItem(LOCAL_ACCOUNT_KEY) || '{}'); }
    catch (_) { return {}; }
  }
  function config() {
    const explicit = window.__STEGVERSE_INTR_CONFIG__ || {};
    return Object.freeze({
      mode: explicit.mode === 'REMOTE_INTR' ? 'REMOTE_INTR' : 'NOT_PROVISIONED',
      endpoint: typeof explicit.endpoint === 'string' ? explicit.endpoint : '',
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
    config,
    authenticate: remoteAuthenticate,
    stepUp: remoteStepUp,
    testAuthenticate,
    testStepUp,
  });
})();
