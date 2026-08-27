(() => {
  'use strict';

  const REQUEST_SCHEMA = 'kv.interlock.request.v1';
  const RESPONSE_SCHEMA = 'kv.interlock.response.v1';
  const ALLOW = 'ALLOW_BOUNDED_CONTEXT';
  const ONBOARDING_CLASS = 'KV_ONBOARDING_STATE';
  const ONBOARDING_SCOPE = Object.freeze([
    'lifecycle_state',
    'kv_ref',
    'owner_identity_ref',
    'device_ref',
    'transition_receipt_refs',
  ]);
  const LIFECYCLE_STATES = new Set([
    'NO_KV',
    'KV_CREATED',
    'OWNER_BOUND',
    'DEVICE_REGISTERED',
    'INSTALLATION_ADMITTED',
    'KV_ACTIVE',
  ]);
  const CANDIDATE_TYPES = Object.freeze({
    CREATE: 'KV_CREATE_REQUEST',
    ATTACH: 'KV_ATTACH_REQUEST',
    OWNER_BIND: 'KV_OWNER_BIND_REQUEST',
    DEVICE_REGISTER: 'KV_DEVICE_REGISTER_REQUEST',
    INSTALL_ADMISSION: 'KV_INSTALL_ADMISSION_REQUEST',
    ACTIVATE: 'KV_ACTIVATION_REQUEST',
  });
  const TOP_LEVEL_KEYS = new Set([
    'schema_version', 'request_id', 'decision', 'granted_scope',
    'context', 'source_refs', 'receipt',
  ]);
  const RECEIPT_KEYS = new Set([
    'receipt_id', 'policy_profile', 'authority_ref', 'requested_scope',
    'granted_scope', 'source_refs', 'redaction_profile', 'decision',
    'timestamp', 'response_hash', 'writeback_candidate_ref',
  ]);
  const FORBIDDEN_CONTEXT_KEYS = new Set([
    'password', 'password_digest', 'secret', 'credential', 'credential_value',
    'token', 'private_key', 'private_key_material', 'raw_secret',
  ]);

  function nowIso() { return new Date().toISOString(); }
  function randomId(prefix) {
    const bytes = new Uint8Array(16);
    crypto.getRandomValues(bytes);
    return `${prefix}-${Array.from(bytes, b => b.toString(16).padStart(2, '0')).join('')}`;
  }
  function uniqueStrings(value) {
    return Array.isArray(value) && value.every(v => typeof v === 'string' && v.length > 0) && new Set(value).size === value.length;
  }
  function sameSet(a, b) {
    return uniqueStrings(a) && uniqueStrings(b) && a.length === b.length && a.every(v => b.includes(v));
  }
  function onlyKeys(obj, allowed) {
    return obj && typeof obj === 'object' && !Array.isArray(obj) && Object.keys(obj).every(k => allowed.has(k));
  }
  function config() {
    const explicit = window.__STEGVERSE_KV_INTR_CONFIG__ || {};
    return Object.freeze({
      mode: explicit.mode === 'REMOTE_INTR' ? 'REMOTE_INTR' : 'NOT_PROVISIONED',
      endpoint: typeof explicit.endpoint === 'string' ? explicit.endpoint : '',
      requesterModule: typeof explicit.requesterModule === 'string' && explicit.requesterModule ? explicit.requesterModule : 'Site',
      requesterComponent: typeof explicit.requesterComponent === 'string' && explicit.requesterComponent ? explicit.requesterComponent : 'generic-login-test',
    });
  }
  function assertionAuthority(assertion) {
    if (!assertion || typeof assertion !== 'object') return null;
    if (typeof assertion.assertion_id !== 'string' || !assertion.assertion_id) return null;
    if (assertion.credential_disclosed !== false || assertion.raw_secret_present !== false) return null;
    if (assertion.expires_at && Date.parse(assertion.expires_at) <= Date.now()) return null;
    return assertion.assertion_id;
  }
  function buildRequest({ operation, authorityRef, purpose, recordClass, requestedScope, justification, disclosureMode, candidateWriteback = undefined }) {
    const cfg = config();
    const request = {
      schema_version: REQUEST_SCHEMA,
      operation,
      request_id: randomId('kv-interlock'),
      requester: { module: cfg.requesterModule, component: cfg.requesterComponent },
      purpose,
      record_class: recordClass,
      requested_scope: [...requestedScope],
      minimum_necessary_justification: justification,
      authority_ref: authorityRef,
      disclosure_mode: disclosureMode,
    };
    if (candidateWriteback) request.candidate_writeback = candidateWriteback;
    return request;
  }
  function validateResponse(request, payload) {
    if (!onlyKeys(payload, TOP_LEVEL_KEYS)) return { ok:false, state:'INVALID_KV_INTERLOCK_RESPONSE' };
    if (payload.schema_version !== RESPONSE_SCHEMA || payload.request_id !== request.request_id) return { ok:false, state:'INVALID_KV_INTERLOCK_RESPONSE' };
    if (!['ALLOW_BOUNDED_CONTEXT','REVIEW_REQUIRED','DENY','FAIL_CLOSED'].includes(payload.decision)) return { ok:false, state:'INVALID_KV_INTERLOCK_RESPONSE' };
    if (!uniqueStrings(payload.granted_scope) || !uniqueStrings(payload.source_refs)) return { ok:false, state:'INVALID_KV_INTERLOCK_RESPONSE' };
    if (!payload.granted_scope.every(scope => request.requested_scope.includes(scope))) return { ok:false, state:'SCOPE_EXPANSION_REJECTED' };
    if (!payload.context || typeof payload.context !== 'object' || Array.isArray(payload.context)) return { ok:false, state:'INVALID_KV_INTERLOCK_RESPONSE' };
    if (!Object.keys(payload.context).every(key => payload.granted_scope.includes(key))) return { ok:false, state:'UNGRANTED_CONTEXT_REJECTED' };
    if (Object.keys(payload.context).some(key => FORBIDDEN_CONTEXT_KEYS.has(key.toLowerCase()))) return { ok:false, state:'SECRET_CONTEXT_REJECTED' };

    const receipt = payload.receipt;
    if (!onlyKeys(receipt, RECEIPT_KEYS)) return { ok:false, state:'INVALID_KV_INTERLOCK_RECEIPT' };
    for (const key of ['receipt_id','policy_profile','authority_ref','requested_scope','granted_scope','decision','timestamp','response_hash']) {
      if (!(key in receipt)) return { ok:false, state:'INVALID_KV_INTERLOCK_RECEIPT' };
    }
    if (receipt.authority_ref !== request.authority_ref) return { ok:false, state:'AUTHORITY_BINDING_REJECTED' };
    if (!sameSet(receipt.requested_scope, request.requested_scope)) return { ok:false, state:'REQUEST_SCOPE_BINDING_REJECTED' };
    if (!sameSet(receipt.granted_scope, payload.granted_scope)) return { ok:false, state:'GRANTED_SCOPE_BINDING_REJECTED' };
    if (receipt.decision !== payload.decision) return { ok:false, state:'DECISION_BINDING_REJECTED' };
    if (!/^[a-f0-9]{64}$/.test(String(receipt.response_hash || ''))) return { ok:false, state:'RESPONSE_HASH_REJECTED' };
    if ('source_refs' in receipt && !sameSet(receipt.source_refs, payload.source_refs)) return { ok:false, state:'SOURCE_REF_BINDING_REJECTED' };

    if (payload.decision !== ALLOW) return { ok:false, state:payload.decision, response:payload };
    return { ok:true, state:ALLOW, response:payload };
  }
  async function send(request) {
    const cfg = config();
    if (cfg.mode !== 'REMOTE_INTR' || !cfg.endpoint) return { ok:false, state:'KV_INTR_NOT_PROVISIONED', request:null, response:null };
    let response;
    try {
      response = await fetch(cfg.endpoint, {
        method:'POST',
        headers:{'content-type':'application/json'},
        credentials:'omit',
        cache:'no-store',
        redirect:'error',
        referrerPolicy:'no-referrer',
        body:JSON.stringify(request),
      });
    } catch (_) {
      return { ok:false, state:'VERIFY_EXTERNALLY', blind_retry_allowed:false, request, response:null };
    }
    if (!response.ok) return { ok:false, state:'KV_INTR_UNAVAILABLE', request, response:null };
    let payload;
    try { payload = await response.json(); }
    catch (_) { return { ok:false, state:'INVALID_KV_INTERLOCK_RESPONSE', request, response:null }; }
    return { ...validateResponse(request, payload), request };
  }
  async function requestOnboardingState(assertion) {
    const authorityRef = assertionAuthority(assertion);
    if (!authorityRef) return { ok:false, state:'INVALID_IDENTITY_ASSERTION', canonical_state:null };
    const request = buildRequest({
      operation:'REQUEST',
      authorityRef,
      purpose:'Read the minimum current KnowledgeVault onboarding state for the authenticated owner.',
      recordClass:ONBOARDING_CLASS,
      requestedScope:ONBOARDING_SCOPE,
      justification:'The Site onboarding UI needs only lifecycle and opaque ownership/device references required to render the next permitted action.',
      disclosureMode:'BOUNDED_CONTEXT',
    });
    const result = await send(request);
    if (!result.ok) return { ...result, canonical_state:null };
    const context = result.response.context;
    const state = context.lifecycle_state;
    if (!LIFECYCLE_STATES.has(state)) return { ok:false, state:'INVALID_KV_LIFECYCLE_STATE', canonical_state:null, request, response:result.response };
    if (state !== 'NO_KV' && result.response.source_refs.length === 0) return { ok:false, state:'MISSING_KV_SOURCE_RECEIPT', canonical_state:null, request, response:result.response };
    return {
      ...result,
      canonical_state:state,
      kv_ref:typeof context.kv_ref === 'string' ? context.kv_ref : null,
      owner_identity_ref:typeof context.owner_identity_ref === 'string' ? context.owner_identity_ref : null,
      device_ref:typeof context.device_ref === 'string' ? context.device_ref : null,
      transition_receipt_refs:Array.isArray(context.transition_receipt_refs) ? [...context.transition_receipt_refs] : [],
      authority_effect:'NONE',
    };
  }
  async function proposeOnboardingTransition(action, assertion, options = {}) {
    const authorityRef = assertionAuthority(assertion);
    if (!authorityRef) return { ok:false, state:'INVALID_IDENTITY_ASSERTION', candidate_only:true };
    const candidateType = CANDIDATE_TYPES[action];
    if (!candidateType) return { ok:false, state:'UNSUPPORTED_KV_TRANSITION', candidate_only:true };
    const payloadRef = typeof options.payload_ref === 'string' && options.payload_ref
      ? options.payload_ref
      : `urn:stegverse:site-kv-intent:${action.toLowerCase()}:${randomId('candidate')}`;
    const request = buildRequest({
      operation:'COMMIT_CANDIDATE',
      authorityRef,
      purpose:`Propose KnowledgeVault onboarding transition ${action}; proposal has no write authority.`,
      recordClass:ONBOARDING_CLASS,
      requestedScope:ONBOARDING_SCOPE,
      justification:'The Site may propose only the minimum onboarding transition required by the owner action; governed KV authority must separately accept and persist it.',
      disclosureMode:'SOURCE_REFERENCE_ONLY',
      candidateWriteback:{
        candidate_type:candidateType,
        payload_ref:payloadRef,
        requested_destination:null,
      },
    });
    const result = await send(request);
    if (!result.ok) return { ...result, candidate_only:true, canonical_state_changed:false };
    return {
      ...result,
      state:'CANDIDATE_ACCEPTED_FOR_REVIEW',
      candidate_only:true,
      canonical_state_changed:false,
      writeback_candidate_ref:result.response.receipt.writeback_candidate_ref || null,
      authority_effect:'NONE',
    };
  }

  window.StegVerseKVInTr = Object.freeze({
    requestSchema:REQUEST_SCHEMA,
    responseSchema:RESPONSE_SCHEMA,
    config,
    validateResponse,
    requestOnboardingState,
    proposeOnboardingTransition,
    candidateTypes:CANDIDATE_TYPES,
  });
})();
