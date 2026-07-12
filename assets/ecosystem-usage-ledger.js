(() => {
  'use strict';

  const STORAGE_KEY = 'stegverse.transitionUsageEvents.v1';
  const roleRoot = document.getElementById('entryPointRoles');
  const summaryRoot = document.getElementById('sessionSummary');
  const timelineRoot = document.getElementById('transitionTimeline');
  const statusRoot = document.getElementById('sessionStatus');

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

  function renderSummary(sessionId, events) {
    const {totals, evidenceCounts} = aggregate(events);
    const owners = [...new Set(events.map((event) => event.metric_owner))];
    const transitions = [...new Set(events.map((event) => event.transition_id))];
    summaryRoot.innerHTML = `
      <div class="card"><strong>Session</strong><span class="muted">${esc(sessionId)}</span></div>
      <div class="card"><strong>Transitions</strong><span class="muted">${transitions.length}</span></div>
      <div class="card"><strong>Measurement owners</strong><span class="muted">${owners.map(esc).join(', ')}</span></div>
      <div class="card"><strong>Evidence posture</strong><span class="muted">Measured ${evidenceCounts.MEASURED} · Configured ${evidenceCounts.CONFIGURED} · Derived ${evidenceCounts.DERIVED} · Unavailable ${evidenceCounts.UNAVAILABLE}</span></div>`;
    statusRoot.textContent = `${events.length} unique usage events · ${totals.size} evidence-separated aggregate metrics · no double counting by owner + measurement identity`;
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
      return `<article class="transition-card">
        <div class="usage-prepend"><strong>Usage prepend</strong><br>Session: ${esc(first.session_id)} · Transition: ${esc(transitionId)} · Origin: ${esc(first.origin_entry_point)} · Entry points: ${esc([...new Set(items.map((item) => item.entry_point))].join(', '))}<br>Metric owners: ${esc(owners.join(', '))} · Receipt refs: ${esc(receipts.join(', ') || 'none')}</div>
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

  async function main() {
    const [roles, fixture] = await Promise.all([
      loadJson('data/entry-point-roles.json'),
      loadJson('data/usage-session-fixture.json')
    ]);
    renderRoles(roles);
    let events = fixture.events;
    try {
      const stored = JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null');
      if (stored && Array.isArray(stored.events) && stored.session_id) {
        events = stored.events;
        fixture.session_id = stored.session_id;
      }
    } catch (error) {
      console.warn('Ignoring invalid local usage ledger', error);
    }
    const unique = dedupe(events, fixture.session_id);
    renderSummary(fixture.session_id, unique);
    renderTimeline(unique);
  }

  main().catch((error) => {
    statusRoot.textContent = `USAGE_LEDGER_LOAD_FAILED: ${error.message}`;
    timelineRoot.innerHTML = '<div class="boundary">The ledger failed closed. No usage totals were displayed.</div>';
  });
})();
