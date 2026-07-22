(() => {
  'use strict';

  const PACKETS_KEY = 'gp10.workspace.evidence.packets.v1';
  const REVIEWS_KEY = 'gp10.workspace.evidence.reviews.v1';
  const RECORDS_KEY = 'gp10.workspace.records.v1';
  const $ = (id) => document.getElementById(id);
  const readStore = (key) => { try { return JSON.parse(localStorage.getItem(key) || '[]'); } catch { return []; } };
  const writeStore = (key, value) => localStorage.setItem(key, JSON.stringify(value));
  const now = () => new Date().toISOString();
  const uuid = (prefix) => `${prefix}-${crypto.randomUUID ? crypto.randomUUID() : Date.now()}`;
  const lines = (text) => String(text || '').split(/\r?\n/).filter(Boolean);

  async function sha256(file) {
    const digest = await crypto.subtle.digest('SHA-256', await file.arrayBuffer());
    return [...new Uint8Array(digest)].map(v => v.toString(16).padStart(2, '0')).join('');
  }

  function parseCsv(text) {
    const rows = lines(text).map(row => row.split(',').map(v => v.trim()));
    if (rows.length < 2) throw new Error('CSV requires a header and at least one row.');
    const headers = rows.shift();
    const objects = rows.map(row => Object.fromEntries(headers.map((h, i) => [h, row[i] ?? ''])));
    const first = objects[0];
    return {
      candidate_id: first.candidate_id,
      source_system: first.source_system,
      source_record_id: first.source_record_id,
      source_owner: first.source_owner,
      authority_class: first.authority_class,
      observed_at: first.observed_at,
      evidence_class: first.evidence_class,
      source_reference: first.source_reference,
      observations: objects.map(row => ({field_name: row.field_name, field_value: row.field_value, unit: row.unit || null}))
    };
  }

  function normalizeJson(value) {
    if (Array.isArray(value)) {
      if (!value.length) throw new Error('JSON array is empty.');
      const first = value[0];
      return {
        candidate_id: first.candidate_id,
        source_system: first.source_system || 'AUTHORIZED_JSON_EXPORT',
        source_record_id: first.source_record_id || first.id || 'unknown-record',
        source_owner: first.source_owner || 'UNKNOWN',
        authority_class: first.authority_class || 'UNVERIFIED_EXPORT',
        observed_at: first.observed_at || now(),
        evidence_class: first.evidence_class || 'OTHER',
        source_reference: first.source_reference || null,
        observations: value.flatMap((item, index) => Object.entries(item).filter(([key]) => !['candidate_id','source_system','source_record_id','source_owner','authority_class','observed_at','evidence_class','source_reference'].includes(key)).map(([field_name, field_value]) => ({field_name: `${field_name}`, field_value: typeof field_value === 'object' ? JSON.stringify(field_value) : String(field_value), unit: null, row: index + 1})))
      };
    }
    if (!value || typeof value !== 'object') throw new Error('JSON must be an object or array.');
    if (Array.isArray(value.observations)) return value;
    return {
      candidate_id: value.candidate_id,
      source_system: value.source_system || 'AUTHORIZED_JSON_EXPORT',
      source_record_id: value.source_record_id || value.id || 'unknown-record',
      source_owner: value.source_owner || 'UNKNOWN',
      authority_class: value.authority_class || 'UNVERIFIED_EXPORT',
      observed_at: value.observed_at || now(),
      evidence_class: value.evidence_class || 'OTHER',
      source_reference: value.source_reference || null,
      observations: Object.entries(value).filter(([key]) => !['candidate_id','source_system','source_record_id','source_owner','authority_class','observed_at','evidence_class','source_reference'].includes(key)).map(([field_name, field_value]) => ({field_name, field_value: typeof field_value === 'object' ? JSON.stringify(field_value) : String(field_value), unit: null}))
    };
  }

  function conflictsFor(packet) {
    const packets = readStore(PACKETS_KEY);
    const conflicts = [];
    for (const observation of packet.observations) {
      const prior = packets.flatMap(p => p.observations.map(o => ({...o, packet_id: p.packet_id, candidate_id: p.candidate_id}))).filter(o => o.candidate_id === packet.candidate_id && o.field_name === observation.field_name && String(o.field_value) !== String(observation.field_value));
      for (const item of prior) conflicts.push({field_name: observation.field_name, incoming_value: observation.field_value, prior_value: item.field_value, prior_packet_id: item.packet_id});
    }
    return conflicts;
  }

  function buildReview(packet, issues) {
    if (!issues.length) return null;
    return {
      review_id: uuid('REVIEW'),
      candidate_id: packet.candidate_id,
      packet_id: packet.packet_id,
      status: 'OPEN',
      priority: issues.some(i => i.type === 'IDENTITY_CONFLICT') ? 'STOP_WORK' : 'HIGH',
      issues: issues.map(i => `${i.type}: ${i.message}`),
      required_actions: ['Compare original source records.', 'Identify the authoritative owner for each disputed field.', 'Preserve the rejected value and rationale; never silently overwrite.'],
      resolution: null,
      resolved_by: null,
      execution_authority: false,
      history: [{timestamp: now(), actor: 'gp10-evidence-integration.js', action: 'Created browser-local evidence review item'}]
    };
  }

  function renderQueue() {
    const target = $('evidenceReviewQueue');
    if (!target) return;
    const reviews = readStore(REVIEWS_KEY);
    if (!reviews.length) { target.textContent = 'No evidence-review items.'; return; }
    target.innerHTML = reviews.map(r => `<article class="transition-card"><strong>${r.priority} · ${r.status}</strong><div class="muted">${r.review_id} · ${r.packet_id}</div><p>${r.issues.map(x => escapeHtml(x)).join('<br>')}</p><button type="button" class="sv-btn sv-btn-secondary" data-review="${r.review_id}">Mark resolved locally</button></article>`).join('');
    target.querySelectorAll('[data-review]').forEach(button => button.addEventListener('click', () => {
      const items = readStore(REVIEWS_KEY);
      const item = items.find(r => r.review_id === button.dataset.review);
      if (item) {
        item.status = 'RESOLVED';
        item.resolution = 'Browser-local tester resolution; requires governed review before reliance.';
        item.resolved_by = 'LOCAL_TESTER';
        item.history.push({timestamp: now(), actor: 'LOCAL_TESTER', action: 'Marked resolved locally; no authority granted'});
        writeStore(REVIEWS_KEY, items);
        renderQueue();
      }
    }));
  }

  function escapeHtml(value) { return String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c])); }

  function download(name, payload) {
    const blob = new Blob([JSON.stringify(payload, null, 2)], {type: 'application/json'});
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = name;
    link.click();
    setTimeout(() => URL.revokeObjectURL(link.href), 1000);
  }

  async function importFile() {
    const file = $('evidenceFile').files[0];
    if (!file) return setIntegrationStatus('Choose a JSON or CSV file.');
    try {
      const text = await file.text();
      const raw = file.name.toLowerCase().endsWith('.csv') ? parseCsv(text) : normalizeJson(JSON.parse(text));
      raw.candidate_id = raw.candidate_id || $('candidateId')?.value?.trim();
      if (!raw.candidate_id) throw new Error('candidate_id is required in the file or current form.');
      if (!Array.isArray(raw.observations) || !raw.observations.length) throw new Error('No observations found.');
      const packet = {
        packet_version: '1.0.0', packet_id: uuid('EVID'), imported_at: now(), candidate_id: raw.candidate_id,
        source: {system: raw.source_system || 'AUTHORIZED_EXPORT', record_id: raw.source_record_id || file.name, owner: raw.source_owner || 'UNKNOWN', authority_class: raw.authority_class || 'UNVERIFIED_EXPORT', observed_at: raw.observed_at || now(), source_reference: raw.source_reference || null, original_filename: file.name, original_sha256: await sha256(file)},
        evidence_class: raw.evidence_class || 'OTHER', observations: raw.observations.map(o => ({field_name: String(o.field_name || ''), field_value: o.field_value, unit: o.unit || null})).filter(o => o.field_name),
        conflicts: [], custody_state: 'BROWSER_LOCAL_UNCUSTODIED', execution_authority: false
      };
      packet.conflicts = conflictsFor(packet);
      const issues = packet.conflicts.map(c => ({type: ['unit_number','serial_number','donor_lineage'].includes(c.field_name) ? 'IDENTITY_CONFLICT' : 'VALUE_CONFLICT', message: `${c.field_name} differs: incoming ${c.incoming_value}; prior ${c.prior_value}`}));
      const packets = readStore(PACKETS_KEY); packets.unshift(packet); writeStore(PACKETS_KEY, packets.slice(0, 100));
      const review = buildReview(packet, issues); if (review) { const reviews = readStore(REVIEWS_KEY); reviews.unshift(review); writeStore(REVIEWS_KEY, reviews.slice(0, 100)); }
      const refs = $('evidenceRefs'); if (refs) refs.value = [...new Set(lines(refs.value).concat(`external-evidence:${packet.packet_id}`))].join('\n');
      $('evidencePacketPreview').textContent = JSON.stringify(packet, null, 2);
      renderQueue();
      setIntegrationStatus(`Imported ${packet.observations.length} observations; ${packet.conflicts.length} conflict(s). No authority granted.`);
    } catch (error) { setIntegrationStatus(`FAIL-CLOSED: ${error.message}`); }
  }

  function exportBundle() {
    const latest = (() => { try { return JSON.parse(localStorage.getItem(`${RECORDS_KEY}.latest`) || 'null'); } catch { return null; } })();
    const bundle = {bundle_version: '1.0.0', exported_at: now(), custody_state: 'BROWSER_LOCAL_UNCUSTODIED', execution_authority: false, latest_candidate_record: latest, evidence_packets: readStore(PACKETS_KEY), evidence_reviews: readStore(REVIEWS_KEY), warnings: ['Export is not custody, approval, or execution authority.']};
    download(`gp10-validation-bundle-${new Date().toISOString().slice(0,10)}.json`, bundle);
    setIntegrationStatus('Validation bundle exported.');
  }

  function setIntegrationStatus(message) { const node = $('integrationStatus'); if (node) node.textContent = message; }

  const form = $('gp10Form');
  if (!form) return;
  const panel = document.createElement('section');
  panel.className = 'panel';
  panel.innerHTML = `<h2 class="sv-h2">External evidence integration</h2><p class="muted">Import an authorized JSON or CSV export. The original file is hashed; source ownership remains external.</p><div class="grid"><label class="field wide"><span>Authorized evidence file</span><input id="evidenceFile" type="file" accept=".json,.csv,application/json,text/csv"></label></div><div class="actions" style="margin-top:12px"><button class="sv-btn sv-btn-secondary" id="importEvidence" type="button">Import evidence</button><button class="sv-btn sv-btn-secondary" id="exportValidationBundle" type="button">Export complete validation bundle</button></div><p id="integrationStatus" class="status" aria-live="polite"></p><h3>Latest evidence packet</h3><pre id="evidencePacketPreview" class="receipt">No imported evidence.</pre><h3>Evidence review queue</h3><div id="evidenceReviewQueue" class="workspace">No evidence-review items.</div>`;
  form.parentNode.insertBefore(panel, form.nextSibling);
  $('importEvidence').addEventListener('click', importFile);
  $('exportValidationBundle').addEventListener('click', exportBundle);
  renderQueue();
})();
