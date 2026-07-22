(() => {
  'use strict';

  const CLAIMS_PATH = 'data/ecosystem-chat-value-claims.fixture.json';
  const HISTORY_PATH = 'data/ecosystem-chat-value-claim-history.fixture.json';
  const I18N_PATH = 'data/ecosystem-chat-value-expectations.i18n.json';
  const hostAnchor = document.getElementById('free-tier-trust') || document.getElementById('technical-details');
  if (!hostAnchor || document.getElementById('ecosystemValueClaimPanel')) return;

  const state = {
    claims: [],
    histories: [],
    i18n: null,
    locale: 'en',
    activeClaimId: null,
    rawMode: false,
  };

  const style = document.createElement('style');
  style.textContent = `
    .ecosystem-value-panel{padding:16px;margin-bottom:18px;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius)}
    .ecosystem-value-head,.ecosystem-value-controls{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
    .ecosystem-value-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:12px;margin-top:14px}
    .ecosystem-value-list,.ecosystem-value-history{display:grid;gap:9px;max-height:520px;overflow:auto}
    .ecosystem-value-card{border:1px solid var(--border);border-radius:var(--radius);padding:12px;background:#080d16;cursor:pointer}
    .ecosystem-value-card strong,.ecosystem-value-card span{display:block}.ecosystem-value-card span{color:var(--muted);font-size:11px;margin-top:4px}
    .ecosystem-value-card.active{outline:2px solid #66ff99;outline-offset:2px}
    .ecosystem-value-boundary{margin-top:10px;border-left:3px solid #66ff99;padding:9px 10px;background:rgba(18,49,27,.18);color:#bce9c5;font-size:12px}
    .ecosystem-value-history-item{border:1px solid var(--border);border-radius:8px;padding:9px;font:10px/1.5 var(--mono)}
    .ecosystem-value-history-item b,.ecosystem-value-history-item span{display:block}.ecosystem-value-history-item span{color:var(--muted)}
    .ecosystem-value-raw{white-space:pre-wrap;overflow-wrap:anywhere;font:10px/1.5 var(--mono);max-height:520px;overflow:auto;border:1px solid var(--border);border-radius:var(--radius);padding:12px;background:#080d16}
    .ecosystem-value-locale{border:1px solid var(--border2);border-radius:999px;background:#080d16;color:var(--text);padding:8px 10px;font:11px var(--mono)}
    @media(max-width:900px){.ecosystem-value-grid{grid-template-columns:1fr}}
  `;
  document.head.appendChild(style);

  const section = document.createElement('section');
  section.className = 'ecosystem-value-panel';
  section.id = 'ecosystemValueClaimPanel';
  section.innerHTML = `
    <div class="ecosystem-value-head">
      <div><h2 class="sv-h2" id="ecosystemValueTitle">Governed contribution value</h2><p class="muted" id="ecosystemValueSummary">Loading governed value-claim projection…</p></div>
      <a class="sv-btn sv-btn-secondary" href="ecosystem-chat-value.html" id="ecosystemValueInspectLink">Inspect governed value claims</a>
    </div>
    <div class="ecosystem-value-controls">
      <select class="ecosystem-value-locale" id="ecosystemValueLocale" aria-label="Value claim language"></select>
      <div class="node-view-actions">
        <button class="sv-btn sv-btn-secondary" type="button" id="ecosystemValueRawToggle">Raw JSONL</button>
        <button class="sv-btn sv-btn-secondary" type="button" id="ecosystemValueExport">Export value history</button>
      </div>
    </div>
    <div class="ecosystem-value-boundary" id="ecosystemValueBoundary">Claim preserved does not mean value proven.</div>
    <div class="ecosystem-value-grid" id="ecosystemValueGrid">
      <div><h3>Claims</h3><div class="ecosystem-value-list" id="ecosystemValueClaims"></div></div>
      <div><h3>Stage history</h3><div class="ecosystem-value-history" id="ecosystemValueHistory"></div></div>
    </div>
    <pre class="ecosystem-value-raw" id="ecosystemValueRaw" hidden></pre>`;
  hostAnchor.parentNode.insertBefore(section, hostAnchor);

  const elements = {
    title: document.getElementById('ecosystemValueTitle'),
    summary: document.getElementById('ecosystemValueSummary'),
    boundary: document.getElementById('ecosystemValueBoundary'),
    locale: document.getElementById('ecosystemValueLocale'),
    claims: document.getElementById('ecosystemValueClaims'),
    history: document.getElementById('ecosystemValueHistory'),
    grid: document.getElementById('ecosystemValueGrid'),
    raw: document.getElementById('ecosystemValueRaw'),
    rawToggle: document.getElementById('ecosystemValueRawToggle'),
    exportButton: document.getElementById('ecosystemValueExport'),
    inspectLink: document.getElementById('ecosystemValueInspectLink'),
  };

  elements.locale.addEventListener('change', () => {
    state.locale = elements.locale.value;
    renderLocale();
  });
  elements.rawToggle.addEventListener('click', toggleRaw);
  elements.exportButton.addEventListener('click', exportHistory);

  Promise.all([loadJson(CLAIMS_PATH), loadJson(HISTORY_PATH), loadJson(I18N_PATH)])
    .then(([claimsPayload, historyPayload, i18nPayload]) => {
      if (claimsPayload.authority_effect !== 'NONE' || historyPayload.authority_effect !== 'NONE' || i18nPayload.authority_effect !== 'NONE') {
        throw new Error('authority boundary mismatch');
      }
      state.claims = Array.isArray(claimsPayload.claims) ? claimsPayload.claims : [];
      state.histories = Array.isArray(historyPayload.histories) ? historyPayload.histories : [];
      state.i18n = i18nPayload;
      state.locale = resolveLocale(Object.keys(i18nPayload.locales || {}));
      populateLocales();
      renderLocale();
      renderClaims();
      selectClaim(state.claims[0]?.claim_id || null);
    })
    .catch((error) => failClosed(error.message));

  async function loadJson(path) {
    const response = await fetch(path, { cache: 'no-store' });
    if (!response.ok) throw new Error(`${path} returned ${response.status}`);
    return response.json();
  }

  function resolveLocale(available) {
    const language = navigator.language || 'en';
    if (available.includes(language)) return language;
    if (/^zh-(TW|HK|MO|Hant)/i.test(language) && available.includes('zh-Hant')) return 'zh-Hant';
    if (/^zh/i.test(language) && available.includes('zh-Hans')) return 'zh-Hans';
    if (/^es/i.test(language) && available.includes('es')) return 'es';
    return 'en';
  }

  function populateLocales() {
    elements.locale.replaceChildren();
    Object.entries(state.i18n.locales || {}).forEach(([code, copy]) => {
      const option = document.createElement('option');
      option.value = code;
      option.textContent = copy.label || code;
      option.selected = code === state.locale;
      elements.locale.appendChild(option);
    });
  }

  function renderLocale() {
    const copy = state.i18n?.locales?.[state.locale] || state.i18n?.locales?.en;
    if (!copy) return;
    elements.title.textContent = copy.title;
    elements.summary.textContent = copy.summary;
    elements.boundary.textContent = `${copy.preserved} ${copy.recognized} ${copy.distributable} ${copy.privacy} ${copy.consent}`;
    elements.inspectLink.textContent = copy.button;
  }

  function renderClaims() {
    elements.claims.replaceChildren();
    state.claims.forEach((claim) => {
      const card = document.createElement('article');
      card.className = 'ecosystem-value-card';
      card.dataset.claimId = claim.claim_id;
      card.dataset.eventId = claim.submission_event_id;
      card.tabIndex = 0;
      card.innerHTML = `<strong>${escapeHtml(claim.claim_id)} · ${escapeHtml(claim.stage)}</strong><span>source=${escapeHtml(claim.information_posture?.source_type || 'unknown')} · reuse=${escapeHtml(claim.information_posture?.reuse_scope || 'unknown')}</span><span>materiality=${escapeHtml(claim.influence?.materiality || 'unassessed')} · reward=${escapeHtml(claim.distribution?.reward_class || 'none')} · dispute=${escapeHtml(claim.dispute_status || 'none')}</span>`;
      card.addEventListener('click', () => selectClaim(claim.claim_id));
      card.addEventListener('focus', () => selectClaim(claim.claim_id));
      elements.claims.appendChild(card);
    });
    elements.raw.textContent = JSON.stringify({
      schema: 'stegverse.value-claim-integrated-projection.v0.1',
      authority_effect: 'NONE',
      claims: state.claims,
      histories: state.histories,
    }, null, 2);
  }

  function selectClaim(claimId) {
    if (!claimId) return;
    state.activeClaimId = claimId;
    elements.claims.querySelectorAll('[data-claim-id]').forEach((node) => node.classList.toggle('active', node.dataset.claimId === claimId));
    const history = state.histories.find((entry) => entry.claim_id === claimId) || null;
    renderHistory(history);
    correlateCanonicalEvent(claimId);
  }

  function renderHistory(history) {
    elements.history.replaceChildren();
    if (!history) {
      const empty = document.createElement('p');
      empty.className = 'muted';
      empty.textContent = 'No stage-history fixture is linked to this claim.';
      elements.history.appendChild(empty);
      return;
    }
    history.events.forEach((event) => {
      const item = document.createElement('div');
      item.className = 'ecosystem-value-history-item';
      item.innerHTML = `<b>${escapeHtml(event.event_type)} · ${escapeHtml(event.history_event_id)}</b><span>${escapeHtml(event.from_stage ?? 'null')} → ${escapeHtml(event.to_stage)} · ${escapeHtml(event.timestamp)}</span><span>reuse=${escapeHtml(event.reuse_scope)} · authority=${escapeHtml(event.authority_effect)}</span>`;
      elements.history.appendChild(item);
    });
  }

  function correlateCanonicalEvent(claimId) {
    const claim = state.claims.find((entry) => entry.claim_id === claimId);
    const eventId = claim?.submission_event_id;
    if (!eventId) return;
    document.querySelectorAll('[data-event-id].correlated-active').forEach((node) => node.classList.remove('correlated-active'));
    document.querySelectorAll(`[data-event-id="${cssEscape(eventId)}"]`).forEach((node) => node.classList.add('correlated-active'));
    window.StegVerseCanonicalEventStream?.selectEvent?.(eventId, 'value-claim');
  }

  function toggleRaw() {
    state.rawMode = !state.rawMode;
    elements.grid.hidden = state.rawMode;
    elements.raw.hidden = !state.rawMode;
    elements.rawToggle.textContent = state.rawMode ? 'Formatted claims' : 'Raw JSONL';
  }

  function exportHistory() {
    const payload = {
      schema: 'stegverse.value-claim-history-export.v0.1',
      authority_effect: 'NONE',
      exported_at: new Date().toISOString(),
      claims: state.claims,
      histories: state.histories,
    };
    const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = 'stegverse-value-claim-history.json';
    anchor.click();
    URL.revokeObjectURL(url);
  }

  function failClosed(message) {
    elements.summary.textContent = 'Governed value projection unavailable.';
    elements.boundary.textContent = `No value, ownership, distribution, payment, custody, or authority claim is inferred. ${message}`;
    elements.claims.innerHTML = '<p class="muted">Fixture validation failed closed.</p>';
    elements.history.innerHTML = '<p class="muted">No stage history displayed.</p>';
  }

  function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, (character) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' }[character]));
  }

  function cssEscape(value) {
    return window.CSS?.escape ? CSS.escape(value) : String(value).replace(/["\\]/g, '\\$&');
  }

  window.StegVerseValueClaimIntegration = Object.freeze({
    version: '0.1',
    getState: () => ({ ...state, claims: state.claims.slice(), histories: state.histories.slice() }),
    selectClaim,
  });
})();
