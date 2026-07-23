(() => {
  'use strict';

  const PRIMARY = Object.freeze({
    title: 'Humans as the Interoperability Layer',
    version: 'v0.5',
    protocolVersion: 'HIL-PROTOCOL-v1.0',
    promptVersion: 'HIL-PROMPT-v1.0',
    promptSha256: '0ebe215318b4eeeb8ed6422e0954372c314fadc8fac9254e452bc7670a1b9922',
    sha256: '52102cccb9ba9016c76434a64e22031b6a8c3edd3b8806e7b664e609216b2946',
    filename: 'Humans_as_the_Interoperability_Layer_Primary_Review_Candidate_v0_5.pdf',
    base64Path: 'data/hil-primary-v0.5-review.pdf.b64'
  });
  const GATEWAY = Object.freeze({
    baseUrl: 'https://stegverse-ecosystem-chat-gateway.onrender.com',
    readinessPath: '/api/hil/readiness',
    submissionPath: '/api/hil/submissions'
  });

  const byId = (id) => document.getElementById(id);
  const status = byId('intake-status');
  const submitButton = byId('prepare-receipt');
  const provenanceButton = byId('download-provenance');
  const receiptButton = byId('download-receipt');
  let gatewayReady = false;
  let currentManifest = null;
  let currentReceipt = null;

  function setStatus(state, message) {
    status.dataset.state = state;
    status.textContent = message;
  }

  async function sha256Hex(buffer) {
    const digest = await crypto.subtle.digest('SHA-256', buffer);
    return Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, '0')).join('');
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
      gatewayReady = payload.state === 'READY'
        && payload.primary_sha256 === PRIMARY.sha256
        && payload.prompt_sha256 === PRIMARY.promptSha256
        && payload.provenance_manifest_required === true;
      submitButton.textContent = gatewayReady ? 'Validate chain and submit artifacts' : 'Prepare provenance locally';
      if (gatewayReady) {
        setStatus('ok', 'Gateway chain intake is READY. Primary and prompt hashes match this Site version.');
      } else {
        setStatus('warn', `Gateway is not ready for this chain (${(payload.blockers || []).join(', ') || payload.state}). You may prepare and download the provenance manifest locally, but no submission will occur.`);
      }
    } catch (error) {
      gatewayReady = false;
      submitButton.textContent = 'Prepare provenance locally';
      setStatus('warn', `Gateway could not be reached. Local provenance preparation remains available: ${error.message}`);
    }
  }

  async function downloadPrimary() {
    const button = byId('download-primary');
    const previous = button.textContent;
    button.disabled = true;
    button.textContent = 'Preparing Primary PDF…';
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
    if (new TextDecoder('ascii').decode(bytes.slice(0, 5)) !== '%PDF-') return 'The selected file does not have a valid PDF signature.';
    return null;
  }

  function buildManifest(responseHash) {
    return {
      schema_version: 'HIL-RESPONSE-PROVENANCE-v1',
      primary_version: PRIMARY.version,
      primary_sha256: PRIMARY.sha256,
      protocol_version: PRIMARY.protocolVersion,
      prompt_version: PRIMARY.promptVersion,
      prompt_sha256: PRIMARY.promptSha256,
      response_sha256: responseHash,
      model: byId('model').value.trim(),
      provider: byId('provider').value.trim(),
      generated_at: new Date().toISOString(),
      conversation_reference: byId('conversation-reference').value.trim() || null,
      producer_signature: {
        state: 'UNAVAILABLE',
        scheme: null,
        value: null,
        key_id: null
      }
    };
  }

  async function submitArtifacts(file, manifest) {
    const form = new FormData();
    form.append('response_pdf', file, file.name);
    form.append('provenance_manifest', new Blob([`${JSON.stringify(manifest, null, 2)}\n`], { type: 'application/json' }), `${file.name}.provenance.json`);
    form.append('participant_identifier', byId('participant-id').value.trim() || 'anonymous');
    form.append('publication_consent', byId('publication-consent').value);
    form.append('primary_sha256', PRIMARY.sha256);
    form.append('model_response_declared_unedited', String(byId('unedited-confirmation').checked));
    form.append('participant_consent_authority_acknowledged', String(byId('participant-authority').checked));
    const response = await fetch(`${GATEWAY.baseUrl}${GATEWAY.submissionPath}`, { method: 'POST', body: form });
    const payload = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(typeof payload.detail === 'string' ? payload.detail : `gateway submission ${response.status}`);
    return payload;
  }

  async function prepareAndSubmit() {
    currentManifest = null;
    currentReceipt = null;
    provenanceButton.disabled = true;
    receiptButton.disabled = true;
    const file = byId('response-file').files[0];
    const model = byId('model').value.trim();
    const provider = byId('provider').value.trim();
    const consent = byId('publication-consent').value;
    if (!file) return setStatus('error', 'Select the Response PDF generated by the LLM.');
    if (!model || !provider) return setStatus('error', 'Model name and provider are required for the provenance chain.');
    if (!consent) return setStatus('error', 'Select a publication-consent state.');
    if (!byId('unedited-confirmation').checked) return setStatus('error', 'Confirm that the model-response portion remained unedited.');
    if (!byId('participant-authority').checked) return setStatus('error', 'Confirm that participant consent is separate from LLM output.');

    submitButton.disabled = true;
    try {
      setStatus('warn', 'Validating PDF and building Primary → prompt → response chain…');
      const buffer = await file.arrayBuffer();
      const bytes = new Uint8Array(buffer);
      const error = validatePdf(file, bytes);
      if (error) return setStatus('error', error);
      const responseHash = await sha256Hex(buffer);
      currentManifest = buildManifest(responseHash);
      provenanceButton.disabled = false;
      if (!gatewayReady) {
        setStatus('warn', `Provenance manifest prepared locally. Response SHA-256: ${responseHash}. Gateway submission remains blocked until the exact Primary and prompt chain is READY.`);
        return;
      }
      setStatus('warn', 'Chain matches locally. Uploading exact PDF bytes and provenance manifest…');
      currentReceipt = await submitArtifacts(file, currentManifest);
      receiptButton.disabled = false;
      setStatus('ok', `${currentReceipt.submission_id} received. ${currentReceipt.chain_validation_state}. Receiver SHA-256: ${currentReceipt.submitted_file_sha256}. Review and publication remain pending.`);
    } catch (error) {
      setStatus('error', error.message || 'The artifact chain could not be processed.');
    } finally {
      submitButton.disabled = false;
    }
  }

  function downloadProvenance() {
    if (!currentManifest) return;
    saveBlob(new Blob([`${JSON.stringify(currentManifest, null, 2)}\n`], { type: 'application/json' }), `HIL-${currentManifest.response_sha256.slice(0, 12)}.provenance.json`);
  }

  function downloadReceipt() {
    if (!currentReceipt) return;
    saveBlob(new Blob([`${JSON.stringify(currentReceipt, null, 2)}\n`], { type: 'application/json' }), `${currentReceipt.receipt_id || currentReceipt.submission_id}.json`);
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
    summary.appendChild(text(`${record.model || 'Unknown model'} · ${record.provider || 'Unknown provider'} · ${record.chain_validation_state || record.publication_state || 'unknown state'}`));
    article.appendChild(summary);
    if (record.response_id) {
      const link = document.createElement('a');
      link.className = 'sv-btn sv-btn-secondary';
      link.href = `humans-as-interoperability-response.html?id=${encodeURIComponent(record.response_id)}`;
      link.textContent = 'Inspect response record';
      article.appendChild(link);
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
        target.appendChild(text('No standardized public responses have been published. HIL-TRACE-0001 remains the approved initiating pre-protocol observation.'));
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
  submitButton.addEventListener('click', prepareAndSubmit);
  provenanceButton.addEventListener('click', downloadProvenance);
  receiptButton.addEventListener('click', downloadReceipt);
  checkGatewayReadiness();
  loadResponseIndex();
})();
