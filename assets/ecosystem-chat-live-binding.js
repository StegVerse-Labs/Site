(() => {
  'use strict';

  const ADVERTISEMENT_PATH = '/api/stegverse-node';
  const STORAGE_KEY = 'stegverse_ecosystem_gateway_base_url';
  const ORIGIN_MANIFEST_ID = 'StegVerse-Labs/Site:ecosystem-chat.html';
  const LOOPBACK_CANDIDATES = ['http://127.0.0.1:8000', 'http://localhost:8000'];
  let discoveredNode = null;

  function uniqueId(prefix) {
    const value = globalThis.crypto && typeof globalThis.crypto.randomUUID === 'function'
      ? globalThis.crypto.randomUUID()
      : `${Date.now()}-${Math.random().toString(16).slice(2)}`;
    return `${prefix}-${value}`;
  }

  function buildTransitionIdentity() {
    return {
      transition_id: uniqueId('site-transition'),
      run_id: uniqueId('site-run'),
      event_id: uniqueId('site-event'),
      origin_manifest_id: ORIGIN_MANIFEST_ID,
      parent_transition_id: null,
      previous_receipt_id: null
    };
  }

  function normalizeBaseUrl(value) {
    if (!value) return '';
    try {
      const url = new URL(String(value), globalThis.location.href);
      if (!['http:', 'https:'].includes(url.protocol)) return '';
      return url.href.replace(/\/$/, '');
    } catch (_) {
      return '';
    }
  }

  function configuredCandidates() {
    const query = new URLSearchParams(globalThis.location.search).get('gateway');
    const injected = globalThis.STEGVERSE_ECOSYSTEM_GATEWAY_URL;
    const stored = globalThis.localStorage.getItem(STORAGE_KEY);
    const sameOrigin = ['http:', 'https:'].includes(globalThis.location.protocol)
      ? globalThis.location.origin
      : '';
    const candidates = [query, injected, stored, sameOrigin, ...LOOPBACK_CANDIDATES]
      .map(normalizeBaseUrl)
      .filter(Boolean);
    if (query) {
      const normalized = normalizeBaseUrl(query);
      if (normalized) globalThis.localStorage.setItem(STORAGE_KEY, normalized);
    }
    return [...new Set(candidates)];
  }

  function canonicalAdvertisement(payload) {
    const material = { ...payload };
    delete material.advertisement_sha256;
    const ordered = {};
    Object.keys(material).sort().forEach((key) => { ordered[key] = material[key]; });
    return JSON.stringify(ordered);
  }

  async function sha256Hex(value) {
    const encoded = new TextEncoder().encode(value);
    const digest = await globalThis.crypto.subtle.digest('SHA-256', encoded);
    return Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, '0')).join('');
  }

  async function validateAdvertisement(payload, candidate) {
    if (!payload || payload.schema !== 'stegverse.node.endpoint-advertisement.v1') return false;
    if (payload.capability_id !== 'ecosystem-chat-gateway') return false;
    if (payload.health_bound !== true) return false;
    if (payload.authority_granted !== false || payload.publication_authority !== false) return false;
    if (payload.execution_authority !== false) return false;
    if (typeof payload.endpoint !== 'string' || !payload.endpoint.startsWith(candidate)) return false;
    if (typeof payload.health_endpoint !== 'string' || !payload.health_endpoint.startsWith(candidate)) return false;
    if (!/^[a-f0-9]{64}$/.test(payload.advertisement_sha256 || '')) return false;
    return (await sha256Hex(canonicalAdvertisement(payload))) === payload.advertisement_sha256;
  }

  async function fetchWithTimeout(url, options = {}, timeoutMs = 2500) {
    const controller = new AbortController();
    const timer = globalThis.setTimeout(() => controller.abort(), timeoutMs);
    try {
      return await fetch(url, { ...options, signal: controller.signal });
    } finally {
      globalThis.clearTimeout(timer);
    }
  }

  async function discoverStegVerseNode() {
    if (discoveredNode) return discoveredNode;
    for (const candidate of configuredCandidates()) {
      try {
        const advertisementResponse = await fetchWithTimeout(`${candidate}${ADVERTISEMENT_PATH}`, {
          method: 'GET', cache: 'no-store', mode: 'cors', headers: { Accept: 'application/json' }
        });
        if (!advertisementResponse.ok) continue;
        const advertisement = await advertisementResponse.json();
        if (!(await validateAdvertisement(advertisement, candidate))) continue;
        const healthResponse = await fetchWithTimeout(advertisement.health_endpoint, {
          method: 'GET', cache: 'no-store', mode: 'cors', headers: { Accept: 'application/json' }
        });
        if (!healthResponse.ok) continue;
        const health = await healthResponse.json().catch(() => ({}));
        if (health.status !== 'ok') continue;
        discoveredNode = Object.freeze({ base_url: candidate, advertisement, health });
        return discoveredNode;
      } catch (_) {
        // Missing, unreachable, or invalid candidates are normal fail-closed conditions.
      }
    }
    return null;
  }

  async function sendGovernedGatewayRequest(message, posture, node) {
    const sessionId = getSessionId();
    const transitionIdentity = buildTransitionIdentity();
    const response = await fetchWithTimeout(node.advertisement.endpoint, {
      method: 'POST',
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
        'X-SteGVerse-Session': sessionId
      },
      body: JSON.stringify({
        message,
        session_id: sessionId,
        requested_route: posture.route,
        transition_intent: posture.intent.id,
        transition_destination: posture.intent.destination,
        goal: 'governed Ecosystem Chat request response provider usage custody and reconstruction',
        execution_model: 'allowlisted_task_request_only',
        raw_shell_allowed: false,
        authority_required: true,
        rate_limit_required: true,
        receipt_required_for_execution: true,
        interaction_profile: posture.interaction_profile,
        interaction_bands: INTERACTION_BANDS.map((band) => band.key),
        math_solver_supported: true,
        transition_identity: transitionIdentity
      })
    }, 15000);

    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
      const reason = data && data.detail ? JSON.stringify(data.detail) : `http_${response.status}`;
      throw new Error(reason);
    }

    const interactionProfile = normalizeInteractionProfile(data.interaction_profile || posture.interaction_profile);
    const provider = data.provider || {};
    const localUsage = data.provider_usage_submission || {};
    const custody = data.master_records_usage_submission || {};
    const authority = data.authority || {};
    const receiptParts = [
      `node_id=${node.advertisement.node_id}`,
      `node_advertisement_sha256=${node.advertisement.advertisement_sha256}`,
      `receipt_id=${data.receipt_id || 'not-issued'}`,
      `final_receipt_id=${data.final_receipt_id || 'pending'}`,
      `transition_id=${data.transition_id || transitionIdentity.transition_id}`,
      `run_id=${data.run_id || transitionIdentity.run_id}`,
      `lifecycle=${data.lifecycle_state || 'unknown'}`,
      `provider_used=${provider.used === true}`,
      `local_usage_persisted=${Boolean(localUsage.status || localUsage.record_id || localUsage.usage_event_id)}`,
      `usage_custody_recorded=${custody.custody_recorded === true}`,
      `usage_reconstructability=${custody.reconstructability || 'PENDING'}`,
      `transition_custody=${data.master_record_status || 'PENDING'}`,
      `transition_reconstruction=${data.reconstruction_status || 'PENDING'}`,
      `authority_granted=${authority.provider_usage_grants_authority === true ? 'true' : 'false'}`,
      'source=llm-adapter',
      'shell=disabled'
    ];

    return {
      response: data.response || 'The governed StegVerse node returned no response text.',
      receipt_line: receiptParts.join(' · '),
      interaction_profile: interactionProfile,
      intent: posture.intent,
      route: data.routed_module || posture.route,
      transition_identity: {
        transition_id: data.transition_id || transitionIdentity.transition_id,
        run_id: data.run_id || transitionIdentity.run_id,
        event_id: data.event_id || transitionIdentity.event_id,
        origin_manifest_id: data.origin_manifest_id || transitionIdentity.origin_manifest_id
      },
      governed_transition: data.transition_candidate || null,
      source: 'llm-adapter'
    };
  }

  routeEcosystemRequest = async function routeEcosystemRequestLive(message) {
    const posture = classifyRequestPosture(message);
    if (posture.restricted) {
      return localRouteResult(message, 'Restricted request detected; no public execution occurred and separate authority review is required.', posture);
    }
    try {
      const node = await discoverStegVerseNode();
      if (!node) throw new Error('verified_stegverse_node_not_found');
      return await sendGovernedGatewayRequest(message, posture, node);
    } catch (error) {
      discoveredNode = null;
      const reason = error instanceof Error ? error.message : 'unknown_gateway_error';
      return localRouteResult(message, `Verified StegVerse node unavailable or rejected the request (${reason}); fail-closed to local classification.`, posture);
    }
  };

  globalThis.STEGVERSE_ECOSYSTEM_CHAT_LIVE_BINDING = Object.freeze({
    discovery: 'verified_provider_neutral_stegverse_node',
    candidate_base_urls: configuredCandidates(),
    advertisement_path: ADVERTISEMENT_PATH,
    configuration_sources: ['query:gateway', 'window.STEGVERSE_ECOSYSTEM_GATEWAY_URL', 'localStorage', 'same-origin', 'loopback'],
    external_host_dependency: false,
    hosting_provider_required: false,
    live_gateway_enabled: true,
    restricted_requests_execute: false,
    local_fallback_enabled: true,
    provider_output_is_authority: false,
    repository_mutation_authority: false
  });
})();
