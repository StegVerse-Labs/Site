(() => {
  'use strict';
  const $ = (id) => document.getElementById(id);
  const PACKETS_KEY = 'gp10.workspace.evidence.packets.v1';
  const REVIEWS_KEY = 'gp10.workspace.evidence.reviews.v1';
  const RECORDS_KEY = 'gp10.workspace.records.v1';
  const read = (key) => { try { return JSON.parse(localStorage.getItem(key) || '[]'); } catch { return []; } };
  const write = (key, value) => localStorage.setItem(key, JSON.stringify(value));
  const now = () => new Date().toISOString();
  const hashText = async (text) => {
    const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
    return [...new Uint8Array(digest)].map(v => v.toString(16).padStart(2, '0')).join('');
  };
  const parseCsv = (text) => {
    const rows = text.trim().split(/\r?\n/).map(line => line.split(',').map(v => v.trim()));
    if (rows.length < 2) throw new Error('CSV requires a header and at least one data row.');
    const headers = rows.shift();
    return rows.map(row => Object.fromEntries(headers.map((header, index) => [header, row[index] ?? ''])));
  };
  const scalar = (value) => {
    const text = String(value ?? '').trim();
    if (!text) return null;
    if (/^-?\d+(\.\d+)?$/.test(text)) return Number(text);
    if (/^(true|false)$/i.test(text)) return text.toLowerCase() === 'true';
    return text;
  };
  const buildObservations = (records, evidenceClass) => {
    const output = [];
    records.forEach((record, row) => Object.entries(record).forEach(([field, raw]) => {
      const value = scalar(raw);
      if (value !== null) output.push({field, value, unit:null, evidence_class:evidenceClass, confidence:'MEDIUM', source_path:`records[${row}].${field}`});
    }));
    if (!output.length) throw new Error('No non-empty observations were found.');
    return output;
  };
  const detectInternalConflicts = (items, authorityClass) => {
    const seen = new Map(), found = [];
    items.forEach(item => {
      if (seen.has(item.field) && JSON.stringify(seen.get(item.field)) !== JSON.stringify(item.value)) {
        found.push({field:item.field, existing_value:seen.get(item.field), incoming_value:item.value,
          existing_authority_class:authorityClass, incoming_authority_class:authorityClass,
          resolution_state:'QUALIFIED_REVIEW_REQUIRED'});
      } else seen.set(item.field, item.value);
    });
    return found;
  };
  const detectCrossPacketConflicts = (packet) => {
    const found = [];
    read(PACKETS_KEY).filter(prior => prior.asset?.candidate_id === packet.asset.candidate_id).forEach(prior => {
      packet.observations.forEach(incoming => prior.observations.forEach(existing => {
        if (incoming.field === existing.field && JSON.stringify(incoming.value) !== JSON.stringify(existing.value)) {
          found.push({field:incoming.field, existing_value:existing.value, incoming_value:incoming.value,
            existing_packet_id:prior.packet_id, existing_authority_class:prior.source.authority_class,
            incoming_authority_class:packet.source.authority_class, resolution_state:'QUALIFIED_REVIEW_REQUIRED'});
        }
      }));
    });
    return found;
  };
  const reviewFor = (packet) => {
    if (!packet.conflicts.length) return null;
    const identityFields = new Set(['candidate_id','unit_number','serial_number','donor_lineage','reporting_mark']);
    const stopWork = packet.conflicts.some(item => identityFields.has(item.field));
    return {
      review_id:`REVIEW-${Date.now()}`,
      candidate_id:packet.asset.candidate_id,
      packet_id:packet.packet_id,
      status:'OPEN',
      priority:stopWork ? 'STOP_WORK' : 'HIGH',
      issues:packet.conflicts.map(item => `${item.field}: ${JSON.stringify(item.existing_value)} conflicts with ${JSON.stringify(item.incoming_value)}`),
      required_actions:['Compare the original source records.','Identify the authoritative owner for each disputed field.','Preserve the rejected value and rationale; never silently overwrite.'],
      resolution:null,resolved_by:null,execution_authority:false,
      history:[{timestamp:now(),actor:'gp10-evidence-import.js',action:'Created browser-local evidence review item'}]
    };
  };
  const escapeHtml = (value) => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]));
  function renderQueue() {
    const target = $('evidenceReviewQueue');
    if (!target) return;
    const reviews = read(REVIEWS_KEY);
    if (!reviews.length) { target.textContent = 'No evidence-review items.'; return; }
    target.innerHTML = reviews.map(item => `<article class="transition-card"><strong>${item.priority} · ${item.status}</strong><div class="muted">${escapeHtml(item.review_id)} · ${escapeHtml(item.packet_id)}</div><p>${item.issues.map(escapeHtml).join('<br>')}</p>${item.status === 'OPEN' ? `<button type="button" class="sv-btn sv-btn-secondary" data-review="${escapeHtml(item.review_id)}">Mark resolved locally</button>` : ''}</article>`).join('');
    target.querySelectorAll('[data-review]').forEach(button => button.addEventListener('click', () => {
      const reviews = read(REVIEWS_KEY);
      const item = reviews.find(review => review.review_id === button.dataset.review);
      if (item) {
        item.status = 'RESOLVED'; item.resolution = 'Browser-local tester resolution; governed review still required.'; item.resolved_by = 'LOCAL_TESTER';
        item.history.push({timestamp:now(),actor:'LOCAL_TESTER',action:'Marked resolved locally; no authority granted'});
        write(REVIEWS_KEY, reviews); renderQueue();
      }
    }));
  }
  async function importFile() {
    const file = $('evidenceFile')?.files?.[0];
    if (!file) return $('importStatus').textContent = 'Choose a JSON or CSV file.';
    try {
      const text = await file.text();
      let records;
      if (file.name.toLowerCase().endsWith('.csv')) records = parseCsv(text);
      else {
        const parsed = JSON.parse(text);
        records = Array.isArray(parsed) ? parsed : Array.isArray(parsed.records) ? parsed.records : [parsed];
        if (!records.every(item => item && typeof item === 'object' && !Array.isArray(item))) throw new Error('JSON must contain object records.');
      }
      const authorityClass = $('importAuthorityClass').value;
      const packet = {
        packet_id:`EVP-LOCAL-${Date.now()}`,created_at:now(),
        source:{system:$('importSourceSystem').value.trim() || 'AUTHORIZED_EXPORT',record_id:$('importSourceRecord').value.trim() || file.name,
          owner_role:$('importOwnerRole').value,authority_class:authorityClass,
          transport:file.name.toLowerCase().endsWith('.csv') ? 'CSV' : 'JSON',source_uri:null,observed_at:null,original_sha256:await hashText(text)},
        asset:{candidate_id:$('candidateId').value.trim() || 'UNASSIGNED',unit_number:$('unitNumber').value.trim() || null,
          reporting_mark:null,donor_lineage:$('donorLineage').value},
        observations:buildObservations(records,$('importEvidenceClass').value),conflicts:[],
        custody_state:'BROWSER_LOCAL_UNCUSTODIED',execution_authority:false,
        history:[{timestamp:now(),actor:'gp10-evidence-import.js',action:'Parsed authorized browser-local export without source mutation'}]
      };
      packet.conflicts = detectInternalConflicts(packet.observations,authorityClass).concat(detectCrossPacketConflicts(packet));
      const packets = read(PACKETS_KEY); packets.unshift(packet); write(PACKETS_KEY,packets.slice(0,100));
      localStorage.setItem('gp10.workspace.import.latest',JSON.stringify(packet));
      const review = reviewFor(packet); if (review) { const reviews = read(REVIEWS_KEY); reviews.unshift(review); write(REVIEWS_KEY,reviews.slice(0,100)); }
      $('importPreview').textContent = JSON.stringify(packet,null,2);
      const reference = `external-evidence:${packet.packet_id}:${packet.source.original_sha256}`;
      if (!$('evidenceRefs').value.includes(reference)) $('evidenceRefs').value = [$('evidenceRefs').value.trim(),reference].filter(Boolean).join('\n');
      $('importStatus').textContent = `Imported ${packet.observations.length} observations; ${packet.conflicts.length} conflict(s). Source authority retained; no execution authority.`;
      renderQueue();
    } catch (error) { $('importStatus').textContent = `FAIL-CLOSED: ${error.message}`; }
  }
  function exportBundle() {
    let latest = null; try { latest = JSON.parse(localStorage.getItem(`${RECORDS_KEY}.latest`) || 'null'); } catch {}
    const bundle = {bundle_version:'1.0.0',exported_at:now(),custody_state:'BROWSER_LOCAL_UNCUSTODIED',execution_authority:false,
      latest_candidate_record:latest,evidence_packets:read(PACKETS_KEY),evidence_reviews:read(REVIEWS_KEY),warnings:['Export is not custody, approval, or execution authority.']};
    const blob = new Blob([JSON.stringify(bundle,null,2)],{type:'application/json'}); const link = document.createElement('a');
    link.href = URL.createObjectURL(blob); link.download = `gp10-validation-bundle-${now().slice(0,10)}.json`; link.click();
    setTimeout(() => URL.revokeObjectURL(link.href),1000); $('importStatus').textContent = 'Complete validation bundle exported.';
  }
  function installReviewUi() {
    const preview = $('importPreview'); if (!preview || $('exportValidationBundle')) return;
    const controls = document.createElement('div'); controls.className = 'actions'; controls.style.marginTop = '12px';
    controls.innerHTML = '<button class="sv-btn sv-btn-secondary" id="exportValidationBundle" type="button">Export complete validation bundle</button>';
    preview.insertAdjacentElement('afterend',controls);
    const heading = document.createElement('h3'); heading.textContent = 'Evidence review queue'; controls.insertAdjacentElement('afterend',heading);
    const queue = document.createElement('div'); queue.id = 'evidenceReviewQueue'; queue.className = 'workspace'; heading.insertAdjacentElement('afterend',queue);
    $('exportValidationBundle').addEventListener('click',exportBundle); renderQueue();
  }
  $('importEvidence')?.addEventListener('click',importFile);
  const latest = localStorage.getItem('gp10.workspace.import.latest'); if (latest && $('importPreview')) $('importPreview').textContent = latest;
  installReviewUi();
})();
