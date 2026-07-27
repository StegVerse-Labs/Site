(() => {
  'use strict';

  const EMAIL_FIELD_ID = 'submission-notification-email';
  const OPT_IN_ID = 'submission-notification-opt-in';
  const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  function byId(id) {
    return document.getElementById(id);
  }

  function installField() {
    if (byId(EMAIL_FIELD_ID)) return;
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

    const optIn = byId(OPT_IN_ID);
    const email = byId(EMAIL_FIELD_ID);
    optIn.addEventListener('change', () => {
      email.disabled = !optIn.checked;
      if (optIn.checked) email.focus();
      else email.value = '';
    });
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

  const originalFetch = window.fetch.bind(window);
  window.fetch = async (input, init = {}) => {
    const url = typeof input === 'string' ? input : input && input.url;
    if (url && url.includes('/api/hil/submissions') && init.body instanceof FormData) {
      const email = selectedEmail();
      init.body.set('participant_notification_requested', String(Boolean(email)));
      init.body.set('participant_notification_email', email || 'not_provided');
      init.body.set('participant_notification_scope', email ? 'ATTEMPT_NOTIFICATION_ONLY' : 'NONE');
    }
    return originalFetch(input, init);
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', installField, { once: true });
  } else {
    installField();
  }
})();
