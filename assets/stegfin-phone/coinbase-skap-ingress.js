(() => {
  'use strict';

  const FORMAT = 'stegverse.skap.browser_ingress/p256-ecdh-hkdf-sha256-aes256gcm/v1';
  const ENDPOINT = 'https://api.coinbase.com';
  const CONFIG_URL = './assets/stegfin-phone/coinbase-skap-ingress-config.json';
  const ROUTE_URL = './assets/stegfin-phone/coinbase-skap-intr-route.json';
  const PURPOSE = 'coinbase.permission_observation';
  const ROUTE_SCHEMA = 'stegverse.tvc.skap_browser_intr_route/v1';
  const ROUTE_CARRIER = 'ZERO_CREDENTIAL_ROTATING_HTTPS_TUNNEL';
  const ROUTE_PATH = '/v1/skap/coinbase/ingress';
  const encoder = new TextEncoder();

  function stable(value) {
    if (value === null || typeof value !== 'object') return JSON.stringify(value);
    if (Array.isArray(value)) return `[${value.map(stable).join(',')}]`;
    return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${stable(value[key])}`).join(',')}}`;
  }

  function b64url(buffer) {
    let value = '';
    for (const byte of new Uint8Array(buffer)) value += String.fromCharCode(byte);
    return btoa(value).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/g, '');
  }

  function hex(buffer) {
    return [...new Uint8Array(buffer)].map((value) => value.toString(16).padStart(2, '0')).join('');
  }

  async function sha256(value) {
    return `sha256:${hex(await crypto.subtle.digest('SHA-256', encoder.encode(stable(value))))}`;
  }

  function wipe(view) {
    if (view?.fill) view.fill(0);
  }

  async function loadConfig() {
    if (!window.isSecureContext || !crypto?.subtle) throw new Error('secure WebCrypto context required');
    const response = await fetch(CONFIG_URL, { cache: 'no-store', redirect: 'error', credentials: 'same-origin' });
    if (!response.ok) throw new Error(`SKAP ingress config unavailable (${response.status})`);
    const config = await response.json();
    if (config?.schema !== 'stegverse.site.coinbase_skap_ingress_config/v1') throw new Error('SKAP ingress config schema invalid');
    if (config?.status !== 'PROVISIONED') throw new Error('SKAP ingress key is not provisioned');
    if (config?.endpoint_origin !== ENDPOINT) throw new Error('SKAP ingress endpoint binding invalid');
    if (config?.credential_authority !== 'TV/TVC' || config?.credential_custody_target !== 'SKAP' || config?.transport_protocol !== 'InTr') throw new Error('SKAP ingress authority/transport binding invalid');
    if (config?.physical_execution_surface !== 'CURRENT_USER_IPHONE' || config?.second_machine_required !== false) throw new Error('SKAP ingress physical execution boundary invalid');
    if (config?.device_durable_secret_custody !== false || config?.kv_secret_resolution_authority !== false || config?.github_environment_secret_access !== false || config?.private_key_present !== false || config?.authority_transfer !== false) throw new Error('SKAP ingress secret authority boundary invalid');
    if (config?.private_key_liveness_required !== true || !config?.runtime_instance_id || !config?.lease_expires_at) throw new Error('SKAP ingress resident liveness binding missing');
    const lease = Date.parse(config.lease_expires_at);
    if (!Number.isFinite(lease) || lease <= Date.now()) throw new Error('SKAP ingress recipient key lease expired');
    if (!String(config?.activation_receipt_hash || '').startsWith('sha256:') || !String(config?.liveness_receipt_hash || '').startsWith('sha256:')) throw new Error('SKAP ingress activation/liveness receipt binding missing');
    if (config?.recipient_public_jwk?.kty !== 'EC' || config?.recipient_public_jwk?.crv !== 'P-256') throw new Error('SKAP ingress public key invalid');
    if ('d' in config.recipient_public_jwk) throw new Error('SKAP ingress config must contain public key only');
    if (!String(config?.recipient_key_id || '').startsWith('tvc://skap/browser-ingress/coinbase/')) throw new Error('SKAP ingress key authority invalid');
    if (config?.recipient_public_jwk_sha256 !== await sha256(config.recipient_public_jwk)) throw new Error('SKAP ingress public key hash mismatch');
    if (!Number.isInteger(config?.credential_version) || config.credential_version < 1 || !config?.wrapping_policy_ref) throw new Error('SKAP ingress credential binding incomplete');
    return config;
  }

  async function loadRoute(config) {
    const response = await fetch(ROUTE_URL, { cache: 'no-store', redirect: 'error', credentials: 'same-origin' });
    if (!response.ok) throw new Error(`SKAP InTr route unavailable (${response.status})`);
    const route = await response.json();
    if (route?.schema !== ROUTE_SCHEMA || route?.status !== 'ROUTE_LIVE') throw new Error('SKAP InTr route is not live');
    if (route?.transport_protocol !== 'InTr' || route?.carrier !== ROUTE_CARRIER) throw new Error('SKAP InTr carrier binding invalid');
    if (route?.credential_authority !== 'TV/TVC' || route?.credential_custody_target !== 'SKAP') throw new Error('SKAP InTr route authority binding invalid');
    if (route?.public_route_authority !== false || route?.provider_operation_authorized !== false || route?.credential_plaintext_carried !== false || route?.github_token_runtime_authority !== false || route?.github_actions_resident_authority !== false) throw new Error('SKAP InTr route authority boundary invalid');
    if (route?.runtime_instance_id !== config.runtime_instance_id || route?.recipient_key_id !== config.recipient_key_id) throw new Error('SKAP InTr recipient runtime mismatch');
    if (route?.activation_receipt_hash !== config.activation_receipt_hash || route?.liveness_receipt_hash !== config.liveness_receipt_hash) throw new Error('SKAP InTr activation/liveness mismatch');
    if (route?.lease_expires_at !== config.lease_expires_at) throw new Error('SKAP InTr lease mismatch');
    const lease = Date.parse(route.lease_expires_at);
    if (!Number.isFinite(lease) || lease <= Date.now()) throw new Error('SKAP InTr route lease expired');
    const origin = new URL(route.public_origin);
    if (origin.protocol !== 'https:' || origin.username || origin.password || origin.port || origin.pathname !== '/' || origin.search || origin.hash || !origin.hostname.endsWith('.trycloudflare.com')) throw new Error('SKAP InTr public origin invalid');
    const expectedIngress = `${origin.origin}${ROUTE_PATH}`;
    if (route.public_ingress_url !== expectedIngress) throw new Error('SKAP InTr ingress URL binding invalid');
    if (route.health_url !== `${origin.origin}/health`) throw new Error('SKAP InTr health URL binding invalid');
    if (!String(route?.route_receipt_hash || '').startsWith('sha256:')) throw new Error('SKAP InTr route receipt binding missing');
    return route;
  }

  async function ownerAuthorization() {
    const bootstrap = window.StegIDDeviceWalletBootstrap;
    if (!bootstrap?.issueCurrentPhonePrepareCapability) throw new Error('StegID phone authorization surface unavailable');
    const packet = await bootstrap.issueCurrentPhonePrepareCapability();
    const identity = packet?.identity_receipt;
    const device = packet?.device_admission_receipt;
    if (identity?.decision !== 'IDENTITY_CONTINUITY_VALID' || device?.decision !== 'DEVICE_ADMITTED') throw new Error('owner/device authorization not admitted');
    if (identity?.credential_authority !== 'TV/TVC' || device?.credential_authority !== 'TV/TVC') throw new Error('credential authority boundary invalid');
    return { method: 'WEBAUTHN', rp_id: location.hostname === 'www.stegverse.org' ? 'stegverse.org' : location.hostname, assertion_digest: device.human_continuity_proof_sha256, device_admission_digest: device.receipt_sha256, identity_continuity_digest: identity.receipt_sha256, user_verification: 'REQUIRED', verified: true };
  }

  async function deriveAesKey(ephemeralPrivateKey, recipientPublicKey, salt, aadBytes) {
    const sharedBits = await crypto.subtle.deriveBits({ name: 'ECDH', public: recipientPublicKey }, ephemeralPrivateKey, 256);
    const shared = new Uint8Array(sharedBits);
    try {
      const hkdfBase = await crypto.subtle.importKey('raw', shared, 'HKDF', false, ['deriveKey']);
      const aadDigest = new Uint8Array(await crypto.subtle.digest('SHA-256', aadBytes));
      const prefix = encoder.encode('stegverse-skap-browser-ingress-v1\u0000');
      const info = new Uint8Array(prefix.length + aadDigest.length); info.set(prefix, 0); info.set(aadDigest, prefix.length);
      try { return await crypto.subtle.deriveKey({ name: 'HKDF', hash: 'SHA-256', salt, info }, hkdfBase, { name: 'AES-GCM', length: 256 }, false, ['encrypt']); }
      finally { wipe(aadDigest); wipe(info); }
    } finally { wipe(shared); }
  }

  async function sealCredentialBytes(credentialBytes, config, owner) {
    if (!(credentialBytes instanceof Uint8Array) || credentialBytes.length === 0) throw new Error('credential bytes required');
    if (Date.parse(config.lease_expires_at) <= Date.now()) { wipe(credentialBytes); throw new Error('SKAP ingress recipient key lease expired before sealing'); }
    const objectId = `skap://APIs/coinbase/owner/${config.credential_version}`;
    const context = { credential_version: config.credential_version, endpoint_ref: ENDPOINT, object_id: objectId, purpose: PURPOSE, recipient_key_id: config.recipient_key_id, wrapping_policy_ref: config.wrapping_policy_ref };
    const aad = encoder.encode(stable(context));
    const recipientPublicKey = await crypto.subtle.importKey('jwk', config.recipient_public_jwk, { name: 'ECDH', namedCurve: 'P-256' }, false, []);
    const ephemeral = await crypto.subtle.generateKey({ name: 'ECDH', namedCurve: 'P-256' }, true, ['deriveBits']);
    const ephemeralPublicJwk = await crypto.subtle.exportKey('jwk', ephemeral.publicKey); delete ephemeralPublicJwk.key_ops; delete ephemeralPublicJwk.ext; delete ephemeralPublicJwk.d;
    const salt = crypto.getRandomValues(new Uint8Array(32)); const nonce = crypto.getRandomValues(new Uint8Array(12));
    try {
      const aesKey = await deriveAesKey(ephemeral.privateKey, recipientPublicKey, salt, aad);
      const ciphertext = await crypto.subtle.encrypt({ name: 'AES-GCM', iv: nonce, additionalData: aad, tagLength: 128 }, aesKey, credentialBytes);
      const envelope = { format: FORMAT, ...context, ephemeral_public_jwk: ephemeralPublicJwk, kdf_salt_b64: b64url(salt), nonce_b64: b64url(nonce), aad_hash: `sha256:${hex(await crypto.subtle.digest('SHA-256', aad))}`, ciphertext_b64: b64url(ciphertext), plaintext_persisted: false, device_private_key_persisted: false, skap_private_key_exported: false, authority_transfer: false };
      const ingressBody = { schema: 'stegverse.tvc.coinbase_iphone_skap_ingress/v1', ingress_id: `coinbase-iphone-${crypto.randomUUID()}`, owner_authorization: owner, physical_execution_surface: 'CURRENT_USER_IPHONE', transport: 'STEGVERSE_BROWSER_CAPSULE', provider: 'coinbase_advanced', endpoint_origin: ENDPOINT, purpose: PURPOSE, credential_ref: objectId, credential_version: config.credential_version, recipient_runtime_instance_id: config.runtime_instance_id, recipient_lease_expires_at: config.lease_expires_at, sealed_material: envelope, plaintext_present: false, device_secret_custody_authority: false, kv_secret_resolution_authority: false, github_environment_secret_access: false, credential_authority: 'TV/TVC' };
      return { ...ingressBody, ingress_digest: await sha256(ingressBody) };
    } finally { wipe(credentialBytes); wipe(salt); wipe(nonce); wipe(aad); }
  }

  async function submitSealedCapsule(packet, config, route) {
    if (!packet?.sealed_material?.ciphertext_b64 || packet?.plaintext_present !== false) throw new Error('sealed SKAP capsule required');
    if (packet?.recipient_runtime_instance_id !== route.runtime_instance_id || packet?.recipient_lease_expires_at !== route.lease_expires_at) throw new Error('sealed capsule route binding mismatch');
    if (Date.parse(route.lease_expires_at) <= Date.now() || Date.parse(config.lease_expires_at) <= Date.now()) throw new Error('SKAP InTr lease expired before submission');
    let response;
    try {
      response = await fetch(route.public_ingress_url, {
        method: 'POST',
        mode: 'cors',
        credentials: 'omit',
        redirect: 'error',
        cache: 'no-store',
        referrerPolicy: 'no-referrer',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(packet),
      });
    } catch (_) {
      throw new Error('SKAP InTr submission state ambiguous; VERIFY_EXTERNALLY and do not retry this ingress_id');
    }
    let result;
    try { result = await response.json(); }
    catch (_) { throw new Error('SKAP InTr response invalid; VERIFY_EXTERNALLY and do not retry this ingress_id'); }
    if (response.status !== 201 || result?.schema !== 'stegverse.tvc.coinbase_browser_ingress_response/v2' || result?.decision !== 'ADMITTED') throw new Error(`SKAP InTr admission denied (${response.status})`);
    if (result?.ingress_id !== packet.ingress_id || result?.credential_ref !== packet.credential_ref || result?.credential_version !== packet.credential_version || result?.endpoint_origin !== ENDPOINT || result?.purpose !== PURPOSE) throw new Error('SKAP InTr admission response binding mismatch');
    if (result?.browser_ingress_digest !== await sha256(packet)) throw new Error('SKAP InTr browser digest mismatch');
    if (result?.browser_ciphertext_returned !== false || result?.credential_plaintext_returned !== false || result?.decryption_performed_at_ingress !== false || result?.rewrap_performed_at_ingress !== false || result?.endpoint_verification_required_before_decryption !== true) throw new Error('SKAP InTr admission secrecy invariant failed');
    if (result?.credential_authority !== 'TV/TVC' || result?.device_secret_custody_authority !== false || result?.kv_secret_resolution_authority !== false || result?.execution_authority !== 'NONE' || result?.may_authorize_order !== false || result?.retry_policy !== 'NEW_OWNER_AUTHORIZED_PACKET_REQUIRED') throw new Error('SKAP InTr admission authority invariant failed');
    return result;
  }

  async function sealCoinbaseCredential({ apiKeyName, apiPrivateKey }) {
    const config = await loadConfig(); const owner = await ownerAuthorization();
    const bundle = encoder.encode(stable({ api_key_name: apiKeyName, api_private_key: apiPrivateKey })); apiKeyName = ''; apiPrivateKey = '';
    return sealCredentialBytes(bundle, config, owner);
  }

  async function sealAndSubmitCoinbaseCredential({ apiKeyName, apiPrivateKey }) {
    const config = await loadConfig();
    const route = await loadRoute(config);
    const owner = await ownerAuthorization();
    const bundle = encoder.encode(stable({ api_key_name: apiKeyName, api_private_key: apiPrivateKey })); apiKeyName = ''; apiPrivateKey = '';
    const packet = await sealCredentialBytes(bundle, config, owner);
    return { packet, admission: await submitSealedCapsule(packet, config, route), route_receipt_hash: route.route_receipt_hash };
  }

  window.StegFinCoinbaseSkapIngress = Object.freeze({ loadConfig, loadRoute, ownerAuthorization, sealCredentialBytes, submitSealedCapsule, sealCoinbaseCredential, sealAndSubmitCoinbaseCredential });
})();
