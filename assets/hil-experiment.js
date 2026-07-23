(() => {
  'use strict';

  const PRIMARY = Object.freeze({
    title: 'Humans as the Interoperability Layer',
    version: 'v0.4',
    protocolVersion: 'HIL-PROTOCOL-v1.0',
    promptVersion: 'HIL-PROMPT-v1.0',
    sha256: '97df3006c8d96212560c5fa970dc7bceac66bde23a8b23373491c030ccc0049d',
    filename: 'Humans_as_the_Interoperability_Layer_Canonical_Input_v0_4.pdf',
    base64Path: 'data/hil-primary-v0.4.pdf.b64'
  });
  const GATEWAY = Object.freeze({
    baseUrl: 'https://stegverse-ecosystem-chat-gateway.onrender.com',
    readinessPath: '/api/hil/readiness',
    submissionPath: '/api/hil/submissions'
  });

  const byId = (id) => document.getElementById(id);
  const status = byId('intake-status');
  const prepareButton = byId('prepare-receipt');
  const downloadReceiptButton = byId('download-receipt');
  let currentReceipt = null;
  let gatewayReady = false;

  function setStatus(state, message) {
    status.dataset.state = state;
    status.textContent = message;
  }

  async function sha256Hex(buffer) {
    const digest = await crypto.subtle.digest('SHA-256', buffer);
    return Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, '0')).join('');
  }

  function uuid() {
    if (crypto.randomUUID) return crypto.randomUUID();
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (char) => {
      const value = Math.random() * 16 | 0;
      return (char === 'x' ? value : (value & 0x3 | 0x8)).toString(16);
    });
  }

  function saveBlob(blob, filename) {
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
  }

  async function checkGatewayReadiness() {
    try {
      const response = await fetch(`${GATEWAY.baseUrl}${GATEWAY.readinessPath}`, { cache: 'no-store' });
      if (!response.ok) throw new Error(`readiness ${response.status}`);
      const payload = await response.json();
      gatewayReady = payload.state === 'READY' && payload.primary_sha256 === PRIMARY.sha256;
      prepareButton.textContent = gatewayReady ? 'Upload Response PDF and receive receipt' : 'Verify PDF and prepare local receipt';
      if (gatewayReady) setStatus('ok', 'Governed Site intake is ready. Your PDF will be transmitted, preserved, receiver-hashed, and returned with a pending-validation receipt.');
      else setStatus('warn', `Governed intake is not ready (${(payload.blockers || []).join(', ') || payload.state}). Browser-local receipt fallback remains available.`);
    } catch (error) {
      gatewayReady = false;
      prepareButton.textContent = 'Verify PDF and prepare local receipt';
      setStatus('warn', `Governed intake could not be reached. Browser-local receipt fallback remains available: ${error.message}`);
    }
  }

  async function downloadPrimary() {
    const button = byId('download-primary');
    const previous = button.textContent;
    button.disabled = true;
    button.textContent = 'Preparing PDF…';
    try {
      const response = await fetch(PRIMARY.base64Path, { cache: 'no-store' });
      if (!response.ok) throw new Error(`Primary artifact unavailable (${response.status})`);
      const encoded = (await response.text()).replace(/\s+/g, '');
      const binary = atob(encoded);
      const bytes = new Uint8Array(binary.length);
      for (let index = 0; index < binary.length; index += 1) bytes[index] = binary.charCodeAt(index);
      const actualHash = await sha256Hex(bytes.buffer);
      if (actualHash !== PRIMARY.sha256) throw new Error('Primary artifact hash mismatch; download blocked fail-closed.');
      saveBlob(new Blob([bytes], { type: 'application/pdf' }), PRIMARY.filename);
    } catch (error) {
      setStatus('error', error.message || 'Unable to prepare the Primary PDF.');
    } finally {
      button.disabled = false;
      button.textContent = previous;
    }
  }

  async function copyPrompt() {
    const prompt = byId('canonical-prompt').textContent.trim();
    try {
      await navigator.clipboard.writeText(prompt);
      const button = byId('copy-prompt');
      const old = button.textContent;
      button.textContent = 'Copied';
      setTimeout(() => { button.textContent = old; }, 1500);
    } catch {
      setStatus('warn', 'Copy was blocked by the browser. Select and copy the prompt manually.');
    }
  }

  function validatePdf(file, bytes) {
    if (!file) return 'Select a Response PDF.';
    if (file.size === 0) return 'The selected file is empty.';
    if (file.size > 10 * 1024 * 1024) return 'The selected file exceeds the 10 MB limit.';
    if (!file.name.toLowerCase().endsWith('.pdf')) return 'The selected file must use the .pdf extension.';
    const header = new TextDecoder('ascii').decode(bytes.slice(0, 5));
    if (header !== '%PDF-') return 'The selected file does not have a valid PDF signature.';
    return null;
  }

  function browserReceipt(file, participantId, contact, consent, unedited, authority, responseHash) {
    const createdAt = new Date().toISOString();
    const intakeId = `HIL-INTAKE-${createdAt.slice(0, 10).replaceAll('-', '')}-${uuid().slice(0, 8).toUpperCase()}`;
    return {
      schema: 'https://stegverse.org/schemas/hil-intake-receipt-v1.json',
      schema_version: 'HIL-SUBMISSION-v1',
      submission_id: intakeId,
      intake_id: intakeId,
      state: 'BROWSER_LOCAL_PREPARED_NOT_SUBMITTED',
      created_at: createdAt,
      received_at: null,
      primary: { title: PRIMARY.title, version: PRIMARY.version, sha256: PRIMARY.sha256, protocol_version: PRIMARY.protocolVersion, prompt_version: PRIMARY.promptVersion },
      response_artifact: { original_filename: file.name, media_type: 'application/pdf', size_bytes: file.size, browser_verified_sha256: responseHash, receiver_verified_sha256: null, public_artifact_path: null },
      participant: { identifier: participantId, contact: contact || null, publication_consent: consent, model_response_declared_unedited: unedited, participant_consent_authority_acknowledged: authority },
      validation: { pdf_signature: 'PASS', primary_reference: 'UNKNOWN', prompt_integrity: 'UNKNOWN', active_content: 'UNKNOWN', malware_scan: 'NOT_RUN', notes: ['Browser-local fallback; receiver validation has not occurred.'] },
      authority: { transmitted: false, custodied: false, accepted: false, published: false, master_record_appended: false },
      previous_record_sha256: null,
      record_sha256: null
    };
  }

  async function submitToGateway(file, participantId, consent, unedited, authority) {
    const form = new FormData();
    form.append('response_pdf', file, file.name);
    form.append('participant_identifier', participantId);
    form.append('publication_consent', consent);
    form.append('primary_sha256', PRIMARY.sha256);
    form.append('model_response_declared_unedited', String(unedited));
    form.append('participant_consent_authority_acknowledged', String(authority));
    const response = await fetch(`${GATEWAY.baseUrl}${GATEWAY.submissionPath}`, { method: 'POST', body: form });
    const payload = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(typeof payload.detail === 'string' ? payload.detail : `gateway submission ${response.status}`);
    return payload;
  }

  async function prepareReceipt() {
    currentReceipt = null;
    downloadReceiptButton.disabled = true;
    const file = byId('response-file').files[0];
    const participantId = byId('participant-id').value.trim() || 'anonymous';
    const contact = byId('contact').value.trim();
    const consent = byId('publication-consent').value;
    const unedited = byId('unedited-confirmation').checked;
    const authority = byId('participant-authority').checked;
    if (!file) return setStatus('error', 'Select the Response PDF generated by the LLM.');
    if (!consent) return setStatus('error', 'Select a publication-consent state.');
    if (!unedited) return setStatus('error', 'Confirm whether the model-response portion remained unedited.');
    if (!authority) return setStatus('error', 'Confirm that participant consent is separate from LLM output.');

    prepareButton.disabled = true;
    setStatus('warn', gatewayReady ? 'Validating locally, then transmitting to governed intake…' : 'Reading and hashing the selected PDF locally…');
    try {
      const buffer = await file.arrayBuffer();
      const bytes = new Uint8Array(buffer);
      const validationError = validatePdf(file, bytes);
      if (validationError) return setStatus('error', validationError);
      const responseHash = await sha256Hex(buffer);
      if (gatewayReady) {
        currentReceipt = await submitToGateway(file, participantId, consent, unedited, authority);
        downloadReceiptButton.disabled = false;
        setStatus('ok', `${currentReceipt.submission_id} received. Receiver SHA-256: ${currentReceipt.submitted_file_sha256}. Validation and publication remain pending.`);
      } else {
        const receiptCore = browserReceipt(file, participantId, contact, consent, unedited, authority, responseHash);
        currentReceipt = { ...receiptCore, receipt_content_sha256: await sha256Hex(new TextEncoder().encode(JSON.stringify(receiptCore))) };
        downloadReceiptButton.disabled = false;
        setStatus('ok', `${currentReceipt.intake_id} prepared locally. PDF SHA-256: ${responseHash}. Download the receipt and use the fallback return channel.`);
      }
    } catch (error) {
      setStatus('error', error.message || 'The selected PDF could not be processed.');
    } finally {
      prepareButton.disabled = false;
    }
  }

  function downloadReceipt() {
    if (!currentReceipt) return;
    const id = currentReceipt.receipt_id || currentReceipt.intake_id || currentReceipt.submission_id || 'HIL-receipt';
    saveBlob(new Blob([`${JSON.stringify(currentReceipt, null, 2)}\n`], { type: 'application/json' }), `${id}.json`);
  }

  function text(value) { return document.createTextNode(value == null ? 'unknown' : String(value)); }

  function responseCard(record) {
    const article = document.createElement('article');
    article.className = 'sv-card';
    const heading = document.createElement('h3');
    heading.className = 'sv-h3';
    heading.appendChild(text(record.response_id));
    article.appendChild(heading);
    const summary = document.createElement('p');
    summary.appendChild(text(`${record.model || 'Unknown model'} · ${record.provider || 'Unknown provider'} · ${record.publication_state || 'unknown state'}`));
    article.appendChild(summary);
    if (record.artifact_path) {
      const actions = document.createElement('div');
      actions.className = 'hil-actions';
      const link = document.createElement('a');
      link.className = 'sv-btn sv-btn-secondary';
      link.href = record.artifact_path;
      link.textContent = 'Open Response PDF';
      actions.appendChild(link);
      article.appendChild(actions);
    }
    return article;
  }

  async function loadResponseIndex() {
    const target = byId('response-index');
    try {
      const response = await fetch('data/hil-responses.json', { cache: 'no-store' });
      if (!response.ok) throw new Error(`response index unavailable (${response.status})`);
      const index = await response.json();
      if (!Array.isArray(index.responses)) throw new Error('response index has invalid shape');
      target.replaceChildren();
      if (index.responses.length === 0) {
        target.className = 'hil-empty';
        target.appendChild(text(`No protocol-compliant public responses have been published yet. The initiating observational trace remains separately identified as ${index.initiating_trace.trace_id}.`));
        return;
      }
      target.className = '';
      index.responses.forEach((record) => target.appendChild(responseCard(record)));
    } catch (error) {
      target.className = 'hil-status';
      target.dataset.state = 'warn';
      target.textContent = `Public response index could not be loaded: ${error.message}`;
    }
  }

  byId('download-primary').addEventListener('click', downloadPrimary);
  byId('copy-prompt').addEventListener('click', copyPrompt);
  prepareButton.addEventListener('click', prepareReceipt);
  downloadReceiptButton.addEventListener('click', downloadReceipt);
  checkGatewayReadiness();
  loadResponseIndex();
})();
