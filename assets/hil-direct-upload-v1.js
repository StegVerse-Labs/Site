(() => {
  'use strict';
  const form = document.getElementById('upload-form');
  if (!form) return;
  const fileInput = document.getElementById('response-file');
  const status = document.getElementById('intake-status');
  const button = document.getElementById('upload-response');
  const INGRESS = 'https://site-rigel-randolphs-projects.vercel.app/api/hil/upload';

  function remember(receipt) {
    const key = 'stegverse.hil.submissions.v1';
    let rows = [];
    try { rows = JSON.parse(localStorage.getItem(key) || '[]'); } catch {}
    rows = rows.filter((row) => row && row.submission_id !== receipt.submission_id);
    rows.unshift(receipt);
    localStorage.setItem(key, JSON.stringify(rows.slice(0, 100)));
    localStorage.setItem(`stegverse.hil.receipt.${receipt.submission_id}`, JSON.stringify(receipt));
  }

  function bytesToBase64(bytes) {
    let binary = '';
    const step = 0x8000;
    for (let i = 0; i < bytes.length; i += step) {
      binary += String.fromCharCode(...bytes.subarray(i, i + step));
    }
    return btoa(binary);
  }

  function hex(buffer) {
    return Array.from(new Uint8Array(buffer), b => b.toString(16).padStart(2, '0')).join('');
  }

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    event.stopImmediatePropagation();
    const file = fileInput.files && fileInput.files[0];
    const authorized = document.getElementById('authorized').checked;
    const unchanged = document.getElementById('unchanged').checked;
    if (!file) { status.textContent = 'Choose the response PDF first.'; return; }
    if (!authorized || !unchanged) { status.textContent = 'Complete the two required confirmations.'; return; }

    button.disabled = true;
    status.dataset.state = 'warn';
    status.textContent = 'Hashing and submitting the response PDF…';
    try {
      const bytes = new Uint8Array(await file.arrayBuffer());
      const digest = hex(await crypto.subtle.digest('SHA-256', bytes));
      const payload = {
        filename: file.name,
        pdf_base64: bytesToBase64(bytes),
        response_sha256: digest,
        display_name: (document.getElementById('display-name').value || '').trim() || 'Anonymous',
        display_name_authorized: document.getElementById('show-name').checked,
        authorized: true,
        unchanged: true
      };
      const response = await fetch(INGRESS, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const result = await response.json().catch(() => ({ detail: 'invalid_ingress_response' }));
      if (!response.ok || !result.submission_id || !result.receipt_id) {
        throw new Error(result.message || result.detail || 'The upload was not accepted.');
      }
      remember(result);
      location.assign(`hil-receipt.html?submission_id=${encodeURIComponent(result.submission_id)}`);
    } catch (error) {
      status.dataset.state = 'error';
      status.textContent = error.message || 'The response packet could not be uploaded.';
      button.disabled = false;
    }
  }, true);
})();
