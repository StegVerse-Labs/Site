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
    if (!ingress) return disableInputs('SKAP ingress module unavailable. Credential entry is disabled.');
    try {
      const config = await ingress.loadConfig();
      if (config.status !== 'PROVISIONED') throw new Error('SKAP ingress key is not provisioned');
      for (const id of ['coinbaseApiKeyName', 'coinbaseApiPrivateKey', 'coinbaseSealCredential']) {
        const node = el(id);
        if (node) node.disabled = false;
      }
      const status = el('coinbaseIngressStatus');
      if (status) status.textContent = 'SKAP public ingress key verified. Credential entry remains local until encrypted.';
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
      // Clear DOM storage immediately after the transient values are copied into
      // the sealing function. JS strings themselves are immutable; no long-lived
      // string, localStorage, sessionStorage, IndexedDB, cookie, URL or log copy is made.
      clearInputs();
      if (!apiKeyName || !apiPrivateKey) throw new Error('both Coinbase credential fields are required');
      const packet = await window.StegFinCoinbaseSkapIngress.sealCoinbaseCredential({ apiKeyName, apiPrivateKey });
      status.textContent = 'Credential encrypted for SKAP. Plaintext fields cleared. Awaiting governed InTr submission adapter.';
      window.dispatchEvent(new CustomEvent('stegverse:coinbase-skap-ingress-sealed', { detail: packet }));
    } catch (error) {
      clearInputs();
      status.textContent = `Fail closed: ${String(error?.message || error)}. No credential was submitted.`;
    } finally {
      try {
        const config = await window.StegFinCoinbaseSkapIngress.loadConfig();
        button.disabled = config.status !== 'PROVISIONED';
      } catch (_) {
        disableInputs('Fail closed: SKAP ingress key unavailable. Credential entry is disabled.');
      }
    }
  }

  window.addEventListener('DOMContentLoaded', () => {
    const button = el('coinbaseSealCredential');
    if (button) button.addEventListener('click', sealFromUi);
    initialize();
  }, { once: true });
})();
