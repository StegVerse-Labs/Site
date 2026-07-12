(() => {
  'use strict';
  const configPath = 'data/ecosystem-chat-gateway.json';
  const q = (id) => document.getElementById(id);
  let loaded = null;

  const lines = (id) => q(id).value.split('\n').map((v) => v.trim()).filter(Boolean);
  const esc = (value) => String(value ?? '—').replace(/[&<>"']/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

  async function baseUrl() {
    const response = await fetch(configPath, {cache: 'no-store'});
    if (!response.ok) throw new Error(`gateway config HTTP ${response.status}`);
    const config = await response.json();
    if (config.enabled !== true || !config.endpoint) throw new Error('governed gateway disabled');
    return config.endpoint.replace(/\/api\/ecosystem-chat$/, '');
  }

  async function loadPackage() {
    const packageId = q('package-id').value.trim();
    const reviewerRef = q('reviewer-ref').value.trim();
    const token = q('reviewer-token').value;
    q('lookup-status').textContent = 'Loading delegated package…';
    try {
      if (!packageId || !reviewerRef || !token) throw new Error('package ID, reviewer reference, and token are required');
      const base = await baseUrl();
      const url = `${base}/api/external-review/reviewer/packages/${encodeURIComponent(packageId)}?reviewer_ref=${encodeURIComponent(reviewerRef)}`;
      const response = await fetch(url, {headers: {Authorization: `Bearer ${token}`}, cache: 'no-store'});
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail?.reason || `HTTP ${response.status}`);
      if (data.reviewer_identity_verified !== true || data.publication_authorized !== false || data.raw_submission_stored !== false) throw new Error('review authority boundary mismatch');
      loaded = data;
      q('package-output').textContent = JSON.stringify(data, null, 2);
      q('lookup-status').innerHTML = '<span class="good">Delegated package loaded.</span> No publication or certification authority was granted.';
      q('reviewed-fields').value = (data.payload?.review_scope || []).join('\n');
    } catch (error) {
      loaded = null;
      q('package-output').textContent = '';
      q('lookup-status').innerHTML = `<span class="error">Lookup failed: ${esc(error.message)}</span>`;
    } finally {
      q('reviewer-token').value = '';
    }
  }

  async function issueCorrection() {
    const token = q('reviewer-token').value;
    const reviewerRef = q('reviewer-ref').value.trim();
    q('correction-status').textContent = 'Issuing delegated correction…';
    try {
      if (!loaded) throw new Error('load a delegated package first');
      if (!token) throw new Error('reviewer token is required again');
      const reviewedFields = lines('reviewed-fields');
      const evidence = lines('supporting-evidence');
      if (!reviewedFields.length || !evidence.length || !q('rationale').value.trim()) throw new Error('reviewed fields, supporting evidence, and rationale are required');
      const decision = q('decision').value;
      const correcting = ['CORRECT', 'PARTIAL_CORRECTION'].includes(decision);
      const payload = {
        packet_type: 'external_framework_correction_request',
        schema_version: '1.0.0',
        package_id: loaded.package_id,
        challenged_receipt_id: loaded.compatibility_receipt_id,
        challenged_submission_sha256: loaded.submission_sha256,
        reviewer_ref: reviewerRef,
        decision,
        reviewed_fields: reviewedFields,
        supporting_evidence_references: evidence,
        rationale: q('rationale').value.trim(),
        replacement_result: correcting ? q('replacement-result').value.trim() || null : null,
        replacement_receipt_id: correcting ? q('replacement-receipt').value.trim() || null : null,
        publication_authorized: false,
      };
      const base = await baseUrl();
      const response = await fetch(`${base}/api/external-review/corrections`, {
        method: 'POST', headers: {'Content-Type':'application/json', Authorization:`Bearer ${token}`}, body: JSON.stringify(payload),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail?.reason || `HTTP ${response.status}`);
      if (data.reviewer_identity_verified !== true || data.reviewer_delegation_verified !== true || data.review_scope_verified !== true) throw new Error('review verification incomplete');
      if (data.publication_authorized !== false || data.certification_created !== false || data.standing_created !== false) throw new Error('correction authority boundary mismatch');
      q('correction-output').textContent = JSON.stringify(data, null, 2);
      q('correction-status').innerHTML = '<span class="good">Correction receipt recorded.</span> Publication still requires a separate publisher transition.';
    } catch (error) {
      q('correction-output').textContent = '';
      q('correction-status').innerHTML = `<span class="error">Correction failed: ${esc(error.message)}</span>`;
    } finally {
      q('reviewer-token').value = '';
    }
  }

  q('load-package').addEventListener('click', loadPackage);
  q('issue-correction').addEventListener('click', issueCorrection);
})();
