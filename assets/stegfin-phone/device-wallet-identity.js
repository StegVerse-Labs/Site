(() => {
  'use strict';

  const STORAGE_KEY = 'stegverse.stegid.wallet-capability.v1';
  const ADMISSION_DB_NAME = 'stegverse-stegid-device-wallet-v1';
  const ADMISSION_STORE = 'state';
  const ADMISSION_KEY = 'latest-admission';
  const WALLET = '0xA503DCe5471492bbA2D06e9f78F4d9D6Bcc852aA'.toLowerCase();
  const SCHEMA = 'stegverse.stegid.wallet_capability_decision.v1';
  const EVIDENCE_SCHEMA = 'stegverse.stegid.sanitized_admission_evidence.v1';
  const protectedKey = /^(authorization|bearer|bearer_token|token|api_key|apikey|provider_key|provider_api_key|github_token|gh_token|password|private_key|seed|seed_phrase|mnemonic|credential|credentials|secret|secret_value)$/i;

  function stable(value) {
    if (value === null || typeof value !== 'object') return JSON.stringify(value);
    if (Array.isArray(value)) return `[${value.map(stable).join(',')}]`;
    return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${stable(value[key])}`).join(',')}}`;
  }
  function hex(buffer) { return [...new Uint8Array(buffer)].map((b) => b.toString(16).padStart(2, '0')).join(''); }
  async function sha256(value) { return `sha256:${hex(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(stable(value))))}`; }

  function rejectProtected(value, path = 'capability') {
    if (Array.isArray(value)) { value.forEach((child, index) => rejectProtected(child, `${path}[${index}]`)); return; }
    if (value && typeof value === 'object') {
      for (const [key, child] of Object.entries(value)) {
        if (protectedKey.test(String(key).replace(/-/g, '_'))) throw new Error(`protected credential field prohibited: ${path}.${key}`);
        rejectProtected(child, `${path}.${key}`);
      }
    }
  }

  function openAdmissionDb() {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(ADMISSION_DB_NAME, 1);
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error || new Error('StegID admission evidence database unavailable'));
    });
  }

  async function readLatestAdmission() {
    const db = await openAdmissionDb();
    try {
      return await new Promise((resolve, reject) => {
        const request = db.transaction(ADMISSION_STORE, 'readonly').objectStore(ADMISSION_STORE).get(ADMISSION_KEY);
        request.onsuccess = () => resolve(request.result || null);
        request.onerror = () => reject(request.error || new Error('StegID latest admission evidence unavailable'));
      });
    } finally {
      db.close();
    }
  }

  function pick(source, keys) {
    const out = {};
    for (const key of keys) if (Object.prototype.hasOwnProperty.call(source || {}, key)) out[key] = source[key];
    return out;
  }

  async function sanitizedAdmissionEvidence(capability) {
    const packet = await readLatestAdmission();
    if (!packet?.identity_receipt || !packet?.device_admission_receipt || !packet?.wallet_capability_request || !packet?.wallet_capability_decision) {
      throw new Error('StegID latest-admission packet incomplete');
    }
    if (packet.wallet_capability_decision.receipt_sha256 !== capability.receipt_sha256) throw new Error('StegID latest-admission capability commitment mismatch');
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
        'identity_continuity_is_not_wallet_authority', 'issued_at', 'receipt_sha256'
      ])
    };

    rejectProtected(evidence, 'sanitized_admission_evidence');
    if (evidence.identity_continuity.decision !== 'IDENTITY_CONTINUITY_VALID') throw new Error('StegID identity continuity evidence not valid');
    if (evidence.device_admission.decision !== 'DEVICE_ADMITTED') throw new Error('StegID device admission evidence not admitted');
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

  async function ensureCapabilityPresent() {
    let raw = localStorage.getItem(STORAGE_KEY);
    if (raw) return raw;
    const bootstrap = window.StegIDDeviceWalletBootstrap;
    if (!bootstrap || typeof bootstrap.issueCurrentPhonePrepareCapability !== 'function') throw new Error('StegID current-phone bootstrap unavailable');
    await bootstrap.issueCurrentPhonePrepareCapability();
    raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) throw new Error('StegID current-phone bootstrap produced no wallet capability');
    return raw;
  }

  async function loadCapability() {
    const raw = await ensureCapabilityPresent();
    let receipt;
    try { receipt = JSON.parse(raw); } catch { throw new Error('StegID device wallet capability is malformed'); }
    rejectProtected(receipt);
    if (receipt.schema !== SCHEMA) throw new Error('unexpected StegID wallet capability schema');
    if (receipt.decision !== 'ALLOW_DEVICE_WALLET_CAPABILITY') throw new Error(`StegID wallet capability not admitted: ${receipt.decision || 'UNKNOWN'}`);
    if (receipt.credential_authority !== 'TV/TVC') throw new Error('StegID wallet capability credential authority drift');
    if (receipt.credential_requirement !== 'NONE') throw new Error('current-phone StegID capability must require no credential');
    if (receipt.non_tv_tvc_secret_or_token_used !== false) throw new Error('non-TV/TVC credential use prohibited');
    if (receipt.wallet_secret_exported !== false || receipt.private_key_present !== false || receipt.seed_present !== false) throw new Error('StegID wallet capability secret boundary drift');
    if (receipt.automatic_signing !== false || receipt.automatic_broadcast !== false) throw new Error('StegID wallet capability execution authority drift');
    if (String(receipt.wallet_id || '').toLowerCase() !== 'stegwallet:primary' && String(receipt.wallet_address || '').toLowerCase() !== WALLET) throw new Error('StegID wallet capability wallet mismatch');
    if (!Array.isArray(receipt.granted_capabilities) || !receipt.granted_capabilities.includes('PREPARE')) throw new Error('StegID PREPARE capability required');
    if (receipt.granted_capabilities.includes('SIGN') || receipt.granted_capabilities.includes('BROADCAST')) throw new Error('current-phone bootstrap may not grant SIGN/BROADCAST');
    if (!receipt.identity_id || !receipt.device_id) throw new Error('StegID identity/device binding required');
    if (receipt.device_specific_authority !== true || receipt.identity_continuity_is_not_wallet_authority !== true) throw new Error('StegID capability separation invariant missing');
    const supplied = receipt.receipt_sha256;
    const material = { ...receipt }; delete material.receipt_sha256;
    if (supplied !== await sha256(material)) throw new Error('StegID wallet capability receipt commitment mismatch');
    return receipt;
  }

  const carrier = window.StegFinDirectRoute;
  if (!carrier || typeof carrier.run !== 'function') throw new Error('TV/TVC-admitted StegVerse direct carrier unavailable');

  async function runIdentityBound() {
    const capability = await loadCapability();
    const admissionEvidence = await sanitizedAdmissionEvidence(capability);
    const result = await carrier.run();
    if (!result?.receipt || result.receipt.state !== 'WALLET_HANDOFF_READY') return result;
    result.receipt.stegid_identity_id = capability.identity_id;
    result.receipt.stegid_device_id = capability.device_id;
    result.receipt.stegid_wallet_capability_receipt_sha256 = capability.receipt_sha256;
    result.receipt.stegid_admission_evidence = admissionEvidence;
    result.receipt.identity_continuity_is_not_wallet_authority = true;
    result.receipt.selected_carrier = 'STEGVERSE_DIRECT_ONCHAIN';
    const material = { ...result.receipt }; delete material.receipt_sha256;
    result.receipt.receipt_sha256 = await sha256(material);
    localStorage.setItem('stegverse.stegfin.wallet-handoff-ready.v1', JSON.stringify(result));
    return result;
  }

  window.StegFinPhoneContinuity = Object.freeze({
    ...carrier,
    run: runIdentityBound,
    requireDeviceWalletCapability: loadCapability,
    readSanitizedAdmissionEvidence: async () => sanitizedAdmissionEvidence(await loadCapability())
  });
})();
