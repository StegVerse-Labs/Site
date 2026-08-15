(() => {
  'use strict';

  const form = document.getElementById('upload-form');
  if (!form) return;

  const fileInput = document.getElementById('response-file');
  const status = document.getElementById('intake-status');
  const button = document.getElementById('upload-response');
  const READINESS = '/api/hil/readiness';
  const INGRESS = '/api/hil/submissions';
  const DB_NAME = 'stegverse-hil-v3';
  const STORE_NAME = 'response_files';
  const RECORD_KEY = 'stegverse.hil.submissions.v1';
  const PRIMARY_SHA256 = 'a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462';
  const PROMPT_SHA256 = 'cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c';

  function remember(record) {
    let rows = [];
    try {
      rows = JSON.parse(localStorage.getItem(RECORD_KEY) || '[]');
    } catch {
      rows = [];
    }
    rows = rows.filter((row) => row && row.submission_id !== record.submission_id);
    rows.unshift(record);
    localStorage.setItem(RECORD_KEY, JSON.stringify(rows.slice(0, 100)));
    localStorage.setItem(`stegverse.hil.receipt.${record.submission_id}`, JSON.stringify(record));
  }

  function openDb() {
    return new Promise((resolve, reject) => {
      if (!('indexedDB' in window)) return reject(new Error('indexeddb_unavailable'));
      const request = indexedDB.open(DB_NAME, 1);
      request.onupgradeneeded = () => {
        const db = request.result;
        if (!db.objectStoreNames.contains(STORE_NAME)) db.createObjectStore(STORE_NAME);
      };
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error || new Error('indexeddb_open_failed'));
      request.onblocked = () => reject(new Error('indexeddb_blocked'));
    });
  }

  async function storeAndRead(key, value) {
    const db = await openDb();
    try {
      await new Promise((resolve, reject) => {
        const tx = db.transaction(STORE_NAME, 'readwrite');
        tx.objectStore(STORE_NAME).put(value, key);
        tx.oncomplete = resolve;
        tx.onerror = () => reject(tx.error || new Error('indexeddb_write_failed'));
        tx.onabort = () => reject(tx.error || new Error('indexeddb_write_aborted'));
      });
      return await new Promise((resolve, reject) => {
        const tx = db.transaction(STORE_NAME, 'readonly');
        const request = tx.objectStore(STORE_NAME).get(key);
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error || new Error('indexeddb_read_failed'));
      });
    } finally {
      db.close();
    }
  }

  function hex(buffer) {
    return Array.from(new Uint8Array(buffer), (byte) => byte.toString(16).padStart(2, '0')).join('');
  }

  async function digestBytes(bytes) {
    return hex(await crypto.subtle.digest('SHA-256', bytes));
  }

  async function persistFallback(file, bytes, digest, submissionId) {
    const objectKey = `response:${submissionId}`;
    const restored = await storeAndRead(objectKey, {
      name: file.name,
      type: file.type || 'application/pdf',
      size: file.size,
      bytes: bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength)
    });
    if (!restored || !restored.bytes) throw new Error('local_fallback_readback_missing');
    const restoredHash = await digestBytes(new Uint8Array(restored.bytes));
    if (restoredHash !== digest) throw new Error('local_fallback_hash_verification_failed');
    return { backend: 'INDEXED_DB', key: objectKey, sha256: restoredHash };
  }

  async function requireReadyReceiver() {
    const response = await fetch(READINESS, {
      method: 'GET',
      credentials: 'same-origin',
      cache: 'no-store',
      headers: { Accept: 'application/json' }
    });
    const payload = await response.json().catch(() => null);
    if (!response.ok || !payload || payload.state !== 'READY') throw new Error('governed_receiver_not_ready');
    if (payload.primary_sha256 !== PRIMARY_SHA256 || payload.prompt_sha256 !== PROMPT_SHA256) {
      throw new Error('governed_receiver_identity_mismatch');
    }
    if (payload.provenance_manifest_required !== true || payload.provenance_manifest_schema !== 'HIL-RESPONSE-PROVENANCE-v1.1') {
      throw new Error('governed_receiver_provenance_contract_mismatch');
    }
    return payload;
  }

  function buildProvenance(digest) {
    const displayName = (document.getElementById('display-name').value || '').trim() || 'Anonymous';
    const displayNameAuthorized = document.getElementById('show-name').checked;
    return {
      schema_version: 'HIL-RESPONSE-PROVENANCE-v1.1',
      primary_version: 'v1.1',
      primary_sha256: PRIMARY_SHA256,
      protocol_version: 'HIL-PROTOCOL-v1.1',
      prompt_version: 'HIL-PROMPT-v1.1',
      prompt_sha256: PROMPT_SHA256,
      response_sha256: digest,
      generated_at: new Date().toISOString(),
      model: null,
      provider: null,
      conversation_reference: null,
      participant_delivery_contract: {
        single_downloadable_pdf: true,
        visible_summary_expected: true,
        participant_conversion_required: false
      },
      participant_optional_metadata: {
        participant_identifier: displayNameAuthorized ? displayName : null,
        publication_consent: displayNameAuthorized ? 'DISPLAY_NAME_IF_APPROVED' : 'ANONYMOUS_IF_APPROVED',
        model_response_declared_unedited: true,
        participant_consent_authority_acknowledged: true
      },
      producer_signature: { state: 'UNAVAILABLE', scheme: null, value: null, key_id: null }
    };
  }

  async function submitDurably(file, digest) {
    await requireReadyReceiver();
    const provenance = buildProvenance(digest);
    const body = new FormData();
    body.append('response_pdf', file, file.name);
    body.append('provenance_manifest', new Blob([`${JSON.stringify(provenance, null, 2)}\n`], { type: 'application/json' }), `${file.name}.provenance.json`);
    body.append('participant_identifier', provenance.participant_optional_metadata.participant_identifier || 'not_provided');
    body.append('publication_consent', provenance.participant_optional_metadata.publication_consent);
    body.append('primary_sha256', PRIMARY_SHA256);
    body.append('prompt_sha256', PROMPT_SHA256);
    body.append('model_response_declared_unedited', 'true');
    body.append('participant_consent_authority_acknowledged', 'true');

    const response = await fetch(INGRESS, {
      method: 'POST',
      body,
      credentials: 'same-origin',
      redirect: 'error',
      cache: 'no-store',
      headers: { Accept: 'application/json' }
    });
    const result = await response.json().catch(() => ({ detail: 'invalid_ingress_response' }));
    if (!response.ok) throw new Error(result.message || result.detail || `ingress_http_${response.status}`);
    if (result.schema_version !== 'HIL-RECEIVER-RECEIPT-v2' || !result.submission_id || !result.receipt_id) {
      throw new Error('ingress_receipt_incomplete');
    }
    if (result.submitted_file_sha256 !== digest) throw new Error('ingress_hash_mismatch');
    if (result.primary_sha256 !== PRIMARY_SHA256 || result.prompt_sha256 !== PROMPT_SHA256) {
      throw new Error('ingress_identity_mismatch');
    }
    if (result.custody_state !== 'EXACT_BYTES_PERSISTED' || result.registry_state !== 'RECORDED') {
      throw new Error('ingress_custody_not_durable');
    }
    return result;
  }

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    event.stopImmediatePropagation();

    const file = fileInput.files && fileInput.files[0];
    const authorized = document.getElementById('authorized').checked;
    const unchanged = document.getElementById('unchanged').checked;

    if (!file) {
      status.textContent = 'Choose the response PDF first.';
      return;
    }
    if (!authorized || !unchanged) {
      status.textContent = 'Complete the two required confirmations.';
      return;
    }
    if ((file.type && file.type !== 'application/pdf') || !file.name.toLowerCase().endsWith('.pdf')) {
      status.textContent = 'The response must be a PDF.';
      return;
    }

    button.disabled = true;
    status.dataset.state = 'warn';
    status.textContent = 'Hashing and submitting the response PDF to the governed StegVerse receiver…';

    try {
      const bytes = new Uint8Array(await file.arrayBuffer());
      if (bytes.length < 5 || String.fromCharCode(...bytes.slice(0, 5)) !== '%PDF-') {
        throw new Error('invalid_pdf_signature');
      }
      const digest = await digestBytes(bytes);

      try {
        const receipt = await submitDurably(file, digest);
        const record = {
          ...receipt,
          response_sha256: receipt.submitted_file_sha256,
          durable_submission: true,
          exact_byte_retrieval: true,
          custody_scope: 'STEGVERSE_GOVERNED_RECEIVER',
          publication_authorized: false,
          primary_sha256: PRIMARY_SHA256,
          prompt_sha256: PROMPT_SHA256,
          protocol: 'HIL-PROTOCOL-v1.1'
        };
        remember(record);
        status.dataset.state = 'ok';
        status.textContent = `${record.submission_id} received. Opening the governed submission result packet…`;
        location.assign(`hil-accepted.html?submission_id=${encodeURIComponent(record.submission_id)}`);
        return;
      } catch (ingressError) {
        const submissionId = `HIL-LOCAL-${Date.now()}-${digest.slice(0, 12)}`;
        const storage = await persistFallback(file, bytes, digest, submissionId);
        const record = {
          schema_version: 'HIL-APPENDED-RECORD-v1',
          submission_id: submissionId,
          receipt_id: `HIL-LOCAL-${digest.slice(0, 16)}`,
          recorded_at: new Date().toISOString(),
          state: 'LOCAL_FALLBACK_PENDING_RESUBMISSION',
          record_state: 'LOCAL_FALLBACK_PENDING_RESUBMISSION',
          upload_state: 'GOVERNED_RECEIVER_UNAVAILABLE_LOCAL_COPY_VERIFIED',
          upload_succeeded: false,
          accepted: false,
          failure: String(ingressError && ingressError.message ? ingressError.message : ingressError),
          response_filename: file.name,
          response_size: file.size,
          response_type: file.type || 'application/pdf',
          response_sha256: digest,
          response_storage: storage,
          response_storage_verified: true,
          durable_submission: false,
          exact_byte_retrieval: true,
          custody_scope: 'PARTICIPANT_DEVICE_FALLBACK',
          publication_authorized: false,
          primary_sha256: PRIMARY_SHA256,
          prompt_sha256: PROMPT_SHA256,
          protocol: 'HIL-PROTOCOL-v1.1'
        };
        remember(record);
        status.dataset.state = 'warn';
        status.textContent = 'The governed receiver was unavailable. A verified local copy was retained, but no StegVerse custody is claimed.';
        location.assign(`hil-receipt.html?submission_id=${encodeURIComponent(record.submission_id)}`);
      }
    } catch (error) {
      status.dataset.state = 'error';
      status.textContent = `The response could not be processed: ${error && error.message ? error.message : 'unknown_error'}`;
      button.disabled = false;
    }
  }, true);
})();
