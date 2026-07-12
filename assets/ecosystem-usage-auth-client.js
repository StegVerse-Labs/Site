(() => {
  'use strict';

  const CONTRACT_PATH = 'data/ecosystem-usage-live-contract.json';
  const SESSION_PATTERN = /^[A-Za-z0-9._:-]+$/;
  const EVIDENCE_CLASSES = new Set(['MEASURED', 'CONFIGURED', 'DERIVED', 'UNAVAILABLE']);
  const INTEGRITY_HTTP_STATUSES = new Set([400, 401, 403, 409, 422]);

  class UsageIntegrityError extends Error {
    constructor(message) {
      super(message);
      this.name = 'UsageIntegrityError';
    }
  }

  const readJson = async (url, options = {}) => {
    const response = await fetch(url, options);
    if (!response.ok) {
      if (INTEGRITY_HTTP_STATUSES.has(response.status)) {
        throw new UsageIntegrityError(`usage request rejected with HTTP ${response.status}`);
      }
      throw new Error(`usage request failed with HTTP ${response.status}`);
    }
    return response.json();
  };

  const validateSessionId = (sessionId, maxLength = 160) => {
    const value = String(sessionId || '').trim();
    if (!value || value.length > maxLength || !SESSION_PATTERN.test(value)) {
      throw new UsageIntegrityError('invalid session identity');
    }
    return value;
  };

  const validateMetric = (metric) => {
    if (!metric || typeof metric !== 'object' || !EVIDENCE_CLASSES.has(metric.evidence_class)) {
      throw new UsageIntegrityError('invalid metric evidence class');
    }
    if (metric.evidence_class === 'UNAVAILABLE' && metric.value !== null) {
      throw new UsageIntegrityError('UNAVAILABLE metric must retain null value');
    }
  };

  const validateEvent = (event, requestedSession) => {
    const required = ['session_id', 'transition_id', 'entry_point', 'metric_owner', 'measurement_id', 'metrics', 'receipt_refs'];
    if (!event || typeof event !== 'object' || required.some((field) => !(field in event))) {
      throw new UsageIntegrityError('usage event contract incomplete');
    }
    if (event.session_id !== requestedSession) {
      throw new UsageIntegrityError('usage event changed session identity');
    }
    if (!event.transition_id || !event.metric_owner || !event.measurement_id) {
      throw new UsageIntegrityError('usage event identity incomplete');
    }
    if (!event.metrics || typeof event.metrics !== 'object' || Array.isArray(event.metrics)) {
      throw new UsageIntegrityError('usage event metrics must be an object');
    }
    Object.values(event.metrics).forEach(validateMetric);
    if (!Array.isArray(event.receipt_refs)) {
      throw new UsageIntegrityError('usage event receipt_refs must be an array');
    }
  };

  const validatePayload = (payload, requestedSession, contract) => {
    if (!payload || typeof payload !== 'object') throw new UsageIntegrityError('usage response must be an object');
    if (payload.schema !== contract.response.schema) throw new UsageIntegrityError('usage response schema mismatch');
    if (payload.session_id !== requestedSession) throw new UsageIntegrityError('live usage response changed session identity');
    if (payload.source_class !== 'LIVE_USAGE_API') throw new UsageIntegrityError('live usage source class mismatch');
    if (!Array.isArray(payload.events)) throw new UsageIntegrityError('live usage events must be an array');
    if (!payload.retrieval_receipt || typeof payload.retrieval_receipt !== 'object') {
      throw new UsageIntegrityError('live usage retrieval receipt missing');
    }
    if (payload.retrieval_receipt.session_id !== requestedSession) {
      throw new UsageIntegrityError('retrieval receipt changed session identity');
    }
    if (payload.retrieval_receipt.authority_granted !== false || payload.retrieval_receipt.custody_recorded !== false) {
      throw new UsageIntegrityError('retrieval receipt exceeded Site authority');
    }
    payload.events.forEach((event) => validateEvent(event, requestedSession));
    return payload;
  };

  const resolveEndpoint = (base, routeTemplate, sessionId) => {
    const endpoint = new URL(routeTemplate.replace('{session_id}', encodeURIComponent(sessionId)), base || window.location.origin);
    const sameOrigin = endpoint.origin === window.location.origin;
    if (!sameOrigin && endpoint.protocol !== 'https:') throw new UsageIntegrityError('cross-origin usage endpoint must use HTTPS');
    return { endpoint, sameOrigin };
  };

  const retrieve = async ({ sessionId, apiBase = window.location.origin } = {}) => {
    const contract = await readJson(CONTRACT_PATH, { cache: 'no-store', credentials: 'same-origin' });
    const clean = validateSessionId(sessionId, contract.request.session_id_max_length);
    const { endpoint, sameOrigin } = resolveEndpoint(apiBase, contract.route_template, clean);
    const controller = new AbortController();
    const timer = window.setTimeout(() => controller.abort(), contract.transport.timeout_ms);
    try {
      const payload = await readJson(endpoint.href, {
        method: 'GET',
        cache: 'no-store',
        credentials: sameOrigin ? 'same-origin' : 'omit',
        headers: { Accept: 'application/json' },
        signal: controller.signal
      });
      return validatePayload(payload, clean, contract);
    } finally {
      window.clearTimeout(timer);
    }
  };

  window.StegVerseUsageAuthClient = Object.freeze({
    retrieve,
    validatePayload,
    UsageIntegrityError,
    contractPath: CONTRACT_PATH,
    authority: 'none',
    custody: 'not-recorded-by-site'
  });
})();
