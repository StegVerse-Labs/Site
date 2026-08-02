(() => {
  'use strict';

  const REGISTRY_PATH = 'data/ecosystem-chat-governed-aspects.registry.json';
  const EVENTS_PATH = 'data/ecosystem-chat-governed-aspect-events.fixture.json';
  const hostAnchor = document.getElementById('ecosystemValueClaimPanel') || document.getElementById('free-tier-trust') || document.getElementById('technical-details');
  if (!hostAnchor || document.getElementById('ecosystemAspectMatrix')) return;

  const state = {
    registry: [],
    events: [],
    activeSubjectRef: null,
    activeAspectId: null,
    view: 'human',
    role: 'public',
    rawMode: false,
  };

  const style = document.createElement('style');
  style.textContent = `
    .aspect-matrix{padding:16px;margin-bottom:18px;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius)}
    .aspect-matrix-head,.aspect-matrix-controls{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap}
    .aspect-matrix-tabs,.aspect-matrix-actions{display:flex;gap:8px;flex-wrap:wrap}
    .aspect-matrix-tab,.aspect-role{border:1px solid var(--border2);border-radius:999px;background:#080d16;color:var(--muted);padding:8px 11px;font:11px var(--mono)}
    .aspect-matrix-tab{cursor:pointer}.aspect-matrix-tab.active{border-color:#66ff99;color:#bce9c5}
    .aspect-matrix-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:9px;margin-top:12px;max-height:640px;overflow:auto}
    .aspect-cell{border:1px solid var(--border);border-radius:9px;padding:10px;background:#080d16;cursor:pointer;min-width:0}
    .aspect-cell.active{outline:2px solid #66ff99;outline-offset:2px}.aspect-cell strong,.aspect-cell span{display:block}.aspect-cell strong{font-size:12px}.aspect-cell span{font:10px/1.5 var(--mono);color:var(--muted);overflow-wrap:anywhere}
    .aspect-cell .aspect-status{color:#bce9c5;margin-top:5px}.aspect-detail{margin-top:12px;border:1px solid var(--border);border-radius:9px;padding:12px;background:#080d16}.aspect-detail pre,.aspect-raw{white-space:pre-wrap;overflow-wrap:anywhere;font:10px/1.5 var(--mono)}
    .aspect-raw{max-height:640px;overflow:auto;border:1px solid var(--border);border-radius:9px;padding:12px;background:#080d16;margin-top:12px}
    .aspect-boundary{border-left:3px solid #66ff99;padding:9px 10px;background:rgba(18,49,27,.18);color:#bce9c5;font-size:12px;margin-top:10px}
  `;
  document.head.appendChild(style);

  const section = document.createElement('section');
  section.id = 'ecosystemAspectMatrix';
  section.className = 'aspect-matrix';
  section.innerHTML = `
    <div class="aspect-matrix-head">
      <div><h2 class="sv-h2">Governed interaction aspects</h2><p class="muted">Independent aspect records attached to stable interaction subjects. Missing evidence remains unresolved.</p></div>
      <span class="node-authority-badge">projection only · authority none</span>
    </div>
    <div class="aspect-matrix-controls">
      <div class="aspect-matrix-tabs" role="tablist" aria-label="Aspect projection view">
        <button class="aspect-matrix-tab active" type="button" data-aspect-view="human" aria-selected="true">Human</button>
        <button class="aspect-matrix-tab" type="button" data-aspect-view="governed" aria-selected="false">Governed</button>
        <button class="aspect-matrix-tab" type="button" data-aspect-view="split" aria-selected="false">Split</button>
      </div>
      <div class="aspect-matrix-actions">
        <select id="ecosystemAspectRole" class="aspect-role" aria-label="Aspect disclosure role">
          <option value="public">Public</option>
          <option value="contributor">Contributor</option>
          <option value="reviewer">Reviewer</option>
          <option value="custodian">Custodian</option>
        </select>
        <button class="sv-btn sv-btn-secondary" id="ecosystemAspectRawToggle" type="button">Raw JSONL</button>
        <button class="sv-btn sv-btn-secondary" id="ecosystemAspectExport" type="button">Export aspects</button>
      </div>
    </div>
    <div class="aspect-boundary">No aspect silently grants ownership, consent, authority, admissibility, value, payment, custody, publication, or settlement.</div>
    <div id="ecosystemAspectGrid" class="aspect-matrix-grid" aria-live="polite"></div>
    <div id="ecosystemAspectDetail" class="aspect-detail"><p class="muted">Select an aspect to inspect its attached records.</p></div>
    <pre id="ecosystemAspectRaw" class="aspect-raw" hidden></pre>`;
  hostAnchor.parentNode.insertBefore(section, hostAnchor.nextSibling);

  const grid = document.getElementById('ecosystemAspectGrid');
  const detail = document.getElementById('ecosystemAspectDetail');
  const raw = document.getElementById('ecosystemAspectRaw');
  const role = document.getElementById('ecosystemAspectRole');
  const rawToggle = document.getElementById('ecosystemAspectRawToggle');
  const exportButton = document.getElementById('ecosystemAspectExport');

  document.querySelectorAll('[data-aspect-view]').forEach((button) => {
    button.addEventListener('click', () => setView(button.dataset.aspectView));
  });
  role.addEventListener('change', () => {
    state.role = role.value;
    render();
  });
  rawToggle.addEventListener('click', toggleRaw);
  exportButton.addEventListener('click', exportAspects);
  document.addEventListener('click', handleCanonicalSubjectSelection);
  document.addEventListener('focusin', handleCanonicalSubjectSelection);

  Promise.all([loadJson(REGISTRY_PATH), loadJson(EVENTS_PATH)])
    .then(([registryPayload, eventsPayload]) => {
      if (registryPayload.authority_effect !== 'NONE' || eventsPayload.authority_effect !== 'NONE') throw new Error('authority boundary mismatch');
      state.registry = Array.isArray(registryPayload.aspects) ? registryPayload.aspects : [];
      state.events = Array.isArray(eventsPayload.events) ? eventsPayload.events : [];
      state.activeSubjectRef = eventsPayload.interaction_id || null;
      render();
    })
    .catch((error) => failClosed(error.message));

  async function loadJson(path) {
    const response = await fetch(path, { cache: 'no-store' });
    if (!response.ok) throw new Error(`${path} returned ${response.status}`);
    return response.json();
  }

  function setView(view) {
    if (!['human', 'governed', 'split'].includes(view)) return;
    state.view = view;
    document.querySelectorAll('[data-aspect-view]').forEach((button) => {
      const selected = button.dataset.aspectView === view;
      button.classList.toggle('active', selected);
      button.setAttribute('aria-selected', String(selected));
    });
    render();
  }

  function handleCanonicalSubjectSelection(event) {
    const node = event.target?.closest?.('[data-event-id],[data-claim-id],[data-artifact-id],[data-execution-id]');
    if (!node) return;
    state.activeSubjectRef = node.dataset.eventId || node.dataset.claimId || node.dataset.artifactId || node.dataset.executionId || null;
    render();
  }

  function recordsFor(aspectId) {
    return state.events.filter((event) => event.aspect_id === aspectId && isDisclosable(event));
  }

  function isDisclosable(event) {
    if (state.role === 'custodian') return true;
    if (state.role === 'reviewer') return event.authority_effect !== 'ALLOW' || event.governed_projection?.reviewer_visible !== false;
    if (state.role === 'contributor') return event.governed_projection?.restricted_to_custodian !== true;
    return event.governed_projection?.public_hidden !== true && !event.subject_refs.some((ref) => String(ref).startsWith('secret:'));
  }

  function render() {
    grid.replaceChildren();
    state.registry.forEach((aspect) => {
      const records = recordsFor(aspect.id);
      const latest = records[records.length - 1] || null;
      const cell = document.createElement('article');
      cell.className = 'aspect-cell';
      cell.dataset.aspectId = aspect.id;
      cell.tabIndex = 0;
      cell.innerHTML = `<strong>${escapeHtml(aspect.id.replaceAll('_', ' '))}</strong><span>${escapeHtml(aspect.question)}</span><span class="aspect-status">status=${escapeHtml(latest?.status || 'UNRESOLVED')} · records=${records.length}</span>`;
      cell.addEventListener('click', () => selectAspect(aspect.id));
      cell.addEventListener('focus', () => selectAspect(aspect.id));
      grid.appendChild(cell);
    });
    raw.textContent = state.events.map((event) => JSON.stringify(projectRecord(event))).join('\n');
    if (state.activeAspectId) selectAspect(state.activeAspectId, false);
  }

  function selectAspect(aspectId, scroll = true) {
    state.activeAspectId = aspectId;
    grid.querySelectorAll('[data-aspect-id]').forEach((node) => node.classList.toggle('active', node.dataset.aspectId === aspectId));
    const aspect = state.registry.find((entry) => entry.id === aspectId);
    const records = recordsFor(aspectId);
    if (!aspect) return;
    const human = `<div><strong>${escapeHtml(aspect.question)}</strong><p>${escapeHtml(humanSummary(records))}</p><p class="muted">Does not prove: ${escapeHtml(aspect.does_not_prove.join(', '))}</p></div>`;
    const governed = `<pre>${escapeHtml(JSON.stringify({ aspect, records: records.map(projectRecord), active_subject_ref: state.activeSubjectRef, role: state.role }, null, 2))}</pre>`;
    detail.innerHTML = state.view === 'human' ? human : state.view === 'governed' ? governed : `<div class="aspect-matrix-grid"><div>${human}</div><div>${governed}</div></div>`;
    if (scroll) detail.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
  }

  function projectRecord(event) {
    if (state.role === 'custodian' || state.role === 'reviewer') return event;
    const copy = JSON.parse(JSON.stringify(event));
    if (state.role === 'public') {
      copy.actor_ref = 'redacted:actor';
      copy.evidence_refs = copy.evidence_refs.map(() => 'redacted:evidence');
      copy.authority_refs = copy.authority_refs.map(() => 'redacted:authority');
      copy.governed_projection = { public_projection: true, authority_effect: copy.authority_effect };
    }
    return copy;
  }

  function humanSummary(records) {
    if (!records.length) return 'No admissible evidence-backed record is available; this aspect remains unresolved.';
    const latest = records[records.length - 1];
    return latest.human_projection?.summary || `Latest governed status: ${latest.status}.`;
  }

  function toggleRaw() {
    state.rawMode = !state.rawMode;
    grid.hidden = state.rawMode;
    detail.hidden = state.rawMode;
    raw.hidden = !state.rawMode;
    rawToggle.textContent = state.rawMode ? 'Formatted aspects' : 'Raw JSONL';
  }

  function exportAspects() {
    const payload = {
      schema: 'stegverse.governed-aspect-export.v0.1',
      authority_effect: 'NONE',
      role: state.role,
      view: state.view,
      active_subject_ref: state.activeSubjectRef,
      exported_at: new Date().toISOString(),
      events: state.events.filter(isDisclosable).map(projectRecord),
    };
    const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = 'stegverse-governed-aspects.json';
    anchor.click();
    URL.revokeObjectURL(url);
  }

  function failClosed(message) {
    grid.innerHTML = '<p class="muted">Aspect records unavailable.</p>';
    detail.innerHTML = `<p class="muted">No aspect, authority, value, ownership, permission, custody, or settlement claim is inferred. ${escapeHtml(message)}</p>`;
    raw.textContent = '';
  }

  function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, (character) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' }[character]));
  }

  window.StegVerseAspectMatrix = Object.freeze({
    version: '0.1',
    getState: () => ({ ...state, registry: state.registry.slice(), events: state.events.slice() }),
    setView,
    selectAspect,
  });
})();
