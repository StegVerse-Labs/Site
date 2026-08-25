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
      const route = await ingress.loadRoute(config);
      if (config.status !== 'PROVISIONED' || route.status !== 'ROUTE_LIVE') throw new Error('SKAP ingress is not live');
      for (const id of ['coinbaseApiKeyName', 'coinbaseApiPrivateKey', 'coinbaseSealCredential']) {
        const node = el(id);
        if (node) node.disabled = false;
      }
      const status = el('coinbaseIngressStatus');
      if (status) status.textContent = 'SKAP recipient and live InTr route verified. Credential stays local until sealed, then ciphertext only is submitted.';
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
      const result = await window.StegFinCoinbaseSkapIngress.sealAndSubmitCoinbaseCredential({ apiKeyName, apiPrivateKey });
      status.textContent = 'Ciphertext admitted into SKAP custody through InTr. No provider operation was authorized.';
      window.dispatchEvent(new CustomEvent('stegverse:coinbase-skap-ingress-admitted', { detail: {
        ingress_id: result.admission.ingress_id,
        credential_ref: result.admission.credential_ref,
        response_digest: result.admission.response_digest,
        transition_receipt: result.admission.transition_receipt,
        route_receipt_hash: result.route_receipt_hash,
        execution_authority: result.admission.execution_authority,
      } }));
    } catch (error) {
      clearInputs();
      status.textContent = `Fail closed: ${String(error?.message || error)}. Do not retry an ambiguous ingress packet; obtain a new owner authorization.`;
    } finally {
      try {
        const config = await window.StegFinCoinbaseSkapIngress.loadConfig();
        const route = await window.StegFinCoinbaseSkapIngress.loadRoute(config);
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
