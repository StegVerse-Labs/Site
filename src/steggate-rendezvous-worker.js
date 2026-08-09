const REGISTRY_URL = 'https://api.github.com/repos/StegVerse-Labs/StegCore/issues/comments/5228464425';
const REGISTRY_STATE = 'State: `LIVE_ACCEPTANCE_PASS`';
const ORIGIN_PATTERN = /Current public origin: `(https:\/\/[-a-z0-9.]+)`/i;
const ALLOWED_PATHS = new Set([
  '/health',
  '/v1/capabilities',
  '/v1/self-test',
  '/v1/evaluate'
]);

function json(body, status = 200) {
  return new Response(JSON.stringify(body, null, 2), {
    status,
    headers: {
      'content-type': 'application/json; charset=utf-8',
      'cache-control': 'no-store'
    }
  });
}

async function fetchWithTimeout(url, init = {}, timeoutMs = 8000) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort('timeout'), timeoutMs);
  try {
    return await fetch(url, { ...init, signal: controller.signal });
  } finally {
    clearTimeout(timer);
  }
}

async function resolveNode() {
  let registry;
  try {
    const response = await fetchWithTimeout(REGISTRY_URL, {
      headers: {
        'accept': 'application/vnd.github+json',
        'user-agent': 'StegVerse-Steggate-Rendezvous/1'
      }
    });
    if (!response.ok) throw new Error(`registry_http_${response.status}`);
    registry = await response.json();
  } catch (error) {
    return { state: 'FAIL_CLOSED', reason: 'registry_unavailable', detail: String(error) };
  }

  const body = String(registry?.body || '');
  if (!body.includes(REGISTRY_STATE)) {
    return { state: 'FAIL_CLOSED', reason: 'registry_not_live' };
  }
  const match = body.match(ORIGIN_PATTERN);
  if (!match) {
    return { state: 'FAIL_CLOSED', reason: 'registry_origin_missing' };
  }

  const origin = match[1].replace(/\/$/, '');
  try {
    const healthResponse = await fetchWithTimeout(`${origin}/health`, {
      headers: { 'accept': 'application/json' }
    });
    if (!healthResponse.ok) {
      return { state: 'FAIL_CLOSED', reason: 'node_health_http', origin, http_status: healthResponse.status };
    }
    const health = await healthResponse.json();
    if (health?.healthy !== true || health?.canonical_three_layer_bound !== true) {
      return { state: 'FAIL_CLOSED', reason: 'node_not_canonically_healthy', origin, health };
    }
    return {
      state: 'LIVE',
      origin,
      health,
      registry_comment_id: registry.id,
      registry_updated_at: registry.updated_at || null
    };
  } catch (error) {
    return { state: 'FAIL_CLOSED', reason: 'node_health_unreachable', origin, detail: String(error) };
  }
}

function upstreamPath(url) {
  const prefix = '/api/steggate';
  const path = url.pathname.slice(prefix.length) || '/';
  return ALLOWED_PATHS.has(path) ? path : null;
}

async function proxy(request) {
  const url = new URL(request.url);
  const path = upstreamPath(url);
  if (!path) return json({ state: 'FAIL_CLOSED', detail: 'unsupported_steggate_route' }, 404);
  if (path === '/v1/evaluate' && request.method !== 'POST') {
    return json({ state: 'FAIL_CLOSED', detail: 'method_not_allowed' }, 405);
  }
  if (path !== '/v1/evaluate' && request.method !== 'GET') {
    return json({ state: 'FAIL_CLOSED', detail: 'method_not_allowed' }, 405);
  }

  const resolved = await resolveNode();
  if (resolved.state !== 'LIVE') {
    return json({
      schema_version: 'STEGGATE-RENDEZVOUS-v1',
      state: 'FAIL_CLOSED',
      routing_authority: false,
      decision_authority: false,
      ...resolved
    }, 503);
  }

  const headers = new Headers();
  headers.set('accept', 'application/json');
  const contentType = request.headers.get('content-type');
  if (contentType) headers.set('content-type', contentType);

  let body;
  if (request.method === 'POST') body = await request.arrayBuffer();

  try {
    const response = await fetchWithTimeout(`${resolved.origin}${path}${url.search}`, {
      method: request.method,
      headers,
      body
    }, 15000);
    const responseBody = await response.arrayBuffer();
    const responseHeaders = new Headers(response.headers);
    responseHeaders.set('cache-control', 'no-store');
    responseHeaders.set('x-steggate-rendezvous', 'stegverse-site-v1');
    responseHeaders.set('x-steggate-node-origin', resolved.origin);
    return new Response(responseBody, {
      status: response.status,
      headers: responseHeaders
    });
  } catch (error) {
    return json({
      schema_version: 'STEGGATE-RENDEZVOUS-v1',
      state: 'FAIL_CLOSED',
      detail: 'selected_node_became_unreachable',
      node_origin: resolved.origin,
      error_class: error?.name || 'Error',
      decision_authority: false
    }, 503);
  }
}

export default {
  async fetch(request) {
    const url = new URL(request.url);
    if (url.pathname === '/api/steggate/readiness' && request.method === 'GET') {
      const resolved = await resolveNode();
      return json({
        schema_version: 'STEGGATE-RENDEZVOUS-v1',
        state: resolved.state === 'LIVE' ? 'READY' : 'FAIL_CLOSED',
        stable_route: 'https://stegverse.org/api/steggate',
        routing_authority: false,
        decision_authority: false,
        selected_node: resolved.state === 'LIVE' ? {
          origin: resolved.origin,
          canonical_three_layer_bound: true,
          registry_updated_at: resolved.registry_updated_at
        } : null,
        blocker: resolved.state === 'LIVE' ? null : resolved
      }, resolved.state === 'LIVE' ? 200 : 503);
    }
    if (url.pathname.startsWith('/api/steggate/')) return proxy(request);
    return json({ detail: 'not_found' }, 404);
  }
};
