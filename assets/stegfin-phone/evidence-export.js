(() => {
  'use strict';

  const WALLET_READY = 'WALLET_HANDOFF_READY';
  const el = (id) => document.getElementById(id);

  function canonicalEvidenceText() {
    const node = el('evidence');
    if (!node) throw new Error('canonical evidence surface unavailable');
    const text = String(node.textContent || '').trim();
    if (!text) throw new Error('canonical evidence is empty');
    let packet;
    try { packet = JSON.parse(text); } catch { throw new Error('canonical evidence is not valid JSON'); }
    validatePacket(packet);
    const canonicalText = JSON.stringify(packet, null, 2);
    if (text !== canonicalText) throw new Error('canonical evidence text is not the exact retained JSON projection');
    return canonicalText;
  }

  function validatePacket(packet) {
    const receipt = packet?.receipt || {};
    const evidence = receipt?.stegid_admission_evidence || {};
    const identity = evidence?.identity_continuity || {};
    const device = evidence?.device_admission || {};
    const capability = evidence?.wallet_capability || {};
    if (receipt.state !== WALLET_READY) throw new Error('fresh terminal WALLET_HANDOFF_READY evidence required');
    if (receipt.credential_authority !== 'TV/TVC' || receipt.credential_requirement !== 'NONE') throw new Error('TV/TVC credential boundary mismatch');
    if (receipt.non_tv_tvc_secret_or_token_used !== false || receipt.hosted_runtime_required !== false) throw new Error('runtime authority boundary mismatch');
    if (receipt.signed !== false || receipt.broadcast !== false) throw new Error('evidence export requires unsigned/unbroadcast receipt');
    if (evidence.schema !== 'stegverse.stegid.sanitized_admission_evidence.v1') throw new Error('fresh StegID admission evidence missing');
    if (identity.decision !== 'IDENTITY_CONTINUITY_VALID') throw new Error('identity continuity evidence missing');
    if (device.decision !== 'DEVICE_ADMITTED') throw new Error('device admission evidence missing');
    const steps = Array.isArray(device.validation_steps) ? device.validation_steps : [];
    for (const required of ['DEVICE_POSSESSION', 'HUMAN_CONTINUITY', 'IDENTITY_CONTINUITY']) {
      if (!steps.includes(required)) throw new Error(`StegID admission evidence missing ${required}`);
    }
    const granted = Array.isArray(capability.granted_capabilities) ? capability.granted_capabilities : [];
    if (!granted.includes('PREPARE')) throw new Error('StegID PREPARE evidence missing');
    if (granted.includes('SIGN') || granted.includes('BROADCAST')) throw new Error('StegID evidence may not grant SIGN/BROADCAST');
    if (!evidence.evidence_sha256 || !receipt.receipt_sha256) throw new Error('hash-bound phone evidence required');
    return packet;
  }

  function ensureControls() {
    let controls = el('phoneEvidenceExportControls');
    if (controls) return controls;
    const evidence = el('evidence');
    if (!evidence) return null;
    controls = document.createElement('div');
    controls.id = 'phoneEvidenceExportControls';
    controls.className = 'evidence-export-controls';

    const copy = document.createElement('button');
    copy.id = 'copyCanonicalEvidence';
    copy.type = 'button';
    copy.textContent = 'Copy canonical evidence';
    copy.disabled = true;

    const share = document.createElement('button');
    share.id = 'shareCanonicalEvidence';
    share.type = 'button';
    share.textContent = 'Share canonical evidence';
    share.disabled = true;

    const status = document.createElement('p');
    status.id = 'phoneEvidenceExportStatus';
    status.className = 'muted';
    status.textContent = 'Fresh WALLET_HANDOFF_READY + StegID admission evidence is required. Export never signs or broadcasts.';

    controls.append(copy, share, status);
    evidence.insertAdjacentElement('afterend', controls);

    copy.onclick = async () => {
      try {
        const text = canonicalEvidenceText();
        if (!navigator.clipboard?.writeText) throw new Error('clipboard API unavailable');
        await navigator.clipboard.writeText(text);
        status.textContent = 'Exact canonical JSON copied. Paste it into the canonical #68/#60 evidence observer. No wallet action occurred.';
      } catch (error) {
        status.textContent = `Fail closed: ${String(error?.message || error)}. No evidence was exported.`;
      }
    };

    share.onclick = async () => {
      try {
        const text = canonicalEvidenceText();
        if (navigator.share) {
          await navigator.share({ title: 'StegFin canonical phone evidence', text });
          status.textContent = 'Exact canonical JSON handed to the user-selected share target. No wallet action occurred.';
        } else {
          if (!navigator.clipboard?.writeText) throw new Error('share and clipboard APIs unavailable');
          await navigator.clipboard.writeText(text);
          status.textContent = 'Share is unavailable; exact canonical JSON was copied instead. No wallet action occurred.';
        }
      } catch (error) {
        if (error?.name === 'AbortError') {
          status.textContent = 'Share cancelled by user. No evidence or wallet action occurred.';
          return;
        }
        status.textContent = `Fail closed: ${String(error?.message || error)}. No evidence was exported.`;
      }
    };
    return controls;
  }

  function refresh() {
    const controls = ensureControls();
    if (!controls) return;
    const copy = el('copyCanonicalEvidence');
    const share = el('shareCanonicalEvidence');
    const status = el('phoneEvidenceExportStatus');
    try {
      canonicalEvidenceText();
      copy.disabled = false;
      share.disabled = false;
      status.textContent = 'Fresh hash-bound phone evidence is ready to copy/share. Signing and broadcast remain USER_ONLY.';
    } catch (error) {
      copy.disabled = true;
      share.disabled = true;
      status.textContent = `Evidence export locked: ${String(error?.message || error)}`;
    }
  }

  const evidence = el('evidence');
  if (evidence) {
    new MutationObserver(refresh).observe(evidence, { childList: true, characterData: true, subtree: true });
  }
  refresh();

  window.StegFinPhoneEvidenceExport = Object.freeze({
    canonicalEvidenceText,
    validatePacket,
    refresh,
    credentialAuthority: 'TV/TVC',
    credentialRequirement: 'NONE',
    walletSigningAuthority: 'USER_ONLY',
    broadcastAuthority: 'USER_ONLY'
  });
})();
