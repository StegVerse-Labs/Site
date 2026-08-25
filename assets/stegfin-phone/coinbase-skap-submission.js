(() => {
  'use strict';

  const CONFIG_URL = './assets/stegfin-phone/coinbase-skap-ingress-config.json';
  const ROUTE_URL = './assets/stegfin-phone/coinbase-skap-intr-route.json';
  const ROUTE_SCHEMA = 'stegverse.tvc.skap_browser_intr_route/v1';
  const FALLBACK_ROUTE_PATH = '/v1/skap/coinbase/ingress';
  const PRIMARY_GATEWAY_PATH = '/api/coinbase/skap/ingress';
  const FALLBACK_CARRIER = 'ZERO_CREDENTIAL_ROTATING_HTTPS_TUNNEL';

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
    if (config?.transport_protocol !== 'InTr' || config?.credential_authority !== 'TV/TVC' || !['SKAP', 'KV_HOSTED_SKAP_VAULT'].includes(config?.credential_custody_target)) throw new Error('SKAP recipient authority/transport binding invalid');
    if (!config?.runtime_instance_id || !config?.recipient_key_id || !config?.lease_expires_at) throw new Error('SKAP recipient runtime binding incomplete');
    requireHash(config.activation_receipt_hash, 'SKAP recipient activation receipt');
    requireHash(config.liveness_receipt_hash, 'SKAP recipient liveness receipt');
    const lease = Date.parse(config.lease_expires_at);
    if (!Number.isFinite(lease) || lease <= Date.now()) throw new Error('SKAP recipient lease expired');
    return config;
  }

  function validatePrimaryGateway(config) {
    if (config?.submission_status !== 'PROVISIONED' || !config?.submission_endpoint) throw new Error('StegVerse primary SKAP Gateway is not provisioned');
    const endpoint = new URL(config.submission_endpoint);
    if (endpoint.protocol !== 'https:' || !['stegverse.org', 'www.stegverse.org'].includes(endpoint.hostname)) throw new Error('primary SKAP Gateway origin invalid');
    if (endpoint.pathname !== PRIMARY_GATEWAY_PATH || endpoint.username || endpoint.password || endpoint.search || endpoint.hash) throw new Error('primary SKAP Gateway endpoint binding invalid');
    return endpoint;
  }

  function validateFallbackRoute(route, config) {
    if (route?.schema !== ROUTE_SCHEMA || route?.status !== 'ROUTE_LIVE') throw new Error('fallback SKAP InTr route is not live');
    if (route?.transport_protocol !== 'InTr' || route?.credential_authority !== 'TV/TVC' || !['SKAP', 'KV_HOSTED_SKAP_VAULT'].includes(route?.credential_custody_target)) throw new Error('fallback SKAP route authority/transport binding invalid');
    if (route?.carrier !== FALLBACK_CARRIER) throw new Error('fallback SKAP carrier class invalid');
    if (route?.public_route_authority !== false || route?.provider_operation_authorized !== false || route?.credential_plaintext_carried !== false || route?.github_token_runtime_authority !== false || route?.github_actions_resident_authority !== false) throw new Error('fallback SKAP route attempted authority escalation');
    for (const field of ['runtime_instance_id', 'recipient_key_id', 'activation_receipt_hash', 'liveness_receipt_hash', 'lease_expires_at']) {
      if (route?.[field] !== config?.[field]) throw new Error(`SKAP recipient/fallback-route binding mismatch: ${field}`);
    }
    requireHash(route.route_receipt_hash, 'fallback SKAP InTr route receipt');
    const lease = Date.parse(route.lease_expires_at);
    if (!Number.isFinite(lease) || lease <= Date.now()) throw new Error('fallback SKAP InTr route lease expired');
    const endpoint = new URL(route.public_ingress_url);
    const origin = new URL(route.public_origin);
    if (endpoint.protocol !== 'https:' || origin.protocol !== 'https:') throw new Error('fallback SKAP InTr route must use HTTPS');
    if (!endpoint.hostname.endsWith('.trycloudflare.com') || endpoint.origin !== origin.origin) throw new Error('fallback SKAP rotating carrier origin invalid');
    if (endpoint.pathname !== FALLBACK_ROUTE_PATH || endpoint.username || endpoint.password || endpoint.search || endpoint.hash) throw new Error('fallback SKAP ingress endpoint binding invalid');
    if (origin.pathname !== '/' || origin.username || origin.password || origin.search || origin.hash) throw new Error('fallback SKAP public origin invalid');
    return endpoint;
  }

  async function loadSubmissionConfig() {
    const [configRaw, route] = await Promise.all([
      fetchJson(CONFIG_URL, 'SKAP recipient config'),
      fetchJson(ROUTE_URL, 'SKAP fallback route descriptor')
    ]);
    const config = validateRecipientConfig(configRaw);
    try {
      const endpoint = validatePrimaryGateway(config);
      return { config, route, endpoint, transportMode: 'PRIMARY_GATEWAY' };
    } catch (primaryError) {
      if (route?.status !== 'ROUTE_LIVE') throw primaryError;
      const endpoint = validateFallbackRoute(route, config);
      return { config, route, endpoint, transportMode: 'EXPLICIT_FALLBACK' };
    }
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

  function validateDeviceKvReceipt(receipt, packet) {
    if (!receipt || receipt.schema !== 'stegverse.intr.boundary_transition_receipt/v1') throw new Error('DEVICE/KV InTr receipt missing');
    if (receipt.connector !== 'InTr' || receipt.from_boundary !== 'DEVICE' || receipt.to_boundary !== 'KV') throw new Error('DEVICE/KV InTr boundary invalid');
    if (receipt.credential_ref !== packet.credential_ref || receipt.operation_id !== packet.ingress_id) throw new Error('DEVICE/KV InTr receipt binding mismatch');
    if (receipt.prior_boundary_receipt_hash !== null) throw new Error('DEVICE/KV InTr receipt must begin chain');
    if (receipt.secret_plaintext_present !== false || receipt.authority_transfer !== false) throw new Error('DEVICE/KV InTr receipt authority/plaintext violation');
    requireHash(receipt.receipt_hash, 'DEVICE/KV InTr receipt hash');
    return receipt;
  }

  function validateGatewayStageResponse(response, packet) {
    if (!response || typeof response !== 'object') throw new Error('Gateway staging response invalid');
    if (response.schema !== 'stegverse.service_gateway.coinbase_skap_stage_receipt/v1' || response.decision !== 'STAGED_FOR_TVC') throw new Error('Gateway did not confirm STAGED_FOR_TVC');
    if (response.credential_ref !== packet.credential_ref || response.ingress_id !== packet.ingress_id) throw new Error('Gateway staging response packet binding mismatch');
    validateDeviceKvReceipt(response.device_kv_interlock_receipt, packet);
    if (response.gateway_credential_value_access !== false || response.gateway_decryption_authority !== false || response.gateway_execution_authority !== 'NONE') throw new Error('Gateway response attempted authority escalation');
    if (response.tvc_admission_completed !== false) throw new Error('Gateway incorrectly claimed TVC/SKAP Vault admission');
    if (response.next_required_transition !== 'KV_SKAP_VAULT_INTERLOCK_ADMISSION') throw new Error('Gateway next transition is not KV/SKAP Vault Interlock');
    if (response.blind_retry_allowed !== false) throw new Error('Gateway response permits blind retry');
    requireHash(response.receipt_digest, 'Gateway staging receipt digest');
    return response;
  }

  function validateSkapVaultAdmissionResponse(response, packet) {
    if (!response || typeof response !== 'object') throw new Error('SKAP Vault admission response invalid');
    if (response.decision !== 'ADMITTED_TO_SKAP_VAULT') throw new Error('SKAP Vault admission was not proven');
    const first = validateDeviceKvReceipt(response.device_kv_interlock_receipt, packet);
    const second = response.kv_skap_interlock_receipt || {};
    if (second.schema !== 'stegverse.intr.boundary_transition_receipt/v1' || second.connector !== 'InTr' || second.from_boundary !== 'KV' || second.to_boundary !== 'SKAP_VAULT') throw new Error('KV/SKAP Vault InTr receipt invalid');
    if (second.credential_ref !== packet.credential_ref || second.operation_id !== packet.ingress_id || second.prior_boundary_receipt_hash !== first.receipt_hash) throw new Error('double-interlock receipt chain mismatch');
    if (second.secret_plaintext_present !== false || second.authority_transfer !== false) throw new Error('KV/SKAP Vault receipt authority/plaintext violation');
    requireHash(second.receipt_hash, 'KV/SKAP Vault InTr receipt hash');
    if (response.kv_decryption_authority !== false || response.device_durable_secret_custody !== false) throw new Error('SKAP Vault response weakened KV/Device boundary');
    if (response.decryption_performed !== false || response.rewrap_performed !== false) throw new Error('SKAP Vault admission performed premature decryption/rewrap');
    if (response.execution_authority !== 'NONE' || response.may_authorize_order !== false) throw new Error('SKAP Vault response attempted execution authority');
    requireHash(response.result_digest || response.response_digest, 'SKAP Vault admission result digest');
    return response;
  }

  async function submitCiphertext(packet) {
    validateCiphertextOnlyPacket(packet);
    const { config, endpoint, transportMode } = await loadSubmissionConfig();
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
    if (!response.ok) throw new Error(`SKAP transport rejected ciphertext (${response.status}); create a NEW owner-authorized packet before any retry`);
    const contentType = String(response.headers.get('content-type') || '').toLowerCase();
    if (!contentType.includes('application/json')) throw new Error('SKAP transport response content type invalid');
    const body = await response.json();
    if (transportMode === 'PRIMARY_GATEWAY') return { transportMode, state: 'STAGED_FOR_TVC', receipt: validateGatewayStageResponse(body, packet) };
    return { transportMode, state: 'ADMITTED_TO_SKAP_VAULT', receipt: validateSkapVaultAdmissionResponse(body, packet) };
  }

  window.addEventListener('stegverse:coinbase-skap-ingress-sealed', async (event) => {
    let packet = event?.detail;
    if (!packet) return;
    try {
      setStatus('Credential encrypted for the SKAP Vault. Revalidating recipient lease and governed transport…');
      const result = await submitCiphertext(packet);
      if (result.state === 'STAGED_FOR_TVC') {
        setStatus('Encrypted credential crossed the Device/KV Interlock and is staged for TVC. SKAP Vault custody is not yet claimed.');
        window.dispatchEvent(new CustomEvent('stegverse:coinbase-skap-ingress-staged-for-tvc', { detail: result.receipt }));
      } else {
        setStatus('Encrypted credential crossed both Interlocks and SKAP Vault custody is admitted. Provider authority remains ungranted until endpoint/session verification.');
        window.dispatchEvent(new CustomEvent('stegverse:coinbase-skap-vault-admitted', { detail: result.receipt }));
      }
    } catch (error) {
      const prefix = error?.code === 'VERIFY_EXTERNALLY' ? 'VERIFY_EXTERNALLY' : 'Fail closed';
      setStatus(`${prefix}: ${String(error?.message || error)}.`);
      window.dispatchEvent(new CustomEvent('stegverse:coinbase-skap-ingress-submission-failed', { detail: { decision: prefix, blind_retry_allowed: false } }));
    } finally { packet = null; }
  });

  window.StegFinCoinbaseSkapSubmission = Object.freeze({
    loadSubmissionConfig,
    validateRecipientConfig,
    validatePrimaryGateway,
    validateFallbackRoute,
    validateCiphertextOnlyPacket,
    validatePacketAgainstCurrentRecipient,
    validateDeviceKvReceipt,
    validateGatewayStageResponse,
    validateSkapVaultAdmissionResponse,
    submitCiphertext
  });
})();
