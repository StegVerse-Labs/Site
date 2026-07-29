(() => {
  'use strict';

  const DB_NAME = 'stegverse-hil-review-v1';
  const STORE = 'accepted-submissions';
  const RECEIPT_PREFIX = 'stegverse.hil.receipt.';

  const byId = (id) => document.getElementById(id);

  function openDb() {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(DB_NAME, 1);
      request.onupgradeneeded = () => {
        const db = request.result;
        if (!db.objectStoreNames.contains(STORE)) db.createObjectStore(STORE, { keyPath: 'response_sha256' });
      };
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  async function sha256Hex(buffer) {
    const digest = await crypto.subtle.digest('SHA-256', buffer);
    return Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, '0')).join('');
  }

  async function stageSelectedSubmission() {
    const input = byId('response-file');
    const file = input && input.files && input.files[0];
    if (!file) return null;
    const buffer = await file.arrayBuffer();
    const responseHash = await sha256Hex(buffer);
    const record = {
      response_sha256: responseHash,
      filename: file.name,
      mime_type: file.type || 'application/pdf',
      pdf_blob: new Blob([buffer], { type: 'application/pdf' }),
      participant_identifier: (byId('participant-id')?.value || '').trim() || null,
      publication_consent: byId('publication-consent')?.value || 'not_provided',
      model: (byId('model')?.value || '').trim() || null,
      provider: (byId('provider')?.value || '').trim() || null,
      staged_at: new Date().toISOString()
    };
    const db = await openDb();
    await new Promise((resolve, reject) => {
      const tx = db.transaction(STORE, 'readwrite');
      tx.objectStore(STORE).put(record);
      tx.oncomplete = resolve;
      tx.onerror = () => reject(tx.error);
    });
    db.close();
    return responseHash;
  }

  function storedReceipt(responseHash) {
    try {
      const raw = localStorage.getItem(`${RECEIPT_PREFIX}${responseHash}`);
      return raw ? JSON.parse(raw) : null;
    } catch {
      return null;
    }
  }

  async function transitionWhenAccepted() {
    const status = byId('intake-status');
    if (!status || status.dataset.reviewTransition === 'true') return;
    if (status.dataset.state !== 'ok' || !/received and receipt verified|was already received/i.test(status.textContent || '')) return;
    const responseHash = await stageSelectedSubmission().catch(() => null);
    if (!responseHash) return;
    const receipt = storedReceipt(responseHash);
    if (!receipt || !receipt.submission_id || !receipt.receipt_id) return;
    status.dataset.reviewTransition = 'true';
    const target = new URL('hil-submission-review.html', window.location.href);
    target.searchParams.set('response_sha256', responseHash);
    target.searchParams.set('submission_id', receipt.submission_id);
    window.location.assign(target.href);
  }

  function install() {
    const upload = byId('upload-response');
    const status = byId('intake-status');
    if (!upload || !status) return;
    upload.addEventListener('click', () => { stageSelectedSubmission().catch(() => {}); }, { capture: true });
    new MutationObserver(() => { transitionWhenAccepted().catch(() => {}); })
      .observe(status, { childList: true, characterData: true, subtree: true, attributes: true });
    transitionWhenAccepted().catch(() => {});
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', install, { once: true });
  else install();
})();
