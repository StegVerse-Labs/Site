(() => {
  'use strict';

  const PACKETS_KEY = 'gp10.workspace.evidence.packets.v1';
  const REVIEWS_KEY = 'gp10.workspace.evidence.reviews.v1';
  const RECORDS_KEY = 'gp10.workspace.records.v1';
  const $ = (id) => document.getElementById(id);
  const now = () => new Date().toISOString();
  const uuid = (prefix) => `${prefix}-${(crypto.randomUUID ? crypto.randomUUID() : String(Date.now())).replace(/[^A-Za-z0-9-]/g, '').toUpperCase()}`;
  const readStore = (key) => { try { return JSON.parse(localStorage.getItem(key) || '[]'); } catch { return []; } };
  const writeStore = (key, value) => localStorage.setItem(key, JSON.stringify(value));
  const splitLines = (value) => String(value || '').split(/\r?\n/).map(v => v.trim()).filter(Boolean);

  async function hashText(text) {
    const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
    return [...new Uint8Array(digest)].map(v => v.toString(16).padStart(2, '0')).join('');
  }

  function parseCsv(text) {
    const rows = splitLines(text).map(line => line.split(',').map(value => value.trim()));
    if (rows.length < 2) throw new Error('CSV requires a header and at least one data row.');
    const headers = rows.shift();
    return rows.map(row => Object.fromEntries(headers.map((header, index) => [header, row[index] ?? ''])));
  }

  function parseRecords(text, filename) {
    if (filename.toLowerCase().endsWith('.csv')) return parseCsv(text);
    const parsed = JSON.parse(text);
    const records = Array.isArray(parsed) ? parsed : Array.isArray(parsed.records) ? parsed.records : [parsed];
    if (!records.length || !records.every(item => item && typeof item === 'object' && !Array.isArray(item))) {
      throw new Error('JSON must contain one object or an array of objects.');
    }
    return records;
  }

  function scalar(value) {
    if (value === null || value === undefined || value === '') return null;
    if (typeof value !== 'string') return value;
    const text = value.trim();
    if (!text) return null;
    if (/^-?\d+(\.\d+)?$/.test(text)) return Number(text);
    if (/^(true|false)$/i.test(text)) return text.toLowerCase() === 'true';
    return text;
  }

  function observations(records, evidenceClass) {
    const ignored = new Set(['candidate_id','source_system','source_record_id','source_owner','owner_role','authority_class','observed_at','evidence_class','source_reference']);
    const output = [];
    records.forEach((record, row) => Object.entries(record).forEach(([field, raw]) => {
      if (ignored.has(field)) return;
      const value = scalar(raw);
      if (value !== null) output.push({field, value, unit: null, evidence_class: evidenceClass, confidence: 'MEDIUM', source_path: `records[${row}].${field}`});
    }));
    if (!output.length) throw new Error('No non-empty observations were found.');
    return output;
  }

  function findConflicts(packet) {
    const priorPackets = readStore(PACKETS_KEY).filter(item => item.asset?.candidate_id === packet.asset.candidate_id);
    const conflicts = [];
    for (const incoming of packet.observations) {
      for (const priorPacket of priorPackets) {
        for (const existing of priorPacket.observations || []) {
          if (existing.field === incoming.field && JSON.stringify(existing.value) !== JSON.stringify(incoming.value)) {
            conflicts.push({
              field: incoming.field,
              existing_value: existing.value,
              incoming_value: incoming.value,
              existing_authority_class: priorPacket.source?.authority_class || null,
              incoming_authority_class: packet.source.authority_class,
              resolution_state: 'QUALIFIED_REVIEW_REQUIRED'
            });
          }
        }
      }
    }
    return conflicts;
  }

  function createReview(packet) {
    if (!packet.conflicts.length) return null;
    const identityFields = new Set(['unit_number','serial_number','reporting_mark','donor_lineage']);
    const stopWork = packet.conflicts.some(conflict => identityFields.has(conflict.field));
    return {
      review_id: uuid('REVIEW'),
      candidate_id: packet.asset.candidate_id,
      packet_id: packet.packet_id,
      status: 'OPEN',
      priority: stopWork ? 'STOP_WORK' : 'HIGH',
      issues: packet.conflicts.map(conflict => `${conflict.field}: incoming ${JSON.stringify(conflict.incoming_value)} conflicts with ${JSON.stringify(conflict.existing_value)}`),
      required_actions: [
        'Compare the original source records and their authority classes.',
        'Identify the authoritative owner for each disputed field.',
        'Preserve the rejected value and rationale; never silently overwrite.'
      ],
      resolution: null,
      resolved_by: null,
      execution_authority: false,
      history: [{timestamp: now(), actor: 'assets/gp10-evidence-integration.js', action: 'Created browser-local evidence review item'}]
    };
  }

  function renderQueue() {
    const target = $('evidenceReviewQueue');
    if (!target) return;
    const reviews = readStore(REVIEWS_KEY);
    if (!reviews.length) { target.textContent = 'No evidence-review items.'; return; }
    target.innerHTML = reviews.map(review => `<article class="transition-card"><strong>${escapeHtml(review.priority)} · ${escapeHtml(review.status)}</strong><div class="muted">${escapeHtml(review.review_id)} · ${escapeHtml(review.packet_id)}</div><p>${review.issues.map(escapeHtml).join('<br>')}</p><button type="button" class="sv-btn sv-btn-secondary" data-review="${escapeHtml(review.review_id)}">Mark resolved locally</button></article>`).join('');
    target.querySelectorAll('[data-review]').forEach(button => button.addEventListener('click', () => {
      const items = readStore(REVIEWS_KEY);
      const item = items.find(review => review.review_id === button.dataset.review);
      if (!item) return;
      item.status = 'RESOLVED';
      item.resolution = 'Browser-local tester resolution; governed review remains required before reliance.';
      item.resolved_by = 'LOCAL_TESTER';
      item.history.push({timestamp: now(), actor: 'LOCAL_TESTER', action: 'Marked resolved locally; no authority granted'});
      writeStore(REVIEWS_KEY, items);
      renderQueue();
    }));
  }

  function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[char]));
  }

  function download(name, payload) {
    const blob = new Blob([JSON.stringify(payload, null, 2)], {type: 'application/json'});
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = name;
    link.click();
    setTimeout(() => URL.revokeObjectURL(link.href), 1000);
  }

  async function importFile() {
    const file = $('evidenceFile')?.files?.[0];
    if (!file) return setStatus('Choose a JSON or CSV file.');
    try {
      const text = await file.text();
      const records = parseRecords(text, file.name);
      const candidateId = $('candidateId').value.trim() || String(records[0].candidate_id || '').trim();
      if (!candidateId) throw new Error('candidate_id is required in the form or source file.');
      const transport = file.name.toLowerCase().endsWith('.csv') ? 'CSV' : 'JSON';
      const packet = {
        packet_id: uuid('EVP'),
        created_at: now(),
        source: {
          system: $('importSourceSystem').value.trim() || String(records[0].source_system || 'AUTHORIZED_EXPORT'),
          record_id: $('importSourceRecord').value.trim() || String(records[0].source_record_id || file.name),
          owner_role: $('importOwnerRole').value,
          authority_class: $('importAuthorityClass').value,
          transport,
          source_uri: null,
          observed_at: records[0].observed_at || null,
          original_sha256: await hashText(text)
        },
        asset: {
          candidate_id: candidateId,
          unit_number: $('unitNumber').value.trim() || null,
          reporting_mark: records[0].reporting_mark || null,
          donor_lineage: $('donorLineage').value || null
        },
        observations: observations(records, $('importEvidenceClass').value),
        conflicts: [],
        custody_state: 'BROWSER_LOCAL_UNCUSTODIED',
        execution_authority: false,
        history: [{timestamp: now(), actor: 'assets/gp10-evidence-integration.js', action: 'Parsed authorized browser-local export without source mutation'}]
      };
      packet.conflicts = findConflicts(packet);
      const packets = readStore(PACKETS_KEY);
      packets.unshift(packet);
      writeStore(PACKETS_KEY, packets.slice(0, 100));
      const review = createReview(packet);
      if (review) {
        const reviews = readStore(REVIEWS_KEY);
        reviews.unshift(review);
        writeStore(REVIEWS_KEY, reviews.slice(0, 100));
      }
      localStorage.setItem('gp10.workspace.import.latest', JSON.stringify(packet));
      $('importPreview').textContent = JSON.stringify(packet, null, 2);
      const reference = `external-evidence:${packet.packet_id}:${packet.source.original_sha256}`;
      const refs = $('evidenceRefs');
      refs.value = [...new Set(splitLines(refs.value).concat(reference))].join('\n');
      renderQueue();
      setStatus(`Imported ${packet.observations.length} observations; ${packet.conflicts.length} conflict(s). Canonical packet retained locally; no authority granted.`);
    } catch (error) {
      setStatus(`FAIL-CLOSED: ${error.message}`);
    }
  }

  function exportBundle() {
    let latest = null;
    try { latest = JSON.parse(localStorage.getItem(`${RECORDS_KEY}.latest`) || 'null'); } catch { latest = null; }
    const bundle = {
      bundle_version: '1.0.0',
      exported_at: now(),
      custody_state: 'BROWSER_LOCAL_UNCUSTODIED',
      execution_authority: false,
      latest_candidate_record: latest,
      evidence_packets: readStore(PACKETS_KEY),
      evidence_reviews: readStore(REVIEWS_KEY),
      warnings: ['Export is not custody, approval, evidence verification, or execution authority.']
    };
    download(`gp10-validation-bundle-${new Date().toISOString().slice(0,10)}.json`, bundle);
    setStatus('Canonical validation bundle exported.');
  }

  function setStatus(message) {
    const node = $('importStatus');
    if (node) node.textContent = message;
  }

  const importButton = $('importEvidence');
  if (!importButton) return;
  importButton.addEventListener('click', importFile);

  const preview = $('importPreview');
  const latest = localStorage.getItem('gp10.workspace.import.latest');
  if (latest && preview) preview.textContent = latest;

  const importPanel = importButton.closest('section');
  const controls = document.createElement('div');
  controls.innerHTML = `<div class="actions" style="margin-top:12px"><button class="sv-btn sv-btn-secondary" id="exportValidationBundle" type="button">Export complete validation bundle</button></div><h3>Evidence review queue</h3><div id="evidenceReviewQueue" class="workspace">No evidence-review items.</div>`;
  importPanel.appendChild(controls);
  $('exportValidationBundle').addEventListener('click', exportBundle);
  renderQueue();
})();
