(() => {
  'use strict';

  const EMAIL_FIELD_ID = 'submission-notification-email';
  const OPT_IN_ID = 'submission-notification-opt-in';
  const DELIVERY_STATUS_ID = 'submission-notification-delivery-status';
  const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const SHA256_RE = /^[a-f0-9]{64}$/;
  const TERMINAL_DELIVERY_STATES = new Set(['DELIVERED', 'PARTIAL_EXPIRED', 'DELIVERY_EXPIRED']);
  const READINESS_SCHEMA = 'HIL-READINESS-v1';
  const READINESS_SCHEMA_PATH = '/schemas/hil-readiness-v1.schema.json';
  const STATUS_SCHEMA = 'HIL-SUBMISSION-STATUS-v1';
  const STATUS_SCHEMA_PATH = '/schemas/hil-submission-status-v1.schema.json';
  const NOTIFICATION_SCHEMA = 'HIL-ATTEMPT-NOTIFICATION-v1';
  const NOTIFICATION_SCHEMA_PATH = '/schemas/hil-attempt-notification-v1.schema.json';
  const AUTHORITY_EVIDENCE_SCHEMA = 'HIL-TVC-AUTHORITY-EVIDENCE-v1';
  const AUTHORITY_EVIDENCE_SCHEMA_PATH = '/schemas/hil-tvc-authority-evidence-v1.schema.json';
  const AUTHORITY_EVIDENCE_PATH = '/api/hil/authority-evidence';

  function byId(id) { return document.getElementById(id); }

  function bindField() {
    const optIn = byId(OPT_IN_ID);
    const email = byId(EMAIL_FIELD_ID);
    if (!optIn || !email || optIn.dataset.bound === 'true') return;
    optIn.dataset.bound = 'true';
    email.disabled = !optIn.checked;
    optIn.addEventListener('change', () => {
      email.disabled = !optIn.checked;
      email.setCustomValidity('');
      if (optIn.checked) email.focus(); else email.value = '';
    });
  }

  function installField() {
    if (!byId(EMAIL_FIELD_ID)) {
      const participantField = byId('participant-id');
      if (!participantField || !participantField.parentElement) return;
      const field = document.createElement('div');
      field.className = 'field';
      field.innerHTML = `
        <label for="${EMAIL_FIELD_ID}">Email a copy of the submission notification <span>(optional)</span></label>
        <input id="${EMAIL_FIELD_ID}" name="${EMAIL_FIELD_ID}" type="email" inputmode="email" autocomplete="email" placeholder="you@example.com" disabled>
        <label><input id="${OPT_IN_ID}" type="checkbox"> Send this attempt's privacy-minimized submission notification to this address.</label>
        <p class="optional-note">The address is retained only while this attempt's bounded delivery authority remains active. It is removed after delivery or retry expiry and is not treated as publication or continuing-contact consent.</p>`;
      participantField.parentElement.insertAdjacentElement('afterend', field);
    }
    bindField();
  }

  function selectedEmail() {
    const optIn = byId(OPT_IN_ID);
    const email = byId(EMAIL_FIELD_ID);
    if (!optIn || !email || !optIn.checked) return null;
    const value = email.value.trim();
    if (!EMAIL_RE.test(value)) {
      email.setCustomValidity('Enter a valid email address or turn off notification delivery.');
      email.reportValidity();
      throw new Error('participant_notification_email_invalid');
    }
    email.setCustomValidity('');
    return value;
  }

  async function sha256Hex(buffer) {
    const digest = await crypto.subtle.digest('SHA-256', buffer);
    return Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, '0')).join('');
  }

  async function fetchBoundArtifact(readinessUrl, path, expectedDigest, acceptedType) {
    if (!SHA256_RE.test(String(expectedDigest || ''))) return null;
    const artifactUrl = new URL(path, readinessUrl);
    const response = await originalFetch(artifactUrl.href, { cache: 'no-store', headers: { Accept: acceptedType } });
    if (!response.ok) return null;
    const contentType = String(response.headers.get('content-type') || '').toLowerCase();
    if (!contentType.includes('json')) return null;
    const body = await response.arrayBuffer();
    if (await sha256Hex(body) !== expectedDigest) return null;
    return { body, json: JSON.parse(new TextDecoder().decode(body)) };
  }

  async function discoveryCompatible(payload, readinessUrl) {
    const advertisedTerminal = new Set(payload.terminal_notification_delivery_states || []);
    const structureMatches = payload.schema_version === READINESS_SCHEMA
      && payload.readiness_schema_path === READINESS_SCHEMA_PATH
      && payload.participant_notification_supported === true
      && payload.participant_notification_scope === 'ATTEMPT_NOTIFICATION_ONLY'
      && payload.attempt_notification_schema === NOTIFICATION_SCHEMA
      && payload.attempt_notification_schema_path === NOTIFICATION_SCHEMA_PATH
      && payload.submission_status_supported === true
      && payload.submission_status_schema === STATUS_SCHEMA
      && payload.submission_status_schema_path === STATUS_SCHEMA_PATH
      && payload.submission_status_authorization === 'SUBMISSION_ID_PLUS_RECEIPT_ID'
      && payload.runtime_contract_version === 'HIL-RTG-RUNTIME-v1'
      && payload.tvc_authority_role === 'service_gateway_intake'
      && typeof payload.tvc_decision_id === 'string' && payload.tvc_decision_id.length > 0
      && /^(sha256:)?[a-fA-F0-9]{64}$/.test(String(payload.tvc_policy_hash || ''))
      && SHA256_RE.test(String(payload.tvc_decision_receipt_sha256 || ''))
      && payload.tvc_admissible === true
      && payload.tvc_binding_matched === true
      && payload.authority_evidence_schema === AUTHORITY_EVIDENCE_SCHEMA
      && payload.authority_evidence_schema_path === AUTHORITY_EVIDENCE_SCHEMA_PATH
      && SHA256_RE.test(String(payload.authority_evidence_schema_sha256 || ''))
      && payload.authority_evidence_path === AUTHORITY_EVIDENCE_PATH
      && SHA256_RE.test(String(payload.authority_evidence_sha256 || ''))
      && Number.isInteger(payload.notification_max_attempts)
      && payload.notification_max_attempts >= 1 && payload.notification_max_attempts <= 20
      && advertisedTerminal.size === TERMINAL_DELIVERY_STATES.size
      && [...TERMINAL_DELIVERY_STATES].every((state) => advertisedTerminal.has(state))
      && payload.completed_recipient_addresses_retained === false
      && payload.expired_recipient_addresses_retained === false
      && payload.notification_delivery_changes_submission_outcome === false;
    if (!structureMatches) return false;

    const schemaBindings = [
      [payload.readiness_schema_path, payload.readiness_schema_sha256],
      [payload.attempt_notification_schema_path, payload.attempt_notification_schema_sha256],
      [payload.submission_status_schema_path, payload.submission_status_schema_sha256],
      [payload.authority_evidence_schema_path, payload.authority_evidence_schema_sha256]
    ];
    const schemas = await Promise.all(schemaBindings.map(([path, digest]) =>
      fetchBoundArtifact(readinessUrl, path, digest, 'application/schema+json, application/json')));
    if (!schemas.every(Boolean)) return false;

    const authority = await fetchBoundArtifact(readinessUrl, payload.authority_evidence_path, payload.authority_evidence_sha256, 'application/json');
    if (!authority) return false;
    const evidence = authority.json;
    const declaredEvidenceFields = new Set([
      'schema_version', 'runtime_contract_version', 'authority_role', 'decision_id', 'policy_hash',
      'admissible', 'binding_matched', 'allowed_keys_sha256', 'denied_keys_sha256',
      'allowed_key_count', 'denied_key_count', 'restricted_fields_exposed'
    ]);
    return Object.keys(evidence).every((field) => declaredEvidenceFields.has(field))
      && evidence.schema_version === AUTHORITY_EVIDENCE_SCHEMA
      && evidence.runtime_contract_version === payload.runtime_contract_version
      && evidence.authority_role === payload.tvc_authority_role
      && evidence.decision_id === payload.tvc_decision_id
      && evidence.policy_hash === payload.tvc_policy_hash
      && evidence.admissible === true
      && evidence.binding_matched === true
      && SHA256_RE.test(String(evidence.allowed_keys_sha256 || ''))
      && SHA256_RE.test(String(evidence.denied_keys_sha256 || ''))
      && evidence.allowed_key_count === 2
      && evidence.denied_key_count === 0
      && evidence.restricted_fields_exposed === false;
  }

  function incompatibleReadinessResponse(payload) {
    return new Response(JSON.stringify({ ...payload, state: 'INCOMPATIBLE', incompatibility_reason: 'HIL_RTG_DISCOVERY_CONTRACT_MISMATCH' }), { status: 200, headers: { 'Content-Type': 'application/json' } });
  }

  function deliveryStatusNode() {
    let node = byId(DELIVERY_STATUS_ID);
    if (node) return node;
    const intake = byId('intake-status');
    if (!intake) return null;
    node = document.createElement('div');
    node.id = DELIVERY_STATUS_ID;
    node.className = 'status';
    node.hidden = true;
    intake.insertAdjacentElement('afterend', node);
    return node;
  }

  function stateLabel(value) { return String(value || 'UNKNOWN').replaceAll('_', ' ').toLowerCase(); }

  function renderDeliveryStatus(status) {
    const node = deliveryStatusNode();
    if (!node) return;
    node.hidden = false;
    const participant = status.participant_copy_requested ? `Your optional copy is ${stateLabel(status.participant_copy_delivery_state)}.` : 'No participant email copy was requested.';
    const retry = status.notification_retry_authority_state === 'TERMINATED' ? ' Notification retry authority has ended and terminal recipient addresses are no longer retained.' : '';
    node.textContent = `Submission accepted. StegVerse notification is ${stateLabel(status.required_recipient_delivery_state)}. ${participant}${retry} Notification delivery does not change the submission outcome.`;
    node.dataset.state = status.notification_delivery_state === 'DELIVERED' ? 'ok' : 'warn';
  }

  async function pollStatus(statusUrl) {
    for (const delay of [1500, 4000, 9000, 18000, 35000]) {
      await new Promise((resolve) => setTimeout(resolve, delay));
      try {
        const response = await originalFetch(statusUrl, { cache: 'no-store', headers: { Accept: 'application/json' } });
        if (!response.ok) continue;
        const status = await response.json();
        if (status.schema_version !== STATUS_SCHEMA) continue;
        renderDeliveryStatus(status);
        if (TERMINAL_DELIVERY_STATES.has(status.notification_delivery_state)) return;
      } catch (error) { console.debug('HIL delivery-status check failed', error); }
    }
  }

  const originalFetch = window.fetch.bind(window);
  window.fetch = async (input, init = {}) => {
    const url = typeof input === 'string' ? input : input && input.url;
    const isReadiness = Boolean(url && url.includes('/api/hil/readiness'));
    const isSubmission = Boolean(url && url.includes('/api/hil/submissions') && init.body instanceof FormData);
    if (isSubmission) {
      const email = selectedEmail();
      init.body.set('participant_notification_requested', String(Boolean(email)));
      init.body.set('participant_notification_email', email || 'not_provided');
      init.body.set('participant_notification_scope', email ? 'ATTEMPT_NOTIFICATION_ONLY' : 'NONE');
    }
    const response = await originalFetch(input, init);
    if (isReadiness && response.ok) {
      try {
        const payload = await response.clone().json();
        if (!await discoveryCompatible(payload, url)) return incompatibleReadinessResponse(payload);
      } catch (error) {
        console.debug('HIL discovery contract validation failed', error);
        return incompatibleReadinessResponse({});
      }
    }
    if (isSubmission && response.ok) {
      try {
        const receipt = await response.clone().json();
        if (receipt && receipt.submission_id && receipt.receipt_id) {
          const submissionUrl = new URL(url, window.location.href);
          const statusUrl = new URL(`${submissionUrl.origin}${submissionUrl.pathname}/${encodeURIComponent(receipt.submission_id)}/status`);
          statusUrl.searchParams.set('receipt_id', receipt.receipt_id);
          pollStatus(statusUrl.href);
        }
      } catch (error) { console.debug('HIL receipt status initialization failed', error); }
    }
    return response;
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', installField, { once: true });
  else installField();
})();
