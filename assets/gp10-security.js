(() => {
  'use strict';

  const IDLE_LIMIT_MS = 15 * 60 * 1000;
  const HIDDEN_LIMIT_MS = 5 * 60 * 1000;
  const GP10_PREFIXES = ['gp10.workspace.', 'gp10.validation.'];
  const sessionNonce = crypto.randomUUID ? crypto.randomUUID() : `${Date.now()}-${Math.random()}`;
  let idleTimer = null;
  let hiddenAt = null;
  let locked = false;

  const now = () => new Date().toISOString();
  const $ = (id) => document.getElementById(id);

  function readJson(key, fallback) {
    try { return JSON.parse(localStorage.getItem(key) || JSON.stringify(fallback)); }
    catch { return fallback; }
  }

  function canonicalJson(value) {
    if (Array.isArray(value)) return `[${value.map(canonicalJson).join(',')}]`;
    if (value && typeof value === 'object') {
      return `{${Object.keys(value).sort().map(key => `${JSON.stringify(key)}:${canonicalJson(value[key])}`).join(',')}}`;
    }
    return JSON.stringify(value);
  }

  async function sha256(text) {
    const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
    return [...new Uint8Array(digest)].map(byte => byte.toString(16).padStart(2, '0')).join('');
  }

  function downloadJson(name, payload) {
    const blob = new Blob([JSON.stringify(payload, null, 2)], {type: 'application/json'});
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = name;
    link.rel = 'noopener';
    link.click();
    setTimeout(() => URL.revokeObjectURL(link.href), 1000);
  }

  function clearFileInputs() {
    document.querySelectorAll('input[type="file"]').forEach(input => { input.value = ''; });
  }

  function ensureLockOverlay() {
    let overlay = $('gp10SecurityLock');
    if (overlay) return overlay;
    overlay = document.createElement('div');
    overlay.id = 'gp10SecurityLock';
    overlay.hidden = true;
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.innerHTML = `
      <div class="gp10-lock-card">
        <strong>Workspace locked</strong>
        <p>This browser-local workspace was locked after inactivity. File selections were cleared. Unlocking does not grant authority or verify identity.</p>
        <button type="button" class="sv-btn sv-btn-primary" id="gp10Unlock">Unlock locally</button>
      </div>`;
    document.body.appendChild(overlay);
    $('gp10Unlock').addEventListener('click', unlock);
    return overlay;
  }

  function lock(reason) {
    if (locked) return;
    locked = true;
    clearFileInputs();
    const overlay = ensureLockOverlay();
    overlay.dataset.reason = reason;
    overlay.hidden = false;
    document.documentElement.dataset.gp10Locked = 'true';
    $('gp10Unlock')?.focus();
  }

  function unlock() {
    locked = false;
    const overlay = ensureLockOverlay();
    overlay.hidden = true;
    document.documentElement.dataset.gp10Locked = 'false';
    resetIdleTimer();
  }

  function resetIdleTimer() {
    if (locked) return;
    clearTimeout(idleTimer);
    idleTimer = setTimeout(() => lock('IDLE_TIMEOUT'), IDLE_LIMIT_MS);
  }

  function clearGp10Data() {
    const keys = [];
    for (let index = 0; index < localStorage.length; index += 1) {
      const key = localStorage.key(index);
      if (key && GP10_PREFIXES.some(prefix => key.startsWith(prefix))) keys.push(key);
    }
    keys.forEach(key => localStorage.removeItem(key));
    clearFileInputs();
    const status = $('status') || $('importStatus');
    if (status) status.textContent = `Cleared ${keys.length} GP10 browser-local item(s). This is not certified media erasure.`;
  }

  async function exportIntegrityReceipt() {
    const payload = {
      latest_candidate_record: readJson('gp10.workspace.records.v1.latest', null),
      evidence_packets: readJson('gp10.workspace.evidence.packets.v1', []),
      evidence_reviews: readJson('gp10.workspace.evidence.reviews.v1', [])
    };
    const canonical = canonicalJson(payload);
    const receipt = {
      receipt_type: 'GP10_BROWSER_INTEGRITY_RECEIPT',
      receipt_version: '1.0.0',
      created_at: now(),
      session_nonce: sessionNonce,
      digest_algorithm: 'SHA-256',
      canonicalization: 'recursive-key-sort-json-v1',
      payload_sha256: await sha256(canonical),
      payload_counts: {
        candidate_records: payload.latest_candidate_record ? 1 : 0,
        evidence_packets: payload.evidence_packets.length,
        evidence_reviews: payload.evidence_reviews.length
      },
      custody_state: 'BROWSER_LOCAL_UNCUSTODIED',
      proves: ['local payload consistency at receipt creation'],
      does_not_prove: ['truth', 'identity', 'source authority', 'approval', 'custody', 'execution authority'],
      execution_authority: false
    };
    downloadJson(`gp10-browser-integrity-${new Date().toISOString().slice(0, 10)}.json`, receipt);
    const status = $('status') || $('importStatus');
    if (status) status.textContent = 'Browser integrity receipt exported. It does not grant custody, approval, or execution authority.';
  }

  function installControls() {
    const review = document.querySelector('[data-step-name="Review and export"]');
    const host = review?.querySelector('.actions') || document.querySelector('.top-actions');
    if (!host || $('gp10IntegrityReceipt')) return;

    const integrity = document.createElement('button');
    integrity.type = 'button';
    integrity.id = 'gp10IntegrityReceipt';
    integrity.className = 'sv-btn sv-btn-secondary';
    integrity.textContent = 'Export integrity receipt';
    integrity.addEventListener('click', exportIntegrityReceipt);

    const clear = document.createElement('button');
    clear.type = 'button';
    clear.id = 'gp10ClearLocalData';
    clear.className = 'sv-btn sv-btn-secondary';
    clear.textContent = 'Clear GP10 local data';
    clear.addEventListener('click', clearGp10Data);

    host.append(integrity, clear);
  }

  ['pointerdown', 'keydown', 'touchstart', 'input', 'change'].forEach(eventName => {
    document.addEventListener(eventName, resetIdleTimer, {passive: true});
  });

  document.addEventListener('visibilitychange', () => {
    if (document.hidden) hiddenAt = Date.now();
    else if (hiddenAt && Date.now() - hiddenAt >= HIDDEN_LIMIT_MS) lock('BACKGROUND_TIMEOUT');
    else resetIdleTimer();
  });

  window.addEventListener('pagehide', clearFileInputs);
  window.GP10Security = Object.freeze({canonicalJson, sha256, exportIntegrityReceipt, lock, clearGp10Data});

  const style = document.createElement('style');
  style.textContent = `
    #gp10SecurityLock{position:fixed;inset:0;z-index:10000;display:grid;place-items:center;background:rgba(2,6,12,.96);padding:20px}
    #gp10SecurityLock[hidden]{display:none!important}
    .gp10-lock-card{max-width:520px;background:#0b1420;border:1px solid #38506f;border-radius:12px;padding:24px;color:#eef5ff}
    .gp10-lock-card strong{font-size:24px}.gp10-lock-card p{line-height:1.6;color:#b7c5d8}
  `;
  document.head.appendChild(style);

  ensureLockOverlay();
  installControls();
  resetIdleTimer();
})();
