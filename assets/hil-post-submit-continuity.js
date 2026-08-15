(() => {
  'use strict';

  const params = new URLSearchParams(window.location.search);
  const submissionId = params.get('submission_id');
  const byId = (id) => document.getElementById(id);
  let responseObjectUrl = null;

  async function sha256Hex(buffer) {
    const digest = await crypto.subtle.digest('SHA-256', buffer);
    return Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, '0')).join('');
  }

  function saveJson(value, filename) {
    const blob = new Blob([`${JSON.stringify(value, null, 2)}\n`], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  function renderHistory() {
    const target = byId('submission-history');
    let rows = [];
    try { rows = JSON.parse(localStorage.getItem('stegverse.hil.submissions.v1') || '[]'); } catch {}
    target.replaceChildren();
    if (!rows.length) {
      target.textContent = 'No additional submissions are recorded in this browser.';
      return;
    }
    rows.forEach((row) => {
      if (!row || !row.submission_id) return;
      const article = document.createElement('article');
      article.className = 'history-item';
      const link = document.createElement('a');
      link.href = row.durable_submission === true
        ? `hil-accepted.html?submission_id=${encodeURIComponent(row.submission_id)}`
        : `hil-receipt.html?submission_id=${encodeURIComponent(row.submission_id)}`;
      link.textContent = row.submission_id;
      const details = document.createElement('div');
      details.className = 'muted';
      details.textContent = `${row.received_at || row.recorded_at || 'time unavailable'} · ${row.submitted_file_sha256 || row.response_sha256 || 'hash unavailable'}`;
      article.append(link, details);
      target.appendChild(article);
    });
  }

  function buildResultPacket(receipt, retrievedHash, byteLength) {
    return {
      schema_version: 'HIL-SUBMISSION-RESULT-PACKET-v1',
      submission_id: receipt.submission_id,
      receipt_id: receipt.receipt_id || null,
      received_at: receipt.received_at || null,
      response: {
        submitted_sha256: receipt.submitted_file_sha256,
        retrieved_sha256: retrievedHash,
        byte_size: byteLength,
        exact_byte_verification: retrievedHash === receipt.submitted_file_sha256 ? 'PASS' : 'FAIL'
      },
      provenance: {
        primary_sha256: receipt.primary_sha256 || null,
        prompt_sha256: receipt.prompt_sha256 || null,
        chain_validation_state: receipt.chain_validation_state || null
      },
      lifecycle: {
        receiver_state: 'ACCEPTED',
        custody_state: receipt.custody_state || null,
        registry_state: receipt.registry_state || null,
        review_state: receipt.review_state || 'PENDING',
        publication_state: receipt.publication_state || 'NOT_AUTHORIZED',
        next_stage: 'PRIVATE_REVIEW_PENDING'
      },
      authority: {
        receiver_custody_evidence: true,
        private_review_authorized: false,
        publication_authorized: false,
        release_authorized: false,
        master_record_append_authorized: false,
        execution_authorized: false
      }
    };
  }

  async function init() {
    renderHistory();
    const packetState = byId('result-packet-state');
    const packetBody = byId('result-packet-body');
    const receiptBody = byId('receipt-body');
    const frame = byId('response-pdf');

    if (!submissionId) {
      packetState.dataset.state = 'error';
      packetState.textContent = 'No submission ID was supplied. No governed result packet can be shown.';
      packetBody.textContent = 'No verified submission-result packet is available.';
      receiptBody.textContent = 'No verified receiver receipt is available.';
      frame.removeAttribute('src');
      return;
    }

    try {
      packetState.dataset.state = 'warn';
      packetState.textContent = `Verifying ${submissionId} against the governed receiver…`;

      const statusResponse = await fetch(`/api/hil/submissions/${encodeURIComponent(submissionId)}`, {
        cache: 'no-store', credentials: 'same-origin', headers: { Accept: 'application/json' }
      });
      if (!statusResponse.ok) throw new Error('submission_status_unavailable');
      const status = await statusResponse.json();
      const receipt = status.receipt;
      if (
        !receipt ||
        receipt.schema_version !== 'HIL-RECEIVER-RECEIPT-v2' ||
        receipt.submission_id !== submissionId ||
        status.state !== 'ACCEPTED' ||
        receipt.custody_state !== 'EXACT_BYTES_PERSISTED' ||
        receipt.registry_state !== 'RECORDED'
      ) {
        throw new Error('accepted_receipt_invalid');
      }

      const contentResponse = await fetch(`/api/hil/submissions/${encodeURIComponent(submissionId)}/content`, {
        cache: 'no-store', credentials: 'same-origin'
      });
      if (!contentResponse.ok) throw new Error('stored_packet_unavailable');
      const buffer = await contentResponse.arrayBuffer();
      const retrievedHash = await sha256Hex(buffer);
      if (retrievedHash !== receipt.submitted_file_sha256) throw new Error('retrieved_packet_hash_mismatch');

      const resultPacket = buildResultPacket(receipt, retrievedHash, buffer.byteLength);
      packetBody.textContent = JSON.stringify(resultPacket, null, 2);
      receiptBody.textContent = JSON.stringify(receipt, null, 2);
      packetState.dataset.state = 'ok';
      packetState.textContent = `${submissionId} received. The prepended result packet is bound to an independently retrieved PDF with matching SHA-256.`;

      responseObjectUrl = URL.createObjectURL(new Blob([buffer], { type: 'application/pdf' }));
      frame.src = responseObjectUrl;

      const downloadReceipt = byId('download-receipt');
      downloadReceipt.disabled = false;
      downloadReceipt.addEventListener('click', () => saveJson(receipt, `${receipt.receipt_id || submissionId}.json`));
      const downloadPacket = byId('download-result-packet');
      downloadPacket.disabled = false;
      downloadPacket.addEventListener('click', () => saveJson(resultPacket, `${submissionId}.submission-result.json`));
    } catch (error) {
      packetState.dataset.state = 'error';
      packetState.textContent = `Result-packet verification failed: ${error.message || 'unknown_error'}.`;
      packetBody.textContent = 'No verified submission-result packet is available.';
      receiptBody.textContent = 'No verified receiver receipt is available.';
      frame.removeAttribute('src');
    }
  }

  window.addEventListener('beforeunload', () => {
    if (responseObjectUrl) URL.revokeObjectURL(responseObjectUrl);
  });

  init();
})();
