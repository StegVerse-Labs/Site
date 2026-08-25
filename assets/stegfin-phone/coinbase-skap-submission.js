(() => {
  'use strict';

  const CONFIG_URL = './assets/stegfin-phone/coinbase-skap-ingress-config.json';
  const ALLOWED_RECEIVER_ORIGINS = new Set(['https://stegverse.org', 'https://www.stegverse.org']);

  function statusNode() { return document.getElementById('coinbaseIngressStatus'); }
  function setStatus(message) { const node = statusNode(); if (node) node.textContent = message; }

  async function loadSubmissionConfig() {
    const response = await fetch(CONFIG_URL, { cache: 'no-store', redirect: 'error', credentials: 'same-origin' });
    if (!response.ok) throw new Error(`SKAP submission config unavailable (${response.status})`);
    const config = await response.json();
    if (config?.schema !== 'stegverse.site.coinbase_skap_ingress_config/v1') throw new Error('SKAP submission config schema invalid');
    if (config?.submission_status !== 'PROVISIONED') throw new Error('SKAP submission receiver is not provisioned');
    if (!config?.submission_endpoint) throw new Error('SKAP submission endpoint missing');
    const endpoint = new URL(config.submission_endpoint, location.origin);
    if (endpoint.protocol !== 'https:') throw new Error('SKAP submission endpoint must use HTTPS');
    if (!ALLOWED_RECEIVER_ORIGINS.has(endpoint.origin)) throw new Error('SKAP submission receiver origin is not StegVerse-authorized');
    if (endpoint.username || endpoint.password || endpoint.search || endpoint.hash) throw new Error('SKAP submission endpoint must not contain credentials/query/fragment');
    if (!endpoint.pathname.startsWith('/')) throw new Error('SKAP submission endpoint path invalid');
    return { config, endpoint };
  }

  function validateCiphertextOnlyPacket(packet) {
    if (!packet || typeof packet !== 'object') throw new Error('sealed ingress packet required');
    if (packet.schema !== 'stegverse.tvc.coinbase_iphone_skap_ingress/v1') throw new Error('sealed ingress packet schema invalid');
    if (packet.plaintext_present !== false) throw new Error('plaintext-bearing ingress packet rejected');
    if (packet.device_secret_custody_authority !== false) throw new Error('device secret custody claim rejected');
    if (packet.kv_secret_resolution_authority !== false) throw new Error('KV secret resolution claim rejected');
    if (packet.github_environment_secret_access !== false) throw new Error('GitHub secret access claim rejected');
    const sealed = packet.sealed_material || {};
    if (sealed.format !== 'stegverse.skap.browser_ingress/p256-ecdh-hkdf-sha256-aes256gcm/v1') throw new Error('browser ciphertext format invalid');
    if (sealed.plaintext_persisted !== false || sealed.device_private_key_persisted !== false || sealed.skap_private_key_exported !== false || sealed.authority_transfer !== false) {
      throw new Error('browser ciphertext authority/persistence boundary invalid');
    }
    const serialized = JSON.stringify(packet).toLowerCase();
    for (const forbidden of ['api_private_key', 'api_key_name', '-----begin private key-----', '"authorization"', '"access_token"', '"refresh_token"']) {
      if (serialized.includes(forbidden)) throw new Error(`plaintext/credential field forbidden in submission packet: ${forbidden}`);
    }
    return packet;
  }

  function validateAdmissionResponse(response) {
    if (!response || typeof response !== 'object') throw new Error('SKAP admission response invalid');
    if (response.schema !== 'stegverse.tvc.coinbase_browser_ingress_response/v2') throw new Error('SKAP admission response schema invalid');
    if (response.decision !== 'ADMITTED') throw new Error('SKAP admission was not admitted');
    if (response.browser_ciphertext_returned !== false || response.credential_plaintext_returned !== false) throw new Error('SKAP response leaked custody material');
    if (response.decryption_performed_at_ingress !== false || response.rewrap_performed_at_ingress !== false) throw new Error('SKAP ingress attempted premature decryption/rewrap');
    if (response.endpoint_verification_required_before_decryption !== true) throw new Error('SKAP response weakened endpoint-before-decryption ordering');
    if (response.execution_authority !== 'NONE' || response.may_authorize_order !== false) throw new Error('SKAP response attempted authority escalation');
    if (response.retry_policy !== 'NEW_OWNER_AUTHORIZED_PACKET_REQUIRED') throw new Error('SKAP response retry policy invalid');
    if (response.transition_receipt?.transition !== 'IPHONE_BROWSER_SEALED->SKAP_CIPHERTEXT_CUSTODY') throw new Error('SKAP custody transition invalid');
    if (response.transition_receipt?.sealed_material_persisted_unchanged !== true) throw new Error('SKAP ciphertext-preservation proof missing');
    if (response.transition_receipt?.decryption_performed !== false || response.transition_receipt?.rewrap_performed !== false) throw new Error('SKAP transition performed premature decryption/rewrap');
    if (!response.response_digest || !String(response.response_digest).startsWith('sha256:')) throw new Error('SKAP admission response digest missing');
    return response;
  }

  async function submitCiphertext(packet) {
    validateCiphertextOnlyPacket(packet);
    const { endpoint } = await loadSubmissionConfig();
    let response;
    try {
      response = await fetch(endpoint.href, {
        method: 'POST',
        redirect: 'error',
        credentials: 'omit',
        referrerPolicy: 'no-referrer',
        cache: 'no-store',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'X-StegVerse-Transport': 'InTr-browser-ciphertext-v1'
        },
        body: JSON.stringify(packet)
      });
    } catch (error) {
      const ambiguous = new Error(`VERIFY_EXTERNALLY: ciphertext submission outcome ambiguous (${String(error?.message || error)}); blind retry forbidden`);
      ambiguous.code = 'VERIFY_EXTERNALLY';
      throw ambiguous;
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
      setStatus('Credential encrypted for SKAP. Submitting ciphertext through governed InTr receiver…');
      const admission = await submitCiphertext(packet);
      setStatus('SKAP accepted ciphertext custody unchanged. Decryption remains forbidden until the Coinbase endpoint/session gate is verified.');
      window.dispatchEvent(new CustomEvent('stegverse:coinbase-skap-ingress-admitted', { detail: admission }));
    } catch (error) {
      const prefix = error?.code === 'VERIFY_EXTERNALLY' ? 'VERIFY_EXTERNALLY' : 'Fail closed';
      setStatus(`${prefix}: ${String(error?.message || error)}.`);
      window.dispatchEvent(new CustomEvent('stegverse:coinbase-skap-ingress-submission-failed', {
        detail: { decision: prefix, blind_retry_allowed: false }
      }));
    } finally {
      packet = null;
    }
  });

  window.StegFinCoinbaseSkapSubmission = Object.freeze({ loadSubmissionConfig, validateCiphertextOnlyPacket, validateAdmissionResponse, submitCiphertext });
})();
