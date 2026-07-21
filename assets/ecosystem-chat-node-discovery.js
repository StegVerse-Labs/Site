(() => {
  'use strict';

  const CONFIG_PATH = 'data/ecosystem-chat-gateway.json';
  const nativeFetch = window.fetch.bind(window);

  function canonical(value) {
    if (Array.isArray(value)) return `[${value.map(canonical).join(',')}]`;
    if (value && typeof value === 'object') {
      return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonical(value[key])}`).join(',')}}`;
    }
    return JSON.stringify(value);
  }

  async function sha256Hex(value) {
    const bytes = new TextEncoder().encode(canonical(value));
    const digest = await crypto.subtle.digest('SHA-256', bytes);
    return Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, '0')).join('');
  }

  function isGatewayConfigRequest(input) {
    const url = typeof input === 'string' ? input : input?.url;
    if (!url) return false;
    try {
      return new URL(url, window.location.href).pathname.endsWith(`/${CONFIG_PATH}`);
    } catch (_) {
      return String(url).endsWith(CONFIG_PATH);
    }
  }

  function validHttpsEndpoint(value, suffix) {
    if (typeof value !== 'string') return false;
    try {
      const url = new URL(value);
      return url.protocol === 'https:' && url.pathname.endsWith(suffix);
    } catch (_) {
      return false;
    }
  }

  async function resolveAdvertisement(config) {
    const discovery = config.discovery || {};
    if (discovery.enabled !== true || !Array.isArray(discovery.advertisement_endpoints)) return config;

    const timeoutMs = Number(discovery.timeout_ms || 4000);
    for (const endpoint of discovery.advertisement_endpoints) {
      if (!validHttpsEndpoint(endpoint, '/api/stegverse-node')) continue;
      const controller = new AbortController();
      const timeout = window.setTimeout(() => controller.abort(), timeoutMs);
      try {
        const response = await nativeFetch(endpoint, { cache: 'no-store', signal: controller.signal });
        if (!response.ok) continue;
        const advertisement = await response.json();
        if (advertisement.schema !== 'stegverse.node.endpoint-advertisement.v1') continue;
        if (advertisement.node_id !== discovery.required_node_id) continue;
        if (advertisement.capability_id !== 'ecosystem-chat-gateway') continue;
        if (advertisement.health_bound !== true) continue;
        if (advertisement.authority_granted !== false || advertisement.publication_authority !== false || advertisement.execution_authority !== false) continue;
        if (!validHttpsEndpoint(advertisement.endpoint, '/api/ecosystem-chat')) continue;
        if (!validHttpsEndpoint(advertisement.health_endpoint, '/health')) continue;

        const claimed = advertisement.advertisement_sha256;
        const binding = { ...advertisement };
        delete binding.advertisement_sha256;
        if (typeof claimed !== 'string' || claimed !== await sha256Hex(binding)) continue;

        return {
          ...config,
          endpoint: advertisement.endpoint,
          health_endpoint: advertisement.health_endpoint,
          resolved_node_id: advertisement.node_id,
          resolved_advertisement_sha256: claimed,
          endpoint_resolution: 'HEALTH_BOUND_NODE_ADVERTISEMENT'
        };
      } catch (_) {
        // Discovery is fail-closed. The existing static endpoint and local classifier remain available.
      } finally {
        window.clearTimeout(timeout);
      }
    }
    return { ...config, endpoint_resolution: 'STATIC_CONFIG_FALLBACK' };
  }

  window.fetch = async function governedNodeDiscoveryFetch(input, init) {
    const response = await nativeFetch(input, init);
    if (!isGatewayConfigRequest(input) || !response.ok) return response;
    try {
      const config = await response.clone().json();
      const resolved = await resolveAdvertisement(config);
      return new Response(JSON.stringify(resolved), {
        status: response.status,
        statusText: response.statusText,
        headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' }
      });
    } catch (_) {
      return response;
    }
  };

  window.StegVerseNodeDiscovery = {
    contract_version: '1.0.0',
    authority_granted: false,
    publication_authority: false,
    resolveAdvertisement
  };
})();
