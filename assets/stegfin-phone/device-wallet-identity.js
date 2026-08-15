(() => {
  'use strict';

  const STORAGE_KEY = 'stegverse.stegid.wallet-capability.v1';
  const WALLET = '0xA503DCe5471492bbA2D06e9f78F4d9D6Bcc852aA'.toLowerCase();
  const SCHEMA = 'stegverse.stegid.wallet_capability_decision.v1';
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
    const result = await carrier.run();
    if (!result?.receipt || result.receipt.state !== 'WALLET_HANDOFF_READY') return result;
    result.receipt.stegid_identity_id = capability.identity_id;
    result.receipt.stegid_device_id = capability.device_id;
    result.receipt.stegid_wallet_capability_receipt_sha256 = capability.receipt_sha256;
    result.receipt.identity_continuity_is_not_wallet_authority = true;
    result.receipt.selected_carrier = 'STEGVERSE_DIRECT_ONCHAIN';
    const material = { ...result.receipt }; delete material.receipt_sha256;
    result.receipt.receipt_sha256 = await sha256(material);
    localStorage.setItem('stegverse.stegfin.wallet-handoff-ready.v1', JSON.stringify(result));
    return result;
  }

  window.StegFinPhoneContinuity = Object.freeze({ ...carrier, run: runIdentityBound, requireDeviceWalletCapability: loadCapability });
})();
