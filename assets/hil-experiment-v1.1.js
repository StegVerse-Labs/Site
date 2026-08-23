(() => {
  'use strict';

  const PRIMARY = Object.freeze({
    version: 'v1.1',
    protocolVersion: 'HIL-PROTOCOL-v1.1',
    promptVersion: 'HIL-PROMPT-v1.1',
    promptSha256: 'cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c',
    sha256: 'a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462',
    filename: 'HIL_Canonical_Paper_v1_1.pdf',
    artifactPath: 'data/HIL_Canonical_Paper_v1_1.pdf'
  });

  const RECEIVER_CONFIG_PATH = 'data/hil-receiver-config.json';
  const GATEWAY_CANDIDATES = Object.freeze([RECEIVER_CONFIG_PATH]);
  const READY_MESSAGE = 'Response-packet intake is ready. Choose the unchanged PDF and tap Upload Response Packet.';
  const NOT_READY_MESSAGE = 'The governed receiver is not currently ready. Your packet has not been uploaded. Please try again later.';
  const RECEIPT_PREFIX = 'stegverse.hil.receipt.';
  const MAX_BYTES = 10 * 1024 * 1024;

  const byId = (id) => document.getElementById(id);
  const status = byId('intake-status');
  const fileInput = byId('response-file');
  const uploadButton = byId('upload-response');
  const prepareButton = byId('prepare-provenance');
  const provenanceButton = byId('download-provenance');
  const receiptButton = byId('download-receipt');

  let receiver = null;
  let currentManifest = null;
  let currentReceipt = null;
  let readinessCheck = null;

  function setStatus(state, message) {
    status.dataset.state = state;
    status.textContent = message;
  }

  function setUploadState(enabled, label = 'Upload Response Packet') {
    uploadButton.disabled = !enabled;
    uploadButton.textContent = label;
  }

  async function sha256Hex(buffer) {
    const digest = await crypto.subtle.digest('SHA-256', buffer);
    return Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, '0')).join('');
  }

  function canonicalJson(value) {
    if (value === null || typeof value !== 'object') return JSON.stringify(value);
    if (Array.isArray(value)) return `[${value.map(canonicalJson).join(',')}]`;
    return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonicalJson(value[key])}`).join(',')}}`;
  }

  async function canonicalHash(value) {
    return sha256Hex(new TextEncoder().encode(canonicalJson(value)).buffer);
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
    const response = await fetchWithTimeout(GATEWAY_CANDIDATES[0], { cache: 'no-store' }, 10000);
    if (!response.ok) throw new Error('receiver_config_unavailable');
    const config = await response.json();
    const baseUrl = normalizeBaseUrl(config.receiver_base_url);
    if (!baseUrl) throw new Error('receiver_config_invalid');
    return {
      baseUrl,
      readinessPath: config.readiness_path || '/api/hil/readiness',
      submissionPath: config.submission_path || '/api/hil/submissions'
    };
  }

  async function receiverIsReady(candidate, timeoutMs) {
    const response = await fetchWithTimeout(
      `${candidate.baseUrl}${candidate.readinessPath}`,
      { cache: 'no-store' },
      timeoutMs
    );
    if (!response.ok) return false;
    const payload = await response.json();
    return payload.state === 'READY'
      && payload.primary_version === PRIMARY.version
      && payload.primary_sha256 === PRIMARY.sha256
      && payload.protocol_version === PRIMARY.protocolVersion
      && payload.prompt_version === PRIMARY.promptVersion
      && payload.prompt_sha256 === PRIMARY.promptSha256
      && payload.provenance_manifest_required === true
      && payload.provenance_manifest_schema === 'HIL-RESPONSE-PROVENANCE-v1.1'
      && payload.participant_metadata_required === false;
  }

  async function checkGatewayReadiness({ quiet = false } = {}) {
    if (readinessCheck) return readinessCheck;
    readinessCheck = (async () => {
      receiver = null;
      setUploadState(false, 'Checking intake…');
      if (!quiet) setStatus('warn', 'Checking governed receiver availability…');
      try {
        const candidate = await loadReceiverConfig();
        for (const timeoutMs of [12000, 30000]) {
          try {
            if (await receiverIsReady(candidate, timeoutMs)) {
              receiver = candidate;
              setUploadState(true);
              if (!quiet) setStatus('ok', READY_MESSAGE);
              return true;
            }
          } catch (error) {
            console.debug('HIL readiness attempt failed', error);
          }
        }
      } catch (error) {
        console.debug('HIL receiver discovery failed', error);
      }
      setUploadState(false, 'Upload unavailable');
      if (!quiet) setStatus('warn', NOT_READY_MESSAGE);
      return false;
    })();
    try {
      return await readinessCheck;
    } finally {
      readinessCheck = null;
    }
  }

  async function downloadPrimary() {
    const button = byId('download-primary');
    const prior = button.textContent;
    button.disabled = true;
    button.textContent = 'Verifying Canonical v1.1 PDF…';
    try {
      const response = await fetchWithTimeout(PRIMARY.artifactPath, { cache: 'no-store' }, 15000);
      if (!response.ok) throw new Error('The Canonical Primary is temporarily unavailable.');
      const buffer = await response.arrayBuffer();
      const bytes = new Uint8Array(buffer);
      if (bytes.byteLength !== 87271 || new TextDecoder('ascii').decode(bytes.slice(0, 5)) !== '%PDF-') {
        throw new Error('Canonical Primary verification failed. Download was blocked.');
      }
      const hash = await sha256Hex(buffer);
      if (hash !== PRIMARY.sha256) throw new Error('Canonical Primary verification failed. Download was blocked.');
      saveBlob(new Blob([buffer], { type: 'application/pdf' }), PRIMARY.filename);
      setStatus('ok', 'Canonical v1.1 Primary verified and downloaded.');
    } catch (error) {
      setStatus('error', error.message || 'Unable to download the Canonical v1.1 Primary.');
    } finally {
      button.disabled = false;
      button.textContent = prior;
    }
  }

  async function copyPrompt() {
    try {
      await navigator.clipboard.writeText(byId('canonical-prompt').textContent.trim());
      const button = byId('copy-prompt');
      const prior = button.textContent;
      button.textContent = 'Copied';
      setTimeout(() => { button.textContent = prior; }, 1500);
    } catch {
      setStatus('warn', 'Copy was blocked by the browser. Select and copy the prompt manually.');
    }
  }

  function validatePdf(file, bytes) {
    if (!file) return 'Choose the single Response PDF generated by the LLM.';
    if (file.size === 0) return 'The selected file is empty.';
    if (file.size > MAX_BYTES) return 'The selected file exceeds the 10 MB limit.';
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

  async function readSelectedPdf() {
    const file = fileInput.files[0];
    if (!file) throw new Error('Choose the single downloadable Response PDF generated by the LLM.');
    const buffer = await file.arrayBuffer();
    const bytes = new Uint8Array(buffer);
    const problem = validatePdf(file, bytes);
    if (problem) throw new Error(problem);
    return { file, responseHash: await sha256Hex(buffer) };
  }

  function receiptStorageKey(responseHash) {
    return `${RECEIPT_PREFIX}${responseHash}`;
  }

  function restoreReceipt(responseHash) {
    try {
      const stored = localStorage.getItem(receiptStorageKey(responseHash));
      if (!stored) return null;
      const receipt = JSON.parse(stored);
      return receipt.submitted_file_sha256 === responseHash ? receipt : null;
    } catch {
      return null;
    }
  }

  function preserveReceipt(receipt) {
    try {
      localStorage.setItem(receiptStorageKey(receipt.submitted_file_sha256), JSON.stringify(receipt));
    } catch {
      // Receipt remains downloadable in the current page session.
    }
  }

  async function validateReceipt(receipt, responseHash) {
    if (!receipt || receipt.schema_version !== 'HIL-RECEIVER-RECEIPT-v2') return false;
    if (!receipt.receipt_id || !receipt.submission_id) return false;
    if (receipt.primary_sha256 !== PRIMARY.sha256 || receipt.prompt_sha256 !== PRIMARY.promptSha256) return false;
    if (receipt.submitted_file_sha256 !== responseHash) return false;
    if (!['PRIMARY_PROMPT_RESPONSE_CHAIN_VERIFIED', 'PRIMARY_PROMPT_RESPONSE_SIGNATURE_CHAIN_VERIFIED'].includes(receipt.chain_validation_state)) return false;
    if (typeof receipt.receipt_sha256 !== 'string') return false;
    const unsigned = { ...receipt };
    delete unsigned.receipt_sha256;
    return await canonicalHash(unsigned) === receipt.receipt_sha256;
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

    const response = await fetchWithTimeout(`${receiver.baseUrl}${receiver.submissionPath}`, {
      method: 'POST',
      body: form,
      headers: { Accept: 'application/json' }
    }, 90000);
    const payload = await response.json().catch(() => null);
    if (!response.ok) {
      console.warn('HIL upload rejected', { status: response.status, detail: payload && payload.detail });
      throw new Error('The governed receiver did not accept the packet. Nothing was recorded. Please try again later.');
    }
    return payload;
  }

  async function uploadResponsePacket() {
    currentReceipt = null;
    receiptButton.disabled = true;
    setUploadState(false, 'Uploading…');
    try {
      setStatus('warn', 'Validating the unchanged response packet…');
      const { file, responseHash } = await readSelectedPdf();
      currentManifest = buildManifest(responseHash);
      provenanceButton.disabled = false;

      const priorReceipt = restoreReceipt(responseHash);
      if (priorReceipt && await validateReceipt(priorReceipt, responseHash)) {
        currentReceipt = priorReceipt;
        receiptButton.disabled = false;
        setStatus('ok', `${priorReceipt.submission_id} was already accepted. Opening the verified review…`);
        window.location.assign(`hil-accepted.html?submission_id=${encodeURIComponent(priorReceipt.submission_id)}`);
        return;
      }

      if (!receiver && !(await checkGatewayReadiness())) throw new Error(NOT_READY_MESSAGE);
      setStatus('warn', 'Uploading the response packet to the governed receiver…');
      const receipt = await submitArtifacts(file, currentManifest);
      if (!(await validateReceipt(receipt, responseHash))) throw new Error('The receiver returned an invalid receipt. The submission cannot be represented as accepted.');
      currentReceipt = receipt;
      preserveReceipt(receipt);
      receiptButton.disabled = false;
      setStatus('ok', `${receipt.submission_id} accepted. Opening the exact response and verified receipt…`);
      window.location.assign(`hil-accepted.html?submission_id=${encodeURIComponent(receipt.submission_id)}`);
    } catch (error) {
      console.error(error);
      setStatus('error', error.message || 'The response packet was not accepted.');
    } finally {
      setUploadState(Boolean(receiver));
    }
  }

  async function prepareProvenance() {
    try {
      const { responseHash } = await readSelectedPdf();
      currentManifest = buildManifest(responseHash);
      provenanceButton.disabled = false;
      setStatus('ok', `Local provenance prepared. Response SHA-256: ${responseHash}`);
    } catch (error) {
      setStatus('error', error.message || 'Unable to prepare provenance.');
    }
  }

  function downloadProvenance() {
    if (!currentManifest) return;
    saveBlob(new Blob([`${JSON.stringify(currentManifest, null, 2)}\n`], { type: 'application/json' }), 'HIL_Response_Provenance_v1_1.json');
  }

  function downloadReceipt() {
    if (!currentReceipt) return;
    saveBlob(new Blob([`${JSON.stringify(currentReceipt, null, 2)}\n`], { type: 'application/json' }), `${currentReceipt.submission_id}.receiver-receipt.json`);
  }

  byId('download-primary').addEventListener('click', downloadPrimary);
  byId('copy-prompt').addEventListener('click', copyPrompt);
  uploadButton.addEventListener('click', uploadResponsePacket);
  prepareButton.addEventListener('click', prepareProvenance);
  provenanceButton.addEventListener('click', downloadProvenance);
  receiptButton.addEventListener('click', downloadReceipt);
  fileInput.addEventListener('change', () => {
    currentManifest = null;
    currentReceipt = null;
    provenanceButton.disabled = true;
    receiptButton.disabled = true;
  });

  setUploadState(false, 'Checking intake…');
  checkGatewayReadiness();
  setInterval(() => checkGatewayReadiness({ quiet: true }), 30000);
})();
