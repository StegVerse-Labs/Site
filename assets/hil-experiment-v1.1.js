(() => {
  'use strict';

  const PRIMARY = Object.freeze({
    title: 'Humans as the Interoperability Layer',
    version: 'v1.1',
    protocolVersion: 'HIL-PROTOCOL-v1.1',
    promptVersion: 'HIL-PROMPT-v1.1',
    promptSha256: 'cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c',
    sha256: 'a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462',
    filename: 'HIL_Canonical_Paper_v1_1.pdf',
    artifactPath: 'data/HIL_Canonical_Paper_v1_1.pdf'
  });

  const GATEWAY_CANDIDATES = Object.freeze([
    '',
    'https://stegverse-ecosystem-chat-gateway.onrender.com'
  ]);
  const READINESS_PATH = '/api/hil/readiness';
  const SUBMISSION_PATH = '/api/hil/submissions';

  const byId = (id) => document.getElementById(id);
  const status = byId('intake-status');
  const submitButton = byId('prepare-receipt');
  const provenanceButton = byId('download-provenance');
  const receiptButton = byId('download-receipt');
  let activeGatewayBase = null;
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
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  async function fetchWithTimeout(url, options = {}, timeoutMs = 12000) {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), timeoutMs);
    try {
      return await fetch(url, { ...options, signal: controller.signal });
    } finally {
      clearTimeout(timeout);
    }
  }

  async function checkGatewayReadiness() {
    activeGatewayBase = null;
    const failures = [];
    for (const base of GATEWAY_CANDIDATES) {
      try {
        const response = await fetchWithTimeout(`${base}${READINESS_PATH}`, { cache: 'no-store' }, 7000);
        if (!response.ok) throw new Error(`readiness ${response.status}`);
        const payload = await response.json();
        const ready = payload.state === 'READY'
          && payload.primary_sha256 === PRIMARY.sha256
          && payload.prompt_sha256 === PRIMARY.promptSha256
          && payload.provenance_manifest_required === true;
        if (ready) {
          activeGatewayBase = base;
          submitButton.textContent = 'Validate chain and submit artifact';
          setStatus('ok', 'Gateway intake is READY for the exact HIL v1.1 Primary and prompt chain.');
          return;
        }
        failures.push(`${base || 'same-origin'}: ${(payload.blockers || []).join(', ') || payload.state}`);
      } catch (error) {
        failures.push(`${base || 'same-origin'}: ${error.message}`);
      }
    }
    submitButton.textContent = 'Prepare provenance locally';
    setStatus('warn', `No conforming HIL v1.1 gateway is currently ready. Local provenance preparation remains available. ${failures.join(' | ')}`);
  }

  async function downloadPrimary() {
    const button = byId('download-primary');
    const previous = button.textContent;
    button.disabled = true;
    button.textContent = 'Verifying Canonical v1.1 PDF…';
    try {
      const response = await fetchWithTimeout(PRIMARY.artifactPath, { cache: 'no-store' }, 15000);
      if (!response.ok) throw new Error(`Canonical Primary unavailable (${response.status})`);
      const buffer = await response.arrayBuffer();
      const bytes = new Uint8Array(buffer);
      if (bytes.byteLength !== 87271) throw new Error(`Canonical Primary size mismatch; expected 87271 bytes, received ${bytes.byteLength}.`);
      if (new TextDecoder('ascii').decode(bytes.slice(0, 5)) !== '%PDF-') throw new Error('Canonical Primary does not have a valid PDF signature; download blocked fail-closed.');
      const actualHash = await sha256Hex(buffer);
      if (actualHash !== PRIMARY.sha256) throw new Error(`Canonical Primary hash mismatch; expected ${PRIMARY.sha256}, received ${actualHash}. Download blocked fail-closed.`);
      saveBlob(new Blob([buffer], { type: 'application/pdf' }), PRIMARY.filename);
      setStatus('ok', `Canonical v1.1 Primary verified and downloaded. SHA-256: ${actualHash}`);
    } catch (error) {
      setStatus('error', error.message || 'Unable to download the Canonical v1.1 Primary.');
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
    if (!file) return 'Select the single Response PDF generated by the LLM.';
    if (file.size === 0) return 'The selected file is empty.';
    if (file.size > 10 * 1024 * 1024) return 'The selected file exceeds the 10 MB limit.';
    if (!file.name.toLowerCase().endsWith('.pdf')) return 'The selected artifact must use the .pdf extension.';
    if (new TextDecoder('ascii').decode(bytes.slice(0, 5)) !== '%PDF-') return 'The selected artifact does not have a valid PDF signature.';
    return null;
  }

  function buildManifest(responseHash) {
    return {
      schema_version: 'HIL-RESPONSE-PROVENANCE-v1.1',
      primary_version: PRIMARY.version,
      primary_filename: PRIMARY.filename,
      primary_sha256: PRIMARY.sha256,
      protocol_version: PRIMARY.protocolVersion,
      prompt_version: PRIMARY.promptVersion,
      prompt_sha256: PRIMARY.promptSha256,
      response_sha256: responseHash,
      model: byId('model').value.trim(),
      provider: byId('provider').value.trim(),
      generated_at: new Date().toISOString(),
      conversation_reference: byId('conversation-reference').value.trim() || null,
      participant_delivery_contract: {
        single_downloadable_pdf: true,
        visible_summary_expected: true,
        participant_conversion_required: false
      },
      producer_signature: { state: 'UNAVAILABLE', scheme: null, value: null, key_id: null }
    };
  }

  async function submitArtifacts(file, manifest) {
    if (activeGatewayBase === null) throw new Error('No conforming HIL v1.1 gateway is ready.');
    const form = new FormData();
    form.append('response_pdf', file, file.name);
    form.append('provenance_manifest', new Blob([`${JSON.stringify(manifest, null, 2)}\n`], { type: 'application/json' }), `${file.name}.provenance.json`);
    form.append('participant_identifier', byId('participant-id').value.trim() || 'anonymous');
    form.append('publication_consent', byId('publication-consent').value);
    form.append('primary_sha256', PRIMARY.sha256);
    form.append('prompt_sha256', PRIMARY.promptSha256);
    form.append('model_response_declared_unedited', String(byId('unedited-confirmation').checked));
    form.append('participant_consent_authority_acknowledged', String(byId('participant-authority').checked));
    const response = await fetchWithTimeout(`${activeGatewayBase}${SUBMISSION_PATH}`, { method: 'POST', body: form }, 30000);
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
    if (!file) return setStatus('error', 'Select the single downloadable Response PDF generated by the LLM.');
    if (!model || !provider) return setStatus('error', 'Model name and provider are required for the provenance chain.');
    if (!consent) return setStatus('error', 'Select a publication-consent state.');
    if (!byId('unedited-confirmation').checked) return setStatus('error', 'Confirm that the PDF remained unchanged after generation.');
    if (!byId('participant-authority').checked) return setStatus('error', 'Confirm that participant consent is separate from LLM output.');

    submitButton.disabled = true;
    try {
      setStatus('warn', 'Validating the single PDF and building the HIL v1.1 Primary → prompt → response chain…');
      const buffer = await file.arrayBuffer();
      const bytes = new Uint8Array(buffer);
      const error = validatePdf(file, bytes);
      if (error) return setStatus('error', error);
      const responseHash = await sha256Hex(buffer);
      currentManifest = buildManifest(responseHash);
      provenanceButton.disabled = false;
      if (activeGatewayBase === null) {
        setStatus('warn', `HIL v1.1 provenance manifest prepared locally. Response SHA-256: ${responseHash}. Gateway submission remains blocked until the exact v1.1 chain is READY.`);
        return;
      }
      setStatus('warn', 'HIL v1.1 chain matches locally. Uploading the exact single PDF and provenance manifest…');
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

  async function loadResponseIndex() {
    const target = byId('response-index');
    try {
      const response = await fetch('data/hil-responses.json', { cache: 'no-store' });
      if (!response.ok) throw new Error(`response index unavailable (${response.status})`);
      const index = await response.json();
      if (!Array.isArray(index.responses)) throw new Error('response index has invalid shape');
      target.replaceChildren();
      if (index.responses.length === 0) {
        target.textContent = 'No standardized public responses have been published. HIL-TRACE-0001 remains the approved initiating pre-protocol observation.';
        return;
      }
      index.responses.forEach((record) => {
        const article = document.createElement('article');
        article.className = 'sv-card';
        const heading = document.createElement('h3');
        heading.className = 'sv-h3';
        heading.textContent = record.response_id || 'unknown response';
        const summary = document.createElement('p');
        summary.textContent = `${record.model || 'Unknown model'} · ${record.provider || 'Unknown provider'} · ${record.chain_validation_state || record.publication_state || 'unknown state'}`;
        article.append(heading, summary);
        target.appendChild(article);
      });
    } catch (error) {
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