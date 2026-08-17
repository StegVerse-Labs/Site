(() => {
  'use strict';

  const STORAGE_KEY = 'stegverse.stegid.wallet-capability.v1';
  const WALLET_HANDOFF_KEY = 'stegverse.stegfin.wallet-handoff-ready.v1';
  const ADMISSION_DB_NAME = 'stegverse-stegid-device-wallet-v1';
  const ADMISSION_STORE = 'state';
  const ADMISSION_KEY = 'latest-admission';
  const DIRECT_DB_NAME = 'stegverse-stegfin-phone-v2';
  const DIRECT_DB_STORE = 'state';
  const DIRECT_TERMINAL_KEY = 'latest-terminal';
  const WALLET = '0xA503DCe5471492bbA2D06e9f78F4d9D6Bcc852aA'.toLowerCase();
  const SCHEMA = 'stegverse.stegid.wallet_capability_decision.v1';
  const EVIDENCE_SCHEMA = 'stegverse.stegid.sanitized_admission_evidence.v1';
  const MAX_CLOCK_SKEW_MS = 5 * 60 * 1000;
  const MIN_PREPARE_VALIDITY_MS = 5 * 60 * 1000;
  const protectedKey = /^(authorization|bearer|bearer_token|token|api_key|apikey|provider_key|provider_api_key|github_token|gh_token|password|private_key|seed|seed_phrase|mnemonic|credential|credentials|secret|secret_value)$/i;

  function stable(value) {
    if (value === null || typeof value !== 'object') return JSON.stringify(value);
    if (Array.isArray(value)) return `[${value.map(stable).join(',')}]`;
    return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${stable(value[key])}`).join(',')}}`;
  }

  function hex(buffer) {
    return [...new Uint8Array(buffer)].map((byte) => byte.toString(16).padStart(2, '0')).join('');
  }

  async function sha256(value) {
    return `sha256:${hex(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(stable(value))))}`;
  }

  function rejectProtected(value, path = 'capability') {
    if (Array.isArray(value)) {
      value.forEach((child, index) => rejectProtected(child, `${path}[${index}]`));
      return;
    }
    if (value && typeof value === 'object') {
      for (const [key, child] of Object.entries(value)) {
        if (protectedKey.test(String(key).replace(/-/g, '_'))) throw new Error(`protected credential field prohibited: ${path}.${key}`);
        rejectProtected(child, `${path}.${key}`);
      }
    }
  }

  function parseTime(value, label) {
    const parsed = Date.parse(String(value || ''));
    if (!Number.isFinite(parsed)) throw new Error(`${label} timestamp missing or invalid`);
    return parsed;
  }

  function assertFreshReceipt(receipt, label, now = Date.now(), minimumRemainingMs = 0) {
    const issuedAt = parseTime(receipt?.issued_at, `${label} issued_at`);
    const expiresAt = parseTime(receipt?.expires_at, `${label} expires_at`);
    if (expiresAt <= issuedAt) throw new Error(`${label} freshness window invalid`);
    if (issuedAt > now + MAX_CLOCK_SKEW_MS) throw new Error(`${label} issued_at is implausibly future-dated`);
    if (expiresAt <= now + minimumRemainingMs) throw new Error(`${label} expired or expires too soon; current-device verification is required`);
    return receipt;
  }

  function capabilityRequiresRenewal(raw) {
    if (!raw) return true;
    try {
      const receipt = JSON.parse(raw);
      assertFreshReceipt(receipt, 'StegID wallet capability', Date.now(), MIN_PREPARE_VALIDITY_MS);
      return false;
    } catch {
      return true;
    }
  }

  function openDb(name, store, createIfMissing = false) {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(name, 1);
      request.onupgradeneeded = () => {
        if (createIfMissing && !request.result.objectStoreNames.contains(store)) request.result.createObjectStore(store);
      };
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error || new Error(`${name} database unavailable`));
    });
  }

  async function readLatestAdmission() {
    const db = await openDb(ADMISSION_DB_NAME, ADMISSION_STORE);
    try {
      return await new Promise((resolve, reject) => {
        if (!db.objectStoreNames.contains(ADMISSION_STORE)) {
          reject(new Error('StegID admission evidence store unavailable'));
          return;
        }
        const request = db.transaction(ADMISSION_STORE, 'readonly').objectStore(ADMISSION_STORE).get(ADMISSION_KEY);
        request.onsuccess = () => resolve(request.result || null);
        request.onerror = () => reject(request.error || new Error('StegID latest admission evidence unavailable'));
      });
    } finally {
      db.close();
    }
  }

  async function deleteDirectTerminal() {
    const db = await openDb(DIRECT_DB_NAME, DIRECT_DB_STORE, true);
    try {
      await new Promise((resolve, reject) => {
        const tx = db.transaction(DIRECT_DB_STORE, 'readwrite');
        tx.objectStore(DIRECT_DB_STORE).delete(DIRECT_TERMINAL_KEY);
        tx.oncomplete = resolve;
        tx.onerror = () => reject(tx.error || new Error('direct terminal deletion failed'));
        tx.onabort = () => reject(tx.error || new Error('direct terminal deletion aborted'));
      });
    } finally {
      db.close();
    }
  }

  async function persistIdentityBoundTerminal(result) {
    const db = await openDb(DIRECT_DB_NAME, DIRECT_DB_STORE, true);
    try {
      await new Promise((resolve, reject) => {
        const tx = db.transaction(DIRECT_DB_STORE, 'readwrite');
        tx.objectStore(DIRECT_DB_STORE).put(result, DIRECT_TERMINAL_KEY);
        tx.oncomplete = resolve;
        tx.onerror = () => reject(tx.error || new Error('identity-bound terminal persistence failed'));
        tx.onabort = () => reject(tx.error || new Error('identity-bound terminal persistence aborted'));
      });
    } finally {
      db.close();
    }
  }

  function pick(source, keys) {
    const out = {};
    for (const key of keys) {
      if (Object.prototype.hasOwnProperty.call(source || {}, key)) out[key] = source[key];
    }
    return out;
  }

  async function sanitizedAdmissionEvidence(capability) {
    const packet = await readLatestAdmission();
    if (!packet?.identity_receipt || !packet?.device_admission_receipt || !packet?.wallet_capability_request || !packet?.wallet_capability_decision) {
      throw new Error('StegID latest-admission packet incomplete');
    }
    if (packet.wallet_capability_decision.receipt_sha256 !== capability.receipt_sha256) {
      throw new Error('StegID latest-admission capability commitment mismatch');
    }
    if (packet.wallet_capability_decision.identity_id !== capability.identity_id || packet.wallet_capability_decision.device_id !== capability.device_id) {
      throw new Error('StegID latest-admission identity/device mismatch');
    }

    const evidence = {
      schema: EVIDENCE_SCHEMA,
      identity_continuity: pick(packet.identity_receipt, [
        'schema', 'decision', 'identity_id', 'continuity_basis', 'human_verification_sha256', 'revoked',
        'credential_authority', 'credential_requirement', 'non_tv_tvc_secret_or_token_used', 'issued_at', 'expires_at', 'receipt_sha256'
      ]),
      device_admission: pick(packet.device_admission_receipt, [
        'schema', 'decision', 'identity_id', 'device_id', 'validation_steps', 'device_possession_proof_sha256',
        'human_continuity_proof_sha256', 'revoked', 'credential_authority', 'credential_requirement',
        'non_tv_tvc_secret_or_token_used', 'issued_at', 'expires_at', 'receipt_sha256'
      ]),
      wallet_capability: pick(packet.wallet_capability_decision, [
        'schema', 'decision', 'identity_id', 'device_id', 'wallet_id', 'wallet_address', 'requested_capabilities',
        'granted_capabilities', 'identity_receipt_sha256', 'device_admission_receipt_sha256', 'request_sha256',
        'credential_authority', 'credential_requirement', 'non_tv_tvc_secret_or_token_used', 'wallet_secret_exported',
        'private_key_present', 'seed_present', 'automatic_signing', 'automatic_broadcast', 'device_specific_authority',
        'identity_continuity_is_not_wallet_authority', 'issued_at', 'expires_at', 'receipt_sha256'
      ])
    };

    rejectProtected(evidence, 'sanitized_admission_evidence');
    if (evidence.identity_continuity.decision !== 'IDENTITY_CONTINUITY_VALID') throw new Error('StegID identity continuity evidence not valid');
    if (evidence.device_admission.decision !== 'DEVICE_ADMITTED') throw new Error('StegID device admission evidence not admitted');
    if (evidence.wallet_capability.decision !== 'ALLOW_DEVICE_WALLET_CAPABILITY') throw new Error('StegID wallet capability evidence not admitted');
    if (evidence.identity_continuity.revoked !== false || evidence.device_admission.revoked !== false) throw new Error('revoked StegID evidence prohibited');
    if (evidence.wallet_capability.identity_receipt_sha256 !== evidence.identity_continuity.receipt_sha256) {
      throw new Error('StegID identity receipt linkage mismatch');
    }
    if (evidence.wallet_capability.device_admission_receipt_sha256 !== evidence.device_admission.receipt_sha256) {
      throw new Error('StegID device receipt linkage mismatch');
    }

    assertFreshReceipt(evidence.identity_continuity, 'StegID identity continuity', Date.now(), MIN_PREPARE_VALIDITY_MS);
    assertFreshReceipt(evidence.device_admission, 'StegID device admission', Date.now(), MIN_PREPARE_VALIDITY_MS);
    assertFreshReceipt(evidence.wallet_capability, 'StegID wallet capability', Date.now(), MIN_PREPARE_VALIDITY_MS);

    const steps = evidence.device_admission.validation_steps || [];
    for (const required of ['DEVICE_POSSESSION', 'HUMAN_CONTINUITY', 'IDENTITY_CONTINUITY']) {
      if (!steps.includes(required)) throw new Error(`StegID device admission missing ${required}`);
    }
    if (!Array.isArray(evidence.wallet_capability.granted_capabilities) || !evidence.wallet_capability.granted_capabilities.includes('PREPARE')) {
      throw new Error('StegID sanitized evidence missing PREPARE grant');
    }
    if (evidence.wallet_capability.granted_capabilities.includes('SIGN') || evidence.wallet_capability.granted_capabilities.includes('BROADCAST')) {
      throw new Error('StegID sanitized evidence may not grant SIGN/BROADCAST');
    }
    evidence.evidence_sha256 = await sha256(evidence);
    return evidence;
  }

  async function clearStalePhoneState() {
    localStorage.removeItem(STORAGE_KEY);
    localStorage.removeItem(WALLET_HANDOFF_KEY);
    await deleteDirectTerminal();
  }

  async function ensureCapabilityPresent() {
    let raw = localStorage.getItem(STORAGE_KEY);
    if (!capabilityRequiresRenewal(raw)) return raw;

    await clearStalePhoneState();

    const bootstrap = window.StegIDDeviceWalletBootstrap;
    if (!bootstrap || typeof bootstrap.issueCurrentPhonePrepareCapability !== 'function') {
      throw new Error('StegID current-phone bootstrap unavailable');
    }
    await bootstrap.issueCurrentPhonePrepareCapability();
    raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) throw new Error('StegID current-phone bootstrap produced no wallet capability');
    if (capabilityRequiresRenewal(raw)) throw new Error('StegID current-phone bootstrap produced stale wallet capability');
    return raw;
  }

  async function loadCapability() {
    const raw = await ensureCapabilityPresent();
    let receipt;
    try {
      receipt = JSON.parse(raw);
    } catch {
      throw new Error('StegID device wallet capability is malformed');
    }
    rejectProtected(receipt);
    if (receipt.schema !== SCHEMA) throw new Error('unexpected StegID wallet capability schema');
    if (receipt.decision !== 'ALLOW_DEVICE_WALLET_CAPABILITY') throw new Error(`StegID wallet capability not admitted: ${receipt.decision || 'UNKNOWN'}`);
    if (receipt.credential_authority !== 'TV/TVC') throw new Error('StegID wallet capability credential authority drift');
    if (receipt.credential_requirement !== 'NONE') throw new Error('current-phone StegID capability must require no credential');
    if (receipt.non_tv_tvc_secret_or_token_used !== false) throw new Error('non-TV/TVC credential use prohibited');
    if (receipt.wallet_secret_exported !== false || receipt.private_key_present !== false || receipt.seed_present !== false) {
      throw new Error('StegID wallet capability secret boundary drift');
    }
    if (receipt.automatic_signing !== false || receipt.automatic_broadcast !== false) {
      throw new Error('StegID wallet capability execution authority drift');
    }
    if (String(receipt.wallet_id || '').toLowerCase() !== 'stegwallet:primary' && String(receipt.wallet_address || '').toLowerCase() !== WALLET) {
      throw new Error('StegID wallet capability wallet mismatch');
    }
    if (!Array.isArray(receipt.granted_capabilities) || !receipt.granted_capabilities.includes('PREPARE')) {
      throw new Error('StegID PREPARE capability required');
    }
    if (receipt.granted_capabilities.includes('SIGN') || receipt.granted_capabilities.includes('BROADCAST')) {
      throw new Error('current-phone bootstrap may not grant SIGN/BROADCAST');
    }
    if (!receipt.identity_id || !receipt.device_id) throw new Error('StegID identity/device binding required');
    if (receipt.device_specific_authority !== true || receipt.identity_continuity_is_not_wallet_authority !== true) {
      throw new Error('StegID capability separation invariant missing');
    }
    const supplied = receipt.receipt_sha256;
    const material = { ...receipt };
    delete material.receipt_sha256;
    if (supplied !== await sha256(material)) throw new Error('StegID wallet capability receipt commitment mismatch');
    assertFreshReceipt(receipt, 'StegID wallet capability', Date.now(), MIN_PREPARE_VALIDITY_MS);
    return receipt;
  }

  const carrier = window.StegFinDirectRoute;
  if (!carrier || typeof carrier.run !== 'function') throw new Error('TV/TVC-admitted StegVerse direct carrier unavailable');

  async function runIdentityBound() {
    const capability = await loadCapability();
    const admissionEvidence = await sanitizedAdmissionEvidence(capability);
    let result;
    try {
      result = await carrier.run();
      if (!result?.receipt || result.receipt.state !== 'WALLET_HANDOFF_READY') return result;

      assertFreshReceipt(capability, 'StegID wallet capability', Date.now(), MIN_PREPARE_VALIDITY_MS);
      assertFreshReceipt(admissionEvidence.identity_continuity, 'StegID identity continuity', Date.now(), MIN_PREPARE_VALIDITY_MS);
      assertFreshReceipt(admissionEvidence.device_admission, 'StegID device admission', Date.now(), MIN_PREPARE_VALIDITY_MS);
      assertFreshReceipt(admissionEvidence.wallet_capability, 'StegID wallet capability evidence', Date.now(), MIN_PREPARE_VALIDITY_MS);

      result.receipt.stegid_identity_id = capability.identity_id;
      result.receipt.stegid_device_id = capability.device_id;
      result.receipt.stegid_wallet_capability_receipt_sha256 = capability.receipt_sha256;
      result.receipt.stegid_admission_evidence = admissionEvidence;
      result.receipt.identity_continuity_is_not_wallet_authority = true;
      result.receipt.selected_carrier = 'STEGVERSE_DIRECT_ONCHAIN';
      const material = { ...result.receipt };
      delete material.receipt_sha256;
      result.receipt.receipt_sha256 = await sha256(material);

      await persistIdentityBoundTerminal(result);
      localStorage.setItem(WALLET_HANDOFF_KEY, JSON.stringify(result));
      return result;
    } catch (error) {
      await deleteDirectTerminal();
      localStorage.removeItem(WALLET_HANDOFF_KEY);
      throw error;
    }
  }

  window.StegFinPhoneContinuity = Object.freeze({
    ...carrier,
    run: runIdentityBound,
    requireDeviceWalletCapability: loadCapability,
    readSanitizedAdmissionEvidence: async () => sanitizedAdmissionEvidence(await loadCapability())
  });
})();
