(() => {
  'use strict';
  const form = document.getElementById('upload-form');
  if (!form) return;
  const fileInput = document.getElementById('response-file');
  const status = document.getElementById('intake-status');
  const button = document.getElementById('upload-response');
  const DB_NAME = 'stegverse-hil-v2';
  const STORE_NAME = 'response_files';
  const CACHE_NAME = 'stegverse-hil-response-v1';
  const RECORD_KEY = 'stegverse.hil.submissions.v1';

  function remember(record) {
    let rows = [];
    try { rows = JSON.parse(localStorage.getItem(RECORD_KEY) || '[]'); } catch {}
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

  async function idbPutAndRead(key, value) {
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

  async function cachePutAndRead(key, bytes, type) {
    if (!('caches' in window)) throw new Error('cache_storage_unavailable');
    const cache = await caches.open(CACHE_NAME);
    const url = `${location.origin}/__hil_response__/${encodeURIComponent(key)}`;
    await cache.put(url, new Response(new Blob([bytes], { type }), { headers: { 'Content-Type': type } }));
    const response = await cache.match(url);
    if (!response) throw new Error('cache_storage_read_failed');
    return new Uint8Array(await response.arrayBuffer());
  }

  function bytesToBase64(bytes) {
    let binary = '';
    const step = 0x8000;
    for (let i = 0; i < bytes.length; i += step) binary += String.fromCharCode(...bytes.subarray(i, i + step));
    return btoa(binary);
  }

  function base64ToBytes(value) {
    const binary = atob(value);
    const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i += 1) bytes[i] = binary.charCodeAt(i);
    return bytes;
  }

  function localPutAndRead(key, bytes) {
    const base64 = bytesToBase64(bytes);
    const chunkSize = 300000;
    const count = Math.ceil(base64.length / chunkSize);
    const prefix = `stegverse.hil.pdf.${key}`;
    localStorage.setItem(`${prefix}.count`, String(count));
    for (let i = 0; i < count; i += 1) localStorage.setItem(`${prefix}.${i}`, base64.slice(i * chunkSize, (i + 1) * chunkSize));
    let restored = '';
    const restoredCount = Number(localStorage.getItem(`${prefix}.count`) || 0);
    for (let i = 0; i < restoredCount; i += 1) restored += localStorage.getItem(`${prefix}.${i}`) || '';
    if (!restored || restored.length !== base64.length) throw new Error('local_storage_verification_failed');
    return base64ToBytes(restored);
  }

  function hex(buffer) {
    return Array.from(new Uint8Array(buffer), b => b.toString(16).padStart(2, '0')).join('');
  }

  async function digestBytes(bytes) {
    return hex(await crypto.subtle.digest('SHA-256', bytes));
  }

  async function storeAndVerify(key, bytes, file, expectedHash) {
    const failures = [];
    try {
      const stored = await idbPutAndRead(key, {
        name: file.name,
        type: file.type || 'application/pdf',
        size: file.size,
        bytes: bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength)
      });
      const restored = stored && stored.bytes ? new Uint8Array(stored.bytes) : null;
      if (!restored || await digestBytes(restored) !== expectedHash) throw new Error('indexeddb_hash_verification_failed');
      return { backend: 'INDEXED_DB', key };
    } catch (error) { failures.push(`INDEXED_DB:${error.message || error}`); }

    try {
      const restored = await cachePutAndRead(key, bytes, file.type || 'application/pdf');
      if (await digestBytes(restored) !== expectedHash) throw new Error('cache_hash_verification_failed');
      return { backend: 'CACHE_STORAGE', key };
    } catch (error) { failures.push(`CACHE_STORAGE:${error.message || error}`); }

    try {
      const restored = localPutAndRead(key, bytes);
      if (await digestBytes(restored) !== expectedHash) throw new Error('local_hash_verification_failed');
      return { backend: 'LOCAL_STORAGE_CHUNKS', key };
    } catch (error) { failures.push(`LOCAL_STORAGE_CHUNKS:${error.message || error}`); }

    throw new Error(failures.join(';'));
  }

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    event.stopImmediatePropagation();
    const file = fileInput.files && fileInput.files[0];
    const authorized = document.getElementById('authorized').checked;
    const unchanged = document.getElementById('unchanged').checked;
    if (!file) { status.textContent = 'Choose the response PDF first.'; return; }
    if (!authorized || !unchanged) { status.textContent = 'Complete the two required confirmations.'; return; }
    if ((file.type && file.type !== 'application/pdf') || !file.name.toLowerCase().endsWith('.pdf')) { status.textContent = 'The response must be a PDF.'; return; }

    button.disabled = true;
    status.dataset.state = 'warn';
    status.textContent = 'Hashing, storing, and verifying the response PDF…';

    try {
      const bytes = new Uint8Array(await file.arrayBuffer());
      if (bytes.length < 5 || String.fromCharCode(...bytes.slice(0, 5)) !== '%PDF-') throw new Error('invalid_pdf_signature');
      const digest = await digestBytes(bytes);
      const submissionId = `HIL-${Date.now()}-${digest.slice(0, 12)}`;
      const objectKey = `response:${submissionId}`;
      const storage = await storeAndVerify(objectKey, bytes, file, digest);
      const record = {
        schema_version: 'HIL-APPENDED-RECORD-v1',
        submission_id: submissionId,
        receipt_id: `HIL-LOCAL-${digest.slice(0, 16)}`,
        recorded_at: new Date().toISOString(),
        record_state: 'APPENDED_RECORD_CREATED',
        upload_state: 'APPENDED_RECORD_CREATED',
        upload_succeeded: true,
        accepted: true,
        failure: null,
        response_filename: file.name,
        response_size: file.size,
        response_type: file.type || 'application/pdf',
        response_sha256: digest,
        response_object_key: objectKey,
        response_storage: storage,
        response_storage_verified: true,
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
        publication_authorized: false
      };
      record.manifest_filename = `${record.submission_id}-record.json`;
      record.appended_record = { ...record, appended_record: undefined };
      remember(record);
      location.assign(`hil-receipt.html?submission_id=${encodeURIComponent(record.submission_id)}`);
    } catch (error) {
      status.dataset.state = 'error';
      status.textContent = `The response could not be appended: ${error && error.message ? error.message : 'unknown_error'}`;
      button.disabled = false;
    }
  }, true);
})();
