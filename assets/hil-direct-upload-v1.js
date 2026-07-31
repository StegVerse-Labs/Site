(() => {
  'use strict';
  const form = document.getElementById('upload-form');
  if (!form) return;
  const fileInput = document.getElementById('response-file');
  const status = document.getElementById('intake-status');
  const button = document.getElementById('upload-response');
  const INGRESS = 'https://site-rigel-randolphs-projects.vercel.app/api/hil/upload';
  const ISSUE_URL = 'https://github.com/StegVerse-Labs/TVC/issues/new';

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
    for (let i = 0; i < bytes.length; i += step) binary += String.fromCharCode(...bytes.subarray(i, i + step));
    return btoa(binary);
  }

  function hex(buffer) {
    return Array.from(new Uint8Array(buffer), b => b.toString(16).padStart(2, '0')).join('');
  }

  function githubFallback(file, payload) {
    const submissionId = `HIL-${Date.now()}-${payload.response_sha256.slice(0, 12)}`;
    const receiptId = `HIL-LOCAL-${payload.response_sha256.slice(0, 16)}`;
    const manifestName = `${submissionId}-provenance.json`;
    const provenance = {
      schema_version: 'HIL-GITHUB-RETURN-v1',
      submission_id: submissionId,
      receipt_id: receiptId,
      state: 'PARTICIPANT_RETURN_PREPARED',
      received_at: new Date().toISOString(),
      source_transport: 'github_issue_attachment',
      response_filename: file.name,
      response_size: file.size,
      response_sha256: payload.response_sha256,
      primary_sha256: 'a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462',
      prompt_sha256: 'cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c',
      protocol: 'HIL-PROTOCOL-v1.1',
      display_name: payload.display_name,
      display_name_authorized: payload.display_name_authorized,
      publication_consent: payload.display_name_authorized ? 'DISPLAY_NAME_IF_APPROVED' : 'ANONYMOUS_IF_APPROVED',
      durable_submission: false,
      exact_byte_retrieval: false,
      publication_authorized: false
    };
    const body = [
      '## HIL participant return',
      '',
      `Submission ID: ${submissionId}`,
      `Response filename: ${file.name}`,
      `Response SHA-256: ${payload.response_sha256}`,
      `Primary SHA-256: ${provenance.primary_sha256}`,
      `Prompt SHA-256: ${provenance.prompt_sha256}`,
      `Display name: ${payload.display_name}`,
      '',
      'Attach both files to this issue before submitting:',
      `1. ${file.name}`,
      `2. ${manifestName}`,
      '',
      'The response PDF must remain unchanged.'
    ].join('\n');
    const githubReturnUrl = `${ISSUE_URL}?title=${encodeURIComponent(`HIL participant return ${submissionId}`)}&body=${encodeURIComponent(body)}`;
    const appendedRecord = {
      ...provenance,
      manifest_filename: manifestName,
      provenance_manifest: provenance,
      github_return_url: githubReturnUrl,
      participant_action_required: true
    };
    remember(appendedRecord);
    location.assign(`hil-receipt.html?submission_id=${encodeURIComponent(submissionId)}`);
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
    const payload = {
      filename: file.name,
      pdf_base64: bytesToBase64(bytes),
      response_sha256: digest,
      display_name: (document.getElementById('display-name').value || '').trim() || 'Anonymous',
      display_name_authorized: document.getElementById('show-name').checked,
      authorized: true,
      unchanged: true
    };

    try {
      const response = await fetch(INGRESS, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const result = await response.json().catch(() => ({ detail: 'invalid_ingress_response' }));
      if (!response.ok || !result.submission_id || !result.receipt_id) throw new Error(result.message || result.detail || 'The upload was not accepted.');
      remember(result);
      location.assign(`hil-receipt.html?submission_id=${encodeURIComponent(result.submission_id)}`);
    } catch (error) {
      githubFallback(file, payload);
    }
  }, true);
})();
