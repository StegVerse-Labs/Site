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

  async function buildIntrTransportIntent(digest, provenance, operationId = null) {
    const intr = window.StegVerseGeneratedInTr;
    if (!intr || typeof intr.buildIntent !== 'function') throw new Error('canonical_intr_connector_unavailable');
    const provenanceSha256 = await digestJsonUri(provenance);
    const binding = {
      schema: 'stegverse.hil.intr_payload_binding/v1',
      protocol: 'HIL-PROTOCOL-v1.1',
      response_sha256: `sha256:${digest}`,
      provenance_sha256: provenanceSha256,
      primary_sha256: `sha256:${PRIMARY_SHA256}`,
      prompt_sha256: `sha256:${PROMPT_SHA256}`
    };
    const op = operationId || randomId('HIL-UPLOAD');
    return intr.buildIntent(
      'hil-submission',
      new TextEncoder().encode(intr.canonical(binding)),
      'SUBMIT',
      op
    );
  }

  async function buildIntrMaterializationRequest(intent, payloadRef) {
    const intr = window.StegVerseGeneratedInTr;
    if (!intr || typeof intr.buildMaterializationRequest !== 'function') throw new Error('canonical_intr_materialization_unavailable');
    const carrier = window.StegVerseHBInTrCarrier;
    if (!carrier || typeof carrier.buildBinding !== 'function') throw new Error('canonical_hb_intr_carrier_unavailable');
    const binding = await carrier.buildBinding(intent.packet_id, intent.payload_hash);
    return intr.buildMaterializationRequest('hil-submission', intent, payloadRef, binding);
  }

  async function stageTransportPacket(file, bytes, digest, provenance, transportIntent) {
    const objectKey = `response:${transportIntent.operation_id}`;
    const payloadRef = `indexeddb://${DB_NAME}/${STORE_NAME}/${encodeURIComponent(objectKey)}`;
    const materializationRequest = await buildIntrMaterializationRequest(transportIntent, payloadRef);
    const value = {
      name: file.name,
      type: file.type || 'application/pdf',
      size: file.size,
      bytes: bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength),
      response_sha256: digest,
      provenance_manifest: provenance,
      intr_transport_intent: transportIntent,
      intr_materialization_request: materializationRequest
    };
    const restored = await storeAndRead(objectKey, value);
    if (!restored || !restored.bytes) throw new Error('intr_prestage_readback_missing');
    const restoredHash = await digestBytes(new Uint8Array(restored.bytes));
    if (restoredHash !== digest) throw new Error('intr_prestage_pdf_hash_mismatch');
    if (canonicalJson(restored.provenance_manifest) !== canonicalJson(provenance)) throw new Error('intr_prestage_provenance_mismatch');
    if (canonicalJson(restored.intr_transport_intent) !== canonicalJson(transportIntent)) throw new Error('intr_prestage_transport_intent_mismatch');
    if (canonicalJson(restored.intr_materialization_request) !== canonicalJson(materializationRequest)) throw new Error('intr_prestage_materialization_request_mismatch');
    const requestBody = { ...materializationRequest };
    const claimed = requestBody.request_hash;
    delete requestBody.request_hash;
    if (claimed !== await digestJsonUri(requestBody)) throw new Error('intr_prestage_materialization_request_hash_mismatch');
    return {
      storage: { backend: 'INDEXED_DB', key: objectKey, sha256: restoredHash },
      materializationRequest
    };
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

  async function validateIntrReceiptChain(chain, ingressIntent) {
    if (!chain || chain.schema !== 'stegverse.hil.intr_receipt_chain/v2') throw new Error('intr_receipt_chain_missing');
    if (canonicalJson(chain.ingress_transport_intent) !== canonicalJson(ingressIntent)) throw new Error('intr_ingress_intent_binding_invalid');

    const operationHash = await digestJsonUri({
      operation_id: ingressIntent.operation_id,
      packet_id: ingressIntent.packet_id,
      payload_hash: ingressIntent.payload_hash
    });
    const first = await validateHopReceipt(chain.device_stegos_ingress_receipt, {
      from: 'DEVICE_SYSTEM',
      to: 'STEGOS_ECOSYSTEM',
      hop: 1,
      operationHash,
      payloadHash: ingressIntent.payload_hash,
      priorReceiptHash: null
    });

    const custodyIntent = chain.hil_custody_transport_intent;
    if (!custodyIntent || custodyIntent.schema !== 'stegverse.universal-intr-transport/v1') throw new Error('intr_custody_intent_missing');
    if (custodyIntent.source?.boundary !== 'STEGOS_ECOSYSTEM' || custodyIntent.source?.subsystem !== 'HIL:Ingress') throw new Error('intr_custody_source_invalid');
    if (custodyIntent.destination?.boundary !== 'STEGOS_ECOSYSTEM' || custodyIntent.destination?.subsystem !== 'HIL:Custody') throw new Error('intr_custody_destination_invalid');
    if (custodyIntent.prior_transport_receipt_hash !== first.receipt_hash || custodyIntent.payload_hash !== ingressIntent.payload_hash) throw new Error('intr_custody_intent_chain_invalid');

    const custodyOperationHash = await digestJsonUri({
      operation_id: custodyIntent.operation_id,
      packet_id: custodyIntent.packet_id,
      payload_hash: custodyIntent.payload_hash
    });
    const second = await validateHopReceipt(chain.hil_custody_interlock_receipt, {
      from: 'STEGOS_ECOSYSTEM',
      to: 'STEGOS_ECOSYSTEM',
      hop: 1,
      operationHash: custodyOperationHash,
      payloadHash: ingressIntent.payload_hash,
      priorReceiptHash: first.receipt_hash
    });

    const nextIntent = chain.next_interlock_intent;
    if (!nextIntent || nextIntent.schema !== 'stegverse.universal-intr-transport/v1') throw new Error('intr_tvc_next_intent_missing');
    if (nextIntent.source?.boundary !== 'STEGOS_ECOSYSTEM' || nextIntent.source?.subsystem !== 'HIL:Custody') throw new Error('intr_tvc_source_invalid');
    if (nextIntent.destination?.boundary !== 'STEGOS_ECOSYSTEM' || nextIntent.destination?.subsystem !== 'TVC:HIL-Lifecycle') throw new Error('intr_tvc_destination_invalid');
    if (nextIntent.prior_transport_receipt_hash !== second.receipt_hash || nextIntent.payload_hash !== ingressIntent.payload_hash) throw new Error('intr_tvc_intent_chain_invalid');
    if (nextIntent.transport_semantics?.always_on_receiver_required !== false || nextIntent.transport_semantics?.event_triggered !== true) throw new Error('intr_tvc_transport_semantics_invalid');

    if (!isSha256Uri(chain.chain_hash)) throw new Error('intr_chain_hash_invalid');
    const chainBody = { ...chain };
    const chainClaimed = chainBody.chain_hash;
    delete chainBody.chain_hash;
    if (chainClaimed !== await digestJsonUri(chainBody)) throw new Error('intr_receipt_chain_hash_mismatch');
    if (chain.next_required_transition !== 'HIL_CUSTODY_TVC_INTERLOCK_ADMISSION') throw new Error('intr_next_transition_invalid');
    if (chain.authority_transfer !== false) throw new Error('intr_chain_authority_invalid');
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

  async function submitDurably(file, digest, provenance, transportIntent = null) {
    const envelope = transportIntent || await buildIntrTransportIntent(digest, provenance);
    const body = new FormData();
    body.append('response_pdf', file, file.name);
    body.append('provenance_manifest', new Blob([`${JSON.stringify(provenance, null, 2)}\n`], { type: 'application/json' }), `${file.name}.provenance.json`);
    body.append('intr_transport_intent', new Blob([`${JSON.stringify(envelope, null, 2)}\n`], { type: 'application/json' }), `${file.name}.intr.json`);
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
    return { receipt: result, transportIntent: envelope };
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
      const transportIntent = await buildIntrTransportIntent(digest, provenance);
      const staged = await stageTransportPacket(file, bytes, digest, provenance, transportIntent);

      try {
        const submitted = await submitDurably(file, digest, provenance, transportIntent);
        const receipt = submitted.receipt;
        const record = {
          ...receipt,
          intr_transport_intent: transportIntent,
          intr_materialization_request: staged.materializationRequest,
          intr_materialization_state: 'SATISFIED_BY_DIRECT_RECEIVER_RECEIPT',
          local_pretransport_staged: true,
          response_storage: staged.storage,
          response_object_key: staged.storage.key,
          response_storage_verified: true,
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
        const storage = staged.storage;
        const record = {
          schema_version: 'HIL-APPENDED-RECORD-v1',
          submission_id: submissionId,
          receipt_id: `HIL-LOCAL-${digest.slice(0, 16)}`,
          recorded_at: new Date().toISOString(),
          state: 'INTR_TRANSPORT_PENDING',
          record_state: 'INTR_TRANSPORT_PENDING',
          upload_state: 'EXACT_PACKET_STORED_PENDING_INTR_TRANSPORT',
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
          intr_transport_intent: transportIntent,
          intr_materialization_request: staged.materializationRequest,
          intr_materialization_state: 'QUEUED_FOR_EVENT_EPHEMERAL_MATERIALIZATION',
          local_pretransport_staged: true,
          automatic_transport_retry: true,
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
        status.textContent = 'The InTr operation was initiated and its exact packet is retained locally. Transport will retry from the same hash-bound intent when a StegOS ingress path is available; no receiver or custody receipt is claimed until the receiving Interlock returns the chained receipts.';
        location.assign(`hil-receipt.html?submission_id=${encodeURIComponent(record.submission_id)}`);
      }
    } catch (error) {
      status.dataset.state = 'error';
      status.textContent = `The response could not be processed: ${error && error.message ? error.message : 'unknown_error'}`;
      button.disabled = false;
    }
  }, true);
})();
