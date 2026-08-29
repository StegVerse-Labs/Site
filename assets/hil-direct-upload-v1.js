(() => {
  'use strict';

  const form = document.getElementById('upload-form');
  if (!form) return;

  const fileInput = document.getElementById('response-file');
  const status = document.getElementById('intake-status');
  const button = document.getElementById('upload-response');
  const INGRESS = '/api/hil/submissions';
  const DB_NAME = 'stegverse-hil-v3';
  const STORE_NAME = 'response_files';
  const RECORD_KEY = 'stegverse.hil.submissions.v1';
  const PRIMARY_SHA256 = 'a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462';
  const PROMPT_SHA256 = 'cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c';
  const INTR_INGRESS_SCHEMA = 'stegverse.hil.intr_ingress_envelope/v1';
  const INTR_HOP_RECEIPT_SCHEMA = 'stegverse.intr.hop_receipt/v1';

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

  function canonicalJson(value) {
    if (value === null || typeof value !== 'object') return JSON.stringify(value);
    if (Array.isArray(value)) return `[${value.map(canonicalJson).join(',')}]`;
    return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonicalJson(value[key])}`).join(',')}}`;
  }

  async function digestJsonUri(value) {
    const bytes = new TextEncoder().encode(canonicalJson(value));
    return `sha256:${await digestBytes(bytes)}`;
  }

  function randomId(prefix) {
    const bytes = new Uint8Array(16);
    crypto.getRandomValues(bytes);
    return `${prefix}-${Array.from(bytes, (b) => b.toString(16).padStart(2, '0')).join('')}`;
  }

  function isSha256Uri(value) {
    return /^sha256:[a-f0-9]{64}$/.test(String(value || ''));
  }

  async function buildIntrIngressEnvelope(digest, provenance) {
    const provenanceSha256 = await digestJsonUri(provenance);
    const binding = {
      schema: 'stegverse.hil.intr_payload_binding/v1',
      protocol: 'HIL-PROTOCOL-v1.1',
      response_sha256: `sha256:${digest}`,
      provenance_sha256: provenanceSha256,
      primary_sha256: `sha256:${PRIMARY_SHA256}`,
      prompt_sha256: `sha256:${PROMPT_SHA256}`
    };
    const body = {
      schema: INTR_INGRESS_SCHEMA,
      protocol: 'InTr',
      packet_id: randomId('HIL-INTR'),
      operation_id: randomId('HIL-UPLOAD'),
      from_role: 'DEVICE',
      to_role: 'HIL_INGRESS',
      payload_hash: await digestJsonUri(binding),
      response_sha256: `sha256:${digest}`,
      provenance_sha256: provenanceSha256,
      prior_receipt_hash: null,
      created_at: new Date().toISOString(),
      secret_plaintext_present: false,
      authority_transfer: false,
      transport_grants_execution_authority: false
    };
    return { ...body, envelope_hash: await digestJsonUri(body) };
  }

  async function validateHopReceipt(receipt, expected) {
    if (!receipt || receipt.schema !== INTR_HOP_RECEIPT_SCHEMA) throw new Error('intr_hop_receipt_missing');
    if (receipt.direction !== 'FORWARD' || receipt.boundary_verification !== 'VERIFIED' || receipt.transition_state !== 'RECEIVED') {
      throw new Error('intr_hop_receipt_state_invalid');
    }
    if (receipt.secret_plaintext_present !== false || receipt.authority_transfer !== false) throw new Error('intr_hop_receipt_authority_invalid');
    if (receipt.from_role !== expected.from || receipt.to_role !== expected.to || receipt.hop_index !== expected.hop) {
      throw new Error('intr_hop_receipt_boundary_invalid');
    }
    if (receipt.operation_hash !== expected.operationHash || receipt.payload_hash !== expected.payloadHash) {
      throw new Error('intr_hop_receipt_binding_invalid');
    }
    if (receipt.prior_receipt_hash !== expected.priorReceiptHash) throw new Error('intr_hop_receipt_chain_invalid');
    if (!isSha256Uri(receipt.receipt_hash)) throw new Error('intr_hop_receipt_hash_invalid');
    const body = { ...receipt };
    const claimed = body.receipt_hash;
    delete body.receipt_hash;
    if (claimed !== await digestJsonUri(body)) throw new Error('intr_hop_receipt_hash_mismatch');
    return receipt;
  }

  async function validateIntrReceiptChain(chain, ingressEnvelope) {
    if (!chain || chain.schema !== 'stegverse.hil.intr_receipt_chain/v1') throw new Error('intr_receipt_chain_missing');
    if (chain.ingress_envelope_hash !== ingressEnvelope.envelope_hash) throw new Error('intr_ingress_envelope_binding_invalid');
    const first = await validateHopReceipt(chain.device_hil_ingress_receipt, {
      from: 'DEVICE',
      to: 'HIL_INGRESS',
      hop: 1,
      operationHash: ingressEnvelope.envelope_hash,
      payloadHash: ingressEnvelope.payload_hash,
      priorReceiptHash: null
    });
    const second = await validateHopReceipt(chain.hil_custody_interlock_receipt, {
      from: 'HIL_INGRESS',
      to: 'HIL_CUSTODY',
      hop: 2,
      operationHash: ingressEnvelope.envelope_hash,
      payloadHash: ingressEnvelope.payload_hash,
      priorReceiptHash: first.receipt_hash
    });
    const egress = chain.tvc_egress_interlock_envelope;
    if (!egress || egress.schema !== 'stegverse.hil.intr_egress_envelope/v1') throw new Error('intr_tvc_egress_envelope_missing');
    if (egress.protocol !== 'InTr' || egress.from_role !== 'HIL_CUSTODY' || egress.to_role !== 'TVC_HIL_LIFECYCLE') {
      throw new Error('intr_tvc_egress_boundary_invalid');
    }
    if (egress.prior_receipt_hash !== second.receipt_hash || egress.payload_hash !== ingressEnvelope.payload_hash) {
      throw new Error('intr_tvc_egress_chain_invalid');
    }
    if (egress.state !== 'READY_FOR_INTERLOCK_ADMISSION' || egress.authority_transfer !== false || egress.transport_grants_execution_authority !== false) {
      throw new Error('intr_tvc_egress_state_invalid');
    }
    if (!isSha256Uri(egress.envelope_hash) || !isSha256Uri(chain.chain_hash)) throw new Error('intr_chain_hash_invalid');
    const egressBody = { ...egress };
    const egressClaimed = egressBody.envelope_hash;
    delete egressBody.envelope_hash;
    if (egressClaimed !== await digestJsonUri(egressBody)) throw new Error('intr_tvc_egress_hash_mismatch');
    const chainBody = { ...chain };
    const chainClaimed = chainBody.chain_hash;
    delete chainBody.chain_hash;
    if (chainClaimed !== await digestJsonUri(chainBody)) throw new Error('intr_receipt_chain_hash_mismatch');
    if (chain.next_required_transition !== 'HIL_CUSTODY_TVC_INTERLOCK_ADMISSION') throw new Error('intr_next_transition_invalid');
    return chain;
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

  async function submitDurably(file, digest, provenance, ingressEnvelope = null) {
    const envelope = ingressEnvelope || await buildIntrIngressEnvelope(digest, provenance);
    const body = new FormData();
    body.append('response_pdf', file, file.name);
    body.append('provenance_manifest', new Blob([`${JSON.stringify(provenance, null, 2)}\n`], { type: 'application/json' }), `${file.name}.provenance.json`);
    body.append('intr_ingress_envelope', new Blob([`${JSON.stringify(envelope, null, 2)}\n`], { type: 'application/json' }), `${file.name}.intr.json`);
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
    await validateIntrReceiptChain(result.intr_receipt_chain, envelope);
    if (result.next_required_transition !== 'HIL_CUSTODY_TVC_INTERLOCK_ADMISSION') {
      throw new Error('ingress_next_transition_invalid');
    }
    return { receipt: result, ingressEnvelope: envelope };
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
    status.textContent = 'Hashing the packet and opening the governed InTr ingress Interlock…';

    try {
      const bytes = new Uint8Array(await file.arrayBuffer());
      if (bytes.length < 5 || String.fromCharCode(...bytes.slice(0, 5)) !== '%PDF-') {
        throw new Error('invalid_pdf_signature');
      }
      const digest = await digestBytes(bytes);
      const provenance = buildProvenance(digest);
      const ingressEnvelope = await buildIntrIngressEnvelope(digest, provenance);

      try {
        const submitted = await submitDurably(file, digest, provenance, ingressEnvelope);
        const receipt = submitted.receipt;
        const record = {
          ...receipt,
          intr_ingress_envelope: ingressEnvelope,
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
          response_object_key: storage.key,
          response_storage_verified: true,
          provenance_manifest: provenance,
          intr_ingress_envelope: ingressEnvelope,
          resubmission_ready: true,
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
        status.textContent = 'The InTr operation was initiated and its exact packet is retained locally. No receiver or custody receipt is claimed until the receiving Interlock returns the chained receipts.';
        location.assign(`hil-receipt.html?submission_id=${encodeURIComponent(record.submission_id)}`);
      }
    } catch (error) {
      status.dataset.state = 'error';
      status.textContent = `The response could not be processed: ${error && error.message ? error.message : 'unknown_error'}`;
      button.disabled = false;
    }
  }, true);
})();
