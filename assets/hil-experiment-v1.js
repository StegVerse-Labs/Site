(() => {
  'use strict';

  const PRIMARY = Object.freeze({
    title: 'Humans as the Interoperability Layer',
    version: 'v1.0',
    protocolVersion: 'HIL-PROTOCOL-v1.0',
    promptVersion: 'HIL-PROMPT-v1.0',
    promptSha256: 'bbb2db652a10ef404d565e561bb0a2f7b078bbe95105400faec14be9a6d5642a',
    sha256: 'e7a86cf05323d8352cfa188e0bff1c35fdb15f9fac6af91ca62b6a126ac4e68f',
    filename: 'HIL_Canonical_Paper_v1_0.pdf',
    base64Path: 'data/hil-primary-v1.0.pdf.b64'
  });

  const CONFIG_PATH = 'data/hil-gateway-config.json';
  const byId = (id) => document.getElementById(id);
  const status = byId('intake-status');
  const submitButton = byId('prepare-receipt');
  const provenanceButton = byId('download-provenance');
  const receiptButton = byId('download-receipt');
  const fileInput = byId('response-file');
  const uploadBox = document.querySelector('.hil-upload');
  let selectedGateway = null;
  let currentManifest = null;
  let currentReceipt = null;

  function setStatus(state, message) {
    status.dataset.state = state;
    status.textContent = message;
  }

  function normalizeBaseUrl(value) {
    return String(value || '').replace(/\/$/, '');
  }

  async function fetchWithTimeout(url, options = {}, timeoutMs = 12000) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);
    try {
      return await fetch(url, { ...options, signal: controller.signal });
    } finally {
      clearTimeout(timer);
    }
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

  async function loadCanonicalBytes() {
    const response = await fetch(PRIMARY.base64Path, { cache: 'no-store' });
    if (!response.ok) throw new Error(`Canonical Primary unavailable (${response.status})`);
    const encoded = (await response.text()).replace(/\s+/g, '');
    const binary = atob(encoded);
    const bytes = new Uint8Array(binary.length);
    for (let index = 0; index < binary.length; index += 1) bytes[index] = binary.charCodeAt(index);
    const actualHash = await sha256Hex(bytes.buffer);
    if (actualHash !== PRIMARY.sha256) throw new Error(`Canonical Primary hash mismatch. Expected ${PRIMARY.sha256}; received ${actualHash}. Download blocked fail-closed.`);
    return bytes;
  }

  async function loadGatewayCandidates() {
    try {
      const response = await fetch(CONFIG_PATH, { cache: 'no-store' });
      if (!response.ok) throw new Error(`gateway config ${response.status}`);
      const config = await response.json();
      if (!Array.isArray(config.gateway_candidates) || config.gateway_candidates.length === 0) throw new Error('gateway candidate list is empty');
      return [...config.gateway_candidates].sort((a, b) => Number(a.priority || 999) - Number(b.priority || 999));
    } catch (error) {
      setStatus('warn', `Gateway configuration could not be loaded. Local provenance preparation remains available: ${error.message}`);
      return [];
    }
  }

  async function probeGateway(candidate) {
    const baseUrl = normalizeBaseUrl(candidate.base_url);
    const readinessUrl = `${baseUrl}${candidate.readiness_path}`;
    const response = await fetchWithTimeout(readinessUrl, { cache: 'no-store' });
    if (!response.ok) throw new Error(`readiness ${response.status}`);
    const payload = await response.json();
    const exactReady = payload.state === 'READY'
      && payload.primary_sha256 === PRIMARY.sha256
      && payload.prompt_sha256 === PRIMARY.promptSha256
      && payload.provenance_manifest_required === true;
    if (!exactReady) throw new Error((payload.blockers || []).join(', ') || payload.state || 'chain mismatch');
    return {
      id: candidate.id,
      baseUrl,
      submissionPath: candidate.submission_path,
      readiness: payload
    };
  }

  async function checkGatewayReadiness() {
    selectedGateway = null;
    submitButton.textContent = 'Checking exact v1.0 intake…';
    const candidates = await loadGatewayCandidates();
    const failures = [];
    for (const candidate of candidates) {
      try {
        selectedGateway = await probeGateway(candidate);
        break;
      } catch (error) {
        failures.push(`${candidate.id}: ${error.message}`);
      }
    }
    if (selectedGateway) {
      submitButton.textContent = 'Submit response PDF';
      setStatus('ok', `Upload intake is ready through ${selectedGateway.id}. Select the response PDF, complete the required fields, and submit once.`);
    } else {
      submitButton.textContent = 'Prepare provenance locally';
      setStatus('warn', `No exact canonical v1.0 gateway is ready. Local provenance preparation remains available.${failures.length ? ` Checked: ${failures.join(' · ')}` : ''}`);
    }
  }

  async function downloadPrimary() {
    const button = byId('download-primary');
    const previous = button.textContent;
    button.disabled = true;
    button.textContent = 'Verifying canonical v1.0…';
    try {
      const bytes = await loadCanonicalBytes();
      saveBlob(new Blob([bytes], { type: 'application/pdf' }), PRIMARY.filename);
      setStatus('ok', `Canonical v1.0 verified and prepared. SHA-256: ${PRIMARY.sha256}`);
    } catch (error) {
      setStatus('error', error.message || 'Unable to prepare the canonical Primary PDF.');
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
    if (!file) return 'Select the response-only PDF generated by the LLM.';
    if (file.size === 0) return 'The selected file is empty.';
    if (file.size > 10 * 1024 * 1024) return 'The selected file exceeds the 10 MB limit.';
    if (!file.name.toLowerCase().endsWith('.pdf')) return 'The selected response must use the .pdf extension.';
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
      producer_signature: { state: 'UNAVAILABLE', scheme: null, value: null, key_id: null }
    };
  }

  async function submitArtifacts(file, manifest) {
    if (!selectedGateway) throw new Error('No exact canonical v1.0 gateway is ready.');
    const form = new FormData();
    form.append('response_pdf', file, file.name);
    form.append('provenance_manifest', new Blob([`${JSON.stringify(manifest, null, 2)}\n`], { type: 'application/json' }), `${file.name}.provenance.json`);
    form.append('participant_identifier', byId('participant-id').value.trim() || 'anonymous');
    form.append('publication_consent', byId('publication-consent').value);
    form.append('primary_sha256', PRIMARY.sha256);
    form.append('model_response_declared_unedited', String(byId('unedited-confirmation').checked));
    form.append('participant_consent_authority_acknowledged', String(byId('participant-authority').checked));
    const response = await fetchWithTimeout(`${selectedGateway.baseUrl}${selectedGateway.submissionPath}`, { method: 'POST', body: form }, 45000);
    const payload = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(typeof payload.detail === 'string' ? payload.detail : `gateway submission ${response.status}`);
    return payload;
  }

  async function prepareAndSubmit() {
    currentManifest = null;
    currentReceipt = null;
    provenanceButton.disabled = true;
    receiptButton.disabled = true;
    const file = fileInput.files[0];
    const model = byId('model').value.trim();
    const provider = byId('provider').value.trim();
    const consent = byId('publication-consent').value;
    if (!file) return setStatus('error', 'Select or drop the response-only PDF generated by the LLM.');
    if (!model || !provider) return setStatus('error', 'Model name and provider are required for the provenance chain.');
    if (!consent) return setStatus('error', 'Select a publication-consent state.');
    if (!byId('unedited-confirmation').checked) return setStatus('error', 'Confirm that the model-response portion remained unedited.');
    if (!byId('participant-authority').checked) return setStatus('error', 'Confirm that participant consent is separate from LLM output.');

    submitButton.disabled = true;
    try {
      setStatus('warn', 'Hashing and validating the exact response PDF…');
      const buffer = await file.arrayBuffer();
      const bytes = new Uint8Array(buffer);
      const error = validatePdf(file, bytes);
      if (error) return setStatus('error', error);
      const responseHash = await sha256Hex(buffer);
      currentManifest = buildManifest(responseHash);
      provenanceButton.disabled = false;
      if (!selectedGateway) {
        setStatus('warn', `Provenance prepared locally. Response SHA-256: ${responseHash}. The PDF has not been submitted because no exact v1.0 gateway is ready.`);
        return;
      }
      setStatus('warn', 'Uploading the exact PDF and provenance record. Keep this page open until the receiver receipt appears…');
      currentReceipt = await submitArtifacts(file, currentManifest);
      receiptButton.disabled = false;
      setStatus('ok', `${currentReceipt.submission_id} received and preserved. ${currentReceipt.chain_validation_state}. Receiver SHA-256: ${currentReceipt.submitted_file_sha256}. Download the receipt for your records; review and publication remain separate.`);
    } catch (error) {
      const timeout = error.name === 'AbortError' ? 'The gateway timed out before issuing a receipt. No successful submission is being claimed.' : error.message;
      setStatus('error', timeout || 'The artifact chain could not be processed.');
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

  function handleSelectedFile(file) {
    if (!file) return;
    const transfer = new DataTransfer();
    transfer.items.add(file);
    fileInput.files = transfer.files;
    setStatus('warn', `${file.name} selected (${file.size.toLocaleString()} bytes). Complete the required fields and submit once.`);
    uploadBox.classList.remove('is-dragging');
  }

  function bindDropZone() {
    ['dragenter', 'dragover'].forEach((eventName) => uploadBox.addEventListener(eventName, (event) => {
      event.preventDefault();
      uploadBox.classList.add('is-dragging');
    }));
    ['dragleave', 'drop'].forEach((eventName) => uploadBox.addEventListener(eventName, (event) => {
      event.preventDefault();
      uploadBox.classList.remove('is-dragging');
    }));
    uploadBox.addEventListener('drop', (event) => handleSelectedFile(event.dataTransfer.files[0]));
    fileInput.addEventListener('change', () => handleSelectedFile(fileInput.files[0]));
  }

  async function loadResponseIndex() {
    const target = byId('response-index');
    try {
      const response = await fetch('data/hil-responses.json', { cache: 'no-store' });
      if (!response.ok) throw new Error(`response index unavailable (${response.status})`);
      const index = await response.json();
      if (!Array.isArray(index.responses)) throw new Error('response index has invalid shape');
      if (index.responses.length === 0) {
        target.textContent = 'No standardized public responses have been published. HIL-TRACE-0001 remains the approved initiating pre-protocol observation.';
        return;
      }
      target.replaceChildren(...index.responses.map((record) => {
        const article = document.createElement('article');
        article.className = 'sv-card';
        const heading = document.createElement('h3');
        heading.className = 'sv-h3';
        heading.textContent = record.response_id || 'unknown response';
        const summary = document.createElement('p');
        summary.textContent = `${record.model || 'Unknown model'} · ${record.provider || 'Unknown provider'} · ${record.chain_validation_state || record.publication_state || 'unknown state'}`;
        article.append(heading, summary);
        return article;
      }));
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
  bindDropZone();
  checkGatewayReadiness();
  loadResponseIndex();
})();
