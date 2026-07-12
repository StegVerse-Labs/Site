(() => {
  'use strict';

  const CONFIG_PATH = 'data/ecosystem-chat-gateway.json';
  const EXAMPLE_PATH = 'data/external-chat-example.json';
  const CATALOG_PATH = 'data/external-framework-catalog.json';
  const CATALOG_RECEIPT_PATH = 'data/external-framework-catalog.receipt.json';
  const idEl = document.getElementById('framework-id');
  const nameEl = document.getElementById('framework-name');
  const submissionEl = document.getElementById('submission');
  const statusEl = document.getElementById('status');
  const resultEl = document.getElementById('result');
  const summaryEl = document.getElementById('summary');
  const linksEl = document.getElementById('wiki-links');
  const outputEl = document.getElementById('output');
  const catalogEl = document.getElementById('known-framework');
  const catalogStatusEl = document.getElementById('catalog-status');
  let lastResult = null;
  let lastSubmission = null;

  const esc = (value) => String(value ?? '—').replace(/[&<>"']/g, (char) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));

  function metric(label, value) {
    return `<div class="metric"><span>${esc(label)}</span><strong>${esc(value)}</strong></div>`;
  }

  function canonical(value) {
    if (Array.isArray(value)) return `[${value.map(canonical).join(',')}]`;
    if (value && typeof value === 'object') {
      return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonical(value[key])}`).join(',')}}`;
    }
    return JSON.stringify(value);
  }

  async function sha256(value) {
    const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(value));
    return [...new Uint8Array(digest)].map((byte) => byte.toString(16).padStart(2, '0')).join('');
  }

  function lines(id) {
    return document.getElementById(id).value.split('\n').map((value) => value.trim()).filter(Boolean);
  }

  function downloadJson(filename, payload) {
    const blob = new Blob([JSON.stringify(payload, null, 2) + '\n'], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = filename;
    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();
    URL.revokeObjectURL(url);
  }

  async function loadCatalog() {
    const [catalogResponse, receiptResponse] = await Promise.all([
      fetch(CATALOG_PATH, { cache: 'no-store' }),
      fetch(CATALOG_RECEIPT_PATH, { cache: 'no-store' }),
    ]);
    if (!catalogResponse.ok || !receiptResponse.ok) throw new Error('catalog or receipt unavailable');
    const catalog = await catalogResponse.json();
    const receipt = await receiptResponse.json();
    if (catalog.artifact_type !== 'external_framework_catalog') throw new Error('catalog contract mismatch');
    if (receipt.receipt_type !== 'external_framework_catalog_projection_receipt') throw new Error('catalog receipt mismatch');
    const digest = await sha256(canonical(catalog));
    if (digest !== receipt.catalog_sha256) throw new Error('catalog receipt hash mismatch');
    if (receipt.framework_count !== catalog.frameworks.length || receipt.projection_only !== true) throw new Error('catalog count or projection boundary mismatch');
    if (Object.values(catalog.authority_boundary || {}).some((value) => value !== false)) throw new Error('catalog authority boundary mismatch');
    if (Object.values(receipt.authority_boundary || {}).some((value) => value !== false)) throw new Error('catalog receipt authority boundary mismatch');
    catalog.frameworks.forEach((entry) => {
      const option = document.createElement('option');
      option.value = entry.framework_id;
      option.textContent = entry.framework_id;
      catalogEl.appendChild(option);
    });
    catalogStatusEl.textContent = `${catalog.frameworks.length} checked-in wiki report identifiers loaded; catalog receipt verified. Inclusion is not certification.`;
  }

  async function loadExample() {
    const response = await fetch(EXAMPLE_PATH, { cache: 'no-store' });
    if (!response.ok) throw new Error(`example HTTP ${response.status}`);
    const payload = await response.json();
    idEl.value = payload.framework_id || '';
    nameEl.value = payload.framework_name || '';
    submissionEl.value = JSON.stringify(payload, null, 2);
    statusEl.textContent = 'Example loaded. Review it before submitting.';
  }

  async function endpoint() {
    const response = await fetch(CONFIG_PATH, { cache: 'no-store' });
    if (!response.ok) throw new Error(`gateway config HTTP ${response.status}`);
    const config = await response.json();
    if (config.enabled !== true || !config.endpoint) throw new Error('governed gateway disabled');
    return config.endpoint.replace(/\/api\/ecosystem-chat$/, '/api/external-framework-compatibility');
  }

  function render(data) {
    lastResult = data;
    resultEl.hidden = false;
    const coverage = data.field_coverage || {};
    summaryEl.innerHTML = [
      metric('Result', data.result),
      metric('Field coverage', `${coverage.present ?? 0}/${coverage.required ?? 0}`),
      metric('Known wiki report', data.known_framework_report === true ? 'YES' : 'NO'),
      metric('Receipt', data.receipt_id || 'none'),
    ].join('');
    const links = [];
    if (data.admissibility_wiki_page) links.push(`<a href="${esc(data.admissibility_wiki_page)}" target="_blank" rel="noopener">Open framework page</a>`);
    if (data.admissibility_wiki_report) links.push(`<a href="${esc(data.admissibility_wiki_report)}" target="_blank" rel="noopener">Open compatibility report</a>`);
    linksEl.innerHTML = links.join(' · ') || 'No existing wiki report matched this framework ID. The result remains provisional intake.';
    outputEl.textContent = JSON.stringify(data, null, 2);
    statusEl.innerHTML = `<span class="good">Compatibility test complete.</span> Evidence only; no certification, execution, or standing was created.`;
  }

  async function submit() {
    statusEl.textContent = 'Running bounded compatibility test…';
    resultEl.hidden = true;
    let payload;
    try {
      payload = JSON.parse(submissionEl.value);
    } catch (error) {
      statusEl.innerHTML = `<span class="error">Invalid JSON: ${esc(error.message)}</span>`;
      return;
    }
    payload.framework_id = idEl.value.trim() || payload.framework_id;
    payload.framework_name = nameEl.value.trim() || payload.framework_name;
    lastSubmission = payload;
    try {
      const url = await endpoint();
      const controller = new AbortController();
      const timeout = window.setTimeout(() => controller.abort(), 20000);
      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          signal: controller.signal,
          body: JSON.stringify(payload),
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.detail?.reason || `HTTP ${response.status}`);
        if (data.compatibility_evidence_only !== true || data.boundary?.compatibility_result_is_authority !== false) throw new Error('compatibility authority boundary mismatch');
        if (data.submission_retained !== false || data.wiki_record_created !== false) throw new Error('submission retention/publication boundary mismatch');
        render(data);
      } finally {
        window.clearTimeout(timeout);
      }
    } catch (error) {
      statusEl.innerHTML = `<span class="error">Compatibility service unavailable: ${esc(error.message)}</span> No result or receipt was claimed.`;
    }
  }

  function downloadResultPacket() {
    if (!lastResult) return;
    downloadJson(`external-chat-${lastResult.framework_id || 'framework'}-result.json`, {
      packet_type: 'external_framework_compatibility_result_packet',
      schema_version: '1.0.0',
      generated_in_browser: true,
      raw_submission_retained_by_site: false,
      result: lastResult,
      boundary: {
        packet_is_certification: false,
        packet_is_execution_authority: false,
        packet_publication_creates_standing: false,
      },
    });
  }

  function downloadChallengePacket() {
    if (!lastResult) return;
    downloadJson(`external-chat-${lastResult.framework_id || 'framework'}-challenge.json`, {
      packet_type: 'external_framework_compatibility_challenge_packet',
      schema_version: '1.0.0',
      challenged_receipt_id: lastResult.receipt_id,
      challenged_submission_sha256: lastResult.submission_sha256,
      framework_id: lastResult.framework_id,
      challenged_field: '',
      reason: '',
      supporting_evidence_references: [],
      requested_correction_or_standing_change: '',
      original_result: lastResult.result,
      raw_submission_included: false,
      boundary: {
        challenge_is_not_automatic_correction: true,
        challenge_is_not_publication_authority: true,
        challenge_creates_no_standing: true,
      },
    });
  }

  function downloadReviewPackage() {
    if (!lastResult) return;
    if (document.getElementById('review-opt-in').checked !== true) {
      statusEl.innerHTML = '<span class="error">Explicit cooperative-review opt-in is required.</span>';
      return;
    }
    const reviewScope = lines('review-scope');
    if (!reviewScope.length) {
      statusEl.innerHTML = '<span class="error">At least one review-scope item is required.</span>';
      return;
    }
    downloadJson(`external-chat-${lastResult.framework_id || 'framework'}-review-package.json`, {
      schema_version: '1.0.0',
      packet_type: 'external_framework_cooperative_review_package',
      framework_id: lastResult.framework_id,
      framework_name: lastResult.framework_name || null,
      compatibility_receipt_id: lastResult.receipt_id,
      submission_sha256: lastResult.submission_sha256,
      compatibility_result: lastResult.result,
      submitter_opt_in: true,
      publication_requested: document.getElementById('publication-requested').checked === true,
      raw_submission_included: false,
      review_scope: reviewScope,
      evidence_references: lines('evidence-references'),
      contact_reference: null,
      boundary: {
        package_is_publication_authority: false,
        package_is_certification: false,
        package_creates_standing: false,
        review_may_change_result_without_receipt: false,
      },
    });
    statusEl.innerHTML = '<span class="good">Cooperative review package created locally.</span> No upload or publication occurred.';
  }

  catalogEl.addEventListener('change', () => {
    if (!catalogEl.value) return;
    idEl.value = catalogEl.value;
    const payload = lastSubmission || {};
    payload.framework_id = catalogEl.value;
    submissionEl.value = JSON.stringify(payload, null, 2);
  });
  document.getElementById('load-example').addEventListener('click', () => loadExample().catch((error) => {
    statusEl.innerHTML = `<span class="error">Could not load example: ${esc(error.message)}</span>`;
  }));
  document.getElementById('submit').addEventListener('click', submit);
  document.getElementById('download-result').addEventListener('click', downloadResultPacket);
  document.getElementById('download-challenge').addEventListener('click', downloadChallengePacket);
  document.getElementById('download-review').addEventListener('click', downloadReviewPackage);
  loadCatalog().catch((error) => { catalogStatusEl.innerHTML = `<span class="error">Catalog unavailable: ${esc(error.message)}</span>`; });
  loadExample().catch(() => {});
})();
