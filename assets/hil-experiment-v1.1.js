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

  const RECEIVER_CONFIG_PATH = 'data/hil-receiver-config.json';
  const DEFAULT_READINESS_PATH = '/api/hil/readiness';
  const DEFAULT_SUBMISSION_PATH = '/api/hil/submissions';
  const READY_MESSAGE = 'Response-packet intake is ready. Choose the unchanged PDF and tap Upload Response Packet.';
  const NOT_READY_MESSAGE = 'The governed receiver is not currently ready. Your packet has not been uploaded. Please try again later.';

  const byId = (id) => document.getElementById(id);
  const status = byId('intake-status');
  const uploadButton = byId('upload-response');
  const prepareButton = byId('prepare-provenance');
  const provenanceButton = byId('download-provenance');
  const receiptButton = byId('download-receipt');
  let receiver = null;
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

  async function fetchWithTimeout(url, options = {}, timeoutMs = 20000) {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), timeoutMs);
    try {
      return await fetch(url, { ...options, signal: controller.signal });
    } finally {
      clearTimeout(timeout);
    }
  }

  function normalizeBaseUrl(value) {
    if (typeof value !== 'string' || !value.trim()) return null;
    try {
      const url = new URL(value.trim(), window.location.href);
      if (!['https:', 'http:'].includes(url.protocol)) return null;
      return url.href.replace(/\/$/, '');
    } catch {
      return null;
    }
  }

  async function loadReceiverConfig() {
    const response = await fetchWithTimeout(RECEIVER_CONFIG_PATH, { cache: 'no-store' }, 10000);
    if (!response.ok) throw new Error('receiver_config_unavailable');
    const config = await response.json();
    const baseUrl = normalizeBaseUrl(config.receiver_base_url);
    if (!baseUrl) throw new Error('receiver_config_invalid');
    return {
      baseUrl,
      readinessPath: config.readiness_path || DEFAULT_READINESS_PATH,
      submissionPath: config.submission_path || DEFAULT_SUBMISSION_PATH
    };
  }

  async function readinessAttempt(candidate, timeoutMs) {
    const response = await fetchWithTimeout(
      `${candidate.baseUrl}${candidate.readinessPath}`,
      { cache: 'no-store' },
      timeoutMs
    );
    if (!response.ok) return false;
    const payload = await response.json();
    return payload.state === 'READY'
      && payload.primary_sha256 === PRIMARY.sha256
      && payload.prompt_sha256 === PRIMARY.promptSha256
      && payload.provenance_manifest_required === true;
  }

  async function checkGatewayReadiness() {
    receiver = null;
    uploadButton.disabled = true;
    setStatus('warn', 'Checking governed receiver availability…');
    try {
      const candidate = await loadReceiverConfig();
      const attempts = [12000, 30000];
      for (const timeoutMs of attempts) {
        try {
          if (await readinessAttempt(candidate, timeoutMs)) {
            receiver = candidate;
            setStatus('ok', READY_MESSAGE);
            uploadButton.disabled = false;
            return;
          }
        } catch {
          // A sleeping or restarting receiver may miss the first attempt.
        }
      }
    } catch {
      // Participant-facing output intentionally omits provider and network details.
    }
    uploadButton.disabled = false;
    setStatus('warn', NOT_READY_MESSAGE);
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
    if (!file) return 'Choose the single Response PDF generated by the LLM.';
    if (file.size === 0) return 'The selected file is empty.';
    if (file.size > 10 * 1024 * 1024) return 'The selected file exceeds the 10 MB limit.';
    if (!file.name.toLowerCase().endsWith('.pdf')) return 'The selected artifact must use the .pdf extension.';
    if (new TextDecoder('ascii').decode(bytes.slice(0, 5)) !== '%PDF-') return 'The selected artifact does not have a valid PDF signature.';
    return null;
  }

  function optionalValue(id) {
    const value = byId(id).value.trim();
    return value || null;
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
      model: optionalValue('model'),
      provider: optionalValue('provider'),
      generated_at: new Date().toISOString(),
      conversation_reference: optionalValue('conversation-reference'),
      participant_delivery_contract: {
        single_downloadable_pdf: true,
        visible_summary_expected: true,
        participant_conversion_required: false
      },
      participant_optional_metadata: {
        participant_identifier: optionalValue('participant-id'),
        publication_consent: byId('publication-consent').value || null,
        model_response_declared_unedited: byId('unedited-confirmation').checked || null,
        participant_consent_authority_acknowledged: byId('participant-authority').checked || null
      },
      producer_signature: { state: 'UNAVAILABLE', scheme: null, value: null, key_id: null }
    };
  }

  async function readAndValidateSelectedPdf() {
    const file = byId('response-file').files[0];
    if (!file) throw new Error('Choose the single downloadable Response PDF generated by the LLM.');
    const buffer = await file.arrayBuffer();
    const bytes = new Uint8Array(buffer);
    const validationError = validatePdf(file, bytes);
    if (validationError) throw new Error(validationError);
    return { file, responseHash: await sha256Hex(buffer) };
  }

  async function submitArtifacts(file, manifest) {
    if (!receiver) throw new Error(NOT_READY_MESSAGE);
    const form = new FormData();
    form.append('response_pdf', file, file.name);
    form.append('provenance_manifest', new Blob([`${JSON.stringify(manifest, null, 2)}\n`], { type: 'application/json' }), `${file.name}.provenance.json`);
    form.append('participant_identifier', optionalValue('participant-id') || 'not_provided');
    form.append('publication_consent', byId('publication-consent').value || 'not_provided');
    form.append('primary_sha256', PRIMARY.sha256);
    form.append('prompt_sha256', PRIMARY.promptSha256);
    form.append('model_response_declared_unedited', String(byId('unedited-confirmation').checked));
    form.append('participant_consent_authority_acknowledged', String(byId('participant-authority').checked));
    const response = await fetchWithTimeout(
      `${receiver.baseUrl}${receiver.submissionPath}`,
      { method: 'POST', body: form },
      60000
    );
    const payload = await response.json().catch(() => ({}));
    if (!response.ok) {
      console.warn('HIL upload rejected', { status: response.status, detail: payload.detail || null });
      throw new Error('The governed receiver did not accept the packet. Nothing was recorded. Please try again later.');
    }
    return payload;
  }

  async function uploadResponsePacket() {
    currentReceipt = null;
    receiptButton.disabled = true;
    uploadButton.disabled = true;
    try {
      setStatus('warn', 'Validating and uploading the unchanged response packet…');
      const { file, responseHash } = await readAndValidateSelectedPdf();
      currentManifest = buildManifest(responseHash);
      provenanceButton.disabled = false;
      if (!receiver) await checkGatewayReadiness();
      currentReceipt = await submitArtifacts(file, currentManifest);
      receiptButton.disabled = false;
      setStatus('ok', `${currentReceipt.submission_id} received. Receiver SHA-256: ${currentReceipt.submitted_file_sha256}. Review and publication remain pending.`);
    } catch (error) {
      const message = error && error.message ? error.message : 'The response packet could not be uploaded.';
      setStatus('error', message);
    } finally {
      uploadButton.disabled = false;
    }
  }

  async function prepareProvenanceLocally() {
    currentManifest = null;
    provenanceButton.disabled = true;
    prepareButton.disabled = true;
    try {
      setStatus('warn', 'Validating the selected PDF and preparing optional provenance locally…');
      const { responseHash } = await readAndValidateSelectedPdf();
      currentManifest = buildManifest(responseHash);
      provenanceButton.disabled = false;
      setStatus('ok', `Optional provenance prepared locally. Response SHA-256: ${responseHash}. No upload occurred.`);
    } catch (error) {
      setStatus('error', error.message || 'Optional provenance could not be prepared.');
    } finally {
      prepareButton.disabled = false;
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
  uploadButton.addEventListener('click', uploadResponsePacket);
  prepareButton.addEventListener('click', prepareProvenanceLocally);
  provenanceButton.addEventListener('click', downloadProvenance);
  receiptButton.addEventListener('click', downloadReceipt);
  checkGatewayReadiness();
  loadResponseIndex();
})();
