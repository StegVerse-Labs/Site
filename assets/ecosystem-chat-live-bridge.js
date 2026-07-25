/* Provider-neutral live bridge for the StegVerse Ecosystem Node.
 *
 * This file intentionally loads after assets/ecosystem-chat.js and replaces only
 * the gateway transport functions. The existing local classifier remains the
 * fail-closed fallback and continues to grant no authority.
 */

const STEGVERSE_GATEWAY_STORAGE_KEY = 'stegverse_ecosystem_gateway_base_url';
const STEGVERSE_ORIGIN_MANIFEST_ID = 'StegVerse-Labs/Site:ecosystem-chat.html';

function normalizeGatewayBaseUrl(value) {
  if (!value) return '';
  try {
    const url = new URL(String(value), window.location.href);
    if (!['http:', 'https:'].includes(url.protocol)) return '';
    return url.href.replace(/\/$/, '');
  } catch (_error) {
    return '';
  }
}

function configuredGatewayBaseUrl() {
  const query = new URLSearchParams(window.location.search).get('gateway');
  const injected = window.STEGVERSE_ECOSYSTEM_GATEWAY_URL;
  const stored = window.localStorage.getItem(STEGVERSE_GATEWAY_STORAGE_KEY);
  const sameOrigin = window.location.protocol === 'http:' || window.location.protocol === 'https:'
    ? window.location.origin
    : '';
  const resolved = normalizeGatewayBaseUrl(query || injected || stored || sameOrigin);
  if (query && resolved) window.localStorage.setItem(STEGVERSE_GATEWAY_STORAGE_KEY, resolved);
  return resolved;
}

function gatewayUrl(path) {
  const base = configuredGatewayBaseUrl();
  return base ? `${base}${path}` : '';
}

function randomIdentifier(prefix) {
  const value = crypto.randomUUID ? crypto.randomUUID() : `${Date.now()}-${Math.random().toString(16).slice(2)}`;
  return `${prefix}:${value}`;
}

function buildTransitionIdentity() {
  return {
    transition_id: randomIdentifier('transition'),
    run_id: randomIdentifier('run'),
    event_id: randomIdentifier('event'),
    origin_manifest_id: STEGVERSE_ORIGIN_MANIFEST_ID,
    parent_transition_id: null,
    previous_receipt_id: null
  };
}

async function probeGateway() {
  const endpoint = gatewayUrl('/api/stegverse-node');
  if (!endpoint) return { available: false, reason: 'gateway_not_configured' };
  const response = await fetch(endpoint, {
    method: 'GET',
    headers: { 'Accept': 'application/json' },
    mode: 'cors',
    cache: 'no-store'
  });
  if (!response.ok) return { available: false, reason: `advertisement_http_${response.status}` };
  const advertisement = await response.json();
  if (!advertisement || advertisement.capability_id !== 'ecosystem-chat-gateway') {
    return { available: false, reason: 'unexpected_capability_advertisement' };
  }
  return { available: true, advertisement };
}

async function routeEcosystemRequest(message) {
  const posture = classifyRequestPosture(message);
  if (posture.restricted) {
    return localRouteResult(message, 'Restricted request detected; local gateway refuses execution and routes to authority review.', posture);
  }
  try {
    const probe = await probeGateway();
    if (!probe.available) {
      return localRouteResult(message, `LLM-adapter unavailable (${probe.reason}); fail-closed to local classification.`, posture);
    }
    return await sendGatewayRequest(message, posture, probe.advertisement);
  } catch (error) {
    const reason = error && error.message ? error.message : 'gateway_error';
    return localRouteResult(message, `LLM-adapter request failed (${reason}); fail-closed to local classification.`, posture);
  }
}

async function sendGatewayRequest(message, posture, advertisement = null) {
  const transitionIdentity = buildTransitionIdentity();
  const endpoint = advertisement && advertisement.endpoint
    ? advertisement.endpoint
    : gatewayUrl(STEGVERSE_GATEWAY_PATH);
  if (!endpoint) throw new Error('gateway_endpoint_not_configured');

  const payload = {
    message,
    session_id: getSessionId(),
    requested_route: posture.route,
    transition_intent: posture.intent.id,
    transition_destination: posture.intent.destination,
    goal: 'user advancement console with governed task boundaries',
    execution_model: 'allowlisted_task_request_only',
    raw_shell_allowed: false,
    authority_required: true,
    rate_limit_required: true,
    receipt_required_for_execution: true,
    interaction_profile: posture.interaction_profile,
    interaction_bands: INTERACTION_BANDS.map((band) => band.key),
    math_solver_supported: true,
    transition_identity: transitionIdentity
  };

  const response = await fetch(endpoint, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'X-SteGVerse-Session': payload.session_id
    },
    mode: 'cors',
    body: JSON.stringify(payload)
  });
  if (!response.ok) throw new Error(`gateway_http_${response.status}`);

  const data = await response.json();
  const returnedTransitionId = data.transition_id || transitionIdentity.transition_id;
  const returnedRunId = data.run_id || transitionIdentity.run_id;
  const receiptLine = data.receipt_id ? `receipt_id=${data.receipt_id}` : 'receipt=not-issued';
  const interactionProfile = normalizeInteractionProfile(data.interaction_profile || posture.interaction_profile);
  return {
    response: data.response || buildLocalResponse(message, data.routed_module || 'Unknown', 'Gateway returned no response body.', posture),
    receipt_line: `${receiptLine} · transition_id=${returnedTransitionId} · run_id=${returnedRunId} · lifecycle=${data.lifecycle_state || 'unknown'} · routed_module=${data.routed_module || 'Unknown'} · intent=${posture.intent.id} · source=llm-adapter · shell=disabled · authority=none · bands=${formatInteractionProfile(interactionProfile)}`,
    interaction_profile: interactionProfile,
    intent: posture.intent,
    route: data.routed_module || posture.route,
    transition_identity: {
      transition_id: returnedTransitionId,
      run_id: returnedRunId,
      event_id: data.event_id || transitionIdentity.event_id,
      origin_manifest_id: data.origin_manifest_id || transitionIdentity.origin_manifest_id
    },
    governed_transition: data.transition_candidate || null,
    source: 'llm-adapter'
  };
}

window.addEventListener('DOMContentLoaded', async () => {
  const systemReceipt = document.querySelector('#chatLog .chat-message.system .receipt-block');
  if (!systemReceipt) return;
  try {
    const probe = await probeGateway();
    if (probe.available) {
      systemReceipt.textContent = `mode=live-gateway-ready · capability=${probe.advertisement.capability_id} · node_id=${probe.advertisement.node_id} · authority=none · governance=enabled`;
    } else {
      systemReceipt.textContent = `mode=local-fallback · reason=${probe.reason} · authority=none · governance=enabled · receipt=not-issued`;
    }
  } catch (_error) {
    systemReceipt.textContent = 'mode=local-fallback · reason=gateway_probe_failed · authority=none · governance=enabled · receipt=not-issued';
  }
});
