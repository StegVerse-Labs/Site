(() => {
  'use strict';

  const CONFIG_URL = './assets/stegfin-phone/coinbase-skap-ingress-config.json';
  const ROUTE_URL = './assets/stegfin-phone/coinbase-skap-intr-route.json';
  const ROUTE_SCHEMA = 'stegverse.tvc.skap_browser_intr_route/v1';
  const ROUTE_PATH = '/v1/skap/coinbase/ingress';
  const CARRIER = 'ZERO_CREDENTIAL_ROTATING_HTTPS_TUNNEL';

  function statusNode() { return document.getElementById('coinbaseIngressStatus'); }
  function setStatus(message) { const node = statusNode(); if (node) node.textContent = message; }

  async function fetchJson(url, label) {
    const response = await fetch(url, { cache: 'no-store', redirect: 'error', credentials: 'same-origin' });
    if (!response.ok) throw new Error(`${label} unavailable (${response.status})`);
    return response.json();
  }

  function requireHash(value, label) {
    if (!String(value || '').startsWith('sha256:')) throw new Error(`${label} missing`);
  }

  function validateRecipientConfig(config) {
    if (config?.schema !== 'stegverse.site.coinbase_skap_ingress_config/v1') throw new Error('SKAP recipient config schema invalid');
    if (config?.status !== 'PROVISIONED') throw new Error('SKAP recipient key is not provisioned');
    if (config?.transport_protocol !== 'InTr' || config?.credential_authority !== 'TV/TVC' || config?.credential_custody_target !== 'SKAP') throw new Error('SKAP recipient authority/transport binding invalid');
    if (!config?.runtime_instance_id || !config?.recipient_key_id || !config?.lease_expires_at) throw new Error('SKAP recipient runtime binding incomplete');
    requireHash(config.activation_receipt_hash, 'SKAP recipient activation receipt');
    requireHash(config.liveness_receipt_hash, 'SKAP recipient liveness receipt');
    const lease = Date.parse(config.lease_expires_at);
    if (!Number.isFinite(lease) || lease <= Date.now()) throw new Error('SKAP recipient lease expired');
    return config;
  }

  function validateRoute(route, config) {
    if (route?.schema !== ROUTE_SCHEMA || route?.status !== 'ROUTE_LIVE') throw new Error('SKAP InTr route is not live');
    if (route?.transport_protocol !== 'InTr' || route?.credential_authority !== 'TV/TVC' || route?.credential_custody_target !== 'SKAP') throw new Error('SKAP InTr route authority/transport binding invalid');
    if (route?.carrier !== CARRIER) throw new Error('SKAP InTr carrier class invalid');
    if (route?.public_route_authority !== false || route?.provider_operation_authorized !== false || route?.credential_plaintext_carried !== false || route?.github_token_runtime_authority !== false || route?.github_actions_resident_authority !== false) throw new Error('SKAP InTr route attempted authority escalation');
    for (const field of ['runtime_instance_id', 'recipient_key_id', 'activation_receipt_hash', 'liveness_receipt_hash', 'lease_expires_at']) {
      if (route?.[field] !== config?.[field]) throw new Error(`SKAP recipient/route binding mismatch: ${field}`);
    }
    requireHash(route.route_receipt_hash, 'SKAP InTr route receipt');
    const lease = Date.parse(route.lease_expires_at);
    if (!Number.isFinite(lease) || lease <= Date.now()) throw new Error('SKAP InTr route lease expired');
    const endpoint = new URL(route.public_ingress_url);
    const origin = new URL(route.public_origin);
    if (endpoint.protocol !== 'https:' || origin.protocol !== 'https:') throw new Error('SKAP InTr route must use HTTPS');
    if (!endpoint.hostname.endsWith('.trycloudflare.com') || endpoint.origin !== origin.origin) throw new Error('SKAP InTr rotating carrier origin invalid');
    if (endpoint.pathname !== ROUTE_PATH || endpoint.username || endpoint.password || endpoint.search || endpoint.hash) throw new Error('SKAP InTr ingress endpoint binding invalid');
    if (origin.pathname !== '/' || origin.username || origin.password || origin.search || origin.hash) throw new Error('SKAP InTr public origin invalid');
    return endpoint;
  }

  async function loadSubmissionConfig() {
    const [configRaw, route] = await Promise.all([
      fetchJson(CONFIG_URL, 'SKAP recipient config'),
      fetchJson(ROUTE_URL, 'SKAP InTr route descriptor')
    ]);
    const config = validateRecipientConfig(configRaw);
    const endpoint = validateRoute(route, config);
    return { config, route, endpoint };
  }

  function validateCiphertextOnlyPacket(packet) {
    if (!packet || typeof packet !== 'object') throw new Error('sealed ingress packet required');
    if (packet.schema !== 'stegverse.tvc.coinbase_iphone_skap_ingress/v1') throw new Error('sealed ingress packet schema invalid');
    if (packet.plaintext_present !== false || packet.device_secret_custody_authority !== false || packet.kv_secret_resolution_authority !== false || packet.github_environment_secret_access !== false) throw new Error('ciphertext packet authority boundary invalid');
    const sealed = packet.sealed_material || {};
    if (sealed.format !== 'stegverse.skap.browser_ingress/p256-ecdh-hkdf-sha256-aes256gcm/v1') throw new Error('browser ciphertext format invalid');
    if (sealed.plaintext_persisted !== false || sealed.device_private_key_persisted !== false || sealed.skap_private_key_exported !== false || sealed.authority_transfer !== false) throw new Error('browser ciphertext authority/persistence boundary invalid');
    const serialized = JSON.stringify(packet).toLowerCase();
    for (const forbidden of ['api_private_key', 'api_key_name', '-----begin private key-----', '"authorization"', '"access_token"', '"refresh_token"']) {
      if (serialized.includes(forbidden)) throw new Error(`plaintext/credential field forbidden in submission packet: ${forbidden}`);
    }
    return packet;
  }

  function validatePacketAgainstCurrentRecipient(packet, config) {
    if (packet.recipient_runtime_instance_id !== config.runtime_instance_id) throw new Error('sealed packet runtime instance is stale');
    if (packet.recipient_lease_expires_at !== config.lease_expires_at) throw new Error('sealed packet recipient lease is stale');
    if (packet.sealed_material?.recipient_key_id !== config.recipient_key_id) throw new Error('sealed packet recipient key is stale');
    if (packet.credential_version !== config.credential_version || packet.sealed_material?.credential_version !== config.credential_version) throw new Error('sealed packet credential version drift');
    if (Date.parse(packet.recipient_lease_expires_at) <= Date.now()) throw new Error('sealed packet recipient lease expired');
  }

  function validateAdmissionResponse(response) {
    if (!response || typeof response !== 'object') throw new Error('SKAP admission response invalid');
    if (response.schema !== 'stegverse.tvc.coinbase_browser_ingress_response/v2' || response.decision !== 'ADMITTED') throw new Error('SKAP admission was not admitted');
    if (response.browser_ciphertext_returned !== false || response.credential_plaintext_returned !== false) throw new Error('SKAP response leaked custody material');
    if (response.decryption_performed_at_ingress !== false || response.rewrap_performed_at_ingress !== false || response.endpoint_verification_required_before_decryption !== true) throw new Error('SKAP response weakened endpoint-before-decryption ordering');
    if (response.execution_authority !== 'NONE' || response.may_authorize_order !== false || response.credential_authority !== 'TV/TVC') throw new Error('SKAP response attempted authority escalation');
    if (response.retry_policy !== 'NEW_OWNER_AUTHORIZED_PACKET_REQUIRED') throw new Error('SKAP response retry policy invalid');
    if (response.transition_receipt?.transition !== 'IPHONE_BROWSER_SEALED->SKAP_CIPHERTEXT_CUSTODY' || response.transition_receipt?.sealed_material_persisted_unchanged !== true) throw new Error('SKAP ciphertext-preservation proof missing');
    if (response.transition_receipt?.decryption_performed !== false || response.transition_receipt?.rewrap_performed !== false) throw new Error('SKAP transition performed premature decryption/rewrap');
    requireHash(response.response_digest, 'SKAP admission response digest');
    return response;
  }

  async function submitCiphertext(packet) {
    validateCiphertextOnlyPacket(packet);
    // Resolve recipient + route immediately before POST. A route observed before
    // owner authorization/sealing is intentionally insufficient after rotation.
    const { config, endpoint } = await loadSubmissionConfig();
    validatePacketAgainstCurrentRecipient(packet, config);
    let response;
    try {
      response = await fetch(endpoint.href, {
        method: 'POST', redirect: 'error', credentials: 'omit', referrerPolicy: 'no-referrer', cache: 'no-store',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(packet)
      });
    } catch (error) {
      const ambiguous = new Error(`VERIFY_EXTERNALLY: ciphertext submission outcome ambiguous (${String(error?.message || error)}); blind retry forbidden`);
      ambiguous.code = 'VERIFY_EXTERNALLY'; throw ambiguous;
    }
    if (!response.ok) throw new Error(`SKAP admission endpoint rejected ciphertext (${response.status}); create a NEW owner-authorized packet before any retry`);
    const contentType = String(response.headers.get('content-type') || '').toLowerCase();
    if (!contentType.includes('application/json')) throw new Error('SKAP admission response content type invalid');
    return validateAdmissionResponse(await response.json());
  }

  window.addEventListener('stegverse:coinbase-skap-ingress-sealed', async (event) => {
    let packet = event?.detail;
    if (!packet) return;
    try {
      setStatus('Credential encrypted for SKAP. Revalidating the live InTr route before ciphertext submission…');
      const admission = await submitCiphertext(packet);
      setStatus('SKAP accepted ciphertext custody unchanged. Decryption remains forbidden until the Coinbase endpoint/session gate is verified.');
      window.dispatchEvent(new CustomEvent('stegverse:coinbase-skap-ingress-admitted', { detail: admission }));
    } catch (error) {
      const prefix = error?.code === 'VERIFY_EXTERNALLY' ? 'VERIFY_EXTERNALLY' : 'Fail closed';
      setStatus(`${prefix}: ${String(error?.message || error)}.`);
      window.dispatchEvent(new CustomEvent('stegverse:coinbase-skap-ingress-submission-failed', { detail: { decision: prefix, blind_retry_allowed: false } }));
    } finally { packet = null; }
  });

  window.StegFinCoinbaseSkapSubmission = Object.freeze({ loadSubmissionConfig, validateRecipientConfig, validateRoute, validateCiphertextOnlyPacket, validatePacketAgainstCurrentRecipient, validateAdmissionResponse, submitCiphertext });
})();
