(() => {
  'use strict';
  const form = document.getElementById('upload-form');
  if (!form) return;
  const fileInput = document.getElementById('response-file');
  const status = document.getElementById('intake-status');
  const button = document.getElementById('upload-response');
  const INGRESS = 'https://site-rigel-randolphs-projects.vercel.app/api/hil/upload';

  function remember(record) {
    const key = 'stegverse.hil.submissions.v1';
    let rows = [];
    try { rows = JSON.parse(localStorage.getItem(key) || '[]'); } catch {}
    rows = rows.filter((row) => row && row.submission_id !== record.submission_id);
    rows.unshift(record);
    localStorage.setItem(key, JSON.stringify(rows.slice(0, 100)));
    localStorage.setItem(`stegverse.hil.receipt.${record.submission_id}`, JSON.stringify(record));
  }

  function bytesToBase64(bytes) {
    let binary = '';
    const step = 0x8000;
    for (let i = 0; i < bytes.length; i += step) binary += String.fromCharCode(...bytes.subarray(i, i + step));
    return btoa(binary);
  }

  function hex(buffer) {
    return Array.from(new Uint8Array(buffer), b => b.toString(16).padStart(2, '0')).join('');
  }

  function baseRecord(file, payload, submissionId) {
    return {
      schema_version: 'HIL-APPENDED-RECORD-v1',
      submission_id: submissionId,
      recorded_at: new Date().toISOString(),
      response_filename: file.name,
      response_size: file.size,
      response_sha256: payload.response_sha256,
      primary_sha256: 'a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462',
      prompt_sha256: 'cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c',
      protocol: 'HIL-PROTOCOL-v1.1',
      display_name: payload.display_name,
      display_name_authorized: payload.display_name_authorized,
      publication_consent: payload.display_name_authorized ? 'DISPLAY_NAME_IF_APPROVED' : 'ANONYMOUS_IF_APPROVED',
      participant_confirmations: {
        authorized: true,
        unchanged: true
      },
      durable_submission: false,
      exact_byte_retrieval: false,
      publication_authorized: false
    };
  }

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    event.stopImmediatePropagation();
    const file = fileInput.files && fileInput.files[0];
    const authorized = document.getElementById('authorized').checked;
    const unchanged = document.getElementById('unchanged').checked;
    if (!file) { status.textContent = 'Choose the response PDF first.'; return; }
    if (!authorized || !unchanged) { status.textContent = 'Complete the two required confirmations.'; return; }
    if (file.type && file.type !== 'application/pdf' && !file.name.toLowerCase().endsWith('.pdf')) { status.textContent = 'The response must be a PDF.'; return; }

    button.disabled = true;
    status.dataset.state = 'warn';
    status.textContent = 'Hashing and submitting the response PDF…';

    const bytes = new Uint8Array(await file.arrayBuffer());
    const digest = hex(await crypto.subtle.digest('SHA-256', bytes));
    const submissionId = `HIL-${Date.now()}-${digest.slice(0, 12)}`;
    const payload = {
      filename: file.name,
      pdf_base64: bytesToBase64(bytes),
      response_sha256: digest,
      display_name: (document.getElementById('display-name').value || '').trim() || 'Anonymous',
      display_name_authorized: document.getElementById('show-name').checked,
      authorized: true,
      unchanged: true
    };

    let record = baseRecord(file, payload, submissionId);

    try {
      const response = await fetch(INGRESS, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const result = await response.json().catch(() => ({ detail: 'invalid_ingress_response' }));
      if (!response.ok || !result.submission_id || !result.receipt_id) {
        throw new Error(result.message || result.detail || `HTTP_${response.status}`);
      }
      record = {
        ...record,
        ...result,
        submission_id: result.submission_id,
        upload_state: 'UPLOAD_ACCEPTED',
        upload_succeeded: true,
        failure: null
      };
    } catch (error) {
      record = {
        ...record,
        receipt_id: `HIL-LOCAL-${digest.slice(0, 16)}`,
        upload_state: 'UPLOAD_FAILED',
        upload_succeeded: false,
        failure: {
          code: 'INGRESS_UNAVAILABLE_OR_REJECTED',
          detail: error && error.message ? error.message : 'unknown_upload_failure'
        }
      };
    }

    record.manifest_filename = `${record.submission_id}-record.json`;
    record.appended_record = {
      ...record,
      appended_record: undefined
    };
    remember(record);
    location.assign(`hil-receipt.html?submission_id=${encodeURIComponent(record.submission_id)}`);
  }, true);
})();
