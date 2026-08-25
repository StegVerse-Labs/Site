(() => {
  'use strict';

  const FORMAT = 'stegverse.skap.browser_ingress/p256-ecdh-hkdf-sha256-aes256gcm/v1';
  const ENDPOINT = 'https://api.coinbase.com';
  const CONFIG_URL = './assets/stegfin-phone/coinbase-skap-ingress-config.json';
  const PURPOSE = 'coinbase.permission_observation';
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
    if (config?.recipient_public_jwk?.kty !== 'EC' || config?.recipient_public_jwk?.crv !== 'P-256') throw new Error('SKAP ingress public key invalid');
    if ('d' in config.recipient_public_jwk) throw new Error('SKAP ingress config must contain public key only');
    if (!String(config?.recipient_key_id || '').startsWith('tvc://skap/browser-ingress/coinbase/')) throw new Error('SKAP ingress key authority invalid');
    return config;
  }

  async function ownerAuthorization() {
    const bootstrap = window.StegIDDeviceWalletBootstrap;
    if (!bootstrap?.issueCurrentPhonePrepareCapability) throw new Error('StegID phone authorization surface unavailable');
    const packet = await bootstrap.issueCurrentPhonePrepareCapability();
    const identity = packet?.identity_receipt;
    const device = packet?.device_admission_receipt;
    if (identity?.decision !== 'IDENTITY_CONTINUITY_VALID' || device?.decision !== 'DEVICE_ADMITTED') {
      throw new Error('owner/device authorization not admitted');
    }
    if (identity?.credential_authority !== 'TV/TVC' || device?.credential_authority !== 'TV/TVC') {
      throw new Error('credential authority boundary invalid');
    }
    return {
      method: 'WEBAUTHN',
      rp_id: location.hostname === 'www.stegverse.org' ? 'stegverse.org' : location.hostname,
      assertion_digest: device.human_continuity_proof_sha256,
      device_admission_digest: device.receipt_sha256,
      identity_continuity_digest: identity.receipt_sha256,
      user_verification: 'REQUIRED',
      verified: true
    };
  }

  async function deriveAesKey(ephemeralPrivateKey, recipientPublicKey, salt, aadBytes) {
    const sharedBits = await crypto.subtle.deriveBits({ name: 'ECDH', public: recipientPublicKey }, ephemeralPrivateKey, 256);
    const shared = new Uint8Array(sharedBits);
    try {
      const hkdfBase = await crypto.subtle.importKey('raw', shared, 'HKDF', false, ['deriveKey']);
      const aadDigest = new Uint8Array(await crypto.subtle.digest('SHA-256', aadBytes));
      const prefix = encoder.encode('stegverse-skap-browser-ingress-v1\u0000');
      const info = new Uint8Array(prefix.length + aadDigest.length);
      info.set(prefix, 0);
      info.set(aadDigest, prefix.length);
      try {
        return await crypto.subtle.deriveKey(
          { name: 'HKDF', hash: 'SHA-256', salt, info },
          hkdfBase,
          { name: 'AES-GCM', length: 256 },
          false,
          ['encrypt']
        );
      } finally {
        wipe(aadDigest);
        wipe(info);
      }
    } finally {
      wipe(shared);
    }
  }

  async function sealCredentialBytes(credentialBytes, config, owner) {
    if (!(credentialBytes instanceof Uint8Array) || credentialBytes.length === 0) throw new Error('credential bytes required');
    const objectId = `skap://APIs/coinbase/owner/${config.credential_version}`;
    const context = {
      credential_version: config.credential_version,
      endpoint_ref: ENDPOINT,
      object_id: objectId,
      purpose: PURPOSE,
      recipient_key_id: config.recipient_key_id,
      wrapping_policy_ref: config.wrapping_policy_ref
    };
    const aad = encoder.encode(stable(context));
    const recipientPublicKey = await crypto.subtle.importKey(
      'jwk',
      config.recipient_public_jwk,
      { name: 'ECDH', namedCurve: 'P-256' },
      false,
      []
    );
    // The one-operation ephemeral pair is generated exportable solely so its
    // public JWK can travel in the ciphertext envelope. The private key is never
    // exported, persisted or included in any receipt and becomes unreachable
    // after this function returns.
    const ephemeral = await crypto.subtle.generateKey({ name: 'ECDH', namedCurve: 'P-256' }, true, ['deriveBits']);
    const ephemeralPublicJwk = await crypto.subtle.exportKey('jwk', ephemeral.publicKey);
    delete ephemeralPublicJwk.key_ops;
    delete ephemeralPublicJwk.ext;
    delete ephemeralPublicJwk.d;
    const salt = crypto.getRandomValues(new Uint8Array(32));
    const nonce = crypto.getRandomValues(new Uint8Array(12));
    try {
      const aesKey = await deriveAesKey(ephemeral.privateKey, recipientPublicKey, salt, aad);
      const ciphertext = await crypto.subtle.encrypt({ name: 'AES-GCM', iv: nonce, additionalData: aad, tagLength: 128 }, aesKey, credentialBytes);
      const envelope = {
        format: FORMAT,
        ...context,
        ephemeral_public_jwk: ephemeralPublicJwk,
        kdf_salt_b64: b64url(salt),
        nonce_b64: b64url(nonce),
        aad_hash: `sha256:${hex(await crypto.subtle.digest('SHA-256', aad))}`,
        ciphertext_b64: b64url(ciphertext),
        plaintext_persisted: false,
        device_private_key_persisted: false,
        skap_private_key_exported: false,
        authority_transfer: false
      };
      const ingressBody = {
        schema: 'stegverse.tvc.coinbase_iphone_skap_ingress/v1',
        ingress_id: `coinbase-iphone-${crypto.randomUUID()}`,
        owner_authorization: owner,
        physical_execution_surface: 'CURRENT_USER_IPHONE',
        transport: 'STEGVERSE_BROWSER_CAPSULE',
        provider: 'coinbase_advanced',
        endpoint_origin: ENDPOINT,
        purpose: PURPOSE,
        credential_ref: objectId,
        credential_version: config.credential_version,
        sealed_material: envelope,
        plaintext_present: false,
        device_secret_custody_authority: false,
        kv_secret_resolution_authority: false,
        github_environment_secret_access: false,
        credential_authority: 'TV/TVC'
      };
      return { ...ingressBody, ingress_digest: await sha256(ingressBody) };
    } finally {
      wipe(credentialBytes);
      wipe(salt);
      wipe(nonce);
      wipe(aad);
    }
  }

  async function sealCoinbaseCredential({ apiKeyName, apiPrivateKey }) {
    const config = await loadConfig();
    const owner = await ownerAuthorization();
    // JavaScript strings are immutable and cannot be guaranteed overwritten. Convert
    // immediately, clear UI fields in the caller, and retain only mutable byte arrays.
    const bundle = encoder.encode(stable({ api_key_name: apiKeyName, api_private_key: apiPrivateKey }));
    apiKeyName = '';
    apiPrivateKey = '';
    return sealCredentialBytes(bundle, config, owner);
  }

  window.StegFinCoinbaseSkapIngress = Object.freeze({ loadConfig, ownerAuthorization, sealCredentialBytes, sealCoinbaseCredential });
})();
