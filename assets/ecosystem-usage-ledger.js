(() => {
  'use strict';

  const STORAGE_KEY = 'stegverse.transitionUsageEvents.v1';
  const roleRoot = document.getElementById('entryPointRoles');
  const summaryRoot = document.getElementById('sessionSummary');
  const timelineRoot = document.getElementById('transitionTimeline');
  const statusRoot = document.getElementById('sessionStatus');
  const filterRoot = document.getElementById('sessionFilter');
  const loadButton = document.getElementById('loadSession');
  const exportButton = document.getElementById('exportSession');
  let activePayload = null;
  let activeConfig = null;

  const esc = (value) => String(value ?? '').replace(/[&<>'"]/g, (char) => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[char]));

  function validateEvent(event, sessionId) {
    const required = ['measurement_id','session_id','transition_id','origin_entry_point','entry_point','entry_point_role','interaction_type','metric_owner','measurement_source','metrics','timestamp'];
    for (const field of required) {
      if (event[field] === undefined || event[field] === null || event[field] === '') throw new Error(`usage event missing ${field}`);
    }
    if (event.session_id !== sessionId) throw new Error('mixed session identities are not allowed');
    if (typeof event.metrics !== 'object' || Array.isArray(event.metrics)) throw new Error('metrics must be an object');
    for (const [name, metric] of Object.entries(event.metrics)) {
      if (!name || typeof metric !== 'object') throw new Error('invalid metric');
      if (!['MEASURED','CONFIGURED','DERIVED','UNAVAILABLE'].includes(metric.evidence_class)) throw new Error(`invalid evidence class for ${name}`);
      if (metric.evidence_class === 'UNAVAILABLE' && metric.value !== null) throw new Error(`UNAVAILABLE metric ${name} must use null`);
    }
  }

  function dedupe(events, sessionId) {
    const seen = new Set();
    return events.filter((event) => {
      validateEvent(event, sessionId);
      const key = `${event.metric_owner}::${event.measurement_id}`;
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });
  }

  function renderRoles(payload) {
    roleRoot.innerHTML = payload.entry_points.map((role) => `
      <article class="card role-card">
        <h3>${esc(role.display_name)}</h3>
        <p>${esc(role.primary_role)}</p>
        <strong>Related roles</strong>
        <ul>${role.related_roles.map((item) => `<li>${esc(item)}</li>`).join('')}</ul>
        <strong>Interaction types</strong>
        <ul>${role.interaction_types.map((item) => `<li>${esc(item)}</li>`).join('')}</ul>
        <p class="muted"><strong>Boundary:</strong> ${esc(role.authority_boundary)}</p>
      </article>`).join('');
  }

  function aggregate(events) {
    const totals = new Map();
    const evidenceCounts = {MEASURED:0, CONFIGURED:0, DERIVED:0, UNAVAILABLE:0};
    for (const event of events) {
      for (const [name, metric] of Object.entries(event.metrics)) {
        evidenceCounts[metric.evidence_class] += 1;
        if (metric.evidence_class === 'UNAVAILABLE' || metric.value === null) continue;
        const key = `${name}::${metric.unit}::${metric.evidence_class}`;
        totals.set(key, (totals.get(key) || 0) + Number(metric.value));
      }
    }
    return {totals, evidenceCounts};
  }

  function renderSummary(sessionId, events, sourceLabel) {
    const {totals, evidenceCounts} = aggregate(events);
    const owners = [...new Set(events.map((event) => event.metric_owner))];
    const transitions = [...new Set(events.map((event) => event.transition_id))];
    summaryRoot.innerHTML = `
      <div class="card"><strong>Session</strong><span class="muted">${esc(sessionId)}</span></div>
      <div class="card"><strong>Transitions</strong><span class="muted">${transitions.length}</span></div>
      <div class="card"><strong>Measurement owners</strong><span class="muted">${owners.map(esc).join(', ')}</span></div>
      <div class="card"><strong>Evidence posture</strong><span class="muted">Measured ${evidenceCounts.MEASURED} · Configured ${evidenceCounts.CONFIGURED} · Derived ${evidenceCounts.DERIVED} · Unavailable ${evidenceCounts.UNAVAILABLE}</span></div>`;
    statusRoot.textContent = `${sourceLabel} · ${events.length} unique usage events · ${totals.size} evidence-separated aggregate metrics · no double counting by owner + measurement identity`;
  }

  function receiptHref(ref, transitionId) {
    const encoded = encodeURIComponent(transitionId);
    if (/^https:\/\//.test(ref)) return ref;
    return `governed-transitions.html?transition_id=${encoded}#receipt-${encodeURIComponent(ref)}`;
  }

  function renderTimeline(events) {
    const grouped = new Map();
    for (const event of events) {
      if (!grouped.has(event.transition_id)) grouped.set(event.transition_id, []);
      grouped.get(event.transition_id).push(event);
    }
    timelineRoot.innerHTML = [...grouped.entries()].map(([transitionId, items]) => {
      items.sort((a, b) => String(a.timestamp).localeCompare(String(b.timestamp)));
      const first = items[0];
      const metricCards = items.flatMap((event) => Object.entries(event.metrics).map(([name, metric]) => `
        <div class="metric"><span>${esc(name)} · ${esc(event.metric_owner)}</span><strong>${metric.value === null ? 'Unavailable' : `${esc(metric.value)} ${esc(metric.unit)}`}</strong><span>${esc(metric.evidence_class)}</span></div>`)).join('');
      const owners = [...new Set(items.map((item) => item.metric_owner))];
      const receipts = [...new Set(items.flatMap((item) => item.receipt_refs || []))];
      const receiptLinks = receipts.length ? `<div class="receipt-links">${receipts.map((ref) => `<a class="sv-btn sv-btn-secondary" href="${esc(receiptHref(String(ref), transitionId))}">${esc(ref)}</a>`).join('')}</div>` : '';
      return `<article class="transition-card">
        <div class="usage-prepend"><strong>Usage prepend</strong><br>Session: ${esc(first.session_id)} · Transition: ${esc(transitionId)} · Origin: ${esc(first.origin_entry_point)} · Entry points: ${esc([...new Set(items.map((item) => item.entry_point))].join(', '))}<br>Metric owners: ${esc(owners.join(', '))} · Receipt refs: ${esc(receipts.join(', ') || 'none')}</div>
        ${receiptLinks}
        <div class="metric-grid">${metricCards}</div>
        <p class="muted">Transition content follows this usage block. The prepend is presentation metadata and does not alter provider output or transition hashes.</p>
      </article>`;
    }).join('');
  }

  async function loadJson(path) {
    const response = await fetch(path, {cache: 'no-store'});
    if (!response.ok) throw new Error(`${path} returned ${response.status}`);
    return response.json();
  }

  function safeApiBase(value) {
    if (!value) return window.location.origin;
    const url = new URL(value, window.location.href);
    if (url.origin !== window.location.origin && url.protocol !== 'https:') throw new Error('usage API must be same-origin or HTTPS');
    return url.href.replace(/\/$/, '');
  }

  function isIntegrityFailure(error) {
    const client = window.StegVerseUsageAuthClient;
    return Boolean(client && client.UsageIntegrityError && error instanceof client.UsageIntegrityError);
  }

  async function loadLiveSession(sessionId) {
    const live = activeConfig.live_transport || {};
    if (live.enabled !== true) return null;
    if (!window.StegVerseUsageAuthClient) throw new Error('authenticated usage client is unavailable');
    if (!activeConfig.usage_api_base) throw new Error('authorized usage API base is not configured');
    const payload = await window.StegVerseUsageAuthClient.retrieve({
      sessionId,
      apiBase: safeApiBase(activeConfig.usage_api_base)
    });
    return {
      payload,
      source: 'LIVE_USAGE_API',
      retrievalReceipt: payload.retrieval_receipt
    };
  }

  async function loadSession(sessionId) {
    const clean = String(sessionId || '').trim();
    if (!clean) throw new Error('session_id is required');

    const liveConfig = activeConfig.live_transport || {};
    if (liveConfig.enabled === true) {
      try {
        const live = await loadLiveSession(clean);
        if (live) return live;
      } catch (error) {
        if (isIntegrityFailure(error) || liveConfig.fallback_on_integrity_failure !== false) throw error;
        if (liveConfig.fallback_on_network_unavailable !== true) throw error;
        console.warn('Live usage transport unavailable; applying explicitly configured bounded fallback', error);
      }
    }

    if (activeConfig.allow_local_storage) {
      try {
        const stored = JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null');
        if (stored && stored.session_id === clean && Array.isArray(stored.events)) {
          return {payload: stored, source: 'SYNCHRONIZED_LOCAL_LEDGER', retrievalReceipt: null};
        }
      } catch (error) {
        console.warn('Ignoring invalid local usage ledger', error);
      }
    }
    if (activeConfig.allow_fixture_fallback) {
      const fixture = await loadJson(activeConfig.fixture_path);
      if (fixture.session_id === clean) return {payload: fixture, source: 'CONFIGURED_FIXTURE_FALLBACK', retrievalReceipt: null};
    }
    throw new Error(`session ${clean} was not available`);
  }

  function present(payload, sourceLabel, retrievalReceipt = null) {
    const unique = dedupe(payload.events, payload.session_id);
    activePayload = {
      session_id: payload.session_id,
      events: unique,
      source: sourceLabel,
      retrieval_receipt: retrievalReceipt,
      authority: 'none',
      custody: 'not-recorded-by-site'
    };
    filterRoot.value = payload.session_id;
    renderSummary(payload.session_id, unique, sourceLabel);
    renderTimeline(unique);
    const url = new URL(window.location.href);
    url.searchParams.set(activeConfig.session_query_parameter, payload.session_id);
    window.history.replaceState({}, '', url);
  }

  function exportActiveSession() {
    if (!activePayload) throw new Error('no active session to export');
    const body = JSON.stringify(activePayload, null, 2) + '\n';
    const blob = new Blob([body], {type: 'application/json'});
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `${activePayload.session_id}.usage.json`;
    link.click();
    URL.revokeObjectURL(link.href);
  }

  async function main() {
    activeConfig = await loadJson('data/ecosystem-usage-config.json');
    const liveConfig = activeConfig.live_transport || {};
    if (liveConfig.enabled === true && liveConfig.activation_requires !== 'AUTHORIZED_DEPLOYED_ENDPOINT') {
      throw new Error('live usage activation boundary is invalid');
    }
    const roles = await loadJson(activeConfig.roles_path);
    renderRoles(roles);
    const querySession = new URL(window.location.href).searchParams.get(activeConfig.session_query_parameter);
    let initial = querySession;
    if (!initial && activeConfig.allow_local_storage) {
      try {
        const stored = JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null');
        if (stored && stored.session_id) initial = stored.session_id;
      } catch (error) {
        console.warn('Ignoring invalid local usage ledger', error);
      }
    }
    if (!initial && activeConfig.allow_fixture_fallback) {
      const fixture = await loadJson(activeConfig.fixture_path);
      initial = fixture.session_id;
    }
    const loaded = await loadSession(initial);
    present(loaded.payload, loaded.source, loaded.retrievalReceipt);
  }

  loadButton.addEventListener('click', async () => {
    try {
      const loaded = await loadSession(filterRoot.value);
      present(loaded.payload, loaded.source, loaded.retrievalReceipt);
    } catch (error) {
      statusRoot.textContent = `USAGE_SESSION_LOAD_FAILED: ${error.message}`;
    }
  });
  exportButton.addEventListener('click', () => {
    try { exportActiveSession(); }
    catch (error) { statusRoot.textContent = `USAGE_EXPORT_FAILED: ${error.message}`; }
  });

  main().catch((error) => {
    statusRoot.textContent = `USAGE_LEDGER_LOAD_FAILED: ${error.message}`;
    timelineRoot.innerHTML = '<div class="boundary">The ledger failed closed. No usage totals were displayed.</div>';
  });
})();
