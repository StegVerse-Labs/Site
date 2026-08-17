(() => {
  'use strict';

  const STORAGE_KEY = 'stegverse.iphone-heartbeat-transition-receipt.v1';
  const EXPECTED_ORIGIN = 'https://stegverse.org';
  const CONTRACT_ID = 'SHWP-IPHONE-HB30-TRANSITION-CAPSULE-001';
  const LEGACY_BLOB = 'd18d57d83cf19b7799cde1a1b4487e496eca7f76';

  const environmentStatus = document.getElementById('environment-status');
  const generateButton = document.getElementById('generate-receipt');
  const copyButton = document.getElementById('copy-receipt');
  const shareButton = document.getElementById('share-receipt');
  const downloadButton = document.getElementById('download-receipt');
  const resultStatus = document.getElementById('result-status');
  const output = document.getElementById('receipt-output');

  function canonicalize(value) {
    if (Array.isArray(value)) {
      return `[${value.map(canonicalize).join(',')}]`;
    }
    if (value && typeof value === 'object') {
      return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonicalize(value[key])}`).join(',')}}`;
    }
    return JSON.stringify(value);
  }

  function toHex(bytes) {
    return Array.from(new Uint8Array(bytes), (byte) => byte.toString(16).padStart(2, '0')).join('');
  }

  async function sha256Hex(text) {
    const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
    return toHex(digest);
  }

  function environmentCheck() {
    const failures = [];
    if (location.origin !== EXPECTED_ORIGIN) failures.push(`origin must be ${EXPECTED_ORIGIN}`);
    if (!navigator.userAgent.includes('iPhone')) failures.push('current browser user agent must identify an iPhone');
    if (window.isSecureContext !== true) failures.push('secure browser context required');
    if (!globalThis.crypto || !crypto.subtle || typeof crypto.subtle.digest !== 'function') failures.push('WebCrypto SHA-256 required');
    return failures;
  }

  function unsignedReceipt() {
    return {
      schema: 'stegverse.iphone-heartbeat-transition-receipt/v1',
      contract_id: CONTRACT_ID,
      physical_execution_surface: 'CURRENT_USER_IPHONE',
      executed_at: new Date().toISOString(),
      seed: {
        repository: 'StegVerse-Labs/.github',
        legacy_state_ref: 'control/heartbeat-state.json',
        legacy_state_git_blob_sha: LEGACY_BLOB,
        epoch: 29,
        generation: 29
      },
      successor: {
        schema: 'stegverse.heartbeat-carrier-runtime-state/v1',
        epoch: 30,
        generation: 30,
        reference_frame: 'heartbeat_epoch:30',
        activation_state: 'ACTIVE',
        authority_effect: 'NONE',
        legacy_hb29_immutable: true
      },
      authority: {
        credential_authority: 'TV/TVC',
        credential_requirement: 'NONE',
        github_token_runtime_authority: 'NONE',
        non_tv_tvc_secret_or_token_used: false,
        worker_authority: false,
        claim_or_fence_mutation: false,
        route_authority: false,
        wallet_authority: false,
        model_output_authority: 'NONE',
        hosted_runtime_production_authority: 'NONE',
        another_physical_machine_required: false
      },
      browser: {
        origin: location.origin,
        user_agent: navigator.userAgent,
        secure_context: window.isSecureContext === true,
        webcrypto: Boolean(globalThis.crypto && crypto.subtle && typeof crypto.subtle.digest === 'function')
      }
    };
  }

  async function generateReceipt() {
    const failures = environmentCheck();
    if (failures.length) {
      resultStatus.textContent = `FAIL_CLOSED: ${failures.join('; ')}`;
      return;
    }

    generateButton.disabled = true;
    resultStatus.textContent = 'Generating deterministic portable receipt…';
    try {
      const receipt = unsignedReceipt();
      receipt.receipt_sha256 = await sha256Hex(canonicalize(receipt));
      const formatted = JSON.stringify(receipt, null, 2);
      localStorage.setItem(STORAGE_KEY, formatted);
      output.value = formatted;
      resultStatus.textContent = `PORTABLE_RECEIPT_READY — sha256:${receipt.receipt_sha256}`;
      copyButton.disabled = false;
      shareButton.disabled = false;
      downloadButton.disabled = false;
    } catch (error) {
      resultStatus.textContent = `FAIL_CLOSED: ${error instanceof Error ? error.message : String(error)}`;
      output.value = '';
    } finally {
      generateButton.disabled = false;
    }
  }

  async function copyReceipt() {
    if (!output.value) return;
    await navigator.clipboard.writeText(output.value);
    resultStatus.textContent = 'Receipt copied locally. Independent canonical verification is still required.';
  }

  async function shareReceipt() {
    if (!output.value) return;
    if (typeof navigator.share !== 'function') {
      resultStatus.textContent = 'Web Share is unavailable. Use Copy receipt or Save receipt file.';
      return;
    }
    const blob = new Blob([output.value], { type: 'application/json' });
    const file = new File([blob], 'stegverse-hb29-hb30-iphone-receipt.json', { type: 'application/json' });
    const payload = { title: 'StegVerse HB29→HB30 portable receipt', text: 'Non-authorizing physical transition evidence.', files: [file] };
    if (navigator.canShare && !navigator.canShare({ files: [file] })) delete payload.files;
    await navigator.share(payload);
  }

  function downloadReceipt() {
    if (!output.value) return;
    const blob = new Blob([output.value], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = 'stegverse-hb29-hb30-iphone-receipt.json';
    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();
    URL.revokeObjectURL(url);
  }

  const failures = environmentCheck();
  if (failures.length) {
    environmentStatus.textContent = `FAIL_CLOSED — ${failures.join('; ')}`;
  } else {
    environmentStatus.textContent = 'READY — current iPhone, stegverse.org HTTPS, secure context, and WebCrypto verified.';
    generateButton.disabled = false;
  }

  const retained = localStorage.getItem(STORAGE_KEY);
  if (retained) {
    output.value = retained;
    resultStatus.textContent = 'A prior local portable receipt is retained on this browser. Generate a new receipt only if canonical HB29 remains current.';
    copyButton.disabled = false;
    shareButton.disabled = false;
    downloadButton.disabled = false;
  }

  generateButton.addEventListener('click', generateReceipt);
  copyButton.addEventListener('click', () => copyReceipt().catch((error) => { resultStatus.textContent = `FAIL_CLOSED: ${error}`; }));
  shareButton.addEventListener('click', () => shareReceipt().catch((error) => { resultStatus.textContent = `FAIL_CLOSED: ${error}`; }));
  downloadButton.addEventListener('click', downloadReceipt);
})();
