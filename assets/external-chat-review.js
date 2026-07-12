(() => {
  'use strict';

  const CONFIG_PATH = 'data/ecosystem-chat-gateway.json';
  const statusEl = document.getElementById('review-status');
  const tokenEl = document.getElementById('review-access-token');
  const outputEl = document.getElementById('output');

  const esc = (value) => String(value ?? '—').replace(/[&<>"']/g, (char) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  const lines = (id) => document.getElementById(id).value.split('\n').map((value) => value.trim()).filter(Boolean);

  async function reviewEndpoint() {
    const response = await fetch(CONFIG_PATH, { cache: 'no-store' });
    if (!response.ok) throw new Error(`gateway config HTTP ${response.status}`);
    const config = await response.json();
    if (config.enabled !== true || !config.endpoint) throw new Error('governed gateway disabled');
    return config.endpoint.replace(/\/api\/ecosystem-chat$/, '/api/external-review/packages');
  }

  function currentResult() {
    const text = outputEl.textContent.trim();
    if (!text) throw new Error('run a compatibility test first');
    const result = JSON.parse(text);
    if (result.compatibility_evidence_only !== true || !result.receipt_id || !result.submission_sha256) {
      throw new Error('current output is not a valid compatibility result');
    }
    return result;
  }

  function buildPackage() {
    if (document.getElementById('review-opt-in').checked !== true) {
      throw new Error('explicit cooperative-review opt-in is required');
    }
    const reviewScope = lines('review-scope');
    if (!reviewScope.length) throw new Error('at least one review-scope item is required');
    const result = currentResult();
    return {
      schema_version: '1.0.0',
      packet_type: 'external_framework_cooperative_review_package',
      framework_id: result.framework_id,
      framework_name: result.framework_name || null,
      compatibility_receipt_id: result.receipt_id,
      submission_sha256: result.submission_sha256,
      compatibility_result: result.result,
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
    };
  }

  async function submitReview() {
    statusEl.textContent = 'Submitting package to authenticated cooperative review intake…';
    const token = tokenEl.value;
    if (!token) {
      statusEl.innerHTML = '<span class="error">A review submission access token is required.</span>';
      return;
    }
    try {
      const payload = buildPackage();
      const endpoint = await reviewEndpoint();
      const controller = new AbortController();
      const timeout = window.setTimeout(() => controller.abort(), 20000);
      try {
        const response = await fetch(endpoint, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
          signal: controller.signal,
          body: JSON.stringify(payload),
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.detail?.reason || `HTTP ${response.status}`);
        if (data.raw_submission_stored !== false || data.wiki_record_created !== false || data.publication_authorized !== false || data.standing_created !== false) {
          throw new Error('review intake authority boundary mismatch');
        }
        if (!data.package_id || !data.intake_receipt_id || data.review_state !== 'AWAITING_DELEGATED_REVIEW') {
          throw new Error('review intake receipt contract mismatch');
        }
        statusEl.innerHTML = `<span class="good">Review package accepted.</span> Package: ${esc(data.package_id)} · Intake receipt: ${esc(data.intake_receipt_id)} · State: ${esc(data.review_state)}. No raw artifact, wiki publication, certification, or standing was created.`;
      } finally {
        window.clearTimeout(timeout);
        tokenEl.value = '';
      }
    } catch (error) {
      tokenEl.value = '';
      statusEl.innerHTML = `<span class="error">Review submission failed: ${esc(error.message)}</span> No review receipt or publication state was claimed.`;
    }
  }

  document.getElementById('submit-review').addEventListener('click', submitReview);
  window.ExternalChatReview = { buildPackage, reviewEndpoint };
})();
