(() => {
  'use strict';

  function el(id) { return document.getElementById(id); }

  function disableInputs(reason) {
    for (const id of ['coinbaseApiKeyName', 'coinbaseApiPrivateKey', 'coinbaseSealCredential']) {
      const node = el(id);
      if (node) node.disabled = true;
    }
    const status = el('coinbaseIngressStatus');
    if (status) status.textContent = reason;
  }

  function clearInputs() {
    const key = el('coinbaseApiKeyName');
    const secret = el('coinbaseApiPrivateKey');
    if (key) key.value = '';
    if (secret) secret.value = '';
  }

  async function initialize() {
    const ingress = window.StegFinCoinbaseSkapIngress;
    const submission = window.StegFinCoinbaseSkapSubmission;
    if (!ingress || !submission) return disableInputs('SKAP ingress/submission modules unavailable. Credential entry is disabled.');
    try {
      const { config, route } = await submission.loadSubmissionConfig();
      if (config.status !== 'PROVISIONED' || route.status !== 'ROUTE_LIVE') throw new Error('SKAP ingress is not live');
      for (const id of ['coinbaseApiKeyName', 'coinbaseApiPrivateKey', 'coinbaseSealCredential']) {
        const node = el(id);
        if (node) node.disabled = false;
      }
      const status = el('coinbaseIngressStatus');
      if (status) status.textContent = 'SKAP recipient and live InTr route verified. Credential stays local until sealed; ciphertext submission revalidates the route again.';
    } catch (error) {
      disableInputs(`Fail closed: ${String(error?.message || error)}. No credential may be entered.`);
    }
  }

  async function sealFromUi() {
    const button = el('coinbaseSealCredential');
    const status = el('coinbaseIngressStatus');
    const keyInput = el('coinbaseApiKeyName');
    const secretInput = el('coinbaseApiPrivateKey');
    if (!button || !status || !keyInput || !secretInput) return;
    button.disabled = true;
    try {
      const apiKeyName = keyInput.value;
      const apiPrivateKey = secretInput.value;
      clearInputs();
      if (!apiKeyName || !apiPrivateKey) throw new Error('both Coinbase credential fields are required');
      const packet = await window.StegFinCoinbaseSkapIngress.sealCoinbaseCredential({ apiKeyName, apiPrivateKey });
      status.textContent = 'Credential sealed for SKAP. Revalidating the live InTr route before ciphertext-only submission…';
      window.dispatchEvent(new CustomEvent('stegverse:coinbase-skap-ingress-sealed', { detail: packet }));
    } catch (error) {
      clearInputs();
      status.textContent = `Fail closed: ${String(error?.message || error)}. No credential was submitted.`;
    } finally {
      try {
        const { config, route } = await window.StegFinCoinbaseSkapSubmission.loadSubmissionConfig();
        button.disabled = config.status !== 'PROVISIONED' || route.status !== 'ROUTE_LIVE';
      } catch (_) {
        disableInputs('Fail closed: SKAP recipient or InTr route unavailable. Credential entry is disabled.');
      }
    }
  }

  window.addEventListener('DOMContentLoaded', () => {
    const button = el('coinbaseSealCredential');
    if (button) button.addEventListener('click', sealFromUi);
    initialize();
  }, { once: true });
})();
