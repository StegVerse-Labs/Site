const ALLOWED = Object.freeze({
  '/api/stegwallet/siwe/health': 'GET',
  '/api/stegwallet/siwe/challenge': 'POST',
  '/api/stegwallet/siwe/verify': 'POST',
  '/api/stegwallet/siwe/session': 'GET',
  '/api/stegwallet/siwe/logout': 'POST',
});

function json(status, payload) {
  return new Response(`${JSON.stringify(payload)}\n`, {
    status,
    headers: {
      'content-type': 'application/json; charset=utf-8',
      'cache-control': 'no-store',
      'x-content-type-options': 'nosniff',
    },
  });
}

function validateEnvironment(env) {
  const upstream = new URL(env.SIWE_UPSTREAM_ORIGIN || '');
  if (upstream.protocol !== 'https:' || !upstream.hostname || upstream.pathname !== '/') {
    throw new Error('CONFIGURATION_REQUIRED:SIWE_UPSTREAM_ORIGIN');
  }
  if (upstream.hostname === 'stegverse.org') {
    throw new Error('FAIL_CLOSED:recursive_upstream_prohibited');
  }
  if (typeof env.SIWE_EDGE_TOKEN !== 'string' || env.SIWE_EDGE_TOKEN.length < 32) {
    throw new Error('CONFIGURATION_REQUIRED:SIWE_EDGE_TOKEN');
  }
  return upstream;
}

export default {
  async fetch(request, env) {
    try {
      const incoming = new URL(request.url);
      if (incoming.protocol !== 'https:' || incoming.hostname !== 'stegverse.org') {
        return json(403, {status: 'FAIL_CLOSED', error: 'canonical_origin_required', transaction_authority: false});
      }
      if (incoming.search || incoming.hash) {
        return json(400, {status: 'FAIL_CLOSED', error: 'query_or_fragment_prohibited', transaction_authority: false});
      }
      const requiredMethod = ALLOWED[incoming.pathname];
      if (!requiredMethod) {
        return json(404, {status: 'NOT_FOUND', transaction_authority: false});
      }
      if (request.method.toUpperCase() !== requiredMethod) {
        return json(405, {status: 'FAIL_CLOSED', error: 'method_not_allowed', transaction_authority: false});
      }

      const upstream = validateEnvironment(env);
      upstream.pathname = incoming.pathname;
      const headers = new Headers(request.headers);
      headers.delete('x-stegwallet-edge-token');
      headers.set('x-stegwallet-edge-token', env.SIWE_EDGE_TOKEN);
      headers.set('x-forwarded-host', incoming.host);
      headers.set('x-forwarded-proto', 'https');
      const clientIp = request.headers.get('cf-connecting-ip');
      if (clientIp) headers.set('x-forwarded-for', clientIp);
      else headers.delete('x-forwarded-for');

      const init = {
        method: request.method,
        headers,
        redirect: 'manual',
      };
      if (!['GET', 'HEAD'].includes(request.method.toUpperCase())) init.body = request.body;

      const response = await fetch(upstream.toString(), init);
      const responseHeaders = new Headers(response.headers);
      responseHeaders.set('cache-control', 'no-store');
      responseHeaders.set('x-content-type-options', 'nosniff');
      responseHeaders.set('x-stegwallet-edge', 'stegwallet-siwe-v1');
      return new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers: responseHeaders,
      });
    } catch (error) {
      return json(503, {
        status: 'CONFIGURATION_REQUIRED',
        error: String(error?.message || 'edge_proxy_unavailable'),
        wallet_authenticated: false,
        transaction_authority: false,
        execution_authority: false,
        delegation_authority: false,
        custody_recorded: false,
      });
    }
  },
};
