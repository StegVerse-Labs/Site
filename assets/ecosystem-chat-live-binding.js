(() => {
  const GATEWAY_BASE_URL = 'https://stegverse-ecosystem-chat-gateway.onrender.com';
  const GATEWAY_URL = `${GATEWAY_BASE_URL}/api/ecosystem-chat`;

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
      origin_manifest_id: uniqueId('site-origin'),
      parent_transition_id: null,
      previous_receipt_id: null
    };
  }

  async function sendGovernedGatewayRequest(message, posture) {
    const sessionId = getSessionId();
    const transitionIdentity = buildTransitionIdentity();
    const response = await fetch(GATEWAY_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
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
    });

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
      `receipt_id=${data.receipt_id || 'not-issued'}`,
      `final_receipt_id=${data.final_receipt_id || 'pending'}`,
      `transition_id=${data.transition_id || transitionIdentity.transition_id}`,
      `run_id=${data.run_id || transitionIdentity.run_id}`,
      `provider_used=${provider.used === true}`,
      `local_usage_persisted=${Boolean(localUsage.status || localUsage.record_id || localUsage.usage_event_id)}`,
      `usage_custody_recorded=${custody.custody_recorded === true}`,
      `usage_reconstructability=${custody.reconstructability || 'PENDING'}`,
      `transition_custody=${data.master_record_status || 'PENDING'}`,
      `transition_reconstruction=${data.reconstruction_status || 'PENDING'}`,
      `authority_granted=${authority.provider_usage_grants_authority === true ? 'true' : 'false'}`,
      'source=governed_gateway',
      'shell=disabled'
    ];

    return {
      response: data.response || 'The governed gateway returned no response text.',
      receipt_line: receiptParts.join(' · '),
      interaction_profile: interactionProfile,
      intent: posture.intent,
      route: data.routed_module || posture.route
    };
  }

  routeEcosystemRequest = async function routeEcosystemRequestLive(message) {
    const posture = classifyRequestPosture(message);
    if (posture.restricted) {
      return localRouteResult(
        message,
        'Restricted request detected; no public execution occurred and separate authority review is required.',
        posture
      );
    }

    try {
      return await sendGovernedGatewayRequest(message, posture);
    } catch (error) {
      const reason = error instanceof Error ? error.message : 'unknown_gateway_error';
      return localRouteResult(
        message,
        `Governed gateway unavailable or rejected the request (${reason}); fail-closed to local classification.`,
        posture
      );
    }
  };

  globalThis.STEGVERSE_ECOSYSTEM_CHAT_LIVE_BINDING = Object.freeze({
    gateway_base_url: GATEWAY_BASE_URL,
    live_gateway_enabled: true,
    restricted_requests_execute: false,
    local_fallback_enabled: true,
    provider_output_is_authority: false,
    repository_mutation_authority: false
  });
})();
