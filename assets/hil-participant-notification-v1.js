(() => {
  'use strict';

  const EMAIL_FIELD_ID = 'submission-notification-email';
  const OPT_IN_ID = 'submission-notification-opt-in';
  const DELIVERY_STATUS_ID = 'submission-notification-delivery-status';
  const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  function byId(id) {
    return document.getElementById(id);
  }

  function bindField() {
    const optIn = byId(OPT_IN_ID);
    const email = byId(EMAIL_FIELD_ID);
    if (!optIn || !email || optIn.dataset.bound === 'true') return;
    optIn.dataset.bound = 'true';
    email.disabled = !optIn.checked;
    optIn.addEventListener('change', () => {
      email.disabled = !optIn.checked;
      email.setCustomValidity('');
      if (optIn.checked) email.focus();
      else email.value = '';
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
        <p class="optional-note">The address is used only to deliver this attempt's notification. It is not published, added to the public response record, or treated as publication consent.</p>`;
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

  function stateLabel(value) {
    return String(value || 'UNKNOWN').replaceAll('_', ' ').toLowerCase();
  }

  function renderDeliveryStatus(status) {
    const node = deliveryStatusNode();
    if (!node) return;
    node.hidden = false;
    const participant = status.participant_copy_requested
      ? `Your optional copy is ${stateLabel(status.participant_copy_delivery_state)}.`
      : 'No participant email copy was requested.';
    node.textContent = `Submission accepted. StegVerse notification is ${stateLabel(status.required_recipient_delivery_state)} ${participant} Notification delivery does not change the submission outcome.`;
    node.dataset.state = status.notification_delivery_state === 'DELIVERED' ? 'ok' : 'warn';
  }

  async function pollStatus(statusUrl) {
    const delays = [1500, 4000, 9000, 18000, 35000];
    for (const delay of delays) {
      await new Promise((resolve) => setTimeout(resolve, delay));
      try {
        const response = await originalFetch(statusUrl, {
          cache: 'no-store',
          headers: { Accept: 'application/json' }
        });
        if (!response.ok) continue;
        const status = await response.json();
        if (status.schema_version !== 'HIL-SUBMISSION-STATUS-v1') continue;
        renderDeliveryStatus(status);
        if (status.notification_delivery_state === 'DELIVERED') return;
      } catch (error) {
        console.debug('HIL delivery-status check failed', error);
      }
    }
  }

  const originalFetch = window.fetch.bind(window);
  window.fetch = async (input, init = {}) => {
    const url = typeof input === 'string' ? input : input && input.url;
    const isSubmission = Boolean(
      url && url.includes('/api/hil/submissions') && init.body instanceof FormData
    );
    if (isSubmission) {
      const email = selectedEmail();
      init.body.set('participant_notification_requested', String(Boolean(email)));
      init.body.set('participant_notification_email', email || 'not_provided');
      init.body.set('participant_notification_scope', email ? 'ATTEMPT_NOTIFICATION_ONLY' : 'NONE');
    }
    const response = await originalFetch(input, init);
    if (isSubmission && response.ok) {
      try {
        const receipt = await response.clone().json();
        if (receipt && receipt.submission_id && receipt.receipt_id) {
          const submissionUrl = new URL(url, window.location.href);
          const statusUrl = new URL(
            `${submissionUrl.origin}${submissionUrl.pathname}/${encodeURIComponent(receipt.submission_id)}/status`
          );
          statusUrl.searchParams.set('receipt_id', receipt.receipt_id);
          pollStatus(statusUrl.href);
        }
      } catch (error) {
        console.debug('HIL receipt status initialization failed', error);
      }
    }
    return response;
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', installField, { once: true });
  } else {
    installField();
  }
})();
