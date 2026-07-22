(() => {
  'use strict';

  const STAGES = ['submitted', 'recognized', 'attributed', 'realized', 'distributable', 'settled'];
  const workspace = document.querySelector('.value-workspace');
  const conversationList = document.getElementById('valueConversationList');
  const governedList = document.getElementById('valueGovernedList');
  const raw = document.getElementById('valueRaw');
  const rawToggle = document.getElementById('valueRawToggle');
  const exportButton = document.getElementById('valueExport');
  let claims = [];
  let rawMode = false;
  let activeClaimId = null;

  if (!workspace || !conversationList || !governedList || !raw) return;

  document.querySelectorAll('[data-value-view]').forEach((button) => {
    button.addEventListener('click', () => setView(button.dataset.valueView));
  });
  rawToggle?.addEventListener('click', toggleRaw);
  exportButton?.addEventListener('click', exportClaims);

  loadClaims();

  async function loadClaims() {
    try {
      const response = await fetch('data/ecosystem-chat-value-claims.fixture.json', { cache: 'no-store' });
      if (!response.ok) throw new Error(`fixture status ${response.status}`);
      const payload = await response.json();
      if (payload.authority_effect !== 'NONE' || !Array.isArray(payload.claims)) {
        throw new Error('invalid authority boundary or claim collection');
      }
      claims = payload.claims.map((claim) => Object.freeze(structuredCloneSafe(claim)));
      render();
    } catch (error) {
      const message = document.createElement('p');
      message.className = 'muted';
      message.textContent = `Value-claim fixture unavailable: ${error.message}`;
      conversationList.replaceChildren(message);
      governedList.replaceChildren(message.cloneNode(true));
    }
  }

  function setView(mode) {
    if (!['conversation', 'governed', 'split'].includes(mode)) return;
    workspace.className = `value-workspace ${mode}`;
    document.querySelectorAll('[data-value-view]').forEach((button) => {
      const selected = button.dataset.valueView === mode;
      button.classList.toggle('active', selected);
      button.setAttribute('aria-selected', String(selected));
    });
  }

  function render() {
    conversationList.replaceChildren();
    governedList.replaceChildren();
    claims.forEach((claim) => {
      conversationList.append(renderConversationClaim(claim));
      governedList.append(renderGovernedClaim(claim));
    });
    raw.textContent = claims.map((claim) => JSON.stringify(claim)).join('\n');
    if (activeClaimId) applySelection(activeClaimId);
  }

  function renderConversationClaim(claim) {
    const article = document.createElement('article');
    article.className = 'value-card';
    article.dataset.claimId = claim.claim_id;
    article.dataset.eventId = claim.submission_event_id;
    article.tabIndex = 0;
    const reward = claim.distribution?.reward_class || 'none';
    const boundary = expectationBoundary(claim.stage, reward);
    article.innerHTML = `
      <h3>${escapeHtml(humanTitle(claim))}</h3>
      <p>${escapeHtml(humanSummary(claim))}</p>
      <div class="value-meta">
        <div><strong>stage</strong><span>${escapeHtml(claim.stage)}</span></div>
        <div><strong>source</strong><span>${escapeHtml(claim.information_posture?.source_type || 'unknown')}</span></div>
        <div><strong>reuse</strong><span>${escapeHtml(claim.information_posture?.reuse_scope || 'unknown')}</span></div>
        <div><strong>materiality</strong><span>${escapeHtml(claim.influence?.materiality || 'unassessed')}</span></div>
        <div><strong>reward class</strong><span>${escapeHtml(reward)}</span></div>
        <div><strong>dispute</strong><span>${escapeHtml(claim.dispute_status || 'none')}</span></div>
      </div>
      <div class="value-boundary">${escapeHtml(boundary)}</div>`;
    bindSelection(article, claim.claim_id);
    return article;
  }

  function renderGovernedClaim(claim) {
    const article = document.createElement('article');
    article.className = 'value-card';
    article.dataset.claimId = claim.claim_id;
    article.dataset.eventId = claim.submission_event_id;
    article.tabIndex = 0;
    article.innerHTML = `
      <h3>${escapeHtml(claim.claim_id)}</h3>
      <div class="value-meta">
        <div><strong>submission_event_id</strong><span>${escapeHtml(claim.submission_event_id)}</span></div>
        <div><strong>stage</strong><span>${escapeHtml(claim.stage)}</span></div>
        <div><strong>confidence</strong><span>${escapeHtml(claim.influence?.confidence ?? 'null')}</span></div>
        <div><strong>consent refs</strong><span>${escapeHtml((claim.information_posture?.consent_refs || []).join(', ') || 'none')}</span></div>
        <div><strong>policy refs</strong><span>${escapeHtml((claim.distribution?.policy_refs || []).join(', ') || 'none')}</span></div>
        <div><strong>contract refs</strong><span>${escapeHtml((claim.distribution?.contract_refs || []).join(', ') || 'none')}</span></div>
      </div>
      <pre>${escapeHtml(JSON.stringify({
        influence: claim.influence,
        value: claim.value,
        distribution: claim.distribution,
        evidence_refs: claim.evidence_refs,
        competing_claim_refs: claim.competing_claim_refs,
        hash: claim.hash
      }, null, 2))}</pre>`;
    bindSelection(article, claim.claim_id);
    return article;
  }

  function bindSelection(element, claimId) {
    element.addEventListener('click', () => selectClaim(claimId));
    element.addEventListener('focus', () => selectClaim(claimId));
    element.setAttribute('aria-label', `Value claim ${claimId}; stable correlated record`);
  }

  function selectClaim(claimId) {
    activeClaimId = claimId;
    applySelection(claimId);
  }

  function applySelection(claimId) {
    document.querySelectorAll('[data-claim-id].correlated-active').forEach((node) => node.classList.remove('correlated-active'));
    document.querySelectorAll(`[data-claim-id="${cssEscape(claimId)}"]`).forEach((node) => {
      node.classList.add('correlated-active');
      node.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    });
  }

  function toggleRaw() {
    rawMode = !rawMode;
    governedList.hidden = rawMode;
    raw.hidden = !rawMode;
    rawToggle.textContent = rawMode ? 'Formatted records' : 'Raw JSONL';
  }

  function exportClaims() {
    const payload = {
      schema: 'stegverse.governed-value-claims.v0.1',
      authority_effect: 'NONE',
      exported_at: new Date().toISOString(),
      claims
    };
    const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = 'stegverse-governed-value-claims.json';
    anchor.click();
    URL.revokeObjectURL(url);
  }

  function humanTitle(claim) {
    const source = (claim.information_posture?.source_type || 'submission').replaceAll('_', ' ');
    return `${source}: ${claim.stage}`;
  }

  function humanSummary(claim) {
    const targetCount = claim.influence?.target_event_refs?.length || 0;
    const uncertainty = claim.influence?.uncertainty || 'Influence has not been evaluated.';
    if (claim.stage === 'submitted') return `The submission is preserved as a claim. No downstream influence or payable value has been established. ${uncertainty}`;
    if (claim.stage === 'recognized') return `Evidence links this contribution to ${targetCount} governed target event${targetCount === 1 ? '' : 's'}, but attribution and realized value remain unresolved. ${uncertainty}`;
    if (claim.stage === 'distributable') return `A policy and contract permit a provisional reward class, but no settlement receipt exists. ${uncertainty}`;
    return `This claim is at the ${claim.stage} stage. Later-stage authority must remain evidence-bound and reconstructable. ${uncertainty}`;
  }

  function expectationBoundary(stage, reward) {
    if (stage === 'submitted') return 'Claim preserved, not value proven. No payment or royalty is implied.';
    if (stage === 'recognized') return 'Influence recognized, not ownership or exclusivity proven.';
    if (stage === 'distributable') return `${reward} is authorized as a candidate class; distributable value is not payment.`;
    if (stage === 'settled') return 'Settlement is valid only with an authorized settlement receipt and reconstructable lineage.';
    return 'Prototype interpretation only. Authority, custody, and settlement remain upstream.';
  }

  function structuredCloneSafe(value) {
    return typeof structuredClone === 'function' ? structuredClone(value) : JSON.parse(JSON.stringify(value));
  }

  function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, (character) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' }[character]));
  }

  function cssEscape(value) {
    return window.CSS?.escape ? CSS.escape(value) : String(value).replace(/["\\]/g, '\\$&');
  }

  window.StegVerseValueClaims = Object.freeze({
    version: '0.1',
    stages: STAGES.slice(),
    getClaims: () => claims.slice(),
    getClaim: (claimId) => claims.find((claim) => claim.claim_id === claimId) || null,
    selectClaim
  });
})();
