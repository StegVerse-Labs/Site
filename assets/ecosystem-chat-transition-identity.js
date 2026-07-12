(() => {
  'use strict';

  const CONTRACT_VERSION = '1.0.0';
  const ORIGIN_CLASS = 'SITE_INPUT';
  const SOURCE_REF = 'StegVerse-Labs/Site/ecosystem-chat.html';
  const SESSION_KEY = 'stegverse_ecosystem_chat_session';
  const COUNTER_KEY = 'stegverse_ecosystem_chat_transition_counter';
  const CONFIG_PATH = 'data/ecosystem-chat-gateway.json';

  function sessionId() {
    const existing = window.sessionStorage.getItem(SESSION_KEY);
    if (existing) return existing;
    const generated = crypto.randomUUID ? crypto.randomUUID() : `session-${Date.now()}`;
    window.sessionStorage.setItem(SESSION_KEY, generated);
    return generated;
  }

  function nextIdentity() {
    const session = sessionId();
    const next = Number(window.sessionStorage.getItem(COUNTER_KEY) || '0') + 1;
    window.sessionStorage.setItem(COUNTER_KEY, String(next));
    const suffix = String(next).padStart(4, '0');
    return {
      transition_id: `transition.site.ecosystem-chat.${session}.${suffix}`,
      run_id: `site-chat-run.${session}.${suffix}`,
      event_id: `site-chat-event:${session}:${suffix}`,
      origin_manifest_id: `origin.site.ecosystem-chat.${session}.${suffix}`,
      parent_transition_id: null,
      previous_receipt_id: null
    };
  }

  function identityEnvelope(identity, message, posture) {
    return {
      schema_version: CONTRACT_VERSION,
      record_type: 'governed_transition_relationship',
      transition_id: identity.transition_id,
      run_id: identity.run_id,
      lifecycle_state: 'DECLARED',
      origin: {
        origin_class: ORIGIN_CLASS,
        event_id: identity.event_id,
        origin_manifest_id: identity.origin_manifest_id,
        observed_at: new Date().toISOString(),
        source_ref: SOURCE_REF
      },
      relationships: {
        parent_transition_id: identity.parent_transition_id,
        previous_receipt_id: identity.previous_receipt_id,
        actor_ref: `site-session:${sessionId()}`,
        target_ref: 'repository:StegVerse-Labs/hybrid-collab-bridge',
        repository_ref: 'StegVerse-Labs/Site',
        handoff_ref: 'docs/SITE_MIRROR_HANDOFF.md',
        task_ref: `task:ecosystem-chat:${posture.intent.id}`,
        next_task_ref: null
      },
      governance: {
        policy_refs: ['policy:site-preview-only', 'policy:ecosystem-chat-candidate'],
        delegation_refs: [],
        evidence_refs: [`evidence:site-chat-message:${identity.event_id}`],
        micro_node_manifest_ref: null,
        admissibility_result: 'PENDING',
        commit_time_validity: 'PENDING'
      },
      execution: { action_ref: null, verification_ref: null, resulting_state_ref: null },
      continuity: {
        final_receipt_id: null,
        master_record_ref: null,
        master_record_status: 'NOT_YET_SUBMITTED',
        reconstruction_status: 'NOT_YET_CHECKED'
      },
      projection: { site_visibility: 'SUMMARY', wiki_visibility: 'SUMMARY', redaction_class: 'PUBLIC_REDACTED' },
      preview_payload: {
        message,
        requested_route: posture.route,
        transition_intent: posture.intent.id,
        interaction_profile: posture.interaction_profile,
        raw_shell_allowed: false,
        execution_authorized: false,
        receipt_issued: false
      }
    };
  }

  async function loadGatewayConfig() {
    try {
      const response = await fetch(CONFIG_PATH, { cache: 'no-store' });
      if (!response.ok) throw new Error(`config HTTP ${response.status}`);
      const config = await response.json();
      if (config.schema_version !== CONTRACT_VERSION) throw new Error('config version mismatch');
      if (!config.authority_boundary || config.authority_boundary.site_execution_authority !== false || config.authority_boundary.gateway_execution_authority !== false) throw new Error('authority boundary mismatch');
      return config;
    } catch (error) {
      return { enabled: false, fallback: 'LOCAL_CLASSIFICATION', error: String(error) };
    }
  }

  async function callGateway(config, message, posture, identity) {
    const controller = new AbortController();
    const timeout = window.setTimeout(() => controller.abort(), Number(config.timeout_ms || 20000));
    try {
      const response = await fetch(config.endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-SteGVerse-Session': sessionId() },
        signal: controller.signal,
        body: JSON.stringify({
          message,
          session_id: sessionId(),
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
          interaction_bands: ['intra', 'inter', 'research', 'provider', 'solver', 'receipt'],
          math_solver_supported: true,
          transition_identity: identity
        })
      });
      if (!response.ok) throw new Error(`gateway HTTP ${response.status}`);
      const data = await response.json();
      if (data.transition_id !== identity.transition_id || data.run_id !== identity.run_id || data.event_id !== identity.event_id || data.origin_manifest_id !== identity.origin_manifest_id) throw new Error('gateway identity mismatch');
      if (data.authority && data.authority.provider_output_is_authority !== false) throw new Error('provider authority boundary mismatch');

      const finalReceipt = data.final_receipt_id || 'null';
      const custodyState = data.custody_submission?.state || data.master_record_status || 'NOT_YET_SUBMITTED';
      const persistence = data.sqlite_persisted === true ? 'SQLITE_PERSISTED' : 'UNCONFIRMED';
      const restartDurability = data.storage_durable_across_restarts === true ? 'DURABLE' : 'EPHEMERAL_HOST_STORAGE';
      const provider = data.provider || {};
      const providerStatus = provider.status || 'NOT_EVALUATED';
      const providerMode = provider.used === true ? 'GOVERNED_PROVIDER_USED' : 'DETERMINISTIC_FALLBACK';
      const providerReceipt = provider.provider_receipt_id || 'null';
      const providerCost = Number(provider.estimated_cost_usd || 0).toFixed(8);

      return {
        response: `${data.response}\n\nTransition identity: ${data.transition_id}\nRun identity: ${data.run_id}\nOrigin manifest: ${data.origin_manifest_id}\nLifecycle: ${data.lifecycle_state || 'UNKNOWN'}\nAdmissibility: ${data.admissibility_result || 'PENDING'}\nCommit-time validity: ${data.commit_time_validity || 'PENDING'}\nResponse source: ${providerMode}\nProvider status: ${providerStatus}\nProvider: ${provider.provider_name || 'none'}\nProvider model: ${provider.model || 'none'}\nProvider response receipt: ${providerReceipt}\nEstimated provider cost: $${providerCost}\nProvider output authority: false\nFinal response receipt: ${finalReceipt}\nLocal persistence: ${persistence}\nRestart durability: ${restartDurability}\nMaster-Records custody: ${data.master_record_status || 'NOT_YET_SUBMITTED'}\nCustody queue: ${custodyState}\nMaster record: ${data.master_record_ref || 'null'}\nReconstruction: ${data.reconstruction_status || 'NOT_YET_CHECKED'}`,
        receipt_line: `gateway_receipt_id=${data.receipt_id || 'null'} · provider_status=${providerStatus} · provider_receipt_id=${providerReceipt} · final_receipt_id=${finalReceipt} · lifecycle=${data.lifecycle_state || 'UNKNOWN'} · persistence=${persistence} · custody=${custodyState} · transition_id=${data.transition_id} · run_id=${data.run_id}`,
        interaction_profile: data.interaction_profile || posture.interaction_profile,
        intent: posture.intent,
        route: data.routed_module || posture.route,
        gateway_status: data.task_status,
        lifecycle_state: data.lifecycle_state,
        provider,
        final_receipt_id: data.final_receipt_id,
        master_record_status: data.master_record_status,
        master_record_ref: data.master_record_ref,
        reconstruction_status: data.reconstruction_status,
        sqlite_persisted: data.sqlite_persisted === true,
        storage_durable_across_restarts: data.storage_durable_across_restarts === true,
        custody_submission: data.custody_submission || null,
        transition_id: data.transition_id,
        run_id: data.run_id,
        event_id: data.event_id,
        origin_manifest_id: data.origin_manifest_id
      };
    } finally {
      window.clearTimeout(timeout);
    }
  }

  const originalRoute = window.routeEcosystemRequest;
  if (typeof originalRoute === 'function') {
    window.routeEcosystemRequest = async function governedIdentityRoute(message) {
      const posture = window.classifyRequestPosture(message);
      const identity = nextIdentity();
      const envelope = identityEnvelope(identity, message, posture);
      window.sessionStorage.setItem('stegverse_ecosystem_chat_last_candidate', JSON.stringify(envelope));
      const config = await loadGatewayConfig();
      if (config.enabled === true && config.endpoint) {
        try {
          const result = await callGateway(config, message, posture, identity);
          window.sessionStorage.setItem('stegverse_ecosystem_chat_last_gateway_result', JSON.stringify(result));
          return result;
        } catch (error) {
          window.sessionStorage.setItem('stegverse_ecosystem_chat_gateway_error', String(error));
        }
      }
      const result = await originalRoute(message);
      Object.assign(result, identity);
      result.receipt_line = `${result.receipt_line} · transition_id=${identity.transition_id} · run_id=${identity.run_id} · origin_manifest_id=${identity.origin_manifest_id} · gateway=fallback · provider_status=NOT_CALLED`;
      result.response = `${result.response}\n\nTransition identity: ${identity.transition_id}\nRun identity: ${identity.run_id}\nOrigin manifest: ${identity.origin_manifest_id}\nLifecycle: DECLARED\nGateway: unavailable or disabled; local fallback active\nProvider: not called\nAuthority effect: none`;
      return result;
    };
  }

  const originalBuildManifest = window.buildManifest;
  if (typeof originalBuildManifest === 'function') {
    window.buildManifest = function governedIdentityManifest() {
      const manifest = originalBuildManifest();
      const identity = nextIdentity();
      return {
        ...manifest,
        schema_version: CONTRACT_VERSION,
        record_type: 'governed_transition_relationship_candidate',
        ...identity,
        origin_class: ORIGIN_CLASS,
        lifecycle_state: 'DECLARED',
        final_receipt_id: null,
        master_record_status: 'NOT_YET_SUBMITTED',
        reconstruction_status: 'NOT_YET_CHECKED'
      };
    };
  }

  window.StegVerseChatTransitionIdentity = {
    contract_version: CONTRACT_VERSION,
    origin_class: ORIGIN_CLASS,
    nextIdentity,
    identityEnvelope,
    loadGatewayConfig
  };
})();
