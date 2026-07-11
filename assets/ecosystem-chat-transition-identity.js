(() => {
  'use strict';

  const CONTRACT_VERSION = '1.0.0';
  const ORIGIN_CLASS = 'SITE_INPUT';
  const SOURCE_REF = 'StegVerse-Labs/Site/ecosystem-chat.html';
  const SESSION_KEY = 'stegverse_ecosystem_chat_session';
  const COUNTER_KEY = 'stegverse_ecosystem_chat_transition_counter';

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
      execution: {
        action_ref: null,
        verification_ref: null,
        resulting_state_ref: null
      },
      continuity: {
        final_receipt_id: null,
        master_record_ref: null,
        master_record_status: 'NOT_YET_SUBMITTED',
        reconstruction_status: 'NOT_YET_CHECKED'
      },
      projection: {
        site_visibility: 'SUMMARY',
        wiki_visibility: 'SUMMARY',
        redaction_class: 'PUBLIC_REDACTED'
      },
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

  const originalRoute = window.routeEcosystemRequest;
  if (typeof originalRoute === 'function') {
    window.routeEcosystemRequest = async function governedIdentityRoute(message) {
      const posture = window.classifyRequestPosture(message);
      const identity = nextIdentity();
      const envelope = identityEnvelope(identity, message, posture);
      window.sessionStorage.setItem('stegverse_ecosystem_chat_last_candidate', JSON.stringify(envelope));
      const result = await originalRoute(message);
      result.transition_id = identity.transition_id;
      result.run_id = identity.run_id;
      result.event_id = identity.event_id;
      result.origin_manifest_id = identity.origin_manifest_id;
      result.receipt_line = `${result.receipt_line} · transition_id=${identity.transition_id} · run_id=${identity.run_id} · origin_manifest_id=${identity.origin_manifest_id}`;
      result.response = `${result.response}\n\nTransition identity: ${identity.transition_id}\nRun identity: ${identity.run_id}\nOrigin manifest: ${identity.origin_manifest_id}\nLifecycle: DECLARED\nAuthority effect: none`;
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
        transition_id: identity.transition_id,
        run_id: identity.run_id,
        event_id: identity.event_id,
        origin_manifest_id: identity.origin_manifest_id,
        origin_class: ORIGIN_CLASS,
        lifecycle_state: 'DECLARED',
        parent_transition_id: null,
        previous_receipt_id: null,
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
    identityEnvelope
  };
})();
