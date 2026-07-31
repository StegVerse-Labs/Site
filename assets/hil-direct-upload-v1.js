(() => {
  'use strict';
  const form = document.getElementById('upload-form');
  if (!form) return;
  const fileInput = document.getElementById('response-file');
  const status = document.getElementById('intake-status');
  const button = document.getElementById('upload-response');

  function remember(receipt) {
    const key = 'stegverse.hil.submissions.v1';
    let rows = [];
    try { rows = JSON.parse(localStorage.getItem(key) || '[]'); } catch {}
    rows = rows.filter((row) => row && row.submission_id !== receipt.submission_id);
    rows.unshift(receipt);
    localStorage.setItem(key, JSON.stringify(rows.slice(0, 100)));
    localStorage.setItem(`stegverse.hil.receipt.${receipt.submission_id}`, JSON.stringify(receipt));
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
    status.textContent = 'Uploading the response PDF…';
    try {
      const body = new FormData();
      body.append('response_pdf', file, file.name);
      body.append('display_name', (document.getElementById('display-name').value || '').trim() || 'Anonymous');
      body.append('display_name_authorized', String(document.getElementById('show-name').checked));
      body.append('authorized', 'true');
      body.append('unchanged', 'true');

      const response = await fetch('/api/hil/upload', { method: 'POST', body });
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
