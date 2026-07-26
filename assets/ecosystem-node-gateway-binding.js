(() => {
  'use strict';

  const STREAM_SCHEMA = 'stegverse.canonical-event-stream.v0.1';
  const EVENT_KEYS = Object.freeze([
    'event_id','parent_event_id','timestamp','actor','event_type','human_projection',
    'governed_projection','policy_refs','evidence_refs','artifact_refs','continuity_refs','hash'
  ]);
  const EVENT_TYPES = new Set(['message','decision','execution','receipt','policy','evidence']);
  const upstreamIds = new Set();

  function stable(value) {
    if (Array.isArray(value)) return `[${value.map(stable).join(',')}]`;
    if (value && typeof value === 'object') {
      return `{${Object.keys(value).sort().map(key => `${JSON.stringify(key)}:${stable(value[key])}`).join(',')}}`;
    }
    return JSON.stringify(value);
  }

  async function sha256Hex(text) {
    const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
    return Array.from(new Uint8Array(digest), byte => byte.toString(16).padStart(2, '0')).join('');
  }

  async function expectedHash(event) {
    const material = JSON.parse(JSON.stringify(event));
    material.hash = '';
    return `sha256:${await sha256Hex(stable(material))}`;
  }

  function requireObject(value, label) {
    if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error(`${label} must be an object`);
  }

  function requireStringArray(value, label) {
    if (!Array.isArray(value) || value.some(item => typeof item !== 'string' || !item)) {
      throw new Error(`${label} must be an array of non-empty strings`);
    }
    if (new Set(value).size !== value.length) throw new Error(`${label} contains duplicate references`);
  }

  async function validateEvent(event, priorIds, pendingIds) {
    requireObject(event, 'event');
    const keys = Object.keys(event).sort();
    if (stable(keys) !== stable([...EVENT_KEYS].sort())) throw new Error('canonical event fields mismatch');
    if (typeof event.event_id !== 'string' || !event.event_id) throw new Error('event_id is required');
    if (priorIds.has(event.event_id) || pendingIds.has(event.event_id)) throw new Error(`duplicate event_id: ${event.event_id}`);
    if (event.parent_event_id !== null && (typeof event.parent_event_id !== 'string' || !priorIds.has(event.parent_event_id))) {
      throw new Error(`unresolved or forward parent_event_id: ${event.parent_event_id}`);
    }
    if (typeof event.timestamp !== 'string' || Number.isNaN(Date.parse(event.timestamp))) throw new Error('timestamp must be RFC3339-compatible');
    requireObject(event.actor, 'actor');
    requireObject(event.human_projection, 'human_projection');
    requireObject(event.governed_projection, 'governed_projection');
    if (!EVENT_TYPES.has(event.event_type)) throw new Error(`unsupported event_type: ${event.event_type}`);
    for (const field of ['policy_refs','evidence_refs','artifact_refs','continuity_refs']) requireStringArray(event[field], field);
    for (const reference of [...event.evidence_refs, ...event.continuity_refs]) {
      if (reference.startsWith('event:')) {
        const target = reference.slice(6);
        if (!priorIds.has(target)) throw new Error(`unresolved event reference: ${reference}`);
      }
    }
    if (event.governed_projection.source_class !== 'upstream_governed') {
      throw new Error('upstream event must declare governed_projection.source_class=upstream_governed');
    }
    if (event.hash !== await expectedHash(event)) throw new Error(`event hash mismatch: ${event.event_id}`);
  }

  async function validateStream(payload) {
    requireObject(payload, 'stream');
    if (payload.schema !== STREAM_SCHEMA) throw new Error('canonical stream schema mismatch');
    if (!Array.isArray(payload.events) || payload.events.length === 0) throw new Error('canonical stream events are required');
    if (payload.authority_effect !== 'NONE') throw new Error('stream authority boundary invalid');
    const priorIds = new Set(upstreamIds);
    const pendingIds = new Set();
    for (const event of payload.events) {
      await validateEvent(event, priorIds, pendingIds);
      pendingIds.add(event.event_id);
      priorIds.add(event.event_id);
    }
    return payload.events.map(event => Object.freeze(JSON.parse(JSON.stringify(event))));
  }

  async function importValidatedStream(payload) {
    const api = globalThis.StegVerseCanonicalEventStream;
    if (!api || typeof api.importCanonicalEvents !== 'function') throw new Error('canonical event renderer is unavailable');
    const events = await validateStream(payload);
    const imported = api.importCanonicalEvents(events);
    events.forEach(event => upstreamIds.add(event.event_id));
    return Object.freeze({ imported_event_ids: imported, authority_effect: 'NONE', source_class: 'upstream_governed' });
  }

  async function fetchAndImport(url, options = {}) {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), options.timeout_ms || 5000);
    try {
      const response = await fetch(url, {
        method: 'GET', cache: 'no-store', credentials: 'omit', mode: 'cors',
        headers: { Accept: 'application/json' }, signal: controller.signal
      });
      if (!response.ok) throw new Error(`gateway canonical event request failed: HTTP ${response.status}`);
      return await importValidatedStream(await response.json());
    } finally {
      clearTimeout(timeout);
    }
  }

  globalThis.StegVerseCanonicalGatewayBinding = Object.freeze({
    version: '1.0', validateStream, importValidatedStream, fetchAndImport,
    source_separation: 'preview_local_vs_upstream_governed',
    silent_repair_allowed: false, rehash_allowed: false, reorder_allowed: false,
    authority_effect: 'NONE'
  });
})();
