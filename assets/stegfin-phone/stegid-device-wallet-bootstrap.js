(() => {
  'use strict';

  const DB = 'stegverse-stegid-device-wallet-v1';
  const STORE = 'state';
  const CAP = 'stegverse.stegid.wallet-capability.v1';
  const WALLET_ID = 'stegwallet:primary';
  const WALLET = '0xA503DCe5471492bbA2D06e9f78F4d9D6Bcc852aA';
  const TTL = 60 * 60 * 1000;

  function stable(value) {
    if (value === null || typeof value !== 'object') return JSON.stringify(value);
    if (Array.isArray(value)) return `[${value.map(stable).join(',')}]`;
    return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${stable(value[key])}`).join(',')}}`;
  }

  function hex(buffer) {
    return [...new Uint8Array(buffer)].map((value) => value.toString(16).padStart(2, '0')).join('');
  }

  function b64url(buffer) {
    let value = '';
    for (const byte of new Uint8Array(buffer)) value += String.fromCharCode(byte);
    return btoa(value).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/g, '');
  }

  async function sha(value) {
    return `sha256:${hex(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(stable(value))))}`;
  }

  function rand(size = 32) {
    const value = new Uint8Array(size);
    crypto.getRandomValues(value);
    return value;
  }

  function openDb() {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(DB, 1);
      request.onupgradeneeded = () => {
        if (!request.result.objectStoreNames.contains(STORE)) request.result.createObjectStore(STORE);
      };
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error || new Error('stegid_db_open_failed'));
    });
  }

  async function get(key) {
    const db = await openDb();
    try {
      return await new Promise((resolve, reject) => {
        const request = db.transaction(STORE, 'readonly').objectStore(STORE).get(key);
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
      });
    } finally {
      db.close();
    }
  }

  async function put(key, value) {
    const db = await openDb();
    try {
      await new Promise((resolve, reject) => {
        const tx = db.transaction(STORE, 'readwrite');
        tx.objectStore(STORE).put(value, key);
        tx.oncomplete = resolve;
        tx.onerror = () => reject(tx.error);
        tx.onabort = () => reject(tx.error);
      });
    } finally {
      db.close();
    }
  }

  async function deviceKey() {
    const prior = await get('device-key');
    if (prior?.privateKey && prior?.publicKey && prior?.publicJwk) return prior;
    const pair = await crypto.subtle.generateKey({ name: 'ECDSA', namedCurve: 'P-256' }, false, ['sign', 'verify']);
    const publicJwk = await crypto.subtle.exportKey('jwk', pair.publicKey);
    const record = { privateKey: pair.privateKey, publicKey: pair.publicKey, publicJwk };
    await put('device-key', record);
    return record;
  }

  async function possession(key) {
    const challenge = rand();
    const signature = await crypto.subtle.sign({ name: 'ECDSA', hash: 'SHA-256' }, key.privateKey, challenge);
    if (!await crypto.subtle.verify({ name: 'ECDSA', hash: 'SHA-256' }, key.publicKey, signature, challenge)) {
      throw new Error('DEVICE_POSSESSION failed');
    }
    return {
      challenge_sha256: await sha({ challenge: b64url(challenge) }),
      signature_sha256: await sha({ signature: b64url(signature) }),
      device_public_jwk_sha256: await sha(key.publicJwk)
    };
  }

  async function human() {
    if (!window.PublicKeyCredential || !navigator.credentials) throw new Error('platform WebAuthn required for HUMAN_CONTINUITY');
    if (!await PublicKeyCredential.isUserVerifyingPlatformAuthenticatorAvailable()) {
      throw new Error('user-verifying platform authenticator unavailable');
    }

    let record = await get('webauthn');
    if (!record?.rawId) {
      const userId = rand();
      const created = await navigator.credentials.create({
        publicKey: {
          challenge: rand(),
          rp: { name: 'StegVerse' },
          user: {
            id: userId,
            name: `stegverse-${b64url(userId).slice(0, 16)}`,
            displayName: 'StegVerse Identity'
          },
          pubKeyCredParams: [{ type: 'public-key', alg: -7 }, { type: 'public-key', alg: -257 }],
          authenticatorSelection: {
            authenticatorAttachment: 'platform',
            residentKey: 'required',
            userVerification: 'required'
          },
          timeout: 60000,
          attestation: 'none'
        }
      });
      if (!created || created.type !== 'public-key') throw new Error('WebAuthn creation failed');
      record = { rawId: b64url(created.rawId), created_at: new Date().toISOString() };
      await put('webauthn', record);
    }

    const raw = Uint8Array.from(
      atob(record.rawId.replace(/-/g, '+').replace(/_/g, '/').padEnd(Math.ceil(record.rawId.length / 4) * 4, '=')),
      (char) => char.charCodeAt(0)
    );
    const assertion = await navigator.credentials.get({
      publicKey: {
        challenge: rand(),
        allowCredentials: [{ type: 'public-key', id: raw }],
        userVerification: 'required',
        timeout: 60000
      }
    });
    if (!assertion || assertion.type !== 'public-key') throw new Error('HUMAN_CONTINUITY WebAuthn assertion failed');
    return {
      webauthn_credential_id_sha256: await sha({ raw_id: record.rawId }),
      user_verification: 'required'
    };
  }

  async function issueCurrentPhonePrepareCapability() {
    const key = await deviceKey();
    const possessionProof = await possession(key);
    const humanProof = await human();
    const now = new Date();
    const expires = new Date(now.getTime() + TTL);
    const issuedAt = now.toISOString();
    const expiresAt = expires.toISOString();
    const identityId = `stegid:${(await sha({ type: 'STEGVERSE_IDENTITY_GENESIS', webauthn: humanProof.webauthn_credential_id_sha256 })).split(':')[1]}`;
    const deviceId = `stegdevice:${possessionProof.device_public_jwk_sha256.split(':')[1]}`;

    const identityReceipt = {
      schema: 'stegverse.stegid.identity_continuity_receipt.v1',
      decision: 'IDENTITY_CONTINUITY_VALID',
      identity_id: identityId,
      continuity_basis: 'GENESIS_PRIMARY_DEVICE_USER_VERIFIED',
      human_verification_sha256: humanProof.webauthn_credential_id_sha256,
      revoked: false,
      credential_authority: 'TV/TVC',
      credential_requirement: 'NONE',
      non_tv_tvc_secret_or_token_used: false,
      issued_at: issuedAt,
      expires_at: expiresAt
    };
    identityReceipt.receipt_sha256 = await sha(identityReceipt);

    const deviceReceipt = {
      schema: 'stegverse.stegid.device_admission_receipt.v1',
      decision: 'DEVICE_ADMITTED',
      identity_id: identityId,
      device_id: deviceId,
      validation_steps: ['DEVICE_POSSESSION', 'HUMAN_CONTINUITY', 'IDENTITY_CONTINUITY'],
      device_possession_proof_sha256: await sha(possessionProof),
      human_continuity_proof_sha256: await sha(humanProof),
      revoked: false,
      credential_authority: 'TV/TVC',
      credential_requirement: 'NONE',
      non_tv_tvc_secret_or_token_used: false,
      issued_at: issuedAt,
      expires_at: expiresAt
    };
    deviceReceipt.receipt_sha256 = await sha(deviceReceipt);

    const request = {
      schema: 'stegverse.stegid.wallet_capability_request.v1',
      identity_id: identityId,
      device_id: deviceId,
      wallet_id: WALLET_ID,
      wallet_address: WALLET,
      requested_capabilities: ['OBSERVE', 'PREPARE'],
      explicit_user_presence: true,
      credential_authority: 'TV/TVC',
      credential_requirement: 'NONE',
      non_tv_tvc_secret_or_token_used: false,
      private_key_requested: false,
      seed_requested: false
    };

    const decision = {
      schema: 'stegverse.stegid.wallet_capability_decision.v1',
      decision: 'ALLOW_DEVICE_WALLET_CAPABILITY',
      identity_id: identityId,
      device_id: deviceId,
      wallet_id: WALLET_ID,
      wallet_address: WALLET,
      requested_capabilities: ['OBSERVE', 'PREPARE'],
      granted_capabilities: ['OBSERVE', 'PREPARE'],
      identity_receipt_sha256: identityReceipt.receipt_sha256,
      device_admission_receipt_sha256: deviceReceipt.receipt_sha256,
      request_sha256: await sha(request),
      credential_authority: 'TV/TVC',
      credential_requirement: 'NONE',
      non_tv_tvc_secret_or_token_used: false,
      wallet_secret_exported: false,
      private_key_present: false,
      seed_present: false,
      automatic_signing: false,
      automatic_broadcast: false,
      device_specific_authority: true,
      identity_continuity_is_not_wallet_authority: true,
      issued_at: issuedAt,
      expires_at: expiresAt
    };
    decision.receipt_sha256 = await sha(decision);

    const packet = {
      identity_receipt: identityReceipt,
      device_admission_receipt: deviceReceipt,
      wallet_capability_request: request,
      wallet_capability_decision: decision
    };
    await put('latest-admission', packet);
    localStorage.setItem(CAP, JSON.stringify(decision));
    return packet;
  }

  window.StegIDDeviceWalletBootstrap = Object.freeze({ issueCurrentPhonePrepareCapability });
})();
