(() => {
  'use strict';
  const form = document.getElementById('upload-form');
  if (!form) return;
  const fileInput = document.getElementById('response-file');
  const status = document.getElementById('intake-status');
  const button = document.getElementById('upload-response');

  function remember(record) {
    const key = 'stegverse.hil.submissions.v1';
    let rows = [];
    try { rows = JSON.parse(localStorage.getItem(key) || '[]'); } catch {}
    rows = rows.filter((row) => row && row.submission_id !== record.submission_id);
    rows.unshift(record);
    localStorage.setItem(key, JSON.stringify(rows.slice(0, 100)));
    localStorage.setItem(`stegverse.hil.receipt.${record.submission_id}`, JSON.stringify(record));
  }

  function openDb() {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open('stegverse-hil-v1', 1);
      request.onupgradeneeded = () => {
        const db = request.result;
        if (!db.objectStoreNames.contains('response_files')) db.createObjectStore('response_files');
      };
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error || new Error('indexeddb_open_failed'));
    });
  }

  async function storeResponse(key, file) {
    const db = await openDb();
    await new Promise((resolve, reject) => {
      const tx = db.transaction('response_files', 'readwrite');
      tx.objectStore('response_files').put(file, key);
      tx.oncomplete = resolve;
      tx.onerror = () => reject(tx.error || new Error('indexeddb_write_failed'));
      tx.onabort = () => reject(tx.error || new Error('indexeddb_write_aborted'));
    });
    db.close();
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
    if (file.type && file.type !== 'application/pdf' && !file.name.toLowerCase().endsWith('.pdf')) { status.textContent = 'The response must be a PDF.'; return; }

    button.disabled = true;
    status.dataset.state = 'warn';
    status.textContent = 'Hashing and appending the response PDF…';

    const bytes = await file.arrayBuffer();
    const digest = hex(await crypto.subtle.digest('SHA-256', bytes));
    const submissionId = `HIL-${Date.now()}-${digest.slice(0, 12)}`;
    const objectKey = `response:${submissionId}`;
    const record = {
      schema_version: 'HIL-APPENDED-RECORD-v1',
      submission_id: submissionId,
      receipt_id: `HIL-LOCAL-${digest.slice(0, 16)}`,
      recorded_at: new Date().toISOString(),
      response_filename: file.name,
      response_size: file.size,
      response_type: file.type || 'application/pdf',
      response_sha256: digest,
      response_object_key: objectKey,
      primary_sha256: 'a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462',
      prompt_sha256: 'cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c',
      protocol: 'HIL-PROTOCOL-v1.1',
      display_name: (document.getElementById('display-name').value || '').trim() || 'Anonymous',
      display_name_authorized: document.getElementById('show-name').checked,
      publication_consent: document.getElementById('show-name').checked ? 'DISPLAY_NAME_IF_APPROVED' : 'ANONYMOUS_IF_APPROVED',
      participant_confirmations: { authorized: true, unchanged: true },
      custody_scope: 'PARTICIPANT_DEVICE',
      durable_submission: false,
      exact_byte_retrieval: true,
      publication_authorized: false,
      upload_state: 'APPENDED_RECORD_CREATED',
      upload_succeeded: true,
      accepted: true,
      failure: null
    };

    try {
      await storeResponse(objectKey, file);
    } catch (error) {
      record.response_object_key = null;
      record.exact_byte_retrieval = false;
      record.upload_state = 'APPENDED_RECORD_FAILED';
      record.upload_succeeded = false;
      record.accepted = false;
      record.failure = { code: 'LOCAL_RECORD_WRITE_FAILED', detail: error && error.message ? error.message : 'unknown_local_record_failure' };
    }

    record.manifest_filename = `${record.submission_id}-record.json`;
    record.appended_record = { ...record, appended_record: undefined };
    remember(record);
    location.assign(`hil-receipt.html?submission_id=${encodeURIComponent(record.submission_id)}`);
  }, true);
})();
